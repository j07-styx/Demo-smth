# BindingDB assay-context and negative-control checkpoint — 2026-11-08

These experiments use the provisional **82 protein-cluster train / 20 protein-cluster inner-development** partition (27,118 / 7,387 pairs). All conclusions are exploratory: the development split has been inspected many times. The reserved future test was not read or evaluated.

## Distribution shift

| Assay text keyword class | Train | Inner-development |
|---|---:|---:|
| DSF / thermal shift | 826 / 27,118 (3.05%) | 4,638 / 7,387 (62.78%) |
| Cellular | 7,591 / 27,118 (27.99%) | 128 / 7,387 (1.73%) |

This protein-cluster holdout is also a major *assay-modality* holdout, confounding architectural evaluation.

## Nonidentifiability from identical inputs

Same canonical protein + compound occurs in multiple assay-specific records with discordant labels: 2,986 repeated input groups in train, 1,913 in inner-development. 575 training and 1,716 development groups have assay-specific pKd spread above 1. The optimistic in-sample squared-loss oracle floor for a protein+compound-only deterministic predictor is RMSE 0.4997 in train and **0.9733** on inner-dev. This is NOT a fitted predictive performance score.

Adding heuristically parsed **endpoint** to the conditioning key lowers inner-dev oracle floor to **0.5732**; adding both endpoint and modality yields **0.5704**. This reflects partitioning observations that may correspond to different experimental endpoints, not proof that an ML model can predict them. In train, endpoint+modality lowers oracle floor from 0.4997 to 0.1843, driven mainly by modality. Exact assay ID trivially gives a zero oracle floor because records were already aggregated within assay; this is an identity lookup, not a deployable generalization claim.

One traceable same-sequence/same-compound conflict is from DOI 10.1016/j.bmc.2018.12.011, with assay descriptions for recombinant CA6 DSF general binding affinity and DSF intrinsic dissociation constant. A sample pair reads pKd 5.0000 vs 9.8539. The assay descriptions differ; manuscript and protocol verification is required before concluding what explains the measurement difference.

## Predictive results

| Predictor | Pooled inner-dev RMSE | Component-macro inner-dev RMSE |
|---|---:|---:|
| Unweighted train-only mean | **1.8039** | 1.6983 |
| Cluster-weighted train-only mean | 1.9834 | **1.3920** |
| Heuristic assay-modality mean (CV-selected) | 1.8107 | 1.4060 |
| Assay-text-flag gradient boosting (CV-selected) | 2.1089 | 1.4539 |

The apparent strong macro improvement from the assay-prior was **not evidence for assay-dependent predictive learning**. In 1,000 negative controls, training modality tokens were shuffled within each protein cluster, preserving cluster label distributions and total weights. Every randomized prior had lower development pooled and macro RMSE than the actual assay-aware prior. The shifted **component-weighted global mean** explains more of the apparent macro gain than the purported modality signal.

Earlier protein-similarity identity permutation similarly showed the actual TF-IDF protein centroid assignment did not beat random permutations.

## Research decision

- Do **not** claim sequence-aware or assay-aware architecture has won.
- First define *assay-harmonized and construct-verified* endpoint eligibility and scientifically adjudicate discordant records.
- Train independent repeated-seed baselines only on a new fixed, provenance-approved cohort, report pooled and protein-component-macro RMSE, and keep the final test untouched.
- Treat modality/assay metadata as candidate confounders and report them explicitly in future study tables.
- Preserve all negative controls and scripts for reproducibility.

Reproduce using scripts/ablate_bindingdb_assay_metadata_identifiability_dev.py, scripts/train_bindingdb_assay_class_prior_dev.py and scripts/permutation_control_bindingdb_assay_class_prior_dev.py.
