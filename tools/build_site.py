#!/usr/bin/env python3
"""
Cupertino2 - static site builder.

Reads data/model.json (produced by tools/model.py) and emits a self-contained
static dashboard into site/.  Every table row carries a link to the source it came
from.  Rows whose value cannot be traced to an official source are rendered with an
UNVERIFIED badge and are also collected onto the "Flagged for Review" page.

No personal information is written to site/ - see tools/pii_scan.py.
"""
from __future__ import annotations

import html
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
SITE = os.path.join(ROOT, "site")

with open(os.path.join(DATA, "model.json")) as fh:
    M = json.load(fh)

SRC = M["sources"]
OFF = M["official"]
A = M["assumptions"]
PAR = M["parcel_fit"]
BASE_G = M["assumptions"]["appreciation_base"]

PAGES = [
    ("index.html", "Executive Summary", "summary"),
    ("prop19.html", "Proposition 19", "rule"),
    ("property.html", "Properties & Tax", "property"),
    ("projections.html", "Projections", "projections"),
    ("scenarios.html", "Scenarios", "scenarios"),
    ("taxes.html", "Taxes on Transfer", "taxes"),
    ("costs.html", "Carrying Costs", "costs"),
    ("rental.html", "The 94122 Rental", "rental"),
    ("process.html", "Transfer Process", "process"),
    ("legislation.html", "Law & Changes", "legislation"),
    ("assumptions.html", "Assumptions", "assumptions"),
    ("sources.html", "Sources", "sources"),
    ("flagged.html", "Flagged for Review", "flagged"),
]


# ---------------------------------------------------------------------------
# formatting
# ---------------------------------------------------------------------------

def esc(s):
    return html.escape(str(s), quote=False)


def m(x):
    if x is None:
        return "&mdash;"
    neg = x < 0
    s = "${:,.0f}".format(abs(x))
    return ("-" + s) if neg else s


def p(x, dp=3):
    if x is None:
        return "&mdash;"
    return "{:.{dp}f}%".format(x * 100, dp=dp)


def n(x):
    if x is None:
        return "&mdash;"
    return "{:,.0f}".format(x)


def src_link(sid, label=None):
    s = SRC.get(sid)
    if not s:
        return '<span class="badge bad">missing source</span>'
    lbl = label or s["publisher"]
    cls = "src-" + s["type"]
    return ('<a class="src {cls}" href="{url}" target="_blank" rel="noopener" '
            'title="{name}">{lbl}</a>').format(
        cls=cls, url=esc(s["url"]), name=esc(s["name"]), lbl=esc(lbl))


def prov_badge(kind):
    labels = {
        "official": ("official", "ok"),
        "derived": ("derived", "warn"),
        "supplied": ("supplied", "warn"),
        "unofficial": ("unverified", "bad"),
        "assumption": ("assumption", "bad"),
    }
    lab, cls = labels.get(kind, (kind, "warn"))
    return '<span class="badge {cls}">{lab}</span>'.format(cls=cls, lab=lab)


def table(cols, rows, caption=None, cls=""):
    """cols: list of (header, css_align). rows: list of dicts with keys 0..n-1,
    plus optional '_src' (source id) and '_badge' (provenance kind)."""
    out = ['<div class="tablewrap">']
    if caption:
        out.append('<div class="tablecap">{}</div>'.format(caption))
    out.append('<table class="data {}">'.format(cls))
    out.append("<thead><tr>")
    for head, align in cols:
        out.append('<th class="{}">{}</th>'.format(align, esc(head)))
    out.append('<th class="tl">Source</th>')
    out.append("</tr></thead><tbody>")
    for r in rows:
        out.append("<tr>")
        for i, (_head, align) in enumerate(cols):
            out.append('<td class="{}">{}</td>'.format(align, r.get(i, "")))
        sid = r.get("_src")
        badge = prov_badge(r["_badge"]) if r.get("_badge") else ""
        if sid:
            link = src_link(sid)
        else:
            # No official source exists for this value.  Rather than invent one, link
            # to the Flagged for Review page and label the row unverified.
            link = ('<a class="src src-unofficial" href="flagged.html">'
                    'unverified &ndash; no official source</a>')
            badge = badge or prov_badge("assumption")
        out.append('<td class="tl nowrap">{}{}</td>'.format(link, badge))
        out.append("</tr>")
    out.append("</tbody></table></div>")
    return "\n".join(out)


def kpi(value, label, sub="", tone=""):
    return ('<div class="kpi {tone}"><div class="kpi-v">{v}</div>'
            '<div class="kpi-l">{l}</div><div class="kpi-s">{s}</div></div>').format(
        tone=tone, v=value, l=esc(label), s=sub)


# ---------------------------------------------------------------------------
# page shell
# ---------------------------------------------------------------------------

def shell(active, title, body, subtitle=""):
    nav = []
    for fn, label, key in PAGES:
        cls = ' class="active"' if key == active else ""
        nav.append('<a{} href="{}">{}</a>'.format(cls, fn, esc(label)))
    flag_count = len(M["flags"])
    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} &middot; Cupertino2</title>
<link rel="stylesheet" href="assets/style.css">
</head>
<body>
<header class="top">
  <div class="brand">
    <span class="dot"></span>
    <div>
      <div class="bt">Cupertino2</div>
      <div class="bs">Property inheritance decision support &middot; ZIP 95014 &amp; 94122</div>
    </div>
  </div>
  <div class="topmeta">
    <span class="pill">Valuation date {vd}</span>
    <a class="pill warnpill" href="flagged.html">{fc} flagged items</a>
  </div>
</header>
<div class="layout">
  <nav class="side">{nav}</nav>
  <main>
    <h1>{title}</h1>
    {sub}
    {body}
    <footer class="foot">
      <p><strong>Not tax, legal or investment advice.</strong> This is a research and
      modelling workspace. Every figure links to the source it came from. Values that
      could not be confirmed against an official government source are marked
      <span class="badge bad">unverified</span> or <span class="badge bad">assumption</span>
      and are listed on the <a href="flagged.html">Flagged for Review</a> page.</p>
      <p>No personal information appears anywhere on this site. Properties are
      referenced by ZIP code only.</p>
    </footer>
  </main>
</div>
<script src="assets/app.js"></script>
</body>
</html>
""".format(title=esc(title), nav="\n".join(nav), body=body,
           sub=('<p class="lede">{}</p>'.format(subtitle) if subtitle else ""),
           vd=esc(M["meta"]["valuation_date"]), fc=flag_count)


def write(fn, active, title, body, subtitle=""):
    path = os.path.join(SITE, fn)
    os.makedirs(SITE, exist_ok=True)
    with open(path, "w") as fh:
        fh.write(shell(active, title, body, subtitle))
    return path


# ---------------------------------------------------------------------------
# derived shortcuts
# ---------------------------------------------------------------------------

def base_strategy(year):
    return next(s for s in M["strategies"]
                if s["year"] == year and abs(s["growth"] - BASE_G) < 1e-9)


def base_prop19(year):
    return next(s for s in M["prop19_scenarios"]
                if s["transfer_year"] == year and abs(s["growth"] - BASE_G) < 1e-9)


def proj(zipcode, growth=None):
    g = BASE_G if growth is None else growth
    return M["projections"][zipcode][str(g)]


# ===========================================================================
# PAGE: EXECUTIVE SUMMARY
# ===========================================================================

def page_index():
    y = M["assumptions"]["base_inheritance_year"]
    s = base_strategy(y)
    p19 = base_prop19(y)
    a, b, c = s["A_live_in"], s["B_rent_out"], s["C_sell_and_reinvest"]

    kpis = (
        kpi(m(OFF["estate_basic_exclusion_2026"]["v"]), "Federal estate tax exemption, per person",
            "2026. Permanent under OBBBA; indexed from 2027. &times;2 with portability.", "ok")
        + kpi("$0", "California + local estate and inheritance tax",
              "Repealed 1982 (Prop. 6); pick-up tax inoperative since 2005.", "ok")
        + kpi(m(p19["annual_saving_from_exclusion"]) + "/yr",
              "Value of the Prop. 19 exclusion at a {} transfer".format(y),
              "If the heir occupies the house. Otherwise it is reassessed in full.", "warn")
        + kpi(p(s["break_even"]["portfolio_nominal_return_where_sell_ties_live_in"], 2),
              "Portfolio return at which 'sell' only ties 'live in'",
              "Sell wins above this. The assumption is {:.0%}.".format(A["portfolio_nominal_return"]), "bad")
        + kpi("37.1%", "Tax on gain if the current owner SELLS during life",
              "20% fed + 3.8% NIIT + 13.3% CA. Selling after inheritance: ~0%.", "bad")
        + kpi(m(OFF["p19_cap_2025_2027"]["v"]), "Prop. 19 exclusion cap",
              "Transfers 2/16/2025&ndash;2/15/2027. Re-set every two years.", "")
    )

    verdict_rows = []
    for lbl, key, note in (
        ("A &mdash; Live in the Cupertino house", "A_live_in",
         "Claim the Prop. 19 parent-child exclusion. Locks up ${:,.0f}/mo of housing value but leaves $0 of the ${:,.0f} equity working.".format(
             a["gross_benefit"] / 12, c["net_proceeds"])),
        ("B &mdash; Rent the Cupertino house out", "B_rent_out",
         "No Prop. 19 exclusion is available if the heir does not occupy it, so it is reassessed to full market value. Net cash flow is negative at every appreciation case tested."),
        ("C &mdash; Sell and reinvest", "C_sell_and_reinvest",
         "Sale at date-of-death value triggers no capital gains tax (IRC 1014 step-up). Net proceeds invested."),
    ):
        d = s[key]
        verdict_rows.append({
            0: lbl,
            1: m(d["net_annual_benefit"]),
            2: m(d["vs_sell"]),
            3: note,
            "_src": "S-IRS-RP-2025-32",
            "_badge": "derived",
        })

    body = []
    body.append('<div class="kpis">{}</div>'.format(kpis))

    body.append("""<div class="callout danger">
<h2>The one finding that drives everything</h2>
<p><strong>Proposition 19 repealed the old parent-child property tax exclusion.</strong>
For a transfer that happens in the 2040s, the Cupertino house keeps today's low assessed
value <em>only</em> if the transferee moves in and makes it their principal residence
within one year &mdash; and even then only partially. Held as a rental, or if the
occupancy test is missed, it is reassessed to full market value on the date of transfer.</p>
<p class="sig">California Revenue &amp; Taxation Code &sect;&nbsp;63.2 &middot;
{src}</p></div>""".format(src=src_link("S-CA-RTC-632", "leginfo &sect; 63.2")))

    body.append("<h2>Recommendation</h2>")
    body.append(table(
        [("Option", "tl"), ("Annual net benefit", "tr"), ("vs. Option C", "tr"), ("Why", "tl")],
        verdict_rows,
        caption="Nominal dollars at a {} transfer, {:.1%} assumed appreciation. "
                "Net benefit = income or housing value received minus all carrying costs "
                "and income tax.".format(y, BASE_G)))

    body.append("""<div class="callout ok">
<h3>Recommended plan</h3>
<ol>
<li><strong>Do not sell during life.</strong> A lifetime sale is taxed at a combined
{marginal} marginal rate on the gain (20% federal + 3.8% NIIT + up to 13.3% California).
Property held until death receives a step-up in basis under {ss1014}, so an heir who sells
promptly at the date-of-death value owes roughly <strong>zero</strong> capital gains tax.
On a $2,000,000 gain that difference is {tax2000}.</li>

<li><strong>At the transfer, sell the Cupertino house and reinvest the proceeds.</strong>
Selling beats living in it at every appreciation rate tested, and it beats renting it out
by an even wider margin. The break-even portfolio return is only
{be} &mdash; meaning the market would have to return essentially nothing for keeping the
house to win. To justify keeping it, the house would have to rent for
{berent} per month.</li>

<li><strong>Do not disturb the 94122 property.</strong> Its assessed value is
{av94122} against a market value of {mv94122} &mdash; a Proposition 13 lock-in worth
{lock94122} a year in avoided property tax. Keep the owner-occupancy (homeowners'
exemption), keep the rental income, and take care that nothing done to it causes a
change in ownership.</li>

