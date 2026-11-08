# Component imbalance diagnosis for Morgan ridge

Recomputed the identical train-only Morgan ridge fit and inner-development predictions, now preserving anonymized per-protein-component RMSE, size and squared-error contributions. No test components were accessed, and the model or split was not altered.

- **One** held-out protein component has 5,027 of 7,387 inner-dev pairs (68.05%). Its Morgan ridge RMSE is 2.8673 versus 1.8401 for the train-only global mean.
- The **three** highest-error components contribute 94.12% of Morgan ridge squared error.
- Morgan ridge improves over the mean comparator on **13 of 20** protein components, despite pooled RMSE being substantially worse (2.5662 vs 1.8039).
- Morgan ridge macro-component RMSE is 1.5981, versus 1.6983 for the global mean comparator (reported in the existing mean baseline). Macro-component improvement is not proof of statistical significance or a valid independent test.

**Interpretation:** the earlier pooled result hides heterogeneous behavior. A few large and/or high-error components dominate the pooled metric. This suggests reporting both pooled and per-component macro scores for any subsequent protein-aware model and using component-block bootstrap uncertainty. Do not optimize on the prospective test or claim broad superiority from this heavily inspected inner-dev split. Assay/construct QC remains provisional.
