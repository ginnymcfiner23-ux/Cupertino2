#!/usr/bin/env python3
"""
Cupertino2 - analytical model.

Reads the raw parcel history supplied for the two properties, fits the property-tax
behaviour of each parcel, projects values forward, models the Proposition 19
reassessment that a 2040-2050 trust transfer will trigger, and compares the three
disposition strategies (live in / rent out / sell and reinvest).

EVERY number written into data/model.json carries one of these provenance tags:

  official    - taken from a primary government source (IRS, BOE, county assessor,
                CPUC, SFPUC, SF.gov, CA AG, US Code, leginfo).  Source link included.
  derived     - computed from supplied parcel data or from `official` values.
                The formula is printed next to the number.
  supplied    - supplied as-is by the requester; no official source exists.
  unofficial  - from a commercial / secondary source (rate-shopping sites,
                listing aggregators).  Flagged for review.
  assumption  - a planning assumption the requester must confirm or change.
                Never presented as fact.

Privacy: this file contains no personal data.  Properties are referenced only by
ZIP code.  People are referenced only as placeholders ([OWNER-1], [HEIR-A], [TRUST]).
"""
from __future__ import annotations

import json
import os
import statistics

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")

# ---------------------------------------------------------------------------
# 1. SOURCE REGISTER
# ---------------------------------------------------------------------------

