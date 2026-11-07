# Unseen-compound challenge

Completed 27 fixed kernel fits (nine target-held-out folds, three chemical exclusion regimes), followed by 900 row-count-matched random-reduction controls. All work uses the same 106 numeric training observations; no external validation or final test is scored. Alpha remains 1.

| Held-out axes | Kernel macro RMSE | Training global-mean macro RMSE |
|---|---:|---:|
| Protein identifier only | 0.8540 | 0.8629 |
| Protein identifier and compound | 0.8821 | 0.8991 |
| Protein identifier and Murcko scaffold | 0.8821 | 0.8991 |

Each fold excludes all query compounds or query scaffolds from other-target training rows. Queries are identical across regimes. Exact compound and scaffold exclusions yield the same result in this small pool; this is not evidence that scaffold splitting generally equals compound splitting. Explicit assertions verify role disjointness. Remaining training rows range from 24 to 88.

The dual-exclusion kernel is 0.0170 better than its fold training-mean baseline, but the descriptive target-bootstrap interval [-0.0364, 0.0039] includes zero. Thus there is no reliable generalization advantage over a constant predictor in this small challenge.

Randomly retaining the same number of other-target training rows gives a mean score approximately 0.8669. Dual exclusion minus this control is +0.0152, interval [-0.0906, 0.1158]. Row counts alone do not control chemical or target composition; this does not isolate a causal overlap effect. It shows that aggregate degradation is too uncertain to support a strong conclusion.

The prior 6.9% gain was relative to compound averages on seven support-eligible proteins, not relative to global mean and not an independent benchmark. The current nine-target challenge exposes how weak the absolute advantage is against the simpler global-mean comparator. Future experiment summaries must include that comparator alongside chemical and neural models.

Decision: keep the reusable chemical kernel as a comparator, not evidence of a successful CPI architecture. Do not tune additional architectures on this tiny pool. A larger source-supported dataset and independent evaluation are required before claiming model progress. Target identifiers are not homology-independent, and numeric-only ascertainment plus unverified constructs remain limitations.
