# Frozen inner-development: cold-protein sequence prior

**Status:** exploratory development result. The historical 4,764-pair validation partition has been quarantined, and none of the prospective 2,936-pair test partition was evaluated.

## Method

Three protein-component-disjoint GroupShuffleSplit folds within the 27,118 training pairs (82 training protein clusters) selected a protein-only prior. Each fold fits a train-only character 3–4-mer TF-IDF representation of its protein sequences, aggregates normalized sequence vectors by component, and represents each training component's typical pKd using protein-balanced labels. The three nearest training-component prototypes generate a similarity-weighted estimate for a previously unseen protein. An optional similarity-dependent shrinkage gate pulls low-confidence estimates toward the training-only mean.

Two selection criteria were assessed on the training-only CV folds:

1. **Macro-oriented** — lowest average of pooled-relative and protein-component-macro-relative RMSE, yielding similarity power 4, gate power 0, residual scale 1.
2. **Conservative** — lowest pooled CV error among candidates no worse than the train mean in both pooled and macro CV RMSE, yielding similarity power 4, gate power 2, residual scale 1.

## Results on internal development (20 protein components, 7,387 pairs)

| Method | Pooled RMSE | Component-macro RMSE | Components better than train-mean |
|---|---:|---:|---:|
| Train-only mean | 1.803902 | 1.698289 | — |
| Macro-oriented sequence prior | 1.902174 | **1.453821** | 17/20 |
| Conservative similarity-gated prior | **1.801194** | **1.671521** | 17/20 |

The macro-oriented prior improves **component-macro RMSE by 14.4%** but hurts pooled RMSE by 5.4%. The conservative prior improves both observed point estimates, but its pooled gain is only **0.002707 RMSE (0.15%)**, too small to establish robust improvement.

One held-out development component contains **5,027 of 7,387 pairs (68.1%)**. Its macro-oriented RMSE worsens from 1.8401 to 2.0013, explaining the pooled/macro trade-off. The conservative gate reduces its RMSE to 1.8450, still slightly worse than the train mean for that component.

A 10,000-draw paired *protein-component* bootstrap (seed 20261108) shows:

- Macro-oriented macro RMSE improvement: 0.2445; descriptive 95% component bootstrap interval **[0.1347, 0.3437]**. Its pooled RMSE is worse, and the pooled interval spans both signs.
- Conservative macro RMSE improvement: 0.02677; descriptive interval **[0.01647, 0.03865]**.
- Conservative pooled RMSE improvement: 0.00271; descriptive interval **[-0.00391, 0.04556]**, which includes zero.

**Important limitations:** the development set has been repeatedly inspected, so the bootstrap intervals are descriptive, not confirmatory; only 20 held-out protein clusters; uneven assay/component sizes; assay and construct provenance unresolved. Do not claim independent-test or publication-level superiority.

## Interpretation

The protein-similarity prior carries useful information about new protein clusters, and conservatively gating its correction can improve macro generalization without a large pooled penalty. This is a candidate cold-start architecture component rather than proof that DynaCPI outperforms PerceiverCPI.

Next: test sequence similarity plus molecule-conditioned residuals on *train-only protein-heldout CV*, and lock the resulting architecture before any prospective test evaluation.

**Reproduce:** run scripts/train_bindingdb_cold_protein_prior_dev.py then scripts/bootstrap_bindingdb_cold_protein_prior_dev.py.
