#!/usr/bin/env python3
"""One-shot gap-fill by session arena-55de235e (T202).

Adds sources retrieved during the re-verification pass, upgrades fact rows
that earlier sessions could not confirm, restores the full owner-provided
assessment history (all years supplied in the original request), resolves
the corresponding flags, and updates build_site.py page copy.

Idempotent-ish: refuses to run if a source id it would add already exists
with a different URL.
"""
import json
import os

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
D = os.path.join(ROOT, "data")

NEW_SOURCES = [
    {"id": "CRS-ESTATE-R48183", "type": "official", "publisher": "Congressional Research Service (congress.gov)",
     "title": "The Estate and Gift Tax: An Overview (CRS R48183, updated 07/14/2025)",
     "url": "https://www.congress.gov/crs-product/R48183",
     "supports": "Estate tax rate on the taxable portion is 40%; $15M basic exclusion for 2026 (P.L. 119-21), indexed; about 0.07% of decedents owe the tax (2019); couple combined exclusion $30M in 2026 with portability"},
    {"id": "IRS-NIIT-QA", "type": "official", "publisher": "Internal Revenue Service",
     "title": "Questions and Answers on the Net Investment Income Tax",
     "url": "https://www.irs.gov/newsroom/questions-and-answers-on-the-net-investment-income-tax",
     "supports": "NIIT rate 3.8%; thresholds $200,000 single / $250,000 MFJ / $125,000 MFS, not indexed for inflation; includes rental income and gain on sale of a second home that is not a principal residence; gain excluded under IRC §121 on a principal residence is not subject"},
    {"id": "FTB-ESTATE-TAX-ANALYSIS", "type": "official", "publisher": "California Franchise Tax Board",
     "title": "FTB analysis of SB 378 (2019) — California Estate & Gift Taxes",
     "url": "https://www.ftb.ca.gov/tax-pros/law/legislation/2019-2020/SB378-032519.pdf",
     "supports": "Highest estate and gift tax rate is 40 percent; California does not conform to federal estate/GST tax and its estate 'pick-up' tax equals the repealed federal credit, i.e., zero; estate tax generally due within nine months of death"},
    {"id": "FTB-CA-2026-RATES", "type": "official", "publisher": "California Franchise Tax Board",
     "title": "2026 California Tax Rate Schedules (Schedule X, single or married/RDP filing separately)",
     "url": "https://www.ftb.ca.gov/forms/2026/2026-540-tax-rate-schedules.pdf",
     "supports": "2026 single-filer marginal rates 1%–12.3%: 9.3% on $75,197–$384,109; 12.3% above $768,213"},
    {"id": "CDI-RESIDENTIAL-REPORT", "type": "official", "publisher": "California Department of Insurance",
     "title": "Residential Property Insurance Report — Part I studies and data (2008–2023)",
     "url": "https://www.insurance.ca.gov/0400-news/0200-studies-reports/0250-homeowners-study/",
     "supports": "Part I data summary: statewide average written premium by coverage type (Homeowners multi-peril $1,176; tenant/multi-family $601; condo $537; renters $190 over 2008–2023)"},
    {"id": "CDI-SB824-DATA", "type": "official", "publisher": "California Department of Insurance",
     "title": "SB 824 report — Residential Property Coverage Amounts, Wildfire Risk and Losses (data workbook)",
     "url": "https://www.insurance.ca.gov/01-consumers/200-wrr/WildfireRiskInfoRpt.cfm",
     "supports": "2023 statewide totals: $14.22B earned premium ÷ 12.58M policy-years = $1,130 average earned premium per residential policy (computed from published totals); average Coverage A (main structure) $324,973"},
    {"id": "SCC-TAX-RATE-BOOK", "type": "official", "publisher": "Santa Clara County Controller",
     "title": "FY 2025-26 Property Tax Rate Book",
     "url": "https://controller.santaclaracounty.gov/property-tax-distribution/property-tax-rate-book",
     "supports": "Total rate = 1.000% base rate plus voter-approved debt, set by Tax Rate Area; example TRA totals in the book range 1.12580%–1.24090% for FY 2025-26"},
    {"id": "LEGINFO-AB1482", "type": "official", "publisher": "California Legislature (leginfo)",
     "title": "AB 1482 Tenant Protection Act (2019, Chapter 597) — bill text",
     "url": "https://www.leginfo.legislature.ca.gov/faces/billTextClient.xhtml?bill_id=201920200AB1482",
     "supports": "Statewide rent increase cap: 5% + local CPI, or 10%, whichever is lower; no more than two increases in 12 months; sunsets Jan 1, 2030; single-family owner-occupied homes (owner rents no more than two units) exempt"},
    {"id": "LEGINFO-SB284", "type": "official", "publisher": "California Legislature (leginfo)",
     "title": "SB 284 (2025-26) — status",
     "url": "https://leginfo.legislature.ca.gov/faces/billStatusClient.xhtml?bill_id=202520260SB284",
     "supports": "Would extend the Proposition 19 family-home/farm transfer exclusion to specified eligible transferees; active bill held in Assembly committee (last action 7/14/2025); not law"},
    {"id": "CONGRESS-S587", "type": "official", "publisher": "congress.gov (Library of Congress)",
     "title": "S.587 Death Tax Repeal Act of 2025 (119th Congress)",
     "url": "https://www.congress.gov/bill/119th-congress/senate-bill/587",
     "supports": "Introduced 02/13/2025; read twice and referred to Senate Finance; status: Introduced — not law"},
    {"id": "FHFA-HPI-2026Q2", "type": "official", "publisher": "Federal Housing Finance Agency",
     "title": "FHFA House Price Index Report 2026Q2",
     "url": "https://www.fhfa.gov/document/d/hpi/fhfa-house-price-index-report-2026q2",
     "supports": "California purchase-only HPI: −0.20% over 12 months; +17.31% over 5 years; +317.15% since 1991Q1 (≈4.1%/yr, computed)"},
    {"id": "FRED-SP500", "type": "official", "publisher": "Federal Reserve Bank of St. Louis (FRED)",
     "title": "S&P 500 Index (FRED daily series SP500)",
     "url": "https://fred.stlouisfed.org/series/SP500",
     "supports": "2,131.52 (2016-11-07) → 7,688.62 (2026-11-04); 10-year change ≈13.7% per year (computed from the official series; past performance, not a forecast)"},
    {"id": "FRED-GS10", "type": "official", "publisher": "Federal Reserve Bank of St. Louis (FRED)",
     "title": "10-Year Treasury Constant Maturity Rate (FRED GS10)",
     "url": "https://fred.stlouisfed.org/series/GS10",
     "supports": "5.13% (observation 2026-10-01)"},
    {"id": "CPUC-SOLAR-GUIDE", "type": "official", "publisher": "California Public Utilities Commission",
     "title": "California Solar Consumer Protection Guide",
     "url": "https://www.cpuc.ca.gov/-/media/cpuc-website/divisions/energy-division/documents/solar-guide/solarguide22_011922.pdf",
     "supports": "PG&E, SCE and SDG&E customers are guaranteed net energy metering for 20 years from installation; excess annual generation is paid as net surplus compensation of about 2–3 cents per kWh"},
    {"id": "SCC-COURTS-TRUST", "type": "official", "publisher": "Superior Court of California, County of Santa Clara",
     "title": "Probate — Trusts (trustee duties after the settlor dies)",
     "url": "https://santaclara.courts.ca.gov/divisions/probate-division/probate-trusts",
     "supports": "Successor trustee: Acceptance/Certification of Trust (Prob. Code §18100.5); written notice to beneficiaries and heirs within 60 days (Prob. Code §16061.7); written notice to the county Assessor within 150 days of death (R&TC §480(b)); inventory and date-of-death valuation; estate tax returns and payment within 9 months; trust EIN"},
]