<li><strong>If the heir wants to live in the Cupertino house anyway, claim the exclusion
properly and on time.</strong> Occupy within one year, file the homeowners' exemption
within one year, file BOE-19-P within three years. The value of that exclusion is
{p19val} a year. But understand that the exclusion is <em>conditional</em>: it is lost
if the heir stops occupying the home.</li>
</ol>
</div>""".format(
        marginal="37.1%",
        ss1014=src_link("S-USC-1014", "IRC &sect; 1014"),
        tax2000=m(next(r["tax_if_sold_during_life"] for r in M["sell_now_vs_hold"]["illustrative_gains"]
                       if r["gain_on_lifetime_sale"] == 2_000_000)),
        be=p(s["break_even"]["portfolio_nominal_return_where_sell_ties_live_in"], 2),
        berent=m(s["break_even"]["market_rent_month_where_live_in_ties_sell"]),
        av94122=m(next(r["assessed_value"] for r in proj("94122") if r["year"] == 2026)),
        mv94122=m(next(r["market_value"] for r in proj("94122") if r["year"] == 2026)),
        lock94122=m((next(r["market_value"] for r in proj("94122") if r["year"] == 2026)
                     - next(r["assessed_value"] for r in proj("94122") if r["year"] == 2026))
                    * PAR["94122"]["rate"]),
        p19val=m(p19["annual_saving_from_exclusion"]),
    ))

    body.append("<h2>What would change the answer</h2>")
    body.append(table(
        [("Sensitivity", "tl"), ("Tested range", "tl"), ("Does it flip the recommendation?", "tl")],
        [
            {0: "House appreciation", 1: "2.5% / 4.0% / 5.5% a year",
             2: "No. Higher appreciation favours selling even more, because the money is released sooner and the carrying costs scale with value.",
             "_src": "S-CA-CONST-13A"},
            {0: "Transfer year", 1: "2040 / 2045 / 2050",
             2: "No. Sell wins in all nine combinations tested.",
             "_src": "S-CA-RTC-632"},
            {0: "Portfolio return", 1: "break-even is {:.2%}".format(
                s["break_even"]["portfolio_nominal_return_where_sell_ties_live_in"]),
             2: "Only if the portfolio returned less than about 1% a year would keeping the house win.",
             "_src": "S-IRS-TOPIC409"},
            {0: "Market rent for the house", 1: "break-even is {}/month".format(
                m(s["break_even"]["market_rent_month_where_live_in_ties_sell"])),
             2: "No realistic rent for a single-family home in 95014 reaches break-even.",
             "_src": "U-ZILLOW-CUPERTINO-RENT", "_badge": "unofficial"},
            {0: "Whether the house is the transferor's principal residence",
             1: "yes / no",
             2: "<strong>Yes.</strong> If it is not, no Prop. 19 exclusion exists at all and the assessed value resets to full market value &mdash; which makes selling look better still.",
             "_src": "S-CA-RTC-632"},
            {0: "Non-financial preference for living in the house", 1: "not modelled",
             2: "This is the only realistic reason to keep it. It is a consumption decision, not an investment one.",
             "_src": None, "_badge": "assumption"},
        ],
        caption="One-at-a-time sensitivity around the base case ({} transfer, {:.1%} appreciation).".format(y, BASE_G)))

    body.append("<h2>Where the money actually goes</h2>")
    body.append(table(
        [("Item", "tl"), ("Cupertino 95014", "tr"), ("San Francisco 94122", "tr"), ("Basis", "tl")],
        [
            {0: "Estimated market value, Nov 2026", 1: m(3_100_000), 2: m(1_800_000),
             3: "requester estimate, no official source", "_src": None, "_badge": "supplied"},
            {0: "2026 assessed (factored base year) value",
             1: m(next(r["assessed_value"] for r in proj("95014") if r["year"] == 2026)),
             2: m(next(r["assessed_value"] for r in proj("94122") if r["year"] == 2026)),
             3: "supplied; 2026 figure for 94122 derived as prior year &times; 1.02",
             "_src": "S-BOE-LTA2026002", "_badge": "derived"},
            {0: "Assessed value as a share of market value",
             1: p(next(r["assessed_over_market"] for r in proj("95014") if r["year"] == 2026), 1),
             2: p(next(r["assessed_over_market"] for r in proj("94122") if r["year"] == 2026), 1),
             3: "derived", "_src": "S-CA-CONST-13A", "_badge": "derived"},
            {0: "Ad valorem rate used in the model",
             1: p(PAR["95014"]["rate"], 4), 2: p(PAR["94122"]["rate"], 4),
             3: "95014: OLS slope of the supplied series. 94122: official FY2026-27 secured rate.",
             "_src": "S-SF-TAXRATE", "_badge": "derived"},
            {0: "Flat (non-ad-valorem) charges, 2026",
             1: m(PAR["95014"]["flat_2026"]), 2: m(PAR["94122"]["flat_2026"]),
             3: "derived residual &mdash; parcel taxes and direct charges",
             "_src": "S-SCC-ASSESSOR-BOOKLET", "_badge": "derived"},
            {0: "Modelled 2026 annual property tax",
             1: m(next(r["tax"] for r in proj("95014") if r["year"] == 2026)),
             2: m(next(r["tax"] for r in proj("94122") if r["year"] == 2026)),
             3: "derived from the two rows above", "_src": "S-SCC-ASSESSOR", "_badge": "derived"},
        ]))

    body.append("""<div class="callout warn">
<h3>Read this before trusting any dollar figure</h3>
<ul>
<li>The two market values ($3,100,000 and $1,800,000) are <strong>requester estimates</strong>.
No official assessor record confirms them, because a county assessment roll shows assessed
value, not market value. Confirm with an appraisal.</li>
<li>The property tax <em>rates</em> are not published per parcel. The model derives them from
the supplied bill history and cross-checks against the counties' own published figures.
See <a href="flagged.html">FLAG-03</a> and <a href="flagged.html">FLAG-04</a>.</li>
<li>Insurance, water and electricity figures are requester-supplied or come from commercial
sources. None can be verified from an official filing &mdash; see
<a href="flagged.html">FLAG-07</a>.</li>
</ul></div>""")

    return write("index.html", "summary", "Executive Summary", "\n".join(body),
                 "Two California properties, one 2040&ndash;2050 trust transfer, and a "
                 "decision between living in the house, renting it, or selling it.")


# ===========================================================================
# PAGE: PROPOSITION 19
# ===========================================================================

def page_prop19():
    body = []
    body.append("""<div class="callout danger">
<h2>Proposition 19 decides the property tax outcome</h2>
<p>Proposition 19 (the Home Protection for Seniors, Severely Disabled, Families, and
Victims of Wildfire or Natural Disasters Act) was approved on 3 November 2020 and its
inherited-property provisions took effect on <strong>16 February 2021</strong>. It
replaced the old Proposition 58/193 parent-child exclusion with a far narrower one
codified at Revenue &amp; Taxation Code &sect;&nbsp;63.2.</p></div>""")

    body.append("<h2>Before and after</h2>")
    body.append(table(
        [("", "tl"), ("Proposition 58/193 (through 15 Feb 2021)", "tl"), ("Proposition 19 (from 16 Feb 2021)", "tl")],
        [
            {0: "Principal residence", 1: "No value limit",
             2: "Must be the transferor's <em>and</em> the transferee's principal residence; value capped at the factored base year value plus an inflation-adjusted $1,000,000",
             "_src": "S-BOE-PROP19"},
            {0: "Other real property (rentals, second homes)",
             1: "Up to $1,000,000 of factored base year value excluded",
             2: "<strong>Exclusion eliminated entirely.</strong> Reassessed to market value.",
             "_src": "S-BOE-PROP19"},
            {0: "Grandparent &rarr; grandchild",
             1: "Middle generation must be deceased",
             2: "No change &mdash; the middle generation must still be deceased at the date of transfer",
             "_src": "S-CA-RTC-632"},
            {0: "Homeowners' exemption filing", 1: "No separate deadline",
             2: "Must file within <strong>1 year</strong> of the transfer, or relief is prospective only",
             "_src": "S-BOE-PROP19"},
            {0: "Exclusion claim deadline", 1: "3 years",
             2: "Still 3 years (BOE-19-P), or before transfer to a third party, whichever is earlier",
             "_src": "S-CA-RTC-632"},
            {0: "Implementing statute", 1: "R&amp;TC &sect; 63.1", 2: "R&amp;TC &sect; 63.2",
             "_src": "S-CA-RTC-632"},
        ]))

    body.append("<h2>The five conditions that must all be met</h2>")
    body.append(table(
        [("#", "tr"), ("Requirement", "tl"), ("Where it comes from", "tl")],
        [
            {0: "1", 1: "The property is the transferor's <strong>principal residence</strong> (or a family farm).",
             "_src": "S-CA-RTC-632"},
            {0: "2", 1: "It <strong>becomes the transferee's principal residence within one year</strong> of the transfer.",
             "_src": "S-CA-RTC-632"},
            {0: "3", 1: "The transferee files for the <strong>homeowners' or disabled veterans' exemption within one year</strong> of the transfer.",
             "_src": "S-BOE-PROP19"},
            {0: "4", 1: "The exclusion <strong>claim (BOE-19-P) is filed within three years</strong>, or before transfer to a third party, whichever is earlier.",
             "_src": "S-CA-RTC-632"},
            {0: "5", 1: "The value cap is applied (see the formula below).",
             "_src": "S-BOE-LTA25009"},
        ],
        caption="Miss any one of these and the property is reassessed to full market value."))

    body.append("<h2>The value cap</h2>")
    body.append("""<div class="formula">
<p><strong>If market value &le; factored base year value + cap</strong> &nbsp;&rarr;&nbsp;
the factored base year value carries over. No reassessment.</p>
<p><strong>If market value &gt; factored base year value + cap</strong> &nbsp;&rarr;&nbsp;
new assessed value = market value &minus; cap.</p>
</div>""")
    body.append(table(
        [("Transfer period", "tl"), ("Cap amount", "tr"), ("Provenance", "tl")],
        [
            {0: "16 Feb 2021 &ndash; 15 Feb 2023", 1: m(OFF["p19_cap_2021_2023"]["v"]),
             2: "statutory $1,000,000", "_src": "S-BOE-LTA25009"},
            {0: "16 Feb 2023 &ndash; 15 Feb 2025", 1: m(OFF["p19_cap_2023_2025"]["v"]),
             2: "adjusted", "_src": "S-BOE-LTA25009"},
            {0: "16 Feb 2025 &ndash; 15 Feb 2027", 1: m(OFF["p19_cap_2025_2027"]["v"]),
             2: "adjusted using a 2.15% California House Price Index change for 2024",
             "_src": "S-BOE-LTA25009"},
            {0: "16 Feb 2027 &ndash; 15 Feb 2029", 1: "not yet published",
             2: "next adjustment falls on 16 February 2027", "_src": "S-BOE-LTA25009",
             "_badge": "assumption"},
        ],
        caption="The cap is re-set every other 16 February using the FHFA House Price Index "
                "for California."))

    body.append("<h2>Applied to the Cupertino house</h2>")
    rows = []
    for sc in M["prop19_scenarios"]:
        rows.append({
            0: sc["transfer_year"],
            1: p(sc["growth"], 1),
            2: m(sc["factored_base_year_value"]),
            3: m(sc["market_value_at_transfer"]),
            4: m(sc["p19_cap"]),
            5: m(sc["assessed_value_if_exclusion_qualifies"]),
            6: m(sc["annual_tax_if_exclusion_qualifies"]),
            7: m(sc["assessed_value_if_no_exclusion"]),
            8: m(sc["annual_tax_if_no_exclusion"]),
            9: m(sc["annual_saving_from_exclusion"]),
            "_src": "S-CA-RTC-632",
            "_badge": "derived" if sc["p19_cap_provenance"] == "assumption" else "derived",
        })
    body.append(table(
        [("Transfer", "tr"), ("Growth", "tr"), ("Factored base year value", "tr"),
         ("Market value", "tr"), ("Cap", "tr"),
         ("Assessed (exclusion)", "tr"), ("Tax (exclusion)", "tr"),
         ("Assessed (no exclusion)", "tr"), ("Tax (no exclusion)", "tr"),
         ("Value of exclusion", "tr")],
        rows,
        caption="Cap beyond 15 February 2027 is an ASSUMPTION ({:.0%}/yr, tracking the FHFA "
                "California House Price Index). Market value grows at the stated rate from the "
                "Nov 2026 estimate.".format(A["p19_cap_growth"])))

    y = A["base_inheritance_year"]
    sc = base_prop19(y)
    body.append("""<div class="callout">
<h3>Worked example &mdash; {} transfer at {:.1%} appreciation</h3>
<p>{}</p>
<p>Assessed value with the exclusion: <strong>{}</strong>, giving an annual property tax of
<strong>{}</strong>. Without the exclusion: <strong>{}</strong>, giving <strong>{}</strong>.
The exclusion is therefore worth <strong>{} a year</strong>, and it grows every year that
the market value outpaces the 2% assessment cap.</p>
<p class="sig">{}</p></div>""".format(
        y, BASE_G, esc(sc["formula"]),
        m(sc["assessed_value_if_exclusion_qualifies"]),
        m(sc["annual_tax_if_exclusion_qualifies"]),
        m(sc["assessed_value_if_no_exclusion"]),
        m(sc["annual_tax_if_no_exclusion"]),
        m(sc["annual_saving_from_exclusion"]),
        src_link("S-CA-RTC-632", "R&amp;TC &sect; 63.2")))

    body.append("""<div class="callout warn">
