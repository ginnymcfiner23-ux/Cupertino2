#!/usr/bin/env python3
"""Build the static GitHub Pages site in docs/ from data/*.json and data/*.csv.

Run:  python3 scripts/model.py && python3 scripts/build_site.py
The build FAILS (non-zero exit) if:
  - any table row has no source ID, or a source ID is not registered in data/sources.json
  - any registered source URL is not https
  - any internal link points to a missing file
  - any external link points to a URL not in data/sources.json
"""
import csv
import html
import json
import os
import re
import sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
DATA = os.path.join(ROOT, "data")
DOCS = os.path.join(ROOT, "docs")
TODAY = "2026-11-06"


def load(name):
    with open(os.path.join(DATA, name), encoding="utf-8") as f:
        return json.load(f)


SOURCES = {s["id"]: s for s in load("sources.json")["sources"]}
FACTS = load("facts.json")["rows"]
FLAGS = load("flagged.json")["items"]
PHIST = load("property_history.json")["rows"]
DEC = load("decision.json")
SENS = list(csv.DictReader(open(os.path.join(DATA, "sensitivity.csv"), encoding="utf-8")))
PROJ = list(csv.DictReader(open(os.path.join(DATA, "projections_base.csv"), encoding="utf-8")))
ERRORS = []


def esc(x):
    return html.escape("" if x is None else str(x))


def money(x, dec=0):
    if x is None or x == "":
        return "blank"
    x = float(x)
    s = f"{abs(x):,.{dec}f}"
    return ("-$" if x < 0 else "$") + s


def pct(x, dec=2):
    return f"{float(x) * 100:.{dec}f}%"


def src_links(ids, context):
    if not ids:
        ERRORS.append(f"{context}: row has no source")
        return "<span class='miss'>MISSING SOURCE</span>"
    if ids == ["NONE"]:
        return "<a href='flagged.html#X23'>No official source: assumption (see Flagged X23)</a>"
    out = []
    for sid in ids:
        if sid not in SOURCES:
            ERRORS.append(f"{context}: unknown source id {sid}")
            continue
        s = SOURCES[sid]
        out.append(f"<a href='{esc(s['url'])}' rel='noopener' title='{esc(s['title'])}'>{esc(sid)}</a>")
    return " · ".join(out)


def table(headers, rows, context, caption=None):
    """rows: list of lists; last cell must be the source-ids list (or pre-rendered)."""
    h = "".join(f"<th>{esc(x)}</th>" for x in headers)
    body = []
    for r in rows:
        cells = "".join(f"<td>{c}</td>" for c in r[:-1])
        cells += f"<td class='src'>{src_links(r[-1], context)}</td>"
        m = re.match(r"^(X\d+)\b", str(r[0]))
        rid = f" id='{m.group(1)}'" if m else ""
        body.append(f"<tr{rid}>{cells}</tr>")
    cap = f"<caption>{esc(caption)}</caption>" if caption else ""
    return f"<div class='tablewrap'><table>{cap}<thead><tr>{h}<th>Source (official)</th></tr></thead><tbody>{''.join(body)}</tbody></table></div>"


def status_badge(s):
    cls = {"verified": "ok", "partially verified": "warn", "user-provided": "warn", "secondary": "bad",
           "assumption": "bad", "blank": "bad"}
    key = "user-provided" if s.startswith("user-provided") else ("blank" if s.startswith("blank") else s)
    return f"<span class='badge {cls.get(key, 'warn')}'>{esc(s)}</span>"


NAV = [
    ("index.html", "Dashboard"),
    ("property-tax.html", "Property tax"),
    ("ownership-costs.html", "Ownership costs"),
    ("projections.html", "Projections"),
    ("decision.html", "Live / rent / sell"),
    ("tax-thresholds.html", "Tax & thresholds"),
    ("inheritance-process.html", "Inheritance steps"),
    ("law-changes.html", "Law changes"),
    ("sources.html", "Sources"),
    ("flagged.html", "Flagged for Review"),
]


def page(filename, title, body, active):
    nav = "".join(
        f"<a href='{href}' class='{'active' if href == active else ''}'>{esc(label)}</a>"
        for href, label in NAV)
    n_flags = len(FLAGS)
    html_doc = f"""<!doctype html>
<html lang='en'>
<head>
<meta charset='utf-8'>
<meta name='viewport' content='width=device-width, initial-scale=1'>
<title>{esc(title)} · Inheritance decision dashboard</title>
<link rel='stylesheet' href='assets/style.css'>
</head>
<body>
<header class='top'>
  <div class='brand'>Inheritance decision dashboard <span class='sub'>Two properties · anonymized</span></div>
  <nav>{nav}</nav>
</header>
<main>
<div class='banner'>Research only, not legal or tax advice. Property A = Cupertino, CA. Property B = San Francisco, CA. No names, addresses, or ZIP codes are published. Data as of {TODAY}. <a href='flagged.html'>{n_flags} items flagged for review</a>.</div>
{body}
</main>
<footer>Sources are listed per row. Blank = not provided or not confirmed on an official source. Flagged items do not block publication. Repo: <a href='https://github.com/ginnymcfiner23-ux/Cupertino2'>ginnymcfiner23-ux/Cupertino2</a>.</footer>
</body>
</html>
"""
    with open(os.path.join(DOCS, filename), "w", encoding="utf-8") as f:
        f.write(html_doc)


