# Nonlinear descriptor baseline on BALM cold-protein development

Fixed input cohort: 12,315 unique train sequence+compound pairs, 3,891 unaggregated development rows, disjoint protein 3-mer graph components. All source assays and constructs remain unverified; reserved test untouched.

**Model:** sklearn HistGradientBoostingRegressor (180 trees, learning rate 0.05, 15 max leaf nodes, depth 5, min leaf 40, L2 regularization 15), plus 21 molecular physicochemical descriptors and optionally 21 protein amino-acid composition features. Component-weighted sample fit used inverse sqrt protein-component frequency, and unweighted fit was included as a separate ablation. All four models were selected using three protein-group-heldout folds within TRAIN, before inspecting inner-development predictions.

| Model | Inner-dev pooled RMSE | Protein-component macro RMSE |
|---|---:|---:|
| Train-only mean | 1.58984 | 1.46409 |
| Chemical descriptors only | 1.41976 | 1.32411 |
| Chemical + protein composition | 1.43952 | 1.29956 |
| Chemical only, component weighted | **1.41052** | 1.30943 |
| Chemical+protein, component weighted (**CV-selected**) | 1.49662 | **1.29931** |
| Morgan+protein k-mer Ridge, CV-selected alpha1 scale.25 | **1.40509** | **1.26922** |

Although training-only group CV favored weighted chemical+protein gradient boosting, this advantage did not transfer: selected model pooled RMSE 1.49662, worse than chemical-only descriptor model and matched Ridge. Macro RMSE of the selected model remains below its own mean baseline, but not the best Ridge configuration. This is a valid negative development result, NOT an improvement claim. It supports retaining the simpler calibrated model as a leading development candidate.

**Caveats:** group split is protein trigram similarity rather than validated MMseqs2 alignment homology, dataset no original experimental source DOI/method, same-input affinity disagreements persist, inner-dev repeatedly inspected, and the prospective 5,271-row test never evaluated.