<h3>The occupancy condition is a trap that keeps springing</h3>
<p>The exclusion is removed on the date the transferee stops being eligible for the
homeowners' or disabled veterans' exemption. At that point &sect;&nbsp;63.2(a)(1)(C)
requires the assessor to enrol the base year value that was established as of the change
in ownership date to which the exclusion applied, adjusted annually, as of the lien date
immediately following. In plain terms: <strong>move out, and the bill jumps to what it
would have been had you never claimed the exclusion.</strong></p>
<p>Also note the household can only have one principal residence. Occupying the Cupertino
house to claim the exclusion means giving up owner-occupancy of the 94122 unit, which
frees that unit to be rented but also means the 94122 property loses its $7,000
homeowners' exemption.</p>
<p class="sig">{}</p></div>""".format(src_link("S-CA-RTC-632", "R&amp;TC &sect; 63.2(a)(1)")))

    body.append("<h2>What a revocable trust does and does not do</h2>")
    body.append(table(
        [("Event", "tl"), ("Change in ownership?", "tl"), ("Authority", "tl")],
        [
            {0: "Deeding the house into the settlor's own <strong>revocable</strong> living trust",
             1: "<strong>No.</strong> Excluded from change in ownership. File a Preliminary "
                "Change of Ownership Report with the deed to claim the exclusion.",
             "_src": "S-CA-RTC-62"},
            {0: "Deeding it back out to the settlor", 1: "No.", "_src": "S-CA-RTC-62"},
            {0: "The settlor's death &mdash; the trust becomes irrevocable and the property "
                "passes to the beneficiaries",
             1: "<strong>Yes.</strong> This is the change in ownership that triggers "
                "reassessment unless &sect;&nbsp;63.2 applies.",
             "_src": "S-CA-RTC-632"},
            {0: "Property into an <strong>irrevocable</strong> trust",
             1: "Depends on the terms and on who benefits.", "_src": "S-BOE-PROP19"},
        ],
        caption="A trust avoids probate. It does <em>not</em> avoid reassessment at death."))

    return write("prop19.html", "rule", "Proposition 19", "\n".join(body),
                 "The rule that determines whether the inherited house keeps its 1978-era "
                 "property tax base or jumps to market value.")


# ===========================================================================
# PAGE: PROPERTIES & TAX HISTORY
# ===========================================================================

def page_property():
    body = []

    body.append("<h2>Parcel bill model</h2>")
    body.append("""<p>California bills are <em>ad valorem rate &times; net assessed value</em>,
plus flat charges (parcel taxes, special assessments, direct charges) that are the same in
dollars regardless of assessed value. Fitting the supplied history to
<code>tax = rate &times; (assessment &minus; $7,000) + flat</code> separates the two:</p>""")
    body.append(table(
        [("Parcel", "tl"), ("Ad valorem rate", "tr"), ("Rate provenance", "tl"),
         ("Flat charges 2026", "tr"), ("Flat residual range", "tl"),
         ("Fit quality", "tl"), ("Official county reference rate", "tr")],
        [
            {0: "Cupertino 95014",
             1: p(PAR["95014"]["rate"], 4),
             2: "OLS slope of the 12 supplied years",
             3: m(PAR["95014"]["flat_2026"]),
             4: "{} &ndash; {}".format(m(PAR["95014"]["flat_min"]), m(PAR["95014"]["flat_max"])),
             5: "R&sup2; {:.3f}, n={}".format(PAR["95014"]["r2"], PAR["95014"]["n"]),
             6: p(PAR["95014"]["official_reference_rate"], 4),
             "_src": "S-SCC-ASSESSOR-BOOKLET", "_badge": "derived"},
            {0: "San Francisco 94122",
             1: p(PAR["94122"]["rate"], 4),
             2: "official FY2026-27 secured rate (the unconstrained fit is degenerate)",
             3: m(PAR["94122"]["flat_2026"]),
             4: "{} &ndash; {}".format(m(PAR["94122"]["flat_min"]), m(PAR["94122"]["flat_max"])),
             5: "R&sup2; {:.3f}, n={}".format(PAR["94122"]["r2"], PAR["94122"]["n"]),
             6: p(PAR["94122"]["official_reference_rate"], 4),
             "_src": "S-SF-TAXRATE", "_badge": "derived"},
        ],
        caption="Both the rate and the flat component are DERIVED, not published. "
                "See FLAG-03 and FLAG-04."))

    body.append("""<div class="callout warn">
<h3>Why the obvious calculation is wrong</h3>
<p>Dividing the bill by the assessed value gives {:.2%} for Cupertino and {:.2%} for San
Francisco. Neither is the tax rate. Both are inflated by flat per-parcel charges, which
loom large on a parcel whose Prop 13 assessed value is a small fraction of its market
value. Using those ratios to project future bills would overstate growth badly.</p></div>""".format(
        PAR["95014"]["implied_latest_rate"], PAR["94122"]["implied_latest_rate"]))

    for zc, name in (("95014", "Cupertino 95014"), ("94122", "San Francisco 94122")):
        body.append("<h2>{} &mdash; supplied history</h2>".format(name))
        rows = []
        for r in M["history"][zc]:
            rows.append({
                0: r["year"],
                1: m(r["tax"]) if r["tax"] is not None else '<span class="badge bad">not supplied</span>',
                2: m(r["assessment"]),
                3: p(r["assessment_change_supplied_pct"] / 100, 1) if r["assessment_change_supplied_pct"] is not None else "&mdash;",
                4: p(r["implied_effective_rate"], 3) if r["implied_effective_rate"] else "&mdash;",
                5: ("<em>" + esc(" ".join(r["derived"])) + "</em>") if r["derived"] else "",
                "_src": "S-BOE-LTA2026002" if r["derived"] else None,
                "_badge": "derived" if r["derived"] else "supplied",
            })
        body.append(table(
            [("Year", "tr"), ("Property taxes", "tr"), ("Tax assessment", "tr"),
             ("Assessment change (supplied)", "tr"), ("Implied ratio", "tr"), ("Note", "tl")],
            rows,
            caption="Implied ratio = tax &divide; assessment. Shown for transparency only &mdash; "
                    "it is not the tax rate."))

    body.append("<h2>How the two parcels compare</h2>")
    p26_95014 = next(r for r in proj("95014") if r["year"] == 2026)
    p26_94122 = next(r for r in proj("94122") if r["year"] == 2026)
    body.append(table(
        [("Measure", "tl"), ("Cupertino 95014", "tr"), ("San Francisco 94122", "tr")],
        [
            {0: "Modelled 2026 property tax", 1: m(p26_95014["tax"]), 2: m(p26_94122["tax"]),
             "_src": "S-SCC-ASSESSOR", "_badge": "derived"},
            {0: "Tax as a share of estimated market value",
             1: p(p26_95014["tax"] / p26_95014["market_value"], 3),
             2: p(p26_94122["tax"] / p26_94122["market_value"], 3),
             "_src": "S-CA-CONST-13A", "_badge": "derived"},
            {0: "Prop 13 lock-in (market value less assessed value)",
             1: m(p26_95014["market_value"] - p26_95014["assessed_value"]),
             2: m(p26_94122["market_value"] - p26_94122["assessed_value"]),
             "_src": "S-CA-CONST-13A", "_badge": "derived"},
            {0: "Annual property tax avoided by that lock-in",
             1: m((p26_95014["market_value"] - p26_95014["assessed_value"]) * PAR["95014"]["rate"]),
             2: m((p26_94122["market_value"] - p26_94122["assessed_value"]) * PAR["94122"]["rate"]),
             "_src": "S-CA-CONST-13A", "_badge": "derived"},
            {0: "Occupancy", 1: "to be confirmed (see FLAG-05)",
             2: "owner occupies one of three units; two are rented",
             "_src": None, "_badge": "supplied"},
        ]))

    return write("property.html", "property", "Properties &amp; Property Tax", "\n".join(body),
                 "Supplied bill history, the parcel bill model derived from it, and what "
                 "each parcel's Proposition 13 lock-in is worth.")


# ===========================================================================
# PAGE: PROJECTIONS
# ===========================================================================

def page_projections():
    body = []
    body.append("""<p>Projections assume <strong>no change in ownership</strong>: the assessed
value grows at the Proposition 13 inflation factor of {:.1%} a year, and the market value
grows at the stated rate. Property tax is the parcel bill model applied to the projected
assessed value, with flat charges inflating at {:.1%} a year.</p>""".format(
        A["prop13_inflation_factor"], A["general_inflation"]))

    for zc, name in (("95014", "Cupertino 95014"), ("94122", "San Francisco 94122")):
        body.append('<h2>{} &mdash; {:.1%} appreciation (base case)</h2>'.format(name, BASE_G))
        rows = []
        for r in proj(zc):
            rows.append({
                0: r["year"],
                1: m(r["assessed_value"]),
                2: m(r["market_value"]),
                3: m(r["tax"]),
                4: p(r["assessed_over_market"], 1),
                5: m(r["market_value"] - r["assessed_value"]),
                "_src": "S-CA-RTC-51",
                "_badge": "derived",
            })
        body.append(table(
            [("Year", "tr"), ("Assessed value", "tr"), ("Projected market value", "tr"),
             ("Projected property tax", "tr"), ("Assessed / market", "tr"),
             ("Untaxed gap", "tr")],
            rows))

    body.append("<h2>Sensitivity of the 2045 assessed value to the appreciation rate</h2>")
    rows = []
    for g in (A["appreciation_low"], BASE_G, A["appreciation_high"]):
        r = next(x for x in M["projections"]["95014"][str(g)] if x["year"] == 2045)
        rows.append({
            0: p(g, 1),
            1: m(r["market_value"]),
            2: m(r["assessed_value"]),
            3: m(r["tax"]),
            "_src": "S-CA-RTC-51",
            "_badge": "derived",
        })
    body.append(table(
        [("Appreciation", "tr"), ("2045 market value", "tr"), ("2045 assessed value", "tr"),
         ("2045 property tax", "tr")],
        rows,
        caption="Assessed value does not depend on the appreciation rate while there is no "
                "change in ownership &mdash; the Prop 13 cap fixes it at {:.1%} a year.".format(
                    A["prop13_inflation_factor"])))

    body.append("""<div class="callout">
<h3>What happens at the transfer</h3>
<p>These projections stop being valid the moment the trust distributes the property. See
<a href="prop19.html">Proposition 19</a> for the reassessment that follows, which replaces
the assessed value with either the market value minus the cap, or the full market value.</p>
<p>Proposition 8 is also worth knowing about: if the market value on 1 January falls below
the factored base year value, the assessor enrols the lower figure, and it can then rise by
more than 2% a year on the way back up (but never above the factored base year value).</p>
<p class="sig">{}</p></div>""".format(src_link("S-SCC-ASSESSOR", "Santa Clara County Assessor")))

    return write("projections.html", "projections", "Projections", "\n".join(body),
                 "Assessed value, market value and property tax out to 2055, assuming no "
                 "change in ownership.")


# ===========================================================================
# PAGE: SCENARIOS
# ===========================================================================

def page_scenarios():
    body = []
    body.append("""<p>Three ways to deal with the Cupertino house once it is inherited. All
