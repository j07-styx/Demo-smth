# Numeric support-transfer experiment

Completed 2,100 paired episodes: seven training target identifiers, 100 draws each, support sizes 1/3/5. Each fold fits a chemical Tanimoto kernel on numeric measurements from the other eight training proteins. No validation targets are scored. Hyperparameters were fixed before scoring; no search was conducted. This is a training-development experiment, not a source-approved benchmark or neural-model comparison.

| Method | 1 support | 3 support | 5 support |
|---|---:|---:|---:|
| Compound mean from other proteins | 0.9300 | 0.9262 | 0.9142 |
| Pooled chemical kernel | 0.8714 | 0.8669 | 0.8514 |
| Support mean | 1.1651 | 0.9893 | 0.9034 |
| Shrunk support offset | 0.9611 | 0.9369 | 0.9004 |
| Chemical kernel with support residuals | 0.8714 | 0.8669 | 0.8505 |
| Same method with shuffled support labels | 0.8714 | 0.8690 | 0.8561 |

Values are target-macro averages of episode RMSE in pKd units, lower is better. Query membership changes with support size; do not interpret cross-column differences as a pure support-size effect. The single-label shuffle is necessarily identical and supplies no negative-control evidence.

At five support measurements, the pooled chemical kernel reduces RMSE by 0.0629 (6.88%) relative to compound means on the same queries. A descriptive target-block bootstrap gives a delta interval [-0.1061, -0.0261]. This establishes a stronger simple baseline in this small training experiment, not a generalization claim.

Support residual adaptation improves RMSE by only 0.0009 relative to the pooled kernel, with interval [-0.0167, 0.0149]. Its advantage over shuffled labels is 0.0056, with interval [-0.0149, 0.0019]. Both intervals include zero. A global support offset performs worse. There is no reliable adaptation gain here, so this adapter should not be promoted on these results.

The 2,100 episodes are repeated draws, not 2,100 independent biological tasks. Bootstrap blocks are seven target identifiers; homology remains a dependence concern. Numeric-only sampling excludes screening-negative cells and creates ascertainment bias. Original physical constructs remain unverified. Existing numeric sequence checkpoint is unchanged.

Practical decision: retain the chemical kernel as an explicit comparator in future experiments, alongside compound means. Require any more complex adapter to beat it with paired target-level evidence; do not use the tiny observed support gain as justification for a larger training run.
