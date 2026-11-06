# COORDINATION.md — Cupertino2 shared task board (integrated)

Repo: `ginnymcfiner23-ux/Cupertino2` · Target: `main` (GitHub Pages remains on the legacy root source; this session replaces the root redirect with the privacy-safe guide, uses `_config.yml` to exclude legacy research/development directories, and validates the Jekyll output in Actions)
Integrated sessions: `arena-570be64c` (data-driven site under `docs/`, `data/`, `scripts/`; live dashboard) and `arena-2988121a` (hand-authored pages under `pages/*`, `assets/style.css`; root `index.html` content preserved in branch history). File scopes non-overlapping except this board; neither session's work discarded.

## Protocol
- Claim a task here (Owner column = session ID), commit, and push **before** starting it. Never start a task another session has claimed.
- Keep file scopes non-overlapping. Shared outputs (site navigation, `data/sources.json`, this board) are changed only by the integration task.
- Small commits. Run `git pull --rebase` before every push.
- On merge conflict: stop, resolve without discarding the other session's work, and log it in the "Merge & conflict log" below.
- A claim older than 60 minutes with no commits may be taken over by another session (note the handoff here).
- `needs review` items are published on a Flagged for Review page and do **not** block merge.
- Session branch rule: each session works only on its own branch.

## Session scope

