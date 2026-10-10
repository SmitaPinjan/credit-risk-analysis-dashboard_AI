# AI Analyzer setup (free local mode)

The dashboard page and its API are served by the same local Flask server. This avoids browser cross-origin and `file://` fetch failures.

## Start the dashboard

Open PowerShell in the project folder and run:

```powershell
python -m pip install -r requirements.txt
python src/app.py
```

Then open [http://127.0.0.1:5000](http://127.0.0.1:5000). Keep the server window open while using the dashboard. No OpenAI API key, credits, or external AI service is required.

The local Analyzer uses transparent rules and the aggregate metrics computed by the dashboard. It can summarize observed default rate, average annual PD, average RWA, total EAD, and compare observed default rates across sectors and origination vintages. It does not provide open-ended language-model reasoning or forecasts. Answers remain limited to available portfolio summaries.

If you update the dashboard template and want to regenerate the HTML, install the project's dashboard dependencies (including pandas, Plotly, and statsmodels) and run `python src/dashboard.py` from this project folder.

