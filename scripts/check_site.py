#!/usr/bin/env python3
"""Dependency-free audit for the public static decision dashboard."""
from __future__ import annotations

from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
PAGES = sorted([*ROOT.glob("*.html"), *ROOT.glob("docs/*.html"), *ROOT.glob("pages/*.html")])
ALLOWED_EXTERNAL_HOSTS = {
    "www.boe.ca.gov", "boe.ca.gov", "www.irs.gov", "irs.gov",
    "www.sco.ca.gov", "sco.ca.gov", "leginfo.legislature.ca.gov",
    "legislature.ca.gov", "santaclara.courts.ca.gov", "www.courts.ca.gov",
    "courts.ca.gov", "www.sf.gov", "sf.gov", "sftreasurer.org",
    "www.sftreasurer.org", "clerkrecorder.santaclaracounty.gov",
    "controller.santaclaracounty.gov", "asr.santaclaracounty.gov",
    "dtac.santaclaracounty.gov", "payments.sccgov.org",
    "www.calwater.com", "calwater.com", "www.sfpuc.gov", "sfpuc.gov",
    "www.cpuc.ca.gov", "cpuc.ca.gov", "www.pge.com", "pge.com",
    "www.cslb.ca.gov", "cslb.ca.gov", "interactive.web.insurance.ca.gov",
    "www.insurance.ca.gov", "insurance.ca.gov", "www.ftb.ca.gov", "ftb.ca.gov",
}

class AuditParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.links: list[str] = []
        self.external: list[str] = []
        self.fragment_links: list[str] = []
        self.errors: list[str] = []
        self.ids: list[str] = []
        self.h1 = 0
        self.titles = 0
        self.forms = 0
        self.scripts = 0
        self.images = 0
        self.tables = 0
        self._table_depth = 0
        self._row: dict[str, bool] | None = None
        self._has_doc_type = False
        self._has_lang = False

    def handle_decl(self, decl: str) -> None:
        if decl.lower().startswith("doctype html"):
            self._has_doc_type = True

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_map = dict(attrs)
        if tag == "html" and attrs_map.get("lang"):
            self._has_lang = True
        if tag == "h1":
            self.h1 += 1
        if tag == "title":
            self.titles += 1
        if tag in {"form", "input", "textarea", "select", "button"}:
            self.forms += 1
        if tag == "script":
            self.scripts += 1
        if tag == "img":
            self.images += 1
        if attrs_map.get("id"):
            self.ids.append(attrs_map["id"] or "")
        if tag == "table":
            self._table_depth += 1
            self.tables += 1
        if tag == "tr" and self._table_depth:
            self._row = {"has_data": False, "has_official_link": False}
        if tag == "td" and self._row is not None:
            self._row["has_data"] = True
        if tag in {"a", "link", "script", "img"}:
            key = "href" if tag in {"a", "link"} else "src"
            href = attrs_map.get(key)
            if href:
                self.links.append(href)
                if href.startswith("https://"):
                    self.external.append(href)
                    if self._row is not None and self._table_depth:
                        self._row["has_official_link"] = True
                    host = (urlparse(href).hostname or "").lower()
                    if host not in ALLOWED_EXTERNAL_HOSTS:
                        self.errors.append(f"non-approved external host: {host} ({href})")
                elif href.startswith("http:") or href.startswith("//"):
                    self.errors.append(f"non-HTTPS external link: {href}")
                elif tag == "a" and not href.startswith(("mailto:", "tel:")):
                    self.fragment_links.append(href)
                if tag == "a" and attrs_map.get("target") == "_blank":
                    rel = set((attrs_map.get("rel") or "").lower().split())
                    if "noopener" not in rel:
                        self.errors.append(f"target=_blank link missing rel=noopener: {href}")

    def handle_endtag(self, tag: str) -> None:
        if tag == "tr" and self._row is not None:
            if self._row["has_data"] and not self._row["has_official_link"]:
                self.errors.append("factual table row has no official HTTPS source link")
            self._row = None
        if tag == "table" and self._table_depth:
            self._table_depth -= 1


