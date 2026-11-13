# Same-protein pair objective — 2026-11-13

ENGINEERING ONLY: reused frozen BALM TRAIN cohort, 5,808 rows, 298 proteins, 253 groups. Reserved test unscored.

Thirty fits completed: five group folds, two seeds, three graph controls. The model adds unit-weight same-protein pair-difference residual MSE to absolute residual MSE. All partners are distinct training rows of the same protein within the current outer training fold. Architecture, cap, anchor batches and schedule match the prior contact-graph run; additional forward computation does not match its compute budget. No checkpoint selection.

| Graph | Pooled RMSE | Group-macro RMSE |
| --- | ---: | ---: |
| Sequence | 1.552158 | 1.345613 |
| Real geometry | 1.551390 | 1.345115 |
| Scrambled geometry | 1.551746 | 1.345799 |

Real geometry minus scrambled pooled delta -0.000356, descriptive 95% group-bootstrap interval [-0.001232, +0.000437]. Macro delta -0.000684, interval [-0.001369, -0.000087]. These unadjusted exploratory intervals on repeatedly inspected data do not establish independent superiority.

## Objective comparison
The prior absolute-only real graph scored pooled 1.542005 and macro 1.343510; the new objective worsens both. Within-protein error MSE rises from 1.282811 to 1.288251 (baseline 1.281833). Within-protein correction energy rises from 0.00005283 to 0.00056081, about 10.6-fold, but this added variation is not more accurate.

Protein-mean correction energy remains 98.629% (previously 99.870%). 46.30% of individual corrections exceed 95% of the cap (previously 46.04%). The loss therefore increases chemical response without resolving saturation or protein-offset dominance. This is evidence against treating chemical sensitivity alone as a success criterion.

## Validation and interpretation
Independent validation reproduces all seed and ensemble metrics, exact row alignment and baseline, finite values, all 30 unique fits and bounded corrections. Diagnostic synthetic checks distinguish pure offsets from within-protein differences and verify orthogonal error decomposition. There are 61 singleton proteins; these contain no within-protein contrast.

Same protein does not necessarily imply the same experimental assay or construct. This pilot did not verify assay comparability of every pair. Pair differences can therefore include assay noise as well as true chemical signal. No claim that this isolates physical ligand-protein interactions is warranted.

## Decision
Do not promote this objective or increase pair-loss weight using these results. Preserve the prior model. Before another sweep, compare training-fold and held-group within-protein error and audit pair comparability using available assay metadata. That distinguishes failure to fit from overfitting or inconsistent targets. Structural sampling remains uniform and may miss pockets; pocket-aware modeling remains a separate untested hypothesis.

Weights and raw predictions remain in research_local/contact_pair_objective_20261113. Aggregates, protocol, validation and objective decomposition are saved here. No other repository or original core checkpoint changed.
