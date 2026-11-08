# Bounded-residual compact DeepDTA — completed architecture experiment

Implemented a dual convolutional compound/protein model with the same basic sequence encoders but a compact 256→128 head, dropout 0.35 and a bounded standardized residual output `0.5*tanh(raw)`. The prediction is re-centered on the train-only pKd mean and standard deviation. This is a deliberate strong-prior architecture, not a faithful DeepDTA reproduction.

On the frozen provisional 27,118-train / 7,387-inner-dev split, seed 2103, inverse-square-root protein-component sampling, 10 RTX 4060 epochs:

| Metric | Result |
|---|---:|
| Parameters | 250,753 |
| Best observed inner-dev pooled RMSE | 1.988632 (epoch 3) |
| Epoch 10 pooled RMSE | 2.048621 |
| Train-only mean baseline | **1.803902** |
| Best previously observed component-sampled DeepDTA (seed 2104) | 1.956261 |

The bounded residual head narrows epoch-to-epoch fluctuations (epochs 3–10 within 1.989–2.049), but **does not beat the mean baseline or the best prior neural result**. The hard residual cap also limits the possible affinity correction to ±0.5 train-standard-deviation units, so it may underfit. A separate controlled ablation is required to isolate the effects of compact head, dropout and residual bound. Development set has been inspected repeatedly; no independent test accessed; assay and construct QC remain provisional.
