# Cupertino2 — Property Plan / Fieldnotes

A static, source-backed California property-succession and operating-cost research workspace.

**Live site:** [ginnymcfiner23-ux.github.io/Cupertino2](https://ginnymcfiner23-ux.github.io/Cupertino2/)
**Research checked:** 6 November 2026. Election results and local tariffs are dated snapshots; refresh official sources before relying on them.

## Pages

- [`index.html`](index.html) — current-law dashboard, dated public-rate snapshot, privacy notes, and blank-by-default scenario calculators.
- [`review.html`](review.html) — detailed legal/current-law review, local-cost references, enacted-versus-proposed bill tracker, unresolved fact checks, election snapshot, and linked source register.
- [`RESEARCH.md`](RESEARCH.md) — research log, source conclusions, calculation assumptions, verification limits, and open property-specific items.

## Privacy and calculator behavior

Calculations run in the browser only. Calculator inputs begin blank; the site does not send or save them, and there is no backend/API endpoint, analytics, cookie, or third-party script. Its Content Security Policy sets `connect-src 'none'` and blocks form submissions. Refreshing, clearing, or leaving the page clears transient values.

No private property values, tax histories, rents, bills, ZIP codes, service addresses, parcel identifiers, or identifying family details are published or prefilled. Published rates are not property-specific bills, and the calculations are not legal or tax eligibility determinations.

## Hosting and local review

GitHub Pages is configured to publish the `main` branch repository root. To inspect locally, run a static server from this folder, for example:

```sh
python3 -m http.server 8000 --bind 0.0.0.0
```

Then open `http://localhost:8000/`. The project has no package dependencies or build step. `.nojekyll` keeps Pages publication a plain static-site deploy.

This educational research is not legal, tax, accounting, appraisal, insurance, or investment advice. Check live official sources and obtain qualified, property-specific review before acting.