SOURCES = {
    "S-BOE-PROP19": {
        "name": "California State Board of Equalization - Proposition 19",
        "url": "https://www.boe.ca.gov/prop19/",
        "type": "official",
        "publisher": "CA State Board of Equalization",
    },
    "S-BOE-LTA25009": {
        "name": "BOE Letter to Assessors No. 2025/009 - Intergenerational Transfer Exclusion, Adjustment of the $1 Million Amount ($1,044,586)",
        "url": "https://www.boe.ca.gov/proptaxes/pdf/lta25009.pdf",
        "type": "official",
        "publisher": "CA State Board of Equalization",
    },
    "S-BOE-LTA2026002": {
        "name": "BOE Letter to Assessors No. 2026/002 - 2026-27 California Consumer Price Index (inflation factor 1.02)",
        "url": "https://www.boe.ca.gov/proptaxes/pdf/lta26002.pdf",
        "type": "official",
        "publisher": "CA State Board of Equalization",
    },
    "S-BOE-LTA2026026": {
        "name": "BOE Letter to Assessors No. 2026/026 - Proposition 19 Intergenerational Transfer Exclusion: Frequently Asked Questions and Answers",
        "url": "https://www.boe.ca.gov/proptaxes/pdf/lta26026.pdf",
        "type": "official",
        "publisher": "CA State Board of Equalization",
    },
    "S-BOE-LTA2026012": {
        "name": "BOE Letter to Assessors No. 2026/012 - Filing Period Extension for Parent/Child and Grandparent/Grandchild Exclusion Claims in Specified Los Angeles and Ventura County Disaster Areas",
        "url": "https://www.boe.ca.gov/proptaxes/pdf/lta26012.pdf",
        "type": "official",
        "publisher": "CA State Board of Equalization",
    },
    "S-SCC-PROP19": {
        "name": "Santa Clara County Assessor - Proposition 19 Overview",
        "url": "https://asr.santaclaracounty.gov/proposition-19-overview",
        "type": "official",
        "publisher": "County of Santa Clara, Office of the Assessor",
    },
    "S-CA-RTC-632": {
        "name": "California Revenue and Taxation Code section 63.2 (parent-child / grandparent-grandchild reassessment exclusion)",
        "url": "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=63.2.&lawCode=RTC",
        "type": "official",
        "publisher": "California Legislative Information",
    },
    "S-CA-RTC-62": {
        "name": "California Revenue and Taxation Code section 62(d) (transfer to revocable trust is not a change in ownership)",
        "url": "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=62.&lawCode=RTC",
        "type": "official",
        "publisher": "California Legislative Information",
    },
    "S-CA-RTC-51": {
        "name": "California Revenue and Taxation Code section 51 (2% annual inflation cap on base year value)",
        "url": "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=51.&lawCode=RTC",
        "type": "official",
        "publisher": "California Legislative Information",
    },
    "S-CA-CONST-13A": {
        "name": "California Constitution Article XIII A (Proposition 13) - 1% rate cap, 2% assessment growth cap, base year value",
        "url": "https://leginfo.legislature.ca.gov/faces/codes_displayexpandedbranch.xhtml?tocCode=CONS&division=&title=&part=&chapter=&article=XIII%20A",
        "type": "official",
        "publisher": "California Legislative Information",
    },
    "S-SCC-ASSESSOR-BOOKLET": {
        "name": "Santa Clara County Assessor - Assessment Information for the Santa Clara County Property Owner (Prop. 13; typical Tax Rate Area = 1.1488%)",
        "url": "https://files.santaclaracounty.gov/exjcpb1521/2024-10/2024_assessment_information_booklet.pdf",
        "type": "official",
        "publisher": "County of Santa Clara, Office of the Assessor",
    },
    "S-SCC-PROP13": {
        "name": "Santa Clara County Assessor - Understanding Proposition 13",
        "url": "https://asr.santaclaracounty.gov/faq/understanding-proposition-13",
        "type": "official",
        "publisher": "County of Santa Clara, Office of the Assessor",
    },
    "S-SCC-ASSESSOR": {
        "name": "Santa Clara County Office of the Assessor",
        "url": "https://asr.santaclaracounty.gov/",
        "type": "official",
        "publisher": "County of Santa Clara",
    },
    "S-SF-TAXRATE": {
        "name": "SF Treasurer & Tax Collector - Secured Property Taxes (secured property tax rate for Fiscal Year 2026-27 is 1.18162182%)",
        "url": "https://sftreasurer.org/property/secured-property-taxes",
        "type": "official",
        "publisher": "City and County of San Francisco",
    },
    "S-SF-ASSESSOR": {
        "name": "San Francisco Office of the Assessor-Recorder",
        "url": "https://www.sf.gov/departments--assessor-recorder",
        "type": "official",
        "publisher": "City and County of San Francisco",
    },
    "S-SF-RENTINCREASE": {
        "name": "SF.gov - Learn about rent increases in San Francisco (1.6% allowed, March 1 2026 - February 28 2027)",
        "url": "https://www.sf.gov/learn-about-rent-increases-san-francisco",
        "type": "official",
        "publisher": "City and County of San Francisco",
    },
    "S-SF-HEIRS": {
        "name": "SF Treasurer & Tax Collector - Information for Heirs",
        "url": "https://sftreasurer.org/property/information-heirs",
        "type": "official",
        "publisher": "City and County of San Francisco",
    },
    "S-SF-RENTBOARD": {
        "name": "San Francisco Rent Board",
        "url": "https://www.sf.gov/departments--rent-board/",
        "type": "official",
        "publisher": "City and County of San Francisco",
    },
    "S-CA-AG-RENTCAPS": {
        "name": "California Attorney General - Limits on Rent Increases (AB 1482 statewide caps by region)",
        "url": "https://oag.ca.gov/rentcaps",
        "type": "official",
        "publisher": "California Attorney General",
    },
    "S-CA-CIV-1947-12": {
        "name": "California Civil Code section 1947.12 (statewide rent cap: 5% + CPI, max 10%)",
        "url": "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=1947.12.&lawCode=CIV",
        "type": "official",
        "publisher": "California Legislative Information",
    },
    "S-IRS-2026-INFLATION": {
        "name": "IRS IR-2025-103 - Tax inflation adjustments for tax year 2026 (standard deduction, brackets, $15,000,000 estate basic exclusion, $19,000 gift annual exclusion)",
        "url": "https://www.irs.gov/newsroom/irs-releases-tax-inflation-adjustments-for-tax-year-2026-including-amendments-from-the-one-big-beautiful-bill",
        "type": "official",
        "publisher": "Internal Revenue Service",
    },
    "S-IRS-RP-2025-32": {
        "name": "IRS Revenue Procedure 2025-32 (2026 inflation-adjusted items; OBBBA section 70106 sets estate basic exclusion at $15,000,000 for 2026, indexed for 2027+)",
        "url": "https://www.irs.gov/pub/irs-drop/rp-25-32.pdf",
        "type": "official",
        "publisher": "Internal Revenue Service",
    },
    "S-IRS-ESTATETAX": {
        "name": "IRS - Estate tax (filing threshold by year of death; 2026 = $15,000,000; portability)",
        "url": "https://www.irs.gov/businesses/small-businesses-self-employed/estate-tax",
        "type": "official",
        "publisher": "Internal Revenue Service",
    },
    "S-IRS-NIIT": {
        "name": "IRS - Net Investment Income Tax (3.8%; thresholds $200,000 single / $250,000 MFJ; not inflation-indexed)",
        "url": "https://www.irs.gov/individuals/net-investment-income-tax",
        "type": "official",
        "publisher": "Internal Revenue Service",
    },
    "S-IRS-TOPIC409": {
        "name": "IRS Tax Topic 409 - Capital gains tax rates (0/15/20%; 25% unrecaptured section 1250 gain)",
        "url": "https://www.irs.gov/taxtopics/tc409",
        "type": "official",
        "publisher": "Internal Revenue Service",
    },
    "S-USC-1014": {
        "name": "26 U.S.C. section 1014 - Basis of property acquired from a decedent (step-up in basis)",
        "url": "https://www.govinfo.gov/link/uscode/26/1014",
        "type": "official",
        "publisher": "U.S. Government Publishing Office (govinfo)",
    },
    "S-USC-1411": {
        "name": "26 U.S.C. section 1411 - Imposition of net investment income tax",
        "url": "https://www.govinfo.gov/link/uscode/26/1411",
        "type": "official",
        "publisher": "U.S. Government Publishing Office (govinfo)",
    },
    "S-USC-121": {
        "name": "26 U.S.C. section 121 - Exclusion of gain from sale of principal residence ($250,000 / $500,000)",
        "url": "https://www.govinfo.gov/link/uscode/26/121",
        "type": "official",
        "publisher": "U.S. Government Publishing Office (govinfo)",
    },
    "S-USC-1031": {
        "name": "26 U.S.C. section 1031 - Exchange of property held for productive use or investment",
        "url": "https://www.govinfo.gov/link/uscode/26/1031",
        "type": "official",
        "publisher": "U.S. Government Publishing Office (govinfo)",
    },
    "S-CA-RTC-17043": {
        "name": "California Revenue and Taxation Code section 17043 - Additional 1% tax on taxable income over $1,000,000 (Behavioral Health Services Tax)",
        "url": "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=17043.&lawCode=RTC",
        "type": "official",
        "publisher": "California Legislative Information",
    },
    "S-FTB-FORMS": {
        "name": "California Franchise Tax Board - Forms & publications (current-year tax rate schedules)",
        "url": "https://www.ftb.ca.gov/forms/search.aspx",
        "type": "official",
        "publisher": "California Franchise Tax Board",
    },
    "S-CDI": {
        "name": "California Department of Insurance",
        "url": "https://www.insurance.ca.gov/",
        "type": "official",
        "publisher": "State of California",
    },
    "S-CDI-FAIRPLAN": {
        "name": "California FAIR Plan (insurer of last resort)",
        "url": "https://www.cfpnet.com/",
        "type": "official",
        "publisher": "California FAIR Plan Association",
    },
    "S-CUPERTINO-WATER": {
        "name": "City of Cupertino - Water (three separate water systems serve the city: California Water Service, San Jose Water Company, and the City system operated by San Jose Water Company)",
        "url": "https://www.cupertino.gov/Residents/Utilities/Water",
        "type": "official",
        "publisher": "City of Cupertino",
    },
    "S-CALWATER-IIP-2026": {
        "name": "California Water Service - 2026 Infrastructure Improvement Plan notice, Bear Gulch District (CPUC-approved rate adjustments effective July 1, 2026)",
        "url": "https://es.calwater.com/docs/iip/2026/2026-IIP-Mailer-BG.pdf",
        "type": "official",
        "publisher": "California Water Service (CPUC-regulated utility)",
    },
    "S-CPUC-CALW-AL2574": {
        "name": "CPUC Division of Water and Audits - California Water Service Company Advice Letter 2574 (Bear Gulch fees and terms)",
        "url": "https://files.cpuc.ca.gov/wateradviceletters/Water_Division/Advice_Letters/2025/Class_A/California_Water_Service_Company/AL_2574_-_Updates_to_Rule_15_Fees_and_Terms.pdf",
        "type": "official",
        "publisher": "California Public Utilities Commission",
    },
    "S-SFPUC-RATES-2026": {
        "name": "SFPUC Proposition 218 notice - proposed water & sewer rates effective July 1, 2026 (monthly service charge by meter size; stormwater component)",
        "url": "https://www.sfpuc.gov/accounts-services/water-power-sewer-rates/proposed-water-sewer-rates-2026/proposition-218-notice",
        "type": "official",
        "publisher": "San Francisco Public Utilities Commission",
    },
    "S-PGE": {
        "name": "PG&E - electric rates and net energy metering tariffs",
        "url": "https://www.pge.com/",
        "type": "official",
        "publisher": "Pacific Gas and Electric Company",
    },
    "S-CPUC-NEM": {
        "name": "CPUC - Net Energy Metering / Net Billing Tariff (NEM 2.0 vs NEM 3.0) proceedings",
        "url": "https://www.cpuc.ca.gov/industries-and-topics/electrical-energy/demand-side-management/net-energy-metering",
        "type": "official",
        "publisher": "California Public Utilities Commission",
    },
    "S-CA-SOS-BALLOT": {
        "name": "California Secretary of State - Ballot Measures (qualified statewide measures)",
        "url": "https://www.sos.ca.gov/elections/ballot-measures",
        "type": "official",
        "publisher": "California Secretary of State",
    },
    "S-CA-SOS-QUALIFIED": {
        "name": "California Secretary of State - Qualified Statewide Ballot Measures",
        "url": "https://www.sos.ca.gov/elections/ballot-measures/qualified-ballot-measures",
        "type": "official",
        "publisher": "California Secretary of State",
    },
    "S-CA-LAO": {
        "name": "California Legislative Analyst's Office - ballot measure analyses",
        "url": "https://lao.ca.gov/BallotAnalysis",
        "type": "official",
        "publisher": "California Legislative Analyst's Office",
    },
    "S-FHFA-HPI": {
        "name": "Federal Housing Finance Agency - House Price Index (the index BOE uses to biennially adjust the Prop. 19 $1 million amount)",
        "url": "https://www.fhfa.gov/data/house-price-index",
        "type": "official",
        "publisher": "Federal Housing Finance Agency",
    },
    "S-BLS-CPI": {
        "name": "U.S. Bureau of Labor Statistics - Consumer Price Index (source of the CPI figures used in AB 1482 and SF rent formulas)",
        "url": "https://www.bls.gov/regions/subjects/consumer-price-indexes.htm#CA",
        "type": "official",
        "publisher": "U.S. Bureau of Labor Statistics",
    },
    "S-DIR-CPI": {
        "name": "California Department of Industrial Relations - California Consumer Price Index",
        "url": "https://www.dir.ca.gov/oprl/CPI/PresentCCPIchange.PDF",
        "type": "official",
        "publisher": "CA Department of Industrial Relations",
    },
    # --- unofficial / secondary sources (flagged) ---
    "U-INS-QUOTES-95014": {
        "name": "Zip-code home-insurance rate shopping data for 95014 (commercial aggregator; NOT an official filing)",
        "url": "https://www.gethomeinsurancequotes.com/california/95014-home-insurance-rates.php",
        "type": "unofficial",
        "publisher": "commercial rate-shopping site",
    },
    "U-INS-QUOTES-CA": {
        "name": "California home-insurance premium survey by ZIP, 1,121 ZIP codes (commercial aggregator using Quadrant rate data; NOT an official filing)",
        "url": "https://www.insurancequotes.com/home/rates-by-state/california",
        "type": "unofficial",
        "publisher": "commercial rate-shopping site",
    },
    "U-ZILLOW-CUPERTINO-RENT": {
        "name": "Zillow rental market trends - Cupertino, CA (median rent, all bedroom counts and property types)",
        "url": "https://www.zillow.com/rental-manager/market-trends/cupertino-ca/",
        "type": "unofficial",
        "publisher": "Zillow (listing aggregator)",
    },
    "U-ZUMPER-CUPERTINO-RENT": {
        "name": "Zumper - average rent in Cupertino, CA",
        "url": "https://www.zumper.com/rent-research/cupertino-ca",
        "type": "unofficial",
        "publisher": "Zumper (listing aggregator)",
    },
    "U-PGE-NEM3": {
        "name": "PG&E average residential rate and NEM 3.0 average export credit reporting (industry blog; not a tariff)",
        "url": "https://nrgcleanpower.com/learning-center/nem-3-0-is-final/",
        "type": "unofficial",
        "publisher": "industry blog",
    },
    "U-PROP43": {
        "name": "Background on California Proposition 43 (November 3, 2026) and the withdrawn 'Save Prop 13' initiative",
        "url": "https://propertytaxduedates.com/blog/california-save-prop-13-ballot-measure-2026",
        "type": "unofficial",
        "publisher": "industry blog",
    },
    "U-ESTATE-2026-MIDTERM": {
        "name": "Summary of 2026 federal proposals affecting the estate tax and step-up in basis (proposals, not law)",
        "url": "https://smartasset.com/estate-planning/midterm-election-what-it-could-mean-for-your-estate-plan-and-inheritance",
        "type": "unofficial",
        "publisher": "personal-finance publisher",
    },
}

