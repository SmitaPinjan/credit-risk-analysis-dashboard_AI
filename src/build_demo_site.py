"""Build a GitHub Pages dashboard using synthetic demonstration records only."""

from pathlib import Path

import numpy as np
import pandas as pd

from dashboard import PROJECT_ROOT, generate_dashboard


SECTORS = [
    "Agriculture", "Construction", "Energy", "Financials", "Healthcare",
    "Manufacturing", "Real Estate", "Retail", "Technology", "Transportation",
]
RATINGS = ["AAA", "AA", "A", "BBB", "BB", "B", "CCC"]
SCENARIOS = {
    "baseline": (1.00, 1.00, 0.0, 0.0, 0.0, 0),
    "mild": (1.15, 1.05, -1.0, 1.0, 0.5, 50),
    "adverse": (1.50, 1.15, -2.5, 2.0, 1.0, 125),
    "severe": (2.00, 1.30, -4.0, 3.5, 1.5, 250),
    "gfc_like": (2.20, 1.35, -4.5, 4.0, 1.0, 300),
    "covid_like": (1.70, 1.20, -3.0, 3.0, 0.0, 200),
}


def make_demo_data(rows_per_sector=160):
    rng = np.random.default_rng(20261010)
    sector_default = np.linspace(0.105, 0.185, len(SECTORS))
    sector_pd = np.linspace(0.018, 0.055, len(SECTORS))
    count = rows_per_sector * len(SECTORS)
    sector_index = np.repeat(np.arange(len(SECTORS)), rows_per_sector)
    rng.shuffle(sector_index)
    year = rng.integers(2015, 2024, size=count)
    ead = rng.lognormal(mean=11.15, sigma=0.72, size=count)
    lgd = np.clip(rng.normal(0.52, 0.13, size=count), 0.12, 0.90)
    pd_annual = np.clip(
        sector_pd[sector_index] * rng.lognormal(0, 0.32, size=count), 0.001, 0.35
    )
    defaulted = rng.binomial(1, sector_default[sector_index])
    rating_index = np.clip(
        np.digitize(pd_annual, [0.008, 0.013, 0.020, 0.032, 0.050, 0.080]), 0, 6
    )
    rwa_factor = np.array([0.20, 0.30, 0.45, 0.75, 1.00, 1.25, 1.50])
    el = pd_annual * lgd * ead
    data = pd.DataFrame({
        "loan_id": [f"DEMO-{index:06d}" for index in range(1, count + 1)],
        "sector": [SECTORS[index] for index in sector_index],
        "origination_date": [f"{year[index]}-{rng.integers(1, 13):02d}-15" for index in range(count)],
        "initial_rating": [RATINGS[index] for index in rating_index],
        "pd_annual": pd_annual,
        "lgd": lgd,
        "ead": ead,
        "el": el,
        "rwa": ead * rwa_factor[rating_index],
        "unexpected_loss": ead * lgd * np.sqrt(pd_annual * (1 - pd_annual)),
        "defaulted": defaulted,
    })
    data["origination_year"] = pd.to_datetime(data["origination_date"]).dt.year
    return data


def make_demo_scenarios():
    rows = []
    for name, (pd_multiplier, lgd_multiplier, gdp, unemployment, rates, spreads) in SCENARIOS.items():
        for sector in SECTORS:
            rows.append({
                "scenario": name,
                "sector": sector,
                "pd_multiplier": pd_multiplier,
                "base_lgd": 0.50,
                "stressed_lgd": min(0.95, 0.50 * lgd_multiplier),
                "gdp_shock_pp": gdp,
                "unemp_shock_pp": unemployment,
                "rate_shock_pp": rates,
                "credit_spread_bps": spreads,
            })
    return pd.DataFrame(rows)


if __name__ == "__main__":
    output = PROJECT_ROOT / "docs" / "index.html"
    generate_dashboard(
        data=make_demo_data(),
        output=output,
        scenarios=make_demo_scenarios(),
        static_demo=True,
    )
