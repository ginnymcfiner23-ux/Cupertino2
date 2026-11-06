# Property Transition Guide

A privacy-safe, source-cited decision guide for a planned inheritance involving one residence (Home A) and a separate multi-unit rental property (Home B). It compares living in, renting, or selling Home A and reinvesting, while keeping Home B as a separate operating baseline.

## Site

- Public URL: `https://ginnymcfiner23-ux.github.io/Cupertino2/`
- Deployment status: **not yet deployed from this implementation**. The latest Pages API check reported `building` with the legacy source set to `main` at `/`; that status is not a deployment of this guide. The new Actions workflow validates pull requests and, after merge and Pages Actions configuration, deploys only the curated HTML pages and `assets/` directory.
- Start at [`index.html`](index.html)
- The guide is organized into decision comparison, operating costs, taxes, inheritance checklist, 2040–2050 outlook, review flags, and official sources.

## Privacy and evidence standard

- Public pages use **Home A** and **Home B** only. They do not publish names, addresses, ZIP codes, parcel numbers, owner identities, private property values, assessed values, tax bills, rents, utility bills or credits, insurance estimates, or maintenance figures.
- All user-supplied property-specific figures are treated as unverified and intentionally omitted. Unsupported future amounts are left blank rather than inferred.
- Every data row in a table links directly to an official source. The site distinguishes current law and published amounts from future uncertainty; it does not present a 2040–2050 property-value, rent, premium, utility-cost, maintenance-cost, or investment-return forecast.
- The optional scenario worksheet runs in the visitor's browser only. It starts blank, uses no storage or analytics, and sends no input to a server. It is an illustration, not a tax calculator or forecast.
- Local agency links are jurisdiction-specific references, not confirmation of either home's location or of a rule's applicability. Verify location, unit coverage, title, and the rules in effect at the actual transfer date.
- Earlier research files under `docs/`, `data/`, and `pages/` remain in the repository for history and provenance, but they are not inputs to this guide and are excluded from the new Pages artifact. This workflow publishes only the root HTML guide, `.nojekyll`, and `assets/`.
- The current Santa Clara County Assessor guidance says to file its Death Statement within 150 days, select the current form from its downloads page, and follow the mailing directions printed on that form; it also notes an Affidavit of Death may be separately required. The county's current attached form could not be read in this review environment, so its exact attachments and destination are explicitly left for verification from the live form.
- This material is educational, not legal, tax, insurance, or investment advice. Verify the law, assessor records, title, and professional advice again when an inheritance or sale is actually contemplated.

## Local checks

```sh
python3 scripts/check_site.py
node --check assets/calculator.js
git diff --check
```

The GitHub Actions workflow runs the site and JavaScript checks for pull requests and pushes to `main`. For deployment, it stages only the root HTML pages, `.nojekyll`, and `assets/` so development documents, scripts, and repository metadata are not included in the public Pages artifact. The actual PR, merge, Pages configuration, and deployment run will be logged after they are confirmed.
