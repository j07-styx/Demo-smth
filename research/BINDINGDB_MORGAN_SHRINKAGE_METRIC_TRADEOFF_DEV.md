# Morgan ridge shrinkage: actual metric trade-off

A completed exploratory experiment blended a train-only fitted Morgan ridge model with its train-only global mean: `prediction = train_mean + ridge_weight * (ridge_prediction - train_mean)`. The ridge model was fitted on 27,118 training pairs and evaluated on 7,387 held-out-protein inner-development pairs. No prospective test data were used.

| Ridge weight | Pooled RMSE | Component-macro RMSE |
|---:|---:|---:|
| 0.00 (train mean) | **1.803902** | 1.698289 |
| 0.35 | 1.970030 | 1.602766 |
| 0.50 | 2.080236 | 1.580551 |
| 0.75 | 2.303955 | **1.571708** |
| 1.00 (raw ridge) | 2.566153 | 1.598080 |

The 0.75 blend reduces macro-component RMSE by 0.026371 (1.65%) versus raw ridge and 0.126580 (7.45%) versus train mean. However pooled RMSE is substantially worse than train mean. The blend was evaluated across seven weights on an already inspected development set, so these numbers are **exploratory and selection-biased**; no unbiased improvement has been established. This is not a new DynaCPI architecture or independent benchmark win.

**Decision:** do not promote a macro-only blend as a broad model improvement. A next defensible experiment needs protein-aware representations, a predeclared selection metric, and component-block uncertainty; the prospective test must remain untouched until the architecture and evaluation are locked. Assay and protein construct QC remain incomplete.
