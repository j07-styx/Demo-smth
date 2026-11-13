# Joint sequence + structure ridge probe — 13 November 2026

ENGINEERING ONLY, exploratory TRAIN-only nested group cross-validation. Same 5,808 rows, 253 groups, five outer folds and three inner folds. No reserved test access.

| Model | Pooled RMSE | Group-macro RMSE |
|---|---:|---:|
| Strong ESM-2 interaction baseline | 1.520691 | 1.325041 |
| Baseline + duplicate ESM protein block | 1.523027 | 1.326797 |
| Baseline + real SaProt protein block | 1.521185 | 1.314274 |
| Baseline + shuffled SaProt protein block | 1.527305 | 1.330895 |

The real joint model improves macro RMSE by 0.010767 (0.81%) relative to the strong sequence baseline while pooled RMSE is marginally worse by 0.000494 (0.03%). Conditional paired group-bootstrap 95% intervals: macro [-0.029351,+0.007495], pooled [-0.021483,+0.021797]. All pairwise intervals against sequence, duplicate ESM and shuffled controls include zero. No established independent 3D advantage.

## Exact design
The base is the earlier shared ridge features plus ESM-2 PCA32 and compound-SVD32 x ESM-PCA32 products, fixed at feature scale .3. Its out-of-fold predictions exactly reproduce the earlier capped ESM-2 model (max absolute error 0). An added 32-dimensional protein-only block comes from real SaProt, shuffled SaProt, or the same ESM-2 features. Inner group-macro selection chooses added-block scale {0,.1,.3}; ties favor lower scale. Every fit uses its own training-only vocabulary, scaling, PCA and SVD. This is one jointly fitted ridge model, not a post-hoc average of predictions. Adding a block refits all coefficients.

The duplicate ESM block controls for feature duplication and changed effective regularization. It adds no new representation. Real structure is selected at nonzero scale in all five folds (.3,.3,.1,.3,.3), shuffled in two, duplicate ESM in one. This selection pattern is descriptive and cannot replace outer performance. Real joint macro improves in 4/5 outer folds versus sequence and 5/5 versus shuffled; 133/253 groups improve versus sequence. Five groups account for 33.6% of absolute group SSE difference versus sequence.

The extra structural block remains protein-only. Its own coefficients express additive target effects; this does not demonstrate ligand-pose or local binding-interaction learning. Whole-protein contextual representation, pretraining confounding and scrambled-token distribution shift remain limitations.

## Implementation and validation
scripts/evaluate_joint_structure_dev.py and scripts/crossvalidate_joint_structure_dev.py preserve the established transformation code but add the fixed ESM interaction block before testing an extra protein block. In machine-readable results, baseline means strong ESM-2 and esm2_sequence means the duplicate ESM control; saprot_real/shuffled denote joint models. Inherited generic design text must be read with the explicit base_esm_scale and readout fields.

All 5,808 rows occur exactly once in outer evaluation; every group occurs in one outer fold. Independent validation reproduces all metrics, rejects duplicated/missing rows and cross-fold group contamination, and verifies exact strong-baseline reproduction. Source compilation checks pass. Arrays, labels and fitted data remain outside Git.

The protocol was chosen after examining earlier TRAIN results. Bootstrap intervals are conditional on saved CV fits, unadjusted for the accumulated development search, and not confirmatory. This improves a development point estimate for equal-weighted protein groups, not pooled accuracy or a held-out-test claim.

Next decision: retain the strong sequence model as the serving default. Freeze this joint candidate for later independent evaluation only after the broader study protocol and cohort are ready. Further tuning on these same folds cannot establish superiority.
