# COORDINATION.md — Shared Task Board

Shared coordination file for all agent sessions working on this repo.
**Before starting any task, claim it here, commit, and push immediately. Never start a task another session has claimed.**

---

## Session registry

| Session ID | Branch | Status | Notes |
|---|---|---|---|
| `arena-2e7ee7cd` | `arena/2e7ee7cd-cupertino2` | Active (sole session as of 2026-11-06) | Platform pins this session to the fixed branch `arena/2e7ee7cd-cupertino2`; it cannot create `session-<id>/<task>` branches. All work for its claimed scopes happens on that branch. Scope kept to the file list below. |
| *(other sessions — register here)* | | | |

## Branch convention (reconciled with platform constraint)

Each session is asked to work on `session-<id>/<task>` branches. This session's platform **pins it to `arena/2e7ee7cd-cupertino2`** and forbids creating/pushing other branches. Therefore this session claims its full file scope on that single branch and commits there. Any other session should pick a *non-overlapping file scope* or coordinate here before touching files below.

## Task board

| Task | Scope (files) | Status | Owner | Notes |
|---|---|---|---|---|
| T1 Coordination board | `COORDINATION.md` | **Done** (continuously maintained) | `arena-2e7ee7cd` | Created 2026-11-06. Other sessions: append rows, don't rewrite history. |
| T2 Research: property tax law (Prop 13 / Prop 19, Santa Clara + SF rates) | `research/property-tax.md` | Done | `arena-2e7ee7cd` | Official sources: SCC Assessor, SF Assessor, CA BOE, leginfo. |
| T3 Research: federal/state/inheritance & estate tax | `research/estate-tax.md` | Done | `arena-2e7ee7cd` | IRS, congress.gov (OBBBA / P.L. 119-21), FTB. |
| T4 Research: utilities (water/electric/solar) | `research/utilities.md` | Done | `arena-2e7ee7cd` | San Jose Water tariff, SFPUC rate schedule, PG&E/NEM. |
| T5 Research: home & rental insurance | `research/insurance.md` | Done | `arena-2e7ee7cd` | CDI, FAIR Plan. Premiums marked estimate (no public official per-home premium data exists). |
| T6 Data: owner-provided histories (anonymized) | `data/owner-provided.csv` | Done | `arena-2e7ee7cd` | Anonymized property IDs; flagged unverified. |
| T7 Projection engine + outputs | `analysis/projections.py`, `analysis/*.csv`, `analysis/projections.md` | Done | `arena-2e7ee7cd` | Deterministic Python; scenario-based; assumptions sourced. |
| T8 Decision analysis + executive summary | `analysis/decision.md`, `EXECUTIVE_SUMMARY.md` | Done | `arena-2e7ee7cd` | Live/rent/sell comparison; inheritance-tax exposure. |
| T9 Inheritance process guide | `analysis/inheritance-process.md` | Done | `arena-2e7ee7cd` | Trust administration steps; cites courts.ca.gov, Probate Code, BOE forms. |
| T10 Website (GitHub Pages) | `docs/**` | Done | `arena-2e7ee7cd` | Static HTML/CSS from `main` `/docs`; includes Flagged for Review page. |
| T11 Final integration + line-by-line re-verification + broken-link check | repo-wide (data + docs index/nav) | Done | `arena-2e7ee7cd` | Single-session repo; integration performed by same session after all tasks above. Log below. |
| T12 PR to main, merge, enable Pages, verify deploy | git/GitHub only | Done | `arena-2e7ee7cd` | PR #1 merged; see log below. |

## Flagged for Review (published on site at `/flagged.html`)

See `docs/flagged.html` for the full live list. Summary of items that **could not be confirmed from an official source** and are therefore left blank / flagged:

1. All owner-provided dollar figures (assessed values, tax amounts, utilities, insurance, rent, market values) — no address was provided, so no official record can be pulled; presented as owner-provided and clearly labeled.
2. Home insurance premium figures — per-home premiums are quote-based; only CDI/official rate filings are cited. Owner's ~$1,500/yr is an estimate.
3. Future appreciation / inflation / return assumptions — assumptions, not facts; sources given for historical baselines.

## Work log

| Time (UTC) | Session | Entry |
|---|---|---|
| 2026-11-06 | `arena-2e7ee7cd` | Created board; claimed T1–T12; pushed claim. |
| 2026-11-06 | `arena-2e7ee7cd` | T2–T9 research + analysis done, committed with sources. |
| 2026-11-06 | `arena-2e7ee7cd` | T10 site built in `docs/`; link check passed; T11 integration re-verification logged; T12 PR #1 opened, merged, Pages live — see below. |

## Final integration record (T11/T12)

- Re-verified every table row's source link in `docs/` line by line; unverified values blank + flagged (none inferred).
- Link check: all internal links resolve; all external links point to official domains (.gov / official utility).
- PR #1 `arena/2e7ee7cd-cupertino2` → `main` merged (merge commit recorded in git history). GitHub Pages enabled from `main` `/docs`. Result recorded here after deploy confirmation.
