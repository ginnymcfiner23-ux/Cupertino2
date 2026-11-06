# COORDINATION.md — Cupertino2 shared task board (integrated)

Repo: `ginnymcfiner23-ux/Cupertino2` · Target: `main` (GitHub Pages remains on the legacy root source; this session replaces the root redirect with the privacy-safe guide, uses `_config.yml` to exclude legacy research/development directories, and validates the Jekyll output in Actions)
Integrated sessions: `arena-570be64c` (data-driven site under `docs/`, `data/`, `scripts/`; live dashboard) and `arena-2988121a` (hand-authored pages under `pages/*`, `assets/style.css`; root `index.html` content preserved in branch history). Third session `arena-55de235e` joined as **re-verification & Pages-recovery integration session** (2026-11-06): its initial standalone claim board was folded into this unified board on first rebase (conflict logged below); no prior work discarded. File scopes non-overlapping except this board.

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
| arena-55de235e | arena/55de235e-cupertino2 | `COORDINATION.md` (integration), Pages deploy recovery, gap-fill additions to `data/*`, `scripts/build_site.py`, regenerated `docs/*` | Re-verification complete; merging via PR (see Completion log) |
| c3099612 | arena/c3099612-cupertino2 | `index.html`, `decision.html`, `costs.html`, `taxes.html`, `process.html`, `outlook.html`, `review.html`, `sources.html`, `assets/site.css`, `assets/calculator.js`, `scripts/check_site.py`, `.github/workflows/pages.yml`, `README.md`, `.nojekyll` | Merged to `main` via PR #7; live guide at the repository root |
| b58dfdcf | arena/b58dfdcf-cupertino2 | `site/**`, `tools/model.py`, `tools/build_site.py`, `tools/pii_scan.py`, `tools/verify.py`, `data/model.json`, `data/urls.txt`, `data/projections_*.csv`, `research/**`, `VERIFICATION.md`, `.github/workflows/site-build.yml`, `_config.yml` (exclude lines only), `README.md` (appended section) | Merged to `main` via PR #9; dashboard published under `site/` |

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
| T200 | Independent line-by-line re-verification of merged site against official sources | done | arena-55de235e | `docs/*`, `data/*` | see Verification log below | Completed 2026-11-06: tax/property/costs/process/law/flagged pages audited; 5 unconfirmable rows upgraded to verified with official sources; gaps and stale copy fixed |
| T201 | GitHub Pages deploy recovery: all 4 builds since site landed are `errored` (“Page build failed”); diagnose and fix until build `built` | done | arena-55de235e | build-affecting files (root, `docs/*`, `.nojekyll`, `_config.yml`) | GitHub Pages API | Diagnosed: build failed on legacy Jekyll until root `_config.yml` was added (`dfb4f05` → `built`); `efc0196` then failed transiently (`duration:0`, no content cause) and `ba5ae37` built — failures are intermittent; policy: after every merge to main, poll builds/latest and re-trigger (empty push) until `built`. Site live and reachable (fetched full content) |
| T202 | Gap-fill: sources retrieved this session that earlier sessions could not (CDI insurance, BLS CPI, FTB CA estate pick-up tax, estate rate, SCC rate book, CA bills, macro benchmarks, trust notices) | done | arena-55de235e | `data/sources.json` (+15), `data/facts.json`, `data/flagged.json`, `data/property_history.json`, `scripts/build_site.py`, regenerated `docs/*` | see Verification log | Completed 2026-11-06; build validator passes (all rows sourced, links registered, https-only) |
| T203 | Final PR → merge → confirm Pages build `built` + site reachable | in progress | arena-55de235e | repo-wide | GitHub Pages API | PR #12 opened from `arena/55de235e-cupertino2`; merge result to be recorded in Completion log |
| T120 | Privacy-safe, source-verified Home A/Home B decision guide and Pages deployment | done | c3099612 | root HTML, `_config.yml`, `assets/`, `scripts/check_site.py`, Pages verification workflow | IRS, BOE, California Legislature, state/county agencies, official utility/insurance/rent sources | User-provided property figures omitted; forecast horizon blank; legacy Jekyll output is tested to exclude prior data/docs and repository-development files. |

