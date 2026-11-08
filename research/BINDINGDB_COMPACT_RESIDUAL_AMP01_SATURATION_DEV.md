# Compact CNN residual amplitude 0.1: constant-output warning

Two RTX 4060 ten-epoch runs on frozen provisional train/inner-dev, seeds 2103 and 2104, use the same 250,753-parameter compact CNN with `0.1*tanh(raw)` output and inverse-square-root protein-component sampling. Both produced **identical inner-dev RMSE 1.829465811153061 for all 10 epochs**, despite varying training minibatch losses. This is strong evidence of output saturation / near-constant predictions, not successful generalization. Exact output saturation has not been directly verified from per-sample predictions.

| Configuration | Seeds | Best RMSE | Epoch 10 RMSE |
|---|---|---:|---:|
| Amplitude 0.1 | 2103, 2104 | 1.829466 each | 1.829466 each |
| Amplitude 0.5 | 2103, 2104 | 1.988632, 1.925573 | 2.048621, 1.986141 |
| Amplitude 1.5 | 2103, 2104 | 2.253713, 2.006732 | 2.653777, 2.400142 |
| Train-only global mean | — | **1.803902** | **1.803902** |

**Interpretation:** stronger shrinkage approaches a trivial baseline but does not beat it. A saturated tanh output is a poor architecture for learning new compound-protein interactions. These are repeatedly inspected exploratory development metrics, not independent test results; assay/construct QC incomplete.
