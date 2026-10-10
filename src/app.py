"""Local Flask API and web server for the credit risk dashboard."""

import os
from pathlib import Path

from flask import Flask, jsonify, request, send_file


app = Flask(__name__)
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DASHBOARD_PATH = PROJECT_ROOT / "dashboard.html"


@app.get("/")
def dashboard():
    """Serve the dashboard from the same origin as its analysis API."""
    if not DASHBOARD_PATH.is_file():
        return (
            "Dashboard not found. Generate it with `python src/dashboard.py` "
            "from the project directory.",
            404,
        )
    return send_file(DASHBOARD_PATH)


@app.get("/health")
def health():
    return jsonify({"ok": True, "analysis_mode": "local"})


def _percent(value):
    try:
        return f"{float(value):.2%}"
    except (TypeError, ValueError):
        return "unavailable"


def _money(value):
    try:
        return f"${float(value):,.2f}"
    except (TypeError, ValueError):
        return "unavailable"


def _local_analysis(question, sector, vintage, signals):
    """Answer portfolio questions from browser-computed aggregates only."""
    if not signals or not signals.get("loan_count"):
        return "There are no loans in the current filter, so I cannot calculate portfolio metrics. Adjust the sector or vintage filters and try again."

    try:
        count = max(0, int(signals.get("loan_count", 0)))
    except (TypeError, ValueError):
        count = 0
    if count == 0:
        return "There are no loans in the current filter, so I cannot calculate portfolio metrics. Adjust the sector or vintage filters and try again."
    default_rate = signals.get("observed_default_rate")
    pd_rate = signals.get("average_annual_pd")
    avg_rwa = signals.get("average_rwa")
    total_ead = signals.get("total_ead")
    scope = f"the {sector} sector" if sector and sector != "All" else "all sectors"
    if vintage and vintage != "All":
        scope += f", vintage {vintage}"
    summary = (
        f"For {scope}, the current filters include {count:,} loans. "
        f"Observed default rate: {_percent(default_rate)}; "
        f"average annual PD: {_percent(pd_rate)}; "
        f"average RWA: {_money(avg_rwa)}; total EAD: {_money(total_ead)}."
    )

    q = question.casefold()
    asks_sector = any(term in q for term in ("sector", "industry"))
    asks_vintage = any(term in q for term in ("vintage", "year", "origination"))
    if asks_sector or asks_vintage:
        key = "by_sector" if asks_sector else "by_vintage"
        label = "sector" if asks_sector else "origination_year"
        groups = signals.get(key) or []
        metric = "observed_default_rate"
        ranked = [row for row in groups if row.get(metric) is not None]
        if ranked:
            highest = max(ranked, key=lambda row: row[metric])
            lowest = min(ranked, key=lambda row: row[metric])
            high_name = highest.get(label, "Unknown")
            low_name = lowest.get(label, "Unknown")
            return (
                f"{summary}\n\nComparing {len(ranked)} {label} groups by observed default rate, "
                f"{high_name} is highest at {_percent(highest[metric])} ({highest.get('loan_count', 0):,} loans), "
                f"and {low_name} is lowest at {_percent(lowest[metric])} ({lowest.get('loan_count', 0):,} loans). "
                "These are descriptive differences and do not establish why defaults differ."
            )

    if any(term in q for term in ("default", "delinquen", "bad loan", "failure")):
        try:
            observed_defaults = round(count * float(default_rate)) if default_rate is not None else None
        except (TypeError, ValueError):
            observed_defaults = None
        count_text = f"approximately {observed_defaults:,} defaults" if observed_defaults is not None else "an unavailable default count"
        return f"{summary}\n\nThe observed default rate corresponds to {count_text} in this filtered portfolio. This is a historical portfolio measure, not a prediction for an individual borrower."

    if any(term in q for term in ("pd", "probability of default", "predict", "future", "forecast")):
        return f"{summary}\n\nAverage annual PD is the portfolio's modeled probability-of-default measure. Observed default rate is the historical share marked as defaulted. These measures are related but are not interchangeable; this summary alone cannot forecast future defaults."

    if any(term in q for term in ("ead", "exposure", "rwa", "risk-weighted")):
        return f"{summary}\n\nEAD is the exposure amount represented in the supplied portfolio data, while RWA is the supplied risk-weighted-asset measure. The dashboard summary does not include enough detail to independently validate either calculation."

    return (
        f"{summary}\n\nI can answer questions about the filtered portfolio's observed defaults, average annual PD, "
        "RWA, EAD, and which sectors or origination vintages have higher or lower observed default rates. "
        "This free local analyst uses fixed, transparent rules rather than an online language model, so it cannot answer open-ended questions beyond those supplied metrics."
    )


@app.post("/ai_analyze")
def ai_analyze():
    data = request.get_json(silent=True) or {}
    question = str(data.get("question", "")).strip()
    if not question:
        return jsonify({"error": "Enter a question for the AI analyst."}), 400
    if len(question) > 4000:
        return jsonify({"error": "Keep the question under 4,000 characters."}), 400

    sector = str(data.get("sector") or "All")
    vintage = str(data.get("vintage") or "All")
    signals = data.get("signals") if isinstance(data.get("signals"), dict) else {}
    return jsonify({"answer": _local_analysis(question, sector, vintage, signals), "mode": "local"})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=int(os.getenv("PORT", "5000")), debug=False)
