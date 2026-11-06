#!/usr/bin/env python3
"""Deterministic projection model for the two-property inheritance decision.

Inputs are read from data/inputs.json (user-provided values, flagged) and
data/assumptions are declared below (labeled ASSUMPTION; never presented as facts).
Outputs:
  data/projections_base.csv   year-by-year, base case, inheritance year = BASE_INHERIT_YEAR
  data/sensitivity.csv        appreciation x return grid + inflation stress row
  data/decision.json          net-worth comparison per inheritance year, best plan, breakevens

Every official constant used below is listed with its source ID in data/facts.json.
"""
import csv
import json
import os

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
DATA = os.path.join(ROOT, "data")

START, END = 2026, 2060   # rows run to 2060 so each 10-year comparison horizon is covered
PROJ_END = 2050            # year-by-year tables published through 2050
HORIZON_YEARS = 10         # net-worth comparison horizon after inheritance
INHERIT_YEARS = [2040, 2045, 2050]
BASE_INHERIT_YEAR = 2045

# ---- user-provided inputs (UNVERIFIED unless noted) -------------------------
CUP_MV_2026 = 3_100_000          # user estimate, Nov 2026
SF_MV_2026 = 1_800_000           # user estimate, Nov 2026
CUP_AV_2026 = 550_537            # user table (2026 AV)
CUP_TAX_2025, CUP_AV_2025 = 7_207, 539_743
SF_TAX_2025, SF_AV_2025 = 2_439, 114_248
CUP_WATER_MO = 125.0             # midpoint of user range $100-150
CUP_SOLAR_CREDIT_MO = 15.0       # midpoint of user range $10-20
CUP_INS_YR = 1_500.0             # user guess
SF_WATER_MO = 365.0              # midpoint of user range $330-400 (3 units)
SF_ELEC_MO = 50.0                # midpoint of user range $30-70
SF_INS_YR = 1_500.0              # user guess
SF_RENT_MO = 7_150.0             # user figure, two rented units

# ---- official constants (see data/facts.json) -------------------------------
PROP19_CAP_2025 = 1_044_586      # BOE LTA 2025/009 (Feb 16 2025 - Feb 15 2027)
SF_RATE_2627 = 0.0118162182      # SF Treasurer, FY2026-27 secured rate
BSC_TIER3_PER_DAY = 0.79343      # PG&E AL 7825-E (per-day tier 3; see flags)
DAYS_PER_MONTH = 365 / 12
FED_EXCLUSION_2026 = 15_000_000  # IRS 2026
SJW_SERVICE_MO = 79.67           # AL 629-A (informational)
DTT_BASE_RATE = 1.10 / 1000      # R&T 11911 base ($0.55 per $500); county adoption unverified

# ---- ASSUMPTIONS (labeled; user should replace) -----------------------------
A = {
    "appreciation": 0.03,        # home value growth, nominal (base; sens 1%/5%)
    "inflation": 0.02,           # Fed 2% objective used as base
    "inflation_stress": 0.037,   # reported CPI reference, stress only (unverified)
    "portfolio_return": 0.06,    # nominal return on invested proceeds (sens 4%/8%)
    "prop13_growth": 0.02,       # Art. XIII A cap on factored base-year value growth
    "cup_maint_rate": 0.005,     # maintenance, % of market value / yr (placeholder)
    "sf_maint_rate": 0.010,      # maintenance, % of market value / yr (placeholder)
    "sale_commission": 0.05,     # placeholder selling commission
    "rent_growth": 0.016,        # SF covered-unit cap used as ongoing rent growth
    "insurance_growth": 0.03,
    "electric_growth": 0.03,
    "water_growth": 0.02,
    "estate_index": 0.02,        # estate exemption indexed after 2026 (assumption)
}