# ---------------------------------------------------------------- numbers
D45 = DEC["decisions"]["2045"]
D40 = DEC["decisions"]["2040"]
D50 = DEC["decisions"]["2050"]
base_row_2045 = next(r for r in PROJ if r["year"] == "2045") if any(r["year"] == "2045" for r in PROJ) else None
sens_by = {r["scenario"]: r for r in SENS}
base_sens = sens_by["appreciation 3%, return 6%"]
keep_wins = [r["scenario"] for r in SENS if float(r["sf_keep_minus_sell"]) > 0]
sell_cup_wins_all = all(float(r["cup_sell_minus_live"]) > 0 for r in SENS)
cup_sell_base = D45["best"]["cupertino"] == "Sell at inheritance"
sf_sell_base = D45["best"]["sf"] == "Sell at inheritance"

# Projection rows for 2045 as numbers
p2045 = next(r for r in PROJ if r["year"] == "2045")
p2026 = next(r for r in PROJ if r["year"] == "2026")

# ---------------------------------------------------------------- pages
def build_index():
    tiles = f"""
<div class='tiles'>
  <div class='tile'><div class='k'>Property A value, Nov 2026 (owner est.)</div><div class='v'>{money(3100000)}</div><div class='s'>Source: owner estimate · flagged</div></div>
  <div class='tile'><div class='k'>Property B value, Nov 2026 (owner est.)</div><div class='v'>{money(1800000)}</div><div class='s'>Source: owner estimate · flagged</div></div>
  <div class='tile'><div class='k'>Prop 19 value cap (to Feb 15, 2027)</div><div class='v'>{money(1044586)}</div><div class='s'>BOE LTA 2025/009</div></div>
  <div class='tile'><div class='k'>Federal estate exclusion, 2026 deaths</div><div class='v'>{money(15000000)}</div><div class='s'>IRS · per person</div></div>
  <div class='tile'><div class='k'>SF secured tax rate, FY2026-27</div><div class='v'>{pct(0.0118162182, 8)}</div><div class='s'>SF Treasurer</div></div>
  <div class='tile'><div class='k'>Flagged for review</div><div class='v'>{len(FLAGS)}</div><div class='s'>See Flagged page</div></div>
</div>"""
    rec_cards = f"""
<div class='cards'>
  <div class='card'>
    <h3>Recommendation (base case)</h3>
    <p><strong>Property A (Cupertino):</strong> {'Sell at inheritance' if cup_sell_base else 'Keep / live in'} is the higher-value option in the base case
    (inheritance {D45['inherit_year']}, 10-year horizon). Selling beats living there in {sum(1 for r in SENS if float(r['cup_sell_minus_live']) > 0)} of {len(SENS)} sensitivity cases.
    Living there becomes worthwhile only if the heir would otherwise pay rent above about {money(D45['breakeven_imputed_rent_cup_yr_at_inheritance'])} per year (year-of-inheritance dollars).</p>
    <p><strong>Property B (San Francisco):</strong> {'Sell at inheritance' if sf_sell_base else 'Keep as rental'} in the base case.
    Keeping wins in {len(keep_wins)} of {len(SENS)} sensitivity cases ({'; '.join(keep_wins) if keep_wins else 'none'}). Full reassessment on transfer is assumed, which is the main cost of keeping it.</p>
    <p class='note'>These results depend on assumptions that are not sourced (appreciation, return, maintenance, selling cost). Change them and test the sensitivity table on the Projections page before acting.</p>
  </div>
  <div class='card'>
    <h3>Key tax facts</h3>
    <ul>
      <li>Transfers by death, including distributions from a trust, are covered by Prop 19 (BOE LTA 2026/026).</li>
      <li>Prop 19 excludes the family home only when the heir makes it their principal residence. Rental property is not eligible (BOE).</li>
      <li>On a sale soon after death, the basis is generally the value at death, so little gain is expected (IRS Pub 551; confirm).</li>
      <li>No documentary transfer tax applies to transfers by reason of death (RTC §11930).</li>
      <li>Federal estate exclusion: $15M per person for 2026 deaths (IRS).</li>
    </ul>
  </div>
  <div class='card'>
    <h3>What to do next</h3>
    <ul>
      <li>Verify the restored full-year assessment history against the assessor portals (links on the Property tax page).</li>
      <li>Verify parcel-level values on the county assessor portals (links on Property tax page).</li>
      <li>Confirm occupancy plans for Property A and mixed-use treatment for Property B with the assessors.</li>
      <li>Get an estate attorney or CPA to review the trust documents and the inheritance steps.</li>
    </ul>
  </div>
</div>"""
    body = f"""
<h1>Executive summary</h1>
<p class='lede'>This dashboard compares three choices for two properties inherited through a trust around 2040–2050: live in, rent, or sell. Figures are projections built from owner-provided inputs and official rules. Anything not confirmed on an official source is flagged.</p>
{tiles}
{rec_cards}
<h2>Projection snapshot (base case, inheritance {D45['inherit_year']})</h2>
<div class='tablewrap'><table><thead><tr><th>Measure</th><th>2026</th><th>{D45['inherit_year']}</th><th>Source (official)</th></tr></thead><tbody>
<tr><td>Property A market value</td><td>{money(p2026['cup_mv'])}</td><td>{money(p2045['cup_mv'])}</td><td class='src'>{src_links(['SCC-ASSESSOR'], 'idx')}</td></tr>
<tr><td>Property A tax, status quo (owner)</td><td>{money(p2026['cup_tax_status_quo'])}</td><td>{money(p2045['cup_tax_status_quo'])}</td><td class='src'>{src_links(['SCC-ASSESSOR','BOE-LTA-2009-036'], 'idx')}</td></tr>
<tr><td>Property A tax after inheritance (Prop 19 move-in)</td><td>blank</td><td>{money(p2045['cup_tax_post_inh_prop19'])}</td><td class='src'>{src_links(['BOE-LTA-2026-026'], 'idx')}</td></tr>
<tr><td>Property B market value</td><td>{money(p2026['sf_mv'])}</td><td>{money(p2045['sf_mv'])}</td><td class='src'>{src_links(['SF-ASSESSOR'], 'idx')}</td></tr>
<tr><td>Property B tax after reassessment</td><td>blank</td><td>{money(p2045['sf_tax_post_inh_reassessed'])}</td><td class='src'>{src_links(['SF-TREASURER-SECURED'], 'idx')}</td></tr>
</tbody></table></div>
<p><a href='projections.html'>Full year-by-year table, 2026–2050 →</a></p>
"""
    page("index.html", "Dashboard", body, "index.html")


