"""Build the local credit-risk dashboard from the supplied portfolio data."""

import html
import json
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
TEMPLATE_PATH = PROJECT_ROOT / "src" / "dashboard_template.html"


def load_data():
    """Load portfolio rows and derive the vintage field used by dashboard filters."""
    portfolio_path = DATA_DIR / "loan_portfolio.csv"
    if not portfolio_path.is_file():
        raise FileNotFoundError(
            "Missing data/loan_portfolio.csv. Follow data/README.md to obtain "
            "the local input before generating the dashboard."
        )
    data = pd.read_csv(portfolio_path)
    data["origination_year"] = pd.to_datetime(
        data["origination_date"], errors="coerce"
    ).dt.year
    return data


def build_filter_options(data):
    sectors = sorted(data["sector"].dropna().astype(str).unique())
    years = sorted(data["origination_year"].dropna().astype(int).unique())

    sector_html = '<select id="sectorFilter" class="form-select"><option value="">All</option>'
    sector_html += "".join(
        f'<option value="{html.escape(sector, quote=True)}">{html.escape(sector)}</option>'
        for sector in sectors
    )
    sector_html += "</select>"

    year_html = '<select id="vintageFilter" class="form-select"><option value="">All</option>'
    year_html += "".join(
        f'<option value="{year}">{year}</option>' for year in years
    )
    year_html += "</select>"
    return sector_html, year_html


def empty_table(table_id, columns):
    headers = "".join(f"<th>{html.escape(column)}</th>" for column in columns)
    return (
        f'<table id="{table_id}" class="table table-striped table-bordered">'
        f"<thead><tr>{headers}</tr></thead><tbody></tbody></table>"
    )


def _json_records(frame):
    # Escape script-closing sequences before embedding source records in HTML.
    records = frame.astype(object).where(pd.notna(frame), None)
    return json.dumps(
        records.to_dict(orient="records"),
        default=str,
        separators=(",", ":"),
        allow_nan=False,
    ).replace("</", "<\\/")


def generate_dashboard(data=None, output=None, scenarios=None, static_demo=False):
    data = load_data() if data is None else data.copy()
    if "origination_year" not in data:
        data["origination_year"] = pd.to_datetime(
            data["origination_date"], errors="coerce"
        ).dt.year
    scenario_path = DATA_DIR / "macro_stress_scenarios.csv"
    if not scenario_path.is_file():
        raise FileNotFoundError(
            "Missing data/macro_stress_scenarios.csv. Follow data/README.md "
            "to obtain the local scenario input before generating the dashboard."
        )
    scenarios = pd.read_csv(scenario_path) if scenarios is None else scenarios.copy()

    sector_options, vintage_options = build_filter_options(data)
    with TEMPLATE_PATH.open("r", encoding="utf-8") as file:
        template = file.read()

    replacements = {
        "{sector_options}": sector_options,
        "{vintage_options}": vintage_options,
        "{pd_spikes_table}": empty_table(
            "pdSpikesTable",
            ["loan_id", "sector", "origination_year", "initial_rating", "pd_annual"],
        ),
        "{rwa_jump_table}": empty_table(
            "rwaJumpTable",
            ["loan_id", "sector", "origination_year", "ead", "rwa", "rwa_to_ead"],
        ),
        "{risky_loans_table}": empty_table(
            "riskyLoansTable",
            ["loan_id", "sector", "origination_year", "pd_annual", "lgd", "ead", "el"],
        ),
        "{portfolio_overview}": "<p>Loading filtered portfolio metrics…</p>",
        "{initial_narrative}": "Loading portfolio observations…",
        "{stress_html}": "<p>Loading supplied scenario assumptions…</p>",
        "{recs_html}": "<p>Loading review priorities…</p>",
        "{full_data_json}": _json_records(data),
        "{stress_scenarios_json}": _json_records(scenarios),
        "{static_demo}": "true" if static_demo else "false",
        "{demo_notice}": (
            '<div class="alert alert-info" role="status"><b>Interactive portfolio demo:</b> '
            'all loan rows below are synthetic and generated for this browser preview. '
            'They are not the Kaggle dataset or real borrower records.</div>'
            if static_demo else ""
        ),
    }
    for placeholder, value in replacements.items():
        template = template.replace(placeholder, value)

    destination = Path(output) if output else PROJECT_ROOT / "dashboard.html"
    if not destination.is_absolute():
        destination = PROJECT_ROOT / destination
    destination.write_text(template, encoding="utf-8")
    print(f"Dashboard generated: {destination}")


if __name__ == "__main__":
    generate_dashboard()