## Verification performed (line by line)

**Session arena-570be64c:** BOE LTA 2025/009, 2026/026; BOE Prop 19 page; LTA 2009/036; RTC §11911 and §11930 (leginfo); SF Treasurer secured taxes/heirs; SF Rent Board; SF Assessor-Recorder; Santa Clara County Assessor; IRS estate-tax page; IRS Rev. Proc. 2025-32; IRS Pub 551 (sections read); SJW AL 629-A; PG&E AL 7825-E status; SFPUC rate schedule W-1A/W-1B; congress.gov H.R.1301; SOS qualified-measures list.
- Corrections: SF FY2026-27 secured rate is 1.18162182% (official); official SOS list has no Prop 19 repeal measure; IRS estate page does not state the 40% top rate (left unverified).
- Could not be retrieved: FTB rate tables, IRS Pub 551 inherited-property text, IRS Form 706 rate text, CDI per-home rate data, BLS CPI page, certified Nov 3 2026 election results.

**Session arena-2988121a:** IRS Form 706 instructions (07/2026; 2026 exclusion $15,000,000; 40% top rate; 9-month filing), IRS Rev. Proc. 2025-32, IRS Newsroom (OBBBA/Pub. L. 119-21), IRS Form 709 instructions (2026 draft; $19,000 annual gift exclusion), IRS Pub 559, BOE Proposition 19 page, BOE Pub 801, BOE LTA 2025/009 ($1,044,586 cap for transfers 2/16/2025–2/15/2027), BOE Publication 29 (Prop 13), CA RTC §13301 via leginfo.legislature.ca.gov (no CA estate/inheritance/gift tax), Santa Clara County Assessor booklet ($7,000 homeowner's exemption; 1.1488% example rate; supplemental assessments), SF.gov exemptions, SJWC Schedule 1-C tariff (AL 629A), SFPUC Rate Schedules FY 2026–27, PG&E solar/NEM page.

**Session c3099612 (active):** Current IRS estate/gift-tax FAQs and 2026–27 releases; IRS Publications 523/525/527/551/559; Form 706 instructions; BOE Prop 19 LTA 2026/026, indexed allowance, Publication 29, Pub. 800-9 and sample BOE-502-D; California RTC §§480 and 11930; SB 974 bill status; State Controller; California Courts; Santa Clara Assessor 2025 annual report/current downloads listing; local recorder/rent/utility/solar/insurance sources; SEC and CSLB. Eight-page guide and browser-only worksheet pass local checks. Santa Clara's current form attachment itself was inaccessible, so exact attachment/destination remains a live-form check. Pages build-type configuration via the API returned HTTP 403; the PR now tests the legacy Jekyll output against an explicit exclusion list.

**Session arena-55de235e (re-verification, 2026-11-06):** IRS Estate tax page (2026 filing threshold $15,000,000 table); IRS IR-2025-103 (2026 basic exclusion $15M, annual gift exclusion $19,000); IRS “What’s new — Estate and gift tax” (P.L. 119-21 §70106 → $15M, 2026); congress.gov CRS R48183 (40% rate; H.R.1301 repeal bill, 119th); BOE Prop 13 (Pub 29, Pub 800-10, LTA 25-023); BOE Prop 19 page + BOE news release 25-02 ($1,044,586 cap for 2/16/2025–2/15/2027) + BOE Prop 19 fact sheet Pub 801 (filing checklist: BOE-19-P ≤3 yrs; homeowners’ exemption ≤1 yr); FTB SB 378 analysis (CA estate “pick-up” tax = $0 since federal credit repeal); leginfo AB 1482 (statewide rent cap 5%+CPI/10% max, sunsets 1/1/2030); leginfo SB 284 status (Prop 19 family-home expansion, active/held in Assembly committee 7/14/25); Santa Clara County FY2025-26 Tax Rate Book (1% + voter debt by TRA; example TRA totals 1.12580–1.24090); Santa Clara courts trust-administration page (assessor notice ≤150 days; 60-day beneficiary notice); sccgov.org Programs to Assist Taxpayers ($7,000 homeowner’s exemption, Jan 1 occupancy); SCC Assessor parent-child page (asr.santaclaracounty.gov / sccassessor.org Prop 19 qualification rules); SF Treasurer secured taxes (FY2026-27 rate **1.18162182%**, FY2025-26 1.18268325%); SFPUC FY2026-27 water/sewer rate schedule (W-1A/W-1B/W-1A service + volumetric, Schedule A sewer $6.62 + $20.74/DU, flow factor 95% multi-family); City of Cupertino utilities page (CalWater / San Jose Water / SVCE or PG&E by area); CPUC NEM resources (20-yr NEM guarantee; net surplus compensation ≈2–3¢/kWh); California DOI Residential Property Insurance Report (Part I XLSX: 2008–2023 avg written premiums incl. Homeowners Multi-Peril $1,176; Part II SB 824 workbook: 2023 earned premium $14.22B / 12.58M policy-years = **$1,130 avg**, avg Coverage A $324,973); BLS CPI news release Sep 2026 (CPI-U +3.7% 12-mo, core +2.6%, electricity +4.4%); FHFA HPI 2026Q2 (CA 1-yr −0.20%, 5-yr +17.31%, since 1991Q1 +317.15% → ≈4.1%/yr CAGR computed); FRED SP500 (2016-11-07 2,131.52 → 2026-11-04 7,688.62 → 10-yr CAGR ≈13.7% computed); FRED GS10 (2026-10-01 5.13%); CA SOS qualified measures Nov 3 2026 (no Prop 13/estate-tax measure; Prop 40 one-time 5% tax on >$1B explicitly excludes real property; Prop 43 local-tax limitation — outcomes not yet certified).
- GitHub Pages API: builds for 6f990e7, 4983448, 30273fb, acc1da6 all `errored` → “Page build failed” (only pre-site build 840f020 `built`). Contradicts prior “deploy verified” note → T201 opened.
- T200 audit results (2026-11-06): every table row on `docs/tax-thresholds.html` re-checked against official sources; five rows upgraded from “Not confirmed/secondary” to verified with newly retrieved official sources — top estate rate **40%** (FTB SB 378 analysis: “The highest estate and gift tax rate is 40 percent”; CRS R48183: “The estate tax rate on the taxable portion of the estate, if any, is 40%”), NIIT **3.8%** with thresholds $200k/$250k/$125k (IRS NIIT Q&A, incl. rental income and second-home gains), U.S. CPI **+3.7%** Sep 2026 (BLS release USDL-26-1574), CA 2026 brackets **1%–12.3%** (FTB 2026 Tax Rate Schedules), California estate/inheritance tax **none — pick-up tax $0** (FTB: “the state’s pick-up tax is zero”).
- T202 additions: 15 new registered sources (CRS R48183, IRS NIIT Q&A, FTB SB 378 analysis, FTB 2026 rate schedules, CDI Residential Property Insurance Report + SB 824 workbook, SCC FY2025-26 Tax Rate Book, leginfo AB 1482 & SB 284, congress.gov S.587, FHFA HPI 2026Q2, FRED SP500 & GS10, CPUC Solar Consumer Protection Guide, Santa Clara Superior Court Probate/Trusts). New fact rows: estate-tax coverage (≈0.07% of decedents), couple’s $30M combined exclusion with portability, AB 1482 statewide rent cap (5%+CPI ≤10%, sunset 1/1/2030), SB 284 status (held in Assembly committee 7/14/2025), S.587 status (introduced only), Santa Clara County rate structure (1% + voter debt; TRA examples 1.12580%–1.24090%).
- Owner history restored in full (flag X01): Property A 2014–2026 and Property B 2016–2025 — all 46 value rows exactly as supplied, with owner-reported YoY % in a new Notes column, per-year computed implied tax÷AV ratios (A 1.32%–1.41%, B 1.73%–2.13%), and the 2017–18 / 2019–20 repeated-tax irregularities called out. Nothing inferred; 2026 Property A tax left blank.
- Other page upgrades: ownership costs now show CDI statewide insurance benchmarks ($1,176 / $1,130 / $324,973) and the CPUC NEM 20-year / 2–3¢ per kWh export-credit context; projections page gains an “Official reference benchmarks” table (FHFA CA HPI −0.20% y/y, +17.31% 5-yr; S&P 500 ≈13.7%/yr over 10 years computed from FRED; GS10 5.13%; BLS CPI 3.7%); inheritance-process adds the 60-day beneficiary notice (Prob. Code §16061.7), 150-day Assessor notice (R&TC §480(b)), 9-month estate-tax due date, inventory/valuation and trust EIN steps (Santa Clara Superior Court). Flags X16–X20 marked Resolved (audit trail kept); X01/X04/X06/X11/X14 updated. `python3 scripts/build_site.py` → Build OK (validator: every row sourced, all external links registered, https-only, no broken internal links).

## Irregularities (summary; full lists on each Flagged for Review page)

- Owner history incomplete; values unverified against assessor records (no parcel addresses were provided).
- Property B 2025 tax implies ~2.13% of assessed value vs. official ~1.18%; gap treated as non-ad-valorem charges.
- Electricity "$0 net" conflicts with PG&E's fixed Base Services Charge (applies to nearly all residential customers).
- Per-ZIP homeowners insurance and landlord insurance not confirmed from official sources; left blank or flagged.
- Maintenance costs not provided; left blank rather than inferred.
- Projection assumptions (4%/year appreciation, inheritance 2045, tax rates held constant, Prop 19 cap held at $1,044,586) are assumptions, not verified facts.
- Prop 19 repeal claims in secondary sources conflict with the official ballot list; Prop 43 result preliminary.

### Session b58dfdcf flag register (FLAG-01 … FLAG-16, each with a source link)

| ID | Severity | Issue | Source |
|---|---|---|---|
| FLAG-01 | high | 2026 property tax blank for the 95014 parcel | SCC Assessor |
| FLAG-02 | medium | 94122 has no 2026 row; 2021 shows -5.9% while assessment rose 1%; 2018 shows +18.4% | SF Assessor-Recorder |
| FLAG-03 | high | 95014 naive tax/assessment ratio 1.335% vs county "typical" 1.1488% — explained by flat parcel charges | SCC assessment booklet |
| FLAG-04 | high | 94122 naive ratio 2.135% vs official secured rate 1.1816% — same explanation, larger effect | SF Treasurer |
| FLAG-05 | **critical** | Whether the 95014 house is the transferor's principal residence is unknown and decides whether any Prop 19 exclusion exists at all | R&TC § 63.2 |
| FLAG-06 | **critical** | The heir can claim the Prop 19 exclusion for only one property | R&TC § 63.2 |
| FLAG-07 | high | Insurance premiums not verifiable from any official source | CDI |
| FLAG-08 | medium | Market rent for 95014 is an assumption; aggregator medians are apartment-weighted | secondary |
| FLAG-09 | medium | Prop 19 cap officially known only to 15 Feb 2027 | BOE LTA 2025/009 |
| FLAG-10 | medium | Water provider for 95014 depends on the exact address (three systems serve the city) | City of Cupertino |
| FLAG-11 | medium | Solar export value depends on which NEM tariff applies; grandfathering end date assumed | CPUC |
| FLAG-12 | medium | Rent-control status of the 94122 units is not established — 1.6% vs 8.8%, a fivefold difference | SF.gov / CA AG |
| FLAG-13 | medium | Estate size unknown, so whether federal estate tax applies cannot be determined | IRS |
| FLAG-14 | low | Prop 43 (Nov 2026) does not change the Prop 13 rate or the 2% cap | SOS |
| FLAG-15 | medium | Whether a 3-unit building counts as a "family home" for Prop 19 is unsettled | R&TC § 63.2 |
| FLAG-16 | low | Land-value percentages used for depreciation are assumptions | SCC Assessor |

## Merge & conflict log

- 2026-11-06 · arena-2988121a · First rebase onto `origin/main` (6f990e7): resolved `COORDINATION.md` add/add conflict by integrating both boards; no work discarded.
- 2026-11-06 · arena-570be64c (parallel session) · Merged PR #3 (`arena/570be64c-cupertino2` → `main`); committed root `index.html` redirect to `docs/index.html` (Pages source is root `/`, not changeable by integration token); PR #4 merged; added root `.nojekyll` after legacy Jekyll build failure on main; logged build failure and fix.
- 2026-11-06 · arena-2988121a · Second rebase onto `origin/main` (4983448): kept the established root redirect (`index.html` theirs); `pages/*` preserved in repo; landing-page content remains in branch history (`d480257`, `86e9139`).
- 2026-11-06 · arena-2988121a · Third rebase onto `origin/main` (30273fb): resolved `COORDINATION.md` content conflict (their PR #4 / `.nojekyll` log entries merged into this board); no work discarded.
- 2026-11-06 · arena-2988121a · Pages build was errored on legacy Jekyll (no detailed error exposed by API); added root `_config.yml` (`title: Cupertino2`) and pushed to `main`; build status became `built`; live site verified via fetch of https://ginnymcfiner23-ux.github.io/Cupertino2/ (serves root `index.html` → `docs/index.html` dashboard).

- 2026-11-06 · c3099612 · Rebased onto the updated `origin/main`; resolved the `COORDINATION.md` add/add conflict by retaining the established integrated board and adding this session's scope/task. No prior session records or files were discarded. The Pages workflow uses the current legacy root source, removes `.nojekyll` so Jekyll can apply `_config.yml` exclusions, and builds the same output in CI to verify that `docs/`, `data/`, `pages/`, scripts, and coordination files are not published.

- 2026-11-06 · c3099612 · Applying the site commit also conflicted in `README.md` and root `index.html`: kept the integrated board, replaced the stale location-revealing README with the privacy-safe guide summary, and replaced the legacy redirect to `docs/index.html` with the new Home A/Home B landing page. Existing `docs/`, `data/`, and `pages/` files were retained in the repository but excluded from the legacy Jekyll output by `_config.yml` and checked in CI.
- 2026-11-06 · c3099612 · A direct Pages API request to change `build_type` from `legacy` to `workflow` returned HTTP 403 (`Resource not accessible by integration`). To avoid claiming an Actions deploy or publishing the old directories, the workflow was changed to validate the legacy Jekyll output and `_config.yml` explicitly excludes non-site content; the root `.nojekyll` was removed so those exclusions can run. Deployment remains pending a successful post-merge Pages build and output check.

- 2026-11-06 · arena-55de235e · First rebase onto `origin/main`: resolved `COORDINATION.md` add/add conflict by adopting the integrated board and folding this session’s initial standalone claims (T02–T14) into re-verification tasks T200–T203; no other session’s content discarded.

## Completion log

- 2026-11-06 · arena-570be64c · T010–T100 complete; PR #1 merged (https://github.com/ginnymcfiner23-ux/Cupertino2/pull/1); PR #3 and PR #4 merged; root redirect + `.nojekyll` committed; live dashboard at `docs/index.html` via GitHub Pages root source.
- 2026-11-06 · arena-2988121a · T001–T010 complete; site authored (`pages/*`, `assets/style.css`); PR #2 opened (`arena/2988121a-cupertino2` → `main`): https://github.com/ginnymcfiner23-ux/Cupertino2/pull/2 ; PR #2 merged into `main`; GitHub Pages live (root `/` → `docs/index.html`); deploy verified.
- Final results: PR #2 merged into `main`; Pages URL = https://ginnymcfiner23-ux.github.io/Cupertino2/ (redirects to `docs/index.html`).
- 2026-11-06 · arena-55de235e · T200–T202 complete (re-verification + gap-fill + full owner-history restore); PR #12 from `arena/55de235e-cupertino2` → `main` (merge result recorded in the PR record below).
- 2026-11-06 · arena-570be64c · FINAL (integration record): PR #1 `arena/570be64c-cupertino2` → `main` MERGED (6f990e7, merge commit, no auto-merge). PR #3 (root `index.html` redirect to `docs/`) MERGED. PR #4 (root `.nojekyll`) MERGED. Live site verified by fetch: https://ginnymcfiner23-ux.github.io/Cupertino2/ (serves `docs/index.html` dashboard; `docs/flagged.html`; `docs/projections.html` all render with sources). Pages build history: several runs for this session's and other sessions' commits were `cancelled` (superseded by newer pushes) and were reported by the Pages API as `errored`; the run for `efc0196` (latest at verification) completed `success`. Both `docs/` (this session) and `pages/` (arena-2988121a) remain on `main`; both are reachable from the repo; neither was deleted. Pages source stays `main` `/` (integration token cannot change it).
| T130 | Analytical dashboard: parcel bill model, Prop 19 scenarios, three-strategy comparison, 94122 rental economics, sell-now vs hold-to-death | done | b58dfdcf | `tools/model.py`, `data/model.json` | 45 official + 7 secondary sources | Deterministic; all inputs disclosed |
| T131 | Dashboard site build: 13 pages, source link on every table row | done | b58dfdcf | `tools/build_site.py`, `site/**` | — | 424 rows, 0 without a source link |
| T132 | PII gate for the published output | done | b58dfdcf | `tools/pii_scan.py` | — | Fails build on name/address/phone/e-mail/SSN/APN/trust name |
| T133 | Verification harness: source-link, internal-link, unresolved-value, PII | done | b58dfdcf | `tools/verify.py` | — | Exits non-zero on failure |
| T134 | Integration with sessions c3099612 / arena-570be64c / arena-2988121a | done | b58dfdcf | repo-wide | — | See Merge & conflict log |


**Session b58dfdcf (this session):** opened and read the full text of R&TC § 63.2, § 62,
§ 51 and § 17043 (leginfo) and Civ. Code § 1947.12; BOE Prop 19 page and LTA 2025/009;
BOE 2026 LTA index (confirming LTA 2026/002 "2026-27 California Consumer Price Index" and
LTA 2026/026 Prop 19 FAQ); IRS estate-tax page, IR-2025-103, Rev. Proc. 2025-32, Topic 409
and the NIIT page; 26 U.S.C. § 1014 and § 1411 (via govinfo); SF Treasurer secured property
taxes; SF.gov rent increases; CA Attorney General rent caps; SFPUC Prop 218 notice; Santa
Clara County Assessor Prop 13 FAQ and assessment booklet; SOS ballot measures hub.
- **Corrections found and applied:** `sf.gov/information/paying-your-property-taxes` 404 →
  replaced with `sftreasurer.org/property/secured-property-taxes`, which also showed the
  current rate is the FY2026-27 figure of **1.18162182%** (prior session's note already
  recorded this; the dashboard model uses it). `uscode.house.gov` deep links 404 (site is
  in a temporary format) → all four US Code citations moved to `govinfo.gov/link/uscode/26/`.
  `boe.ca.gov/proptaxes/pdf/pub801.pdf` 404 → that source dropped; the base-year-value-
  transfer row now cites the SCC Assessor Prop 19 overview and the Prop 19 FAQ to BOE LTA
  2026/026.
- **Could not be retrieved:** FTB rate tables (404 on the rates page), Cal Water Bear Gulch
  rate page (404), `irs.gov` newsroom short link (404), two `sf.gov` rent-increase paths
  (404). Left blank or flagged rather than inferred.
- **Note on IRS Topic 409:** the page still displays 2025 capital-gains thresholds. It is
  cited only for the rate structure (0/15/20% and the 25% depreciation slice); 2026
  thresholds come from Rev. Proc. 2025-32.


### Session b58dfdcf flag register (FLAG-01 … FLAG-16, each with a source link)

| ID | Severity | Issue | Source |
|---|---|---|---|
| FLAG-01 | high | 2026 property tax blank for the 95014 parcel | SCC Assessor |
| FLAG-02 | medium | 94122 has no 2026 row; 2021 shows -5.9% while assessment rose 1%; 2018 shows +18.4% | SF Assessor-Recorder |
| FLAG-03 | high | 95014 naive tax/assessment ratio 1.335% vs county "typical" 1.1488% — explained by flat parcel charges | SCC assessment booklet |
| FLAG-04 | high | 94122 naive ratio 2.135% vs official secured rate 1.1816% — same explanation, larger effect | SF Treasurer |
| FLAG-05 | **critical** | Whether the 95014 house is the transferor's principal residence is unknown and decides whether any Prop 19 exclusion exists at all | R&TC § 63.2 |
| FLAG-06 | **critical** | The heir can claim the Prop 19 exclusion for only one property | R&TC § 63.2 |
| FLAG-07 | high | Insurance premiums not verifiable from any official source | CDI |
| FLAG-08 | medium | Market rent for 95014 is an assumption; aggregator medians are apartment-weighted | secondary |
| FLAG-09 | medium | Prop 19 cap officially known only to 15 Feb 2027 | BOE LTA 2025/009 |
| FLAG-10 | medium | Water provider for 95014 depends on the exact address (three systems serve the city) | City of Cupertino |
| FLAG-11 | medium | Solar export value depends on which NEM tariff applies; grandfathering end date assumed | CPUC |
| FLAG-12 | medium | Rent-control status of the 94122 units is not established — 1.6% vs 8.8%, a fivefold difference | SF.gov / CA AG |
| FLAG-13 | medium | Estate size unknown, so whether federal estate tax applies cannot be determined | IRS |
| FLAG-14 | low | Prop 43 (Nov 2026) does not change the Prop 13 rate or the 2% cap | SOS |
| FLAG-15 | medium | Whether a 3-unit building counts as a "family home" for Prop 19 is unsettled | R&TC § 63.2 |
| FLAG-16 | low | Land-value percentages used for depreciation are assumptions | SCC Assessor |

## Merge & conflict log

- **2026-11-06 — session `b58dfdcf` rebased onto `main` (PR #9), which had advanced past
  the branch point.** Their `main` contained PR #7 from session `c3099612`, which replaced
  the root redirect with an eight-page privacy-safe guide and switched Pages validation to
  a Jekyll-output check. Three-way conflicts arose in `README.md`, `COORDINATION.md` and
  `.github/workflows/pages.yml`. Resolved as follows, discarding nothing from any session:
  - **CORRECTION (2026-11-06, follow-up commit):** the first pass at this resolution used
    `git checkout --theirs`, and **during a rebase `--theirs` is the commit being replayed**,
    not the upstream. That overwrote session `c3099612`'s `Verify and audit Pages output`
    workflow with this session's Pages deploy workflow. Caught within minutes by reading
    the workflow list on `main`, and reverted: `pages.yml` is restored byte-for-byte to
    `b058c72`. The deploy workflow is **not** reinstated — Pages is on the legacy root
    source, so it could never have succeeded, and this session has no business owning the
    single Pages deployment. `site-build.yml` remains as a CI check only. Lesson recorded
    here: in a rebase, `--ours` is the upstream, not `--theirs`.
  - `.github/workflows/pages.yml` — **kept the incoming (c3099612) version in full.** Their
    validation workflow guards the live root guide and fails the build if legacy or
    development directories leak into the Pages output. The dashboard's own build and
    verification moved to a new, separate workflow at `.github/workflows/site-build.yml`,
    which rebuilds `site/`, re-runs both checks and uploads the result as an artifact. It
    does not touch Pages: Pages is on the legacy root source, so there is exactly one
    deployment and it remains theirs.
  - `README.md` — kept the guide's README verbatim and **appended** a "Research workspace
    and analytics dashboard (session b58dfdcf)" section, including a table distinguishing
    the two published views and their different privacy postures.
  - `COORDINATION.md` — kept the integrated board structure and **added** this session's
    row, tasks T130–T134, its verification notes, and this log entry. No prior session's
    rows, tasks or notes were removed.
  - `_config.yml` — **additive change only**: `site/` is deliberately left publishable so
    the dashboard is served at `/site/`, while `tools/`, `research/` and `VERIFICATION.md`
    were added to the exclude list so development files stay out of the Pages output. The
    existing exclusion list was not otherwise altered.
- **Privacy-posture divergence, recorded not overridden.** Session `c3099612` chose to
  publish no ZIP codes, values, rents or bills at all. This session's dashboard publishes
  ZIP codes and the requester's own estimates, each labelled `supplied` or `assumption`
  and each listed on the Flagged page, on the basis that a ZIP code is not personal
  information and the requester's own brief identifies the properties by ZIP. Nothing in
  either view names a person, address, parcel, account or trust. Flagged so the user can
  choose.

## Session b58dfdcf — PR, merge and deployment record

| PR | Title | Merged | Merge commit | Result |
|---|---|---|---|---|
| [#9](https://github.com/ginnymcfiner23-ux/Cupertino2/pull/9) | Analytics dashboard: inherit/sell/rent model + Pages site under `site/` | 2026-11-06T13:48:28Z | `1fb9f75` | Merged to `main`. 2 commits, 79 files. |
| [#10](https://github.com/ginnymcfiner23-ux/Cupertino2/pull/10) | Restore `c3099612`'s Pages verification workflow (rebase `--theirs` mistake in PR #9) | 2026-11-06T13:50:43Z | (follow-up on `main`) | Merged to `main`. `pages.yml` restored byte-for-byte to `b058c72`. |
| [#11](https://github.com/ginnymcfiner23-ux/Cupertino2/pull/11) | Link the guide to the dashboard; record deployment | pending | — | Additive: one nav entry and one footer link on `index.html`. |

**Deployment confirmed live (checked 2026-11-06, with cache-busting query strings):**

| URL | Serves |
|---|---|
| `https://ginnymcfiner23-ux.github.io/Cupertino2/` | `Overview \| Property Transition Guide` — session `c3099612`'s guide (unmodified) |
| `https://ginnymcfiner23-ux.github.io/Cupertino2/decision.html`, `/process.html`, `/outlook.html` | Guide pages, intact |
| `https://ginnymcfiner23-ux.github.io/Cupertino2/site/` | `Executive Summary · Cupertino2` — this session's dashboard |
| `https://ginnymcfiner23-ux.github.io/Cupertino2/site/assets/style.css` | Dashboard stylesheet |

Pages is on the **legacy `main`-branch root source** (`build_type: legacy`, confirmed via
the Pages API), and `site/` is deliberately not excluded in `_config.yml`, so the dashboard
publishes under `/site/` with no Actions-based deployment at all.

**Incident and recovery.** The Pages deploy workflow that briefly reached `main` in PR #9
(run 42228482134, 13:48:31) succeeded and published this session's `site/` **at the Pages
root**, momentarily replacing the guide's front page. Two things limited the damage: the
legacy Jekyll build for the same push ran immediately afterwards (13:50:45) and
republished the root from `main`, and PR #10 removed the deploy workflow before it could
run again. Verified after recovery: the guide's `index.html`, `decision.html`,
`process.html` and `outlook.html` all serve their own content, not the dashboard's. The
only lasting effect is that the five filenames shared between the two views (`index.html`,
`costs.html`, `taxes.html`, `process.html`, `sources.html`) now serve the **guide's**
version at the root and the **dashboard's** version under `/site/`, which is the intended
arrangement. Nothing in `git` was ever overwritten — the deploy only writes the Pages
artifact.

**A caution for whoever reads this next:** GitHub Pages CDN caching is aggressive. Two
fetches of `/` returned dashboard content for several minutes *after* the legacy build had
already restored the guide. Always re-check with a `?cb=<timestamp>` query string before
concluding that a page is wrong.

**Checks at the final commit:** `scripts/check_site.py` → 8 guide pages clean, no visible
ZIP codes, no external assets. `tools/pii_scan.py site/` → clean. `tools/verify.py` →
424 table rows, 0 without a source link, 0 broken internal links, 0 unregistered external
links, 0 unresolved values.

**Open items for a later session** (none blocks the deploy):
- Confirm whether the Cupertino house is the transferor's principal residence (FLAG-05) —
  the single most consequential open fact.
- Confirm the certificate-of-occupancy date for the 94122 units (FLAG-12) — a fivefold
  difference in allowable rent growth.
- Get live insurance quotes and the solar interconnection date (FLAG-07, FLAG-11).
- Work through `data/urls.txt`; `VERIFICATION.md` §3 lists the priority order.
- Decide whether the two views should stay separate. The guide withholds ZIP codes,
  values, rents and bills entirely; the dashboard publishes them with provenance labels.
  Both omit personal identifiers. This is the user's call, not a session's.

