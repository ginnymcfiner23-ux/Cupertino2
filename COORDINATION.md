# Coordination board

## Task board

| Task | Status | Owner | File scope |
|---|---|---|---|
| Privacy-safe research, source verification, site implementation, and final integration | implementation and local smoke checks complete; awaiting PR, merge, and Pages confirmation | Arena session on `arena/4a906cb7-cupertino2` | `COORDINATION.md`, `README.md`, `index.html`, `review.html`, `styles.css`, `app.js`, `RESEARCH.md`, `.nojekyll` |

## Coordination notes

- No other claims or concurrent worktrees were visible when this task was claimed.
- All work remains on the Arena-assigned branch `arena/4a906cb7-cupertino2`.
- Privacy constraint: do not publish property-specific financial inputs or identifying details. Public-facing content uses generic labels and public-law research only.
- Calculator fields are blank by default and are not written to storage or transmitted. Static CSP includes `connect-src 'none'`.

## Research and verification

- Reviewed the BOE’s 2026/026 Prop 19 multi-unit guidance, current value-cap window, federal and California tax references, trust administration, SF local rates/rent limits, Cupertino/South Bay/SF water schedules, CDI insurance profile caveats, legislation status, and timestamped preliminary SF election results.
- Current external references and unresolved property-specific fact checks are documented in `RESEARCH.md` and linked in `review.html`.
- Local static serving returned HTTP 200 for the dashboard, review, CSS, script, research log, and `.nojekyll`; local anchors/IDs and blank calculator inputs were checked; `node --check app.js` and Node-based calculator smoke tests passed. PR, merge, and Pages confirmation remain.
