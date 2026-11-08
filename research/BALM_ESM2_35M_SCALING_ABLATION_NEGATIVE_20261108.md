# Frozen ESM2 35M versus ESM2 8M: alignment/scaffold-cold BALM TRAIN benchmarks

**Date:** 2026-11-08. **Status:** fully executed exploratory negative scaling ablation, no independent test.

## Extracted representations

Downloaded pretrained ESM2 t12 35M (33,501,394 parameters) and encoded all 639 distinct BALM frozen TRAIN proteins using the RTX 4060. Frozen weights, layer 12, 480-d non-special residue mean pooled embeddings, first 1022 amino acids. As in the earlier 8M cache, 85 long proteins were truncated, not represented at full length. No original frozen dev or prospective test sequences/labels used. Local compressed binary cache and pretrained weights remain UNTRACKED; the tracked manifest records encoder weight and embedding-cache SHA256 hashes, dimensions, and process.

## Controlled architecture comparison

Use the SAME four Smith-Waterman-alignment protein-group and strict Bemis-Murcko scaffold-cold folds for both 40% and 30% local alignment identity (each 80% shorter-sequence coverage). All 15,538 original BALM TRAIN records held out exactly once per rule; zero shared alignment group or Murcko core between each fold fit/holdout, including common acyclic scaffold group. Fit each fold using 3,904–5,676 unique averaged protein/compound pairs.

Reference model: 75% sparse Ridge on chiral Morgan2048, TRAIN-fitted 3/4-mer protein TF-IDF and ESM2 protein embedding (scaled 0.25), plus 25% unchanged joint RDKit molecule descriptor/amino-acid composition gradient boosting. Do not change any booster weights or fixed training hyperparameters. Previously selected train-nested shrinkage beta is inherited exactly per outer fold, with no new outer-label tuning.

Candidate protein representation in RIDGE only:
- **ESM2 8M:** precomputed 320-dimensional L2-normalized frozen protein vector.
- **ESM2 35M:** corresponding 480-dimensional frozen vector, same scale.
- **8M + 35M fusion:** concatenate both unit vectors each divided by sqrt(2), preserving total protein representation norm and same Ridge scaling 0.25.

All three candidates share the same chemical features, same fold-train only protein k-mer vocabulary and exact same gradient booster. Candidate comparisons are paired on the same heldout rows.

## Out-of-fold results

| Encoder inside ensemble | 40% pooled RMSE | 40% component-macro RMSE | 30% pooled RMSE | 30% component-macro RMSE |
|---|---:|---:|---:|---:|
| **8M reference** | **1.430266** | **1.337548** | 1.460624 | 1.379023 |
| 35M | 1.431878 | 1.341952 | 1.460585 | **1.377991** |
| 8M+35M fusion | 1.431759 | 1.339541 | **1.460293** | 1.378372 |

The 35M and fusion candidates do NOT yield a consistent improvement across both protein identity cutoffs or metrics. Under 40% identity, 35M macro delta +0.004404 versus 8M has paired 5,000-component-bootstrap percentile 95% interval **[+0.000539,+0.008386]**, favoring the SMALLER encoder. The fusion macro delta +0.001993 interval **[+0.000213,+0.003792]** also favors 8M. Pooled 40% differences have intervals crossing zero.

At 30% identity, both candidates' apparent pooled/macro gains are tiny. For 35M-minus-8M, pooled delta -0.000039, 95% interval [-0.011322,+0.008527]; macro delta -0.001032, interval [-0.005417,+0.003516]. For fusion-minus-8M, pooled delta -0.000331, interval [-0.004964,+0.003207], macro delta -0.000651, interval [-0.002482,+0.001284]. All include zero.

**Decision: retain ESM2 8M as the more efficient, better-supported reference.** More encoder capacity does not establish more robust cold-start affinity prediction here. The model still has not achieved a robust pooled-RMSE win against a train-fold mean when stricter protein homology proxies and scaffold novelty are enforced.

## Reproducibility and limitations

Scripts: scripts/cache_balm_train_only_frozen_esm2_35m_dev.py and scripts/compare_balm_esm2_8m_vs_35m_alignment_cold_dev.py (run for identity30_cover80 and identity40_cover80). Outputs research/balm_esm2_8m_vs_35m_fusion_sw_identity30_cover80_scaffold_cold_traincv_dev.json and its identity40 counterpart. Checksums in research/balm_esm2_t12_35m_train_only_feature_manifest_dev.json. Tests: tests_v4/balm_esm35m_fusion_alignment_test.py.

Source BALM lacks assay DOI, construct and method information and contains discordant repeated-input labels; protein groups use local alignment-derived homology PROXIES, not validated orthology, and Murcko scaffold disjointness does not remove all chemical analogs. This is repeated exploratory TRAIN-only testing, with bootstrap uncertainty omitting prior model-selection history. Formal scientific source approval remains blocked and no reserved prospective test evaluated. No claim of beating fully replicated PerceiverCPI/DeepDTA.
