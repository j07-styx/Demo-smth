# BALM chemical-neighborhood gated ensemble ablation — 2026-11-08

## Status: implemented; TRAIN-only CV selected fixed 25% reference, not the adaptive gate

The prior 75% Morgan+protein Ridge / 25% ordinary joint chemical/protein HistGradientBoosting predictor improved over Ridge. This experiment asks whether chemical domain novelty should modulate the 25% booster coefficient per compound. Novelty uses maximum Morgan-2048-bit cosine similarity to molecules in that fold's training set, calculated from molecular features alone, with no validation labels. Evaluated against three predeclared gating functions: constant w=.25; w=.40-.30*similarity; w=.10+.30*similarity. Prediction is (1-w)*Ridge+w*boosting.

A NEW four-fold GroupKFold within frozen BALM TRAIN assigned each protein graph group to exactly one held-out fold. No hyperparameters or gate weights were selected using frozen development, and reserved test was neither loaded nor evaluated.

| Model | Mean four-fold pooled RMSE | Mean component-macro RMSE |
|---|---:|---:|
| Ridge | 1.343487 | 1.216188 |
| Fixed w=.25 | **1.313114** | 1.193418 |
| Higher boost when chemistry is novel | 1.313940 | **1.192272** |
| Higher boost when chemistry is familiar | 1.315901 | 1.197129 |

Our conservative candidate selection requires both pooled and macro RMSE no worse than fixed blend. The selected candidate is therefore fixed w=.25, i.e. no additional architecture complexity.

### Frozen development (exploratory; same repeatedly inspected split)
Locked fixed reference: pooled RMSE **1.382236**, macro **1.245649**, compared with Ridge **1.405092** pooled / **1.269216** macro. This reconstructs the previously observed joint ensemble; it does not represent a new development improvement.

Mean max chemical cosine similarity across development pairs is **0.83069**; **59.26%** have a fingerprint cosine >=.999 to some train compound (including exact or fingerprint-near matches). Four training-only protein-holdout folds had 52%–70% of heldout pairs with such a match. These are fingerprint matches, not necessarily identical canonical molecules. Protein group coldness is not chemical coldness. A dual holdout that removes compounds from TRAIN is now necessary to test robust generalization.

## Caveats
Public BALM source has no individual assay DOI/method and conflicting same-input affinities. Protein graph grouping is by approximate trigram similarity, not verified homology. Frozen development has been repeatedly inspected. No independent test evaluated, and scientific cohort approval remains blocked. Do not claim adaptation helped or claim superiority over PerceiverCPI.

Reproduce: python -m scripts.train_balm_bindingdb_chemical_domain_gated_ensemble_dev (after deliberately archiving old output); run python -m unittest tests_v4.balm_chemical_domain_gate_test -v.
