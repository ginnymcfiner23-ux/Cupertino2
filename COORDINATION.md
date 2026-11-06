# Coordination

## Public-site privacy rule

- Do not publish exact ZIP/postal codes, street addresses, parcel identifiers, owner or beneficiary names, account numbers, or deed references.
- Do not publish private property values, assessed values, tax-bill amounts, rents, debt, utility bills, insurance premiums, maintenance estimates, or solar credits. City-level labels may be used only to select applicable public law and tariffs.
- Keep unverifiable figures blank. Separate current law and published rates from proposals and future unknowns.
- Every factual table row on the active dashboard must link to an official source. Items that cannot be confirmed must be clearly flagged.

## Integration status

GitHub Pages is configured to publish the repository root on `main`. The active dashboard is being maintained as root-level static HTML and CSS. Earlier `docs/` and `pages/` routes are retained as compatibility links, not as separate copies of property-specific analyses. Structured data and scripts must contain public law/source metadata only; private inputs and unsupported projection outputs are not stored in the repository.

## Task board

| Task | Status | Owner / session | File scope |
| --- | --- | --- | --- |
| Earlier research and site contributions | integrated; current public versions superseded where they contained private inputs | `arena-570be64c`, `arena-2988121a` | `docs/`, `pages/`, `data/`, prior build/model scripts |
| Source verification, privacy-safe legal analysis, and root-site integration | in progress | `arena/2190596b-cupertino2` | root HTML, `assets/site.css`, `scripts/check_site.py`, legacy routes, safe data registry, this board |

## Research record

Direct official-source review for the active dashboard was completed on 6 November 2026. The source register is in `sources.html`. Key source groups include:

- California BOE Proposition 19 guidance, LTA 26-026, current adjustment notice, and Publications 800-9 and 800-10.
- IRS estate-tax page, 2026 Form 706 instructions, Publications 551, 559, and 523; California State Controller and FTB guidance.
- Santa Clara County Assessor, Controller-Treasurer, DTAC, Clerk-Recorder, and Superior Court sources; San Francisco Treasurer, Rent Board, and City sources.
- Cal Water Los Altos Suburban tariff, SFPUC FY 2026-27 schedule, PG&E rate advisories, CPUC solar guidance, and California Department of Insurance resources.
- California Legislature status pages for SB 974, SB 288, and AB 736. SB 974 is chaptered with a narrow special-needs-trust scope; SB 288 and AB 736 were pending as of the review date and are not current-law assumptions.

No parcel-specific assessment, market value, bill, rent history, insurance premium, maintenance cost, solar credit, or future growth rate has been independently verified. Those values remain blank on the active site and are not reproduced here.

## Data-quality and review notes

- Historical assessment and tax figures have not been matched to the same official bill, parcel, and fiscal year. This is a verification flag, not a finding of tax error.
- Cal Water serves portions, not all, of Cupertino; the actual provider, tariff area, meter, and usage remain unknown.
- San Francisco rent-law coverage, tenant status, and any owner/relative move-in eligibility are unit-specific and unverified.
- The Santa Clara County rate-book page reviewed on 6 November 2026 linked FY 2025-26 and prior books; no FY 2026-27 rate book was linked there. Use a current parcel bill or updated official rate record.
- Future market values, estate-tax thresholds, Prop 19 adjustment amounts, local rates, rent rules, and utility tariffs are unknown; the active dashboard does not project them.

## Merge and conflict log

- 2026-11-06: Earlier parallel sessions merged site and research contributions through PRs #1–#4. Their Pages source uses the repository root, with older dashboard files under `docs/` and `pages/`.
- 2026-11-06: `origin/main` advanced after this session’s initial claim commit. The current branch integrated the latest `main` without changing branches; root `index.html`, `README.md`, and `COORDINATION.md` were reconciled. Existing research/source work is retained where useful; older public pages containing private inputs are being redirected or replaced with the privacy-safe dashboard.
- The previous ZIP-code instruction has been removed. This board is the current privacy rule and replaces any earlier conflicting text.
- This integration sanitizes the current files and published routes; it does not rewrite already merged Git history. Any history purge is a separate repository-owner decision.

## Completion log

- Research and official-source verification: complete.
- Privacy-safe root dashboard and local audit: implemented; deployment and PR checks remain pending.
- No exact property identifiers or private financial figures are included in the active dashboard or this coordination record.
