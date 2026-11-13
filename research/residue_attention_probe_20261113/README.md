# Ligand-conditioned residue attention pilot — 13 November 2026

ENGINEERING ONLY. Completed 40 fits: five TRAIN protein-group folds, two seeds, four arms. Reserved test untouched. All 5,808 out-of-fold predictions cover 253 groups. This is a bounded, short-training exploratory experiment on the repeatedly inspected TRAIN cohort.

| Model (two-seed prediction average) | Pooled RMSE | Group-macro RMSE |
|---|---:|---:|
| Shared ridge baseline | 1.556304 | 1.362221 |
| ESM-2 residue attention | 1.553666 | 1.350400 |
| Real SaProt residue attention | 1.539896 | 1.337485 |
| Shuffled SaProt residue attention | 1.566139 | 1.346996 |
| Real SaProt uniform pooling | 1.534368 | 1.338142 |

Real minus uniform pooling pooled delta +0.005528, conditional 95% paired group-bootstrap interval [-0.000721,+0.012377]; macro -0.000657 [-0.005854,+0.004496]. Real minus sequence-attention pooled -0.013769 [-0.030267,+0.002554]; macro -0.012915 [-0.026203,+0.000593]. Real minus shuffled pooled -0.026243 [-0.058009,+0.005675]. These comparisons do not establish an attention benefit or confirmed geometry superiority.

## What changed
Cached up to 96 uniformly spaced contextual residue embeddings per protein from the same frozen 35M SaProt and ESM-2 checkpoints, with identical positions across arms. Full-residue averages reproduced prior whole-protein caches with maximum errors below 6e-6. These are residue-level features, not verified pocket features or docked ligand contacts. Nonoverlapping 510-residue foundation-model windows remain unchanged.

A direct fingerprint path supplies a 32-dimensional compound representation. Residue features project to 32 dimensions. Compound queries attend over residue keys, then the head receives compound features, residue mean, attended context and a compound/context product. Uniform pooling replaces attention weights with equal valid-residue weights while retaining the same head inputs and allocated parameter count (query/key parameters are unused in that control). No pretrained encoder fine-tuning.

The head predicts a correction bounded at +/-0.25 raw affinity units on top of the shared ridge baseline. Training targets are residuals to three-fold group-cross-fitted ridge predictions generated entirely inside each outer training partition. Ridge, feature normalization and target information never use outer evaluation labels. Fixed five epochs, maximum 64 batches per epoch, batch size 32, AdamW lr .0003, decay .01, gradient clipping 1. Final epoch only; no epoch or seed selection.

## Finding
Real SaProt attention has effective residue coverage 91.3%-97.8%, averaging 95.2% across the ten fold/seed runs. It remains broad. Uniform pooling has slightly better pooled RMSE and essentially identical macro RMSE. Thus this pilot does not show that learned ligand-conditioned localization adds predictive value over averaging.

The regularized ridge experiment from v5.5 remains stronger: capped ESM-2 interaction ridge pooled RMSE 1.520691, real SaProt 1.529681. Those models have different training procedures; this is a practical performance reference, not a controlled isolated comparison of attention versus ridge.

Do not infer that attention cannot work, that 3D is useless, or that it found binding sites. Five epochs, two seeds, uniform residue subsampling, frozen representations and bounded corrections limit this negative result. Further work should target genuine pocket information or external interaction supervision rather than increase global attention complexity without evidence.

## Validation and artifacts
Synthetic model checks pass: consistent token permutation invariance, masked-residue invariance, compound-dependent attention, exact uniform weights, nonzero query gradients and correction bounds. The independent result audit reproduces every seed and ensemble metric, verifies all corrections within +/-0.25, checks all 40 fold/seed/arm combinations, and exactly matches the earlier ridge baseline predictions (max error 0).

Source: scripts/cache_residue_probe_dev.py, scripts/train_residue_attention_probe_dev.py, scripts/validate_residue_attention_probe_dev.py. All require explicit cache/bundle/output arguments. Cache extraction uses existing verified checkpoint hashes and Transformers dependencies. Training uses two CPU threads and CUDA when available with a 25% process allocator limit. Weights, residue arrays, labels and per-row predictions remain outside Git; aggregate results, protocol and validation are saved here. Original model and demo defaults remain unchanged.
