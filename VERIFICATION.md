# VERIFICATION.md

How every number in this project was checked, what was confirmed, and what could not be
confirmed. Written so that any figure can be traced back by hand.

**Rule applied throughout:** a value is only written down if it comes from an official
government source. If it cannot, the value is either left blank or explicitly labelled
`assumption`, `supplied`, or `unverified`, and it appears on the site's
**Flagged for Review** page. Nothing was inferred to fill a gap.

---

## 1. What the automated checks do

| Check | Tool | Result |
|---|---|---|
| Every table row carries a source link | `tools/verify.py` | 424 rows checked, 0 without a link |
| No unregistered external links (nothing invented mid-page) | `tools/verify.py` | 52 URLs, all on the source register |
| No broken internal links | `tools/verify.py` | 0 |
| No unresolved values (`nan` / `None` / `undefined`) in output | `tools/verify.py` | 0 |
| No personal information in `site/` | `tools/pii_scan.py` | clean |
| Every flag id in `COORDINATION.md` exists in the data | `tools/verify.py` | 16 / 16 |

Run them with:

```
python3 tools/model.py        # recompute data/model.json
python3 tools/build_site.py   # regenerate site/
python3 tools/pii_scan.py site/
python3 tools/verify.py       # non-zero exit on failure
```

### URL liveness — important limitation

This sandbox has outbound network access **only** to `github.com`, `codeload.github.com`,
`api.github.com`, `registry.npmjs.org`, `pypi.org` and `files.pythonhosted.org`. The
verification script therefore **cannot** make HTTP requests to `irs.gov`, `boe.ca.gov`,
`sftreasurer.org` and so on, and `tools/verify.py` does not pretend to. Instead it writes
the complete list of external URLs to `data/urls.txt` (52 URLs) so each one can be fetched
and confirmed.

---

## 2. URLs fetched and read directly during this build

These were opened and their content read, not merely located by search. The quoted value is
what the page actually says.

