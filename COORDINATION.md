# COORDINATION.md — Cupertino2 shared task board

Session branch: `arena/2988121a-cupertino2`
This session ID: `arena-2988121a`

## Rules (per project instructions)
- Claim a task by writing your session ID in the Owner column, then commit and push the claim immediately.
- Never start a task another session has claimed.
- Keep scopes non-overlapping: each session works on its own branch/worktree and edits only files in its claimed scope.
- If a task requires changing a file owned by another session, log the request here instead of editing it.
- Make small, frequent commits; run `git pull --rebase` before every push.
- On merge conflict: stop, resolve without discarding the other session's work, log what happened.
- A claim older than 60 minutes with no commits may be taken over by another session (note the handoff here).
- `needs review` means published on the Flagged for Review page and does not block other work.
- When finished, record sources, verification performed, and irregularities here, and mark the task done.
- Shared outputs (table data, site index/navigation) are changed only by the final integration session once all other tasks are done.

## Task board

| Task ID | Description | Status | Owner | Files touched | Sources verified | Notes |
|---|---|---|---|---|---|---|
| T001 | Create coordination board (this file) | done | arena-2988121a | COORDINATION.md | — | Claimed + pushed 2026-11-06 |
| T002 | Executive summary + anonymization placeholders | done | arena-2988121a | pages/executive-summary.html | IRS, BOE, CA RTC, county assessors | All personal info anonymized |
| T003 | Step-by-step trust inheritance process (CA) | done | arena-2988121a | pages/inheritance-process.html | CA Probate Code, BOE, IRS, county assessors | 60-day notice, BOE-19-P, PCOR |
| T004 | Property tax & assessment research (Prop 13, 58, 19; county data) | done | arena-2988121a | pages/property-tax.html | boe.ca.gov, SCC assessor booklet, sf.gov | Owner tables flagged unverified |
| T005 | Ownership cost projections (water, electricity, insurance, maintenance) | done | arena-2988121a | pages/ownership-costs.html | sjwater.com tariffs, sfpuc.gov, CDI | Blanks where unverified |
| T006 | Rent vs. live vs. sell financial analysis | done | arena-2988121a | pages/decision-analysis.html | Projections (assumptions stated) | Sell-and-reinvest recommended direction |
| T007 | Inheritance / estate tax thresholds (federal, state, local) | done | arena-2988121a | pages/inheritance-tax.html | irs.gov i706, rp-25-32, RTC 13301 | $15M exclusion 2026; CA none |
| T008 | Pending law changes affecting inheritance/property tax | done | arena-2988121a | pages/law-changes.html | Public Law 119-21, BOE LTA 2025/009 | Monitoring checklist included |
| T009 | Site build: landing page + dashboard subpages, tables with sources | done | arena-2988121a | index.html, pages/*, assets/style.css | All rows carry source or unverified flag | HTML validated; links checked |
| T010 | Line-by-line verification + Flagged for Review page | done | arena-2988121a | pages/flagged-for-review.html | Source link on every table row | 14 flagged items listed |
| T011 | GitHub Pages deployment + broken-link check | unclaimed | — | repo settings (gh pages API) | — | Not started; do after merge to main |
| T012 | Pull request + merge to main + record results | unclaimed | — | PR on GitHub, COORDINATION.md | — | Not started |

## Completed & verified log
- T001 done: COORDINATION.md created and pushed (commit 86de27f).
- T002–T010 done: all site content authored on branch arena/2988121a-cupertino2.
  - Verified against official sources: IRS Form 706 instructions (2026 exclusion $15,000,000; 40% top rate), IRS Rev. Proc. 2025-32, IRS Newsroom (OBBBA/Pub. L. 119-21), IRS Pub 559 & Form 709 instructions, BOE prop19 page, BOE Pub 801, BOE LTA 2025/009 ($1,044,586 cap), BOE Publication 29 (Prop 13), CA RTC §13301 via leginfo.legislature.ca.gov (no CA estate/inheritance/gift tax), Santa Clara County Assessor booklet ($7,000 homeowner's exemption; 1.1488% example rate; supplemental assessments), SF.gov exemptions, SJWC Schedule 1-C tariff (AL 629A), SFPUC Rate Schedules FY 2026–27.
  - Unverified items (owner-provided histories, market values, per-zip insurance, maintenance, SF rate, projection assumptions) flagged on pages/flagged-for-review.html with suggested official sources; never inferred.

## Handoffs / irregularities
- Repo contained only README.md; all site content created from scratch.
- No parcel addresses were provided, so county assessor roll verification is impossible; all owner-provided tables are flagged unverified.
- Remaining for this session: T011 enable GitHub Pages on main, T012 open PR arena/2988121a-cupertino2 -> main, merge, confirm deploy, record results here.