def main() -> int:
    errors: list[str] = []
    if not PAGES:
        print("ERROR: no root HTML pages found")
        return 1

    parsed: dict[Path, AuditParser] = {}
    for page in PAGES:
        parser = AuditParser()
        parser.feed(page.read_text(encoding="utf-8"))
        parser.close()
        parsed[page.resolve()] = parser
        label = page.relative_to(ROOT)
        if not parser._has_doc_type:
            errors.append(f"{label}: missing HTML doctype")
        if not parser._has_lang:
            errors.append(f"{label}: missing document language")
        if parser.h1 != 1:
            errors.append(f"{label}: expected exactly one h1, found {parser.h1}")
        if parser.titles != 1:
            errors.append(f"{label}: expected exactly one title, found {parser.titles}")
        if parser.forms:
            errors.append(f"{label}: forms/inputs are not allowed in the public site")
        if parser.scripts:
            errors.append(f"{label}: scripts are not allowed in the public site")
        if parser.images:
            errors.append(f"{label}: external or unreviewed images are not allowed")
        duplicate_ids = [name for name, count in Counter(parser.ids).items() if count > 1]
        if duplicate_ids:
            errors.append(f"{label}: duplicate id(s): {', '.join(duplicate_ids)}")
        errors.extend(f"{label}: {error}" for error in parser.errors)
        print(f"OK {label}: {parser.tables} tables, {len(parser.external)} official HTTPS links")

    # Verify file links and in-page / cross-page fragments.
    for page in PAGES:
        parser = parsed[page.resolve()]
        label = page.relative_to(ROOT)
        for href in parser.fragment_links:
            raw_path, _, fragment = href.partition("#")
            raw_path = raw_path.split("?", 1)[0]
            if raw_path:
                target = (page.parent / unquote(raw_path)).resolve()
            else:
                target = page.resolve()
            if not target.exists():
                errors.append(f"{label}: broken internal link {href}")
                continue
            if fragment and target.suffix.lower() == ".html":
                target_parser = parsed.get(target)
                if target_parser is None:
                    target_parser = AuditParser()
                    target_parser.feed(target.read_text(encoding="utf-8"))
                    target_parser.close()
                if unquote(fragment) not in target_parser.ids:
                    errors.append(f"{label}: missing anchor {href}")

    if not (ROOT / "assets" / "site.css").is_file():
        errors.append("missing assets/site.css")
    if not (ROOT / ".nojekyll").exists():
        errors.append("missing .nojekyll for the static root site")

    # Exact postal codes are not part of this public site. The decimal form avoids
    # misclassifying statutory references such as Probate Code §16061.7.
    postal_re = re.compile(r"\b\d{5}(?:-\d{4})?\b(?!\.\d)")
    public_files = [
        *PAGES,
        ROOT / "README.md",
        ROOT / "COORDINATION.md",
        *sorted((ROOT / "data").glob("*.json")),
        *sorted((ROOT / "data").glob("*.csv")),
        *sorted((ROOT / "scripts").glob("*.py")),
    ]
    for path in public_files:
        content = path.read_text(encoding="utf-8")
        if postal_re.search(content):
            errors.append(f"{path.relative_to(ROOT)}: possible exact postal code in public content")

    # Keep structured data useful for public facts while refusing private inputs or projections.
    data_dir = ROOT / "data"
    sources_path = data_dir / "sources.json"
    source_ids: set[str] = set()
    try:
        source_records = json.loads(sources_path.read_text(encoding="utf-8")).get("sources", [])
        source_ids = {record.get("id", "") for record in source_records}
        if len(source_ids) != len(source_records):
            errors.append("data/sources.json: duplicate or blank source IDs")
        for record in source_records:
            url = record.get("url", "")
            parsed_url = urlparse(url)
            if parsed_url.scheme != "https" or (parsed_url.hostname or "").lower() not in ALLOWED_EXTERNAL_HOSTS:
                errors.append(f"data/sources.json: unapproved source URL {url}")
    except (OSError, json.JSONDecodeError, AttributeError) as exc:
        errors.append(f"data/sources.json: cannot read source registry ({exc})")

    for name in ("facts.json", "flagged.json", "property_history.json"):
        path = data_dir / name
        try:
            document = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"data/{name}: invalid JSON ({exc})")
            continue
        rows = document.get("rows", document.get("items", []))
        if not isinstance(rows, list):
            errors.append(f"data/{name}: expected a list of rows/items")
            continue
        for row in rows:
            missing = set(row.get("sources", [])) - source_ids
            if missing:
                errors.append(f"data/{name}: unknown source IDs {sorted(missing)}")
            if name == "property_history.json" and row.get("value") not in (None, ""):
                errors.append("data/property_history.json: property-specific values must remain blank")

    decision_path = data_dir / "decision.json"
    try:
        decision = json.loads(decision_path.read_text(encoding="utf-8"))
        if decision.get("decisions") or decision.get("assumptions"):
            errors.append("data/decision.json: private scenario inputs and outputs must not be stored")
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"data/decision.json: invalid JSON ({exc})")

    for name in ("projections_base.csv", "sensitivity.csv"):
        path = data_dir / name
        try:
            rows = [line for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
            if len(rows) > 1:
                errors.append(f"data/{name}: projection data rows must not be stored publicly")
        except OSError as exc:
            errors.append(f"data/{name}: cannot read file ({exc})")

    if errors:
        print("\nAUDIT FAILED")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"\nAUDIT PASSED: {len(PAGES)} HTML pages; internal links/anchors resolve; no forms, scripts, images, exact postal codes, or unlinked table rows.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
