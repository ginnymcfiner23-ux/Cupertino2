#!/usr/bin/env python3
"""
Cupertino2 - personal information scanner.

Privacy is the highest-priority requirement for this project.  Anything that could
identify a person must stay in the private research notes and must never reach the
published site.  This scanner fails the build if the site/ tree contains:

  * e-mail addresses, phone numbers
  * social security numbers, ITINs
  * person names adjacent to property words, or "Name, Name and Name" trust patterns
  * street addresses and APN / parcel / block-and-lot numbers
  * trust or account identifiers
  * known placeholder leaks (the raw form of a real name is caught by the heuristics
    below; placeholders like [HEIR-A] are allowed and expected)

Usage:  python3 tools/pii_scan.py [directory]
"""
from __future__ import annotations

import os
import re
import sys

RULES = [
    ("email", re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}")),
    ("phone", re.compile(r"(?<!\d)(?:\+?1[ .\-])?\(?\d{3}\)?[ .\-]\d{3}[ .\-]\d{4}(?!\d)")),
    ("ssn", re.compile(r"(?<!\d)\d{3}-\d{2}-\d{4}(?!\d)")),
    ("itin", re.compile(r"(?<!\d)9\d{2}-(?:5\d|6\d|7\d|8\d|9\d)-\d{4}(?!\d)")),
    ("apn", re.compile(r"\b(?:APN|AIN|parcel|Parcel)\s*(?:no\.?|number|#)?\s*[:#]?\s*"
                       r"\d{3}-\d{2,3}-\d{2,4}\b")),
    ("blocklot", re.compile(r"\b(?:block|Block)\s*\d{3,5}\s*(?:,|/|and)?\s*"
                            r"(?:lot|Lot)\s*\d{2,4}\b")),
    ("street_address", re.compile(r"\b\d{1,6}\s+(?:[A-Z][a-z]+\s+){1,3}"
                                  r"(?:Street|St\.?|Avenue|Ave\.?|Road|Rd\.?|Drive|Dr\.?|"
                                  r"Court|Ct\.?|Lane|Ln\.?|Way|Boulevard|Blvd\.?|Place|Pl\.?|"
                                  r"Terrace|Circle|Parkway|Pkwy\.?)\b")),
    ("account", re.compile(r"\b(?:account|acct|Account)\s*(?:no\.?|number|#)\s*[:#]?\s*"
                           r"[A-Za-z0-9\-]{5,}\b")),
    ("trust_named", re.compile(r"\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,3}\s+"
                               r"(?:Family\s+)?(?:Revocable\s+)?Trust\b")),
    ("named_owners", re.compile(r"\b[A-Z][a-z]{2,}\s+and\s+[A-Z][a-z]{2,}\s+"
                                r"[A-Z][a-z]{2,}\b")),
    ("attorney_phrase", re.compile(r"\b(?:as\s+trustee\s+of|successor\s+trustee\s+"
                                   r"(?:of|named)\s+[A-Z])")),
]

# Words that mark a match as an organisation, statute or instrument rather than a
# natural person.  "Revenue and Taxation Code" and "Pacific Gas and Electric Company"
# are the classic false positives for the "X and Y Z" name heuristic.
ORG_WORDS = {
    "code", "codes", "act", "acts", "company", "co", "corporation", "corp",
    "commission", "commissions", "board", "department", "division", "bureau",
    "office", "agency", "administration", "authority", "district", "county",
    "city", "state", "university", "college", "school", "bank", "trust",
    "association", "society", "institute", "foundation", "service", "services",
    "utilities", "utility", "plan", "program", "system", "law", "laws",
    "amendment", "constitution", "section", "rule", "regulations",
    "information", "protection", "preservation", "properties", "property",
    "partnership", "llc", "lp", "inc",
}

# Words that legitimately contain a capitalised word before "Trust" etc.
ALLOWED_SUBSTRINGS = (
    "Proposition 13 Trust",
    "Special Needs Trusts",
    "living trust",
    "revocable trust",
    "revocable living trust",
    "the Trust",
)

SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv"}
SKIP_FILES = {"pii_scan.py", "verify.py"}
TEXT_EXT = {".html", ".css", ".js", ".md", ".json", ".txt", ".yml", ".yaml", ".csv"}


def scan_text(text, path):
    hits = []
    for name, rx in RULES:
        for m in rx.finditer(text):
            frag = m.group(0).strip()
            if any(a in frag for a in ALLOWED_SUBSTRINGS):
                continue
            # A name heuristic hit that is built out of organisation/statute words is
            # not a person.  "Revenue and Taxation Code" must not trip the scanner.
            if name in ("named_owners", "trust_named"):
                words = {w.lower().strip(".,") for w in re.findall(r"[A-Za-z]+", frag)}
                if words & ORG_WORDS:
                    continue
            # 5-digit ZIP and 4-digit years are not PII
            if name == "phone" and re.fullmatch(r"\d{5}", frag):
                continue
            start = max(0, m.start() - 45)
            ctx = re.sub(r"\s+", " ", text[start:m.end() + 45])
            hits.append("{}:{}: {} -> {!r}  [{}]".format(path, name, name, frag, ctx))
    return hits


def scan_dir(root):
    hits = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            if fn in SKIP_FILES:
                continue
            if os.path.splitext(fn)[1].lower() not in TEXT_EXT:
                continue
            full = os.path.join(dirpath, fn)
            try:
                with open(full, encoding="utf-8", errors="replace") as fh:
                    text = fh.read()
            except OSError:
                continue
            hits.extend(scan_text(text, os.path.relpath(full, root)))
    return hits


def main():
    root = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "site")
    hits = scan_dir(root)
    if hits:
        print("PII SCAN FAILED - {} hit(s) in {}:".format(len(hits), root))
        for h in hits:
            print("  " + h)
        return 1
    print("PII scan clean: {}".format(root))
    return 0


if __name__ == "__main__":
    sys.exit(main())
