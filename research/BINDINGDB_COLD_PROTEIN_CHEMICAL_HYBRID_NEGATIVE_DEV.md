# Cold-target chemical + protein hybrid: failed pooled transfer

**Experiment:** reproducible grouped-train-CV mixture of a protein similarity prior and Morgan2048 chirality fingerprint ridge regression, with bounded chemical corrections. The reserved prospective test set was not evaluated.

## Design

- Chemical expert: ridge alpha 100 trained on 2048-bit Morgan fingerprints.
- Protein expert: nearest three training protein clusters, 3–4mer TF-IDF, similarity shrinkage selected by train-only grouped CV in the preceding experiment.
- Fusion: training-only mean plus a weighted protein correction and weighted clipped chemical residual.
- Select weights and clipping threshold on three training-only protein-component-heldout folds; require both pooled and component-macro CV RMSE to beat each fold's average mean predictor. Frozen inner-development is evaluated after selection.

## Result

| Model | Pooled inner-dev RMSE | Component-macro RMSE |
|---|---:|---:|
| Train-only global mean | **1.803902** | 1.698289 |
| Protein-only conservative prior (preceding experiment) | 1.801194 | 1.671521 |
| Protein + chemical ridge hybrid | **2.135278** | **1.522726** |

Train-only grouped CV selected full protein-prior correction plus a capped chemical ridge residual (cap 1.0, weight 1.0), with average CV pooled RMSE 1.601 and component-macro RMSE 1.468 compared with train-mean 1.688 and 1.822.

The selected hybrid **failed to transfer its CV pooled improvement** to the repeatedly inspected development cohort. Its pooled error is 18.4% higher than the mean baseline despite 10.3% lower cluster-macro RMSE. Fourteen of twenty development components improve.

**Decision:** do not promote this chemical residual fusion as the DynaCPI default. The pooled regression on the held-out protein components is too severe. The safer sequence-only gate remains the more reliable candidate from this sprint.

## Scientific qualification

These are provisional BindingDB Kd tasks; assay and construct quality controls are incomplete. All development results are exploratory due to repeated inspection; the reserved prospective test must not be accessed until a new architecture is locked. Do not claim a positive independent test, paper-level performance, or general superiority.

Reproduce with scripts/train_bindingdb_cold_protein_chemical_hybrid_dev.py.