def build_property_tax():
    rows = []
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
                 "2019–20 as supplied.")

    facts_rows = []
    for f in FACTS:
        if f["id"] in ("F-PROP13-CAP", "F-P19-CAP", "F-P19-NTV", "F-P19-DEATH", "F-P19-RESIDENCE", "F-P19-RENTAL", "F-SF-RATE-2627", "F-SF-DUE", "F-PCOR", "F-DTT-BASE", "F-DTT-EXEMPT-DEATH"):
            facts_rows.append([f["label"], f["value"], status_badge(f["status"]), f["sources"]])
    fact_tbl = table(["Rule / rate", "Value", "Status"], facts_rows, "property-facts", "Official rules and rates")
    links = """<h2>Verify your own values (official lookup)</h2>
<ul>
<li>Property A: <a href='https://asr.santaclaracounty.gov/home'>Santa Clara County Assessor</a> (Property Search and Assessment Look-Up).</li>
<li>Property B: <a href='https://www.sf.gov/departments--assessor-recorder'>San Francisco Assessor-Recorder</a> (community portal).</li>
<li>Property B tax: <a href='https://sftreasurer.org/property/secured-property-taxes'>SF Treasurer, secured property taxes</a>.</li>
</ul>"""
    body = f"""
<h1>Property tax and assessment</h1>
<p class='lede'>Prop 13 limits annual growth in the assessed value to inflation, not more than 2% per year. When a home passes to a child, Prop 19 can keep part of that protection, but only if the child lives in it as their principal residence. Owner-provided numbers are shown with their status; none is verified against an assessor record yet.</p>
<h2>Owner-provided assessment history (anonymized)</h2>
{hist}
<h2>Official rules and rates</h2>
{fact_tbl}
{links}
<h2>Prop 19 worked example (base case, inheritance {D45['inherit_year']})</h2>
<p>Excluded amount = factored base year value + Prop 19 cap. New taxable value = full cash value − cap when value exceeds the cap (BOE LTA 2026/026). Property A: market value {money(D45['cup_mv_at_inheritance'])}, new taxable value {money(D45['cup_ntv_prop19'])} (with Prop 19) vs {money(D45['cup_ntv_full'])} (full reassessment). Property B: rental units are not eligible; full reassessment modeled.</p>
"""
    page("property-tax.html", "Property tax", body, "property-tax.html")


