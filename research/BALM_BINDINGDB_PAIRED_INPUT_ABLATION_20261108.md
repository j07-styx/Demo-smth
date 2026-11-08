# BALM cold-protein Ridge paired-input ablation — 2026-11-08

The same frozen train/inner-development split was used for all models: 15,538 raw train rows, reduced to 12,315 unique protein+compound training examples by averaging only training duplicates; 3,891 unchanged development records; 519 training and 173 held-out development protein-3mer graph components.

**All comparisons use fixed Ridge alpha 10**, chosen by three group-disjoint cross-validation folds within training. Train-only feature fitting: L2-normalized 2048-bit Morgan radius-2 chiral fingerprints and protein TF-IDF character 3-4-mers. Development labels are for diagnostics, not model fitting. Reserved 5,271-row test labels were never accessed.

| Fixed-alpha model | Dev pooled RMSE | Component-macro RMSE |
|---|---:|---:|
| Train-only mean after duplicate training aggregation | 1.589844 | 1.464093 |
| Chemical-only | **1.422987** | 1.325383 |
| Protein-only | 1.539357 | 1.408174 |
| Additive chemical + protein | 1.436325 | **1.309695** |

**Interpretation:** chemical features drive a large, credible development improvement over the constant baseline. Protein features improve the mean across equally weighted protein components but make the overall pair-weighted pooled RMSE *slightly worse* than the chemical-only model. Do NOT promote "protein-aware" as a universal advantage. The architecture's pooled and macro objective conflict remains relevant even in this less-imbalanced dataset.

## Negative controls

Twelve deterministic identity permutation trials were trained with one representation's training mapping randomly reassigned, keeping the other representation and the frozen development protein/compound inputs unchanged.

- Shuffle training protein-feature identity, preserve genuine chemistry: pooled RMSE mean **1.45888**, cluster-macro mean **1.35079**. The unshuffled model beats all twelve in *macro* RMSE, but not all twelve in pooled RMSE.
- Shuffle training chemical-feature identity, preserve genuine protein: pooled RMSE mean **1.55382**, cluster-macro mean **1.41988**. The real paired model beats all twelve in both metrics.

These 12 shuffles are a diagnostic rather than a formal randomization hypothesis test.

A 10,000-draw protein-component bootstrap gives a *descriptive* pooled RMSE improvement for the combined model over train mean with 95% quantile interval **[0.05369, 0.25568]**, and macro improvement interval **[0.09991, 0.20985]**. The combined-vs-chemical interval spans zero for both metrics, so a protein-specific advantage is not robustly established.

## Next checks

- Match nonlinear descriptor regressors and sequence-plus-chemistry interaction models under the same training-only CV.
- Retrain upstream PerceiverCPI on this exact development split, reporting fixed epoch and compute budgets rather than selectively chosen validation epochs.
- Confirm homology separation with alignment-based clustering before any independent test claim.
- Verify assay source provenance, which BALM source Arrow does not retain.
