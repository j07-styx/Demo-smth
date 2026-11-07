# Structural cross-attention warm-start ablation (development only)

**Hypothesis:** A stronger, initially nonzero GVP structural path might avoid weak gradients from the original zero-initialized GVP projection and small structural output scale.

**Intervention:** Isolated seed 1128, GVP final weight initialized N(0, 0.01), structural output projection initialized N(0, 0.02), scale 1.0 rather than 0.1. All other frozen foundation and selected DAVIS engineering cohort restrictions retained. This changes both seed and initialization/scale, so it is a screening experiment, **not a controlled matched-seed causal ablation**.

| Model | Best target-macro validation RMSE |
|---|---:|
| Sequence-only frozen baseline | 0.9256850780053539 |
| Original cross-attention seed 1127 | 0.9256850757253131 |
| Warm-start cross-attention seed 1128 | 0.9257089159519601 |

Warm-start best at epoch 1; by epoch 5 target-macro validation RMSE reached 0.9279702866639413, while training standardized MSE decreased from 0.7644294745944165 to 0.7641935453983982. Early stopping triggered at epoch 5. Peak CUDA memory 468.04 MiB.

**Interpretation:** Increased signal strength did not help on this selected engineering cohort and showed a widening train/validation gap. This may reflect overfitting or distribution mismatch but is not proof of either. Do not claim superiority or generality.

**Next:** Instrument gradient magnitudes and signal-to-prediction sensitivity; use matched-seed controls and independent protein-family holdout before further architecture selection.

Local training artifacts: `research/pilot_structural_cross_attention_warmstart_dev/seed_1128/` (not committed).