def build_costs():
    cost_rows = [
        ["Property A water (owner estimate $100–150/mo)", "$125/mo midpoint (model)", status_badge("user-provided — unverified"), ["SJW-AL-629A"]],
        ["San Jose Water Schedule 1 service charge, 5/8-inch meter", "$79.67 per meter per month", status_badge("verified"), ["SJW-AL-629A"]],
        ["San Jose Water quantity rate, 0–6 ccf", "$5.0355 per ccf", status_badge("verified"), ["SJW-AL-629A"]],
        ["San Jose Water quantity rate, 6–12 ccf", "$7.5156 per ccf", status_badge("verified"), ["SJW-AL-629A"]],
        ["San Jose Water quantity rate, over 12 ccf", "$14.3548 per ccf", status_badge("verified"), ["SJW-AL-629A"]],
        ["Property A electricity, net of solar credit (owner: ~$0)", "Model: −$9/mo net cost (BSC top tier less $15 credit)", status_badge("user-provided — unverified"), ["PGE-BSC-AL-7825E"]],
        ["PG&E Base Services Charge applies to almost all residential customers", "Applies (fixed daily charge)", status_badge("partially verified"), ["PGE-BSC-AL-7825E"]],
        ["Property A insurance (owner guess $1,500/yr)", "$1,500/yr (model)", status_badge("user-provided — unverified"), ["CDI-HOME"]],
        ["Property B water, three units (owner $330–400/mo)", "$365/mo midpoint (model)", status_badge("user-provided — unverified"), ["SFPUC-RATES-2026-27"]],
        ["SFPUC W-1B service charge per meter per month, FY2026-27", "$19.65", status_badge("verified"), ["SFPUC-RATES-2026-27"]],
        ["SFPUC W-1B quantity charge per dwelling unit (first 3)", "$12.03; additional $12.91", status_badge("verified"), ["SFPUC-RATES-2026-27"]],
        ["Property B electricity (owner $30–70/mo)", "$50/mo midpoint (model)", status_badge("user-provided — unverified"), ["PGE-BSC-AL-7825E"]],
        ["Property B insurance, three-unit rental (owner guess $1,500/yr)", "$1,500/yr (model); likely low for a landlord policy", status_badge("user-provided — unverified"), ["CDI-HOME"]],
        ["Property B rent, two covered units (owner)", "$7,150/mo (model)", status_badge("user-provided — unverified"), ["SF-RENT-BOARD"]],
        ["Property A rental income", "blank (not provided)", status_badge("blank"), ["SCC-ASSESSOR"]],
        ["California statewide average homeowners premium benchmark (multi-peril, 2008–2023)", "$1,176 average written premium per policy-year", status_badge("verified"), ["CDI-RESIDENTIAL-REPORT"]],
        ["California statewide average earned premium per residential policy, 2023", "$1,130 ($14.22B ÷ 12.58M policy-years, computed from CDI totals)", status_badge("verified"), ["CDI-SB824-DATA"]],
        ["California statewide average Coverage A (main structure limit), 2023", "$324,973", status_badge("verified"), ["CDI-SB824-DATA"]],
        ["Rooftop solar export credits (context for the owner's $10–20/mo credit)", "NEM guaranteed 20 years; surplus annual generation paid ≈2–3¢/kWh", status_badge("verified"), ["CPUC-SOLAR-GUIDE"]],
        ["Maintenance (placeholders)", "A 0.5% and B 1.0% of market value per year", status_badge("assumption"), ["NONE"]],
    ]
    tbl = table(["Item", "Value used", "Status"], cost_rows, "costs", "Ownership costs: tariffs (official) and owner inputs")
    body = f"""
<h1>Ownership costs</h1>
<p class='lede'>Utilities are priced from published tariffs where possible. Owner estimates are used as given, marked unverified, and flagged. Maintenance is a placeholder.</p>
{tbl}
<h2>Notes</h2>
<ul>
<li>Owner's $100–150/mo Property A water range corresponds to about 4–9 ccf per month on a 5/8-inch meter under Schedule No. 1, so the meter size and usage should be confirmed (flag X12).</li>
<li>Property A electricity: the fixed charge is modeled at the top tier, net of the owner's $15 average credit. The per-day tier amounts still need confirming (flag X11).</li>
<li>Property B water in SF is not reconciled to tariff components because sewer and stormwater charges were not reviewed (flag X13).</li>
<li>Official statewide insurance benchmarks (CDI) are shown for context only — they are not property-specific. The owner's $1,500/yr figures for both properties remain unverified; property and landlord quotes are required (flag X14).</li>
<li>Statewide insurance averages cannot be applied to a specific home: CDI publishes per-ZIP data (SB 824 workbook) but it was not machine-readable in this session; retrieve a quote instead.</li>
</ul>
"""
    page("ownership-costs.html", "Ownership costs", body, "ownership-costs.html")


