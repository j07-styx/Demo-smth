# BALM strict scaffold-cold frozen ESM2 protein-feature ablation — 2026-11-08

## What was actually implemented

We loaded the public 7.5-million-parameter pretrained ESM2_t6_8M_UR50D encoder, **froze its weights**, and used the RTX 4060 to infer final-layer mean residue representations for all **639 distinct protein sequences appearing in the frozen BALM TRAIN partition only**. Each protein becomes a 320-dimensional embedding, L2-normalized for regression. 85 proteins are longer than the model limit and were **N-terminal truncated to the first 1,022 residues**. The cache is retained locally under data/reference and is not committed. The research feature manifest records the pretrained-weight hash, model, extraction protocol, cache hash and truncation count. No frozen dev/test labels or protein sequences were encoded.

This ablation is entirely within the same four **protein-group and strict Bemis-Murcko-scaffold cold TRAIN-only folds** as the previous experiment. There is zero scaffold overlap between each fold's fit and heldout records (including all acyclic molecules in one common scaffold group). All 15,538 frozen TRAIN records are out-of-fold prediction targets exactly once; each scaffold-cold fitted training fold contains 3,856–4,475 unique averaged protein/compound pairs. Protein group disjointness is by approximate 3-mer similarity graph, **not** verified identity-based homology. The original prospective test is untouched.

### Feature-level ablation (fixed alpha=1 Ridge)

Chemical representation is L2-normalized chiral Morgan radius-2 2048-bit fingerprints. Protein alternatives are train-fold-fitted char 3–4-mer TF-IDF up to 4096 dimensions (scaled 0.25), frozen mean ESM2 320 dimensions (scaled 0.25 unless noted), or both. All candidates use the identical four group/scaffold-cold folds and target normalization.

| Ridge features | Out-of-fold pooled RMSE | Protein-component macro RMSE |
|---|---:|---:|
| Molecular fingerprint + protein k-mers | 1.487539 | 1.394103 |
| Molecular fingerprint + ESM2 | 1.502328 | 1.388489 |
| **Molecular fingerprint + k-mers + ESM2** | **1.475606** | **1.371095** |

The k-mer + ESM2 fusion beats plain k-mer Ridge by **0.023008 lower macro RMSE** (paired group-bootstrap 95% interval **[-0.033767,-0.012073]**); its pooled reduction **0.011933** has interval **[-0.030146,+0.006335]**, including zero. The Ridge family remains worse than the train-mean baseline on pooled RMSE, so representation fusion alone is not a solved model.

### Fixed ensemble ablation (controlled protein-feature change)

To isolate ESM2's contribution within the stronger model, retain exactly the same **25% ordinary joint chemical/protein-descriptor HistGradientBoosting branch** and add ESM2 only to the **75% Ridge branch**. Preserve nested shrinkage coefficients [1.0,1.0,1.0,0.75] selected inside the earlier scaffold-cold TRAIN folds; do **not** retune shrinkage on newly observed outer labels.

| Nested-calibrated predictor | Pooled RMSE | Protein-component macro RMSE |
|---|---:|---:|
| Corresponding fold-training mean | 1.441784 | 1.362346 |
| Original k-mer Ridge + joint booster | 1.412784 | 1.319430 |
| **ESM2 + k-mer Ridge + same joint booster** | **1.409107** | **1.305516** |

ESM2 augmentation improves macro RMSE by **0.013913** (1.05% of previous macro RMSE), pooled RMSE by **0.003677** (0.26%). The difference is smaller pooled than macro; its uncertainty matters.

### Paired protein-component uncertainty

All confidence intervals below resample **519 heldout protein graph groups** with replacement (5,000 replicates, seed 20261108). Differences are ESM-augmented nested model minus comparator, negative better.

| Comparator | Pooled difference | 95% pooled interval | Macro difference | 95% macro interval |
|---|---:|---|---:|---|
| Original nested k-mer joint ensemble | -0.003677 | **[-0.018014,+0.010930]** | **-0.013913** | **[-0.021845,-0.006113]** |
| Fold-training mean | -0.032677 | **[-0.090710,+0.025283]** | **-0.056830** | **[-0.101173,-0.013927]** |

**Conclusion:** The pretrained protein features make a consistent improvement to **protein-component-macro RMSE** on this exploratory scaffold-cold training-only challenge. There is no 95%-interval evidence of a pooled improvement over the previous nested ensemble or fold-training-mean comparator. Do not claim benchmark supremacy based on the macro result.

### Reproduction

- scripts/cache_balm_train_only_frozen_esm2_8m_dev.py: frozen ESM2 inference for only the 639 BALM TRAIN proteins; writes local compressed feature cache and research/balm_esm2_t6_8m_train_only_feature_manifest_dev.json.
- scripts/compare_balm_train_esm2_8m_vs_kmer_scaffold_cold_dev.py: exact strict scaffold-cold Ridge-feature comparison and group bootstrap, result research/balm_esm2_8m_vs_kmer_strict_scaffold_cold_traincv_dev.json.
- scripts/compare_balm_esm8m_augmented_joint_ensemble_scaffold_dev.py: paired controlled ensemble feature replacement, fixed prior nested betas and group bootstrap, result research/balm_esm8m_augmented_joint_ensemble_scaffold_cold_traincv_dev.json.
- tests_v4/balm_esm8m_train_feature_integrity_test.py and tests_v4/balm_esm8m_joint_ensemble_integrity_test.py.
- Downloaded ESM2 weights and local cached protein vectors are intentionally **not** committed; manifest stores hashes to permit regeneration. Results scripts refuse overwriting existing experiment files.

### Scientific limitations

The public BALM source lacks per-record original assay descriptions/DOIs/construct evidence and includes contradictory repeated identical-input labels. Frozen splits are based on an approximate protein 3-mer similarity graph, not independently validated homology clusters. The pretrained ESM2 encoder truncates 85 longer sequences to first 1,022 residues. ESM2 features are global protein embeddings, not residue-level drug binding predictions. Candidates are informed by repeatedly inspected prior experimental development work, and confidence intervals omit this selection history. This is **TRAIN-only exploratory evidence**, not independent PerceiverCPI/DeepDTA superiority, approved assay-quality benchmarking or scientific proof of a physical interaction mechanism. The reserved prospective test is not evaluated.
