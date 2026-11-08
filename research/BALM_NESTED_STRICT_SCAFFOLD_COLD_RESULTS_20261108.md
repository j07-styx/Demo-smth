# BALM strict protein/Bemis–Murcko scaffold-cold benchmark — November 8, 2026

## What changed
This experiment replaces canonical-compound exclusion with strict RDKit Bemis–Murcko scaffold exclusion inside all four outer protein-group-disjoint folds and the three nested protein-group-disjoint training folds for each outer fit. Every acyclic compound without a Murcko core shares the same ACYCLIC_SINGLE_GROUP key, rather than receiving a special exception. No matching scaffold is retained between fit and heldout rows.

The frozen BALM TRAIN-only cohort contains 15,538 original records, 519 approximate protein 3-mer graph components, 5,971 unique SMILES, and 2,969 scaffold groups. Before averaging repeated inputs, each outer fold retains 4,252–4,981 records after scaffold exclusion. The outer fitted datasets contain 3,856–4,475 unique protein–SMILES pairs. All 15,538 original training rows are scored exactly once as outer heldout records; frozen development and the reserved prospective test provide no outcomes here.

Model: 75% Morgan2048/chiral chemical + train-fitted TF–IDF protein k-mer Ridge, alpha 1, protein-scale 0.25, and 25% ordinary joint chemical and protein descriptor HistGradientBoosting. A nested three-fold, again scaffold-cold, selects beta in {0, 0.25, 0.5, 0.75, 1} using average inner pooled and component-macro RMSE, enforcing both to beat the inner train-label mean. Prediction = outer fold training mean + beta × (joint ensemble prediction minus outer fold training mean).

Nested selected betas: **[1.0, 1.0, 1.0, 0.75]**.

## Out-of-fold metrics

| Predictor | Pooled RMSE | Protein-component macro RMSE |
|---|---:|---:|
| Corresponding fold train mean | 1.441784 | 1.362346 |
| Ridge alone | 1.487539 | 1.394103 |
| Unshrunk ordinary joint ensemble | 1.423290 | 1.327415 |
| **Nested mean-calibrated joint ensemble** | **1.412784** | **1.319430** |

This is about 0.74% lower pooled RMSE and 0.60% lower macro RMSE compared to unshrunk joint ensemble. Compared with the fold-train mean, point-estimate reductions are about 2.01% pooled and 3.15% macro.

## Paired protein-component bootstrap uncertainty
Resample 519 heldout protein graph components with replacement 5,000 times, seeded 20261108. Differences are nested ensemble minus comparator; negative is favorable.

| Comparator | Pooled delta | 95% pooled percentile interval | Macro delta | 95% macro percentile interval |
|---|---:|---|---:|---|
| Unshrunk joint ensemble | **-0.010506** | **[-0.019261,-0.001731]** | **-0.007985** | **[-0.014241,-0.001483]** |
| Fold-training mean | -0.029000 | **[-0.079794,+0.021776]** | **-0.042917** | **[-0.084900,-0.002999]** |
| Sparse Ridge | -0.074755 | [-0.099351,-0.050792] | -0.074673 | [-0.088369,-0.060922] |

The improvement over the unshrunk ensemble is favorable on both bootstrap intervals. Pooled improvement against the mean baseline **remains uncertain** (interval includes zero). The macro improvement over the mean narrowly clears zero in these descriptive intervals. This is NOT proof of a statistically independent benchmark win.

## Interpretation and limits
The previous identity-exclusion nested challenge selected betas [.75, 1, .75, .75] and achieved pooled RMSE 1.402154 and macro RMSE 1.298593; different training cohorts and chemical novelty levels mean these numbers cannot be compared as isolated architecture effects. The strict scaffold experiment favors no shrinkage in three of four outer fits, supporting nested adaptation rather than a universal fixed coefficient.

The BALM public source lacks original per-record assay DOI/method/construct provenance and contains conflicting repeated identical-input labels. Protein grouping uses unvalidated approximate 3-mer similarity rather than MMseqs2. Chemical analogs from different scaffolds may still be highly similar. Model design follows prior repeatedly inspected exploratory development runs. Bootstrap samples graph components which may be correlated. The original frozen development and prospective test were **not evaluated in this experiment**, and no claim of defeating PerceiverCPI is justified.

Reproduction: scripts/audit_balm_murcko_scaffold_cold_retention_dev.py; scripts/train_balm_nested_scaffold_cold_mean_shrinkage_dev.py; research/balm_bindingdb_nested_scaffold_cold_mean_shrinkage_traincv_dev.json; tests_v4/balm_nested_scaffold_cold_shrinkage_test.py.
