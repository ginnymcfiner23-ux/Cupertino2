# Research log: California family-property planning

**Last checked:** 6 November 2026, 13:23 UTC
**Scope:** Public, official-law and local-cost references for the static dashboard and review page. No address, ZIP code, parcel number, family identifier, user-provided home value, tax history, rent, utility bill, insurance amount, or other private property input is reproduced here.

The corresponding human-readable citations are linked by source ID in [`review.html`](review.html#sources). This log records the conclusions, limits, and unresolved items that shape the dashboard. It is educational research, not a legal, tax, accounting, appraisal, insurance, or investment opinion.

## Research and publication rules

- Prefer statutes, agency guidance, official tariff sheets, official election results, and bill-status pages.
- Date all time-sensitive numbers. A rate or threshold is a snapshot, not a forecast.
- Label a bill as enacted only after chaptering/enactment; keep introduced, held, or canceled proposals out of current-law calculations.
- Do not infer a water provider from a city or ZIP code. Confirm the actual service account and meter.
- Keep property-specific eligibility, values, occupancy, rent coverage, and costs unresolved until supported by the relevant records.
- Calculator forms start blank and run locally in the browser. There is no server-side form endpoint, analytics, cookie, external script, `fetch`/XHR, or browser-storage write. The Content Security Policy sets `connect-src 'none'`; clearing the page or leaving it clears transient values.

## Legal and tax findings

### California Proposition 19

- The intergenerational exclusion is not a blanket inheritance exclusion. For the transfer types described by the BOE, eligibility generally requires a parent-child transfer or (under limited conditions) grandparent-grandchild transfer; for a grandchild, the relevant middle-generation parents generally must be deceased on the transfer date. The statutory step-parent exception is narrow. See **S01–S02**.
- A family home must qualify for the transferor’s Homeowners’ or Disabled Veterans’ Exemption, and an eligible transferee must make it their principal residence. The statute also separately covers qualifying family farms. A family home/farm may be transferred during life or at death, including through a trust; the property-specific change-in-ownership date and route require review. See **S02**.
- BOE LTA 2026/026 says separately assessed dwelling units in a multi-unit property must independently satisfy the rules. Its apartment-complex illustration identifies the transferor-occupied principal-residence unit as qualifying and treats the other units separately. The BOE’s separate single-family-plus-ADU/JADU example has different conditions. Therefore, neither the parcel label nor an heir’s planned occupancy of another apartment establishes eligibility. See **S02**.
- The transferee generally must claim the Homeowners’ or Disabled Veterans’ Exemption within one year and file the intergenerational-exclusion claim within three years of transfer or before a third-party transfer, whichever is earlier, subject to statutory and BOE exceptions. SB 293’s wildfire relief is specific to named disaster circumstances; it is not a general extension. See **S02, S24**.
- For eligible transfers dated **16 February 2025 through 15 February 2027**, the adjusted value-cap amount is **$1,044,586**. In a simple 100%-interest screen, the calculator uses factored base-year value + max(0, full cash value immediately before transfer − factored base-year value − $1,044,586). This is an arithmetic screen only; it does not resolve eligibility, unit splits, ownership percentages, Prop 8 value, reassessment, or the enrolled value. Recheck the adjustment for transfer dates outside this stated window. See **S03**.
- SB 974 was chaptered as **Chapter 665, Statutes of 2026**, on 27 September 2026, and is non-urgency legislation with a 1 January 2027 effective date. It adds a qualifying Probate Code §3604 special-needs trust as a transfer medium for the specified Prop 19 exclusion; it does not remove the home, occupancy, or value-cap tests. See **S23**.

### Death, estate, trust, and income taxes

- California Revenue and Taxation Code §13301 prohibits a standalone state or local gift, inheritance, succession, legacy, income, estate, or other tax on transfers by reason of death. That does not decide property-tax reassessment, income tax on later earnings, trust administration, or documentary transfer tax. See **S04**.
- For a U.S. citizen/resident who dies in **2026**, the IRS lists a **$15,000,000** Form 706 filing threshold. The gross estate is considered with adjusted taxable gifts and the specific gift-tax exemption. A portability election for a surviving spouse requires a Form 706 filing even when the estate is below the usual threshold; the ordinary due date is nine months after death, with a timely-requested six-month filing extension available. See **S05–S06**.
- The **2026 annual gift-tax exclusion is $19,000 per donee**. This is distinct from the estate-tax filing threshold and does not make every lifetime transfer tax-free. See **S07**.
- Inherited property is generally excluded from the recipient’s income, and its basis is generally fair market value at date of death, subject to exceptions. Later rent, interest, business income, depreciation, trust distributions, or sale gain has separate federal/California treatment. A qualified appraisal and records should be reviewed with a fiduciary tax professional. See **S08–S10, S34**.
- California Form 541 filing conditions differ for estates and trusts. The FTB’s 2025 guidance lists estate tests that include California decedent residency, income thresholds, California-source income, or a distribution; trust tests depend on California residency, California-source income, or distributions to a California resident and the trust’s gross/net income. Do not use a single threshold as a complete filing determination. See **S10**.
- A funded living trust can pass trust-held assets outside formal probate, but an asset omitted from the trust may need a separate route. California Probate Code §16061.7 generally gives notice obligations within 60 days after specified events and sets a trust-contest period; service, triggering facts, and exceptions require counsel review. Neither a trust nor avoiding probate by itself resolves estate, income, or property-tax questions. See **S11, S35**.

### Property tax and San Francisco transfer tax

- California’s general Proposition 13 baseline is a 1% ad valorem property-tax rate plus voter-approved bond debt. Base-year assessments generally receive an annual inflation factor capped at 2%; a temporary Proposition 8 decline-in-value assessment, new construction, change in ownership, direct charges, and special assessments can change the result. See **S16, S36**.
- San Francisco’s published secured-property tax rate for **FY 2026–27 is 1.18162182%**. An actual bill also includes direct charges/special assessments; supplemental or escape assessments may follow a reassessable event. See **S16**.
- San Francisco transfer tax is tiered by the entire value/consideration band—not a marginal-rate calculation. Its public rate schedule ranges from $2.50 per $500 above $100,000 through $250,000 to $30 per $500 for $25 million or more. A claimed inheritance exemption generally requires the required affidavit and Preliminary Change of Ownership Report, and documentation may be requested. An inheritance with no consideration and a later market sale are different transactions. See **S17–S18**.

### San Francisco rent references

- The Rent Board’s local allowable annual increase is **1.6% for 1 March 2026–28 February 2027**, for units covered by the ordinance and subject to separate requirements. See **S19**.
- The SF Rent Board lists **8.8%** as the AB 1482 maximum for units subject to the state rent cap from **1 August 2026–31 July 2027**. Units already governed by the lower SF rent-increase limits are not subject to the AB 1482 rent cap. Coverage and exemptions must be checked. See **S20**.
- San Francisco owner/relative move-in is not an automatic vacancy right: the official guidance describes a 36-month principal-residence requirement, generally one unit per building, ownership-share thresholds, protected-tenant rules, relocation payments, and notice/good-faith requirements. Seek current Rent Board and legal advice before an action. See **S21**.

## Local operating-rate checks

- Cupertino’s official service finder lists different service territories, including California Water Service and San Jose Water; confirm the provider by actual service address/account rather than ZIP. See **S12**.
- **Cal Water, Los Altos Tariff Area, residential metered single-family service:** tariff effective **1 October 2026**; 5/8-inch monthly service charge **$48.86**. Quantity rates are $2.8466/CCF for 1–6 CCF; $11.3542 for 7–20; $14.2607 for 21–30; and $17.0381 above 30. Separate surcharges/surcredits and other account conditions may apply. It is not a universal Cupertino tariff. See **S13**.
- **San Jose Water, residential general metered service:** CPUC-approved AL 629-A revised sheets effective **1 July 2026**; 5/8-inch monthly service charge **$79.67**; quantity rates $5.0355/CCF for 0–6, $7.5156/CCF over 6 through 12, and $14.3548/CCF over 12. Later 629-A revised sheets 2409-W onward control over the earlier 628-A sequence. The estimate excludes separate charges/credits and requires matching meter/account class. See **S14**.
- **SFPUC FY 2026–27:** 5/8-inch monthly water-service charge **$19.65**. Single-family water: first 4 CCF at $12.20/CCF, additional use at $13.55. Multi-family water: first 3 CCF per dwelling unit at $12.03/CCF, additional use at $12.91. Residential sewer: $6.62 monthly plus $20.74 per discharge unit, using default flow factors of 90% single-family / 95% multi-family. Stormwater is parcel-based and not included in the calculator; drought surcharge and account-specific adjustments may also apply. See **S15**.
- California DOI’s 2026 homeowners comparison profiles are hypothetical comparisons, not a property quote; the tool excludes wildfire surcharges. Obtain current coverage and eligibility directly from insurers. See **S22**.
- Solar savings are not projected. Legacy NEM and the Solar Billing Plan/Net Billing Tariff differ; verify system ownership, permission-to-operate/interconnection date, tariff, interval use, provider/CCA, export compensation, and storage. See **S32**.

## Legislation and proposal tracker

| Measure | Status checked 6 Nov 2026 | Treatment in dashboard |
| --- | --- | --- |
| California SB 974, Ch. 665 (2026) | Chaptered 27 Sep 2026; effective 1 Jan 2027 | Enacted, narrow special-needs-trust clarification; not a general Prop 19 expansion. |
| California SB 293, Ch. 539 (2025) | Chaptered 10 Oct 2025 | Enacted, disaster-specific wildfire clarification/claim relief. |
| California SB 710, Ch. 328 (2025) / AB 1516, Ch. 72 (2025) | Enacted; specified solar claim rules operative 1 Jan 2027 | Enacted, but solar exclusion is narrow and time-limited; property/system dates need assessor review. |
| California AB 698 | Official status page: active, pending referral; last action shown 9 Jun 2025 | Proposal; not a current charge. |
| California AB 2389 | Held under submission 14 May 2026 | Proposal; no extension assumed. |
| California SB 1329 | First hearing canceled at author’s request, 5 Aug 2026 | Proposal; no valuation change assumed. |
| U.S. H.R. 601 | Introduced 22 Jan 2025; referred to House committees, no later action listed | Proposal only; not current tax law. |
| U.S. S. 4196 | Introduced 25 Mar 2026; referred to Senate Finance, no later action listed | Proposal only; not current tax law. |

Sources: official California Legislature bill text/status and Congress.gov bill/status pages **S23–S30**. Status must be refreshed before relying on a proposal or effective date.

## Election snapshot

The San Francisco Department of Elections page said its **5 November 2026, 4:00 p.m.** results were preliminary and identified **6 November 2026, 4:00 p.m.** as the next update. At the last check at **13:23 UTC on 6 November**, the live page still showed that prior snapshot and about 86,700 ballots to count. Measure I: **No 53.37%, Yes 46.63%**; Measure J: **Yes 80.4%, No 19.6%**. Treat both figures as timestamped preliminary results; refresh the official page for the update and final certification. Source **S31**.

## Unresolved property-specific checks

No property-specific answer is established by public research alone. Collect and review:

1. Recorded deed, ownership/beneficial-interest terms, trust and amendments, and the legally relevant transfer date.
2. County assessor’s parcel/unit map, unit-level assessment, transferor’s actual principal-residence unit, eligible transferee’s intended occupancy, and homeowner/disabled-veteran exemption records.
3. Factored base-year value, transfer-date appraisal, current secured bill, parcel/direct charges, and any supplemental/escape assessments.
4. Tenant coverage, lease and rent history, allowed increase date, licenses/notices, and tenant protections.
5. Actual utility provider, account class, meter, consumption, stormwater and sewer account details, insurance quote/coverage, and maintenance records.
6. Solar ownership, system size, installation and permission-to-operate dates, interconnection tariff, battery, and tax-exclusion claim.
7. Estate/trust documents, beneficiaries and distributions, fiduciary income, estate/gift-tax history, filing elections, and professional tax analysis.

Until these records are reviewed, do not treat prior property-specific values, costs, tax/rent history, estimates, or long-range projections as verified. The public site intentionally contains none of those private values.
