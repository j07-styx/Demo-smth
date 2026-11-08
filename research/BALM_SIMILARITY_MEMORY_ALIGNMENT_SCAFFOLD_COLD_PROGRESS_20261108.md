# DynaCPI: chemical–protein similarity-memory ensemble under alignment+scaffold cold conditions

**Completed 2026-11-08. Status: positive TRAIN-only exploratory research, NOT an independent PerceiverCPI win.**

## New model, actual implementation

A three-arm compound–protein affinity estimator: existing 75% sparse Morgan/protein-k-mer/frozen ESM2-8M Ridge + 25% ordinary joint chemical/protein descriptor boosting, coupled to a conservative nonparametric **memory of fold-training compound–protein affinities**.

The memory compares every prospective compound–protein input to *only that fold's training examples*. Molecular similarity is cosine of L2-normalized chiral Morgan radius2/2048-bit fingerprints; protein similarity is cosine of L2-normalized frozen ESM2-8M 320-D pooled protein vectors. Each memory specification selects the TOP k highest weighted similarity training pairs (not the least similar). Similarity weights are nonnegative and use predeclared chemical and protein exponents. The memory estimate is a normalized weighted average of the corresponding fold-training p-affinity labels. When all weights vanish it safely falls back to the fold-training label mean.

Memory prediction = fold-training mean + 0.5 * (weighted neighbor average - fold-training mean).

New predictor = 0.75 * (original nested shrinkage-calibrated ESM2 joint ensemble) + 0.25 * memory prediction. The base nested beta is inherited from prior training-only inner cold folds, not tuned from the new heldout outcomes. None of the neighbor labels comes from heldout records.

Predeclared memory variants:
- chemical cosine^4, k=64 (chemical-only negative control),
- chemical cosine^2 * positive ESM cosine^8, k=64 (fixed primary joint candidate),
- chemical cosine^2 * positive ESM cosine^16, k=64,
- chemical cosine^2 * positive ESM cosine^8, k=256.

Each variant is evaluated both standalone (half shrunk to mean) and as a 25%-weighted additive memory branch. This is a set of exploratory comparisons; reporting the best number after inspecting outer outcomes is NOT independent model selection.

## Cold generalization protocol

All 15,538 frozen BALM TRAIN records held out once across four outer folds for each protein grouping rule. Protein groups arise from previously recorded exhaustive Smith–Waterman local-alignment proxies at >=30% or >=40% sequence identity over >=80% shorter-sequence aligned coverage. In each outer fold, training excludes every compound whose RDKit Bemis–Murcko scaffold appears in its heldout fold, including a shared acyclic group. Train duplicate exact protein/SMILES values are mean-collapsed. No alignment component or scaffold core crosses train/holdout. Frozen original inner-development and reserved prospective test sequences/labels were never accessed. ESM2 weights and training-only feature cache were frozen.

## Out-of-fold results: 40% alignment identity grouping (396 protein groups)

| Model | Pooled RMSE | Protein group-macro RMSE |
|---|---:|---:|
| Fold train-mean baseline | 1.441199 | 1.397327 |
| Previous ESM2 ensemble | 1.430266 | 1.337548 |
| Ensemble + chemical-only memory k64 | 1.399705 | 1.322367 |
| **Ensemble + fixed joint ESM8 memory k64** | **1.399824** | **1.321830** |
| Ensemble + joint ESM16 memory k64 | 1.397602 | 1.320899 |

Compared with previous ESM2 ensemble, the fixed joint k64 memory branch improves pooled RMSE **-0.030442** (5,000 protein-group bootstrap 95% interval **[-0.043176,-0.018513]**) and component macro RMSE **-0.015718** (interval **[-0.025545,-0.005764]**). Both favor the new ensemble.

## Out-of-fold results: 30% alignment identity grouping (271 protein groups)

| Model | Pooled RMSE | Protein group-macro RMSE |
|---|---:|---:|
| Fold train-mean baseline | 1.460959 | 1.463230 |
| Previous ESM2 ensemble | 1.460624 | 1.379023 |
| Ensemble + chemical-only memory k64 | 1.427946 | **1.367691** |
| **Ensemble + fixed joint ESM8 memory k64** | **1.420606** | 1.369985 |
| Ensemble + joint ESM16 memory k64 | 1.417515 | 1.367833 |

The fixed joint k64 memory branch improves pooled RMSE against previous ESM2 ensemble **-0.040018** (group bootstrap interval **[-0.060391,-0.016002]**). Its component-macro difference **-0.009038** has interval **[-0.021397,+0.004105]**, including zero.

## Critical mechanistic negative control

To determine whether *protein similarity in the memory* matters beyond chemical similarity alone, we re-ran both folds with direct paired comparisons of matched fixed k64 memory branches (same 25% blend and half-mean shrinkage).

| Joint-protein memory minus chemical-only memory | Pooled delta | 95% pooled interval | Macro delta | 95% macro interval |
|---|---:|---:|---:|---|
| 40% identity | +0.000119 | [-0.004746,+0.004729] | -0.000536 | [-0.005074,+0.004032] |
| 30% identity | -0.007341 | [-0.020900,+0.005413] | +0.002294 | [-0.003264,+0.008046] |

**Every interval includes zero.** The memory **ensemble mechanism** improves the prior ensemble on pooled error at both identity thresholds, but we CANNOT attribute the gain specifically to protein-conditioned memory similarities. A simpler chemical-only memory achieves similar scores. Correct protein ESM features are already present in the Ridge branch and earlier shuffled-protein negative controls supported their macro-level relevance; this does not establish an additional causal advantage for using ESM inside the memory weights.

## Against the simple fold-training mean

The joint-memory ensemble point estimates beat fold mean on both pooled and macro RMSE in both grouping regimes. But the paired pooled intervals against mean still cross zero:
- 40%: pooled -0.041375, interval [-0.097625,+0.015262]; macro -0.075497, interval [-0.119409,-0.031074].
- 30%: pooled -0.040354, interval [-0.152606,+0.071062]; macro -0.093244, interval [-0.148217,-0.038068].

Thus **no reliable pooled-RMSE superiority over a trivial train-mean baseline has been established**, even with the memory branch.

## Engineering verification and limitations

The initial prototype erroneously selected the *least* similar neighbors due to a sign error in argpartition. A unit test caught this. We corrected ranking to use the negative similarity, verified true top-1 behavior, and reran both cold conditions. The invalid trial is archived locally under data/audit_local_invalid_runs, intentionally NOT committed or treated as results.

New reusable inference-kernel function: dynacpi/cpi_similarity_memory_dev.py. Main executable: scripts/compare_balm_similarity_memory_alignment_cold_dev.py. The --paired-controls option reproduces all scores with direct group bootstrap against chemical-only memory. Four result artifacts (40%/30% and each paired-controls report). Tests: tests_v4/cpi_similarity_memory_test.py and tests_v4/cpi_similarity_memory_cv_report_test.py. No binary model checkpoints required for this training-only experiment; frozen pretrained ESM2 cache is local and hash-verified.

Caveats: BALM dataset lacks per-record assay DOI/method and construct; repeated identical inputs can disagree. Protein alignment groups are exploratory homology proxies, not verified biological homology. Murcko scaffold exclusion does not remove all molecular analogs. Numerous architecture candidates have been inspected across prior experiments; group bootstrap intervals describe within-TRAIN behavior and do NOT account for all research choice multiplicity. Reserved test untouched and scientific cohort approval gate still blocked. Full, independently replicated PerceiverCPI/DeepDTA comparisons remain necessary for any superiority claim.
