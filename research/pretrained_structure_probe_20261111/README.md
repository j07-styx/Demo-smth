# Frozen pretrained structure probe — 11 November 2026

ENGINEERING ONLY. This uses 5,808 rows from the frozen BALM TRAIN cohort, 298 proteins and 253 groups. The reused internal holdout has 826 rows and 50 groups; 4,982 rows fit the models. The reserved test was not loaded or scored.

## Results
| Arm | Pooled RMSE | Group-macro RMSE |
|---|---:|---:|
| Shared ridge baseline | 1.480541 | 1.267409 |
| ESM-2 35M sequence | 1.478252 | 1.266147 |
| SaProt 35M real AA+3Di | 1.409843 | 1.230320 |
| Same SaProt, shuffled 3Di | 1.504710 | 1.240530 |

Real SaProt reduces pooled RMSE by 4.78% against the shared baseline. However, all paired 95% group-bootstrap intervals cross zero. Real minus ESM-2 pooled delta is -0.068409 [-0.143502, +0.027695]; real minus shuffled is -0.094868 [-0.206812, +0.011850]. The latter macro delta is only -0.010210 [-0.055054, +0.038326]. This is a promising exploratory point estimate, not an established independent structural advantage.

## Design and interpretation
Pinned public SaProt_35M_AF2 and ESM2_t12_35M_UR50D checkpoints are frozen. Foldseek version 39b02b9fd8fea53a26a13ce638bfda616a0e2003 generated full-reference 3Di tokens; exact residue mapping and pLDDT>=70 masking precede token assembly. The earlier temporary executable was missing, so the binary was restored under the persistent original-workspace data/tools directory. Its version differs from the earlier download; the actual version used is preserved in feature_provenance.json.

All 298 proteins were encoded in each arm. Shuffling preserves amino acids, structure-token composition and confidence-mask positions. Validation checks reject deliberate amino-acid, masking and composition corruption and verify feature SHA256 hashes, ordering, finite values, and 298x480 dimensions. All 298 proteins have changed 3Di arrangements.

Each encoder uses nonoverlapping 510-residue windows and residue-weighted final-layer mean pooling. The readout shares Morgan fingerprints, sequence TFIDF, mask fraction and log sequence length. Encoder features are reduced to 32 dimensions and combined with 32 compound dimensions through an explicit outer product. Every fitted transform uses only inner-fit data. Three grouped inner folds select feature scale from {0, .1, .3, 1}; all three arms independently selected .3. Ridge alpha is fixed at 1. No final-holdout epoch or scale selection occurs.

The baseline differs slightly from the previous 1.489130 baseline because every arm now shares confidence/length covariates and a tighter ridge solver tolerance. Do not compare it as an unchanged baseline.

The new evidence narrows the diagnosis: pretrained structural representations plus a compound interaction readout can produce a useful point estimate where scratch-trained pooled descriptors did not. It does not isolate pretraining versus architecture, establish a physical binding mechanism, or reproduce full GenSPARC. SaProt vs ESM-2 also differs in pretraining. Within-SaProt shuffling can be out of distribution; it is a sensitivity control, not proof of causal geometry usefulness.

## Reproduction
Use scripts/cache_pretrained_structure_dev.py with --source-workspace, --bundle-dir, --out, --foldseek (persistent Linux path), and --device cuda. The pinned model revisions, file hashes, PDB hashes and tokenization choices are in feature_provenance.json. Transformers 4.44.2 is installed in the original workspace data/tooldeps_chemberta. Foldseek runs through WSL Ubuntu.

Then run scripts/validate_pretrained_structure_dev.py --features CACHE_DIR and scripts/evaluate_pretrained_structure_dev.py --bundle-dir BUNDLE_DIR --features CACHE_DIR --out NEW_RESULT_DIR. Evaluation refuses to overwrite an existing output directory. Source scripts and aggregate results are versioned; raw feature arrays, tokens, model weights, labels and per-row predictions stay outside this repository.

## Next discriminating experiment
Freeze these choices and run outer protein-group cross-validation confined to the TRAIN cohort, with the same inner selection and three encoder arms. Report pooled and macro results with paired group uncertainty and per-group concentration. This tests whether the point estimate survives a different allocation of proteins before any reserved-test use. If it persists, investigate residue-level ligand-conditioned readout and fine-tuning as separate ablations. Do not promote this exploratory model to the demo default yet.
