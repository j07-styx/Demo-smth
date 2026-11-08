# Negative controls: do frozen ESM2 protein representations carry meaningful identity-specific information?

**Date:** 2026-11-08. **Scope:** TRAIN-only BALM strictly protein-group/Murcko-scaffold-cold evaluation. **Result:** Real ESM2 vectors improve protein-component-macro RMSE over three independent deranged-vector controls. Pooled RMSE differences remain uncertain. No independent test.

## Exact intervention
Keep the molecular Morgan fingerprints, fold-trained protein character TF-IDF k-mer features, fixed 25%-weighted joint molecular/protein descriptor booster, training target normalization, nested betas [1,1,1,.75], full original TRAIN-only 4-fold scaffold/group-cold assignments and heldout labels unchanged.

Only change the 320-dimensional frozen ESM2_t6_8M protein representation. For each predeclared seed 2103, 2104 and 2105, take a random **one-to-one derangement** of the 639 distinct TRAIN protein-sequence hash keys and map each key to a different pretrained ESM2 vector. Apply each permutation consistently to every sample in that run, both train and heldout, without reading labels during permutation creation. The derangements preserve all embeddings, marginal feature distributions and model capacity, but destroy their correct relationship to protein sequence identities.

Note: The other protein features, especially true k-mer TF-IDF and amino-acid composition, were NOT shuffled. This isolates whether the additional ESM2 vector has correct protein-specific content beyond true k-mer context.

## Four-fold strict dual-cold out-of-fold results

15,538 original TRAIN rows, 519 disjoint heldout protein 3-mer graph components. Each fold excludes every training molecule sharing a heldout Bemis-Murcko scaffold core; 0 scaffold overlaps, all acyclic compounds share one scaffold group. Same 3,856–4,475 averaged unique training pairs per fold. Fold betas were selected previously inside original TRAIN folds, not retuned here.

| ESM2 input | Pooled RMSE | Protein-component macro RMSE |
|---|---:|---:|
| Unaugmented classical nested joint ensemble | 1.412784 | 1.319430 |
| **Correct pretrained ESM2 input** | **1.409107** | **1.305516** |
| Deranged vectors, seed 2103 | 1.411882 | 1.321431 |
| Deranged vectors, seed 2104 | 1.414254 | 1.322508 |
| Deranged vectors, seed 2105 | 1.410721 | 1.318548 |

Correct ESM2 is better macro than all three derangements; pooled improvement is small and does not have stable bootstrap support.

## Paired 5,000 protein-component bootstrap resamples
Each bootstrap samples 519 heldout protein graph components with replacement, preserving within-group label correlation, seed 20261108. Differences are **deranged minus correct ESM2 RMSE**; positive favors correct ESM2.

| Derangement | Pooled difference | 95% pooled interval | Macro difference | 95% macro interval |
|---|---:|---|---:|---|
| 2103 | +0.002775 | [-0.012558,+0.018744] | **+0.015915** | **[+0.007132,+0.024515]** |
| 2104 | +0.005147 | [-0.013097,+0.020790] | **+0.016992** | **[+0.008339,+0.026072]** |
| 2105 | +0.001614 | [-0.013615,+0.016441] | **+0.013032** | **[+0.004698,+0.021372]** |

Correct ESM2 versus the previously selected unaugmented ensemble: macro improvement −0.013913, 95% group-bootstrap interval [−0.021845,−0.006113]; pooled −0.003677, interval [−0.018014,+0.010930]. Correct pretrained features therefore show a **protein-specific macro-metric signal**, above random vector expansion. This does NOT imply the model has learned an interpretable molecular binding mechanism or that the new model reliably improves pooled RMSE.

## Scientific interpretation and limitations
Three derangements are a limited negative control, not a complete permutation-test null distribution or formal p-value. These candidate features/weights were motivated by repeatedly inspected development research. Group bootstrap intervals are descriptive and assume approximate 3-mer graph components act as independent units, which is not validated sequence-identity homology. Source BALM affinities have missing original assay method/DOI and known contradictory same-input labels. ESM2 truncates 85 of the 639 training proteins to their first 1022 amino acids. Only original frozen TRAIN records were used as feature inputs/outcomes; frozen inner-development and reserved prospective test were not evaluated. No claim of outperforming fully matched PerceiverCPI or DeepDTA is justified.

## Reproducibility
- Script: scripts/ablate_balm_esm8m_protein_derangement_scaffold_dev.py.
- Output: research/balm_esm8m_protein_derangement_negative_controls_scaffold_cv_dev.json.
- Test: tests_v4/balm_esm8m_derangement_control_test.py.
- Frozen ESM2 cache and weight hash recorded in research/balm_esm2_t6_8m_train_only_feature_manifest_dev.json; binary cache and pretrained weights are local, not committed.
- All output scripts refuse overwriting existing experimental result JSONs.
