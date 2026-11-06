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
