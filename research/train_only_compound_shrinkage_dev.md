# Training-only protein LOTO: compound-mean shrinkage

Implemented an interpretable regularized compound-average baseline with `alpha` selected exclusively using **leave-one-training-protein-out** (LOTO) cross-validation on nine training proteins. Each compound prediction is `(sum(training labels) + alpha * training global mean) / (compound count + alpha)`. The selection criterion is the mean of held-out-training-protein RMSE, not the existing validation error. Candidate alphas: 0, 1, 3, 10, 30, 100, 300, 1000.

The training-only criterion selects **alpha = 3** (LOTO macro RMSE **0.593281** versus **0.607927** for alpha 0). On the **already-inspected** four-protein development validation cohort, alpha 3 gives target-macro RMSE **0.835729** versus **0.836518** for unregularized compound averages, while pooled RMSE **worsens** to **0.916237** from **0.907667**. This mixed result does not establish superiority. The score combines exact numeric Kd and screening-negative/weak-binding labels; family-disjointness and assayed construct identity remain unverified.

A regression test mutates every validation label and verifies the selected alpha and every training CV score remain identical, preventing accidental validation-based hyperparameter selection. The script is read-only and modifies no source data or checkpoints.

Reproduce: `python scripts/train_only_compound_shrinkage_dev.py` and `python tests_v4/train_only_compound_shrinkage_test.py`.