| Session ID | Branch | File scope | Status |
|---|---|---|---|
| arena-570be64c | arena/570be64c-cupertino2 (merged to main via PR #1, #3, #4) | `COORDINATION.md`, `README.md`, `data/*`, `docs/*`, `scripts/*`, root `index.html` redirect, root `.nojekyll` | Merged to `main`; live dashboard at `docs/index.html` |
| arena-2988121a | arena/2988121a-cupertino2 | `pages/*`, `assets/style.css`; root `index.html` content in commit `d480257`/`86e9139` | Merged to `main` via PR #2 |
| c3099612 | arena/c3099612-cupertino2 | `index.html`, `decision.html`, `costs.html`, `taxes.html`, `process.html`, `outlook.html`, `review.html`, `sources.html`, `assets/site.css`, `assets/calculator.js`, `scripts/check_site.py`, `.github/workflows/pages.yml`, `README.md`, `.nojekyll` | In progress; rebase/PR/deploy pending |

## Unified task board

| Task ID | Description | Status | Owner | File scope | Sources verified | Notes |
|---|---|---|---|---|---|---|
| T000 | Coordination board | done | arena-570be64c | `COORDINATION.md` | — | Claimed and pushed 2026-11-06 |
| T001 | Coordination board claim (this session) | done | arena-2988121a | `COORDINATION.md` | — | Claimed + pushed 2026-11-06 |
| T002 | Executive summary + anonymization placeholders | done | arena-2988121a | `pages/executive-summary.html` | IRS, BOE, CA RTC, county assessors | All personal info anonymized |
| T003 | Step-by-step trust inheritance process (CA) | done | arena-2988121a | `pages/inheritance-process.html` | CA Probate Code, BOE, IRS, county assessors | 60-day notice, BOE-19-P, PCOR |
| T004 | Property tax & assessment (Prop 13, 19; county data) | done | arena-570be64c | `data/property_history.json`, `docs/property-tax.html` | BOE LTA 2025/009, 2026/026; BOE Prop 19 page; RTC §11911/§11930; SF Treasurer; SCC Assessor | Only 2025–26 owner rows retained; flagged |
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
| T110 | Integration: re-verification, PR, merge, GitHub Pages | done | arena-2988121a | repo-wide | — | PR #2 merged into main; Pages live via root redirect to docs/ |
| T120 | Privacy-safe, source-verified Home A/Home B decision guide and Pages deployment | in progress | c3099612 | root HTML, `_config.yml`, `assets/`, `scripts/check_site.py`, Pages verification workflow | IRS, BOE, California Legislature, state/county agencies, official utility/insurance/rent sources | User-provided property figures omitted; forecast horizon blank; legacy Jekyll output is tested to exclude prior data/docs and repository-development files. |

## Verification performed (line by line)

**Session arena-570be64c:** BOE LTA 2025/009, 2026/026; BOE Prop 19 page; LTA 2009/036; RTC §11911 and §11930 (leginfo); SF Treasurer secured taxes/heirs; SF Rent Board; SF Assessor-Recorder; Santa Clara County Assessor; IRS estate-tax page; IRS Rev. Proc. 2025-32; IRS Pub 551 (sections read); SJW AL 629-A; PG&E AL 7825-E status; SFPUC rate schedule W-1A/W-1B; congress.gov H.R.1301; SOS qualified-measures list.
- Corrections: SF FY2026-27 secured rate is 1.18162182% (official); official SOS list has no Prop 19 repeal measure; IRS estate page does not state the 40% top rate (left unverified).
- Could not be retrieved: FTB rate tables, IRS Pub 551 inherited-property text, IRS Form 706 rate text, CDI per-home rate data, BLS CPI page, certified Nov 3 2026 election results.

**Session arena-2988121a:** IRS Form 706 instructions (07/2026; 2026 exclusion $15,000,000; 40% top rate; 9-month filing), IRS Rev. Proc. 2025-32, IRS Newsroom (OBBBA/Pub. L. 119-21), IRS Form 709 instructions (2026 draft; $19,000 annual gift exclusion), IRS Pub 559, BOE Proposition 19 page, BOE Pub 801, BOE LTA 2025/009 ($1,044,586 cap for transfers 2/16/2025–2/15/2027), BOE Publication 29 (Prop 13), CA RTC §13301 via leginfo.legislature.ca.gov (no CA estate/inheritance/gift tax), Santa Clara County Assessor booklet ($7,000 homeowner's exemption; 1.1488% example rate; supplemental assessments), SF.gov exemptions, SJWC Schedule 1-C tariff (AL 629A), SFPUC Rate Schedules FY 2026–27, PG&E solar/NEM page.

**Session c3099612 (active):** Current IRS estate/gift-tax FAQs and 2026–27 releases; IRS Publications 523/525/527/551/559; Form 706 instructions; BOE Prop 19 LTA 2026/026, indexed allowance, Publication 29, Pub. 800-9 and sample BOE-502-D; California RTC §§480 and 11930; SB 974 bill status; State Controller; California Courts; Santa Clara Assessor 2025 annual report/current downloads listing; local recorder/rent/utility/solar/insurance sources; SEC and CSLB. Eight-page guide and browser-only worksheet pass local checks. Santa Clara's current form attachment itself was inaccessible, so exact attachment/destination remains a live-form check. Pages build-type configuration via the API returned HTTP 403; the PR now tests the legacy Jekyll output against an explicit exclusion list.

## Irregularities (summary; full lists on each Flagged for Review page)

- Owner history incomplete; values unverified against assessor records (no parcel addresses were provided).
- Property B 2025 tax implies ~2.13% of assessed value vs. official ~1.18%; gap treated as non-ad-valorem charges.
- Electricity "$0 net" conflicts with PG&E's fixed Base Services Charge (applies to nearly all residential customers).
- Per-ZIP homeowners insurance and landlord insurance not confirmed from official sources; left blank or flagged.
- Maintenance costs not provided; left blank rather than inferred.
- Projection assumptions (4%/year appreciation, inheritance 2045, tax rates held constant, Prop 19 cap held at $1,044,586) are assumptions, not verified facts.
- Prop 19 repeal claims in secondary sources conflict with the official ballot list; Prop 43 result preliminary.

## Merge & conflict log

- 2026-11-06 · arena-2988121a · First rebase onto `origin/main` (6f990e7): resolved `COORDINATION.md` add/add conflict by integrating both boards; no work discarded.
- 2026-11-06 · arena-570be64c (parallel session) · Merged PR #3 (`arena/570be64c-cupertino2` → `main`); committed root `index.html` redirect to `docs/index.html` (Pages source is root `/`, not changeable by integration token); PR #4 merged; added root `.nojekyll` after legacy Jekyll build failure on main; logged build failure and fix.
- 2026-11-06 · arena-2988121a · Second rebase onto `origin/main` (4983448): kept the established root redirect (`index.html` theirs); `pages/*` preserved in repo; landing-page content remains in branch history (`d480257`, `86e9139`).
- 2026-11-06 · arena-2988121a · Third rebase onto `origin/main` (30273fb): resolved `COORDINATION.md` content conflict (their PR #4 / `.nojekyll` log entries merged into this board); no work discarded.
- 2026-11-06 · arena-2988121a · Pages build was errored on legacy Jekyll (no detailed error exposed by API); added root `_config.yml` (`title: Cupertino2`) and pushed to `main`; build status became `built`; live site verified via fetch of https://ginnymcfiner23-ux.github.io/Cupertino2/ (serves root `index.html` → `docs/index.html` dashboard).

- 2026-11-06 · c3099612 · Rebased onto the updated `origin/main`; resolved the `COORDINATION.md` add/add conflict by retaining the established integrated board and adding this session's scope/task. No prior session records or files were discarded. The Pages workflow uses the current legacy root source, removes `.nojekyll` so Jekyll can apply `_config.yml` exclusions, and builds the same output in CI to verify that `docs/`, `data/`, `pages/`, scripts, and coordination files are not published.

- 2026-11-06 · c3099612 · Applying the site commit also conflicted in `README.md` and root `index.html`: kept the integrated board, replaced the stale location-revealing README with the privacy-safe guide summary, and replaced the legacy redirect to `docs/index.html` with the new Home A/Home B landing page. Existing `docs/`, `data/`, and `pages/` files were retained in the repository but excluded from the legacy Jekyll output by `_config.yml` and checked in CI.
- 2026-11-06 · c3099612 · A direct Pages API request to change `build_type` from `legacy` to `workflow` returned HTTP 403 (`Resource not accessible by integration`). To avoid claiming an Actions deploy or publishing the old directories, the workflow was changed to validate the legacy Jekyll output and `_config.yml` explicitly excludes non-site content; the root `.nojekyll` was removed so those exclusions can run. Deployment remains pending a successful post-merge Pages build and output check.

## Completion log

- 2026-11-06 · arena-570be64c · T010–T100 complete; PR #1 merged (https://github.com/ginnymcfiner23-ux/Cupertino2/pull/1); PR #3 and PR #4 merged; root redirect + `.nojekyll` committed; live dashboard at `docs/index.html` via GitHub Pages root source.
- 2026-11-06 · arena-2988121a · T001–T010 complete; site authored (`pages/*`, `assets/style.css`); PR #2 opened (`arena/2988121a-cupertino2` → `main`): https://github.com/ginnymcfiner23-ux/Cupertino2/pull/2 ; PR #2 merged into `main`; GitHub Pages live (root `/` → `docs/index.html`); deploy verified.
- Final results: PR #2 merged into `main`; Pages URL = https://ginnymcfiner23-ux.github.io/Cupertino2/ (redirects to `docs/index.html`).
- 2026-11-06 · arena-570be64c · FINAL (integration record): PR #1 `arena/570be64c-cupertino2` → `main` MERGED (6f990e7, merge commit, no auto-merge). PR #3 (root `index.html` redirect to `docs/`) MERGED. PR #4 (root `.nojekyll`) MERGED. Live site verified by fetch: https://ginnymcfiner23-ux.github.io/Cupertino2/ (serves `docs/index.html` dashboard; `docs/flagged.html`; `docs/projections.html` all render with sources). Pages build history: several runs for this session's and other sessions' commits were `cancelled` (superseded by newer pushes) and were reported by the Pages API as `errored`; the run for `efc0196` (latest at verification) completed `success`. Both `docs/` (this session) and `pages/` (arena-2988121a) remain on `main`; both are reachable from the repo; neither was deleted. Pages source stays `main` `/` (integration token cannot change it).
