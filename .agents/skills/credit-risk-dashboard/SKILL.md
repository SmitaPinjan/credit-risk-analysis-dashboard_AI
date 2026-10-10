---
name: credit-risk-dashboard
description: Make changes to this repository's Flask dashboard, AI Analyzer, portfolio data flow, or credit-risk metrics while preserving the project's scope and source-of-truth boundaries.
---

# Credit Risk Dashboard skill

Use this guide when changing the dashboard, AI Analyzer, API, or risk calculations in this repository.

## Understand the data path

1. CSV inputs live in `data/`.
2. `src/dashboard.py` loads the portfolio, derives dashboard data, and fills placeholders in `src/dashboard_template.html`.
3. The generated page is written to root-level `dashboard.html` and served from `/` by `src/app.py`.
4. The browser sends a question, active filters, and computed summary metrics to `POST /ai_analyze`.
5. `src/app.py` applies local, rule-based analysis and returns `{ "answer": ..., "mode": "local" }`.

Keep these steps consistent when changing fields, filters, or metrics. The API should receive summaries needed to answer questions, not an unnecessarily large raw portfolio payload.

## Editing rules

- Edit the template and generator for durable dashboard changes. Treat `dashboard.html` as generated output.
- Keep fetch URLs relative (`/ai_analyze`) while the dashboard is served by Flask.
- Keep the Analyzer local and free; do not add external AI credentials or paid model calls unless the user asks for them.
- Validate empty, malformed, and oversized user input. Return useful HTTP status codes and JSON error messages.
- Make uncertainty visible: distinguish observed metrics from hypotheses, and do not invent unsupported causes or trends.
- Preserve active sector and vintage filters in the AI request.
- Keep the analysis grounded in aggregate summaries; do not send personal or loan-level data to external services.
- Avoid changing CSVs or notebooks when the request concerns the application unless those files are necessary to the requested result.

## Run and review

From the repository root, use `python -m pip install -r requirements.txt`, then `python src/app.py`. Open the dashboard at `http://127.0.0.1:5000/`; opening the generated HTML through `file://` bypasses the API server.

Regenerate the HTML with `python src/dashboard.py` after template or generator changes. Inspect the diff or generated output when possible, and report when a missing runtime/dependency prevents regeneration or verification.