| Fact | Value | Source | Confirmed wording |
|---|---|---|---|
| Federal estate basic exclusion, 2026 | $15,000,000 | [IRS IR-2025-103](https://www.irs.gov/newsroom/irs-releases-tax-inflation-adjustments-for-tax-year-2026-including-amendments-from-the-one-big-beautiful-bill) | "Estates of decedents who die during 2026 have a basic exclusion amount of $15,000,000, up from a total of $13,990,000 for estates of decedents who died in 2025." |
| OBBBA makes it permanent and indexes it | §70106 | [Rev. Proc. 2025-32](https://www.irs.gov/pub/irs-drop/rp-25-32.pdf) | "Section 70106 of the OBBBA amends § 2010(c)(3) by increasing the basic exclusion amount to $15,000,000 for calendar year 2026... These numbers are adjusted for inflation for taxable years beginning after December 31, 2026." |
| GST exemption, 2026 | $15,000,000 | [Rev. Proc. 2025-32](https://www.irs.gov/pub/irs-drop/rp-25-32.pdf) | "For calendar year 2026, the generation-skipping transfer exemption amount under § 2631(c) is equal to $15,000,000." |
| Annual gift exclusion, 2026 | $19,000 | [IRS IR-2025-103](https://www.irs.gov/newsroom/irs-releases-tax-inflation-adjustments-for-tax-year-2026-including-amendments-from-the-one-big-beautiful-bill) | "For tax year 2026, the annual exclusion for gifts remains at $19,000." |
| Form 706 filing threshold, 2026 | $15,000,000 | [IRS Estate tax](https://www.irs.gov/businesses/small-businesses-self-employed/estate-tax) | row "2026 … $15,000,000" in the year-of-death table |
| Portability requires a timely return | — | [IRS Estate tax](https://www.irs.gov/businesses/small-businesses-self-employed/estate-tax) | "estates of decedents survived by a spouse may elect to pass any of the decedent's unused exemption… This election is made on a timely filed estate tax return" |
| Net investment income tax | 3.8%; $200k / $250k / $125k | [IRS NIIT](https://www.irs.gov/individuals/net-investment-income-tax) | "liable for a 3.8 percent Net Investment Income Tax on the lesser of their net investment income, or the amount by which their modified adjusted gross income exceeds the statutory threshold amount" |
| NIIT statutory thresholds | $250,000 / $125,000 / $200,000 | [26 U.S.C. 1411(b)](https://www.govinfo.gov/link/uscode/26/1411) | "threshold amount" means… $250,000 (joint), ½ of that (MFS), $200,000 (any other case) |
| Step-up in basis | FMV at date of death | [26 U.S.C. 1014(a)](https://www.govinfo.gov/link/uscode/26/1014) | "the basis of property in the hands of a person acquiring the property from a decedent… shall be… (1) the fair market value of the property at the date of the decedent's death" |
| Capital gains rate ladder; 25% unrecaptured 1250 | 0/15/20%; 25% | [IRS Topic 409](https://www.irs.gov/taxtopics/tc409) | "a capital gains rate of 20% applies to the extent that your taxable income exceeds the thresholds set for the 15% capital gain rate"; "unrecaptured section 1250 gain… is taxed at a maximum 25% rate" |
| **Prop 19 value cap** | $1,044,586 | [BOE LTA 2025/009](https://www.boe.ca.gov/proptaxes/pdf/lta25009.pdf) | "the $1 million amount is adjusted to **$1,044,586**" for transfers 2/16/2025 – 2/15/2027 |
| Cap history | $1,000,000 / $1,022,600 / $1,044,586 | [BOE LTA 2025/009](https://www.boe.ca.gov/proptaxes/pdf/lta25009.pdf) | enclosure table |
| Cap is re-set every other 16 February | — | [BOE LTA 2025/009](https://www.boe.ca.gov/proptaxes/pdf/lta25009.pdf) | "The next adjustment of the $1 million amount will occur in February 2027." |
| Prop 19 before/after table | — | [BOE Prop 19](https://www.boe.ca.gov/prop19/) | "Eliminates exclusion for other real property other than the principal residence" |
| BOE-19-P and BOE-266 deadlines | 3 years / 1 year | [BOE Prop 19](https://www.boe.ca.gov/prop19/) | filing-requirements checklist |
| **Prop 19 statutory conditions** | § 63.2 | [R&TC 63.2](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=63.2.&lawCode=RTC) | (a)(1) "The transfer is required to be of a principal residence of the transferor, and become the principal residence of the transferee within one year of the transfer." (a)(1)(B) "file for the homeowners' or disabled veterans' exemption within a year" |
| Exclusion removed on move-out | § 63.2(a)(1)(C) | [R&TC 63.2](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=63.2.&lawCode=RTC) | (a)(1)(C) enrolment rule on the lien date following loss of eligibility |
| Revocable trust transfer excluded | § 62(d) | [R&TC 62](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=62.&lawCode=RTC) | "Any transfer by the trustor… into a trust for so long as (1) the transferor is the present beneficiary of the trust, or (2) the trust is revocable" |
| 2% assessment cap | § 51(a)(1)(D) | [R&TC 51](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=51.&lawCode=RTC) | "In no event shall the percentage increase for any assessment year… exceed 2 percent of the prior year's value." |
| BOE 2026-27 inflation factor | 1.02 | [BOE 2026 LTA index](https://www.boe.ca.gov/proptaxes/2026.htm) | "2026/002 — 2026-27 California Consumer Price Index" (PDF: [lta26002.pdf](https://www.boe.ca.gov/proptaxes/pdf/lta26002.pdf)) |
| Prop 13 1% rate and 2% cap | — | [Santa Clara County Assessor](https://asr.santaclaracounty.gov/faq/understanding-proposition-13) | "all real property has established base year values, a restricted rate of increase on assessments of no greater than 2% each year, and a limit on property taxes to 1% of the assessed value" |
| Santa Clara "typical" tax rate area | 1.1488% | [SCC Assessment Information booklet](https://files.santaclaracounty.gov/exjcpb1521/2024-10/2024_assessment_information_booklet.pdf) | base 1% + county bonds 0.0388% + school bonds 0.100% + water bonds 0.010% = $1.1488 per $100 |
| **SF secured property tax rate** | **FY 2026-27: 1.18162182%** | [SF Treasurer & Tax Collector](https://sftreasurer.org/property/secured-property-taxes) | "The secured property tax rate for Fiscal Year 2026-27 is 1.18162182%." |
| **SF allowed rent increase** | **1.6%** | [SF.gov](https://www.sf.gov/learn-about-rent-increases-san-francisco) | "Effective March 1, 2026, the allowed rent increase percentage is 1.6%… based on 60% of the increase in the Consumer Price Index for All Urban Consumers in the Bay Area." |
| AB 1482 cap, SF area | 8.8% (8/1/26–7/31/27) | [CA Attorney General](https://oag.ca.gov/rentcaps) | table row "San Francisco Area … 8.8%" |
| AB 1482 formula | 5% + CPI, max 10% | [Civ. Code § 1947.12](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=1947.12.&lawCode=CIV) / [CA AG](https://oag.ca.gov/tenants) | "cannot raise rent more than 10% total or 5% plus the percentage change in the cost of living – whichever is lower" |
| California 1% tax over $1m | § 17043 | [R&TC 17043](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=17043.&lawCode=RTC) | additional 1% on taxable income over $1,000,000 (source of the 13.3% top rate) |
| SFPUC water / stormwater charges | see table on Costs page | [SFPUC Prop 218 notice](https://www.sfpuc.gov/accounts-services/water-power-sewer-rates/proposed-water-sewer-rates-2026/proposition-218-notice) | 5/8" meter: $18.36 → $19.65 → $21.02; stormwater tier 1: $8.24 → $12.63 → $18.08 |
| Cupertino has three water systems | — | [City of Cupertino](https://www.cupertino.gov/Residents/Utilities/Water) | "three separate water systems… California Water Services… San Jose Water Company… The City's own water distribution infrastructure system" |

### Corrections made as a result of these checks

Three URLs that had been constructed rather than verified turned out to be dead, and one
published figure had been superseded. All were corrected before the site was built:

1. `sf.gov/information/paying-your-property-taxes` → 404. Replaced with
   `sftreasurer.org/property/secured-property-taxes`. Doing so also revealed that the
   current rate is the **FY 2026-27** figure of **1.18162182%**, not the FY 2025-26 figure
   of 1.18268325% that secondary sources were still quoting. The model was updated.
2. `uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title26-section1014` → 404 (the
   site is running "in a temporary format" and deep links are down). All four US Code
   references were switched to `govinfo.gov/link/uscode/26/<section>`, which resolve and
   return the statutory text.
3. `boe.ca.gov/proptaxes/pdf/pub801.pdf` → 404. That source was dropped. The Prop 19 FAQ
   is now cited to BOE LTA 2026/026, and the base-year-value-transfer row to the Santa
   Clara County Assessor's own Prop 19 overview.

One further observation: **IRS Topic 409 still displays 2025 capital-gains thresholds**
($48,350 / $533,400 for single) even though today is November 2026. This build cites Topic
409 only for the rate structure (0/15/20% and the 25% depreciation slice), which is
unchanged; the 2026 thresholds themselves come from Rev. Proc. 2025-32. Noted so nobody
reads 2025 thresholds off that page by mistake.

---

## 3. URLs on the register that were NOT individually fetched

Every remaining URL came from an official government or utility domain and was returned by
a search, but was not opened and read in full. They are listed in `data/urls.txt` and on
the site's **Sources** page for manual review. The ones that carry the most weight:

- [Santa Clara County Assessor](https://asr.santaclaracounty.gov/) — parcel rate book, appeal window
- [SF Assessor-Recorder](https://www.sf.gov/departments--assessor-recorder) — block/lot detail
- [SF Treasurer – Information for Heirs](https://sftreasurer.org/property/information-heirs)
- [Cal Water 2026 IIP notice, Bear Gulch](https://es.calwater.com/docs/iip/2026/2026-IIP-Mailer-BG.pdf)
- [CPUC Advice Letter 2574](https://files.cpuc.ca.gov/wateradviceletters/Water_Division/Advice_Letters/2025/Class_A/California_Water_Service_Company/AL_2574_-_Updates_to_Rule_15_Fees_and_Terms.pdf)
- [CPUC net energy metering](https://www.cpuc.ca.gov/industries-and-topics/electrical-energy/demand-side-management/net-energy-metering)
- [CDI](https://www.insurance.ca.gov/) and [CA FAIR Plan](https://www.cfpnet.com/)
- [CA Secretary of State – qualified ballot measures](https://www.sos.ca.gov/elections/ballot-measures/qualified-ballot-measures)
- [Legislative Analyst's Office](https://lao.ca.gov/BallotAnalysis)
- [FHFA House Price Index](https://www.fhfa.gov/data/house-price-index)
- [BLS regional CPI](https://www.bls.gov/regions/subjects/consumer-price-indexes.htm#CA), [CA DIR CPI](https://www.dir.ca.gov/oprl/CPI/PresentCCPIchange.PDF)

**Suggested manual check, in priority order:** the parcel-specific tax rate area and direct
charges from the two county assessors (FLAG-03, FLAG-04); live insurance quotes (FLAG-07);
the solar interconnection date and NEM tariff (FLAG-11).

---

## 4. Facts that could not be verified, and were therefore NOT written down

Per the rule "never infer or fill in values", these were left out of the model rather than
estimated:

| Missing | Why it was left blank |
|---|---|
| Rent for the third unit at 94122 | The $7,150/month covers two units. Rather than divide by two, the model is constructed so the figure cancels out of every option comparison. It is genuinely not needed. |
| Cost basis of either property | Not supplied. Not needed for the inheritance analysis (IRC § 1014 resets basis at death). It *would* be needed to price a lifetime sale, which is why that comparison is given as a marginal tax rate rather than a dollar figure. |
| Parcel-specific ad valorem rate and direct charges | Not published per parcel. Derived from the supplied bill history and disclosed as derived, with the derivation shown. |
| Insurance premium | No official filing publishes a ZIP-level average. Flagged, not filled in. |
| Market rent for a single-family home in 95014 | Aggregator medians are apartment-weighted and not applicable to a $3.1M house. Used as a flagged assumption only. |
| Certificate-of-occupancy date for 94122 | Determines which rent cap applies — a fivefold difference. Flagged (FLAG-12). |
| Whether 95014 is the transferor's principal residence | The single most consequential fact in the analysis. Flagged as critical (FLAG-05). |

---

## 5. Irregularities found in the supplied data

Recorded on the site's Flagged page and in `data/model.json`. Summary:

- **FLAG-01** — 2026 property tax blank for 95014.
- **FLAG-02** — 94122 has no 2026 row, and 2021 shows −5.9% while assessment rose 1%.
- **FLAG-03** — 95014's naive tax/assessment ratio (1.335%) exceeds the county's published
  "typical" rate (1.1488%). Explained by flat parcel charges; the model separates them.
- **FLAG-04** — 94122's naive ratio (2.135%) is ~1.8× the official secured rate (1.1816%).
  Same explanation, and a much larger effect because the assessed value is so low.
- **FLAG-05** — occupancy status of 95014 is unknown and decides everything.
- **FLAG-06** — the heir can claim the Prop 19 exclusion for only one property.
- **FLAG-07** — insurance unverifiable from an official source.
- **FLAG-08** — market rent for 95014 is an assumption.
- **FLAG-09** — the Prop 19 cap is officially known only to 15 Feb 2027.
- **FLAG-10** — water provider for 95014 depends on the exact address.
- **FLAG-11** — solar export value depends on which NEM tariff applies.
- **FLAG-12** — rent-control status of the 94122 units is not established.
- **FLAG-13** — estate size unknown, so whether federal estate tax applies cannot be determined.
- **FLAG-14** — Prop 43 (Nov 2026) does not change Prop 13's rate or the 2% cap.
- **FLAG-15** — whether a 3-unit building counts as a "family home" is unsettled.
- **FLAG-16** — land-value percentages used for depreciation are assumptions.
