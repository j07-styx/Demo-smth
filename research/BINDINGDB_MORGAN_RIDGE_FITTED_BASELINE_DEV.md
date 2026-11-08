# BindingDB inner-development: fitted Morgan ridge baseline

A newly trained **Morgan radius-2, 2048-bit, chirality-aware fingerprint ridge model** was fitted on 27,118 provisional BindingDB training pairs, with an explicit intercept and fixed predeclared regularization alpha=100. It was evaluated on 7,387 inner-development pairs across 20 held-out protein components. The reserved prospective test was not read or evaluated. The sparse least-squares fit converged after 64 iterations in approximately 11 seconds.

| Model | Inner-dev pooled RMSE |
|---|---:|
| Train-only global mean | **1.803902** |
| DeepDTA normalized AdamW lr=0.0003, best observed dev epoch | 2.224241 |
| DeepDTA normalized AdamW lr=0.0001, best observed dev epoch | 2.323641 |
| Morgan fingerprint ridge alpha=100 | **2.566153** |

Morgan ridge component-macro RMSE was 1.598080, sharply below its pooled RMSE, indicating disproportionate influence from some large or high-error components. Macro and pooled scores answer different questions; neither should be selected post hoc to claim a win. The fitted chemical-only ridge model performs poorly on pooled RMSE, so stronger chemical representations **alone** are not a demonstrated solution to the observed held-out-protein plus compound-novelty shift.

This is a single fixed-alpha experiment, not an optimized chemical model or proof that molecular fingerprints are intrinsically inferior. Protein identity is absent from the ridge features. The source assays and constructs remain provisional and development data have been repeatedly inspected. No scientific cohort approval, independent test evaluation, or superiority claim is made.
