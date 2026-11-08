# Frozen ESM2-conditioned nonlinear booster ablation

2026-11-08; four outer alignment-protein and strict Bemis-Murcko scaffold-cold folds for each alignment identity threshold (30% and 40%, both at 80% shorter-sequence coverage); all data from BALM frozen TRAIN only. No development or prospective test records were loaded.

## Experiment

The previously supported predictor uses a 75% Ridge branch on chiral Morgan 2048, training-only protein k-mer TF-IDF and frozen ESM2 8M mean vectors, plus 25% HistGradientBoosting branch on 21 RDKit molecular descriptors and 21 AA-composition features. Beta calibration was inherited from the earlier 3-fold nested train-only selection for each outer fold.

This experiment changes only the nonlinear booster: original 42-dimensional features, those features plus 16/32 train-fold-fitted PCA components of ESM2, or 21 chemical features and 32 PCA components of ESM2 without AA composition. PCA was fitted exclusively on distinct proteins belonging to each OUTER fit partition; no validation protein vectors or labels were used to fit its PCA axes. All feature modes use the same fixed boosting hyperparameters and ensemble weights. Strict scaffold exclusion also applies to every fold.

## Results

| Booster | 40% protein group pooled RMSE | 40% macro RMSE | 30% pooled RMSE | 30% macro RMSE |
|---|---:|---:|---:|---:|
| Reference joint chemical/AA | 1.430266 | **1.337548** | 1.460624 | **1.379023** |
| Joint + PCA16 | 1.432477 | 1.342703 | **1.457022** | 1.385468 |
| Joint + PCA32 | 1.429912 | 1.344606 | 1.461183 | 1.386415 |
| Chemical + PCA32 without AA | **1.427008** | 1.348659 | 1.457406 | 1.380494 |

The slight pooled gains do NOT have group-bootstrap confidence intervals excluding zero. The 40% condition chemical+PCA32 variant shows worse macro RMSE than reference (delta +0.011110, 95% interval [+0.000207,+0.021955]). No variant consistently improves both metrics across both group rules. The best-supported architecture remains frozen ESM features regularized inside Ridge, not added freely to nonlinear boosting.

This is exploratory TRAIN-only ablation, NOT independently confirmed performance. Protein groups are alignment-derived homology proxies, not verified evolutionary homology. Scaffold exclusions do not remove all chemical analogs. The original BALM data lacks source assay DOI/method/construct and has discordant repeated-input labels; ESM2 truncates 85 long proteins to first 1022 amino acids. Development data had been inspected in earlier experiments, so bootstrap intervals are descriptive. Reserved prospective test untouched. Scientific approval gate blocked.
