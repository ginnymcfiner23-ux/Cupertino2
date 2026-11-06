# Property Transition Guide

A privacy-safe, source-cited decision guide for a planned inheritance involving one residence (Home A) and a separate multi-unit rental property (Home B). It compares living in, renting, or selling Home A and reinvesting, while keeping Home B as a separate operating baseline.

## Site and deployment

- Public URL: `https://ginnymcfiner23-ux.github.io/Cupertino2/`
- GitHub Pages is currently configured for the legacy `main`-branch root source. An attempt to switch the Pages build type to GitHub Actions returned HTTP 403 (`Resource not accessible by integration`), so this project retains the existing legacy source.
- The root `_config.yml` excludes prior research/data directories and development files from the Jekyll site output. The GitHub Actions workflow builds that same Jekyll output on pull requests and pushes, then fails if excluded directories or structured data appear in the rendered site. It is a validation workflow, not a Pages deployment job; GitHub Pages automatically rebuilds from `main` after merge.
- Deployment status: **not yet verified for this implementation**. The new post-merge Pages build and public URL must be checked before claiming success.
- Start at [`index.html`](index.html). The guide includes decision paths, costs/rent, tax rules, inheritance steps, the 2040–2050 outlook, review flags, and official sources.

## Privacy and evidence standard

- Public pages use **Home A** and **Home B** only. They do not publish names, addresses, ZIP codes, parcel numbers, owner identities, private property values, assessed values, tax bills, rents, utility bills or credits, insurance estimates, or maintenance figures.
- All user-supplied property-specific figures are treated as unverified and intentionally omitted from this guide. Unsupported future amounts are left blank rather than inferred.
- Every data row in a table links directly to an official source. The guide distinguishes current law and published amounts from future uncertainty; it does not present a 2040–2050 property-value, rent, premium, utility-cost, maintenance-cost, or investment-return forecast.
- The optional scenario worksheet runs in the visitor's browser only. It starts blank, uses no storage or analytics, and sends no input to a server. It is an illustration, not a tax calculator or forecast.
- Local agency links are jurisdiction-specific references, not confirmation of either home's location or of a rule's applicability. Verify location, unit coverage, title, and the rules in effect at the actual transfer date.
- Earlier research files under `docs/`, `data/`, and `pages/` are retained in the repository but are excluded from the new Pages output. This change does not rewrite or scrub previous Git history; repository history should not be treated as a private store.
- The current Santa Clara County Assessor guidance says to file its Death Statement within 150 days, select the current form from its downloads page, and follow the mailing directions printed on that form; it also notes an Affidavit of Death may be separately required. The current attached form could not be read in this review environment, so its exact attachments and destination must be confirmed from the live form.
- This material is educational, not legal, tax, insurance, or investment advice. Verify the law, assessor records, title, and professional advice again when an inheritance or sale is actually contemplated.

## Local checks

```sh
python3 scripts/check_site.py
node --check assets/calculator.js
git diff --check
```

The pull-request workflow additionally builds with GitHub's Jekyll Pages action and verifies that the published output contains only the guide and its assets—not the legacy research directories or development files.

---

# Research workspace and analytics dashboard (session `b58dfdcf`)

A separate, independently built analytical dashboard lives under `site/`. It is additive:
it does not replace or modify the guide above.

**Question:** for a potential 2040–2050 trust inheritance of a house in **Cupertino 95014**
(est. $3,100,000, Nov 2026) versus keeping a three-unit property in San Francisco's
**Outer Sunset 94122** (est. $1,800,000; two of three units rented at ~$7,150/month) —
should the beneficiary live in the house, rent it out, or sell it and reinvest?

## Two views, one repository

