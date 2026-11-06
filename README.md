# Cupertino2

A source-linked, privacy-safe static dashboard for inheritance, property-tax, rental, utility, insurance, and sale decisions involving a California home and an existing San Francisco property.

## Public site

GitHub Pages publishes from the repository root on `main`:

<https://ginnymcfiner23-ux.github.io/Cupertino2/>

The active dashboard is built from root-level HTML pages and `assets/site.css`. Earlier URLs under `docs/` and `pages/` are compatibility redirects to the current pages. The site has no build-time dependencies, analytics, forms, client-side scripts, or external images.

## Privacy and evidence rules

- Do not publish exact addresses, ZIP/postal codes, parcel identifiers, account numbers, owner/beneficiary names, or deed references.
- Do not copy property-specific market values, assessed values, rents, tax bills, mortgage details, insurance premiums, utility bills, maintenance estimates, or solar credits into public files.
- Keep unverifiable property inputs blank and label the reason; do not convert a missing value to zero.
- Link factual claims and every factual table row to an official source. Separate current law and published rates from pending bills and future unknowns.
- The 2040–2050 horizon is not projected without defensible, explicit assumptions.
- Public data files contain source metadata and blank placeholders only. The former property-specific projection generator is disabled.

## Local checks

Run from the repository root:

```sh
python3 scripts/check_site.py
```

The dependency-free audit checks active and legacy HTML pages, internal file and anchor links, official HTTPS hosts, source links on factual table rows, and the absence of forms, scripts, external images, and exact five-digit postal codes in public text and data files.

There is no separate compilation step: GitHub Pages serves the static HTML and CSS after the change is merged.

## Scope

The dashboard is general information, not legal, tax, insurance, appraisal, or investment advice. All current rates and laws need to be rechecked at the actual inheritance, billing, occupancy, or sale date. See [Flagged for review](flags.html) for unresolved evidence gaps and [Sources](sources.html) for the official links used.