def build_projections():
    cols = [
        ("year", "Year", None, None),
        ("cup_mv", "A market value", "cup", "SCC-ASSESSOR"),
        ("cup_av", "A assessed value (2% cap)", "cup", "BOE-LTA-2009-036"),
        ("cup_tax_status_quo", "A tax, owner", "cup", "SCC-ASSESSOR"),
        ("cup_tax_post_inh_prop19", "A tax after inheritance (Prop 19)", "cup", "BOE-LTA-2026-026"),
        ("sf_mv", "B market value", "sf", "SF-ASSESSOR"),
        ("sf_av", "B assessed value (2% cap)", "sf", "BOE-LTA-2009-036"),
        ("sf_tax_status_quo", "B tax, owner", "sf", "SF-TREASURER-SECURED"),
        ("sf_tax_post_inh_reassessed", "B tax after reassessment", "sf", "SF-TREASURER-SECURED"),
        ("sf_rent_annual", "B rent (annual)", "sf", "SF-RENT-BOARD"),
        ("cup_water", "A water/yr", "cup", "SJW-AL-629A"),
        ("cup_electric_net_cost", "A electricity net cost/yr", "cup", "PGE-BSC-AL-7825E"),
        ("cup_insurance", "A insurance/yr", "cup", "CDI-HOME"),
        ("cup_maintenance", "A maintenance/yr", "cup", "NONE"),
        ("sf_water", "B water/yr", "sf", "SFPUC-RATES-2026-27"),
        ("sf_electric", "B electricity/yr", "sf", "PGE-BSC-AL-7825E"),
        ("sf_insurance", "B insurance/yr", "sf", "CDI-HOME"),
        ("sf_maintenance", "B maintenance/yr", "sf", "NONE"),
    ]
    head = "".join(f"<th>{esc(c[1])}</th>" for c in cols)
    src_row = "".join(f"<td class='src'>{src_links([c[3]], 'proj') if c[3] else ''}</td>" for c in cols)
    body_rows = []
    for r in PROJ:
        cells = []
        for key, _, _, _ in cols:
            v = r.get(key, "")
            if key == "year":
                cells.append(f"<td>{v}</td>")
            elif v == "" or v is None:
                cells.append("<td class='blank'>blank</td>")
            else:
                cells.append(f"<td>{money(v)}</td>")
        body_rows.append("<tr>" + "".join(cells) + "</tr>")
    tbl = (f"<div class='tablewrap wide'><table class='proj'><thead><tr>{head}</tr><tr class='srcrow'><th>Sources →</th>{src_row}</tr></thead>"
           f"<tbody>{''.join(body_rows)}</tbody></table></div>")
    sens_rows = []
    for s in SENS:
        sens_rows.append([s["scenario"], s["inherit_year"], money(s["cup_live_nw_h"]), money(s["cup_sell_nw_h"]), money(s["sf_keep_nw_h"]), money(s["sf_sell_nw_h"]), ["NONE"]])
    sens_tbl = table(["Scenario", "Inheritance", "A live (net worth)", "A sell", "B keep", "B sell", ], [r[:6] + [r[6]] for r in sens_rows], "sens", None)
    bench = [
        ["California home price growth, purchase-only (FHFA, 2026Q2)", "Last 12 months −0.20%; last 5 years +17.31% (≈4.1%/yr since 1991Q1, computed)", status_badge("verified"), ["FHFA-HPI-2026Q2"]],
        ["U.S. large-cap equities (S&P 500 index)", "2,131.52 → 7,688.62 over 10 years (2016-11-07 → 2026-11-04), ≈13.7%/yr computed from the official FRED series — history, not a forecast", status_badge("verified"), ["FRED-SP500"]],
        ["10-year U.S. Treasury yield", "5.13% (2026-10-01 observation)", status_badge("verified"), ["FRED-GS10"]],
        ["U.S. inflation (CPI-U)", "+3.7% over the 12 months ending September 2026", status_badge("verified"), ["BLS-CPI"]],
        ["Model cost-inflation assumption", "2%–3% per year (assumption; Fed longer-run PCE objective 2%)", status_badge("assumption"), ["FED-PCE-TARGET"]],
    ]
    bench_tbl = table(["Reference benchmark", "Value", "Status"], bench, "bench", None)
    body = f"""
<h1>Projections, 2026–2050</h1>
<p class='lede'>Base case: inheritance in {D45['inherit_year']}, home values growing 3% a year, costs inflating 2–3%. Tax after inheritance assumes the heir's occupancy for Property A (Prop 19) and full reassessment for Property B. Projections are not forecasts. Change the assumptions in the flagged list and re-run.</p>
<div class='notice'>Columns show nominal dollars. Blank before the inheritance year means the heir does not yet own the property.</div>
{tbl}
<h2>Sensitivity: net worth 10 years after inheritance (nominal)</h2>
<p>Appreciation and portfolio return are the two inputs with the biggest effect. "Live" nets out the carrying costs; "sell" invests the proceeds. Positive differences favor selling for A; for B, a keep result above the sell result means keeping is better.</p>
{sens_tbl}
<h2>Official reference benchmarks (context for the assumptions above)</h2>
{bench_tbl}
"""
    page("projections.html", "Projections", body, "projections.html")


def build_decision():
    def row(label, key_prefix, Y):
        d = DEC["decisions"][str(Y)]
        return d
    rows = []
    for Y in (2040, 2045, 2050):
        d = DEC["decisions"][str(Y)]
        rows.append([f"Property A: live in (Prop 19 applies), inheritance {Y}", money(d["cup_live_nw_h"]), ["BOE-LTA-2026-026", "BOE-LTA-2025-009"]])
        rows.append([f"Property A: live in (no Prop 19, full reassessment), inheritance {Y}", money(d["cup_live_no_prop19_nw_h"]), ["BOE-LTA-2026-026"]])
        rows.append([f"Property A: sell at inheritance, inheritance {Y}", money(d["cup_sell_nw_h"]), ["RTC-11911", "RTC-11930"]])
        rows.append([f"Property B: keep as rental, inheritance {Y}", money(d["sf_keep_nw_h"]), ["SF-TREASURER-SECURED", "SF-RENT-BOARD"]])
        rows.append([f"Property B: sell at inheritance, inheritance {Y}", money(d["sf_sell_nw_h"]), ["RTC-11911", "RTC-11930"]])
        rows.append([f"Best plan, inheritance {Y}: A = {d['best']['cupertino']}; B = {d['best']['sf']}", money(d["best"]["combined_nw"]), ["BOE-LTA-2026-026", "SF-TREASURER-SECURED"]])
    tbl = table(["Option (10-year horizon after inheritance)", "Net worth (nominal)", ], rows, "decision", "Live / rent / sell comparison")
    be = [[f"Break-even imputed rent for A, inheritance {Y}, per year (year-of-inheritance $)", money(DEC['decisions'][str(Y)]['breakeven_imputed_rent_cup_yr_at_inheritance']), ["BOE-LTA-2026-026"]] for Y in (2040, 2045, 2050)]
    be_tbl = table(["Measure", "Value"], be, "breakeven", "Break-even rent")
    body = f"""
<h1>Live / rent / sell</h1>
<p class='lede'>Each option is valued at the end of a 10-year horizon after inheritance. Carrying costs are netted out, and surpluses or deficits are compounded at the portfolio return. Property A break-even rent is the amount the heir would need to save each year, growing with inflation, for living there to equal selling.</p>
<h2>Net worth comparison</h2>
{tbl}
<h2>Break-even</h2>
{be_tbl}
<h2>Best plan (base case, inheritance {D45['inherit_year']})</h2>
<ul>
<li><strong>Property A:</strong> {esc(D45['best']['cupertino'])}.</li>
<li><strong>Property B:</strong> {esc(D45['best']['sf'])}.</li>
<li>Recommendation: sell both at inheritance unless the heir needs housing and would otherwise pay rent above the break-even above. Re-run with the owner's own appreciation, return, and rent figures before acting.</li>
</ul>
<h2>What is not in these numbers</h2>
<ul>
<li>Income tax on rent or portfolio income (flag X25).</li>
<li>Imputed value of the owner-occupied third unit in Property B (flag X25).</li>
<li>City transfer taxes on sale (flag X15).</li>
</ul>
"""
    page("decision.html", "Live / rent / sell", body, "decision.html")


