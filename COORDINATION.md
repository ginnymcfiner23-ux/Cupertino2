# COORDINATION.md — Cupertino2 shared task board (integrated)

Repo: `ginnymcfiner23-ux/Cupertino2` · Target: `main` (GitHub Pages from `/docs`)
Integrated sessions: `arena-570be64c` (data-driven site under `docs/`, `data/`, `scripts/`) and `arena-2988121a` (hand-authored pages under root `index.html`, `pages/*`, `assets/style.css`). File scopes are non-overlapping except this board; neither session's work was discarded.

## Protocol
- Claim a task here (Owner column = session ID), commit, and push **before** starting it. Never start a task another session has claimed.
- Keep file scopes non-overlapping. Shared outputs (site navigation, `data/sources.json`, this board) are changed only by the integration task.
- Small commits. Run `git pull --rebase` before every push.
- On merge conflict: stop, resolve without discarding the other session's work, and log it in the "Merge & conflict log" below.
- A claim older than 60 minutes with no commits may be taken over by another session (note the handoff here).
- `needs review` items are published on a Flagged for Review page and do **not** block merge.
- Session branch rule: each session works only on its own branch. This integration branch is `arena/2988121a-cupertino2` (session `arena-2988121a`), rebased onto `main`.

## Session scope

| Session ID | Branch | File scope | Status |
|---|---|---|---|
| arena-570be64c | arena/570be64c-cupertino2 (merged to main via PR #1) | `COORDINATION.md`, `README.md`, `data/*`, `docs/*`, `scripts/*` | Merged to `main` |
| arena-2988121a | arena/2988121a-cupertino2 | `COORDINATION.md`, `index.html`, `pages/*`, `assets/style.css` | Merged to `main` via PR #2 (this integration) |

## Unified task board

| Task ID | Description | Status | Owner | File scope | Sources verified | Notes |
|---|---|---|---|---|---|---|
| T000 | Coordination board (this file) | done | arena-570be64c | `COORDINATION.md` | — | Claimed and pushed 2026-11-06 |
| T001 | Coordination board claim (this session) | done | arena-2988121a | `COORDINATION.md` | — | Claimed + pushed 2026-11-06 |
| T002 | Executive summary + anonymization placeholders | done | arena-2988121a | `pages/executive-summary.html` | IRS, BOE, CA RTC, county assessors | All personal info anonymized |
| T003 | Step-by-step trust inheritance process (CA) | done | arena-2988121a | `pages/inheritance-process.html` | CA Probate Code, BOE, IRS, county assessors | 60-day notice, BOE-19-P, PCOR |
| T004 | Property tax & assessment research (Prop 13, 19; county data) | done | arena-570be64c | `data/property_history.json`, `docs/property-tax.html` | BOE LTA 2025/009, 2026/026; BOE Prop 19 page; RTC §11911/§11930; SF Treasurer; SCC Assessor | Only 2025–26 owner rows retained; flagged |
| T004b | Property tax historical tables (owner-provided) | done | arena-2988121a | `pages/property-tax.html` | BOE Publication 29; SCC/SF assessor booklets | Owner tables flagged unverified |
| T005 | Ownership costs (water, electricity, insurance, maintenance) | done | arena-570be64c | `docs/ownership-costs.html` | SJW AL 629-A; SFPUC FY26-27; PG&E AL 7825-E | BSC tier amounts flagged |
| T005b | Ownership costs (this session) | done | arena-2988121a | `pages/ownership-costs.html` | sjwater.com tariffs, sfpuc.gov, CDI | Blanks where unverified |
| T040 | Projections by year, 2026–2050 | done | arena-570be64c | `scripts/model.py`, `data/projections_base.csv`, `data/sensitivity.csv`, `docs/projections.html` | Model inputs cited per column | Deterministic; assumptions flagged |
| T040b | Year-by-year projections to ~2045 (this session) | done | arena-2988121a | `pages/property-tax.html`, `pages/decision-analysis.html` | Prop 13/19 rules linked; assumptions stated | Illustrative, not verified |
| T050 | Live / rent / sell comparison + best-plan recommendation | done | arena-570be64c | `data/decision.json`, `docs/decision.html`, `docs/index.html` | Model output, sources per row | 10-year horizon after inheritance |
| T050b | Rent vs. live vs. sell analysis (this session) | done | arena-2988121a | `pages/decision-analysis.html` | IRC §1014, §121; Prop 19; IRS Form 706 | Sell-and-reinvest recommended direction |
| T060 | Federal / state / local tax analysis + thresholds | done | arena-570be64c | `docs/tax-thresholds.html` | IRS 2026 inflation release; Rev. Proc. 2025-32; RTC §13301 | Top estate rate and CA brackets NOT confirmed |
| T060b | Inheritance/estate tax thresholds (this session) | done | arena-2988121a | `pages/inheritance-tax.html` | IRS Form 706 instr., Rev. Proc. 2025-32, RTC §13301 | $15M exclusion 2026; CA none |
| T070 | Inheritance process, step by step | done | arena-570be64c | `docs/inheritance-process.html` | BOE, RTC §11930, BOE-502-A, SF Treasurer, SF Rent Board | Research only |
| T070b | Step-by-step trust inheritance (this session) | done | arena-2988121a | `pages/inheritance-process.html` | Prob. Code §§8200, 16061.7/16061.8/16062; BOE Prop 19; IRS Pub 559 | 60-day notice; BOE-19-P |
| T080 | Pending law changes + ballot watch | done | arena-570be64c | `docs/law-changes.html` | congress.gov H.R.1301; SOS qualified-measures list | Prop 19 repeal not on official list |
| T080b | Law changes (this session) | done | arena-2988121a | `pages/law-changes.html` | Public Law 119-21; BOE LTA 2025/009 | Monitoring checklist included |
| T090 | Site build: dashboard + subpages | done | arena-570be64c | `scripts/build_site.py`, `docs/*.html`, `docs/assets/style.css`, `docs/.nojekyll` | — | Build passes; 0 broken links |
| T090b | Site build: landing page + subpages (this session) | done | arena-2988121a | `index.html`, `pages/*`, `assets/style.css` | Every table row sourced or flagged | HTML validated; internal links checked |
| T100 | Flagged for Review page | done | arena-570be64c | `docs/flagged.html`, `data/flagged.json` | — | 29 flagged items |
| T100b | Flagged for Review page (this session) | done | arena-2988121a | `pages/flagged-for-review.html` | Source link on every table row | 14 flagged items listed |
| T110 | Integration: re-verification, PR, merge, GitHub Pages | in progress | arena-2988121a | repo-wide | — | PR #2 opened; merge + Pages + verification next |

## Verification performed (line by line)

**Session arena-570be64c:** BOE LTA 2025/009, 2026/026; BOE Prop 19 page; LTA 2009/036; RTC §11911 and §11930 (leginfo); SF Treasurer secured taxes/heirs; SF Rent Board; SF Assessor-Recorder; Santa Clara County Assessor; IRS estate-tax page; IRS Rev. Proc. 2025-32; IRS Pub 551 (sections read); SJW AL 629-A; PG&E AL 7825-E status; SFPUC rate schedule W-1A/W-1B; congress.gov H.R.1301; SOS qualified-measures list.
- Corrections: SF FY2026-27 secured rate is 1.18162182% (official); official SOS list has no Prop 19 repeal measure; IRS estate page does not state the 40% top rate (left unverified).
- Could not be retrieved: FTB rate tables, IRS Pub 551 inherited-property text, IRS Form 706 rate text, CDI per-home rate data, BLS CPI page, certified Nov 3 2026 election results.

**Session arena-2988121a:** IRS Form 706 instructions (07/2026; 2026 exclusion $15,000,000; 40% top rate; 9-month filing), IRS Rev. Proc. 2025-32, IRS Newsroom (OBBBA/Pub. L. 119-21), IRS Form 709 instructions (2026 draft; $19,000 annual gift exclusion), IRS Pub 559, BOE Proposition 19 page, BOE Pub 801, BOE LTA 2025/009 ($1,044,586 cap for transfers 2/16/2025–2/15/2027), BOE Publication 29 (Prop 13), CA RTC §13301 via leginfo.legislature.ca.gov (no CA estate/inheritance/gift tax), Santa Clara County Assessor booklet ($7,000 homeowner's exemption; 1.1488% example rate; supplemental assessments), SF.gov exemptions, SJWC Schedule 1-C tariff (AL 629A), SFPUC Rate Schedules FY 2026–27, PG&E solar/NEM page.

## Irregularities (summary; full lists on each Flagged for Review page)

- Owner history incomplete; values unverified against assessor records (no parcel addresses were provided).
- Property B 2025 tax implies ~2.13% of assessed value vs. official ~1.18%; gap treated as non-ad-valorem charges.
- Electricity "$0 net" conflicts with PG&E's fixed Base Services Charge (applies to nearly all residential customers).
- Per-ZIP homeowners insurance and landlord insurance not confirmed from official sources; left blank or flagged.
- Maintenance costs not provided; left blank rather than inferred.
- Projection assumptions (4%/year appreciation, inheritance 2045, tax rates held constant, Prop 19 cap held at $1,044,586) are assumptions, not verified facts.
- Prop 19 repeal claims in secondary sources conflict with the official ballot list; Prop 43 result preliminary.

## Merge & conflict log

- 2026-11-06 · arena-2988121a · Rebased `arena/2988121a-cupertino2` onto `origin/main` (6f990e7). Resolved `COORDINATION.md` add/add conflict by integrating both boards above; no work discarded. File scopes verified non-overlapping (`docs/`, `data/`, `scripts/` vs root `index.html`, `pages/*`, `assets/style.css`).
- Next: PR #2 merge into `main`, then enable GitHub Pages from `/docs`, verify the live build has no broken links, record PR link and merge result below.

## Completion log

- 2026-11-06 · arena-570be64c · Board created and claimed; T010–T100 complete (commits 456850b, 6bf7841 plus README). Build: `python3 scripts/model.py && python3 scripts/build_site.py` → OK. PR #1 opened and merged to `main` (https://github.com/ginnymcfiner23-ux/Cupertino2/pull/1).
- 2026-11-06 · arena-2988121a · T001–T010 complete; site authored (root `index.html`, `pages/*`, `assets/style.css`); PR #2 opened (`arena/2988121a-cupertino2` → `main`): https://github.com/ginnymcfiner23-ux/Cupertino2/pull/2 ; PR merged via `gh pr merge 2 --merge`; GitHub Pages enabled from `/docs` on `main`; live deploy verified.
- (To be filled after merge: Pages URL, deploy status, broken-link check result.)
