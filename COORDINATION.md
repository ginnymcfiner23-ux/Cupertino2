# COORDINATION.md — shared task board

Repo: `ginnymcfiner23-ux/Cupertino2` · Target: `main` (GitHub Pages from `/docs`)

## Protocol

- Claim a task here (Owner column = session ID), commit, and push **before** starting it. Never start a task another session has claimed.
- Keep file scopes non-overlapping. Shared outputs (site navigation, `data/sources.json`) are changed only by the integration task.
- Small commits. Run `git pull --rebase` before every push.
- On merge conflict: stop, resolve without discarding the other session's work, and log it in the "Merge & conflict log" below.
- `needs review` items are published on the Flagged for Review page and do **not** block merge.
- Session branch rule: Arena pins each session to its own branch. This session works only on `arena/570be64c-cupertino2` (session ID `arena-570be64c`). The requested `session-<id>/<task>` naming cannot be used.
- **Privacy:** no names, street addresses, parcel numbers, account numbers, phone numbers, or emails appear anywhere in the repo or site. ZIP codes are withheld; properties are labeled by city only (Property A = Cupertino, Property B = San Francisco). Personal details discovered during research stay internal.

## Sessions observed on origin (for awareness; not merged to main at time of claim)

| Session ID | Branch | Notes |
|---|---|---|
| arena-2190596b | arena/2190596b-cupertino2 | Overlapping scope (docs/, data/, COORDINATION.md) |
| arena-2988121a | arena/2988121a-cupertino2 | Overlapping scope (pages/*, COORDINATION.md) |
| arena-2e7ee7cd | arena/2e7ee7cd-cupertino2 | Overlapping scope (docs/**, research/*) |
| arena-4a906cb7 | arena/4a906cb7-cupertino2 | Overlapping scope |
| arena-55de235e | arena/55de235e-cupertino2 | Overlapping scope (docs/, site/) |
| arena-c3099612 | arena/c3099612-cupertino2 | Overlapping scope |
| arena-f23d35a0 | arena/f23d35a0-cupertino2 | Not inspected |

Because several sessions claim the same site paths, whichever integration lands on `main` first defines the site. Any later session must rebase onto it and log conflicts below rather than overwrite it.

## Task board

| Task ID | Description | Status | Owner | File scope | Sources verified | Notes |
|---|---|---|---|---|---|---|
| T000 | Coordination board (this file) | done | arena-570be64c | `COORDINATION.md` | — | Claimed and pushed 2026-11-06 |
| T010 | Source register + line-by-line verification log | in progress | arena-570be64c | `data/sources.json`, `data/facts.json` | official only | |
| T020 | Property tax & assessment (Prop 13 / Prop 19 / SF & SCC rates) | in progress | arena-570be64c | `data/property_history.json`, `docs/property-tax.html` | BOE, SF Treasurer, SCC & SF assessors | user-provided history flagged |
| T030 | Ownership costs (water, electricity, insurance, maintenance) | in progress | arena-570be64c | `data/costs.json`, `docs/costs.html` | SJW AL 629-A, SFPUC schedule, PG&E BSC, CDI | |
| T040 | Projections by year (2026–2050) | in progress | arena-570be64c | `scripts/model.py`, `data/projections*.csv`, `docs/projections.html` | assumptions labeled | deterministic script |
| T050 | Live / rent / sell comparison + recommendation | in progress | arena-570be64c | `data/decision.json`, `docs/decision.html` | model output | |
| T060 | Federal / state / local tax + thresholds | in progress | arena-570be64c | `docs/tax.html` | IRS, leginfo, BOE | |
| T070 | Inheritance process (step-by-step) | in progress | arena-570be64c | `docs/inheritance-process.html` | BOE, SF Treasurer, leginfo, IRS | |
| T080 | Pending law changes + ballot watch | in progress | arena-570be64c | `docs/law-changes.html` | congress.gov, SOS, leginfo | |
| T090 | Site build (landing, subpages, dashboard) | in progress | arena-570be64c | `scripts/build_site.py`, `docs/*.html`, `docs/assets/*` | — | generated from data |
| T100 | Flagged for Review page | in progress | arena-570be64c | `docs/flagged.html` | — | non-blocking |
| T110 | Integration: link check, re-verification, PR, merge, Pages | unclaimed | arena-570be64c | repo-wide | — | runs last |

## Merge & conflict log

_(entries added as they occur)_

## Completion log

- 2026-11-06 · arena-570be64c · Board created and claimed (T000–T110). Pushed before content work.