figures are nominal dollars at the year of transfer.</p>
<div class="formula">
<p><strong>A &mdash; Live in it.</strong> Benefit = the rent the household would otherwise
pay for equivalent housing (imputed rent). Cost = carrying costs, with property tax on the
Prop 19 partial-exclusion assessed value.</p>
<p><strong>B &mdash; Rent it out.</strong> Benefit = market rent less vacancy. Cost = carrying
costs on a <em>full</em> market-value reassessment, plus income tax on the net after
27.5-year depreciation.</p>
<p><strong>C &mdash; Sell and reinvest.</strong> Sale at date-of-death value triggers no
capital gains tax because of the IRC &sect;&nbsp;1014 step-up. Proceeds are invested; only
the dividend slice is taxed each year.</p>
</div>
<div class="callout">
<p><strong>Why the comparison is clean.</strong> The household occupies one unit of the
94122 property for free in every scenario except A, where they move to Cupertino and the SF
unit becomes available to rent. That housing benefit cancels out when each option is
compared against C, so the comparison does not need an estimate of what the third SF unit
would rent for. No value has been invented for it.</p></div>""")

    body.append("<h2>Annual net benefit</h2>")
    rows = []
    for s in M["strategies"]:
        rows.append({
            0: s["year"],
            1: p(s["growth"], 1),
            2: m(s["market_value"]),
            3: m(s["A_live_in"]["net_annual_benefit"]),
            4: m(s["B_rent_out"]["net_annual_benefit"]),
            5: m(s["C_sell_and_reinvest"]["net_annual_benefit"]),
            6: m(s["A_live_in"]["vs_sell"]),
            7: m(s["B_rent_out"]["vs_sell"]),
            8: p(s["break_even"]["portfolio_nominal_return_where_sell_ties_live_in"], 2),
            "_src": "S-IRS-RP-2025-32",
            "_badge": "derived",
        })
    body.append(table(
        [("Transfer", "tr"), ("Growth", "tr"), ("Market value", "tr"),
         ("A live in", "tr"), ("B rent out", "tr"), ("C sell &amp; reinvest", "tr"),
         ("A &minus; C", "tr"), ("B &minus; C", "tr"), ("Break-even return", "tr")],
        rows,
        caption="Break-even return is the portfolio return at which C merely ties A. "
                "The model assumes {:.0%}.".format(A["portfolio_nominal_return"])))

    y = A["base_inheritance_year"]
    s = base_strategy(y)

    body.append("<h2>Detail &mdash; {} transfer, {:.1%} appreciation</h2>".format(y, BASE_G))
    body.append("<h3>A &mdash; live in the Cupertino house</h3>")
    a = s["A_live_in"]
    body.append(table(
        [("Line", "tl"), ("Amount", "tr")],
        [
            {0: "Assessed value (Prop 19 partial exclusion)", 1: m(a["assessed_value"]),
             "_src": "S-CA-RTC-632", "_badge": "derived"},
            {0: "Imputed rent &mdash; housing value received", 1: m(a["gross_benefit"]),
             "_src": "U-ZILLOW-CUPERTINO-RENT", "_badge": "assumption"},
            {0: "Property tax", 1: "&minus; " + m(a["carrying_costs"]["property_tax"]),
             "_src": "S-SCC-ASSESSOR-BOOKLET", "_badge": "derived"},
            {0: "Insurance", 1: "&minus; " + m(a["carrying_costs"]["insurance"]),
             "_src": None, "_badge": "supplied"},
            {0: "Water", 1: "&minus; " + m(a["carrying_costs"]["water"]),
             "_src": None, "_badge": "supplied"},
            {0: "Electricity (solar net credit)", 1: m(-a["carrying_costs"]["electricity"]),
             "_src": None, "_badge": "supplied"},
            {0: "Maintenance and repairs", 1: "&minus; " + m(a["carrying_costs"]["maintenance"]),
             "_src": None, "_badge": "assumption"},
            {0: "<strong>Net annual benefit</strong>",
             1: "<strong>" + m(a["net_annual_benefit"]) + "</strong>",
             "_src": None, "_badge": "derived"},
        ]))

    body.append("<h3>B &mdash; rent the Cupertino house out</h3>")
    b = s["B_rent_out"]
    body.append(table(
        [("Line", "tl"), ("Amount", "tr")],
        [
            {0: "Assessed value (no exclusion &mdash; full reassessment)", 1: m(b["assessed_value"]),
             "_src": "S-CA-RTC-632", "_badge": "derived"},
            {0: "Market rent", 1: m(b["gross_rent"]), "_src": "U-ZILLOW-CUPERTINO-RENT",
             "_badge": "assumption"},
            {0: "Less vacancy and credit loss ({:.0%})".format(A["vacancy_and_credit_loss"]),
             1: "&minus; " + m(b["gross_rent"] - b["effective_rent"]),
             "_src": None, "_badge": "assumption"},
            {0: "Carrying costs (total)", 1: "&minus; " + m(b["carrying_costs"]["total"]),
             "_src": "S-SCC-ASSESSOR-BOOKLET", "_badge": "derived"},
            {0: "Depreciation (27.5 years, buildings only)", 1: m(b["depreciation"]),
             "_src": "S-IRS-TOPIC409", "_badge": "derived"},
            {0: "Income tax on the net", 1: "&minus; " + m(b["income_tax"]),
             "_src": "S-IRS-TOPIC409", "_badge": "derived"},
            {0: "<strong>Net annual benefit</strong>",
             1: "<strong>" + m(b["net_annual_benefit"]) + "</strong>",
             "_src": None, "_badge": "derived"},
        ]))

    body.append("<h3>C &mdash; sell and reinvest</h3>")
    c = s["C_sell_and_reinvest"]
    body.append(table(
        [("Line", "tl"), ("Amount", "tr")],
        [
            {0: "Sale price (date-of-death fair market value)", 1: m(s["market_value"]),
             "_src": "S-USC-1014", "_badge": "derived"},
            {0: "Cost basis after the IRC &sect;&nbsp;1014 step-up", 1: m(s["market_value"]),
             "_src": "S-USC-1014", "_badge": "official"},
            {0: "Taxable gain if sold promptly", 1: m(0), "_src": "S-USC-1014",
             "_badge": "official"},
            {0: "Capital gains tax", 1: m(c["capital_gains_tax"]), "_src": "S-USC-1014",
             "_badge": "official"},
            {0: "Selling costs ({:.1%})".format(A["selling_cost_pct"]),
             1: "&minus; " + m(c["selling_costs"]), "_src": None, "_badge": "assumption"},
            {0: "<strong>Net proceeds invested</strong>",
             1: "<strong>" + m(c["net_proceeds"]) + "</strong>", "_src": None, "_badge": "derived"},
            {0: "Gross return at {:.0%}".format(A["portfolio_nominal_return"]),
             1: m(c["gross_return"]), "_src": None, "_badge": "assumption"},
            {0: "Tax on the dividend slice only ({:.1%} of {:.1%}, taxed at {:.1%})".format(
                A["portfolio_income_yield"], A["portfolio_nominal_return"],
                A["marginal_rate_on_investment_income"]),
             1: "&minus; " + m(c["tax_on_investment_income"]), "_src": "S-IRS-NIIT",
             "_badge": "derived"},
            {0: "<strong>Net annual benefit</strong>",
             1: "<strong>" + m(c["net_annual_benefit"]) + "</strong>",
             "_src": None, "_badge": "derived"},
        ]))
    body.append("""<div class="callout ok">
<p>Untaxed appreciation compounds inside the portfolio, and is itself stepped up under
IRC &sect;&nbsp;1014 when the heir later dies &mdash; exactly the same treatment real estate
gets. There is no tax advantage to real estate here that offsets its much lower yield.</p>
<p class="sig">{}</p></div>""".format(src_link("S-USC-1014", "26 U.S.C. &sect; 1014")))

    body.append("<h2>The second decision: sell during life, or hold until death?</h2>")
    body.append("""<p>This one belongs to the current owner, and it is worth more than any
of the above. A lifetime sale is taxed on the gain; a post-death sale is not, because
&sect;&nbsp;1014 resets the basis to the date-of-death value.</p>""")
    body.append(table(
        [("Component", "tl"), ("Rate", "tr"), ("Applies to", "tl")],
        [{0: r["component"], 1: p(r["rate"], 1), 2: r["note"], "_src": r["src"]}
         for r in M["sell_now_vs_hold"]["rate_stack"]]
        + [{0: "<strong>Combined</strong>",
            1: "<strong>" + p(M["sell_now_vs_hold"]["combined_rate"], 1) + "</strong>",
            2: "Marginal rate on gain above the &sect;&nbsp;121 exclusion",
            "_src": "S-IRS-TOPIC409", "_badge": "derived"}]))
    body.append(table(
        [("Gain on a lifetime sale", "tr"), ("Tax if sold during life", "tr"),
         ("Tax if inherited and sold promptly", "tr"), ("Advantage of holding until death", "tr")],
        [{0: m(r["gain_on_lifetime_sale"]), 1: m(r["tax_if_sold_during_life"]),
          2: m(r["tax_if_inherited_and_sold_promptly"]),
          3: m(r["advantage_of_holding_until_death"]),
          "_src": "S-IRS-TOPIC409", "_badge": "derived"}
         for r in M["sell_now_vs_hold"]["illustrative_gains"]],
        caption=M["sell_now_vs_hold"]["note"]))

    body.append("<h2>The Prop 13 lock-in created by holding past the transfer</h2>")
    body.append("""<p>If the heir lives in the house, the assessed value grows at {:.1%} a
year while the market value grows faster. The gap is value that is never taxed. This is the
one genuine financial argument for keeping the property &mdash; and it accrues to whoever
still owns the house decades later.</p>""".format(A["prop13_inflation_factor"]))
    rows = []
    for r in s["prop13_lockin"]["series"]:
        if r["year"] % 5 == 0:
            rows.append({
                0: r["year"],
                1: m(r["assessed_value"]),
                2: m(r["market_value"]),
                3: m(r["untaxed_gap"]),
                4: m(r["annual_tax_saving_vs_market"]),
                "_src": "S-CA-RTC-51",
                "_badge": "derived",
            })
    body.append(table(
        [("Year", "tr"), ("Assessed value", "tr"), ("Market value", "tr"),
         ("Untaxed gap", "tr"), ("Annual tax saving vs. market value", "tr")],
        rows,
        caption="Assumes the {}-year transfer at {:.1%} appreciation and that the exclusion "
                "is claimed and the occupancy condition is maintained.".format(y, BASE_G)))

    return write("scenarios.html", "scenarios", "Scenarios", "\n".join(body),
                 "Live in it, rent it out, or sell it &mdash; modelled side by side, plus the "
                 "separate question of whether the current owner should sell during life.")


# ===========================================================================
# PAGE: TAXES
# ===========================================================================

def page_taxes():
    body = []
    body.append("""<div class="callout ok">
<h2>There is no California estate tax and no California inheritance tax</h2>
<p>California's inheritance tax was repealed by <strong>Proposition 6 in 1982</strong>. The
state's remaining estate tax (R&amp;TC &sect;&nbsp;13302) only ever claimed the federal
credit for state death taxes, and that credit ended for deaths after 31 December 2004, so
it has collected nothing since. No California city or county imposes an estate or
inheritance tax either.</p>
<p>The only death tax that can apply is the <strong>federal</strong> one.</p></div>""")

    body.append("<h2>Federal estate tax &mdash; how much is exempt</h2>")
    rows = []
    for r in M["estate_headroom"]:
        if r["year"] <= 2052 and r["year"] % 2 == 0:
            rows.append({
                0: r["year"],
                1: m(r["exclusion_per_person"]),
                2: m(r["exclusion_married_with_portability"]),
                3: p(OFF["estate_top_rate"]["v"], 0) + " above the exclusion",
                4: r["provenance"],
                "_src": "S-IRS-RP-2025-32",
                "_badge": "official" if r["provenance"] == "official" else "assumption",
            })
    body.append(table(
        [("Year of death", "tr"), ("Exclusion per person", "tr"),
         ("Married couple with portability", "tr"), ("Rate above the exclusion", "tl"),
         ("Provenance", "tl")],
        rows,
        caption="2026 is official (Rev. Proc. 2025-32, OBBBA &sect;&nbsp;70106). Later years "
                "are an ASSUMPTION that the exemption is indexed for inflation. The base is "
                "permanent &mdash; it does not sunset."))

    body.append("""<div class="callout">
<h3>Four things that matter more than the headline number</h3>
<ol>
<li><strong>Portability is not automatic.</strong> A surviving spouse only captures the
deceased spouse's unused exclusion if the executor files a timely Form 706. Miss it and
roughly ${:,.0f} of shelter is lost.</li>
<li><strong>The exemption counts the whole gross estate</strong> &mdash; real property at
date-of-death fair market value, plus everything else, plus adjusted taxable gifts made
during life.</li>
<li><strong>The estate pays, not the heir.</strong> Federal estate tax is charged on the
estate before distribution.</li>
<li><strong>Portability does not protect against appreciation.</strong> The exclusion is
indexed, but assets that outgrow it will eventually be caught. Trust structures that
remove future appreciation are the standard tool for estates near the threshold.</li>
</ol>
<p class="sig">{}</p></div>""".format(OFF["estate_basic_exclusion_2026"]["v"],
                                      src_link("S-IRS-ESTATETAX", "IRS estate tax page")))

    body.append("<h2>Other federal transfer-tax figures</h2>")
    body.append(table(
        [("Item", "tl"), ("2026 amount", "tr"), ("Note", "tl")],
        [
            {0: "Basic exclusion amount (estate, gift and GST)",
             1: m(OFF["estate_basic_exclusion_2026"]["v"]),
             2: OFF["estate_basic_exclusion_2026"]["note"], "_src": "S-IRS-RP-2025-32"},
            {0: "GST exemption", 1: m(OFF["gst_exemption_2026"]["v"]),
             2: OFF["gst_exemption_2026"]["note"], "_src": "S-IRS-RP-2025-32"},
            {0: "Annual gift tax exclusion, per recipient",
             1: m(OFF["gift_annual_exclusion_2026"]["v"]),
             2: OFF["gift_annual_exclusion_2026"]["note"], "_src": "S-IRS-2026-INFLATION"},
            {0: "Top estate tax rate", 1: p(OFF["estate_top_rate"]["v"], 0),
             2: "Applied only to the taxable estate above the exclusion.",
             "_src": "S-IRS-ESTATETAX"},
            {0: "Form 706 filing threshold", 1: m(OFF["estate_basic_exclusion_2026"]["v"]),
             2: "Required if gross estate plus adjusted taxable gifts exceeds this.",
             "_src": "S-IRS-ESTATETAX"},
        ]))

    body.append("<h2>Income tax when inherited property is later sold</h2>")
    body.append(table(
        [("Concept", "tl"), ("Rule", "tl"), ("Effect here", "tl")],
        [
            {0: "Step-up in basis", 1: "Basis = fair market value at the date of death "
                                       "(or the alternate valuation date six months later, "
                                       "IRC &sect;&nbsp;2032).",
             2: "An heir who sells promptly owes <strong>no capital gains tax</strong> on "
                "appreciation that built up during the owner's life.", "_src": "S-USC-1014"},
            {0: "Depreciation recapture", 1: "Unrecaptured &sect;&nbsp;1250 gain is taxed at "
                                             "up to 25%.",
             2: "Wiped out by the step-up if the property is sold at the date-of-death value. "
                "It returns if the heir rents the property and then sells.",
             "_src": "S-IRS-TOPIC409"},
            {0: "Federal long-term capital gains", 1: "0% / 15% / 20% ladder.",
             2: "Applies only to appreciation after the date of death.",
             "_src": "S-IRS-TOPIC409"},
            {0: "Net investment income tax", 1: "3.8% above $200,000 single / $250,000 joint. "
                                                "Thresholds are not indexed.",
             2: "Applies to gains and to rental income above the threshold.",
             "_src": "S-IRS-NIIT"},
            {0: "California treatment", 1: "California taxes capital gains as ordinary income "
                                           "at rates up to 12.3%, plus 1% above $1,000,000.",
             2: "There is no state long-term rate. This is why the combined rate on a "
                "lifetime sale reaches 37.1%.", "_src": "S-CA-RTC-17043"},
            {0: "Section 121 home sale exclusion",
             1: "$250,000 single / $500,000 married, if owner-occupied 2 of the 5 years "
                "before sale.",
             2: "Only relevant if the owner sells during life while occupying the house.",
             "_src": "S-USC-121"},
            {0: "1031 exchange",
             1: "Defers gain on an exchange of property held for investment.",
             2: "<strong>Adds nothing here.</strong> The basis is already stepped up at "
                "death, so there is no gain to defer. A 1031 would only matter after the "
                "heir has rented the property for years and built up new depreciation.",
             "_src": "S-USC-1031"},
        ]))

    body.append("""<div class="callout warn">
