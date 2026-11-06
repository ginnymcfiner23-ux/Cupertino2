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
| T001 | Create coordination board (this file) | in progress | arena-2988121a | COORDINATION.md | — | Initial claim |
| T002 | Executive summary + anonymization placeholders | unclaimed | — | docs/executive-summary.md | TBD | Anonymize all personal info |
| T003 | Step-by-step trust inheritance process (CA) | unclaimed | — | docs/inheritance-process.md | TBD | CA probate, trustee duties, title transfer |
| T004 | Property tax & assessment research (Prop 13, 58, 19; county data) | unclaimed | — | docs/property-tax.md | TBD | Santa Clara County + SF Assessor |
| T005 | Ownership cost projections (water, electricity, insurance, maintenance) | unclaimed | — | docs/ownership-costs.md | TBD | Cupertino 95014 + SF 94122 |
| T006 | Rent vs. live vs. sell financial analysis | unclaimed | — | docs/rent-vs-live-vs-sell.md | TBD | Projections with inflation/tax factors |
| T007 | Inheritance / estate tax thresholds (federal, state, local) | unclaimed | — | docs/inheritance-tax.md | TBD | Federal exemption, CA has no estate/inheritance tax |
| T008 | Pending law changes affecting inheritance/property tax | unclaimed | — | docs/law-changes.md | TBD | TCJA sunset, CA proposals |
| T009 | Site build: landing page + dashboard subpages, tables with sources | unclaimed | — | index.html, pages/*, assets/* | TBD | GitHub Pages static site |
| T010 | Line-by-line verification + Flagged for Review page | unclaimed | — | pages/flagged-for-review.html | TBD | Every table row sourced or flagged |
| T011 | GitHub Pages deployment + broken-link check | unclaimed | — | site settings, GH Pages | TBD | Do not merge a broken deploy |
| T012 | Pull request + merge to main + record results | unclaimed | — | PR on GitHub, COORDINATION.md | TBD | PR from arena/2988121a-cupertino2 to main |

## Completed & verified log
(None yet)

## Handoffs / irregularities
(None yet)