| | Guide (repository root) | Dashboard (`site/`) |
|---|---|---|
| Built by | sessions `c3099612`, `arena-570be64c`, `arena-2988121a` | session `b58dfdcf` |
| Published at | `https://ginnymcfiner23-ux.github.io/Cupertino2/` | `https://ginnymcfiner23-ux.github.io/Cupertino2/site/` |
| Privacy posture | Publishes **no** ZIP codes, values, rents or bills | Publishes ZIP codes and the requester's own estimates, every one labelled `supplied` or `assumption`; no names, addresses, parcel numbers or identifiers |
| Depth | Rule walkthrough and decision paths; no numeric forecast | Year-by-year projections and a quantified three-way comparison |

Both views omit every personal identifier. `tools/pii_scan.py` fails the build if a name,
street address, phone number, e-mail address, SSN, parcel number or named trust reaches
`site/`.

The two views reach the same bottom line: hold until death for the IRC § 1014 step-up,
then sell and reinvest rather than live in or rent the house, and leave the rental property
alone.

## The recommendation, in one paragraph

**Do not sell the house during life** — a lifetime sale is taxed at a combined **37.1%**
marginal rate on the gain (20% federal + 3.8% NIIT + 13.3% California), whereas property
held until death gets a step-up in basis under IRC § 1014, so an heir who sells promptly at
the date-of-death value owes essentially nothing. **At the transfer, sell and reinvest.**
Selling beats living in the house at every appreciation rate (2.5 / 4.0 / 5.5%) and every
transfer year (2040 / 2045 / 2050) tested, and beats renting it out by a wider margin
still: the break-even portfolio return is under 1% a year, and the house would have to rent
for roughly $40,000 a month to justify keeping it. **Leave the 94122 property exactly as it
is** — its Proposition 13 lock-in is worth tens of thousands of dollars a year and would be
destroyed by a non-qualifying change in ownership.

The finding that drives all of it is on the [Proposition 19](site/prop19.html) page.

## Layout

```
tools/
  model.py        analytical model -> data/model.json
  build_site.py   renders site/ from data/model.json
  pii_scan.py     fails the build if personal information reaches site/
  verify.py       source-link, internal-link, unresolved-value and PII checks
data/
  model.json      all computed output (single source of truth for site/)
  urls.txt        every external URL used, for manual review
research/         working notes
site/             the published dashboard (plain HTML/CSS, no framework)
VERIFICATION.md   what was confirmed, against which source, and what was left blank
COORDINATION.md   parallel-session claim board, task list and flag register
```

## How the numbers were produced

Every figure is either (a) read directly from an official government source, or (b)
explicitly labelled `assumption`, `supplied` or `unverified`. **Nothing was inferred to
fill a gap.** Two deliberate choices:

- **The parcel property tax rate is derived, not published.** California does not publish a
  per-parcel ad valorem rate. The model fits the supplied bill history to
  `tax = rate x (assessment - $7,000 homeowners' exemption) + flat charges`, separating the
  ad valorem component from flat parcel charges that cost the same however low the assessed
  value is. This matters: the naive tax ÷ assessment ratio is 1.335% for the Cupertino
  parcel and 2.135% for the San Francisco parcel, and neither is the tax rate.
- **The comparison is built so unsupplied values cancel out.** Rent for the owner-occupied
  third unit at 94122 was never supplied. Rather than guess it, each option is compared
  against "sell and reinvest", in which that housing benefit is identical and cancels.

## Rebuilding

```sh
python3 tools/model.py        # recompute data/model.json
python3 tools/build_site.py   # regenerate site/
python3 tools/pii_scan.py site/
python3 tools/verify.py       # exits non-zero if any check fails
```

**URL liveness is not checked automatically** — the build environment has no outbound
access to `irs.gov`, `boe.ca.gov` and the rest. `tools/verify.py` writes all 52 URLs to
`data/urls.txt` instead. `VERIFICATION.md` §2 lists the ~30 URLs opened and read during the
build with their confirmed wording; §3 lists the rest for manual review.

## Disclaimer

Not tax, legal, or investment advice. This is a research and modelling workspace. Confirm
every figure against your own documents and a professional adviser before acting on it.