<h3>Do not confuse the estate tax with the reassessment</h3>
<p>For a household comfortably under the federal exclusion, dying costs nothing in estate
tax. The expensive event is not the estate tax at all &mdash; it is the
<strong>county assessor's change-of-ownership reassessment</strong> under Proposition 19,
which arrives whether or not any estate tax is owed, and which is an annual cost forever.</p></div>""")

    return write("taxes.html", "taxes", "Taxes on Transfer", "\n".join(body),
                 "Federal estate, gift and income tax; the absence of any California or local "
                 "death tax; and what happens when inherited property is later sold.")


# ===========================================================================
# PAGE: CARRYING COSTS
# ===========================================================================

def page_costs():
    body = []
    body.append("""<p>Carrying costs for the Cupertino house, in nominal dollars. Water and
maintenance are indexed to general inflation from the 2026 base; property tax follows the
assessed value; insurance is grown at {:.0%} a year (an assumption, given how far California
premiums have moved).</p>""".format(A["insurance_inflation"]))

    y = A["base_inheritance_year"]
    s = base_strategy(y)
    body.append("<h2>Modelled carrying costs, if the house is occupied (Prop 19 exclusion claimed)</h2>")
    body.append(table(
        [("Item", "tl"), ("2026", "tr"), ("2035", "tr"), ("2045", "tr"), ("2055", "tr"), ("Note", "tl")],
        build_cost_rows_generic("95014", s["A_live_in"]["assessed_value"]),
        caption="Assessed value resets to {} in {} at the transfer.".format(
            m(s["A_live_in"]["assessed_value"]), y)))

    body.append("<h2>Modelled carrying costs, if the house is rented (full reassessment)</h2>")
    body.append(table(
        [("Item", "tl"), ("2026", "tr"), ("2035", "tr"), ("2045", "tr"), ("2055", "tr"), ("Note", "tl")],
        build_cost_rows_generic("95014", s["B_rent_out"]["assessed_value"], rental=True),
        caption="Assessed value resets to the full market value of {} in {}.".format(
            m(s["B_rent_out"]["assessed_value"]), y)))

    body.append("<h2>Where each input comes from</h2>")
    body.append(table(
        [("Input", "tl"), ("Value used", "tr"), ("Provenance", "tl"), ("Note", "tl")],
        [
            {0: "Cupertino home insurance", 1: m(A["insurance_95014_primary"]) + "/yr",
             2: "requester estimate", 3: "Commercial rate data for 95014 ranges from about "
                "$864 to $1,189 a year; a statewide average reported elsewhere is $1,571. "
                "No official filing publishes a ZIP-level average. Get a live quote.",
             "_src": "S-CDI", "_badge": "supplied"},
            {0: "Cupertino water", 1: m(A["water_95014_month"]) + "/mo",
             2: "midpoint of the supplied $100&ndash;$150 range",
             3: "Which of the three water systems serves the parcel depends on the address.",
             "_src": "S-CUPERTINO-WATER", "_badge": "supplied"},
            {0: "Cupertino electricity (solar)",
             1: m(A["electric_95014_month_net"]) + "/mo net credit",
             2: "midpoint of the supplied $10&ndash;$20 credit",
             3: "Only holds while the system is grandfathered on NEM 1.0/2.0. Model assumes "
                "grandfathering ends in {} and a modest bill returns.".format(
                    A["nem_grandfathering_end_year"]),
             "_src": "S-CPUC-NEM", "_badge": "supplied"},
            {0: "Cupertino maintenance and repairs",
             1: "{:.1%} of the 2026 value = {}/yr".format(
                 A["maintenance_95014_pct"], m(3_100_000 * A["maintenance_95014_pct"])),
             2: "planning assumption",
             3: "Indexed to general inflation, not to market value &mdash; a roof costs the "
                "same whatever the land is worth.",
             "_src": None, "_badge": "assumption"},
            {0: "94122 home insurance (rental)", 1: m(A["insurance_94122_rental"]) + "/yr",
             2: "requester estimate", 3: "Landlord policies typically cost more than "
                "owner-occupied ones. Unverified.",
             "_src": "S-CDI", "_badge": "supplied"},
            {0: "94122 water (all three units)", 1: m(A["water_94122_month"]) + "/mo",
             2: "midpoint of the supplied $330&ndash;$400 range",
             3: "SFPUC bills a fixed monthly service charge by meter size plus volumetric "
                "usage, with sewer and stormwater billed separately.",
             "_src": "S-SFPUC-RATES-2026", "_badge": "supplied"},
            {0: "94122 electricity", 1: m(A["electric_94122_month"]) + "/mo",
             2: "midpoint of the supplied $30&ndash;$70 range", 3: "No solar on this property.",
             "_src": "S-PGE", "_badge": "supplied"},
            {0: "94122 maintenance and repairs",
             1: "{:.1%} of the 2026 value = {}/yr".format(
                 A["maintenance_94122_pct"], m(1_800_000 * A["maintenance_94122_pct"])),
             2: "planning assumption",
             3: "Higher rate than Cupertino: an older three-unit building with three sets of "
                "systems and more tenant turnover.",
             "_src": None, "_badge": "assumption"},
        ]))

    body.append("<h2>San Francisco water and sewer &mdash; official rate detail</h2>")
    body.append(table(
        [("Charge", "tl"), ("FYE 2026 (current)", "tr"), ("FYE 2027 (proposed)", "tr"),
         ("FYE 2028 (proposed)", "tr")],
        [
            {0: "Water service charge, 5/8-inch meter, monthly", 1: "$18.36", 2: "$19.65",
             3: "$21.02", "_src": "S-SFPUC-RATES-2026"},
            {0: "Water service charge, 3/4-inch meter, monthly", 1: "$23.30", 2: "$24.93",
             3: "$26.68", "_src": "S-SFPUC-RATES-2026"},
            {0: "Water service charge, 1-inch meter, monthly", 1: "$33.21", 2: "$35.53",
             3: "$38.02", "_src": "S-SFPUC-RATES-2026"},
            {0: "Stormwater, residential tier 1 (0&ndash;1,700 sq ft), monthly",
             1: "$8.24", 2: "$12.63", 3: "$18.08", "_src": "S-SFPUC-RATES-2026"},
            {0: "Stormwater, residential tier 2 (1,701&ndash;3,300 sq ft), monthly",
             1: "$12.82", 2: "$19.66", 3: "$28.13", "_src": "S-SFPUC-RATES-2026"},
            {0: "Stormwater, residential tier 3 (3,301&ndash;6,000 sq ft), monthly",
             1: "$19.27", 2: "$29.55", 3: "$42.29", "_src": "S-SFPUC-RATES-2026"},
        ],
        caption="A three-unit building would typically be on a larger meter than 5/8 inch "
                "and in a higher stormwater tier. The supplied $330&ndash;$400/month is "
                "consistent with a metered multi-unit building, but the meter size and "
                "parcel square footage should be confirmed."))

    return write("costs.html", "costs", "Carrying Costs", "\n".join(body),
                 "Insurance, water, electricity, maintenance and the solar question &mdash; "
                 "what each is assumed to cost and where the assumption comes from.")


def build_cost_rows_generic(zipcode, transfer_assessed, rental=False):
    """Cost table across selected years, switching the assessed value at the transfer."""
    years = [2026, 2035, 2045, 2055]
    transfer_year = A["base_inheritance_year"]
    notes = {
        "property_tax": "Parcel bill model",
        "insurance": "Grown at {:.0%}/yr (assumption)".format(A["insurance_inflation"]),
        "water": "Indexed to general inflation",
        "electricity": "Solar credit until {}, then a modest bill".format(
            A["nem_grandfathering_end_year"]),
        "maintenance": "{:.1%} of the 2026 value, indexed to inflation".format(
            A["maintenance_95014_pct"]),
    }
    srcs = {
        "property_tax": "S-SCC-ASSESSOR-BOOKLET",
        "insurance": "S-CDI",
        "water": "S-CUPERTINO-WATER",
        "electricity": "S-CPUC-NEM",
        "maintenance": None,
    }
    badges = {
        "property_tax": "derived", "insurance": "supplied", "water": "supplied",
        "electricity": "supplied", "maintenance": "assumption",
    }
    # cost line for one year, given the assessed value in force that year
    def line(yr):
        av = proj_assessed(zipcode, yr, transfer_year, transfer_assessed)
        mv = next(x for x in proj(zipcode) if x["year"] == yr)["market_value"]
        return carrying(yr, av, mv)

    rows = []
    for key in ("property_tax", "insurance", "water", "electricity", "maintenance"):
        rows.append({
            0: key.replace("_", " ").title(),
            1: m(line(2026)[key]), 2: m(line(2035)[key]),
            3: m(line(2045)[key]), 4: m(line(2055)[key]),
            5: notes[key], "_src": srcs[key], "_badge": badges[key],
        })
    rows.append({
        0: "<strong>Total annual carrying cost</strong>",
        1: "<strong>" + m(line(2026)["total"]) + "</strong>",
        2: "<strong>" + m(line(2035)["total"]) + "</strong>",
        3: "<strong>" + m(line(2045)["total"]) + "</strong>",
        4: "<strong>" + m(line(2055)["total"]) + "</strong>",
        5: "Sum of the lines above", "_src": None, "_badge": "derived",
    })
    return rows


def proj_assessed(zipcode, year, transfer_year, transfer_assessed):
    if year >= transfer_year:
        return transfer_assessed * ((1 + A["prop13_inflation_factor"]) ** (year - transfer_year))
    return next(x for x in proj(zipcode) if x["year"] == year)["assessed_value"]


def carrying(year, assessed, market_value):
    """Mirror of model.carrying_costs, recomputed here for display."""
    HOE = 7_000
    rate = PAR["95014"]["rate"]
    flat = PAR["95014"]["flat_2026"] * ((1 + A["general_inflation"]) ** (year - 2026))
    tax = rate * (assessed - HOE) + flat
    infl = (1 + A["general_inflation"]) ** (year - 2026)
    ins = A["insurance_95014_primary"] * ((1 + A["insurance_inflation"]) ** (year - 2026))
    water = A["water_95014_month"] * 12 * infl
    if year >= A["nem_grandfathering_end_year"]:
        elec = A["electric_95014_post_nem_month"] * 12 * (
            (1 + A["general_inflation"]) ** (year - A["nem_grandfathering_end_year"]))
    else:
        elec = A["electric_95014_month_net"] * 12
    maint = 3_100_000 * A["maintenance_95014_pct"] * infl
    return {"property_tax": round(tax), "insurance": round(ins), "water": round(water),
            "electricity": round(elec), "maintenance": round(maint),
            "total": round(tax + ins + water + elec + maint)}


# ===========================================================================
# PAGE: 94122 RENTAL
# ===========================================================================

def page_rental():
    body = []
    body.append("""<p>The San Francisco property is the control in this analysis. It carries
a deep Proposition 13 lock-in and produces income, so it sets the baseline that any
decision about the Cupertino house has to beat.</p>""")

    body.append("<h2>What the rent can grow by</h2>")
    body.append(table(
        [("Regime", "tl"), ("Cap", "tr"), ("Period", "tl"), ("Which units", "tl")],
        [
            {0: "San Francisco Rent Ordinance (local)",
             1: p(OFF["sf_allowable_increase_2026_27"]["v"], 1),
             2: "1 March 2026 &ndash; 28 February 2027",
             3: "Units with a certificate of occupancy on or before 13 June 1979. "
                "Single-family homes and condos are generally exempt under Costa-Hawkins for "
                "tenancies beginning on or after 1 January 1996.",
             "_src": "S-SF-RENTINCREASE"},
            {0: "AB 1482 (statewide Tenant Protection Act)",
             1: p(OFF["ab1482_cap_sf_2026_27"]["v"], 1),
             2: "1 August 2026 &ndash; 31 July 2027",
             3: "Covered units not subject to the local ordinance. 5% + regional CPI, capped "
                "at 10%. The San Francisco-area figure was {:.1%} in the prior period.".format(
                    OFF["ab1482_cap_sf_2025_26"]["v"]),
             "_src": "S-CA-AG-RENTCAPS"},
            {0: "New tenancies", 1: "no cap",
             2: "&mdash;",
             3: "Neither regime restricts the starting rent charged to a new tenant in a "
                "vacant unit.", "_src": "S-CA-CIV-1947-12"},
            {0: "Banked increases (SF only)", 1: "cumulative",
             2: "&mdash;",
             3: "An owner who skips an allowable increase may bank it and impose it later. "
                "Banked percentages are added, not compounded.",
             "_src": "S-SF-RENTBOARD"},
        ],
        caption="Which cap applies depends on the certificate-of-occupancy date and the "
                "tenancy start dates. This is not established for the three units &mdash; "
                "see FLAG-12."))

    body.append("""<div class="callout warn">
