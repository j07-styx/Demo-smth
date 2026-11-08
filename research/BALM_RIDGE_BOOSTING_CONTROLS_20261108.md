# BALM Ridge + boosting controls — 2026-11-08

This matched follow-up changes the interpretation of the earlier explicit-cross-product experiment: the improvement is not specific to handcrafted protein × compound cross-products. Comparison is retrospective after prior development inspection.

## Fixed 25% booster comparisons

Same 75% Morgan-2048 / protein tri/tetra-gram Ridge (alpha=1, protein feature scaling .25) across models. Boosters: (A) 21 molecular RDKit descriptors, (B) 21 molecule+21 protein AA features, (C) both plus 64 cross products. Fixed HistGradientBoosting hyperparameters across modes: 160 trees, learning rate .05, max leaves 15, max depth 5, min leaf 50, L2 15. Three train-only graph-component-disjoint folds; final fit uses 12,315 unique averaged training sequence–compound pairs. Frozen development has 3,891 original pair labels and 173 held-out graph components. Reserved 5,271-row test untouched.

| Model | TRAIN CV pooled RMSE | TRAIN CV macro RMSE | Development pooled RMSE | Development macro RMSE |
|---|---:|---:|---:|---:|
| Ridge | 1.321318 | 1.200437 | 1.405092 | 1.269216 |
| Ridge+chemical-only boost | 1.304784 | 1.197528 | **1.376388** | 1.251580 |
| Ridge+ordinary joint boost | 1.304647 | **1.185342** | 1.382236 | **1.245649** |
| Ridge+explicit interaction boost | **1.303467** | 1.190172 | 1.383743 | 1.247097 |

## 5000 paired group bootstrap resamples, seed 20261108

95% percentile confidence intervals for candidate-minus-Ridge RMSE; group is the unit of resampling, not each individual row.

| Candidate | Pooled delta | Pooled 95% CI | Macro delta | Macro 95% CI |
|---|---:|---|---:|---|
| Ridge+chemical | -0.02870 | [-0.05457, -0.00321] | -0.01764 | [-0.03685, +0.00166] |
| Ridge+joint | -0.02286 | **[-0.04482, -0.00042]** | -0.02357 | **[-0.04572, -0.00233]** |
| Ridge+cross | -0.02135 | [-0.04658, +0.00573] | -0.02212 | [-0.04441, -0.00081] |

The direct paired joint-minus-chemical and cross-minus-joint bootstrap intervals **both include zero** on pooled and macro metrics. There is no credible evidence that manually engineered interaction products produce additional gains. All three blends are competitive and the simple joint-feature booster is a balanced experimental candidate. Picking chemistry-only by its best inspected development pooled number would be improper tuning.

## Context and limitations
Previously computed DeepDTA-inspired 10-epoch single-seed best development pooled RMSE approximately 1.37176; PerceiverCPI upstream short-run best approximately 1.43175. Conditions and compute budget are unmatched; no general superiority claim. The BALM public dataset lacks source assay DOI/method and contains inconsistent same-input labels. Protein graph components derive from approximate trigram similarity, not validated homology identity. The three overlapping CV folds and repeatedly inspected development set do not constitute an unbiased benchmark, and bootstrap uncertainty cannot correct repeated inspection. No reserved prospective test scoring and no approved scientific cohort. Only exploratory engineering evidence.

Scripts: scripts/ablate_balm_bindingdb_ensemble_interaction_controls_dev.py and scripts/bootstrap_balm_bindingdb_ensemble_controls_dev.py. They refuse to overwrite result JSON; archive outputs before deliberate reruns.
