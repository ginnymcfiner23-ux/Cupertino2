#!/usr/bin/env python3
"""Offline integrity checks for the static, privacy-safe GitHub Pages site."""
from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
HTML_FILES = sorted(ROOT.glob("*.html"))
ERRORS: list[str] = []


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: set[str] = set()
        self.duplicates: set[str] = set()
        self.links: list[tuple[str, str]] = []
        self.table_rows: list[tuple[int, bool]] = []
        self._in_row = False
        self._row_external_source = False
        self._row_has_cells = False
        self._row_is_data = False
        self._in_cell = False
        self._cell_is_header = False
        self._cell_has_external = False
        self._row_number = 0
        self.visible_text: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_dict = dict(attrs)
        element_id = attrs_dict.get("id")
        if element_id:
            if element_id in self.ids:
                self.duplicates.add(element_id)
            self.ids.add(element_id)

        if tag in {"a", "link", "script", "img"}:
            attribute = "href" if tag in {"a", "link"} else "src"
            url = attrs_dict.get(attribute)
            if url:
                self.links.append((tag, url))

        if tag == "a" and attrs_dict.get("target") == "_blank":
            rel = (attrs_dict.get("rel") or "").lower().split()
            if "noopener" not in rel:
                ERRORS.append(
                    "External link with target=_blank must use rel=noopener: "
                    f"{attrs_dict.get('href', '')}"
                )

        if tag == "tr":
            self._in_row = True
            self._row_external_source = False
            self._row_has_cells = False
            self._row_is_data = False
            self._row_number += 1
        elif tag in {"td", "th"} and self._in_row:
            self._in_cell = True
            self._cell_is_header = tag == "th"
            self._cell_has_external = False
            self._row_has_cells = True
            if tag == "td" or attrs_dict.get("scope") == "row":
                self._row_is_data = True
        elif tag == "a" and self._in_cell:
            href = attrs_dict.get("href", "") or ""
            if urlsplit(href).scheme in {"http", "https"}:
                self._cell_has_external = True

        if tag in {"script", "img"}:
            source = attrs_dict.get("src", "") or ""
            if source.startswith(("http://", "https://", "//")):
                ERRORS.append(
                    "External asset is not allowed for privacy/offline operation: "
                    f"{source}"
                )

    def handle_endtag(self, tag: str) -> None:
        if tag in {"td", "th"} and self._in_cell:
            if not self._cell_is_header and self._cell_has_external:
                self._row_external_source = True
            self._in_cell = False
        elif tag == "tr" and self._in_row:
            # Ignore thead header rows; validate only rows containing td or th[scope=row].
            if self._row_has_cells and self._row_is_data:
                self.table_rows.append((self._row_number, self._row_external_source))
            self._in_row = False

    def handle_data(self, data: str) -> None:
        if data.strip():
            self.visible_text.append(data)


def fail(message: str) -> None:
    ERRORS.append(message)


if not HTML_FILES:
    fail("No root-level HTML pages found.")

parsers: dict[Path, PageParser] = {}
for path in HTML_FILES:
    parser = PageParser()
    try:
        parser.feed(path.read_text(encoding="utf-8"))
        parser.close()
    except Exception as exc:  # pragma: no cover - diagnostic path
        fail(f"Could not parse {path.relative_to(ROOT)}: {exc}")
    parsers[path] = parser
    if parser.duplicates:
        fail(f"Duplicate id(s) in {path.relative_to(ROOT)}: {sorted(parser.duplicates)}")
    for row_number, has_source in parser.table_rows:
        if not has_source:
            fail(
                f"Data row {row_number} in {path.relative_to(ROOT)} "
                "has no direct external source link."
            )
    text = " ".join(parser.visible_text)
    if re.search(r"(?<![A-Za-z0-9§])\d{5}(?:-\d{4})?(?!\d)", text):
        fail(
            f"Possible postal code in visible text of {path.relative_to(ROOT)}; "
            "public pages must not expose ZIP codes."
        )

# Check relative files and same-page/cross-page fragments without network access.
for path, parser in parsers.items():
    for tag, href in parser.links:
        if href.startswith(("http://", "https://", "mailto:", "tel:", "data:", "javascript:")) or href.startswith("//"):
            if href.startswith("http://"):
                fail(f"Non-HTTPS external link in {path.relative_to(ROOT)}: {href}")
            continue
        parts = urlsplit(href)
        target_path = unquote(parts.path)
        if not target_path:
            resolved = path
        else:
            resolved = (path.parent / target_path).resolve()
            try:
                resolved.relative_to(ROOT)
            except ValueError:
                fail(f"Link escapes the repository in {path.relative_to(ROOT)}: {href}")
                continue
            if resolved.is_dir():
                resolved = resolved / "index.html"
        if not resolved.exists():
            fail(f"Broken local {tag} target in {path.relative_to(ROOT)}: {href}")
            continue
        if parts.fragment and resolved.suffix.lower() == ".html" and resolved in parsers:
            fragment = unquote(parts.fragment)
            if fragment not in parsers[resolved].ids:
                fail(
                    f"Missing fragment #{fragment} in {resolved.relative_to(ROOT)} "
                    f"(linked from {path.relative_to(ROOT)})."
                )

# External links are restricted to government or official investor-education domains.
ALLOWED_DOMAINS = (
    "irs.gov", "boe.ca.gov", "leginfo.legislature.ca.gov", "sco.ca.gov",
    "selfhelp.courts.ca.gov", "courts.ca.gov", "santaclaracounty.gov",
    "clerkrecorder.santaclaracounty.gov", "files.santaclaracounty.gov",
    "sf.gov", "sfpuc.gov", "cupertino.gov", "cpuc.ca.gov",
    "insurance.ca.gov", "investor.gov", "ftb.ca.gov", "cslb.ca.gov",
    "asr.santaclaracounty.gov",
)
for path, parser in parsers.items():
    for _tag, href in parser.links:
        parts = urlsplit(href)
        if parts.scheme not in {"http", "https"}:
            continue
        hostname = (parts.hostname or "").lower()
        if not any(hostname == domain or hostname.endswith("." + domain) for domain in ALLOWED_DOMAINS):
            fail(
                f"External link is outside the official-source allowlist in "
                f"{path.relative_to(ROOT)}: {href}"
            )

if ERRORS:
    print("Site checks failed:", file=sys.stderr)
    for error in ERRORS:
        print(f" - {error}", file=sys.stderr)
    sys.exit(1)

print(
    f"Site checks passed: {len(HTML_FILES)} pages; all data rows have a direct "
    "external official citation; all local files/fragments resolve; no visible "
    "ZIP codes; no external assets."
)