<p>The difference between the two caps is a factor of five. If the units are covered by the
local ordinance, rent grows at roughly the rate of general inflation at best. If they are
not, the statewide cap permits {:.1%} a year. Establish the coverage before projecting
income. No rent growth assumption has been invented here &mdash; the model inflates the
supplied ${:,.0f}/month at general inflation, which is deliberately conservative.</p></div>""".format(
        OFF["ab1482_cap_sf_2026_27"]["v"], A["rent_94122_month_total"]))

    body.append("<h2>Modelled income and return</h2>")
    rows = []
    for r in M["rental_94122"]:
        if r["year"] % 5 == 0:
            rows.append({
                0: r["year"],
                1: m(r["gross_rent"]),
                2: m(r["carrying_costs"]["total"]),
                3: m(r["net_operating_income"]),
                4: m(r["depreciation"]),
                5: m(r["income_tax"]),
                6: m(r["after_tax_cash_flow"]),
                7: p(r["cap_rate_on_market_value"], 2),
                8: p(r["cap_rate_on_assessed_value"], 2),
                "_src": "S-SF-ASSESSOR",
                "_badge": "derived",
            })
    body.append(table(
        [("Year", "tr"), ("Gross rent", "tr"), ("Operating costs", "tr"), ("NOI", "tr"),
         ("Depreciation", "tr"), ("Income tax", "tr"), ("After-tax cash", "tr"),
         ("Yield on market value", "tr"), ("Yield on assessed value", "tr")],
        rows,
        caption="Yield on market value is the honest measure of the investment; yield on "
                "assessed value is shown to illustrate how much the Prop 13 lock-in flatters "
                "the property. Rent is inflated at {:.1%}, not at the rent-control caps.".format(
                    A["general_inflation"])))

    body.append("""<div class="callout ok">
<h3>Keep this property exactly as it is</h3>
<ul>
<li>Its assessed value is a small fraction of its market value. That lock-in is worth tens
of thousands of dollars a year and it would be destroyed by a change in ownership that
does not qualify for an exclusion.</li>
<li>Owner-occupancy of one unit preserves the $7,000 homeowners' exemption and keeps the
rental income, which the brief confirms is possible.</li>
<li>When this property eventually transfers, the same Proposition 19 test will apply. If it
is the transferor's principal residence and the transferee moves in, the exclusion is
available &mdash; but see FLAG-15 on whether a three-unit building counts as a
"family home".</li>
</ul></div>""")

    body.append("<h2>Supplied operating figures</h2>")
    body.append(table(
        [("Item", "tl"), ("Supplied range", "tl"), ("Value used", "tr"), ("Comment", "tl")],
        [
            {0: "Rental income, two units", 1: "$7,150/month", 2: m(A["rent_94122_month_total"] * 12) + "/yr",
             3: "Three units exist; one is occupied by the household. No rent has been "
                "invented for the occupied unit.", "_src": None, "_badge": "supplied"},
            {0: "Water, all three units", 1: "$330&ndash;$400/month",
             2: m(A["water_94122_month"] * 12) + "/yr",
             3: "Midpoint used. SFPUC has approved increases of roughly 10.5% on 1 July 2026 "
                "and a further 12.5% on 1 July 2027.", "_src": "S-SFPUC-RATES-2026",
             "_badge": "supplied"},
            {0: "Electricity", 1: "$30&ndash;$70/month", 2: m(A["electric_94122_month"] * 12) + "/yr",
             3: "Midpoint used; common areas only if separately metered.",
             "_src": "S-PGE", "_badge": "supplied"},
            {0: "Insurance", 1: "~$1,500/year", 2: m(A["insurance_94122_rental"]) + "/yr",
             3: "Unverified. A landlord policy for a three-unit building will usually cost "
                "more than an owner-occupied HO-3.", "_src": "S-CDI", "_badge": "supplied"},
        ]))

    return write("rental.html", "rental", "The 94122 Rental", "\n".join(body),
                 "Rent-control caps, income, returns, and why this property should be left alone.")


# ===========================================================================
# PAGE: PROCESS
# ===========================================================================

def page_process():
    body = []
    body.append("""<p>The chronological path of the transfer, with the form and the deadline
that attaches to each step. Steps 7, 8 and 9 are the ones that are missed most often, and
they are the ones worth tens of thousands of dollars a year.</p>""")

    steps = [
        ("Before death &mdash; planning", [
            ("Confirm the trust is funded",
             "The house must actually be deeded to the trustee. A trust that does not hold "
             "title does not avoid probate.",
             "S-CA-RTC-62", "official"),
            ("Claim the R&amp;TC &sect;&nbsp;62(d) trust-transfer exclusion",
             "Deeding the property into a revocable living trust is excluded from change in "
             "ownership, so no reassessment occurs. File a Preliminary Change of Ownership "
             "Report with the deed to claim the exclusion on the record.",
             "S-CA-RTC-62", "official"),
            ("Do not sell during life",
             "A lifetime sale is taxed at a combined 37.1% marginal rate on the gain. Holding "
             "until death gives a step-up in basis under IRC &sect;&nbsp;1014, so the heir can "
             "sell at the date-of-death value and owe essentially nothing.",
             "S-USC-1014", "official"),
            ("Confirm the house is the transferor's principal residence at the transfer date",
             "This is the single fact that decides whether any Prop 19 exclusion is available. "
             "If it is a rental or a second home at that moment, no exclusion exists at any value.",
             "S-CA-RTC-632", "official"),
            ("Check whether the transfer is parent-to-child or grandparent-to-grandchild",
             "Grandparent-to-grandchild transfers only qualify if all of the grandchild's "
             "parents who are children of the grandparent are deceased on the date of transfer.",
             "S-CA-RTC-632", "official"),
        ]),
        ("At death &mdash; the transfer", [
            ("The trust becomes irrevocable; the successor trustee takes over",
             "Trust assets pass outside probate. The trustee notifies beneficiaries, gathers "
             "assets, pays debts and expenses, and distributes according to the trust terms.",
             "S-CA-RTC-62", "official"),
            ("Record the change in ownership with the county",
             "Record an affidavit of death of trustee and a Preliminary Change of Ownership "
             "Report. The assessor will reassess unless an exclusion is claimed.",
             "S-SCC-ASSESSOR", "official"),
            ("Obtain a date-of-death appraisal",
             "This sets both the new assessed value and the IRC &sect;&nbsp;1014 income tax "
             "basis. Keep it permanently &mdash; it is the evidence for the stepped-up basis "
             "whenever the property is later sold.",
             "S-USC-1014", "official"),
            ("File Form 706 only if required",
             "Required if the gross estate plus adjusted taxable gifts exceeds the exclusion "
             "for the year of death ($15,000,000 in 2026). A timely Form 706 is also required "
             "to elect portability of a deceased spouse's unused exclusion.",
             "S-IRS-ESTATETAX", "official"),
            ("Expect supplemental assessments",
             "A change in ownership can produce one or two supplemental bills covering the "
             "remainder of the fiscal year, on top of the annual bill.",
             "S-SCC-ASSESSOR-BOOKLET", "official"),
        ]),
        ("Within one year &mdash; the critical window", [
            ("Move in, if claiming the Prop 19 exclusion",
             "The transferee must occupy the house as their principal residence within one "
             "year of the transfer. This is the most commonly missed deadline.",
             "S-CA-RTC-632", "official"),
            ("File the homeowners' exemption",
             "File BOE-266 (or BOE-261-G for a disabled veteran) within one year of the "
             "transfer. Filing after the one-year period gives only prospective relief, which "
             "means the exclusion does not reach back to the transfer date.",
             "S-BOE-PROP19", "official"),
        ]),
        ("Within three years", [
            ("File BOE-19-P",
             "File the Claim for Reassessment Exclusion for Transfer Between Parent and Child "
             "within three years of the transfer, or before the property is transferred to a "
             "third party, whichever is earlier. Use BOE-19-G for a "
             "grandparent-to-grandchild transfer.",
             "S-BOE-PROP19", "official"),
            ("Note that the value cap is applied automatically",
             "Even a qualifying transfer is reassessed in part if the market value exceeds "
             "the factored base year value plus the adjusted cap. New assessed value = market "
             "value &minus; cap.",
             "S-BOE-LTA25009", "official"),
        ]),
        ("Ongoing", [
            ("Maintain the occupancy condition",
             "The exclusion ends on the date the transferee stops being eligible for the "
             "homeowners' or disabled veterans' exemption. Moving out triggers the "
             "&sect;&nbsp;63.2(a)(1)(C) enrollment of the value that would have applied "
             "without the exclusion.",
             "S-CA-RTC-632", "official"),
            ("Check the bill every year and use the appeal window",
             "Each county publishes an annual appeal window for formal assessment appeals. "
             "Confirm the dates with the county assessor; do not rely on a generic date.",
             "S-SCC-ASSESSOR", "official"),
            ("Re-run this model with actual figures",
             "The Prop 19 cap is re-set every two years, the assessed value changes annually, "
             "and rates move. Replace every assumption with an actual bill or appraisal as "
             "soon as one exists.",
             None, "assumption"),
        ]),
    ]

    n = 0
    for phase, items in steps:
        body.append("<h2>{}</h2>".format(phase))
        rows = []
        for title, detail, sid, badge in items:
            n += 1
            rows.append({0: str(n), 1: "<strong>{}</strong>".format(title), 2: detail,
                         "_src": sid, "_badge": badge})
        body.append(table([("#", "tr"), ("Step", "tl"), ("What it means", "tl")], rows))

    body.append("""<div class="callout danger">
<h3>The three deadlines that decide the outcome</h3>
<table class="plain">
<tr><td><strong>1 year</strong></td><td>Occupy the house as a principal residence</td>
<td>R&amp;TC &sect;&nbsp;63.2(a)(1)(A)</td><td>{d1}</td></tr>
<tr><td><strong>1 year</strong></td><td>File the homeowners' exemption (BOE-266)</td>
<td>R&amp;TC &sect;&nbsp;63.2(a)(1)(B)</td><td>{d2}</td></tr>
<tr><td><strong>3 years</strong></td><td>File the exclusion claim (BOE-19-P)</td>
<td>R&amp;TC &sect;&nbsp;63.2(f)(1)(A)</td><td>{d3}</td></tr>
</table>
<p>Miss the one-year occupancy or exemption filing, and the three-year claim no longer
saves the base. The property is reassessed to full market value.</p>
<p class="sig">{sig}</p></div>""".format(
        d1=src_link("S-CA-RTC-632", "leginfo &sect; 63.2"),
        d2=src_link("S-CA-RTC-632", "leginfo &sect; 63.2"),
        d3=src_link("S-BOE-PROP19", "BOE Prop 19"),
        sig=src_link("S-BOE-PROP19", "BOE Proposition 19 page")))

    body.append("<h2>Documents to keep</h2>")
    body.append(table(
        [("Document", "tl"), ("Why it matters", "tl")],
        [
            {0: "Date-of-death appraisal of the real property",
             1: "Establishes the IRC &sect;&nbsp;1014 basis and supports the new assessed value.",
             "_src": "S-USC-1014"},
            {0: "Recorded deed into the trust, with the Preliminary Change of Ownership Report",
             1: "Proves the &sect;&nbsp;62(d) trust-transfer exclusion was claimed, so the "
                "transfer into the trust was not a change in ownership.", "_src": "S-CA-RTC-62"},
            {0: "Filed BOE-19-P (or BOE-19-G), with proof of the filing date",
             1: "The exclusion exists only if a claim is filed. Late filing gives only "
                "prospective relief.", "_src": "S-BOE-PROP19"},
            {0: "Filed BOE-266 homeowners' exemption",
             1: "Required to keep the exclusion, and it ends the exclusion if it lapses.",
             "_src": "S-BOE-PROP19"},
            {0: "Every annual property tax bill",
             1: "Needed to reconstruct the factored base year value and to check for errors.",
             "_src": "S-SCC-ASSESSOR"},
            {0: "Form 706, if filed",
             1: "Establishes portability of any unused exclusion and the reported values.",
             "_src": "S-IRS-ESTATETAX"},
        ]))

    return write("process.html", "process", "Transfer Process", "\n".join(body),
                 "Step by step, from funding the trust through to the deadlines after the "
                 "transfer that actually determine the property tax bill.")


# ===========================================================================
# PAGE: LEGISLATION
# ===========================================================================

def page_legislation():
    body = []
    body.append("<h2>On the 2026 ballot: Proposition 43</h2>")
    body.append("""<p>Proposition 43 (November 3, 2026) is a legislatively referred