def build_tax():
    fed = [f for f in FACTS if f["category"] == "federal"]
    st = [f for f in FACTS if f["category"] == "state"]
    lo = [f for f in FACTS if f["category"] == "local"]

    def rows_of(lst):
        return [[f["label"], f["value"], status_badge(f["status"]), f["sources"]] for f in lst]
    # estate threshold by year (2026 official; later years are a labeled projection)
    est_rows = []
    for y in (2026, 2030, 2035, 2040, 2045, 2050):
        val = DEC["estate_exclusion_by_year"][str(y)]
        status = status_badge("verified") if y == 2026 else status_badge("assumption")
        est_rows.append([y, money(val), status, ["IRS-ESTATE-TAX"] if y == 2026 else ["IRS-2026-INFLATION"]])
    est_tbl = table(["Year of death", "Basic exclusion (per person)", "Status"], est_rows, "estate-years", None)
    body = f"""
<h1>Tax and thresholds</h1>
<p class='lede'>Federal, California, and local rules that apply to inheriting and then holding or selling these properties. The 2026 federal exclusion is official; later years are a projection.</p>
<h2>Federal</h2>
{table(["Rule", "Value", "Status"], rows_of(fed), "fed", None)}
<h2>Estate exclusion by year of death (projection after 2026)</h2>
{est_tbl}
<p>Estate tax exposure = (taxable estate − exclusion) × rate. The top rate is 40% (FTB analysis; CRS R48183). Only about 0.07% of decedents owe any federal estate tax (2019 data, CRS), and a couple can cover $30M in 2026 with portability. Enter the estate total from the owner's own records to test against these thresholds.</p>
<h2>California</h2>
{table(["Rule", "Value", "Status"], rows_of(st), "state", None)}
<h2>Local (San Francisco) and county</h2>
{table(["Rule", "Value", "Status"], rows_of(lo), "local", None)}
<h2>Capital gain on a sale soon after inheritance</h2>
<p>Basis is generally the value at death, so a sale near that value produces little or no gain (IRS Pub 551; confirm on linked page). The 2026 federal long-term capital gain brackets are in the federal table above. California income tax is not modeled because the expected gain is near zero (flag X17).</p>
"""
    page("tax-thresholds.html", "Tax & thresholds", body, "tax-thresholds.html")


