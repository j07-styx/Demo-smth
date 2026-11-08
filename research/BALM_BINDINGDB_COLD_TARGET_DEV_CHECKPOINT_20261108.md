# DynaCPI public BALM BindingDB cold-protein development baseline — 2026-11-08

## Why this second cohort was staged

The provisional BindingDB assay-specific cohort has severe assay heterogeneity, incompatible same-input labels, and highly imbalanced protein clusters. The strict DOI+SPR/ITC+explicit-Kd filter leaves only 66 train rows and 82 inner-dev rows, so it cannot support a trustworthy generalized CPI experiment. The broader DOI-linked physical-assay screen is only 902 train rows and 294 dev rows, with model-selection CV retaining the train-mean predictor.

As an independent exploratory track, stage the publicly available **BALM/BALM-benchmark BindingDB_filtered** data (CC-BY-4.0), containing 24,700 records and 1,069 unique protein sequences. This source is derived from curated TDC data but **does not expose the original assay descriptions or source DOI per record**. It is not a substitute for source-verified experimental harmonization.

## Reproducibility

- Public source: BALM/BALM-benchmark, BindingDB_filtered, upstream Arrow data (20 MB).
- Source SHA256: 13fbb1ae1c0731a5f3f7345e64a4d027b725dccfbf935a95b5253bd3633967dc.
- Local copy is kept under data/reference/balm_bindingdb_202611/ and **not committed to git**.
- Python pyarrow 17.0.0 installed for Arrow I/O. Source staging script checks exact length and source SHA.
- Protein sequence metadata only were used for split creation: binary 3-mer count cosine >=0.5, connected components of the similarity graph.
- Deterministic SHA256 component assignment: 519 components/15,538 rows train, 173 components/3,891 rows inner-development, 173 components/5,271 rows reserved test.
- **This approximate 3-mer graph is NOT validated protein homology clustering or MMseqs sequence identity.**
- Test membership was frozen before any test labels were inspected. Only train and inner-dev labels are accessible via the data-loading helper.

## Frozen train and development QC

| Metric | Train | Inner-dev |
|---|---:|---:|
| Rows | 15,538 | 3,891 |
| Unique protein sequences | 639 | 209 |
| Unique canonical molecular strings | 5,971 | 2,005 |
| Maximum component pair share | 4.64% | 4.99% |
| Repeated identical-sequence+compound input groups | 1,305 | 333 |
| Groups with same-input affinity spread >1 pKd | 461 | 74 |
| Optimistic same-input oracle RMSE floor | 0.3358 | 0.2016 |

Exact protein sequences shared between train and inner-dev: 0. Exact compounds shared: 737. Input conflict persists, but is lower than the previous provisional assay cohort. These are mathematical in-sample oracle floors, not predictive scores.

## Train-only CV of linear CPI predictors

On three protein-component-disjoint folds inside the frozen training partition, train-only target means and duplicate-record averaging were used for each fold. Compound features: Morgan radius-2 chiral 2048-bit, L2 normalized. Protein features: training-fold-fitted character TF-IDF 3–4-mers (up to 4096). Candidate Ridge penalties: 0.1, 1, 10.

**Selected using TRAIN-only group CV:** concatenated chemical+protein features, Ridge alpha=10, based on a pooled/macro error objective requiring both metrics beat the mean comparator.

| Inner-development (3,891 rows, 173 protein groups) | RMSE |
|---|---:|
| Train-only mean, after train duplicate consolidation | 1.589844 |
| Chemical+protein Ridge alpha10, TRAIN-CV selected | **1.436325** |
| Train-only mean component-macro RMSE | 1.464093 |
| Selected Ridge component-macro RMSE | **1.309695** |

**These are exploratory internal development results**, not independent test scores. The paired input ablation has not yet demonstrated protein signal independently of chemical input; comparison with chemical-only and negative controls is necessary before a mechanistic claim. The reserved 5,271-pair test has never been scored. Do not claim we have beaten PerceiverCPI on a common benchmark from this result, because PerceiverCPI has not been retrained on this split with matched conditions.

## Outstanding next steps

1. Run explicit chemical-only, protein-only, and matched regularization ablations plus protein-input permutation controls on the frozen inner-dev.
2. Repeat across seeds (when stochastic model used) and obtain cluster-bootstrap uncertainty.
3. Train upstream PerceiverCPI and DeepDTA on this exact partition with matching availability of protein/compound context and transparent compute budgets.
4. Validate approximate k-mer graph against a true MMseqs2 alignment-based protein homology split before claiming homolog independence.
5. Evaluate reserved test only once after protocol is finalized and all hyperparameters/checkpoint choices are locked. Retain CC-BY-4.0 attribution.
