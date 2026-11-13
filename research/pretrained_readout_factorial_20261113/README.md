# Readout and feature-strength factorial — 13 November 2026

ENGINEERING ONLY; exploratory follow-up designed after inspecting the prior TRAIN cross-validation. No reserved test was read. All four cells use the same five outer group folds and three inner folds. The shared ridge baseline is identical across cells: pooled RMSE 1.556304, group-macro RMSE 1.362221.

## Results
Numbers are pooled / group-macro RMSE over all 5,808 out-of-fold predictions.

| Added pretrained block | Maximum scale | ESM-2 | Real SaProt | Shuffled SaProt |
|---|---:|---:|---:|---:|
| Protein + compound products (previous) | 1.0 | 1.548379 / 1.335627 | 1.569070 / 1.345643 | 1.561716 / 1.341636 |
| Protein + compound products | 0.3 | 1.520691 / 1.325041 | 1.529681 / 1.320468 | 1.561716 / 1.341636 |
| Protein only | 1.0 | 1.545529 / 1.343248 | 1.530454 / 1.324015 | 1.573216 / 1.348142 |
| Protein only | 0.3 | 1.545529 / 1.343248 | 1.532437 / 1.323140 | 1.573216 / 1.348142 |

Protein-only refers only to the added pretrained block. Every model retains the same compound fingerprints and sequence baseline. With this additive ridge readout, that extra block can only produce protein main effects; it cannot supply compound-specific structural corrections.

## What this isolates
1. Strong explicit compound-product features were unstable. Excluding scale 1 improves real SaProt pooled RMSE from 1.569070 to 1.529681 (2.51%). The previously difficult fold improves from 1.755689 to 1.591912. ESM-2 also improves, so this is not uniquely a geometry defect.
2. Compound products are not clearly necessary for SaProt's current benefit. Removing them achieves 1.530454, nearly the capped interaction result 1.529681. This does not prove all interaction mechanisms fail; only this frozen pooled PCA/product readout was tested.
3. Structural correspondence has a stronger signal in the simple additive readout. Protein-only, max .3: real minus shuffled pooled delta -0.040778, conditional 95% group-bootstrap CI [-0.074428,-0.007199]; macro -0.025002 [-0.049271,-0.001170]. Real beats shuffled pooled RMSE in 5/5 folds, with 134/253 groups improving. These are unadjusted exploratory intervals on a reused cohort, not a confirmatory discovery.
4. Superiority over sequence is not established. Capped interaction real minus ESM-2: pooled +0.008990 [-0.024593,+0.042948], macro -0.004573 [-0.027922,+0.018124]. Protein-only max 1 real minus ESM-2 pooled -0.015075 [-0.056720,+0.023883]. Comparing each family's best observed cell is itself development selection.

## Implementation and validation
The evaluator now accepts --readout interaction|protein and --max-scale .3|1.0, preserving prior defaults. Scale is selected within inner folds from {0,.1,.3} or {0,.1,.3,1}; zero means exact shared-baseline fallback. All PCA, SVD, scaling and vocabulary fits remain training-only. Maximum scale is not a prediction cap.

scripts/run_pretrained_readout_factorial_dev.py locks the factorial before execution, reuses the saved original cell, and runs 15 additional outer-fold evaluations. scripts/validate_pretrained_cv_dev.py validates every new cell: 5,808 rows exactly once, 253 groups each in one evaluation fold, metrics independently reproduced, and three deliberately invalid partitions rejected. Cross-cell row order and baseline predictions must match within absolute tolerance 1e-7. Feature hashes are checked against provenance. No GPU training or unrelated process termination.

Some inherited per-fold free-text design descriptions refer generically to the original interaction design; the explicit readout field records whether products are present. The code's protein branch returns only the 32 protein dimensions; interaction returns 32 plus 1,024 products.

## Reproduction and limits
Run scripts/run_pretrained_readout_factorial_dev.py with --bundle-dir, --features, --previous-cv and a fresh --out directory. Aggregate and per-fold JSON are versioned here; weights, labels and raw predictions remain outside Git. Previous cell is research/pretrained_structure_cv_20261111.

The evidence supports keeping a simple additive structure feature as a diagnostic reference, while investigating local residue representations rather than adding more global compound products. A future local-attention experiment must beat both this additive structure model and the matched sequence model. Whole-protein pooling, a single shuffle realization, pretraining overlap and unverified assay constructs remain limitations. Do not replace the demo default or claim independent 3D superiority.
