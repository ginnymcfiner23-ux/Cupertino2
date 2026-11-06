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
| --- | --- | --- | --- | --- | --- | --- |
| T000 | Coordination board (this file) | done | arena-570be64c | `COORDINATION.md` | — | Claimed and pushed 2026-11-06 (commit 69054a9) |
| T010 | Source register + fact register with status labels | done | arena-570be64c | `data/sources.json`, `data/facts.json` | 29 registered sources (official and flagged secondary) | Every fact row has ≥1 registered source; build fails otherwise |
| T020 | Property tax & assessment (Prop 13 / Prop 19 / SF & SCC) | done | arena-570be64c | `data/property_history.json`, `docs/property-tax.html` | BOE LTA 2009/036, 2025/009, 2026/026; BOE Prop 19 FAQ; SF Treasurer; RTC 11911/11930 | Owner history: only 2025–26 rows retained (see X01) |
| T030 | Ownership costs (water, electricity, insurance, maintenance) | done | arena-570be64c | `docs/ownership-costs.html` | SJW AL 629-A; SFPUC FY26-27 schedule; PG&E AL 7825-E (applicability) | Per-day BSC tier amounts flagged (X11) |
| T040 | Projections by year, 2026–2050 | done | arena-570be64c | `scripts/model.py`, `data/projections_base.csv`, `data/sensitivity.csv`, `docs/projections.html` | model inputs cited per column | Deterministic; assumptions flagged (X23) |
| T050 | Live / rent / sell comparison + best-plan recommendation | done | arena-570be64c | `data/decision.json`, `docs/decision.html`, `docs/index.html` | model output (see sources per row) | 10-year horizon after inheritance |
| T060 | Federal / state / local tax analysis + thresholds | done | arena-570be64c | `docs/tax-thresholds.html` | IRS 2026 inflation release; IRS estate page; Rev. Proc. 2025-32; RTC 11911/11930 | Top estate rate and CA brackets NOT confirmed (X16, X17) |
| T070 | Inheritance process, step by step | done | arena-570be64c | `docs/inheritance-process.html` | BOE, RTC 11930, BOE-502-A, SF Treasurer, SF Rent Board | Research only |
| T080 | Pending law changes + ballot watch | done | arena-570be64c | `docs/law-changes.html` | congress.gov H.R.1301; SOS qualified-measures list; news (Prop 43, unofficial) | Prop 19 repeal not on official list (X07) |
| T090 | Site build (dashboard + subpages) | done | arena-570be64c | `scripts/build_site.py`, `docs/*.html`, `docs/assets/style.css`, `docs/.nojekyll` | — | Build passes; 0 broken links; all external links registered |
| T100 | Flagged for Review page | done | arena-570be64c | `docs/flagged.html`, `data/flagged.json` | — | 29 items, each with source links; non-blocking |
| T110 | Integration: link check, re-verification, PR, merge, GitHub Pages | in progress | arena-570be64c | repo-wide | — | See completion log |

## Verification performed (line by line)

- Official pages fetched and read this session: BOE LTA 2025/009, 2026/026; BOE Prop 19 page (search), LTA 2009/036; RTC §11911 and §11930 (leginfo); SF Treasurer secured taxes, heirs; SF Rent Board; SF Assessor-Recorder; Santa Clara County Assessor; IRS estate-tax page; IRS Rev. Proc. 2025-32; IRS Pub 551 (sections read: basis adjustments; inherited-property text not reached); SJW AL 629-A; PG&E AL 7825-E status; SFPUC rate schedule (W-1A/W-1B); congress.gov H.R.1301; SOS qualified-measures list (via search).
- Corrections made during verification: SF FY2026-27 secured rate is **1.18162182%** (official), not the 1.18268325% figure in secondary sources; the official SOS list does **not** include a Prop 19 repeal measure; the IRS estate page does **not** state the 40% top rate (left unverified).
- Could not be retrieved: FTB rate tables (CA brackets), IRS Pub 551 inherited-property section text, IRS Form 706 rate text, CDI per-home rate data, BLS CPI release page, official certified Nov 3, 2026 results.

## Irregularities (summary; full list on Flagged for Review)

- Owner history incomplete in retained records (only 2025–26 Property A and 2025 Property B rows); values unverified against assessor records.
- Property B 2025 tax implies 2.13% of AV versus official 1.18%; the gap (~$1,089/yr) treated as non-ad-valorem charges.
- Property A electricity "$0 net" conflicts with PG&E's fixed Base Services Charge (applies to almost all residential customers).
- Property A water range implies ~4–9 ccf/month at SJW Schedule 1 rates; meter/provider to confirm.
- Prop 19 repeal claims in secondary sources conflict with the official ballot list.
- Prop 43 result is preliminary (trailing); certification pending.

## Merge & conflict log

- 2026-11-06 · arena-570be64c · `origin/main` was at `840f020` (Initial commit) at PR time; no other session had merged. Other sessions' branches (arena-2190596b, -2988121a, -2e7ee7cd, -4a906cb7, -55de235e, -c3099612, -f23d35a0) exist with overlapping site paths but are unmerged. This session merges its own work only; any later session must rebase onto `main` and log conflicts here.

## Completion log

- 2026-11-06 · arena-570be64c · Board created and claimed (T000–T110). Pushed before content work.
- 2026-11-06 · arena-570be64c · T010–T100 complete on `arena/570be64c-cupertino2` (commits 456850b, 6bf7841, plus README). Build: `python3 scripts/model.py && python3 scripts/build_site.py` → OK.
- 2026-11-06 · arena-570be64c · PR opened: https://github.com/ginnymcfiner23-ux/Cupertino2/pull/1 (`arena/570be64c-cupertino2` → `main`). Merge and Pages steps follow in the next entries.
- 2026-11-06 · arena-570be64c · PR #1 MERGED (merge commit 6f990e7) into `main` with merge (not auto). Post-merge check: `main` contains `docs/` and `scripts/`.
- 2026-11-06 · arena-570be64c · GitHub Pages: repo-level Pages settings already existed with source `main` `/` (legacy). The integration token received HTTP 403 when attempting to change the source to `/docs`, so Pages cannot be pointed at `/docs` from this session. Workaround in PR #2: root `index.html` redirects to `docs/index.html`, so the live site is served from the repo root. Site URL: https://ginnymcfiner23-ux.github.io/Cupertino2/ (root redirect) and `/docs/index.html`. Owner action (optional): set Pages source to `main` `/docs` in repo settings.
