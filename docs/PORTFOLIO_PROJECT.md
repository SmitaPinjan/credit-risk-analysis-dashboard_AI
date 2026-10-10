# Portfolio project summary

## Credit Risk Analysis Dashboard

An interactive, local-first dashboard for exploring a 50,000-loan credit-risk dataset. The project combines filter-aware portfolio metrics, data visualizations, descriptive stress sensitivities, and a no-cost rule-based Analyzer that answers a bounded set of questions from aggregate metrics.

### What I built

- A Flask app serving a browser dashboard and same-origin analysis endpoint.
- A reproducible Python build that turns a source HTML template and local CSV inputs into a dashboard page.
- Filter-aware views for sector and origination vintage, including observed default rate, PD, LGD, EAD, expected loss, and the supplied RWA field.
- A local Analyzer that uses transparent rules and aggregate summaries, with no API credentials or paid inference service.
- Documentation that distinguishes observed outcomes, supplied model fields, illustrative scenarios, and regulatory reference material.

### Risk and data boundaries

The Analyzer is intentionally limited and is not a general-purpose language model. Sector and vintage differences are descriptive, not causal. Dataset RWA is not independently recalculated as regulatory RWA. Stress sensitivities are illustrative, not OSFI-prescribed tests. This prototype is not an individual credit decision system or a regulatory compliance tool.

### Data source

The primary data source is attributed to Sergio Nefedov's Kaggle [Credit Risk Dataset — 50k loans, 10 sectors](https://www.kaggle.com/datasets/sergionefedov/credit-risk-dataset-50k-loans-10-sectors). OSFI BCAR pages are linked as regulatory background only. The public source repository excludes the CSVs and generated HTML until the exact redistribution license and attribution requirements are confirmed.

### Run locally

See the repository README and [`data/README.md`](../data/README.md) for Python setup, required local inputs, and launch commands.

### Browser demo

The repository's GitHub Pages demo is designed to run in a browser using clearly labeled synthetic data. It does not include the Kaggle loan records. The full local dashboard can be built from the user's local dataset files.
