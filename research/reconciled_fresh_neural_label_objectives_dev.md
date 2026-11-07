# Reconciled DAVIS fresh neural training: mixed versus numeric-only labels

Two new SequenceFoundation models were **randomly initialized and trained** for four epochs on the separate source-reconciled development subset. They used the same architecture and optimizer family, but different training labels and seeds. Mixed-label model: seed 2101, all 450 training pairs. Numeric-only model: seed 2102, only 106 primary numeric-Kd training pairs. Both evaluated on the same 200 previously inspected development validation rows; **no independent holdout**. This is a hypothesis-generating comparison, not a matched-seed ablation, and not a structure-aware DynaCPI win.

| Model | Numeric Kd validation RMSE, 71 pairs | Screening-negative validation RMSE, 129 pairs | Best overall target-macro RMSE among four inspected epochs |
|---|---:|---:|---:|
| Train-only compound average | 1.447462 | 0.352363 | 0.836518 |
| Fresh sequence, mixed training labels, epoch 4 | 1.643771 | 0.271401 | 0.913600 |
| Fresh sequence, numeric-only training labels, epoch 4 | **1.026294** | 1.230227 | 1.088122 |

**Interpretation:** Numeric-only training gives a strong *development-only* signal on measured affinities: its last-epoch numeric Kd RMSE is about 29% lower than the mixed-label compound-average baseline, while screening-negative error worsens sharply. This is consistent with conflicting label objectives, but does not prove causation. Seeds differ, epoch selection is not training-only, and the numeric-only model has fewer training rows. The mixed-label model remains better on screening-negative rows. Source screening negatives are not exact numeric Kd measurements. No experimental construct identity or protein-family-disjointness has been verified.

**Follow-up:** repeat matched seeds for both training objectives; use training-protein-only model selection; validate primary assay semantics; create an approved independent cohort; then test whether geometry adds reproducible benefit. Do not use the current best-of-four development metric as a paper benchmark.

Reproduce using `python scripts/train_reconciled_clean_sequence_seed_2101_dev.py sequence` and `python scripts/train_reconciled_numeric_only_sequence_seed_2102_dev.py sequence` **only in fresh isolated output directories** (both scripts intentionally refuse to overwrite existing checkpoints); inspect with `python scripts/compare_reconciled_fresh_training_dev.py`. Checkpoints and local predictions are deliberately excluded from Git.
