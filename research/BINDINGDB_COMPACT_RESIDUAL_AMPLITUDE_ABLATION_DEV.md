# Compact compound-protein CNN: residual amplitude ablation

Completed **two additional 10-epoch RTX 4060 training runs**, seed 2103 and 2104, on the frozen provisional 27,118 training / 7,387 inner-dev pair split. Architecture is the compact 250,753-parameter dual-CNN with dropout 0.35, inverse-square-root component sampling, train-only normalization, and output `1.5*tanh(raw)` in standardized target units. The prior model used `0.5*tanh(raw)`; seed 2103 is a controlled amplitude comparison. Seed 2104 at amplitude 0.5 has not yet been run.

| Model | Seed | Best observed inner-dev RMSE | Epoch-10 RMSE |
|---|---:|---:|---:|
| Compact CNN, amplitude 0.5 | 2103 | **1.988632** | **2.048621** |
| Compact CNN, amplitude 1.5 | 2103 | 2.253713 | 2.653777 |
| Compact CNN, amplitude 1.5 | 2104 | 2.006732 | 2.400142 |
| Train-only global mean | — | **1.803902** | **1.803902** |

The wider correction range improves training loss substantially (seed 2103 final training MSE 0.2349 versus 0.6603 for amplitude 0.5), but harms held-out protein development performance. This is consistent with increased overfitting, though the amplitude-1.5 results vary substantially between seeds. The stronger prior is not proven optimal. All results are exploratory; development has been repeatedly inspected, no reserved test accessed, and assay/construct QC is incomplete.
