# Data sources and references

## Primary portfolio dataset

- **Dataset:** [Credit Risk Dataset — 50k loans, 10 sectors](https://www.kaggle.com/datasets/sergionefedov/credit-risk-dataset-50k-loans-10-sectors)
- **Publisher:** Sergio Nefedov on Kaggle.
- **Description:** The supplied dataset listing describes 50,000 loans across 10 sectors, with credit-risk fields including PD, LGD, and EAD, and material related to Moody's transition matrices, Basel III stress testing, and OSFI/Basel.
- **Local dashboard input:** `data/loan_portfolio.csv`. `src/dashboard.py` currently reads this file as its primary portfolio input.
- **License and attribution:** Use the license shown on the Kaggle dataset page as the source of truth. Before redistributing the raw dataset or a generated dashboard that embeds its rows, record the exact license and required attribution here and in the repository README. Public availability on Kaggle does not by itself establish permission to redistribute the files.

## Other local data files

The `data/` directory also contains `credit_ratings.csv`, `macro_stress_scenarios.csv`, `payment_history.csv`, `payment_history_dictionary.csv`, `portfolio_metrics.csv`, `vintage_analysis.csv`, and a UUID-named CSV. The dashboard uses `macro_stress_scenarios.csv` for filtered illustrative stress sensitivities; other supporting files are not treated as inputs to those dashboard views. Confirm the source and license for each supporting file before describing it as part of the Kaggle download or publishing it.

## Regulatory reference

- **2026 reference supplied for this project:** [OSFI — 2026 Basel Capital Adequacy Reporting (BCAR)](https://www.osfi-bsif.gc.ca/en/data-forms/reporting-returns/filing-financial-returns/financial-reporting-instructions/2026-basel-capital-adequacy-reporting-bcar).
- **Newer OSFI version:** [OSFI — 2027 Basel Capital Adequacy Reporting (BCAR)](https://www.osfi-bsif.gc.ca/en/data-forms/reporting-returns/filing-financial-returns/financial-reporting-instructions/2027-basel-capital-adequacy-reporting-bcar). The 2027 page is updated September 2026 and links to the previous version for reporting before January 31, 2027.
- **Capital methodology:** OSFI's [2027 Capital Adequacy Requirements (CAR) Guideline, Chapter 1](https://www.osfi-bsif.gc.ca/en/guidance/guidance-library/capital-adequacy-requirements-car-2027-chapter-1-overview-risk-based-capital-requirements) describes regulatory RWA as a broader capital framework, including credit, market, and operational risk components and, where applicable, a capital floor. The dashboard's supplied loan-level `rwa` field is not a replacement for that calculation.
- **Project use:** These are regulatory context and reference material for concepts such as capital adequacy, credit risk, and RWA. The current dashboard does not produce a BCAR return, implement all BCAR calculations, or establish regulatory compliance. Consult the applicable reporting-period instructions and related OSFI guidelines for official reporting.

## Publication checklist

- Include the Kaggle dataset link, creator attribution, and exact dataset license in the repository.
- Do not commit raw source CSVs unless their license permits redistribution.
- Remember that the generated root `dashboard.html` embeds portfolio rows. Regenerate it only with a dataset that is permitted for redistribution, or omit it from a public repository and document how to build it locally.
- `docs/index.html` is a separate GitHub Pages demo built from the deterministic synthetic rows in `src/build_demo_site.py`; it does not use or include the Kaggle loan rows. Keep that distinction visible in the demo notice.
- Keep regulatory links versioned by reporting year; do not silently treat a prior-year BCAR page as current guidance.
