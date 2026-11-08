# BALM nested dual-cold mean-shrinkage experiment — 2026-11-08

**Status:** Positive TRAIN-only exploratory nested out-of-fold experiment, not an independent benchmark.

We conducted four outer GroupKFold protein graph-group splits of the 15,538 BALM frozen TRAIN rows across 519 protein components. In each outer split we excluded all training rows whose canonical RDKit isomeric SMILES matches any heldout compound, then collapsed repeated identical protein/SMILES training pairs into one averaged label (4,425–5,199 fit pairs per fold). There was zero canonical-compound overlap between each fold's training and holdout sets.

Our base is 75% Morgan-2048/TF-IDF-protein Ridge (alpha 1, protein scale .25) plus 25% ordinary joint compound-descriptor/protein-composition HistGradientBoosting. Its predictions were shrunk toward the *corresponding outer fold's train-label mean*. For each outer fold, three inner GroupKFold protein-component splits of the outer TRAIN portion, with chemical identity exclusion applied anew to inner training, selected beta from predeclared [0, .25, .5, .75, 1]. Both average inner pooled and inner macro RMSE had to beat the inner train-mean comparator, then the balanced relative score selected beta. No frozen development or reserved test outcomes were fitted, selected or scored.

Outer-fold chosen betas: **0.75, 1.0, 0.75, 0.75**.

## Out-of-fold results (all 15,538 original TRAIN outcomes scored once)

| Predictor | Pooled RMSE | Protein-component macro RMSE |
|---|---:|---:|
| Fold train-only mean | 1.445091 | 1.355613 |
| Sparse Ridge | 1.488583 | 1.381514 |
| Unshrunk ordinary joint ensemble | 1.424463 | 1.316399 |
| **Nested-selected, mean-shrunk joint ensemble** | **1.402154** | **1.298593** |

Nested shrinkage improves pooled RMSE **1.57%** and macro RMSE **1.35%** against the unshrunk ensemble; **2.97% pooled** and **4.21% macro** against fold mean, as point estimates.

## Paired uncertainty: 5,000 group bootstrap replicates

Differences are nested-selected RMSE minus comparator RMSE; percentile 95% intervals resample 519 heldout protein graph groups.

| Comparator | Pooled difference | Pooled interval | Macro difference | Macro interval |
|---|---:|---|---:|---|
| Unshrunk joint ensemble | **-0.022309** | **[-0.033626,-0.010945]** | **-0.017806** | **[-0.027471,-0.007490]** |
| Fold train mean | -0.042937 | [-0.094107,+0.009664] | **-0.057020** | **[-0.094249,-0.021623]** |
| Sparse Ridge | -0.086429 | [-0.118294,-0.055878] | -0.082921 | [-0.099821,-0.066098] |

The improvement over unshrunk ensemble is supported by both sampled group intervals. **Pooled improvement over training mean remains uncertain because the 95% interval includes zero.**

## Reproduction and limitations

Code: scripts/train_balm_nested_dual_cold_mean_shrinkage_dev.py. Authoritative result: research/balm_bindingdb_nested_dual_cold_mean_shrinkage_paired_bootstrap_dev.json. Tests: tests_v4/balm_nested_dual_cold_shrinkage_test.py. Scripts refuse accidental overwrite. A preliminary same-score run had an incomplete control-bootstrap table and remains intentionally local, not committed.

This challenge used only frozen TRAIN records. Its models and beta candidates follow prior exploratory development, so it cannot retroactively provide unbiased final performance. BALM has missing original assay conditions/DOI and conflicting repeated identical-input labels. Protein components are approximate trigram similarity graphs, not validated homology clusters; scaffold similarity may persist despite canonical-compound exclusion. No scientific cohort approval. **No reserved test evaluation, and no established PerceiverCPI superiority.**