def run(appr=A["appreciation"], infl=A["inflation"], ret=A["portfolio_return"],
        inherit_year=BASE_INHERIT_YEAR):
    """Return dict of per-year series and the net-worth comparison."""
    a = dict(A, appreciation=appr, inflation=infl, portfolio_return=ret)
    cup_rate = CUP_TAX_2025 / CUP_AV_2025      # user-derived effective rate (UNVERIFIED)
    sf_rate_eff = SF_TAX_2025 / SF_AV_2025     # user-derived effective rate (UNVERIFIED)
    sf_fixed = SF_TAX_2025 - SF_RATE_2627 * SF_AV_2025  # implied non-ad-valorem charges (derived)
    cup_elec_cost_mo = BSC_TIER3_PER_DAY * DAYS_PER_MONTH - CUP_SOLAR_CREDIT_MO  # net cost, conservative

    years = list(range(START, END + 1))
    rows = []
    for t in years:
        n = t - START
        cup_mv = CUP_MV_2026 * (1 + a["appreciation"]) ** n
        cup_av = CUP_AV_2026 * (1 + a["prop13_growth"]) ** n
        sf_mv = SF_MV_2026 * (1 + a["appreciation"]) ** n
        sf_av = SF_AV_2025 * (1 + a["prop13_growth"]) ** (t - 2025)
        cup_tax_sq = cup_rate * cup_av
        sf_tax_sq = sf_rate_eff * sf_av
        cap_t = PROP19_CAP_2025 * (1 + a["inflation"]) ** max(0, t - 2027)
        rows.append({
            "year": t, "cup_mv": cup_mv, "cup_av": cup_av, "cup_tax_status_quo": cup_tax_sq,
            "cup_cap_prop19": cap_t,
            "sf_mv": sf_mv, "sf_av": sf_av, "sf_tax_status_quo": sf_tax_sq,
            "cup_water": CUP_WATER_MO * 12 * (1 + a["water_growth"]) ** n,
            "cup_electric_net_cost": cup_elec_cost_mo * 12 * (1 + a["electric_growth"]) ** n,
            "cup_insurance": CUP_INS_YR * (1 + a["insurance_growth"]) ** n,
            "cup_maintenance": a["cup_maint_rate"] * cup_mv,
            "sf_water": SF_WATER_MO * 12 * (1 + a["water_growth"]) ** n,
            "sf_electric": SF_ELEC_MO * 12 * (1 + a["electric_growth"]) ** n,
            "sf_insurance": SF_INS_YR * (1 + a["insurance_growth"]) ** n,
            "sf_maintenance": a["sf_maint_rate"] * sf_mv,
            "sf_rent_annual": SF_RENT_MO * 12 * (1 + a["rent_growth"]) ** n,
        })

    # --- Cupertino at inheritance year Y -----------------------------------
    Y = inherit_year
    rY = next(r for r in rows if r["year"] == Y)
    fbyv_Y = rY["cup_av"]
    # Prop 19 New Taxable Value = FBYV + excess (FCV - (FBYV + cap)) when FCV > cap; BOE LTA 2026/026
    ntv_Y_prop19 = fbyv_Y + max(0.0, rY["cup_mv"] - (fbyv_Y + rY["cup_cap_prop19"]))
    ntv_Y_full = rY["cup_mv"]  # full reassessment (no exclusion)
    H = Y + HORIZON_YEARS
    r = a["portfolio_return"]

    def cup_cf_live(ntv_Y):
        cfs = {}
        for row in rows:
            t = row["year"]
            if t < Y or t > H:
                continue
            ntv_t = ntv_Y * (1 + a["prop13_growth"]) ** (t - Y)
            tax = cup_rate * ntv_t
            cfs[t] = -(tax + row["cup_insurance"] + row["cup_water"]
                       + row["cup_electric_net_cost"] + row["cup_maintenance"])
        return cfs

    def fv_cf(cfs):
        return sum(cf * (1 + r) ** (H - t) for t, cf in cfs.items())

    def sf_fixed_t(t):
        return sf_fixed * (1 + a["inflation"]) ** (t - START)

    cupA_cf = cup_cf_live(ntv_Y_prop19)
    cupA_nw = rY["cup_mv"] * (1 + a["appreciation"]) ** (H - Y) + fv_cf(cupA_cf)
    cupA_alt_cf = cup_cf_live(ntv_Y_full)
    cupA_alt_nw = rY["cup_mv"] * (1 + a["appreciation"]) ** (H - Y) + fv_cf(cupA_alt_cf)
    proceeds_cup = rY["cup_mv"] * (1 - a["sale_commission"] - DTT_BASE_RATE)
    cupB_nw = proceeds_cup * (1 + r) ** (H - Y)

    # --- SF at inheritance year Y ------------------------------------------
    # Rental units are not eligible for the Prop 19 family-home exclusion (BOE); conservative full reassessment.
    sfC_cf = {}
    for row in rows:
        t = row["year"]
        if t < Y or t > H:
            continue
        ntv_t = rY["sf_mv"] * (1 + a["prop13_growth"]) ** (t - Y)
        tax = SF_RATE_2627 * ntv_t + sf_fixed_t(t)
        cfs_t = (row["sf_rent_annual"] - tax - row["sf_water"] - row["sf_electric"]
                 - row["sf_insurance"] - row["sf_maintenance"])
        sfC_cf[t] = cfs_t
    sfC_nw = rY["sf_mv"] * (1 + a["appreciation"]) ** (H - Y) + fv_cf(sfC_cf)
    proceeds_sf = rY["sf_mv"] * (1 - a["sale_commission"] - DTT_BASE_RATE)
    sfD_nw = proceeds_sf * (1 + r) ** (H - Y)

    # breakeven imputed rent for Cupertino live vs sell (annual, from Y, growing with inflation)
    S = sum((1 + a["inflation"]) ** (t - Y) * (1 + r) ** (H - t) for t in range(Y, H + 1))
    breakeven_rent_cup = max(0.0, (cupB_nw - cupA_nw) / S)

    # Post-inheritance taxable-value columns (blank before inheritance year)
    for row in rows:
        t = row["year"]
        row["cup_tax_post_inh_prop19"] = None
        row["cup_tax_post_inh_full"] = None
        row["sf_tax_post_inh_reassessed"] = None
        if Y <= t <= H:
            row["cup_tax_post_inh_prop19"] = cup_rate * ntv_Y_prop19 * (1 + a["prop13_growth"]) ** (t - Y)
            row["cup_tax_post_inh_full"] = cup_rate * ntv_Y_full * (1 + a["prop13_growth"]) ** (t - Y)
            row["sf_tax_post_inh_reassessed"] = SF_RATE_2627 * rY["sf_mv"] * (1 + a["prop13_growth"]) ** (t - Y) + sf_fixed_t(t)

    estate_ex = {t: FED_EXCLUSION_2026 * (1 + a["estate_index"]) ** (t - START) if t >= 2027 else FED_EXCLUSION_2026
                 for t in years}

    return {
        "rows": rows,
        "inherit_year": Y,
        "ntv_cup_prop19": ntv_Y_prop19,
        "ntv_cup_full": ntv_Y_full,
        "cup_live_nw": cupA_nw,
        "cup_live_no_prop19_nw": cupA_alt_nw,
        "cup_sell_nw": cupB_nw,
        "sf_keep_nw": sfC_nw,
        "sf_sell_nw": sfD_nw,
        "breakeven_imputed_rent_cup": breakeven_rent_cup,
        "estate_exclusion_by_year": estate_ex,
        "sf_fixed_charges_derived": sf_fixed,
        "cup_elec_net_cost_mo": cup_elec_cost_mo,
        "assumptions": a,
    }