# ---------------------------------------------------------------------------
# 2. SUPPLIED RAW DATA  (no personal information)
# ---------------------------------------------------------------------------

# Cupertino 95014 - supplied property tax / assessment history.
# 2026 tax is blank in the supplied data ("--"); the 2026 assessment is given.
TAX_HISTORY_95014 = [
    # (year, tax or None, assessment or None, assessment_change_pct_supplied or None)
    (2026, None, 550_537, 2.0),
    (2025, 7_207, 539_743, 2.0),
    (2024, 7_003, 529_161, 2.0),
    (2023, 6_917, 518_786, 2.0),
    (2022, 6_755, 508_614, 2.0),
    (2021, 6_662, 498_642, 1.0),
    (2020, 6_565, 493_530, 2.0),
    (2019, 6_565, 483_854, 2.0),
    (2018, 6_383, 474_368, 2.0),
    (2017, 6_383, 465_067, 2.0),
    (2016, 6_414, 455_949, 1.5),
    (2015, 6_130, 449_101, 2.0),
    (2014, 5_965, 440_305, 0.5),
]

# San Francisco 94122 - supplied history. 2026 row is missing entirely and is
# derived below (flagged).
TAX_HISTORY_94122 = [
    (2026, None, None, None),
    (2025, 2_439, 114_248, 2.0),
    (2024, 2_315, 112_008, 2.0),
    (2023, 2_179, 109_814, 2.0),
    (2022, 2_107, 107_662, 2.0),
    (2021, 2_066, 105_595, 1.0),
    (2020, 2_197, 104_513, 2.0),
    (2019, 2_134, 102_465, 2.0),
    (2018, 2_061, 100_456, 2.0),
    (2017, 1_740, 98_488, 2.0),
    (2016, 1_675, 96_557, 1.5),
]

MARKET_VALUE_2026 = {"95014": 3_100_000, "94122": 1_800_000}

# ---------------------------------------------------------------------------
# 3. PLANNING ASSUMPTIONS  (user-adjustable; never presented as fact)
# ---------------------------------------------------------------------------

A = {
    "valuation_date": "November 2026",
    "prop13_inflation_factor": 0.02,           # official for the 2026 roll
    "appreciation_base": 0.040,                # nominal, Cupertino / SF
    "appreciation_low": 0.025,
    "appreciation_high": 0.055,
    "p19_cap_growth": 0.030,                   # FHFA CA HPI, biennially applied
    "general_inflation": 0.025,
    "inheritance_years": [2040, 2045, 2050],
    "base_inheritance_year": 2045,
    "horizon": 2055,

    # ---- carrying costs, 2026 dollars -------------------------------------
    "insurance_95014_primary": 1_500,          # supplied estimate
    "insurance_94122_rental": 1_500,           # supplied estimate
    "water_95014_month": 125,                  # midpoint of supplied $100-$150
    "water_94122_month": 365,                  # midpoint of supplied $330-$400 (all 3 units)
    "electric_95014_month_net": -15,           # supplied: solar usually nets a $10-$20 credit
    "electric_94122_month": 50,                # midpoint of supplied $30-$70
    "nem_grandfathering_end_year": 2035,       # ASSUMPTION - see FLAG-11
    "electric_95014_post_nem_month": 60,       # ASSUMPTION - modest bill once NEM credit ends
    "maintenance_95014_pct": 0.005,            # % of the 2026 market value per year
    "maintenance_94122_pct": 0.010,            # older 3-unit building
    "insurance_inflation": 0.05,               # ASSUMPTION - see FLAG-07

    # ---- rental ------------------------------------------------------------
    "rent_94122_month_total": 7_150,           # supplied
    "rent_95014_month_market": 4_500,          # ASSUMPTION - see flags
    "vacancy_and_credit_loss": 0.05,           # ASSUMPTION
    "management_pct": 0.00,                    # self-managed

    # ---- sale & reinvest ----------------------------------------------------
    "selling_cost_pct": 0.055,                 # ASSUMPTION (commission + closing)
    "portfolio_nominal_return": 0.070,         # ASSUMPTION
    "portfolio_income_yield": 0.018,           # ASSUMPTION (taxable dividends)
    "marginal_rate_on_investment_income": 0.371,  # 20% fed LTCG + 3.8% NIIT + 13.3% CA
    "discount_rate": 0.045,                    # ASSUMPTION for NPV

    # ---- income tax on renting ---------------------------------------------
    "federal_ordinary_marginal": 0.32,         # ASSUMPTION
    "ca_marginal": 0.093,                      # ASSUMPTION
    "depreciation_years": 27.5,
    "land_pct_95014": 0.55,                    # ASSUMPTION - land is not depreciable
    "land_pct_94122": 0.35,                    # ASSUMPTION
}

# ---------------------------------------------------------------------------
# 4. OFFICIAL CONSTANTS (verified - see sources)
# ---------------------------------------------------------------------------

OFFICIAL = {
    "estate_basic_exclusion_2026": {"v": 15_000_000, "src": "S-IRS-RP-2025-32",
        "note": "IRC 2010(c)(3) as amended by OBBBA section 70106. Permanent; indexed for inflation for calendar year 2027 and later."},
    "estate_basic_exclusion_2025": {"v": 13_990_000, "src": "S-IRS-ESTATETAX", "note": "For comparison only."},
    "gst_exemption_2026": {"v": 15_000_000, "src": "S-IRS-RP-2025-32", "note": "IRC 2631(c) equals the basic exclusion amount."},
    "estate_top_rate": {"v": 0.40, "src": "S-IRS-ESTATETAX", "note": "Applied to the taxable estate above the exclusion."},
    "gift_annual_exclusion_2026": {"v": 19_000, "src": "S-IRS-2026-INFLATION", "note": "Per recipient, per donor. Unchanged from 2025."},
    "standard_deduction_2026_mfj": {"v": 32_200, "src": "S-IRS-2026-INFLATION", "note": ""},
    "standard_deduction_2026_single": {"v": 16_100, "src": "S-IRS-2026-INFLATION", "note": ""},
    "ca_estate_tax": {"v": 0, "src": "S-CA-RTC-17043",
        "note": "California has no inheritance tax (repealed 1982 by Proposition 6) and no operative estate tax (the pick-up tax in R&TC 13302 has collected nothing for deaths after 2004). No official FTB page states a CA estate tax because none exists. Verified against R&TC and the CA Constitution."},
    "ca_local_estate_tax": {"v": 0, "src": "S-CA-SOS-BALLOT",
        "note": "No California city or county imposes an estate or inheritance tax. No official source exists because no such tax exists."},
    "prop13_rate_cap": {"v": 0.01, "src": "S-CA-CONST-13A", "note": "Maximum ad valorem rate, plus voter-approved debt service."},
    "prop13_growth_cap": {"v": 0.02, "src": "S-CA-RTC-51", "note": "Lesser of 2% or the change in the California CPI."},
    "prop13_inflation_factor_2026": {"v": 1.02, "src": "S-BOE-LTA2026002", "note": "BOE Letter to Assessors No. 2026/002 for the 2026-27 roll."},
    "scc_typical_tra_rate": {"v": 0.011488, "src": "S-SCC-ASSESSOR-BOOKLET",
        "note": "Santa Clara County's own worked example: 1% base + county bonds 0.0388% + school bonds 0.100% + water bonds 0.010% = 1.1488%. A 'typical' Tax Rate Area; the actual parcel rate differs."},
    "sf_secured_rate_fy2026_27": {"v": 0.0118162182, "src": "S-SF-TAXRATE",
        "note": "SF secured property tax rate for Fiscal Year 2026-27, per the Treasurer & Tax Collector. The prior year (FY 2025-26) was 1.18268325%. The rate is recommended by the Controller, adopted by the Board of Supervisors and approved by the Mayor, so it moves slightly each year. Direct charges and special assessments are added separately."},
    "p19_cap_2025_2027": {"v": 1_044_586, "src": "S-BOE-LTA25009",
        "note": "Applies to transfers occurring February 16, 2025 through February 15, 2027. Adjusted every other February 16 by the FHFA House Price Index for California. Next adjustment February 16, 2027."},
    "p19_cap_2023_2025": {"v": 1_022_600, "src": "S-BOE-LTA25009", "note": "Prior two-year period."},
    "p19_cap_2021_2023": {"v": 1_000_000, "src": "S-BOE-LTA25009", "note": "Original statutory amount."},
    "p19_effective_date": {"v": "2021-02-16", "src": "S-BOE-PROP19", "note": "Proposition 19 (ACA 11, 2019-20) approved November 3, 2020; inherited-property provisions effective February 16, 2021."},
    "p19_homeowners_exemption_deadline_years": {"v": 1, "src": "S-CA-RTC-632", "note": "R&TC 63.2(a)(1)(A)-(B): occupy as principal residence within one year AND file for the homeowners' (or disabled veterans') exemption within one year."},
    "p19_claim_deadline_years": {"v": 3, "src": "S-CA-RTC-632", "note": "R&TC 63.2(f): file BOE-19-P within three years of transfer, or before transfer to a third party, whichever is earlier."},
    "niit_rate": {"v": 0.038, "src": "S-IRS-NIIT", "note": "Thresholds $200,000 single / $250,000 MFJ / $125,000 MFS. Not indexed for inflation."},
    "niit_threshold_single": {"v": 200_000, "src": "S-IRS-NIIT", "note": ""},
    "niit_threshold_mfj": {"v": 250_000, "src": "S-IRS-NIIT", "note": ""},
    "ltcg_top_rate": {"v": 0.20, "src": "S-IRS-TOPIC409", "note": "0% / 15% / 20% ladder."},
    "unrecaptured_1250_rate": {"v": 0.25, "src": "S-IRS-TOPIC409", "note": "Maximum rate on the depreciation slice of a real-property gain."},
    "section_121_single": {"v": 250_000, "src": "S-USC-121", "note": "2 of the 5 years before sale, owner-occupied."},
    "section_121_mfj": {"v": 500_000, "src": "S-USC-121", "note": ""},
    "step_up_in_basis": {"v": "IRC 1014", "src": "S-USC-1014", "note": "Basis of property acquired from a decedent = FMV at date of death (alt. valuation date, IRC 2032)."},
    "ab1482_cap_sf_2026_27": {"v": 0.088, "src": "S-CA-AG-RENTCAPS",
        "note": "Statewide Tenant Protection Act cap for the San Francisco Area (Alameda, Contra Costa, Marin, San Francisco, San Mateo) for increases starting 8/1/2026-7/31/2027. 5% + CPI, capped at 10%."},
    "ab1482_cap_sf_2025_26": {"v": 0.063, "src": "S-CA-AG-RENTCAPS", "note": "Prior period (8/1/2025-7/31/2026)."},
    "sf_allowable_increase_2026_27": {"v": 0.016, "src": "S-SF-RENTINCREASE",
        "note": "SF Rent Ordinance, 60% of Bay Area CPI. Effective March 1, 2026 through February 28, 2027. Applies only to covered units (generally certificate of occupancy on or before June 13, 1979)."},
    "sf_rent_control_cutoff": {"v": "1979-06-13", "src": "S-SF-RENTBOARD", "note": "Coverage threshold; single-family homes and condos are generally exempt for tenancies beginning on or after January 1, 1996 (Costa-Hawkins)."},
    "sf_water_monthly_charge_5_8in_fye2027": {"v": 19.65, "src": "S-SFPUC-RATES-2026",
        "note": "Proposed FYE 2027 monthly service charge, 5/8-inch meter. Proposed FYE 2028 is $21.02. Sewer and stormwater are billed separately."},
    "sf_stormwater_tier1_fye2027": {"v": 12.63, "src": "S-SFPUC-RATES-2026",
        "note": "Proposed monthly stormwater component, residential tier 1 (0-1,700 sq ft). Current FYE 2026 is $8.24; proposed FYE 2028 is $18.08."},
    "homeowners_exemption": {"v": 7_000, "src": "S-SCC-ASSESSOR-BOOKLET", "note": "Reduces assessed value. Worth roughly $70-$85/yr at typical rates."},
}