# ---------------------------------------------------------------- facts edits
def load(name):
    with open(os.path.join(D, name), encoding="utf-8") as f:
        return json.load(f)

def save(name, obj):
    with open(os.path.join(D, name), "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)
        f.write("\n")

src = load("sources.json")
by_id = {s["id"]: s for s in src["sources"]}
for s in NEW_SOURCES:
    if s["id"] in by_id:
        if by_id[s["id"]]["url"] != s["url"]:
            raise SystemExit(f"source id conflict: {s['id']}")
        continue
    src["sources"].append(s)
src["accessed"] = "2026-11-06"
save("sources.json", src)

facts = load("facts.json")
rows = facts["rows"]

def find(sub):
    hits = [r for r in rows if sub in r["label"]]
    if len(hits) != 1:
        raise SystemExit(f"fact match failed for {sub!r}: {len(hits)} hits")
    return hits[0]

# Top federal estate rate -> verified
r = find("Top federal estate tax rate")
r["value"] = "40% of the taxable estate above the exclusion"
r["status"] = "verified"
r["sources"] = ["FTB-ESTATE-TAX-ANALYSIS", "CRS-ESTATE-R48183"]
r["notes"] = ("Confirmed 2026-11-06: FTB analysis ('The highest estate and gift tax rate is 40 percent') "
              "and CRS R48183 ('The estate tax rate on the taxable portion of the estate, if any, is 40%'). "
              "Prior flag X16 resolved.")

# NIIT -> verified
r = find("Net investment income tax")
r["value"] = "3.8% on the lesser of net investment income or MAGI over $200,000 (single) / $250,000 (MFJ)"
r["status"] = "verified"
r["sources"] = ["IRS-NIIT-QA"]
r["notes"] = ("IRS NIIT Q&A: thresholds not indexed for inflation; income includes rental and royalty income "
              "and gain on the sale of a second home that is not a principal residence; gain excluded under "
              "IRC §121 on a principal residence is not subject. Flag X19 resolved 2026-11-06.")

# 2026 exclusion: add couple/portability note + CRS source
r = find("Federal estate & gift basic exclusion amount")
if "CRS-ESTATE-R48183" not in r["sources"]:
    r["sources"].append("CRS-ESTATE-R48183")
r["notes"] = ("Per person; with portability of the deceased spouse's unused exclusion a couple can combine to "
              "$30,000,000 in 2026 (CRS R48183). Annual gifts up to $19,000 per donee (2026) do not use it.")

# Prop 19 residence conditions -> explicit windows
r = find("Prop 19 family-home exclusion conditions")
r["value"] = ("Heir must occupy as principal residence within 1 year of transfer and claim the Homeowners' "
              "Exemption (Form BOE-266) within 1 year; file exclusion claim (Form BOE-19-P) within 3 years")
r["notes"] = ("Family home = dwelling eligible for homeowners' or disabled veterans' exemption from the "
              "transferor's ownership and occupancy. Rental homes are not eligible. Filing windows per BOE "
              "Prop 19 checklist (verified 2026-11-06).")

# CPI -> verified on BLS release
r = find("U.S. CPI, 12-month change")
r["value"] = "3.7% (12 months ending September 2026)"
r["status"] = "verified"
r["notes"] = ("BLS news release USDL-26-1574 fetched 2026-11-06: CPI-U +3.7% over 12 months; core (less food "
              "and energy) +2.6%; electricity +4.4%. Flag X20 resolved.")

# CA income tax brackets -> verified on FTB 2026 schedules
r = find("California personal income tax brackets")
r["value"] = ("2026 Schedule X (single): 1% up to $11,456; 9.3% on $75,197–$384,109; "
              "12.3% above $768,213 (marginal rates 1%–12.3%)")
r["status"] = "verified"
r["sources"] = ["FTB-CA-2026-RATES"]
r["notes"] = "FTB 2026 California Tax Rate Schedules retrieved 2026-11-06. Flag X17 resolved."

# CA estate/inheritance tax -> verified none
r = find("California estate or inheritance tax")
r["value"] = ("None — California does not conform to the federal estate/GST tax; the state estate "
              "'pick-up' tax equals the repealed federal credit, i.e., $0")
r["status"] = "verified"
r["sources"] = ["FTB-ESTATE-TAX-ANALYSIS"]
r["notes"] = ("FTB: 'Because the federal estate tax credit was repealed, the state's pick-up tax is zero.' "
              "No California inheritance tax either. Flag X18 resolved 2026-11-06.")

NEW_FACTS = [
    {"id": "F-ESTATE-COVERAGE", "category": "federal",
     "label": "Share of U.S. decedents who owe federal estate tax",
     "value": "About 0.07% (2019 year-of-death data)",
     "status": "verified", "sources": ["CRS-ESTATE-R48183"],
     "notes": "CRS R48183: declined from 2.1% of the population (2001) to 0.07% (2019). Context for how rarely the tax applies."},
    {"id": "F-COUPLE-EXCLUSION", "category": "federal",
     "label": "Combined federal estate & gift basic exclusion for a couple with portability, 2026",
     "value": "$30,000,000 ($15M each, including the deceased spouse's unused exclusion)",
     "status": "verified", "sources": ["CRS-ESTATE-R48183", "IRS-ESTATE-TAX"],
     "notes": "Portability requires a timely filed Form 706 for the first spouse to die (IRS)."},
    {"id": "F-AB1482", "category": "legislation",
     "label": "AB 1482 statewide rent cap (California Tenant Protection Act)",
     "value": "5% + CPI or 10% max per 12 months (lower of the two), max two increases/year; sunsets Jan 1, 2030",
     "status": "verified", "sources": ["LEGINFO-AB1482"],
     "notes": "Applies to a Property A rental while the heir lives elsewhere; owner-occupied single-family homes renting no more than two units are exempt. SF covered units also follow SF Rent Board rules."},
    {"id": "F-SB284", "category": "legislation",
     "label": "CA SB 284 (2025-26): extend Prop 19 family-home/farm exclusion to eligible transferees",
     "value": "Active bill, not law — held in Assembly committee (last action July 14, 2025)",
     "status": "verified", "sources": ["LEGINFO-SB284"],
     "notes": "Would change who can use the intergenerational exclusion. Watch status."},
    {"id": "F-S587", "category": "legislation",
     "label": "S.587 Death Tax Repeal Act of 2025 (119th Congress)",
     "value": "Introduced Feb 13, 2025; referred to Senate Finance; not law",
     "status": "verified", "sources": ["CONGRESS-S587"],
     "notes": "Would repeal the federal estate and GST taxes. Companion bill H.R. 1301 in the House. Neither enacted as of 2026-11-06."},
    {"id": "F-SCC-TRA", "category": "local",
     "label": "Santa Clara County total property tax rate structure (FY 2025-26)",
     "value": "1.000% base rate + voter-approved debt by Tax Rate Area; example TRA totals 1.12580%–1.24090%",
     "status": "verified", "sources": ["SCC-TAX-RATE-BOOK"],
     "notes": "Exact TRA for Property A needs a parcel lookup (kept off-site for privacy). Owner-billed totals imply 1.32%–1.41% — see flags X04/X06."},
]
have = {r["id"] for r in rows}
for nf in NEW_FACTS:
    if nf["id"] not in have:
        rows.append(nf)
facts["rows"] = rows
save("facts.json", facts)

# ---------------------------------------------------------------- flagged edits
flags = load("flagged.json")
items = flags["items"]

def fget(fid):
    hits = [i for i in items if i["id"] == fid]
    if len(hits) != 1:
        raise SystemExit(f"flag {fid} not unique")
    return hits[0]

i = fget("X01")
i["item"] = ("Owner-provided assessment history RESTORED in full on 2026-11-06 (arena-55de235e): "
             "Property A 2014–2026 and Property B 2016–2025, values and owner-reported YoY %, exactly as "
             "supplied. Still unverified against assessor records. Irregularities as supplied: Property A tax "
             "repeats in 2017–18 ($6,383) and 2019–20 ($6,565) despite AV growth; Property A 2026 tax not "
             "provided (left blank).")
i["action"] = "Check each year against the assessor's roll (portal links on the Property tax page)."

i = fget("X04")
i["item"] = ("Owner-provided Property B taxes imply 1.73% (2016) to 2.13% (2025) of assessed value, above the "
             "official FY2026-27 SF secured rate of 1.18162182%. For 2025 the gap is ~$1,089/yr, treated as "
             "non-ad-valorem charges. Computed checks on all supplied years are shown in the history table.")
i["action"] = "Compare the bill's line items with the Treasurer's rate."

i = fget("X06")
i["item"] = ("Property A implied effective rate is 1.32%–1.41% across 2014–2025 (1.3352% in 2025), computed "
             "from owner-provided tax ÷ AV. County TRA examples in the FY2025-26 rate book are 1.12580%–1.24090%; "
             "no official composite rate for this parcel was verified.")
i["action"] = "Use the Santa Clara County tax bill's composite rate (1% + voter debt) to verify."

i = fget("X14")
i["item"] = ("Insurance figures ($1,500/yr each) are owner estimates and remain unverified for these properties. "
             "Statewide official benchmarks now attached: CDI Part I average Homeowners multi-peril written "
             "premium $1,176 per policy-year (2008–2023); 2023 average earned premium $1,130 and average "
             "Coverage A $324,973 (SB 824 workbook).")
i["action"] = "Obtain property-specific quotes; compare with the CDI statewide benchmarks linked here."
i["sources"] = ["CDI-HOME", "CDI-RESIDENTIAL-REPORT", "CDI-SB824-DATA"]

i = fget("X16")
i["type"] = "Resolved 2026-11-06"
i["item"] = ("RESOLVED (arena-55de235e): top federal estate tax rate confirmed at 40% of the taxable estate "
             "above the exclusion — FTB analysis ('The highest estate and gift tax rate is 40 percent') and "
             "CRS R48183 ('The estate tax rate on the taxable portion of the estate, if any, is 40%').")
i["action"] = "None; figure now sourced (kept in the list for the audit trail)."
i["sources"] = ["FTB-ESTATE-TAX-ANALYSIS", "CRS-ESTATE-R48183"]

i = fget("X17")
i["type"] = "Resolved 2026-11-06"
i["item"] = ("RESOLVED (arena-55de235e): California 2026 income tax brackets confirmed on FTB's 2026 Tax Rate "
             "Schedules (Schedule X: 1%–12.3%; 9.3% bracket $75,197–$384,109; 12.3% above $768,213).")
i["action"] = "None; figure now sourced."
i["sources"] = ["FTB-CA-2026-RATES"]

i = fget("X18")
i["type"] = "Resolved 2026-11-06"
i["item"] = ("RESOLVED (arena-55de235e): no California estate or inheritance tax — FTB: California's estate "
             "'pick-up' tax equals the repealed federal credit, so 'the state's pick-up tax is zero'.")
i["action"] = "None; figure now sourced."
i["sources"] = ["FTB-ESTATE-TAX-ANALYSIS"]

i = fget("X19")
i["type"] = "Resolved 2026-11-06"
i["item"] = ("RESOLVED (arena-55de235e): NIIT confirmed on the IRS NIIT Q&A — 3.8%; thresholds $200,000 single / "
             "$250,000 MFJ / $125,000 MFS, not indexed; includes rental income and gains on a second home that "
             "is not a principal residence.")
i["action"] = "None; figure now sourced."
i["sources"] = ["IRS-NIIT-QA"]

i = fget("X20")
i["type"] = "Resolved 2026-11-06"
i["item"] = ("RESOLVED (arena-55de235e): BLS CPI release fetched — CPI-U +3.7% over the 12 months ending "
             "September 2026 (core +2.6%; electricity +4.4%).")
i["action"] = "None; figure now sourced."
i["sources"] = ["BLS-CPI"]

i = fget("X11")
if "CPUC-SOLAR-GUIDE" not in i["sources"]:
    i["sources"].append("CPUC-SOLAR-GUIDE")
i["item"] = (i["item"] + " CPUC guide context: NEM is guaranteed for 20 years and surplus annual generation is "
             "paid ≈2–3¢/kWh, so a $10–20/mo net credit depends on system size and usage (owner's figure still "
             "needs the bill).")

save("flagged.json", flags)

# ---------------------------------------------------- property history restore
A_TAX = {2014: (5965, None), 2015: (6130, "+2.8%"), 2016: (6414, "+4.6%"), 2017: (6383, "\u22120.5%"),
         2018: (6383, None), 2019: (6565, "+2.8%"), 2020: (6565, None), 2021: (6662, "+1.5%"),
         2022: (6755, "+1.4%"), 2023: (6917, "+2.4%"), 2024: (7003, "+1.2%"), 2025: (7207, "+2.9%"),
         2026: (None, None)}
A_AV = {2014: (440305, "+0.5%"), 2015: (449101, "+2%"), 2016: (455949, "+1.5%"), 2017: (465067, "+2%"),
        2018: (474368, "+2%"), 2019: (483854, "+2%"), 2020: (493530, "+2%"), 2021: (498642, "+1%"),
        2022: (508614, "+2%"), 2023: (518786, "+2%"), 2024: (529161, "+2%"), 2025: (539743, "+2%"),
        2026: (550537, "+2%")}
B_TAX = {2016: (1675, "+1.6%"), 2017: (1740, "+3.9%"), 2018: (2061, "+18.4%"), 2019: (2134, "+3.5%"),
         2020: (2197, "+3%"), 2021: (2066, "\u22125.9%"), 2022: (2107, "+2%"), 2023: (2179, "+3.4%"),
         2024: (2315, "+6.2%"), 2025: (2439, "+5.3%")}
B_AV = {2016: (96557, "+1.5%"), 2017: (98488, "+2%"), 2018: (100456, "+2%"), 2019: (102465, "+2%"),
        2020: (104513, "+2%"), 2021: (105595, "+1%"), 2022: (107662, "+2%"), 2023: (109814, "+2%"),
        2024: (112008, "+2%"), 2025: (114248, "+2%")}

ph = load("property_history.json")
existing = {}
for r in ph["rows"]:
    existing[(r["property"], r["year"], r["metric"])] = r

def yoy_note(yoy, extra=""):
    base = f"Owner-reported YoY: {yoy}." if yoy else "Owner did not report a YoY change for this year."
    return (base + " " + extra).strip()

new_rows = []
for y in range(2014, 2027):
    val, yoy = A_TAX[y]
    ex = existing.get(("A", y, "Property tax (total billed)"))
    notes = yoy_note(yoy)
    if y == 2018:
        notes += " Tax equals 2017 as supplied although AV rose 2% (irregularity, as given)."
    if y == 2020:
        notes += " Tax equals 2019 as supplied although AV rose 2% (irregularity, as given)."
    if val is not None and A_AV[y][0]:
        notes += f" Implied tax÷AV = {val / A_AV[y][0] * 100:.2f}% (computed)."
    if ex and ex.get("notes"):
        notes = ex["notes"] + " " + notes
    new_rows.append({"property": "A", "city": "Cupertino, CA", "year": y,
                     "metric": "Property tax (total billed)", "value": val, "unit": "USD",
                     "status": ("blank — not provided" if val is None else "user-provided — unverified"),
                     "sources": ["SCC-ASSESSOR"],
                     "notes": notes if val is not None else "Left blank; not supplied by the owner."})
    av, yoy_av = A_AV[y]
    ex = existing.get(("A", y, "Assessed value (AV)"))
    notes = yoy_note(yoy_av)
    if y == 2026:
        notes = "Owner-reported YoY: +2%, consistent with the 2% Prop 13 cap (computed check, not an official figure)."
    if ex and ex.get("notes") and y != 2026:
        notes = ex["notes"] + " " + notes
    new_rows.append({"property": "A", "city": "Cupertino, CA", "year": y,
                     "metric": "Assessed value (AV)", "value": av, "unit": "USD",
                     "status": "user-provided — unverified",
                     "sources": ["SCC-ASSESSOR", "BOE-LTA-2009-036"] if y == 2026 else ["SCC-ASSESSOR"],
                     "notes": notes})

for y in range(2016, 2026):
    val, yoy = B_TAX[y]
    ex = existing.get(("B", y, "Property tax (total billed)"))
    notes = yoy_note(yoy) + f" Implied tax÷AV = {val / B_AV[y][0] * 100:.2f}% (computed)."
    if ex and ex.get("notes"):
        notes = ex["notes"] + " " + notes
    new_rows.append({"property": "B", "city": "San Francisco, CA", "year": y,
                     "metric": "Property tax (total billed)", "value": val, "unit": "USD",
                     "status": "user-provided — unverified",
                     "sources": ["SF-TREASURER-SECURED"], "notes": notes})
    av, yoy_av = B_AV[y]
    notes = yoy_note(yoy_av)
    ex = existing.get(("B", y, "Assessed value (AV)"))
    if ex and ex.get("notes"):
        notes = ex["notes"] + " " + notes
    new_rows.append({"property": "B", "city": "San Francisco, CA", "year": y,
                     "metric": "Assessed value (AV)", "value": av, "unit": "USD",
                     "status": "user-provided — unverified",
                     "sources": ["SF-ASSESSOR"], "notes": notes})

ph["rows"] = new_rows
ph["note"] = ("Owner-provided values, exactly as supplied in the request (values and YoY %); anonymized to city. "
              "None checked against an official assessor record (no parcel identifier is published). Rows are "
              "flagged 'user-provided — unverified'. Per-year implied tax÷AV ratios are computed for review. "
              "Official lookup: Santa Clara County Assessor (Property A) and SF Assessor-Recorder (Property B).")
save("property_history.json", ph)

# ------------------------------------------------------------- build_site.py
p = os.path.join(ROOT, "scripts", "build_site.py")
s = open(p, encoding="utf-8").read()

def rep(old, new):
    global s
    if old not in s:
        raise SystemExit(f"build_site.py: pattern not found:\n{old[:120]}")
    s = s.replace(old, new, 1)

# 1. property-tax page: notes column + restored-history caption
rep('''    rows = []
    for r in PHIST:
        rows.append([
            f"Property {r['property']} · {r['city']}",
            r["year"],
            r["metric"],
            money(r["value"]) if r["value"] is not None else "blank",
            status_badge(r["status"]),
            r["sources"],
        ])
    hist = table(["Property", "Year", "Metric", "Value", "Status", ], [r[:5] + [r[5]] for r in rows], "property-history", "Owner-provided assessment history (retained records; flagged)")''',
'''    rows = []
    for r in PHIST:
        rows.append([
            f"Property {r['property']} · {r['city']}",
            r["year"],
            r["metric"],
            money(r["value"]) if r["value"] is not None else "blank",
            status_badge(r["status"]),
            esc(r.get("notes") or "—"),
            r["sources"],
        ])
    hist = table(["Property", "Year", "Metric", "Value", "Status", "Notes"],
                 [r[:6] + [r[6]] for r in rows], "property-history",
                 "Owner-provided assessment history, complete as supplied (Property A 2014–2026; Property B "
                 "2016–2025): values and owner-reported YoY % are unverified; each tax row shows the computed "
                 "implied tax÷AV ratio (A 1.32%–1.41%, B 1.73%–2.13% vs official SF rate 1.18162182% and "
                 "county TRA examples 1.126%–1.241% — flags X04/X06). Property A tax repeats in 2017–18 and "
                 "2019–20 as supplied.")''')

# 2. index "what to do" bullet
rep('<li>Re-supply the full multi-year assessment history (only some years are retained; see Flagged).</li>',
    '<li>Verify the restored full-year assessment history against the assessor portals (links on the Property tax page).</li>')

# 3. tax page closing paragraph (rate now confirmed)
rep('''<p>Estate tax exposure = (taxable estate − exclusion) × rate. The top rate is not confirmed (flag X16) so exposure is left blank. Enter the estate total from the owner's own records to test against these thresholds.</p>''',
    '''<p>Estate tax exposure = (taxable estate − exclusion) × rate. The top rate is 40% (FTB analysis; CRS R48183). Only about 0.07% of decedents owe any federal estate tax (2019 data, CRS), and a couple can cover $30M in 2026 with portability. Enter the estate total from the owner's own records to test against these thresholds.</p>''')

# 4. ownership-costs: official insurance benchmarks + solar/NEM context
rep('''        ["Maintenance (placeholders)", "A 0.5% and B 1.0% of market value per year", status_badge("assumption"), ["NONE"]],''',
    '''        ["California statewide average homeowners premium benchmark (multi-peril, 2008–2023)", "$1,176 average written premium per policy-year", status_badge("verified"), ["CDI-RESIDENTIAL-REPORT"]],
        ["California statewide average earned premium per residential policy, 2023", "$1,130 ($14.22B ÷ 12.58M policy-years, computed from CDI totals)", status_badge("verified"), ["CDI-SB824-DATA"]],
        ["California statewide average Coverage A (main structure limit), 2023", "$324,973", status_badge("verified"), ["CDI-SB824-DATA"]],
        ["Rooftop solar export credits (context for the owner's $10–20/mo credit)", "NEM guaranteed 20 years; surplus annual generation paid ≈2–3¢/kWh", status_badge("verified"), ["CPUC-SOLAR-GUIDE"]],
        ["Maintenance (placeholders)", "A 0.5% and B 1.0% of market value per year", status_badge("assumption"), ["NONE"]],''')
rep('''<li>Property B water in SF is not reconciled to tariff components because sewer and stormwater charges were not reviewed (flag X13).</li>''',
    '''<li>Property B water in SF is not reconciled to tariff components because sewer and stormwater charges were not reviewed (flag X13).</li>
<li>Official statewide insurance benchmarks (CDI) are shown for context only — they are not property-specific. The owner's $1,500/yr figures for both properties remain unverified; property and landlord quotes are required (flag X14).</li>
<li>Statewide insurance averages cannot be applied to a specific home: CDI publishes per-ZIP data (SB 824 workbook) but it was not machine-readable in this session; retrieve a quote instead.</li>''')

# 5. projections page: official reference benchmarks
rep('''{sens_tbl}
"""''',
    '''{sens_tbl}
<h2>Official reference benchmarks (context for the assumptions above)</h2>
{bench_tbl}
"""''')
rep('''    body = f"""
<h1>Projections, 2026–2050</h1>''',
    '''    bench = [
        ["California home price growth, purchase-only (FHFA, 2026Q2)", "Last 12 months −0.20%; last 5 years +17.31% (≈4.1%/yr since 1991Q1, computed)", status_badge("verified"), ["FHFA-HPI-2026Q2"]],
        ["U.S. large-cap equities (S&P 500 index)", "2,131.52 → 7,688.62 over 10 years (2016-11-07 → 2026-11-04), ≈13.7%/yr computed from the official FRED series — history, not a forecast", status_badge("verified"), ["FRED-SP500"]],
        ["10-year U.S. Treasury yield", "5.13% (2026-10-01 observation)", status_badge("verified"), ["FRED-GS10"]],
        ["U.S. inflation (CPI-U)", "+3.7% over the 12 months ending September 2026", status_badge("verified"), ["BLS-CPI"]],
        ["Model cost-inflation assumption", "2%–3% per year (assumption; Fed longer-run PCE objective 2%)", status_badge("assumption"), ["FED-PCE-TARGET"]],
    ]
    bench_tbl = table(["Reference benchmark", "Value", "Status"], bench, "bench", None)
    body = f"""
<h1>Projections, 2026–2050</h1>''')

# 6. inheritance-process: notice step + 9-month detail, renumber tail
rep('''        ("3", "Check federal estate tax filing", "Form 706 is required when the gross estate plus adjusted taxable gifts exceeds the filing threshold for the year of death ($15,000,000 for 2026). Portability to a surviving spouse requires a timely return.", ["IRS-ESTATE-TAX"]),''',
    '''        ("3", "Check federal estate tax filing", "Form 706 is required when the gross estate plus adjusted taxable gifts exceeds the filing threshold for the year of death ($15,000,000 for 2026). It is due within 9 months of death (extensions available), and portability to a surviving spouse requires a timely return.", ["IRS-ESTATE-TAX", "FTB-ESTATE-TAX-ANALYSIS"]),''')
rep('''        ("11", "Decide: live, rent, or sell (see Decision page)", "Compare the break-even rent for Property A and the keep vs sell results for Property B using the owner's own inputs.", ["BOE-LTA-2026-026"]),
        ("12", "If selling, track basis and holding period", "Basis is the value at death. A sale soon after death generally produces little gain. Use the federal brackets for any gain.", ["IRS-REV-PROC-2025-32", "IRS-PUB-551"]),
        ("13", "Keep records", "Retain the appraisal, the deed, the PCOR, Prop 19 filings, and tax bills. These support basis and exclusion claims.", ["IRS-PUB-551"]),''',
    '''        ("11", "Send the statutory trust notices", "Within 60 days of the settlor's death the trustee must give written notice to all beneficiaries and heirs (Prob. Code §16061.7), and within 150 days give written notice to the county Assessor of any real estate in the trust (R&TC §480(b)) — per the Santa Clara Superior Court.", ["SCC-COURTS-TRUST"]),
        ("12", "Inventory, value assets, set up the trust EIN", "The trustee inventories and values all assets as of the date of death to test the estate-tax threshold; file/pay any estate tax within 9 months; obtain a trust EIN for income-tax filing.", ["SCC-COURTS-TRUST"]),
        ("13", "Decide: live, rent, or sell (see Decision page)", "Compare the break-even rent for Property A and the keep vs sell results for Property B using the owner's own inputs.", ["BOE-LTA-2026-026"]),
        ("14", "If selling, track basis and holding period", "Basis is the value at death. A sale soon after death generally produces little gain. Use the federal brackets for any gain.", ["IRS-REV-PROC-2025-32", "IRS-PUB-551"]),
        ("15", "Keep records", "Retain the appraisal, the deed, the PCOR, Prop 19 filings, the 60-day and 150-day notices, and tax bills. These support basis and exclusion claims.", ["IRS-PUB-551", "SCC-COURTS-TRUST"]),''')

open(p, "w", encoding="utf-8").write(s)
print("data + build_site.py updated")
