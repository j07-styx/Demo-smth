# Frozen BindingDB nonlinear protein models and training-only ensemble calibration

## Scope

All results use the 27,118-pair / 82-component frozen training split and 7,387-pair / 20-component exploratory inner-development split. Reserved prospective test pairs excluded before target-label inspection. Assay/construct QC incomplete and the inner-dev set has been repeatedly inspected; no independent benchmark superiority claims.

## Model training

Fixed scikit-learn HistGradientBoostingRegressor: 160 rounds, learning rate 0.05, 15 max leaves, depth 5, min leaf 80, L2 regularization 15. Features: 21 RDKit molecular descriptors; plus 20 amino-acid fraction values and log protein length (21 values) for joint model.

| Frozen inner-dev | Train mean | Chemistry only | Chemistry + protein |
|---|---:|---:|---:|
| Pooled RMSE | **1.803902** | 2.327239 | 2.243330 |
| Component-macro RMSE | 1.698289 | 1.516156 | **1.458854** |
| Components better than mean (of 20) | — | 14 | **15** |

Reweighting training examples by inverse sqrt of protein-component count **did not help** the joint model: pooled RMSE 2.277618, macro RMSE 1.497215.

## Train-only protein-group cross-validation

Three GroupShuffleSplit folds, each holding out 17 protein components within **training only**:

| Mean fold RMSE | Mean | Chemistry | Chemistry+protein | Joint weighted |
|---|---:|---:|---:|---:|
| Pooled | 1.688024 | **1.573277** | 1.663677 | 1.749634 |
| Component macro | 1.821762 | 1.434480 | **1.346020** | 1.351095 |

Fold training sizes range from 6,279 to 26,003 pairs. One fold has a giant held-out component comprising 85.5% of the fold pairs. Splits overlap and are not an independent performance estimate.

## Train-only selected ensemble

Candidate ensemble = train-only mean + shrink factor times weighted chemical/joint deviations from train-only mean. Tested shrink [0, 0.15, 0.3, 0.5, 0.75, 1] and protein weight [0, 0.5, 1], chosen entirely on three training-only folds by equal-weighted pooled/macro RMSE objective.

Selected combination: **shrink 1.0, protein weight 0.5**. CV mean pooled RMSE **1.592761**, macro RMSE **1.356940**. Refit on entire train: frozen inner-dev pooled **2.252562**, component macro **1.463351**. Pooled is substantially worse than mean 1.803902; macro is better than mean 1.698289. No candidate global shrink within this grid beat the unshrunk mixed model on the CV balanced objective.

Interpretation: additional protein features consistently improve macro performance, but cannot currently solve pair-weighted generalization on large novel components. Further adjustment requires train-only validation or an approved independent benchmark, not development-set overfitting.
