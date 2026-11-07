# Does frozen protein similarity improve chemical transfer?

Fixed training-only leave-one-protein-out experiment over nine target identifiers and 106 numeric observations. Each fold trains on eight proteins and scores the ninth. Mean ESM embeddings define a protein RBF kernel, with bandwidth derived exclusively from training target embeddings. Ridge alpha is fixed at 1. No hyperparameter search or validation scoring occurs.

| Model | Target-macro RMSE |
|---|---:|
| Chemical Tanimoto kernel | 0.8540 |
| Protein RBF kernel | 0.8506 |
| Product of chemical and protein kernels | 0.8813 |
| Equal mixture of chemical and product kernels | 0.8651 |
| Same mixture with shuffled protein embeddings, mean of 20 controls | 0.8470 |

The hybrid worsens RMSE by 0.0111 relative to chemistry alone. Its target-bootstrap delta interval [-0.0108, 0.0351] spans zero and only four of nine targets improve. Shuffled controls outperform the real hybrid on average. Thus this experiment does not support the proposed mean-ESM similarity fusion. The protein-only model ignores compound identity; its similar aggregate error is a diagnostic limitation, not grounds to promote it as a CPI model.

This tests one fixed similarity construction and regularization, not every possible use of protein representations. It does not establish that proteins are irrelevant. The small numeric-only dataset and homology dependence limit inference. Shuffling is a negative control, not a candidate model to deploy. No independent test is touched and no existing checkpoint changes.

Do not compare these absolute scores directly against the previous support-transfer experiment: that used seven eligible proteins and changing query subsets. This run covers all nine training proteins and all 106 numeric rows.

Decision: retain chemical baseline; do not integrate this hybrid or launch a larger run based on it. A larger verified pool and matched evaluation of the neural sequence model are prerequisites for a defensible architectural claim.
