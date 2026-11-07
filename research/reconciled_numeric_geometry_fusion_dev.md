# Numeric-Kd-only structural fusion against a matched frozen sequence baseline

Ran two new **structural cross-attention** geometry-branch experiments on the primary-reconciled DAVIS development cohort, using the same frozen numeric-only sequence checkpoint from seed 2103, 106 numeric-Kd training pairs, and 71 numeric-Kd validation pairs (the other 129 validation screening-negative records were excluded from the scored metric). Four fixed epochs, no independent holdout; only the geometry branch is trained. AlphaFold structure mappings are sequence-exact but **experimental constructs remain unverified**.

| Experiment | Numeric validation pooled RMSE epoch 1 | epoch 4 | Frozen sequence baseline |
|---|---:|---:|---:|
| Low-gain structural attention (scale 0.1, initial projection std 0.001, lr 5e-5) | 1.021684 | 1.021684 | 1.021684 |
| High-gain structural attention (scale 1.0, projection std 0.05, lr 1e-3) | 1.021713 | **1.064493** | 1.021684 |

The low-gain branch is functionally inert at the precision of this metric; high gain perturbs predictions and **worsens** numeric affinity error by epoch four. Neither variant improves the frozen sequence baseline. The 106/71 numeric pairs are drawn from nine training and four validation proteins, respectively; the source kinase family STE overlaps across splits. These results do not support a structural benefit and are not independent scientific benchmarks. The high-gain run is an exploratory sensitivity test, not a validation-selected model. The original run manifests were written before correcting a display-only `val_pair_count` bug (they show 200 overall validation rows, not the 71 actually evaluated); the source code now reports the scored 71 correctly. No source data or checkpoints were overwritten.

Next engineering question: use explicit gradient and attention/residual magnitude diagnostics to test why the low-gain branch is effectively inert, then assess whether any geometry gain is robust to graph shuffling and missing-graph negative controls. Do not add structural complexity without a validated gain.