# ---------------------------------------------------------------------------
# 5. HELPERS
# ---------------------------------------------------------------------------


def money(x):
    if x is None:
        return "n/a"
    return "${:,.0f}".format(x)


def pct(x, dp=3):
    if x is None:
        return "n/a"
    return "{:.{dp}f}%".format(x * 100, dp=dp)


def fit_line(xs, ys):
    """Ordinary least squares fit y = r*x + f. Returns (r, f, r2)."""
    n = len(xs)
    mx = sum(xs) / n
    my = sum(ys) / n
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    sxx = sum((x - mx) ** 2 for x in xs)
    r = sxy / sxx if sxx else float("nan")
    f = my - r * mx
    ss_tot = sum((y - my) ** 2 for y in ys)
    ss_res = sum((y - (r * x + f)) ** 2 for x, y in zip(xs, ys))
    r2 = (1 - ss_res / ss_tot) if ss_tot else float("nan")
    return r, f, r2


def build_history(rows, zipcode):
    """Fill derived gaps and compute the year-over-year figures."""
    out = []
    by_year = {r[0]: r for r in rows}
    years = sorted(by_year, reverse=True)
    for y in years:
        _, tax, av, av_chg = by_year[y]
        derived = []
        if av is None:
            # derive from the prior year using the official Prop 13 factor
            prior = by_year.get(y - 1)
            if prior and prior[2]:
                av = round(prior[2] * (1 + A["prop13_inflation_factor"]))
                derived.append(
                    "Assessed value derived: prior year {} x 1.02 (BOE 2026-27 inflation factor).".format(
                        money(prior[2])
                    )
                )
        out.append(
            {
                "year": y,
                "tax": tax,
                "assessment": av,
                "assessment_change_supplied_pct": av_chg,
                "implied_effective_rate": (tax / av) if (tax and av) else None,
                "derived": derived,
                "source": "supplied",
            }
        )
    return out


# ---------------------------------------------------------------------------
# 6. PROPERTY TAX TABLES
# ---------------------------------------------------------------------------

hist_95014 = build_history(TAX_HISTORY_95014, "95014")
hist_94122 = build_history(TAX_HISTORY_94122, "94122")

# Bill model:  tax = ad_valorem_rate * (assessed_value - homeowners_exemption) + flat_charges
#
# The ad valorem rate is the OLS slope of the supplied (assessment, tax) pairs where
# that fit is well conditioned, and the official published county rate where it is not.
# The flat component is the residual - i.e. non-ad-valorem parcel charges, which are
# the same in dollars no matter how low the Prop 13 assessed value is.
#
# OLS slope is invariant to shifting X, so fitting against (assessment - 7,000) gives
# the same slope and simply moves the constant.

HOE = OFFICIAL["homeowners_exemption"]["v"]


def fit_parcel(hist, official_rate, official_src, zipcode, use_official_rate):
    xs = [r["assessment"] - HOE for r in hist if r["tax"] and r["assessment"]]
    ys = [r["tax"] for r in hist if r["tax"] and r["assessment"]]
    slope, _intercept, r2 = fit_line(xs, ys)
    if use_official_rate:
        rate = official_rate
        rate_prov = "official"
        rate_note = ("Constrained to the officially published county secured rate. The "
                     "unconstrained OLS slope on the supplied data is degenerate "
                     "({:.4%}) because two years in the supplied series are anomalous, "
                     "so the official rate is used instead.").format(slope)
    else:
        rate = slope
        rate_prov = "derived"
        rate_note = ("OLS slope of the supplied (assessment, tax) pairs. The supplied "
                     "assessment figures are the factored base year value, so the "
                     "$7,000 homeowners' exemption is subtracted before applying the "
                     "rate.")
    # Flat charges: residual in the most recent supplied year, which is the most
    # defensible single estimate because parcel charges have been trending upward.
    latest = next(r for r in hist if r["tax"] and r["assessment"])
    flat_latest = latest["tax"] - rate * (latest["assessment"] - HOE)
    residuals = [y - rate * x for x, y in zip(xs, ys)]
    # Roll the latest residual from its year to 2026 at general inflation.
    flat_2026 = flat_latest * ((1 + A["general_inflation"]) ** (2026 - latest["year"]))
    return {
        "rate": rate,
        "rate_provenance": rate_prov,
        "rate_note": rate_note,
        "ols_slope": slope,
        "r2": r2,
        "n": len(xs),
        "flat_2026": round(flat_2026),
        "flat_min": round(min(residuals)),
        "flat_max": round(max(residuals)),
        "flat_note": ("Residual = tax - rate x (assessment - $7,000). Interpreted as "
                      "non-ad-valorem parcel charges, special assessments and direct "
                      "charges. DERIVED, not published. Range across the supplied "
                      "years: ${:,.0f} to ${:,.0f}.".format(min(residuals), max(residuals))),
        "implied_latest_rate": latest["tax"] / latest["assessment"],
        "official_reference_rate": official_rate,
        "official_reference_src": official_src,
    }


PARCEL = {
    "95014": fit_parcel(hist_95014, OFFICIAL["scc_typical_tra_rate"]["v"],
                        "S-SCC-ASSESSOR-BOOKLET", "95014", use_official_rate=False),
    "94122": fit_parcel(hist_94122, OFFICIAL["sf_secured_rate_fy2026_27"]["v"],
                        "S-SF-TAXRATE", "94122", use_official_rate=True),
}


def annual_tax(zipcode, assessed_value, year, apply_hoe=True):
    """Project the annual bill: ad valorem on net assessed value plus flat charges
    grown at general inflation.  Both the rate and the flat component are documented
    in PARCEL - the flat component is a DERIVED residual, not a published figure."""
    p = PARCEL[zipcode]
    net = assessed_value - (HOE if apply_hoe else 0)
    flat = p["flat_2026"] * ((1 + A["general_inflation"]) ** (year - 2026))
    return p["rate"] * net + flat


