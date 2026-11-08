# DeepDTA protein-component sampling intervention

A completed 10-epoch RTX 4060 experiment changed **only training sampling** relative to the normalized DeepDTA baseline. Instead of uniform shuffled samples, each training observation was sampled with replacement at probability proportional to `1/sqrt(training protein-component size)` (fixed sampler seed 2103). The training split, held-out protein-component inner-development split, DeepDTA architecture, label normalization, AdamW lr=0.0003, batch size 128, epoch count and primary model seed were retained. The resampling changes both the training data frequency and optimizer minibatch order; thus the effect cannot be separated from stochastic order using one seed.

| Experiment | Best observed inner-dev RMSE | Epoch-10 RMSE |
|---|---:|---:|
| Uniform DeepDTA | 2.224241 (epoch 6) | 2.387794 |
| Inverse-sqrt component sampling DeepDTA | **2.107162 (epoch 1)** | 2.381689 |
| Train-only global mean | 1.803902 | 1.803902 |

The component-rebalanced training run improved best-observed inner-development RMSE by 0.117080 (5.26%) compared with the uniform baseline, but this was an epoch-selected exploratory metric, not a final-epoch improvement (final-epoch RMSE differs by only 0.006105). The rebalanced model still underperforms the train-mean comparator, and its training MSE fell from 0.5105 to 0.1669 while validation RMSE fluctuated between 2.107 and 2.576, consistent with unstable generalization. One seed is insufficient to claim robustness.

**Decision:** keep as a promising training intervention, not a promoted model or publication-quality result. Next require multiple seeds and fixed selection policy, component-macro evaluation and held-out component uncertainty. No prospective test was accessed. Assay/construct source approval remains blocked.