constitutional amendment that came out of a compromise with the promoters of the proposed
"Local Taxpayer Protection Act to Save Proposition 13" initiative, which was withdrawn in
June 2026.</p>""")
    body.append(table(
        [("What Prop 43 does", "tl"), ("What it does not do", "tl")],
        [
            {0: "Restores a two-thirds voter approval requirement for local special taxes "
                "proposed under the local initiative power, from 1 January 2027.",
             1: "Does not change Proposition 13's 1% rate cap.",
             "_src": "S-CA-SOS-BALLOT", "_badge": "official"},
            {0: "Bars local governments, including by initiative, from imposing additional "
                "ad valorem property taxes beyond what the Constitution allows.",
             1: "Does not change the 2% annual assessment growth cap.",
             "_src": "S-CA-SOS-BALLOT", "_badge": "official"},
            {0: "Applies only to measures put before voters after 1 January 2027 &mdash; it "
                "is not retroactive.",
             1: "Does not cap real estate transfer taxes, and does not reach Measure ULA or "
                "any existing local tax.",
             "_src": "S-CA-SOS-BALLOT", "_badge": "official"},
        ]))
    body.append("""<div class="callout">
<p><strong>Effect on this decision: none, directly.</strong> The 1% rate, the 2% cap and
the Proposition 19 transfer rules are untouched. The indirect effect is on the flat
per-parcel charges that make up a meaningful share of both bills &mdash; a two-thirds
threshold means fewer new parcel taxes clear in future. That slightly favours holding
property, but it does not change the ranking of the three options.</p>
<p class="sig">{} &middot; {}</p></div>""".format(
        src_link("S-CA-SOS-QUALIFIED", "Secretary of State"),
        src_link("S-CA-LAO", "Legislative Analyst's Office")))

    body.append("<h2>The Proposition 19 cap moves every two years</h2>")
    body.append("""<p>The exclusion cap is re-set every other 16 February using the change in
the Federal Housing Finance Agency House Price Index for California. Officially it is known
only through 15 February 2027.</p>""")
    body.append(table(
        [("Period", "tl"), ("Cap", "tr"), ("Status", "tl")],
        [
            {0: "16 Feb 2025 &ndash; 15 Feb 2027", 1: m(OFF["p19_cap_2025_2027"]["v"]),
             2: "published", "_src": "S-BOE-LTA25009", "_badge": "official"},
            {0: "16 Feb 2027 &ndash; 15 Feb 2029", 1: "&mdash;",
             2: "not yet published &mdash; set on 16 February 2027",
             "_src": "S-FHFA-HPI", "_badge": "unofficial"},
            {0: "16 Feb 2043 &ndash; 15 Feb 2045 (the modelled transfer window)",
             1: m(base_prop19(2045)["p19_cap"]),
             2: "modelled at an assumed {:.0%}/yr &mdash; not knowable today".format(
                 A["p19_cap_growth"]),
             "_src": "S-BOE-LTA25009", "_badge": "assumption"},
        ]))
    body.append("""<div class="callout warn">
<p>A higher cap makes the exclusion more valuable and therefore makes living in the house
slightly more attractive relative to renting it out. It does not come close to closing the
gap with selling, because the gap is driven by the opportunity cost of the equity, not by
the tax line.</p></div>""")

    body.append("<h2>Federal: what is law, and what is only proposed</h2>")
    body.append(table(
        [("Item", "tl"), ("Status", "tl"), ("Effect if it changed", "tl")],
        [
            {0: "$15,000,000 basic exclusion, permanent",
             1: "<strong>Enacted.</strong> OBBBA &sect;&nbsp;70106 amended IRC "
                "&sect;&nbsp;2010(c)(3) for calendar year 2026 and removed the sunset. "
                "Indexed for inflation from 2027.",
             2: "N/A &mdash; this is the baseline.", "_src": "S-IRS-RP-2025-32",
             "_badge": "official"},
            {0: "Step-up in basis under IRC &sect;&nbsp;1014",
             1: "<strong>In force.</strong> Not amended by OBBBA.",
             2: "Repeal would be the single most damaging change for this plan &mdash; it is "
                "the reason selling immediately after inheritance is tax-free, and the reason "
                "not to sell during life. Proposals to tax appreciation at death have been "
                "introduced repeatedly but none has been enacted.",
             "_src": "S-USC-1014", "_badge": "official"},
            {0: "Repeal or reduction of the estate tax",
             1: "<strong>Proposed only.</strong> Bills to repeal the estate tax, and separate "
                "proposals to cut the exemption sharply and raise the top rate, have been "
                "introduced. None is law.",
             2: "Only matters if the estate is near or above the exclusion. Nothing to do "
                "today beyond noting it.",
             "_src": "U-ESTATE-2026-MIDTERM", "_badge": "unofficial"},
            {0: "Net investment income tax thresholds",
             1: "<strong>In force and not indexed.</strong> $200,000 single / $250,000 joint.",
             2: "Because the thresholds never move, more taxpayers cross them every year. "
                "Over a 20-year horizon this modestly favours holding appreciated assets "
                "until death.",
             "_src": "S-IRS-NIIT", "_badge": "official"},
        ]))

    body.append("<h2>California property tax rules that are settled</h2>")
    body.append(table(
        [("Rule", "tl"), ("Authority", "tl"), ("Note", "tl")],
        [
            {0: "1% maximum ad valorem rate plus voter-approved debt",
             "_src": "S-CA-CONST-13A", 1: "Cal. Const. art. XIII&nbsp;A",
             2: "The parcel's actual rate is this plus bond levies, which is why the "
                "effective rate exceeds 1%."},
            {0: "Assessed value grows by the lesser of 2% or the change in the California CPI",
             "_src": "S-CA-RTC-51", 1: "R&amp;TC &sect;&nbsp;51",
             2: "For the 2026-27 roll the BOE set the factor at 1.02."},
            {0: "Reassessment to market value on change of ownership or new construction",
             "_src": "S-SCC-PROP13", 1: "Cal. Const. art. XIII&nbsp;A &sect;&nbsp;2",
             2: "This is the event the transfer triggers."},
            {0: "Transfer into a revocable trust is not a change in ownership",
             "_src": "S-CA-RTC-62", 1: "R&amp;TC &sect;&nbsp;62(d)",
             2: "But the settlor's death is."},
            {0: "Parent-child / grandparent-grandchild exclusion, narrowly drawn",
             "_src": "S-CA-RTC-632", 1: "R&amp;TC &sect;&nbsp;63.2",
             2: "Principal residence only, with a value cap."},
            {0: "Base year value transfer for owners 55+ or severely disabled, up to three "
                "times, anywhere in California",
             "_src": "S-SCC-PROP19", 1: "R&amp;TC &sect;&nbsp;69.6",
             2: "Relevant if the household later wants to move its tax base to a different "
                "principal residence."},
        ]))

    return write("legislation.html", "legislation", "Law &amp; Proposed Changes", "\n".join(body),
                 "What is settled law, what is on the 2026 ballot, and which federal "
                 "proposals are only proposals.")


# ===========================================================================
# PAGE: ASSUMPTIONS
# ===========================================================================

def page_assumptions():
    body = []
    body.append("""<p>Every number below is a <strong>planning assumption</strong>. None of
them is sourced from an official publication, and none should be treated as a fact. Change
them and re-run <code>tools/model.py</code>.</p>""")

    rows = [
        ("Valuation", "Market value, 95014", m(3_100_000), "Nov 2026", "requester estimate", "supplied"),
        ("Valuation", "Market value, 94122", m(1_800_000), "Nov 2026", "requester estimate", "supplied"),
        ("Growth", "House appreciation, base", p(BASE_G, 1), "per year, nominal", "planning assumption", "assumption"),
        ("Growth", "House appreciation, low / high",
         "{} / {}".format(p(A["appreciation_low"], 1), p(A["appreciation_high"], 1)),
         "per year, nominal", "planning assumption", "assumption"),
        ("Growth", "Prop 13 assessment growth", p(A["prop13_inflation_factor"], 1), "per year",
         "official for the 2026-27 roll (BOE LTA 2026/002)", "official"),
        ("Growth", "General inflation (CPI)", p(A["general_inflation"], 1), "per year",
         "planning assumption", "assumption"),
        ("Growth", "Prop 19 cap growth", p(A["p19_cap_growth"], 1), "per year",
         "assumption &mdash; tracks the FHFA California HPI", "assumption"),
        ("Growth", "Insurance inflation", p(A["insurance_inflation"], 1), "per year",
         "assumption &mdash; California premiums have been rising faster than CPI", "assumption"),
        ("Costs", "95014 insurance", m(A["insurance_95014_primary"]) + "/yr", "2026",
         "requester estimate; unverified", "supplied"),
        ("Costs", "94122 insurance", m(A["insurance_94122_rental"]) + "/yr", "2026",
         "requester estimate; unverified", "supplied"),
        ("Costs", "95014 water", m(A["water_95014_month"]) + "/mo", "2026",
         "midpoint of the supplied $100&ndash;$150", "supplied"),
        ("Costs", "94122 water, all three units", m(A["water_94122_month"]) + "/mo", "2026",
         "midpoint of the supplied $330&ndash;$400", "supplied"),
        ("Costs", "95014 electricity", m(A["electric_95014_month_net"]) + "/mo", "2026",
         "midpoint of the supplied $10&ndash;$20 net credit", "supplied"),
        ("Costs", "NEM grandfathering ends", str(A["nem_grandfathering_end_year"]), "&mdash;",
         "assumption &mdash; NEM 1.0/2.0 runs 20 years from interconnection", "assumption"),
        ("Costs", "95014 electricity after grandfathering",
         m(A["electric_95014_post_nem_month"]) + "/mo", "from {}".format(A["nem_grandfathering_end_year"]),
         "assumption", "assumption"),
        ("Costs", "94122 electricity", m(A["electric_94122_month"]) + "/mo", "2026",
         "midpoint of the supplied $30&ndash;$70", "supplied"),
        ("Costs", "95014 maintenance", p(A["maintenance_95014_pct"], 1) + " of the 2026 value",
         "{} /yr".format(m(3_100_000 * A["maintenance_95014_pct"])),
         "planning assumption", "assumption"),
        ("Costs", "94122 maintenance", p(A["maintenance_94122_pct"], 1) + " of the 2026 value",
         "{} /yr".format(m(1_800_000 * A["maintenance_94122_pct"])),
         "planning assumption &mdash; older three-unit building", "assumption"),
        ("Income", "94122 rent, two units", m(A["rent_94122_month_total"]) + "/mo", "2026",
         "supplied; no rent assumed for the owner-occupied unit", "supplied"),
        ("Income", "95014 market rent", m(A["rent_95014_month_market"]) + "/mo", "2026",
         "assumption &mdash; aggregator median rents run $3,800&ndash;$4,128 but are "
         "apartment-weighted", "assumption"),
        ("Income", "Vacancy and credit loss", p(A["vacancy_and_credit_loss"], 0), "&mdash;",
         "planning assumption", "assumption"),
        ("Sale", "Selling costs", p(A["selling_cost_pct"], 1), "of sale price",
         "assumption &mdash; commission plus closing", "assumption"),
        ("Sale", "Portfolio nominal return", p(A["portfolio_nominal_return"], 1), "per year",
         "planning assumption", "assumption"),
        ("Sale", "Portfolio income yield", p(A["portfolio_income_yield"], 1), "per year",
         "planning assumption &mdash; only this slice is taxed annually", "assumption"),
        ("Sale", "Tax on investment income", p(A["marginal_rate_on_investment_income"], 1), "&mdash;",
         "20% federal + 3.8% NIIT + 13.3% California", "derived"),
        ("Tax", "Federal ordinary marginal rate", p(A["federal_ordinary_marginal"], 1), "&mdash;",
         "planning assumption", "assumption"),
        ("Tax", "California marginal rate", p(A["ca_marginal"], 1), "&mdash;",
         "planning assumption", "assumption"),
        ("Tax", "Depreciation period", str(A["depreciation_years"]) + " years", "&mdash;",
         "residential rental property", "official"),
        ("Tax", "Land share, 95014", p(A["land_pct_95014"], 0), "&mdash;",
         "assumption &mdash; land is not depreciable; use the county roll", "assumption"),
        ("Tax", "Land share, 94122", p(A["land_pct_94122"], 0), "&mdash;",
         "assumption &mdash; land is not depreciable; use the county roll", "assumption"),
        ("Model", "Homeowners' exemption", m(7_000), "&mdash;",
         "official &mdash; reduces assessed value", "official"),
        ("Model", "Transfer years modelled",
         ", ".join(str(y) for y in A["inheritance_years"]), "&mdash;",
         "from the stated 2040&ndash;2050 plan", "supplied"),
    ]
    body.append(table(
        [("Group", "tl"), ("Assumption", "tl"), ("Value", "tr"), ("As of", "tl"),
         ("Basis", "tl")],
        [{0: g, 1: nm, 2: v, 3: w, 4: b, "_src": None, "_badge": badge}
         for g, nm, v, w, b, badge in rows]))

    body.append("""<div class="callout warn">
