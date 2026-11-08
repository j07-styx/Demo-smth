# DynaCPI: Smith-Waterman protein grouping and scaffold-cold sensitivity study

**Date:** 2026-11-08. **Status:** Completed TRAIN-only exploratory experiment. Reserved test untouched.

## Summary and methodological correction

The original BALM protein groups were built with binary protein character-3-mer cosine >=0.5. They do NOT guarantee full protein homology separation. To investigate, every one of the 639*638/2 = 203,841 pairs of the 639 distinct protein sequences in the frozen BALM TRAIN partition was evaluated with a Smith-Waterman local protein alignment, BLOSUM62 substitution matrix, gap-open 10, gap-extend 1, parasail 1.3.4. 2,871 possible matches passed inexpensive alignment-statistics filters and were traceback-verified for aligned-column identity and coverage of the shorter sequence. This is exhaustive *screening* with a prefilter, not a mathematical proof of no alignments missed by the screen.

| TRAIN protein grouping | Components | Alignment edges | Edges crossing original k-mer groups | Largest component, proteins / rows |
|---|---:|---:|---:|---:|
| Original binary 3-mer cosine graph | 519 | — | — | — |
| SW identity >=50%, shorter coverage >=80% | 451 | 320 | 153 | 11 / 721 |
| SW identity >=40%, shorter coverage >=80% | 396 | 484 | **317** | 25 / 1050 |
| SW identity >=30%, shorter coverage >=80% | **271** | 1276 | **1109** | 125 / 3066 |

The 40%-identity condition found 317 alignment-passing protein pairs split across old 3-mer components. Therefore the original graph-cold models cannot be described as verified homology-cold. The alternative groups are *homology proxies*, NOT ground-truth evolutionary homology clusters: a shorter sequence's 80% coverage can represent one shared domain, and connected components can chain loosely related full-length proteins.

## Training-only scaffold and protein-alignment cold experiments

For each identity rule (30% and 40%), run four OUTER GroupKFold partitions over all 15,538 frozen BALM TRAIN rows, grouped by the alignment-derived sequence component. Before fitting, delete every training molecule whose RDKit Bemis–Murcko core appears in that fold's heldout molecules; all molecules with no scaffold core (acyclic) form one shared group. Average repeat training protein–SMILES labels before fitting. Each row is evaluated once out-of-fold; no protein alignment component or Murcko core overlaps across fit and heldout rows.

Within each outer fold, use three inner protein alignment-component grouped and Murcko-excluded folds to select one of [0, .25, .5, .75, 1] as shrinkage beta using pooled and protein-component macro RMSE. Reference architecture: 75% sparse chiral Morgan/protein k-mer Ridge and 25% ordinary chemical descriptor/protein composition gradient boosting. Add frozen 320-dimensional ESM2 8M mean protein embeddings only to the Ridge branch, and transfer that outer fold's classically selected beta unchanged to its ESM version. This isolates the contribution of ESM features, without outer-label hyperparameter selection. Five thousand bootstrap resamples of alignment components give paired intervals.

### 30%-identity / 80%-shorter-coverage (271 alignment groups)

Nested beta = [1.0, .75, 1.0, 1.0].

| Model | Out-of-fold pooled RMSE | Macro component RMSE |
|---|---:|---:|
| Fold training mean | **1.460959** | 1.463230 |
| Nested classical joint ensemble | 1.473994 | 1.389744 |
| **Nested ESM2-augmented ensemble** | **1.460624** | **1.379023** |

ESM2-minus-training-mean pooled delta = -0.000335, 95% group-bootstrap interval **[-0.132100, +0.130549]**, so essentially a pooled tie. Macro delta = -0.084207, interval **[-0.150145, -0.018733]**. ESM2-minus-classical pooled delta -0.013369, interval [-0.032251, +0.009362]; macro delta -0.010721, interval [-0.022757, +0.001063]. Neither ESM2-versus-classical 95% interval excludes zero under this stricter grouping.

### 40%-identity / 80%-shorter-coverage (396 alignment groups)

Nested beta = [1.0, 1.0, 1.0, 1.0], meaning no shrinkage was selected on these outer training partitions.

| Model | Out-of-fold pooled RMSE | Macro component RMSE |
|---|---:|---:|
| Fold training mean | 1.441199 | 1.397327 |
| Classical joint ensemble | 1.438519 | 1.354784 |
| **ESM2-augmented joint ensemble** | **1.430266** | **1.337548** |

ESM2-minus-train-mean pooled delta = -0.010933, 95% group-bootstrap interval [-0.078419, +0.056752], includes zero; macro delta = -0.059779, interval [-0.112952, -0.007630]. ESM2-minus-classical pooled delta = -0.008253, interval [-0.024800, +0.009421], includes zero; **macro delta = -0.017236**, interval **[-0.027065, -0.007345]**.

**Scientific interpretation:** At two alignment-group thresholds, the ESM-augmented approach demonstrates lower protein-component macro RMSE against the train-mean baseline. There is still NO well-supported pooled RMSE win over the train mean or a fully matched reference PerceiverCPI model. Results on different grouping thresholds have different train/heldout partitions and should not be compared as if they isolate only the architecture.

## Reproducibility, limitations and next gating tasks

- Code: scripts/audit_balm_train_protein_parasail_homology_dev.py; scripts/audit_balm_alignment_group_scaffold_retention_dev.py; scripts/crossvalidate_balm_sw_alignment_groups_scaffold_esm_dev.py.
- Audit artifacts: research/balm_train_only_smith_waterman_protein_group_audit_20261108.json; research/balm_train_only_alignment_group_edges_20261108.jsonl (one row per verified graph edge).
- Experimental result JSONs: research/balm_esm8m_nested_sw_identity30_cover80_murcko_scaffold_cold_traincv_dev.json and identity40_cover80 counterpart.
- Tests: tests_v4/balm_sw_alignment_group_audit_test.py and tests_v4/balm_sw_alignment_scaffold_cv_test.py.
- Dependency for alignment audit: requirements_balm_homology_audit_dev.txt (parasail==1.3.4).
- Local ESM2 pretrained weights and binary feature cache are deliberately NOT committed. Their SHA256 and extraction specification are in research/balm_esm2_t6_8m_train_only_feature_manifest_dev.json.
- No original frozen development or prospective reserved-test protein sequences, labels or predictions were processed in this audit or two experiments.
- The source BALM BindingDB_filtered dataset lacks individual assay DOI, method and construct provenance and has some conflicting repeated identical-input labels. Protein local alignment groups are an approximation, not a verified MMseqs2 or evolutionary homology certification. Model architecture and thresholds were examined following previous exploratory development inspection, so bootstrap intervals are descriptive, not independent proof of superiority.

Next scientific actions: curate provenance-backed Kd assay records, validate alignment grouping with an independent homology method, lock architecture/hyperparameters, and only then consider untouched prospective evaluation subject to the scientific cohort approval gate.
