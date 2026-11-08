# DynaCPI research: explicit compound–protein interaction ensemble (BALM internal development)

**Experiment date:** 2026-11-08. **Status:** positive *exploratory development* result, **not independently validated**.

## What was implemented
An explicitly interaction-aware ensemble of:
- **75% molecular Morgan-2048 + protein tri/tetra-gram TF–IDF Ridge** (standardized targets; fixed alpha=1 and protein scaling=0.25), and
- **25% HistGradientBoostingRegressor** on 21 molecular descriptors, 21 amino-acid composition features, and **64 explicit compound × protein interaction features** (8 predeclared physicochemical molecular descriptors times 8 protein-residue class summaries).

The complementarity hypothesis is that sparse chemical substructures and sequence k-mers give robust broad generalization, while shallow nonlinear descriptors capture residual physically meaningful interactions (polarity, aromaticity, charge, hydrophobicity). The ensemble is not an attention model and does not prove molecular mechanism.

## Data hygiene
Public BALM/BALM-benchmark BindingDB_filtered. Original source lacks per-record assay provenance. Frozen 519 train protein-trigram graph components (15,538 raw pairs; 12,315 unique protein-compound averages) vs 173 development graph components (3,891 original rows). Three fixed, overlapping group-heldout splits *within train only*. Training-only duplicate protein–compound observations are averaged. Every fold fits TF–IDF from its training rows. No reserved 5,271-row prospective test labels or predictions accessed. Protein trigram graph components are an approximate similarity proxy, not independently verified homolog disjointness.

## Predeclared candidates and TRAIN-only selection
Blend weights \`[0,.25,.5,.75,1]\`, plus pure Ridge, plain joint descriptor boosting, explicit interaction boosting. Boosting fixed hyperparameters: 160 iterations, rate=.05, 15 leaves, depth5, minleaf50, L2=15. Training-only group CV selected \`ridge_interaction_blend_0.25\` by the mean relative pooled/macro score requiring both metrics no worse than standalone Ridge.

| Model | Mean 3-fold TRAIN-only pooled RMSE | Mean component-macro RMSE |
|---|---:|---:|
| Ridge only | 1.321318 | 1.200437 |
| Ridge + 25% interaction boosting | **1.303467** | **1.190172** |

## Frozen development scores (one selected blend; transparently show ridge)
| Model | Pooled RMSE | Component-macro RMSE |
|---|---:|---:|
| Train-only mean | 1.589844 | 1.464093 |
| Fixed Ridge comparator | 1.405092 | 1.269216 |
| TRAIN-CV-selected interaction ensemble | **1.383743** | **1.247097** |
| Standalone explicit interaction boosting | 1.465738 | 1.297750 |

Paired improvement against Ridge: pooled RMSE -0.021349 (1.52%), macro -0.022119 (1.74%). The neural DeepDTA short-run best development score (~1.37176) is still numerically lower, and short-run PerceiverCPI best dev (~1.43175) uses a different architecture, sequence length, compute budget and single seed. **Do not claim established superiority to PerceiverCPI or DeepDTA**.

## Paired uncertainty (development-only)
Re-fitted only TRAIN, kept locked blend, aggregated 3,891 development squared errors by 173 protein graph components, and resampled **components**, not individual rows, 5,000 times using seed 20261108. Component-macro improvement on 93/173 components, loss on 80.

| Paired ensemble-minus-Ridge delta | Point | Group bootstrap 95% percentile interval |
|---|---:|---|
| Pooled RMSE | -0.02135 | **[-0.04658, +0.00573]** |
| Component-macro RMSE | -0.02212 | **[-0.04441, -0.00081]** |

**Important:** Pooled interval includes zero. Macro interval barely excludes zero in this exploratory non-independent development dataset. This is insufficient for a robust superiority claim, especially after repeated development inspection and without true homology clusters. A locked untouched evaluation later is necessary.

## Earlier provisional-cohort controls
Separately, on an *older and scientifically weaker* assay-ambiguous frozen cohort (27,118 train / 7,387 development), plain descriptor boosting performed poorly pooled (chemical-only 2.3272; joint protein 2.2433 vs mean baseline 1.8039), although component-macro favored protein features (1.4589 vs 1.5162). Inverse-square-root component weights worsened joint boosting (pooled 2.2776, macro 1.4972). Three additional group-shuffle splits *inside old training* showed heterogeneous pooled results: mean 1.5733 chemical-only vs 1.6637 joint, but component macro 1.4345 vs 1.3460. The older cohort is not the BALM experiment and these metrics must not be mixed.

## Reproduce
Run \`python -m scripts.train_balm_bindingdb_explicit_interaction_ensemble_dev\` to fit TRAIN-only CV and selected development experiment, then \`python -m scripts.bootstrap_balm_bindingdb_interaction_ensemble_dev\` for paired group uncertainty. They refuse to overwrite existing outputs; archive or deliberately rename generated reports to rerun. The BALM public Arrow data must already be staged locally with the separate source manifest.

## Scientific limitations
No per-record assay DOI/method on BALM source, duplicate label conflicts, approximate protein similarity graph, only three overlapping training folds, non-independent repeatedly inspected development, no full match to reference-model training budgets or seed replication. Reserved test has not been evaluated. Maintain scientific cohort gate.

## Matched negative-control addendum (2026-11-08)
The later report at research/BALM_RIDGE_BOOSTING_CONTROLS_20261108.md demonstrates that both ordinary joint-feature boosting and chemical-only boosting improve Ridge. Explicit cross-product features do not show distinct mechanistic value. Development macro RMSE of joint ensemble was 1.24565 versus explicit-cross ensemble 1.24710, while chemical-only ensemble had best inspected pooled RMSE 1.37639. Prior observed improvement is a valid exploratory ensemble observation, not proof that hand-designed cross-products are necessary.
