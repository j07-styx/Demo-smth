# Structural cross-attention: first architecture pilot (development only)

**Change:** Added `StructuralCrossAttention`, which uses a compound query over the GVP-derived residue correction values with sequence token keys. The resulting compound-specific summary is projected and added to the compound representation before the frozen sequence foundation readout. This bypasses uniform-gate mean-cancellation without changing the original branch.

**Experiment:** Seed 1127; 486 training pairs across 9 proteins, 216 validation pairs across 4 proteins; identical selected DAVIS engineering cohort and frozen sequence checkpoint. Existing training data and checkpoints were not overwritten.

| Configuration | Best target-macro validation RMSE |
|---|---:|
| Frozen sequence-only baseline | 0.9256850780053539 |
| Earlier centered geometry, seed 1124 | 0.9256864253200320 |
| Structural cross-attention, seed 1127 | 0.9256850757253131 |

Structural cross-attention best at epoch 1; epoch 5 RMSE 0.9257069797512810, early stopping after four non-improving epochs. Peak CUDA memory: 469.06 MiB.

**Interpretation:** New branch trains end-to-end and supports structure-conditioned compound summaries, but improvement over the frozen baseline is ~2.28e-9 RMSE, not meaningful. Subsequent epochs degrade validation. This is not a scientific improvement, a held-out result, or proof of model superiority.

**Research direction:** The shared frozen foundation and 13-protein selected cohort may limit sensitivity. Next compare with structure-ablated controls and test whether a carefully constrained, independently validated readout can learn beyond baseline. Experimental construct identity and independent family-disjoint evaluation remain unresolved.

Local artifacts (not committed): `research/pilot_structural_cross_attention_dev/seed_1127/`.