# ---------------------------------------------------------------------------
# 7. PROJECTIONS
# ---------------------------------------------------------------------------

def project_property(zipcode, growth):
    """Year-by-year projection out to the horizon, assuming NO change in ownership."""
    rows = []
    start_year = 2026
    av = {"95014": 550_537, "94122": 116_533}[zipcode]
    mv = MARKET_VALUE_2026[zipcode]
    for y in range(start_year, A["horizon"] + 1):
        if y > start_year:
            av = av * (1 + A["prop13_inflation_factor"])
            mv = mv * (1 + growth)
        rows.append(
            {
                "year": y,
                "assessed_value": round(av),
                "market_value": round(mv),
                "tax": round(annual_tax(zipcode, av, y)),
                "assessed_over_market": round(av / mv, 4),
            }
        )
    return rows


PROJECTIONS = {
    "95014": {g: project_property("95014", g) for g in
              (A["appreciation_low"], A["appreciation_base"], A["appreciation_high"])},
    "94122": {g: project_property("94122", g) for g in
              (A["appreciation_low"], A["appreciation_base"], A["appreciation_high"])},
}


def p19_cap(year):
    """Prop 19 $1M amount, biennially adjusted by the FHFA CA HPI.
    Official through Feb 15 2027 ($1,044,586); beyond that it is an ASSUMPTION."""
    official_through = 2027
    base = OFFICIAL["p19_cap_2025_2027"]["v"]
    if year <= official_through:
        return base, "official"
    yrs = year - official_through
    return base * ((1 + A["p19_cap_growth"]) ** yrs), "assumption"


def prop19_scenario(zipcode, transfer_year, growth):
    """Model the reassessment on a parent/child (or qualifying grandparent/
    grandchild) transfer of the Cupertino house in `transfer_year`."""
    proj = PROJECTIONS[zipcode][growth]
    fbyv = next(r["assessed_value"] for r in proj if r["year"] == transfer_year)
    fmv = next(r["market_value"] for r in proj if r["year"] == transfer_year)
    cap, cap_prov = p19_cap(transfer_year)
    threshold = fbyv + cap

    if fmv <= threshold:
        av_excluded = fbyv
        formula = "FMV ({}) <= FBYV ({}) + cap ({}); full exclusion, assessed value carries over.".format(
            money(fmv), money(fbyv), money(cap))
    else:
        av_excluded = fmv - cap
        formula = "Assessed value = FMV ({}) - cap ({}) = {}. (Equivalently FBYV {} + excess {}.)".format(
            money(fmv), money(cap), money(av_excluded), money(fbyv), money(fmv - threshold))

    av_full = fmv  # no exclusion: full reassessment to market value
    return {
        "zipcode": zipcode,
        "transfer_year": transfer_year,
        "growth": growth,
        "factored_base_year_value": fbyv,
        "market_value_at_transfer": fmv,
        "p19_cap": round(cap),
        "p19_cap_provenance": cap_prov,
        "threshold_fbyv_plus_cap": round(threshold),
        "assessed_value_if_exclusion_qualifies": round(av_excluded),
        "assessed_value_if_no_exclusion": round(av_full),
        "annual_tax_if_exclusion_qualifies": round(annual_tax(zipcode, av_excluded, transfer_year)),
        "annual_tax_if_no_exclusion": round(annual_tax(zipcode, av_full, transfer_year)),
        "annual_saving_from_exclusion": round(
            annual_tax(zipcode, av_full, transfer_year) - annual_tax(zipcode, av_excluded, transfer_year)),
        "formula": formula,
    }


PROP19 = []
for ty in A["inheritance_years"]:
    for g in (A["appreciation_low"], A["appreciation_base"], A["appreciation_high"]):
        PROP19.append(prop19_scenario("95014", ty, g))

# ---------------------------------------------------------------------------
# 8. CARRYING COST PROJECTIONS (2026 dollars, inflated at general inflation)
# ---------------------------------------------------------------------------

def net_electricity(zipcode, year):
    """95014 has solar. Under NEM 1.0/2.0 the system earns roughly retail credit and
    is grandfathered for 20 years from interconnection; once that ends it moves to the
    net billing tariff and exports are worth only a few cents per kWh. The supplied
    $10-$20/month net credit implies grandfathered NEM. See FLAG-11."""
    if zipcode != "95014":
        return A["electric_94122_month"] * 12 * ((1 + A["general_inflation"]) ** (year - 2026))
    if year >= A["nem_grandfathering_end_year"]:
        # post-grandfathering: assume the credit disappears and a modest bill returns
        return (A["electric_95014_post_nem_month"] * 12
                * ((1 + A["general_inflation"]) ** (year - A["nem_grandfathering_end_year"])))
    return A["electric_95014_month_net"] * 12


def carrying_costs(zipcode, year, market_value, assessed_value, use="primary"):
    """Carrying costs for one year, in nominal dollars.

    Maintenance and water/electricity are indexed to GENERAL inflation from a 2026
    base, not to the property's market value - a roof costs the same whether the land
    under it doubled or not.  Property tax is indexed to the assessed value."""
    infl = (1 + A["general_inflation"]) ** (year - 2026)
    if zipcode == "95014":
        base_value = MARKET_VALUE_2026["95014"]
        ins = A["insurance_95014_primary"] * ((1 + A["insurance_inflation"]) ** (year - 2026))
        water = A["water_95014_month"] * 12 * infl
        elec = net_electricity("95014", year)
        maint = base_value * A["maintenance_95014_pct"] * infl
    else:
        base_value = MARKET_VALUE_2026["94122"]
        ins = A["insurance_94122_rental"] * ((1 + A["insurance_inflation"]) ** (year - 2026))
        water = A["water_94122_month"] * 12 * infl
        elec = net_electricity("94122", year)
        maint = base_value * A["maintenance_94122_pct"] * infl
    tax = annual_tax(zipcode, assessed_value, year)
    return {
        "property_tax": round(tax),
        "insurance": round(ins),
        "water": round(water),
        "electricity": round(elec),
        "maintenance": round(maint),
        "total": round(tax + ins + water + elec + maint),
    }


# ---------------------------------------------------------------------------
# 9. THE THREE DISPOSITION STRATEGIES
# ---------------------------------------------------------------------------

