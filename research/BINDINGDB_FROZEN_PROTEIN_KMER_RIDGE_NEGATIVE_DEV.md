# Frozen protein-aware ridge experiment — negative result

Executed a new train-only fitted protein-aware ridge baseline using the existing chemical Morgan radius-2 1024-bit representation plus train-fitted TF-IDF character 2–3-gram protein sequence features (up to 4096 dimensions). Used the **frozen** 82 protein-component train and 20 protein-component inner-development split (27,118 and 7,387 pairs), not the older preliminary hash split. Fixed ridge alpha=1 from prior exploratory work; no new hyperparameter grid on the frozen development set. No reserved prospective test was read or evaluated.

| Baseline | Frozen inner-dev pooled RMSE |
|---|---:|
| Train-only mean | **1.803902** |
| DeepDTA inverse-sqrt component sampling, best observed epoch seed 2104 | 1.956261 |
| Chemical Morgan + protein sequence k-mer ridge alpha=1 | **2.402659** |

The protein-aware linear model fails to beat the mean comparator. This does **not** imply protein representations are useless: linear TF-IDF k-mers are limited, and the frozen split contains substantial novel-compound shift. It shows that simply appending protein sequence features does not solve the task. The DeepDTA best-epoch result is development-selected, not directly equivalent to a fixed-checkpoint model comparison. Assay and construct QC remain provisional; no independent test was evaluated.
