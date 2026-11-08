# BALM compound-and-protein dual-cold ensemble stress test — 2026-11-08

## Implemented experiment

Unlike earlier protein-group-only cross-validation, this procedure imposes **simultaneous protein-group coldness and canonical compound coldness** within the *already frozen TRAIN partition* of the public BALM BindingDB_filtered cohort.

1. Make four non-overlapping protein-trigram-graph group folds using GroupKFold(4) on 15,538 original TRAIN records (519 graph components).
2. For each fold, obtain isomeric RDKit canonical SMILES of all held-out compounds. Remove **every training record** whose canonical SMILES appears in the held-out fold. This is done before any model fit; no held-out labels used to decide exclusion. Do NOT call this scaffold-cold: related structures remain.
3. Collapse repeated identical sequence and original SMILES training pairs by mean. Each resulting fit has 4,425 to 5,199 unique protein-compound training pairs (average 4,818), after removing 5,822 to 6,744 raw training rows with held-out canonical compound identity.
4. Fit a fixed Morgan-2048 + training-fold protein tri/tetra-gram Ridge (alpha=1, protein feature scale .25), and three fixed 75/25 Ridge+HistGradientBoosting ensembles (chemical-only descriptors, ordinary joint molecular/protein descriptors, or explicit cross-product descriptors).
5. Report *all* fold held-out predictions as out-of-fold aggregate, not best epoch, and paired 5,000-resample bootstrap by 519 held-out graph components.
6. Frozen inner-development and 5,271-row reserved test Y outcomes are not used. Dedicated get_train_only() projects label-bearing Python records **only for TRAIN**, not the frozen inner-development or test partitions.

Exact RDKit isomeric canonical-SMILES overlap between each fold's train/holdout sets was **zero**. Remaining average maximum Morgan cosine to training fingerprints was approximately .54 to .57, compared to .78-.87 in the previous protein-only training folds. Only 0%-0.15% of held-out rows retained fingerprint cosine >= .999 (possible fingerprint collisions or close analogs, not identical canonicals).

## Primary fully out-of-fold metrics

| Candidate | Pooled RMSE | Macro protein-component RMSE |
|---|---:|---:|
| Train-fold label mean | 1.445091 | 1.355613 |
| Fixed Morgan+protein Ridge | 1.488583 | 1.381514 |
| Ridge + chemical descriptor boosting | 1.427519 | 1.324235 |
| **Ridge + joint chemical/protein boosting** | **1.424463** | **1.316399** |
| Ridge + explicit chemical/protein cross boosting | 1.422987 | 1.319868 |

Unlike the protein-only split, here plain Ridge is **worse than the train-fold mean** on both pooled and macro metrics. Three booster ensembles recover part of the loss; ordinary joint boosting improves over Ridge by ~4.31% pooled and ~4.71% macro. On this harder split, the ensemble has better point estimates than the mean by 0.02063 pooled / 0.03921 macro, but **uncertainty intervals include zero**: this is not a confirmed mean-baseline win.

## Paired 5,000-resample bootstrap by component

Differences below are candidate RMSE minus comparator RMSE. Each bootstrap samples *held-out protein graph components*, preserving within-component label correlation and uneven component sizes.

| Comparison | Pooled delta | Pooled 95% interval | Macro delta | Macro 95% interval |
|---|---:|---|---:|---|
| Ordinary joint ensemble - Ridge | **-0.06412** | **[-0.08919, -0.03860]** | **-0.06511** | **[-0.07599, -0.05370]** |
| Ordinary joint ensemble - train mean | -0.02063 | **[-0.07951, +0.03797]** | -0.03921 | **[-0.08370, +0.00355]** |
| Explicit cross ensemble - ordinary joint | -0.00148 | **[-0.00718, +0.00417]** | +0.00347 | **[-0.00167, +0.00845]** |
| Chemical-only ensemble - ordinary joint | +0.00306 | **[-0.01599, +0.02262]** | +0.00784 | **[-0.00329, +0.01933]** |

Ordinary joint beats Ridge on 391/519 protein groups. It beats mean on only 215/519 groups, despite lower average macro RMSE, highlighting heterogeneity of benefit. No clear advantage for manually formed cross-products or chemical-only booster over simpler ordinary joint boosting.

## Interpretation and scientific safety

This is meaningful evidence of **diversity between a sparse chemical/protein linear model and a low-dimensional nonlinear descriptor model**, across both known-chemistry and removed-compound regimes. It does **not** show a reliably better model than a train mean under dual novelty. Do not claim a paper-quality PerceiverCPI improvement.

Important limitations:
- The train-only dual-cold cross-validation uses only ~4.4k-5.2k unique training pairs per fit (rather than full 12.3k). Relative performance includes that reduced-data effect.
- BALM source still lacks individual assay conditions, DOI, and construct definitions; same compound-protein labels can disagree.
- Protein graph groups use approximate trigram features, not verified sequence-identity homology.
- All architecture choices arose in previous exploratory research and the inner-development set has been inspected many times. This challenge uses only TRAIN outcomes but cannot retroactively make those design choices unbiased.
- Bootstrap components may be correlated despite approximate graph grouping; percentile CIs are descriptive, not independent benchmark certification.
- No reserved prospective test evaluated.

## Code and reproducibility

- scripts/crossvalidate_balm_dual_cold_ensemble_train_only_dev.py: first dual-cold OOF run and model-versus-Ridge bootstrap.
- scripts/crossvalidate_balm_dual_cold_with_mean_bootstrap_dev.py: complete model, mean, and paired-control bootstrap; primary result file.
- dynacpi/balm_public_data_dev.py: get_train_only() loads only frozen TRAIN labels into Python data records.
- tests_v4/balm_dual_cold_ensemble_cv_test.py: canonicalization/sterochemistry/bootstraps and output integrity.
- research/balm_bindingdb_train_only_dual_cold_group_cv_with_mean_bootstrap.json: complete reproducible diagnostics.

To rerun, first deliberately archive the JSON result files; scripts intentionally refuse to overwrite prior experimental results.
