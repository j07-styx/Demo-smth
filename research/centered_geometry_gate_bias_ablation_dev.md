# Centered geometry gate-initialization ablation (development only)

This is a controlled engineering pilot, **not** a scientific benchmark or independent holdout.

- Fixed initialization seed: **1124**
- Same DAVIS selected development cohort: **486 train / 216 validation pairs**
- Frozen sequence-only target-macro RMSE: **0.9256850780053539**
- Original gate initialization bias: **-3.5**; best target-macro RMSE **0.9256864253200320** (epoch 1)
- Ablation gate initialization bias: **-1.0**; best target-macro RMSE **0.9256987248247740** (epoch 1)
- Difference ablation minus original: **+0.0000122995047420** (worse)
- Both stopped after epoch 5; validation RMSE worsened after epoch 1.

Only the gate bias and isolated output directory changed between scripts. A less negative bias initializes the sigmoid gate more open, but this experiment does **not** prove why performance deteriorated. No new independent evaluation or protein-disjoint split was used.

Next step: directly measure gate activations, residual magnitudes and per-protein prediction deltas, then test one motivated change at a time.

Local artifacts, intentionally not committed: `research/pilot_compound_conditioned_geometry_centered_gate_ablation_dev/seed_1124/`.
