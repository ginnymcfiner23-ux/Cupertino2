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
| T002 | Executive summary + anonymization placeholders | in progress | arena-2988121a | pages/executive-summary.html | IRS, BOE, CA RTC, county assessors | In draft |
| T003 | Step-by-step trust inheritance process (CA) | in progress | arena-2988121a | pages/inheritance-process.html | CA Probate Code, BOE, IRS | In draft |
| T004 | Property tax & assessment research (Prop 13, 58, 19; county data) | in progress | arena-2988121a | pages/property-tax.html | boe.ca.gov, sccassessor booklet, sf.gov | In draft |
| T005 | Ownership cost projections (water, electricity, insurance, maintenance) | in progress | arena-2988121a | pages/ownership-costs.html | sjwater.com tariffs, sfpuc.gov, CDI | In draft |
| T006 | Rent vs. live vs. sell financial analysis | in progress | arena-2988121a | pages/decision-analysis.html | Projections (assumptions stated) | In draft |
| T007 | Inheritance / estate tax thresholds (federal, state, local) | in progress | arena-2988121a | pages/inheritance-tax.html | irs.gov i706, rp-25-32, RTC 13301 | In draft |
| T008 | Pending law changes affecting inheritance/property tax | in progress | arena-2988121a | pages/law-changes.html | Public Law 119-21, BOE LTA | In draft |
| T009 | Site build: landing page + dashboard subpages, tables with sources | unclaimed | — | index.html, pages/*, assets/style.css | — | Not started |
| T010 | Line-by-line verification + Flagged for Review page | unclaimed | — | pages/flagged-for-review.html | — | Not started |
| T011 | GitHub Pages deployment + broken-link check | unclaimed | — | repo settings (gh pages API) | — | Not started |
| T012 | Pull request + merge to main + record results | unclaimed | — | PR on GitHub, COORDINATION.md | — | Not started |

## Completed & verified log
- T001 done: COORDINATION.md created and pushed to origin/arena/2988121a-cupertino2 (commit 86de27f).

## Handoffs / irregularities
- Repo contains only README.md; all site content must be created from scratch.
- User-provided property tax history tables (Cupertino 95014, SF 94122) and estimated market values ($3,100,000 / $1,800,000, Nov 2026) are NOT verified against county assessor records — no parcel addresses were provided, so parcel-level lookup is not possible. These rows will be flagged "unverified — user-provided" on the site per the verification rule.
