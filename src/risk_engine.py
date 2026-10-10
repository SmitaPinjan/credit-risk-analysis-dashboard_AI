"""Transparent descriptive credit-risk metrics for portfolio exploration.

These calculations summarize the supplied dataset. They do not implement an
OSFI capital methodology, IFRS 9 staging, or an approved credit-risk model.
"""

import pandas as pd


REQUIRED_COLUMNS = {
    "loan_id", "sector", "defaulted", "pd_annual", "lgd", "ead", "el", "rwa"
}


def _number_series(data, column):
    if column not in data:
        return pd.Series(dtype="float64")
    return pd.to_numeric(data[column], errors="coerce")


def _group_summary(data, group_column):
    if group_column not in data:
        return pd.DataFrame()
    grouped = data.groupby(group_column, dropna=False)
    result = grouped.agg(
        loan_count=("loan_id", "count"),
        observed_default_rate=("defaulted", "mean"),
        average_annual_pd=("pd_annual", "mean"),
        average_lgd=("lgd", "mean"),
        total_ead=("ead", "sum"),
        total_expected_loss=("el", "sum"),
        total_source_rwa=("rwa", "sum"),
    )
    return result.sort_values("observed_default_rate", ascending=False)


def risk_signals(frame):
    """Return measured totals and descriptive group comparisons for a portfolio."""
    missing = REQUIRED_COLUMNS.difference(frame.columns)
    if missing:
        raise ValueError(f"Missing required portfolio columns: {', '.join(sorted(missing))}")
    if frame.empty:
        return {
            "loan_count": 0,
            "default_count": 0,
            "observed_default_rate": None,
            "average_annual_pd": None,
            "average_lgd": None,
            "total_ead": 0.0,
            "total_expected_loss": 0.0,
            "total_source_rwa": 0.0,
            "sector_summary": pd.DataFrame(),
            "vintage_summary": pd.DataFrame(),
            "rating_distribution": pd.Series(dtype="int64"),
        }

    data = frame.copy()
    for column in ("defaulted", "pd_annual", "lgd", "ead", "el", "rwa"):
        data[column] = _number_series(data, column)
    data["defaulted"] = data["defaulted"].fillna(0)
    data["origination_year"] = pd.to_datetime(
        data["origination_date"], errors="coerce"
    ).dt.year if "origination_date" in data else pd.NA

    defaults = data["defaulted"].dropna()
    signals = {
        "loan_count": int(data["loan_id"].count()),
        "default_count": int(defaults.sum()),
        "observed_default_rate": float(defaults.mean()) if len(defaults) else None,
        "average_annual_pd": float(data["pd_annual"].mean()),
        "average_lgd": float(data["lgd"].mean()),
        "total_ead": float(data["ead"].sum()),
        "total_expected_loss": float(data["el"].sum()),
        "total_source_rwa": float(data["rwa"].sum()),
        "sector_summary": _group_summary(data, "sector"),
        "vintage_summary": _group_summary(data, "origination_year"),
        "rating_distribution": data["initial_rating"].value_counts(dropna=False)
        if "initial_rating" in data else pd.Series(dtype="int64"),
    }

    # A reconciliation diagnostic: dataset EL should be close to PD × LGD × EAD.
    calculated_el = data["pd_annual"] * data["lgd"] * data["ead"]
    difference = (data["el"] - calculated_el).abs().dropna()
    signals["el_formula_mean_absolute_difference"] = (
        float(difference.mean()) if len(difference) else None
    )
    return signals