def best_plan(res):
    cup_best = "Live in (Prop 19 applies)" if res["cup_live_nw"] >= res["cup_sell_nw"] else "Sell at inheritance"
    sf_best = "Keep as rental" if res["sf_keep_nw"] >= res["sf_sell_nw"] else "Sell at inheritance"
    cup_val = max(res["cup_live_nw"], res["cup_sell_nw"])
    sf_val = max(res["sf_keep_nw"], res["sf_sell_nw"])
    return {"cupertino": cup_best, "sf": sf_best, "combined_nw": cup_val + sf_val}


def write_outputs():
    base = run(inherit_year=BASE_INHERIT_YEAR)
    with open(os.path.join(DATA, "projections_base.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(base["rows"][0].keys()))
        w.writeheader()
        for row in base["rows"]:
            if row["year"] > PROJ_END:
                continue
            w.writerow({k: (round(v, 2) if isinstance(v, float) else ("" if v is None else v)) for k, v in row.items()})

    sens_rows = []
    for g in (0.01, 0.03, 0.05):
        for r_ in (0.04, 0.06, 0.08):
            res = run(appr=g, ret=r_)
            sens_rows.append(_sens_row(res, f"appreciation {g:.0%}, return {r_:.0%}"))
    stress = run(infl=A["inflation_stress"])
    sens_rows.append(_sens_row(stress, "inflation stress 3.7% (base appreciation & return)"))
    with open(os.path.join(DATA, "sensitivity.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(sens_rows[0].keys()))
        w.writeheader()
        w.writerows(sens_rows)

    decisions = {}
    for Y in INHERIT_YEARS:
        res = run(inherit_year=Y)
        decisions[str(Y)] = {
            "inherit_year": Y,
            "cup_mv_at_inheritance": next(r for r in res["rows"] if r["year"] == Y)["cup_mv"],
            "cup_ntv_prop19": res["ntv_cup_prop19"],
            "cup_ntv_full": res["ntv_cup_full"],
            "cup_live_nw_h": res["cup_live_nw"],
            "cup_live_no_prop19_nw_h": res["cup_live_no_prop19_nw"],
            "cup_sell_nw_h": res["cup_sell_nw"],
            "sf_keep_nw_h": res["sf_keep_nw"],
            "sf_sell_nw_h": res["sf_sell_nw"],
            "breakeven_imputed_rent_cup_yr_at_inheritance": res["breakeven_imputed_rent_cup"],
            "estate_exclusion_in_year": res["estate_exclusion_by_year"][Y],
            "best": best_plan(res),
        }
    out = {
        "assumptions": A,
        "constants_note": "Official constants are cited in data/facts.json; user inputs in scripts/model.py header.",
        "estate_exclusion_by_year": run()["estate_exclusion_by_year"],
        "sf_fixed_charges_derived": base["sf_fixed_charges_derived"],
        "cup_elec_net_cost_mo": base["cup_elec_net_cost_mo"],
        "decisions": decisions,
    }
    with open(os.path.join(DATA, "decision.json"), "w") as f:
        json.dump(out, f, indent=2)
    return out


def _sens_row(res, label):  # horizon = inheritance year + HORIZON_YEARS
    Y = res["inherit_year"]
    return {
        "scenario": label,
        "inherit_year": Y,
        "cup_live_nw_h": round(res["cup_live_nw"]),
        "cup_sell_nw_h": round(res["cup_sell_nw"]),
        "cup_sell_minus_live": round(res["cup_sell_nw"] - res["cup_live_nw"]),
        "sf_keep_nw_h": round(res["sf_keep_nw"]),
        "sf_sell_nw_h": round(res["sf_sell_nw"]),
        "sf_keep_minus_sell": round(res["sf_keep_nw"] - res["sf_sell_nw"]),
    }


if __name__ == "__main__":
    out = write_outputs()
    print(json.dumps(out["decisions"], indent=2))