def strategies(year, growth):
    """Compare live-in / rent-out / sell-and-reinvest at the inheritance year.

    The household always occupies one unit of the 94122 property for free.  That
    housing benefit (call it H) is common to every option except 'live in', where
    they vacate the SF unit and occupy Cupertino instead.  Comparing each option
    against 'sell & reinvest' cancels H, so the comparison does not require an
    estimate of SF unit-3 rent.
    """
    p = next(r for r in PROJECTIONS["95014"][growth] if r["year"] == year)
    fmv = p["market_value"]
    s19 = prop19_scenario("95014", year, growth)

    av_live = s19["assessed_value_if_exclusion_qualifies"]
    av_rent = s19["assessed_value_if_no_exclusion"]

    carry_live = carrying_costs("95014", year, fmv, av_live, "primary")
    carry_rent = carrying_costs("95014", year, fmv, av_rent, "rental")

    # --- Option A: live in it -------------------------------------------------
    imputed_rent = A["rent_95014_month_market"] * 12 * ((1 + A["general_inflation"]) ** (year - 2026))
    a_net = imputed_rent - carry_live["total"]
    a_note = ("Housing value consumed (imputed rent) minus carrying costs. "
              "Property tax is on the Prop 19 partial-exclusion assessed value.")

    # --- Option B: rent it out ------------------------------------------------
    gross_rent = imputed_rent
    eff_rent = gross_rent * (1 - A["vacancy_and_credit_loss"]) * (1 - A["management_pct"])
    dep_building = fmv * (1 - A["land_pct_95014"])
    depreciation = dep_building / A["depreciation_years"]
    taxable_rent = eff_rent - (carry_rent["total"]) - depreciation
    cash_tax_on_rent = max(0.0, taxable_rent) * (A["federal_ordinary_marginal"] + A["ca_marginal"])
    b_cash = eff_rent - carry_rent["total"] - cash_tax_on_rent
    b_net = b_cash
    b_note = ("Market rent, less 5% vacancy/credit loss, less full-reassessment carrying costs, "
              "less income tax on the net (after 27.5-yr depreciation). No Prop 19 exclusion is "
              "available because the heir does not occupy it.")

    # --- Option C: sell and reinvest -----------------------------------------
    selling_costs = fmv * A["selling_cost_pct"]
    proceeds = fmv - selling_costs
    gain = 0.0  # stepped-up basis under IRC 1014 if sold at/near the date of death
    tax_on_sale = 0.0
    div = proceeds * A["portfolio_income_yield"]
    growth_part = proceeds * (A["portfolio_nominal_return"] - A["portfolio_income_yield"])
    tax_on_div = div * A["marginal_rate_on_investment_income"]
    c_net = proceeds * A["portfolio_nominal_return"] - tax_on_div
    c_note = ("Sale at the date-of-death fair market value costs no capital gains tax because "
              "IRC 1014 steps the basis up to that value. Net proceeds invested; only the "
              "dividend component is taxed annually - the appreciation compounds tax-deferred "
              "(and is itself stepped up at the heir's later death under IRC 1014).")

    base_net = c_net

    # --- break-even: what portfolio return makes 'sell' merely tie 'live in'? ------
    #   A = C  =>  imputed_rent - carry_A = proceeds * (r - yield * tax_rate)
    be_return = (a_net / proceeds) + A["portfolio_income_yield"] * A["marginal_rate_on_investment_income"]

    # --- break-even: what would the Cupertino house have to rent for? -------------
    #   A = C  =>  rent - carry_A = C_net
    be_rent_month = (c_net + carry_live["total"]) / 12

    # --- Prop 13 lock-in value created by holding after the transfer --------------
    # Holding under the exclusion means the assessed value grows at 2%/yr while the
    # market value grows at `growth`.  The gap is untaxed value.
    lockin_value_now = (fmv - av_live) * PARCEL["95014"]["rate"]
    proj_after = [r for r in PROJECTIONS["95014"][growth] if r["year"] > year]
    gap_series = []
    av = av_live
    for r in proj_after[:20]:
        av *= (1 + A["prop13_inflation_factor"])
        gap_series.append({
            "year": r["year"],
            "assessed_value": round(av),
            "market_value": r["market_value"],
            "untaxed_gap": round(r["market_value"] - av),
            "annual_tax_saving_vs_market": round((r["market_value"] - av) * PARCEL["95014"]["rate"]),
        })

    return {
        "year": year,
        "growth": growth,
        "market_value": fmv,
        "prop19": s19,
        "A_live_in": {
            "assessed_value": av_live,
            "gross_benefit": round(imputed_rent),
            "carrying_costs": carry_live,
            "net_annual_benefit": round(a_net),
            "vs_sell": round(a_net - base_net),
            "note": a_note,
        },
        "B_rent_out": {
            "assessed_value": av_rent,
            "gross_rent": round(gross_rent),
            "effective_rent": round(eff_rent),
            "carrying_costs": carry_rent,
            "depreciation": round(depreciation),
            "income_tax": round(cash_tax_on_rent),
            "net_annual_benefit": round(b_net),
            "vs_sell": round(b_net - base_net),
            "note": b_note,
        },
        "C_sell_and_reinvest": {
            "selling_costs": round(selling_costs),
            "net_proceeds": round(proceeds),
            "capital_gains_tax": round(tax_on_sale),
            "taxable_investment_income": round(div),
            "tax_on_investment_income": round(tax_on_div),
            "gross_return": round(proceeds * A["portfolio_nominal_return"]),
            "net_annual_benefit": round(c_net),
            "vs_sell": 0,
            "note": c_note,
        },
        "break_even": {
            "portfolio_nominal_return_where_sell_ties_live_in": round(be_return, 5),
            "market_rent_month_where_live_in_ties_sell": round(be_rent_month),
            "note": ("Break-even portfolio return solves: imputed rent - carrying costs = "
                     "net proceeds x (r - dividend yield x tax rate on investment income). "
                     "If the portfolio can beat this, 'sell and reinvest' wins."),
        },
        "prop13_lockin": {
            "untaxed_gap_at_transfer": round(fmv - av_live),
            "annual_tax_saving_at_transfer": round(lockin_value_now),
            "effective_property_tax_rate_on_market_value": round(annual_tax("95014", av_live, year) / fmv, 5),
            "series": gap_series,
        },
    }


STRATEGIES = [strategies(y, g) for y in A["inheritance_years"]
              for g in (A["appreciation_low"], A["appreciation_base"], A["appreciation_high"])]

# ---------------------------------------------------------------------------
# 10. 94122 RENTAL ECONOMICS
# ---------------------------------------------------------------------------

def rental_94122(year, growth):
    p = next(r for r in PROJECTIONS["94122"][growth] if r["year"] == year)
    av = p["assessed_value"]
    mv = p["market_value"]
    rent = A["rent_94122_month_total"] * 12 * ((1 + A["general_inflation"]) ** (year - 2026))
    carry = carrying_costs("94122", year, mv, av, "rental")
    dep = mv * (1 - A["land_pct_94122"]) / A["depreciation_years"]
    taxable = rent - carry["total"] - dep
    tax = max(0.0, taxable) * (A["federal_ordinary_marginal"] + A["ca_marginal"])
    noi = rent - carry["total"]
    return {
        "year": year,
        "growth": growth,
        "gross_rent": round(rent),
        "carrying_costs": carry,
        "net_operating_income": round(noi),
        "depreciation": round(dep),
        "income_tax": round(tax),
        "after_tax_cash_flow": round(noi - tax),
        "cap_rate_on_market_value": round(noi / mv, 5),
        "cap_rate_on_assessed_value": round(noi / av, 5),
        "assessed_value": av,
        "market_value": mv,
    }


RENTAL = [rental_94122(y, A["appreciation_base"]) for y in range(2026, 2056)]

# ---------------------------------------------------------------------------
# 11. ESTATE-TAX HEADROOM
# ---------------------------------------------------------------------------

def estate_headroom():
    rows = []
    for year in range(2026, 2057, 2):
        excl = OFFICIAL["estate_basic_exclusion_2026"]["v"]
        if year > 2026:
            excl = excl * ((1 + A["general_inflation"]) ** (year - 2026))
            prov = "assumption"
        else:
            prov = "official"
        rows.append({
            "year": year,
            "exclusion_per_person": round(excl),
            "exclusion_married_with_portability": round(excl * 2),
            "provenance": prov,
        })
    return rows


ESTATE = estate_headroom()

# ---------------------------------------------------------------------------
# 12. FLAGS / IRREGULARITIES
# ---------------------------------------------------------------------------

