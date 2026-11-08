# Frozen BindingDB development: negative controls reveal assay-context ambiguity

**Date:** 2026-11-08. **Status:** provisional, repeatedly inspected internal development. No positive prospective-test claim.

## Results at a glance

Same frozen 82 train and 20 inner-development protein components, 27,118 train pairs and 7,387 dev pairs. The separately designated 2,936-pair prospective test has NOT been evaluated.

| Method | Inner-dev pooled RMSE | Inner-dev cluster-macro RMSE |
|---|---:|---:|
| Training-mean predictor | 1.803902 | 1.698289 |
| Conservative protein similarity prior | **1.801194** | 1.671521 |
| Protein nearest-component chemical analog correction | 1.842287 | 1.608613 |
| Assay-text-aware chemical+protein gradient boosting | 2.108862 | **1.453863** |

The compound analog model was selected on three protein-component-heldout folds *inside training*. It used a bounded nearest-chemical residual from compounds measured for three similar training protein clusters. Train-CV found 0.5 coefficient, capped at 1 pKd, but this worsened pooled development RMSE despite improving the component-macro average. The CV-to-dev transfer gap is substantial.

The assay-aware model consumes scientific assay description metadata, not an arbitrary assay ID: 21 RDKit compound descriptors, 21 protein sequence composition features, and boolean flags for terminology such as "intrinsic", "apparent", "DSF", "binding affinity". Fixed 160-iteration HistGradientBoostingRegressor settings were selected among three feature variants using training-only protein-group CV. The text-flag variant was selected, but failed pooled inner-development RMSE.

## Protein prior fails its identity-shuffle negative control

For the conservative protein prior, 1,000 permutations randomly reassigned training protein-component sequence centroids to fixed training component affinity profiles, preserving all training and development labels.

- Actual pooled RMSE: **1.801194**; permuted mean 1.801191, one-sided empirical lower-RMSE rank 0.668.
- Actual cluster-macro RMSE: **1.671521**; permuted mean 1.636732, one-sided empirical lower-RMSE rank 0.752.

This refutes a strong claim that the chosen TF-IDF sequence-similarity assignments are driving predictive improvement. It does not prove protein identity is irrelevant for CPI in general; it invalidates the current mechanistic interpretation. Do not present the similarity prior as biologically verified.

## Input ambiguity is severe

After filtering only for minimum assays with 15 compounds and within-assay technical repeat span <=0.1 pKd:

| Audit statistic | Train | Inner-development |
|---|---:|---:|
| Assay-specific rows | 27,118 | 7,387 |
| Unique protein-sequence + canonical-compound inputs | 21,267 | 4,866 |
| Inputs appearing under multiple assay keys | 2,986 | 1,913 |
| Rows belonging to repeated identical-input groups | 8,837 (32.6%) | 4,434 (60.0%) |
| Identical inputs with cross-assay pKd spread >1 | 575 | 1,716 |
| Optimistic within-input squared-loss RMSE floor | 0.499732 | **0.973269** |

The "floor" is the square root of the empirical within-identical-input residual SSE divided by all rows. It uses all of the internal split's labels to compute an *oracle* per-input mean and is therefore a nonpredictive **in-sample mathematical lower bound**, NOT a test score or a lower bound on the underlying physical prediction task. The true measurement process can depend on assay protocol not provided to a sequence+compound-only model.

The largest dev component has 5,027/7,387 rows, 12 protein sequences, 134 different assay keys, and just 453 canonical compounds. The largest train component holds 17,814/27,118 rows, 252 protein sequences, and 459 assay keys. These weights can dominate pooled RMSE and absorb many incompatible endpoint definitions.

## Concrete same-publication conflict

Within one held-out development component, the same protein sequence and canonical compound occur in two assays from the same DOI **10.1016/j.bmc.2018.12.011**:

- Entry assay key 50006842_21: **pKd 5.0**, description "Binding affinity to recombinant human CA6 by DSF-based fluorescence thermal shift assay".
- Entry assay key 50006842_9: **pKd 9.853872**, description "Binding affinity to recombinant human CA6 assessed as intrinsic dissociation constant by DSF-based fluorescence thermal shift assay".

The affinity spread is **4.853872 pKd** for the same sequence+compound-only input. These may be distinct scientific endpoints/assay interpretations, not erroneous measurements. BindingDB explicitly organizes data by protein, compound, experimental binding measurement, and assay details. Ignoring assay context erases meaningful distinctions. The source publication is "Pyrrolidinone-bearing methylated and halogenated benzenesulfonamides as inhibitors of carbonic anhydrases" (2019).

## Direction for DynaCPI

1. **Suspend architecture-superiority claims on this provisional cohort.** The model objective is not unique under its current inputs.
2. Define and verify a **single comparable binding endpoint**, including assay method, conditions, qualifier/exactness, target construct, source publication, and substrate effects. Do not collapse distinct intrinsic and apparent measures blindly.
3. Build a protocol-aware benchmark with **assay- or endpoint-specific task keys and conflict quarantine**, using train-only QC rules defined before looking at any new test.
4. Maintain protein-component disjointness, source duplication audits, molecule scaffold diagnostics, and evaluation stratified both by assay and protein family. Preserve pooled and cluster-macro metrics.
5. Re-train controlled PerceiverCPI and architecture candidates on the new cohort, compare matched training budgets and repeated seeds, and only then evaluate on a genuinely uninspected test.
6. Use meaningful negative controls: protein centroids shuffled, compound labels shuffled, and assay-context disabled. Sequence priors that match randomized controls must not be counted as protein-aware advances.

**Important limitations:** internal-development labels have been inspected repeatedly. Assay descriptions can be ambiguous, and physical constructs are not yet verified against publications; the one paper above is a traceable example, not proof every conflict reflects a particular mechanism. Earlier experiments used some of the later designated test components as training data, so any future test must use fresh-from-scratch model weights. A stronger independent evaluation will need a truly untouched, quality-reviewed cohort.

**Reproduction files:** scripts/train_bindingdb_cold_protein_chemical_analogs_dev.py, scripts/permutation_control_bindingdb_cold_protein_similarity_dev.py, scripts/audit_bindingdb_frozen_assay_heterogeneity_dev.py, scripts/audit_bindingdb_identical_input_label_conflicts_dev.py, scripts/train_bindingdb_assay_text_aware_boosting_dev.py.