def build_process():
    steps = [
        ("1", "Confirm the trust terms and the successor trustee", "Read the trust for distribution rules and whether the property goes outright or in continuing trust. Prop 19 applies to distributions from a trust.", ["BOE-LTA-2026-026"]),
        ("2", "Obtain date-of-death values for both properties", "Appraisal or broker opinion of value at the date of death. This sets the new basis for a later sale (step-up).", ["IRS-PUB-551"]),
        ("3", "Check federal estate tax filing", "Form 706 is required when the gross estate plus adjusted taxable gifts exceeds the filing threshold for the year of death ($15,000,000 for 2026). It is due within 9 months of death (extensions available), and portability to a surviving spouse requires a timely return.", ["IRS-ESTATE-TAX", "FTB-ESTATE-TAX-ANALYSIS"]),
        ("4", "Deed from trustee to heir and documentary transfer tax exemption", "Transfers by reason of death, outright or in trust, are exempt from the documentary transfer tax. Claim the exemption on the recorded deed.", ["RTC-11930"]),
        ("5", "File the Preliminary Change of Ownership Report (BOE-502-A)", "Required on the change in ownership. Mark the inheritance or parent-child box, as applicable.", ["BOE-502A"]),
        ("6", "Property A: choose occupancy and claim Prop 19 if eligible", "Prop 19 keeps the value below the cap only if the heir makes it their principal residence and claims the homeowners' exemption within the BOE windows. Otherwise full reassessment applies.", ["BOE-LTA-2026-026", "BOE-PROP19-PAGE"]),
        ("7", "Property B: expect reassessment and a supplemental bill", "Rental property is not eligible for the family-home exclusion. Expect a supplemental assessment, prorated from the change date. Confirm the mixed-use treatment with the Assessor.", ["BOE-PROP19-PAGE", "SF-ASSESSOR", "SF-TREASURER-SECURED"]),
        ("8", "Set up tax bills and due dates", "SF secured taxes: first installment delinquent after Dec 10 (10% penalty); second after Apr 10 (10% plus fees).", ["SF-TREASURER-SECURED"]),
        ("9", "Property B: rental obligations", "Owner must pay the Rent Board fee and keep the Housing Inventory current. The allowable increase for covered units is 1.6% for Mar 1, 2026 – Feb 28, 2027.", ["SF-RENT-BOARD"]),
        ("10", "Transfer utilities and insurance", "Move water, electricity, and the property policy into the heir's name. Get a landlord policy for Property B.", ["SJW-AL-629A", "SFPUC-RATES-2026-27", "CDI-HOME"]),
        ("11", "Send the statutory trust notices", "Within 60 days of the settlor's death the trustee must give written notice to all beneficiaries and heirs (Prob. Code §16061.7), and within 150 days give written notice to the county Assessor of any real estate in the trust (R&TC §480(b)) — per the Santa Clara Superior Court.", ["SCC-COURTS-TRUST"]),
        ("12", "Inventory, value assets, set up the trust EIN", "The trustee inventories and values all assets as of the date of death to test the estate-tax threshold; file/pay any estate tax within 9 months; obtain a trust EIN for income-tax filing.", ["SCC-COURTS-TRUST"]),
        ("13", "Decide: live, rent, or sell (see Decision page)", "Compare the break-even rent for Property A and the keep vs sell results for Property B using the owner's own inputs.", ["BOE-LTA-2026-026"]),
        ("14", "If selling, track basis and holding period", "Basis is the value at death. A sale soon after death generally produces little gain. Use the federal brackets for any gain.", ["IRS-REV-PROC-2025-32", "IRS-PUB-551"]),
        ("15", "Keep records", "Retain the appraisal, the deed, the PCOR, Prop 19 filings, the 60-day and 150-day notices, and tax bills. These support basis and exclusion claims.", ["IRS-PUB-551", "SCC-COURTS-TRUST"]),
    ]
    rows = [[s[0], f"<strong>{esc(s[1])}</strong><br>{esc(s[2])}", s[3]] for s in steps]
    tbl = table(["Step", "What to do", ], [[r[0], r[1], r[2]] for r in rows], "process", None)
    body = f"""
<h1>Inheritance steps (California trust)</h1>
<p class='lede'>A general sequence for a trust-held inheritance of two California properties. This is research, not legal advice. Have an estate attorney or CPA confirm each step against the trust documents.</p>
{tbl}
<p class='note'>Probate and trust-administration timelines vary. Court and trustee steps are not listed in detail here.</p>
"""
    page("inheritance-process.html", "Inheritance steps", body, "inheritance-process.html")


def build_law():
    law = [f for f in FACTS if f["category"] in ("legislation",)]
    rows = [[f["label"], f["value"], status_badge(f["status"]), f["sources"]] for f in law]
    rows.append(["Federal estate tax exclusion after 2026 (indexed)", "Projection assumes 2% indexing; official amounts later", status_badge("assumption"), ["IRS-2026-INFLATION"]])
    rows.append(["Prop 19 $1M value cap next adjustment", "February 2027 (BOE)", status_badge("verified"), ["BOE-LTA-2025-009"]])
    tbl = table(["Item", "Status / value", "Status"], rows, "law", None)
    body = f"""
<h1>Pending and recent law changes</h1>
<p class='lede'>What could change the numbers. Items are shown with their status as of {TODAY}. Unofficial election results are flagged.</p>
{tbl}
"""
    page("law-changes.html", "Law changes", body, "law-changes.html")


def build_sources():
    rows = []
    for sid, s in SOURCES.items():
        rows.append([f"{esc(s['title'])} <span class='muted'>({esc(s['publisher'])})</span>", s["supports"], status_badge("verified") if s["type"] == "official" else status_badge("secondary"), [sid]])
    tbl = table(["Source", "Used for", "Type"], rows, "sources", None)
    body = f"""
<h1>Sources</h1>
<p class='lede'>Every row on this site cites one or more sources below. "Official" means a government agency, statute, IRS publication, or utility-filed CPUC tariff. "Secondary" sources are used only to flag conflicts.</p>
{tbl}
"""
    page("sources.html", "Sources", body, "sources.html")


def build_flagged():
    rows = []
    for it in FLAGS:
        rows.append([f"{esc(it['id'])} · {esc(it['type'])}", it["item"], it["action"], it["sources"]])
    tbl = table(["ID · type", "Issue", "Action"], rows, "flagged", None)
    body = f"""
<h1>Flagged for Review</h1>
<div class='notice bad'>Items here could not be confirmed from an official source, conflict between sources, are estimates, or are assumptions. They do not block publication. Each item links to the official page where it should be checked.</div>
{tbl}
"""
    page("flagged.html", "Flagged for Review", body, "flagged.html")