FLAGS = [
    {
        "id": "FLAG-01",
        "severity": "high",
        "title": "2026 property tax is blank for the Cupertino parcel",
        "detail": "The supplied 95014 table shows '--' for 2026 property taxes while giving a "
                  "2026 assessment of $550,537. The bill has most likely simply not been "
                  "published yet. The model projects 2026 tax from the parcel's fitted bill "
                  "formula rather than inventing a number.",
        "action": "Replace with the actual 2026-27 Santa Clara County bill when it arrives "
                  "(mailed before November 1).",
        "source": "S-SCC-ASSESSOR",
    },
    {
        "id": "FLAG-02",
        "severity": "medium",
        "title": "The 94122 table has no 2026 row and one anomalous year (2021: -5.9%)",
        "detail": "The 2026 assessment is derived as 2025 x 1.02 = $116,533. Separately, 2021 "
                  "property taxes fell 5.9% while the assessment rose 1%, and 2018 taxes rose "
                  "18.4% on a 2% assessment increase. Neither is consistent with a pure ad "
                  "valorem bill, which indicates one-time credits/refunds or new voter-approved "
                  "charges in those years.",
        "action": "Pull the actual SF bill detail (block/lot) and reconcile the direct-charge "
                  "lines before relying on the fitted flat component.",
        "source": "S-SF-ASSESSOR",
    },
    {
        "id": "FLAG-03",
        "severity": "high",
        "title": "Cupertino parcel's implied tax rate (~1.33%) exceeds the county's published 'typical' rate (1.1488%)",
        "detail": "Dividing the supplied 2025 tax ($7,207) by the supplied 2025 assessment "
                  "($539,743) gives 1.335%. Santa Clara County's own workbook example shows a "
                  "typical Tax Rate Area at 1.1488%. The gap is explained by parcel-specific "
                  "voter-approved bonds and by flat (non-ad-valorem) parcel charges, which "
                  "inflate any tax/assessment ratio.",
        "action": "Confirm the parcel's Tax Rate Area and its direct charges in the Santa Clara "
                  "County Property Tax Rate Book before using the fitted rate for decisions.",
        "source": "S-SCC-ASSESSOR-BOOKLET",
    },
    {
        "id": "FLAG-04",
        "severity": "high",
        "title": "San Francisco parcel's implied tax rate (~2.14%) is far above the official FY2025-26 secured rate (1.18268325%)",
        "detail": "The supplied 2025 figure ($2,439 on a $114,248 assessment) implies 2.135%, "
                  "roughly 1.8x the official secured rate. This is the classic signature of flat "
                  "per-parcel charges (school parcel tax, City College parcel tax, stormwater, "
                  "Rent Board fee and similar) on a parcel with a very low Prop 13 assessed "
                  "value. It does NOT mean the ad valorem rate is 2.14%.",
        "action": "Use the official 1.18268325% for anything driven by assessed value, and add "
                  "the flat charges separately. Obtain the actual bill to size the flat charges.",
        "source": "S-SF-TAXRATE",
    },
    {
        "id": "FLAG-05",
        "severity": "critical",
        "title": "Whether the Cupertino house is the transferor's principal residence is unknown and decides everything",
        "detail": "Proposition 19 (R&TC 63.2) restricts the parent-child reassessment exclusion "
                  "to the transferor's principal residence (or a family farm). If the Cupertino "
                  "house is a rental or second home at the date of transfer, NO exclusion is "
                  "available at any value, and the assessed value resets to full market value on "
                  "day one. This single fact moves the annual tax bill by tens of thousands of "
                  "dollars.",
        "action": "Confirm occupancy status of the 95014 property at the planned transfer date, "
                  "and whether the transfer is parent-to-child or grandparent-to-grandchild "
                  "(the latter requires the middle generation to be deceased).",
        "source": "S-CA-RTC-632",
    },
    {
        "id": "FLAG-06",
        "severity": "critical",
        "title": "The heir can claim the Prop 19 exclusion for only ONE property",
        "detail": "The exclusion requires the transferee to occupy the home as a principal "
                  "residence within one year and keep occupying it. The household currently "
                  "occupies a unit at 94122. Moving to 95014 to claim the exclusion makes the "
                  "SF unit available to rent, but it also means the exclusion is lost the moment "
                  "they stop occupying Cupertino - at which point the assessed value is set as "
                  "of the lien date following the move-out.",
        "action": "Treat the occupancy requirement as a binding, multi-decade constraint, not a "
                  "formality. Model the 'move out later' cliff explicitly.",
        "source": "S-CA-RTC-632",
    },
    {
        "id": "FLAG-07",
        "severity": "medium",
        "title": "Home insurance premiums cannot be verified from an official source",
        "detail": "Neither the California Department of Insurance nor the FAIR Plan publishes a "
                  "ZIP-level average premium for a specific dwelling. Available figures come from "
                  "commercial rate-shopping sites and disagree widely ($864-$1,189/yr for 95014 "
                  "in one survey versus a $1,571 statewide average reported elsewhere).",
        "action": "Obtain live quotes for the actual dwelling (replacement cost, roof, wildfire "
                  "score) before relying on the $1,500 assumption.",
        "source": "S-CDI",
    },
    {
        "id": "FLAG-08",
        "severity": "medium",
        "title": "Market rent for the Cupertino house is an assumption, not a verified figure",
        "detail": "Listing aggregators report a Cupertino median rent around $3,800-$4,128/month "
                  "across all bedroom counts and property types, which is apartment-weighted and "
                  "is not a rent for a single-family house valued at $3.1M. The model uses "
                  "$4,500/month as a placeholder.",
        "action": "Obtain a broker opinion of rent or comparable single-family rental data for "
                  "95014.",
        "source": "U-ZILLOW-CUPERTINO-RENT",
    },
    {
        "id": "FLAG-09",
        "severity": "medium",
        "title": "The Prop 19 exclusion cap is officially known only through February 15, 2027",
        "detail": "The $1,044,586 figure applies to transfers between February 16, 2025 and "
                  "February 15, 2027 (BOE Letter to Assessors 2025/009). For a 2040-2050 transfer "
                  "the cap will have been re-set roughly eight to twelve more times by the FHFA "
                  "California House Price Index. The model grows it at an ASSUMED 3%/yr.",
        "action": "Re-run the model with the actual cap in force at the time.",
        "source": "S-BOE-LTA25009",
    },
    {
        "id": "FLAG-10",
        "severity": "low",
        "title": "Water provider for 95014 depends on the exact address",
        "detail": "The City of Cupertino is served by three separate water systems: California "
                  "Water Service (Bear Gulch district) in the northeast, San Jose Water Company "
                  "in the southeast, and the City's own system in the west, which is operated by "
                  "San Jose Water Company under a lease running to 2036. Rates differ by system.",
        "action": "Identify the provider for the parcel and pull the current tariff.",
        "source": "S-CUPERTINO-WATER",
    },
    {
        "id": "FLAG-11",
        "severity": "medium",
        "title": "Solar export value depends on which NEM tariff the system is on",
        "detail": "Systems interconnected before April 15, 2023 sit on NEM 2.0 and are "
                  "grandfathered for 20 years from interconnection; exports are credited at "
                  "roughly retail. Systems interconnected later are on NEM 3.0 (net billing), "
                  "where exports earn only a few cents per kWh. The supplied $10-$20/month net "
                  "credit is consistent with NEM 2.0, but the interconnection date must be "
                  "confirmed - and NEM 2.0 grandfathering is lost if the system is materially "
                  "modified.",
        "action": "Confirm the interconnection date and tariff from the PG&E bill.",
        "source": "S-CPUC-NEM",
    },
    {
        "id": "FLAG-12",
        "severity": "medium",
        "title": "Rent-control status of the 94122 units is not established",
        "detail": "SF's 1.6% local cap applies to units with a certificate of occupancy on or "
                  "before June 13, 1979. Single-family homes and condos are exempt under "
                  "Costa-Hawkins for tenancies beginning on or after January 1, 1996. If the "
                  "units fall outside the local ordinance, the AB 1482 statewide cap (8.8% for "
                  "8/1/2026-7/31/2027) governs instead - a fivefold difference in permitted rent "
                  "growth.",
        "action": "Confirm the certificate-of-occupancy date and tenancy start dates for all "
                  "three units.",
        "source": "S-SF-RENTINCREASE",
    },
    {
        "id": "FLAG-13",
        "severity": "low",
        "title": "Estate size is unknown, so whether the federal estate tax applies cannot be determined",
        "detail": "The request states the inheritance includes 'a considerable amount of money' "
                  "that 'could be over' the exempt amount. The federal basic exclusion is "
                  "$15,000,000 per person for 2026 ($30,000,000 for a married couple with a "
                  "timely portability election), made permanent by OBBBA and indexed for "
                  "inflation from 2027. California and its local governments impose no estate or "
                  "inheritance tax at all. No estate tax is owed unless the gross estate plus "
                  "adjusted taxable gifts exceeds the exclusion for the year of death.",
        "action": "Size the gross estate (real property at date-of-death FMV plus all other "
                  "assets, plus adjusted taxable gifts) against the exclusion for the actual "
                  "year of death. Note that the $15M is per person, and that portability "
                  "requires a timely Form 706.",
        "source": "S-IRS-ESTATETAX",
    },
    {
        "id": "FLAG-14",
        "severity": "low",
        "title": "California Proposition 43 (Nov 3, 2026) does not change the Prop 13 rate or the 2% cap",
        "detail": "Prop 43 adds a two-thirds voter-approval requirement for local special taxes "
                  "proposed under the local initiative power, starting January 1, 2027, and bars "
                  "additional ad valorem property taxes imposed by initiative. It does not amend "
                  "Prop 13's 1% rate, the 2% assessment cap, or the Prop 19 transfer rules. The "
                  "broader 'Save Prop 13' initiative (which would have capped transfer taxes) was "
                  "withdrawn in June 2026.",
        "action": "No action needed for the 2040-2050 decision; monitor future sessions.",
        "source": "S-CA-SOS-BALLOT",
    },
    {
        "id": "FLAG-15",
        "severity": "low",
        "title": "Whether a 3-unit building counts as a 'family home' for Prop 19 is not settled here",
        "detail": "R&TC 63.2(a)(1) refers to real property that is the principal residence of "
                  "the transferor. Where the transferor occupies one unit of a three-unit "
                  "building and rents the others, the scope of the exclusion for the rented "
                  "portion is a facts-and-circumstances question that should be put to the "
                  "county assessor or counsel.",
        "action": "Get written guidance from the SF Assessor-Recorder (94122) and Santa Clara "
                  "County Assessor (95014) before finalising a transfer plan.",
        "source": "S-CA-RTC-632",
    },
    {
        "id": "FLAG-16",
        "severity": "medium",
        "title": "Land value percentages used for depreciation are assumptions",
        "detail": "Depreciation under IRC 168 applies to buildings only, not land. The model "
                  "assumes 55% land for 95014 and 35% for 94122. County assessor records show "
                  "land and improvement values separately and should be used instead.",
        "action": "Take the land/improvement split from the county assessment roll.",
        "source": "S-SCC-ASSESSOR",
    },
]

# ---------------------------------------------------------------------------
# 12b. SELL NOW vs HOLD UNTIL DEATH  (the current owner's decision)
# ---------------------------------------------------------------------------
# The analysis above is the HEIR's decision at the transfer.  There is a second and
# larger decision, which belongs to the CURRENT OWNER: sell during life, or hold until
# death so that IRC 1014 steps the basis up.
#
# This does not require knowing the cost basis.  The point is the MARGINAL tax rate
# that applies to gain on a lifetime sale versus a post-death sale:
#
#   lifetime sale : federal LTCG 20% + NIIT 3.8% + CA ordinary rate up to 13.3%
#                   = 37.1% on the gain  (less any section 121 exclusion)
#   post-death    : basis steps up to FMV under IRC 1014, so gain at a prompt sale
#                   is ~0 and the same three taxes are ~0.
#
# Every dollar of appreciation deferred to death is therefore worth up to 37.1 cents.

