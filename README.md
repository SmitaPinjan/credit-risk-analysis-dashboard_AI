# Credit Risk Analysis Dashboard with AI analyzer

An interactive portfolio dashboard for exploring credit-risk indicators across a loan portfolio. It includes filter-aware charts and narratives plus an AI (currently a local rule-based) Analyzer that answers supported questions from the currently filtered aggregate metrics.

> **Portfolio prototype:** this project is for exploration and demonstration. It is not a lending decision tool, a validated risk model, an official OSFI/BCAR calculator, or evidence of regulatory compliance.

## Features

- Filter portfolio views by sector and origination vintage, with a loan search for narrowing displayed analysis.
- Review observed defaults, annual PD, LGD, EAD, expected loss, supplied RWA, ratings, and illustrative stress sensitivities.
- Ask the Analyzer questions about the active filter. It runs locally with transparent fixed rules; no API key, model subscription, or external AI service is needed.
- Rebuild the dashboard HTML from the source template and local data.
- Browse the [GitHub Pages demo](https://smitapinjan.github.io/credit-risk-analysis-dashboard_AI/) after enabling Pages and completing its first deployment. It uses generated synthetic rows, and its Analyzer runs in the browser.


The public repository intentionally excludes source CSVs and `dashboard.html`: the latter embeds loan-level rows. After obtaining the required files locally, `python src/dashboard.py` builds the page. The generator reports a useful missing-file error if required files have not been placed in `data/`.

## Use on another computer

For the complete dashboard and working Analyzer, copy or clone the source project to that computer, obtain the required CSVs there under the applicable data license, install Python dependencies, and follow the Quick start. The dashboard is generated locally from the local data; GitHub does not need to host the data.

You can also generate `dashboard.html` on your own computer and transfer that single file privately to another computer to view the charts in a browser. **That HTML embeds the loan-level portfolio rows.** Do not upload it to GitHub or share it publicly unless the dataset license permits redistribution. When opened as a file, dashboard visuals and browser-side filters can work, but the AI Analyzer API requires Flask; run the app and open it at the local URL above to use the Analyzer.

## AI Analyzer behavior

This Analyzer is demo purpose and is not connected to any AI models yet so it will be providing answers based on pre determined questions and not a live AI analysis and reasoning. The Analyzer is a local deterministic rules engine, not an open-ended language model. It answers a limited set of questions grounded in aggregate values computed in the browser, including observed defaults, average annual PD, EAD, supplied RWA, and descriptive sector or vintage comparisons. It explains the scope and evidence in its answer and cannot infer unsupported causes or forecast future defaults. Browser requests send aggregate signals rather than raw loan rows.

The hosted Pages demo uses synthetic demonstration data and a browser-side version of the same bounded rule-based analysis. The full local dashboard uses the Flask API. Do not interpret synthetic demo values as findings about the Kaggle portfolio.

## Project map

- `src/app.py` — Flask routes and local analysis API.
- `src/dashboard.py` — dashboard generation, chart/table scaffolding, and local input loading.
- `src/dashboard_template.html` — editable dashboard interface and browser-side filter calculations.
- `src/risk_engine.py` — reusable descriptive risk calculations.
- `data/README.md` — local input requirements and provenance.
- `docs/PROJECT_SCOPE.md` — purpose, intended users, scope, and boundaries.
- `docs/DATA_SOURCES.md` — dataset and OSFI reference links and redistribution notes.
- `docs/PORTFOLIO_ANALYSIS.md` — metric definitions, audited snapshot, and limitations.
- `AGENTS.md`, `skills.md`, `.agents/skills/` — project-specific agent guidance.

## Data and references

The primary input is based on Sergio Nefedov's Kaggle [Credit Risk Dataset — 50k loans, 10 sectors](https://www.kaggle.com/datasets/sergionefedov/credit-risk-dataset-50k-loans-10-sectors). Review Kaggle's current license and download terms before using or redistributing any files. Public availability does not itself grant permission to redistribute. Required local filenames and build steps are in [`data/README.md`](data/README.md).

OSFI's [2026 BCAR instructions](https://www.osfi-bsif.gc.ca/en/data-forms/reporting-returns/filing-financial-returns/financial-reporting-instructions/2026-basel-capital-adequacy-reporting-bcar) and [2027 BCAR instructions](https://www.osfi-bsif.gc.ca/en/data-forms/reporting-returns/filing-financial-returns/financial-reporting-instructions/2027-basel-capital-adequacy-reporting-bcar) are regulatory references. The dashboard displays supplied dataset fields and illustrative sensitivities; it does not implement complete BCAR calculations or reporting. Read [`docs/DATA_SOURCES.md`](docs/DATA_SOURCES.md) and [`docs/PORTFOLIO_ANALYSIS.md`](docs/PORTFOLIO_ANALYSIS.md) for details.

## Development

Edit `src/dashboard_template.html` and `src/dashboard.py`; treat root `dashboard.html` as generated output. For dashboard changes, rebuild with `python src/dashboard.py`, then run `python src/app.py` and inspect the page at the local URL above. Keep new calculations grounded in source fields, preserve active filters across views, and update metric documentation when definitions change.

To regenerate the safe, static Pages demo, run `python src/build_demo_site.py`. It writes `docs/index.html` from deterministic synthetic data only; no Kaggle data is read by that command. GitHub Actions deploys the `docs/` directory to Pages after it is enabled for the repository.
