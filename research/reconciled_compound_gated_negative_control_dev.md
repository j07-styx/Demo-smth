# Compound-conditioned geometry gate: matched real-versus-shuffled development experiment

This experiment tests the existing `dynacpi.compound_conditioned_geometry.CompoundConditionedGeometry` module as an alternative to earlier residue-level fusion and cross-attention. The module generates per-compound, per-residue sigmoid gates from the compound vector, sequence token, and GVP residual. Geometry is injected before the frozen sequence foundation's protein readout. Initial gate bias -3 reduces perturbation of the pretrained sequence prediction.

**Fixed protocol:** seed 2103; frozen numeric-only sequence checkpoint; 106 measured numeric-Kd training pairs, 71 measured numeric-Kd validation pairs; four epochs; learning rate 3e-4; fixed epoch-4 comparison. Negative control permutes graph node scalar/vector features together but retains graph edges and connectivity, so it does not eliminate all structural information. Both arms use the same random seed, code path, and hyperparameters.

| Epoch | Real compound-conditioned geometry pooled RMSE | Shuffled node features pooled RMSE | Frozen sequence pooled RMSE |
|---|---:|---:|---:|
| 1 | 1.021684350 | 1.021683939 | 1.021683942 |
| 2 | 1.021705619 | 1.021684197 | 1.021683942 |
| 3 | 1.022020113 | 1.021721796 | 1.021683942 |
| 4 | 1.023292454 | 1.022964573 | **1.021683942** |

**Conclusion:** the real-graph branch does not improve over the frozen sequence baseline and at fixed epoch 4 underperforms the shuffled-node control. The training loss is essentially flat. Do not interpret this as a general statement that 3D structure is unhelpful; this is a tiny repeatedly inspected development cohort with incomplete structural provenance, not a family-disjoint test. No independent benchmark improvement or PerceiverCPI superiority is established.

Research implementation implication: prioritize source-verified training labels, independent cold-protein evaluation, and controlled protein/compound representation ablations before adding more structural modules. The base architecture and checkpoints remain unchanged.