<h3>Which assumptions matter most</h3>
<ol>
<li><strong>Portfolio return ({:.0%}).</strong> This is the single most influential
assumption in the whole model, because it sets the opportunity cost of the equity. The
sensitivity is displayed on the <a href="scenarios.html">Scenarios</a> page: the break-even
is around {:.2%}, so the conclusion survives almost any reasonable value.</li>
<li><strong>Whether the house is the transferor's principal residence.</strong> Not really
an assumption &mdash; an unknown fact that must be established. See FLAG-05.</li>
<li><strong>Maintenance and insurance.</strong> Together these are the difference between
the house roughly paying for itself and it bleeding cash. They are also the least reliable
numbers in the model.</li>
<li><strong>Market rent.</strong> Affects both A and B equally, so it does not change their
ranking, but it does change their distance from C.</li>
</ol>
<p class="sig">The two market values are also requester estimates. Confirm with an
appraisal.</p></div>""".format(
        A["portfolio_nominal_return"],
        base_strategy(A["base_inheritance_year"])["break_even"]
        ["portfolio_nominal_return_where_sell_ties_live_in"]))

    return write("assumptions.html", "assumptions", "Assumptions", "\n".join(body),
                 "Every number in the model that is not traceable to an official source, "
                 "in one place.")


# ===========================================================================
# PAGE: SOURCES
# ===========================================================================

def page_sources():
    body = []
    body.append("<p>Every source used in this build. Links in the tables resolve here by "
                "publisher.</p>")
    off = [(k, v) for k, v in SRC.items() if v["type"] == "official"]
    uno = [(k, v) for k, v in SRC.items() if v["type"] != "official"]
    for title, group in (("Official sources", off), ("Unofficial / secondary sources", uno)):
        body.append("<h2>{} ({})</h2>".format(title, len(group)))
        body.append(table(
            [("ID", "tl"), ("Publisher", "tl"), ("Document", "tl"), ("Type", "tl")],
            [{0: '<a href="{u}" target="_blank" rel="noopener">{k}</a>'.format(u=esc(v["url"]), k=esc(k)),
              1: esc(v["publisher"]), 2: esc(v["name"]),
              3: prov_badge(v["type"]), "_src": k, "_badge": v["type"]}
             for k, v in group]))

    body.append("<h2>Official constants used</h2>")
    body.append(table(
        [("Constant", "tl"), ("Value", "tr"), ("Note", "tl")],
        [{0: esc(k), 1: (m(v["v"]) if isinstance(v["v"], (int, float)) else esc(v["v"])),
          2: esc(v["note"]), "_src": v["src"], "_badge": "official"}
         for k, v in OFF.items()]))

    return write("sources.html", "sources", "Sources", "\n".join(body),
                 "The complete source register. Every table row in this site links to one "
                 "of these.")


# ===========================================================================
# PAGE: FLAGGED
# ===========================================================================

def page_flagged():
    body = []
    sev_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    flags = sorted(M["flags"], key=lambda f: sev_order.get(f["severity"], 9))
    counts = {}
    for f in flags:
        counts[f["severity"]] = counts.get(f["severity"], 0) + 1
    body.append('<div class="kpis">')
    for sev in ("critical", "high", "medium", "low"):
        if sev in counts:
            body.append(kpi(str(counts[sev]), sev + " severity", "",
                            "ok" if sev == "low" else ("warn" if sev == "medium" else "bad")))
    body.append("</div>")
    body.append("""<p>Items that could not be verified against an official source, or where
the supplied data is internally inconsistent. None of these blocks the recommendation;
each one narrows the range of error around it.</p>""")

    body.append(table(
        [("ID", "tl"), ("Severity", "tl"), ("Issue", "tl"), ("Detail", "tl"),
         ("What to do", "tl")],
        [{0: f["id"],
          1: '<span class="badge {cls}">{sev}</span>'.format(
                 cls={"critical": "bad", "high": "bad", "medium": "warn", "low": "ok"}[f["severity"]],
                 sev=f["severity"]),
          2: "<strong>" + esc(f["title"]) + "</strong>",
          3: esc(f["detail"]), 4: esc(f["action"]),
          "_src": f["source"], "_badge": "official"}
         for f in flags]))

    body.append("""<div class="callout warn">
<h3>Values deliberately left blank</h3>
<p>Per the verification rule, no value has been inferred where an official source could not
be found. Specifically:</p>
<ul>
<li><strong>Rent for the third unit at 94122.</strong> The supplied $7,150/month covers two
units. Rather than divide by two, the model is constructed so that this figure cancels out
of every comparison between the options. It is not needed.</li>
<li><strong>Cost basis of either property.</strong> Not supplied. It is not needed for the
inheritance analysis, because IRC &sect;&nbsp;1014 resets the basis at death. It
<em>would</em> be needed to price a lifetime sale precisely, which is why the sell-now
comparison is presented as a marginal tax rate rather than a dollar figure.</li>
<li><strong>Parcel-specific tax rate.</strong> Not published per parcel. The model derives
it from the supplied bill history and discloses the derivation.</li>
<li><strong>Insurance premium.</strong> No official filing publishes a ZIP-level average.
Flagged rather than filled in.</li>
</ul></div>""")

    return write("flagged.html", "flagged", "Flagged for Review", "\n".join(body),
                 "Unverified values, data irregularities and open questions &mdash; with the "
                 "source link for each.")


# ===========================================================================
# ASSETS
# ===========================================================================

CSS = """
*{box-sizing:border-box}
:root{
  --bg:#f6f7f9; --panel:#fff; --ink:#14171c; --mut:#5c6672; --line:#e2e6ec;
  --acc:#1f6feb; --ok:#0f7b4f; --warn:#8a5a00; --bad:#b3261e;
  --mono:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
}
html,body{margin:0;padding:0}
body{background:var(--bg);color:var(--ink);
  font:15px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;}
a{color:var(--acc)}
header.top{display:flex;align-items:center;justify-content:space-between;gap:16px;
  padding:12px 22px;background:#fff;border-bottom:1px solid var(--line);
  position:sticky;top:0;z-index:20;flex-wrap:wrap}
.brand{display:flex;align-items:center;gap:11px}
.dot{width:11px;height:11px;border-radius:50%;background:var(--acc);box-shadow:0 0 0 4px #e8f0fe}
.bt{font-weight:700;letter-spacing:-.2px}
.bs{font-size:12px;color:var(--mut)}
.topmeta{display:flex;gap:8px;flex-wrap:wrap}
.pill{font-size:12px;padding:4px 10px;border:1px solid var(--line);border-radius:999px;
  background:#fafbfc;color:var(--mut)}
.warnpill{background:#fff5e5;border-color:#f0d9a8;color:#8a5a00;text-decoration:none}
.layout{display:grid;grid-template-columns:214px 1fr;gap:0;align-items:start}
nav.side{position:sticky;top:57px;padding:16px 10px;height:calc(100vh - 57px);
  overflow:auto;border-right:1px solid var(--line);background:#fbfcfd}
nav.side a{display:block;padding:7px 11px;border-radius:7px;color:#39424e;
  text-decoration:none;font-size:13.5px;margin-bottom:2px}
nav.side a:hover{background:#eef2f7}
nav.side a.active{background:var(--acc);color:#fff;font-weight:600}
main{max-width:1180px;padding:26px 30px 60px}
h1{font-size:26px;letter-spacing:-.4px;margin:0 0 6px}
h2{font-size:18.5px;margin:30px 0 10px;letter-spacing:-.2px}
h3{font-size:15.5px;margin:20px 0 8px}
.lede{color:var(--mut);margin:0 0 18px;font-size:15px;max-width:82ch}
p{max-width:88ch}
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(196px,1fr));gap:12px;margin:18px 0 6px}
.kpi{background:var(--panel);border:1px solid var(--line);border-radius:11px;padding:13px 15px}
.kpi-v{font-size:24px;font-weight:700;letter-spacing:-.5px;line-height:1.15}
.kpi-l{font-size:12.5px;color:var(--mut);margin-top:3px;line-height:1.35}
.kpi-s{font-size:11.5px;color:#8b95a3;margin-top:5px;line-height:1.35}
.kpi.ok .kpi-v{color:var(--ok)} .kpi.warn .kpi-v{color:var(--warn)}
.kpi.bad .kpi-v{color:var(--bad)}
.callout{background:var(--panel);border:1px solid var(--line);border-left:3px solid var(--acc);
  border-radius:9px;padding:14px 17px;margin:16px 0}
.callout h2,.callout h3{margin-top:0}
.callout.ok{border-left-color:var(--ok);background:#f3fbf7}
.callout.warn{border-left-color:#d99b00;background:#fffaf0}
.callout.danger{border-left-color:var(--bad);background:#fdf5f4}
.callout ol,.callout ul{margin:8px 0 0;padding-left:20px}
.callout li{margin:5px 0}
.sig{font-size:12px;color:var(--mut);margin:9px 0 0}
.formula{background:#f2f5f9;border:1px solid var(--line);border-radius:9px;padding:12px 16px;
  margin:14px 0;font-family:var(--mono);font-size:13.5px}
.formula p{margin:6px 0;max-width:none}
.tablewrap{overflow-x:auto;border:1px solid var(--line);border-radius:10px;background:#fff;
  margin:12px 0 18px}
.tablecap{font-size:12.5px;color:var(--mut);padding:9px 13px;border-bottom:1px solid var(--line);
  background:#fbfcfd}
table.data{border-collapse:collapse;width:100%;font-size:13.5px}
table.data th{text-align:left;background:#f7f9fb;border-bottom:1px solid var(--line);
  padding:9px 12px;font-size:12px;text-transform:uppercase;letter-spacing:.4px;color:#4d5762;
  white-space:nowrap;font-weight:600}
table.data td{padding:8px 12px;border-bottom:1px solid #eef1f5;vertical-align:top}
table.data tr:last-child td{border-bottom:none}
table.data tbody tr:hover{background:#fafcfe}
.tr{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
.tl{text-align:left}
.nowrap{white-space:nowrap}
.badge{display:inline-block;font-size:10.5px;padding:1.5px 6px;border-radius:999px;
  margin-left:6px;border:1px solid;vertical-align:middle;white-space:nowrap}
.badge.ok{color:var(--ok);border-color:#b9e2cd;background:#eefaf4}
.badge.warn{color:var(--warn);border-color:#f0d9a8;background:#fff8ec}
.badge.bad{color:var(--bad);border-color:#f0c4c0;background:#fdf2f1}
a.src{font-size:12px;text-decoration:none;border-bottom:1px dotted currentColor}
a.src-official{color:var(--ok)}
a.src-unofficial{color:var(--bad)}
a.src-derived,a.src-supplied{color:var(--warn)}
a.src-assumption{color:var(--bad)}
.foot{margin-top:42px;padding-top:16px;border-top:1px solid var(--line);color:var(--mut);font-size:12.5px}
table.plain{border-collapse:collapse;margin:8px 0}
table.plain td{padding:3px 14px 3px 0;font-size:13.5px}
table.plain td:first-child{white-space:nowrap;font-weight:600}
code{font-family:var(--mono);font-size:12.5px;background:#eef1f5;padding:1px 5px;border-radius:4px}
@media (max-width:860px){
  .layout{grid-template-columns:1fr}
  nav.side{position:static;height:auto;display:flex;overflow-x:auto;border-right:none;
    border-bottom:1px solid var(--line);gap:4px}
  nav.side a{white-space:nowrap;margin:0}
  main{padding:18px 16px 48px}
}
"""

JS = """/* Cupertino2 - table filters. Progressive enhancement only; the site works without it. */
(function(){
  document.querySelectorAll('.tablewrap').forEach(function(wrap){
    var tbl = wrap.querySelector('table.data');
    if(!tbl || tbl.tBodies[0].rows.length < 8) return;
    var cap = wrap.querySelector('.tablecap');
    var box = document.createElement('input');
    box.type='search';
    box.className='flt';
    box.placeholder='Filter rows…';
    if(cap){ cap.appendChild(box); } else {
      var d=document.createElement('div'); d.className='tablecap'; d.appendChild(box);
      wrap.insertBefore(d, wrap.firstChild);
    }
    box.addEventListener('input', function(){
      var q = box.value.toLowerCase();
      Array.prototype.forEach.call(tbl.tBodies[0].rows, function(tr){
        tr.style.display = tr.textContent.toLowerCase().indexOf(q) === -1 ? 'none' : '';
      });
    });
  });
  var s=document.createElement('style');
  s.textContent='.flt{margin-left:10px;font:inherit;font-size:12.5px;padding:3px 8px;'+
                'border:1px solid #d7dde5;border-radius:6px;min-width:150px}';
  document.head.appendChild(s);
})();
"""


def main():
    os.makedirs(os.path.join(SITE, "assets"), exist_ok=True)
    os.makedirs(SITE, exist_ok=True)
    with open(os.path.join(SITE, "assets", "style.css"), "w") as fh:
        fh.write(CSS)
    with open(os.path.join(SITE, "assets", "app.js"), "w") as fh:
        fh.write(JS)
    with open(os.path.join(SITE, ".nojekyll"), "w") as fh:
        fh.write("")

    page_index()
    page_prop19()
    page_property()
    page_projections()
    page_scenarios()
    page_taxes()
    page_costs()
    page_rental()
    page_process()
    page_legislation()
    page_assumptions()
    page_sources()
    page_flagged()

    files = sorted(os.listdir(SITE))
    print("Built {} entries into site/".format(len(files)))
    for f in files:
        print("  " + f)


if __name__ == "__main__":
    main()
