# BALM Ridge protein-weight sensitivity and matched negative control

All scores use the frozen 15,538-row train / 3,891-row internal development split, with training duplicates collapsed to 12,315 unique protein–compound inputs. The final test remains held out.

**TRAIN-only grouped CV** over protein-feature scales 0, .25, .5, 1, 2 and Ridge alpha 1, 10, 100 chose protein scale 0.25, alpha 1. Development evaluation:

| Configuration | Pooled RMSE | Protein-group macro RMSE |
|---|---:|---:|
| Training mean after duplicate collapse | 1.589844 | 1.464093 |
| Chemical-only alpha10 | 1.422987 | 1.325383 |
| **Chemical-only alpha1 (proper regularization control)** | **1.403701** | 1.296069 |
| Combined chemical+0.25 protein alpha1 | 1.405092 | **1.269216** |

**Critical matched comparison:** assigning some improvement to the protein modality by comparing combined alpha1 against chemical alpha10 would confound protein features with regularization strength. At the **same alpha1**, protein features make pooled RMSE **0.00139 worse**, while improving component-macro RMSE by **0.02685**. Do NOT claim a pooled protein feature gain.

The selected weighted model improves pooled RMSE by 11.6% and component-macro RMSE by 13.3% versus the corresponding train mean, but most of this arises from chemistry features and Ridge regularization. It is still a good exploratory predictive model.

## Paired cluster uncertainty

A 10,000-draw paired protein-group bootstrap comparing weighted combined alpha1 against chemical-only alpha10 gives a *descriptive* pooled improvement interval **[-0.0481, 0.0779]** and cluster-macro improvement interval **[0.0101, 0.1038]**. The pooled interval crosses zero; no independent-test statistical conclusion is warranted.

## Protein identity negative control

On 32 deterministic trials, reassign training protein sequences randomly to other training protein-feature identities, keeping chemistry and labels fixed, and keep real dev sequences unchanged. Shuffled mean pooled RMSE = **1.40967**, shuffled mean macro = **1.30155**. Actual weighted model pooled RMSE is lower than only 59.4% of these shuffles, but its macro RMSE is lower than **all 32**. This supports the interpretation that the real protein representation contains some cluster-macro information, but not a robust pooled advantage. 32 shuffles are descriptive, not a calibrated p-value.

**Limitations:** repeatedly inspected development, approximate 3-mer rather than validated homology clustering, missing assay-protocol/source provenance, and no reserved test evaluation.

Reproduce using scripts/train_balm_bindingdb_weighted_ridge_groupcv_dev.py and scripts/negative_control_balm_bindingdb_weighted_protein_ridge_dev.py.
