# Residue-level geometry fusion: real graph versus shuffled-node negative control

Implemented `StructuralResidueFusion`, an opt-in alternative to compound-query geometry attention. It computes centered GVP residue corrections and injects them into the residue tokens **before the frozen sequence foundation's protein readout**, while preserving the compound embedding. Missing graph returns the original residue tensor exactly. A unit test verifies finite outputs and nonzero gradients through the projection and GVP final layer.

The training experiment used the same seed-2103 numeric-only sequence checkpoint, 106 source-reconciled numeric-Kd training pairs, 71 numeric-Kd validation pairs, four fixed epochs, and identical initialization for real and shuffled graph conditions. Node scalar and vector features were permuted together, leaving topology and edges intact; this is a **partial** negative control.

| Epoch | Real geometry numeric-Kd pooled RMSE | Shuffled node-feature control | Frozen sequence |
|---|---:|---:|---:|
| 1 | 1.023889 | 1.023803 | 1.021684 |
| 2 | 1.026732 | 1.026414 | 1.021684 |
| 3 | 1.032082 | 1.031005 | 1.021684 |
| 4 | 1.022053 | 1.025237 | **1.021684** |

**Verdict:** At fixed epoch 4, real geometry beats shuffled features by about 0.00318 RMSE but **does not beat the frozen sequence baseline**. In earlier epochs shuffled features slightly outperformed real geometry. One seed and a repeatedly inspected, non-family-disjoint development split cannot establish useful structural generalization. No architecture superiority claim is justified.

Important scientific caveats: AlphaFold graph mappings are not verified against assay constructs; source blanks are not exact affinity values; original compound identity mismatches were excluded from this reconciled subset; no independent held-out benchmark is approved. This experiment isolates a new fusion pathway without changing production defaults.