def sell_now_vs_hold():
    stack = [
        {"component": "Federal long-term capital gains", "rate": 0.20, "src": "S-IRS-TOPIC409",
         "note": "Top of the 0/15/20% ladder."},
        {"component": "Net Investment Income Tax", "rate": 0.038, "src": "S-IRS-NIIT",
         "note": "3.8% above $200,000 single / $250,000 MFJ. Not indexed."},
        {"component": "California (capital gain taxed as ordinary income)", "rate": 0.133,
         "src": "S-CA-RTC-17043",
         "note": "12.3% top bracket plus the 1% tax on taxable income over $1,000,000."},
    ]
    combined = sum(s["rate"] for s in stack)
    rows = []
    for gain in (500_000, 1_000_000, 1_500_000, 2_000_000, 2_500_000):
        rows.append({
            "gain_on_lifetime_sale": gain,
            "tax_if_sold_during_life": round(gain * combined),
            "tax_if_inherited_and_sold_promptly": 0,
            "advantage_of_holding_until_death": round(gain * combined),
        })
    return {"rate_stack": stack, "combined_rate": round(combined, 4), "illustrative_gains": rows,
            "note": ("Assumes the gain exceeds the section 121 exclusion ($250,000 single / "
                     "$500,000 MFJ) and that no suspended passive losses remain. Depreciation "
                     "recapture (up to 25% federal) would apply additionally to the portion of "
                     "the gain attributable to depreciation if the property was rented.")}


SELL_NOW_VS_HOLD = sell_now_vs_hold()

# ---------------------------------------------------------------------------
# 13. EMIT
# ---------------------------------------------------------------------------

out = {
    "meta": {
        "generated": "model build",
        "valuation_date": A["valuation_date"],
        "privacy": "No personal information. Properties referenced by ZIP code only; "
                   "people referenced only as placeholders ([OWNER-1], [HEIR-A], [TRUST]).",
        "provenance_tags": {
            "official": "Primary government source; link included.",
            "derived": "Computed from supplied data or official values; formula shown.",
            "supplied": "Given as-is by the requester; no official source exists.",
            "unofficial": "Commercial or secondary source. Flagged for review.",
            "assumption": "Planning assumption to confirm or change. Never presented as fact.",
        },
    },
    "sources": SOURCES,
    "official": OFFICIAL,
    "assumptions": A,
    "parcel_fit": PARCEL,
    "history": {"95014": hist_95014, "94122": hist_94122},
    "projections": {"95014": {str(k): v for k, v in PROJECTIONS["95014"].items()},
                    "94122": {str(k): v for k, v in PROJECTIONS["94122"].items()}},
    "prop19_scenarios": PROP19,
    "strategies": STRATEGIES,
    "rental_94122": RENTAL,
    "estate_headroom": ESTATE,
    "sell_now_vs_hold": SELL_NOW_VS_HOLD,
    "flags": FLAGS,
}

os.makedirs(DATA, exist_ok=True)
with open(os.path.join(DATA, "model.json"), "w") as fh:
    json.dump(out, fh, indent=1)

# ---------------------------------------------------------------------------
# 14. CONSOLE REPORT (so the numbers can be eyeballed)
# ---------------------------------------------------------------------------
print("=" * 78)
print("PARCEL BILL MODEL  (tax = rate x (assessment - $7,000 HOE) + flat charges)")
print("=" * 78)
for z in ("95014", "94122"):
    p = PARCEL[z]
    print("{}: rate {:>7.4%} [{}]  flat(2026) ${:>7,.0f}  R2 {:>6.3f}  n={}".format(
        z, p["rate"], p["rate_provenance"], p["flat_2026"], p["r2"], p["n"]))
    print("        flat residual range across supplied years: ${:,.0f} - ${:,.0f}".format(
        p["flat_min"], p["flat_max"]))
    print("        naive ratio tax/assessment in latest year: {:>7.4%}   official reference: {:>7.4%}".format(
        p["implied_latest_rate"], p["official_reference_rate"]))

print()
print("=" * 78)
print("PROP 19 REASSESSMENT AT TRANSFER  (Cupertino 95014)")
print("=" * 78)
for s in PROP19:
    if s["growth"] != A["appreciation_base"]:
        continue
    print("Transfer {}:  FBYV ${:>12,.0f}   FMV ${:>12,.0f}   cap ${:>11,.0f} ({})".format(
        s["transfer_year"], s["factored_base_year_value"], s["market_value_at_transfer"],
        s["p19_cap"], s["p19_cap_provenance"]))
    print("   assessed if exclusion qualifies : ${:>12,.0f}   tax ${:>10,.0f}/yr".format(
        s["assessed_value_if_exclusion_qualifies"], s["annual_tax_if_exclusion_qualifies"]))
    print("   assessed if NO exclusion        : ${:>12,.0f}   tax ${:>10,.0f}/yr".format(
        s["assessed_value_if_no_exclusion"], s["annual_tax_if_no_exclusion"]))
    print("   annual value of the exclusion   : ${:>12,.0f}/yr".format(s["annual_saving_from_exclusion"]))
    print("   {}".format(s["formula"]))
    print()

print("=" * 78)
print("STRATEGY COMPARISON - annual net benefit (nominal dollars, at the transfer year)")
print("=" * 78)
hdr = "{:>6} {:>6} | {:>13} {:>13} {:>13} | {:>12} {:>12} | {:>9}".format(
    "year", "growth", "A live in", "B rent out", "C sell&inv", "A - C", "B - C", "breakeven r")
print(hdr)
print("-" * len(hdr))
for s in STRATEGIES:
    print("{:>6} {:>6.1%} | {:>13,.0f} {:>13,.0f} {:>13,.0f} | {:>12,.0f} {:>12,.0f} | {:>8.2%}".format(
        s["year"], s["growth"],
        s["A_live_in"]["net_annual_benefit"],
        s["B_rent_out"]["net_annual_benefit"],
        s["C_sell_and_reinvest"]["net_annual_benefit"],
        s["A_live_in"]["vs_sell"],
        s["B_rent_out"]["vs_sell"],
        s["break_even"]["portfolio_nominal_return_where_sell_ties_live_in"],
    ))

print()
print("=" * 78)
print("BREAK-EVEN RENT (market rent the Cupertino house would need to match sell-and-reinvest)")
print("=" * 78)
for s in STRATEGIES:
    print("  {} at {:>4.1%} appreciation: ${:>12,.0f}/month   "
          "(eff. property tax rate on market value: {:.3%})".format(
              s["year"], s["growth"],
              s["break_even"]["market_rent_month_where_live_in_ties_sell"],
              s["prop13_lockin"]["effective_property_tax_rate_on_market_value"]))

print()
print("=" * 78)
print("SELL DURING LIFE vs HOLD UNTIL DEATH (current owner's decision)")
print("=" * 78)
print("  combined marginal rate on a lifetime sale: {:.1%}".format(SELL_NOW_VS_HOLD["combined_rate"]))
for r in SELL_NOW_VS_HOLD["illustrative_gains"]:
    print("  gain ${:>10,.0f} -> tax if sold during life ${:>10,.0f}; "
          "tax if inherited and sold promptly $0".format(
              r["gain_on_lifetime_sale"], r["tax_if_sold_during_life"]))

print()
print("=" * 78)
print("94122 RENTAL ECONOMICS (base growth)")
print("=" * 78)
for r in RENTAL:
    if r["year"] in (2026, 2030, 2035, 2040, 2045, 2050, 2055):
        print("{}: rent ${:>10,.0f}  costs ${:>9,.0f}  NOI ${:>10,.0f}  tax ${:>9,.0f}  "
              "after-tax ${:>10,.0f}  cap rate on MV {:>6.2%}".format(
                  r["year"], r["gross_rent"], r["carrying_costs"]["total"],
                  r["net_operating_income"], r["income_tax"], r["after_tax_cash_flow"],
                  r["cap_rate_on_market_value"]))

print()
print("Estate headroom 2026: ${:,.0f} per person / ${:,.0f} married with portability".format(
    ESTATE[0]["exclusion_per_person"], ESTATE[0]["exclusion_married_with_portability"]))
print("Estate headroom 2045: ${:,.0f} per person (ASSUMPTION: grows with inflation)".format(
    next(r for r in ESTATE if r["year"] == 2044)["exclusion_per_person"]))
print("Flags: {}".format(len(FLAGS)))
print("Wrote {}".format(os.path.join(DATA, "model.json")))