CSS = """
:root{--ink:#1d2430;--muted:#66707e;--line:#e3e7ee;--bg:#f6f8fb;--ok:#e7f6ec;--okink:#16643a;--warn:#fff4dc;--warnink:#8a5a00;--bad:#fdebec;--badink:#9b1c1c;--brand:#1f4e79}
*{box-sizing:border-box}body{margin:0;font:15px/1.5 system-ui,-apple-system,Segoe UI,Roboto,sans-serif;color:var(--ink);background:var(--bg)}
header.top{background:#fff;border-bottom:1px solid var(--line);padding:12px 20px;position:sticky;top:0;z-index:5}
.brand{font-weight:700;color:var(--brand)}.brand .sub{font-weight:400;color:var(--muted);margin-left:8px;font-size:13px}
nav{display:flex;flex-wrap:wrap;gap:6px 14px;margin-top:8px}nav a{color:var(--ink);text-decoration:none;font-size:14px;padding:3px 0;border-bottom:2px solid transparent}
nav a.active,nav a:hover{border-bottom-color:var(--brand);color:var(--brand)}
main{max-width:1280px;margin:0 auto;padding:20px}
.banner{background:#eef4fb;border:1px solid #cfe0f4;border-radius:8px;padding:10px 14px;font-size:14px;margin-bottom:18px}
.banner a,main a{color:var(--brand)}
h1{font-size:26px;margin:6px 0 10px}h2{font-size:19px;margin:26px 0 8px;color:#2b3a4d}h3{margin:0 0 8px;font-size:16px}
.lede{font-size:16px;color:#34404f;max-width:900px}
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:12px;margin:16px 0}
.tile{background:#fff;border:1px solid var(--line);border-radius:10px;padding:14px}.tile .k{font-size:12px;color:var(--muted)}.tile .v{font-size:22px;font-weight:700;margin:4px 0}.tile .s{font-size:12px;color:var(--muted)}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:14px}
.card{background:#fff;border:1px solid var(--line);border-radius:10px;padding:16px}.card ul{margin:0;padding-left:18px}
.tablewrap{overflow-x:auto;background:#fff;border:1px solid var(--line);border-radius:10px;margin:8px 0}
table{border-collapse:collapse;width:100%;font-size:14px}th,td{padding:8px 10px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}
thead th{background:#f1f4f9;font-weight:600;position:sticky;top:0}
td.src{font-size:12px;white-space:nowrap}td.blank{color:var(--muted);font-style:italic}
table.proj td,table.proj th{font-size:12.5px;white-space:nowrap;text-align:right}table.proj th:first-child,table.proj td:first-child{text-align:left}
tr.srcrow td{font-size:11px;color:var(--muted);text-align:left}
.badge{display:inline-block;border-radius:999px;padding:1px 8px;font-size:12px;white-space:nowrap}
.badge.ok{background:var(--ok);color:var(--okink)}.badge.warn{background:var(--warn);color:var(--warnink)}.badge.bad{background:var(--bad);color:var(--badink)}
.notice{background:var(--warn);border-radius:8px;padding:10px 14px;margin:10px 0}.notice.bad{background:var(--bad)}
.note,.muted{color:var(--muted);font-size:13px}.miss{color:var(--badink);font-weight:700}
footer{max-width:1280px;margin:20px auto;padding:0 20px 40px;color:var(--muted);font-size:13px}
@media (max-width:700px){main{padding:12px}h1{font-size:22px}}
"""


def write_css():
    os.makedirs(os.path.join(DOCS, "assets"), exist_ok=True)
    with open(os.path.join(DOCS, "assets", "style.css"), "w") as f:
        f.write(CSS)
    open(os.path.join(DOCS, ".nojekyll"), "w").close()


def check_links():
    href_re = re.compile(r"""href=['"]([^'"]+)['"]""")
    ext_ok = {s["url"] for s in SOURCES.values()} | {"https://github.com/ginnymcfiner23-ux/Cupertino2"}
    problems = []
    for fn in os.listdir(DOCS):
        if not fn.endswith(".html"):
            continue
        text = open(os.path.join(DOCS, fn), encoding="utf-8").read()
        for h in (html.unescape(x) for x in href_re.findall(text)):
            h = h.split("#")[0] if not h.startswith("http") else h
            if not h:
                continue
            if h.startswith("http"):
                if h not in ext_ok:
                    problems.append(f"{fn}: unregistered external link {h}")
                if not h.startswith("https://"):
                    problems.append(f"{fn}: non-https link {h}")
            elif h.startswith("#"):
                continue
            else:
                if not os.path.exists(os.path.join(DOCS, h)):
                    problems.append(f"{fn}: broken internal link {h}")
    for s in SOURCES.values():
        if not s["url"].startswith("https://"):
            problems.append(f"source {s['id']} is not https")
    return problems


def check_facts():
    for f in FACTS:
        if not f.get("sources"):
            ERRORS.append(f"fact {f['id']} has no source")
        for sid in f.get("sources", []):
            if sid not in SOURCES:
                ERRORS.append(f"fact {f['id']} unknown source {sid}")
    for it in FLAGS:
        for sid in it["sources"]:
            if sid not in SOURCES:
                ERRORS.append(f"flag {it['id']} unknown source {sid}")


def main():
    os.makedirs(DOCS, exist_ok=True)
    write_css()
    check_facts()
    build_index()
    build_property_tax()
    build_costs()
    build_projections()
    build_decision()
    build_tax()
    build_process()
    build_law()
    build_sources()
    build_flagged()
    problems = check_links()
    problems += ERRORS
    if problems:
        print("BUILD FAILED:")
        for p in problems:
            print("  -", p)
        sys.exit(1)
    print("Build OK. Pages:", sorted(f for f in os.listdir(DOCS) if f.endswith('.html')))


if __name__ == "__main__":
    main()
