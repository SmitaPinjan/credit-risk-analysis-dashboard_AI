# Project purpose and scope

## Purpose

Credit Risk Analysis is a local, exploratory dashboard for reviewing a loan portfolio. It combines portfolio filters, deterministic credit-risk indicators, visual summaries, and an AI Analyzer that answers natural-language questions using computed summaries of the filtered portfolio.

The primary portfolio source is the Kaggle [Credit Risk Dataset — 50k loans, 10 sectors](https://www.kaggle.com/datasets/sergionefedov/credit-risk-dataset-50k-loans-10-sectors). OSFI's [2026 BCAR instructions](https://www.osfi-bsif.gc.ca/en/data-forms/reporting-returns/filing-financial-returns/financial-reporting-instructions/2026-basel-capital-adequacy-reporting-bcar) and [2027 BCAR instructions](https://www.osfi-bsif.gc.ca/en/data-forms/reporting-returns/filing-financial-returns/financial-reporting-instructions/2027-basel-capital-adequacy-reporting-bcar) are reference material for regulatory context, not implemented reporting outputs. See [DATA_SOURCES.md](DATA_SOURCES.md) for details.

## Intended users

- Credit-risk analysts exploring portfolio composition and risk signals.
- Developers maintaining the dashboard, risk calculations, or AI request flow.
- Reviewers evaluating a prototype before any production deployment.

## In scope

- Loading and preparing portfolio CSV data.
- Summarizing probability of default (PD), defaults, risk-weighted assets (RWA), exposure, sector, and origination vintage.
- Displaying charts, tables, filters, and risk narratives in a local dashboard.
- Recomputing portfolio summaries, charts, review lists, narratives, and illustrative stress sensitivities from the selected sector, vintage, and loan search.
- Answering supported natural-language portfolio questions locally from aggregate dashboard summaries and active filters.
- Improving local setup, reproducibility, error handling, and documentation.

## Out of scope

- Automated loan approval, pricing, collections, or other individual credit decisions.
- A production multi-user service, authentication, authorization, audit logging, or deployment infrastructure.
- Replacing validated risk models, regulatory processes, or analyst review with AI output.
- Inferring causal explanations from descriptive portfolio summaries.

## Data and AI boundaries

- Source data is stored under `data/`; treat it as user/project data and do not modify it during routine feature work.
- The browser submits aggregate summary signals to the local analysis API. Do not send borrower identifiers or raw loan-level records.
- The local analyst uses fixed rules; it has no external model, API key, or API billing requirement. It supports answers grounded in the supplied summary metrics, not unrestricted conversation.
- Answers are explanations, not verified model outputs. They should identify the evidence available, flag missing information, and avoid unsupported conclusions.
- The supplied file has no IFRS 9 stage field. Rating is shown from the source `initial_rating`; it is not converted into IFRS 9 stages.
- RWA is displayed as a supplied dataset field. The dashboard does not reproduce OSFI's complete regulatory RWA calculation, capital ratios, or BCAR returns.
- Stress results are illustrative calculations using the local scenario file's sector-level PD multipliers and LGD stresses. They are not OSFI-prescribed stress tests.

## Success criteria

- A developer can install dependencies, start the local server, and open the dashboard using documented steps.
- Dashboard edits are reproducible from the template and generator.
- Filter selections and the data used for the AI answer stay aligned.
- Invalid or unsupported local analysis requests produce clear, data-grounded responses.
