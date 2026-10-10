# Local data setup

This folder is intentionally excluded from the public Git repository. The generated `dashboard.html` also stays local because it embeds the portfolio rows.

## Required files

Place the following locally obtained CSV files in this folder before building the dashboard:

- `loan_portfolio.csv` — primary loan-level input. The project describes its source as Sergio Nefedov's Kaggle [Credit Risk Dataset — 50k loans, 10 sectors](https://www.kaggle.com/datasets/sergionefedov/credit-risk-dataset-50k-loans-10-sectors).
- `macro_stress_scenarios.csv` — sector-level illustrative stress assumptions used by the dashboard. Confirm its source and license; do not assume it is included in the Kaggle download.

Then, from the project root, run:

```powershell
python src/dashboard.py
python src/app.py
```

Review the Kaggle page's current license and terms before downloading, using, or sharing data. Do not upload raw CSVs or the generated dashboard unless the applicable license allows it and required attribution is included. The dashboard page contains loan-level records when generated.

To use the full dashboard on another computer without putting data in GitHub, clone/copy the source project, place the locally obtained CSV inputs in its `data/` folder, install `requirements.txt`, generate the dashboard, and run Flask. A privately transferred generated HTML file can display the charts, but it contains the loan rows and its Analyzer requires the Flask API.

The other CSVs that may exist in a developer's local copy are not required by the current dashboard generator. They remain excluded until their provenance and redistribution terms are verified.

## Public browser demo

The GitHub Pages version is generated separately by `python src/build_demo_site.py`. It uses deterministic synthetic records and does not read files from this folder. The hosted sample makes the charts, filters, and bounded Analyzer available in a browser without publishing the Kaggle rows.
