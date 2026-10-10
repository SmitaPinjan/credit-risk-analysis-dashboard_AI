# Portfolio analysis notes

## Audited input snapshot

The dashboard's primary input, `data/loan_portfolio.csv`, contains 50,000 unique loan rows across ten sectors, originated from January 2015 through December 2023. The observed `defaulted` field marks 6,950 rows as defaults (13.90%). The arithmetic mean of `pd_annual` is 2.246%; mean LGD is 54.65%. Source-field totals are EAD 164,930,233,732.19, expected loss 1,923,786,053.37, and RWA 25,490,165,225.99 in the dataset's unspecified units/currency.

The source expected-loss field closely reconciles to `pd_annual × lgd × ead` (small row-level differences are consistent with rounding). The default label is observed history; average annual PD is a model input/estimate. The dashboard reports both separately and does not call their difference model miscalibration because the dataset does not document a common forecast horizon, censoring method, or calibration methodology.

Financials has the highest raw sector default rate in the full portfolio (14.75% across 5,023 loans); Healthcare has the lowest (13.19% across 4,982 loans). These are descriptive statistics and are recalculated under the selected filters. Vintage rates can be affected by unequal time on books, so they are shown as observed outcomes rather than forecasts or performance rankings.

## Dashboard definitions

- **Observed default rate:** sum of the source `defaulted` indicator divided by the number of filtered rows with a usable indicator.
- **Average annual PD / LGD:** arithmetic averages of the source fields for the filtered rows.
- **EAD, expected loss, RWA, unexpected loss:** sums/records from the supplied dataset fields. The dashboard does not infer a currency from numeric values.
- **Sector and vintage charts:** observed default rates are shown with group counts in hover details; the vintage chart uses `origination_year` from `origination_date`.
- **Initial rating distribution:** uses source `initial_rating`. There is no `ifrs9_stage` or equivalent accounting-stage field in this input, so no IFRS 9 Stage 1/2/3 classification is inferred.
- **RWA review list:** sorts by source RWA divided by EAD. This is a screening ratio, not a regulatory outlier test.
- **Largest expected-loss exposures:** ranks the supplied `el` values. It is a portfolio review list, not an individual credit decision.
- **Stress sensitivity:** for each loan, applies the matching sector's `pd_multiplier` and `stressed_lgd / base_lgd` from `macro_stress_scenarios.csv` to the loan's PD, LGD, and EAD; PD and LGD are capped at 100%. The displayed expected loss is then summed over the active filters. This is an illustrative scenario application, not a validated model.

All sector, vintage, and loan-ID filters apply consistently to summary values, narrative, charts, review tables, stress sensitivity, and Analyzer context.

## Regulatory boundary

OSFI's [2027 BCAR instructions](https://www.osfi-bsif.gc.ca/en/data-forms/reporting-returns/filing-financial-returns/financial-reporting-instructions/2027-basel-capital-adequacy-reporting-bcar) describe reporting schedules, data validation, exposures, expected loss, and RWA. The [2027 CAR Guideline, Chapter 1](https://www.osfi-bsif.gc.ca/en/guidance/guidance-library/capital-adequacy-requirements-car-2027-chapter-1-overview-risk-based-capital-requirements) describes RWA as part of a wider framework that includes credit, market, and operational risk, with a capital floor where applicable. This dashboard only explores supplied loan-level fields; it does not calculate regulatory capital ratios, implement BCAR schedules, establish compliance, or replace OSFI reporting instructions. Use the version applicable to the institution's reporting period.
