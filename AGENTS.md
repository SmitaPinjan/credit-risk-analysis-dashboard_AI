# Instructions for coding agents

## Goal and boundaries

This repository builds a local credit-risk analysis dashboard for portfolio exploration. Preserve the distinction between measured portfolio data, computed indicators, and AI-generated explanations. Do not present correlation as causation or use this prototype as the sole basis for a lending or credit decision.

## Before changing code

- Read `docs/PROJECT_SCOPE.md` for product purpose, users, non-goals, and data boundaries.
- Read `docs/DATA_SOURCES.md` before changing, redistributing, or describing dataset and regulatory provenance.
- Read `skills.md` and `.agents/skills/credit-risk-dashboard/SKILL.md` for this project's working conventions.
- Inspect the current implementation and preserve unrelated user changes.
- Treat `src/dashboard_template.html` and `src/dashboard.py` as the source for the generated `dashboard.html`.

## Source-of-truth map

- `src/app.py` owns HTTP routes and server-side AI calls.
- `src/dashboard.py` owns generation of dashboard data, charts, and tables.
- `src/dashboard_template.html` owns the dashboard UI and client-side filtering/fetch behavior.
- `src/risk_engine.py` owns reusable descriptive portfolio metrics; `src/dashboard_template.html` recomputes dashboard views in the browser for the active filters.
- `data/` contains source datasets. Never edit or replace these files as part of routine feature work unless the user specifically requests data changes.
- `dashboard.html` is generated output and may be large. Avoid hand-editing it; make durable UI changes in the template and regenerate it when dependencies are available.

## Implementation rules

- The current AI Analyzer is local and rule-based; do not reintroduce external API credentials or paid services unless the user explicitly requests that change.
- Keep the dashboard and API same-origin when feasible. The intended local entry point is `http://127.0.0.1:5000/`.
- Validate API inputs and return actionable JSON errors. Do not expose secrets or raw provider responses to browser users.
- Keep AI answers grounded in the supplied data. Say when a question cannot be answered from the available summaries.
- When changing dashboard filters or data fields, keep the generated browser dataset, filters, AI summaries, and server prompt aligned.
- Keep data transformations reproducible. Prefer calculations in Python or small named JavaScript functions over unexplained inline constants.
- Avoid adding dependencies unless needed; update `requirements.txt` when adding one.
- Do not commit private datasets, API keys, virtual environments, or generated exports unless the user explicitly asks.

## Local workflow

- Install dependencies: `python -m pip install -r requirements.txt`.
- Run the app from the repository root: `python src/app.py`.
- Regenerate the dashboard from the root: `python src/dashboard.py`.
- The local rule-based Analyzer needs no API key or external model service.
- Review existing checks before relying on them. Files named `src/test_*.py` currently contain scripts and may not be a complete automated test suite.
- Do not claim a check passed unless it was run successfully in the current environment. If dependencies or runtime are unavailable, report that clearly.

## Change reporting

Summarize changed files, user-visible behavior, commands/checks run, and any limitations. Link to local files using absolute paths in the final response.
