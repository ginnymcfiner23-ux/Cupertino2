# Cupertino2

A source-linked, privacy-safe static dashboard for comparing inheritance, property-tax, rental, utility, insurance, and sale decisions involving a Cupertino-area home and an existing San Francisco property.

## Public site

GitHub Pages publishes from the repository root on `main`:

<https://ginnymcfiner23-ux.github.io/Cupertino2/>

The dashboard lives in root-level HTML pages and `assets/site.css`. It has no build-time dependencies, analytics, forms, client-side scripts, or external images.

## Privacy and evidence rules

- Do not publish exact addresses, ZIP/postal codes, parcel identifiers, account numbers, owner/beneficiary names, or private deed references.
- Do not copy property-specific market values, assessed values, rents, tax bills, mortgage details, insurance premiums, utility bills, maintenance estimates, or solar credits into public files.
- Keep unverifiable property inputs blank and label the reason; do not convert a missing value to zero.
- Link factual claims and every factual table row to an official source. Separate current law and published rates from pending bills and future unknowns.
- The 2040–2050 horizon is not projected without defensible, explicit assumptions.

## Local checks

Run from the repository root:

```sh
python3 scripts/check_site.py
```

The dependency-free audit checks root HTML pages, internal file links, official HTTPS hosts, source links on factual table rows, and the absence of forms, scripts, images, and exact five-digit postal codes in public site assets.

The dashboard is static HTML and CSS. To preview locally, you may run a static file server from the repository root; GitHub Pages uses the same root files after merge.

## Scope

The dashboard is general information, not legal, tax, insurance, appraisal, or investment advice. All current rates and laws need to be rechecked at the actual inheritance, billing, occupancy, or sale date. See [Flagged for review](flags.html) for unresolved evidence gaps and [Sources](sources.html) for the official links used.
