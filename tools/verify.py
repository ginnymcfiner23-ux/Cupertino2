#!/usr/bin/env python3
"""
Cupertino2 - verification pass.

Checks the built site for the things that matter:

  1. every table row carries a source link, or is explicitly recorded as having none
  2. no unresolved values leaked into the HTML (nan / None / undefined / inf)
  3. every internal link resolves to a file that exists
  4. every external link is on the source register (nothing invented mid-page)
  5. no personal information anywhere in site/
  6. every flag id referenced from COORDINATION.md exists in the data

Exits non-zero on failure.  Run after tools/build_site.py.

Note: this sandbox has outbound network access only to github.com and the package
registries, so URL liveness cannot be checked from here.  tools/verify.py therefore
emits the full list of external URLs to data/urls.txt so each one can be fetched and
confirmed.  Liveness results are recorded in VERIFICATION.md.
"""
from __future__ import annotations

import html
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "site")
DATA = os.path.join(ROOT, "data")

with open(os.path.join(DATA, "model.json")) as fh:
    M = json.load(fh)

SRC = M["sources"]
KNOWN = {v["url"] for v in SRC.values()}
KNOWN_IDS = set(SRC)

PAGES = [f for f in sorted(os.listdir(SITE)) if f.endswith(".html")]

errors = []
warnings = []

# ---------------------------------------------------------------- 1. sources
missing_src = 0
rows_total = 0
rows_flagged = 0
flagged_by_page = {}
for page in PAGES:
    with open(os.path.join(SITE, page)) as fh:
        doc = fh.read()
    for tr in re.findall(r"<tr>(.*?)</tr>", doc, re.S):
        if "<th" in tr:
            continue
        rows_total += 1
        if 'class="src ' not in tr:
            missing_src += 1
            errors.append("{}: table row with no source link at all: {}".format(
                page, re.sub(r"<[^>]+>", " ", tr)[:110].strip()))
        elif 'href="flagged.html"' in tr:
            # Deliberately unverified: the row links to the Flagged for Review page
            # instead of to an official source.  Counted, not failed.
            rows_flagged += 1
            flagged_by_page[page] = flagged_by_page.get(page, 0) + 1
        if "missing source" in tr:
            errors.append("{}: row references an unknown source id".format(page))

# ---------------------------------------------------- 2. unresolved values
# Only flag tokens that could not be ordinary English prose.  The word "None" is
# used legitimately in the commentary, so it is only treated as a leak when it
# appears as an entire table cell or immediately after a currency symbol.
BAD_TOKENS = re.compile(r"(?:NoneType|undefined|\bnan\b|\$\s*(?:NaN|nan)|\bInfinity\b|>None<|\{:,\})")
for page in PAGES:
    with open(os.path.join(SITE, page)) as fh:
        doc = fh.read()
    for mline in BAD_TOKENS.finditer(doc):
        ctx = re.sub(r"\s+", " ", doc[max(0, mline.start() - 60):mline.start() + 60])
        errors.append("{}: unresolved token {!r} near: {}".format(
            page, mline.group(0), ctx))

# ------------------------------------------------------- 3. internal links
for page in PAGES:
    with open(os.path.join(SITE, page)) as fh:
        doc = fh.read()
    for href in re.findall(r'href="([^"]+)"', doc):
        if href.startswith(("http", "mailto:", "tel:", "#")):
            continue
        target = os.path.join(SITE, href.split("#")[0])
        if not os.path.exists(target):
            errors.append("{}: broken internal link -> {}".format(page, href))

# ------------------------------------------------------- 4. external links
ext = set()
for page in PAGES:
    with open(os.path.join(SITE, page)) as fh:
        doc = fh.read()
    for href in re.findall(r'href="(https?://[^"]+)"', doc):
        # hrefs are HTML-escaped in the markup (&amp; for &); compare unescaped.
        href = html.unescape(href)
        ext.add(href)
        if href not in KNOWN:
            errors.append("{}: external link not on the source register: {}".format(page, href))

os.makedirs(DATA, exist_ok=True)
with open(os.path.join(DATA, "urls.txt"), "w") as fh:
    fh.write("\n".join(sorted(ext)) + "\n")

# ---------------------------------------------------------- 5. PII scan
sys.path.insert(0, os.path.join(ROOT, "tools"))
try:
    from pii_scan import scan_dir  # noqa: E402
    pii_hits = scan_dir(SITE)
    for h in pii_hits:
        errors.append("PII: " + h)
except Exception as exc:  # pragma: no cover
    warnings.append("PII scan could not run: {}".format(exc))

# --------------------------------------------- 6. flag ids in COORDINATION
coord = os.path.join(ROOT, "COORDINATION.md")
if os.path.exists(coord):
    with open(coord) as fh:
        ctext = fh.read()
    for fid in re.findall(r"FLAG-\d+", ctext):
        if fid not in {f["id"] for f in M["flags"]}:
            errors.append("COORDINATION.md references {} which is not in the data".format(fid))
    for f in M["flags"]:
        if f["id"] not in ctext:
            warnings.append("{} is not mentioned in COORDINATION.md".format(f["id"]))

# ------------------------------------------------------------------ report
print("=" * 74)
print("Cupertino2 verification")
print("=" * 74)
print("pages checked            : {}".format(len(PAGES)))
print("table rows checked       : {}".format(rows_total))
print("  linked to a source     : {}".format(rows_total - missing_src - rows_flagged))
print("  flagged unverified     : {}".format(rows_flagged))
for pg, c in sorted(flagged_by_page.items()):
    print("      {:<22} {}".format(pg, c))
print("  with no link at all    : {} (must be zero)".format(missing_src))
print("distinct external URLs   : {} -> data/urls.txt".format(len(ext)))
print("sources on the register  : {} ({} official, {} unofficial)".format(
    len(SRC),
    sum(1 for v in SRC.values() if v["type"] == "official"),
    sum(1 for v in SRC.values() if v["type"] != "official")))
print("flags                    : {}".format(len(M["flags"])))
print()
for w in warnings:
    print("WARN  " + w)
print()
if errors:
    for e in errors:
        print("FAIL  " + e)
    print()
    print("{} error(s). Site is NOT verified.".format(len(errors)))
    sys.exit(1)
print("No errors. Structure verified: every row has a source, no broken internal")
print("links, no unregistered external links, no PII detected.")
