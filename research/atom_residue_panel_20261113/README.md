# Atom/residue real-data fit diagnostic — 2026-11-13 (v5.15)

ENGINEERING ONLY. Four completed fits, one seed (7133), 200 fixed updates each, batch 8, AdamW lr 0.001 and weight decay 0.01. No checkpoint selection or tuning from these results.

## Data and model
64 training rows from four proteins/groups and 64 held-group rows from another four proteins/groups, all drawn from the previously reused frozen BALM TRAIN bundle. Selection uses existing ordering and molecule/protein eligibility, not labels: 16 distinct SMILES per protein, full molecules of at most 96 atoms. Larger molecules are explicitly ineligible; selected molecules are never truncated. This tiny convenience panel is not representative or an independent test.

SMILES and protein sequences are recovered from source metadata at exact verified TRAIN row indices. Source protein hashes match the bundle. Complete RDKit bonds and atoms feed the new interaction model. Pretrained residue caches and bundle hashes are checked. Features and targets are normalized on training data only. The four controls use chemical-only (constant protein input), ESM2 sequence, real SaProt, and structurally shuffled SaProt features. Sequence-vs-SaProt also changes pretrained encoders; real-vs-shuffled is the closer structure control.

## Results
| Arm | Train RMSE | Held-group RMSE | Train within-protein RMSE | Held within-protein RMSE |
| --- | ---: | ---: | ---: | ---: |
| Constant train mean | 1.762829 | 1.741742 | 0.750876 | 1.149006 |
| Chemical only | 0.279797 | 1.820683 | 0.237313 | 1.212472 |
| Sequence | 0.264088 | 1.934855 | 0.229566 | 1.129019 |
| Real structure | 0.259692 | 1.952780 | 0.230068 | 1.137994 |
| Shuffled structure | 0.250950 | 1.773211 | 0.234252 | 1.146221 |

Within-protein RMSE centers errors separately per protein for descriptive scoring; it is not deployable calibration with held labels.

## Interpretation
The real-data training-fit gate passes: the uncapped model reduces both total and within-protein training errors substantially. It is not universally unable to learn chemical variation. However, every learned model is worse than the constant train mean on held-group pooled RMSE. Real structure does not beat sequence or shuffled structure. This small experiment reveals a large fit-transfer gap, not a geometry benefit.

Chemical-only also fits training well. Therefore low training loss does not prove atom-residue interaction learning or meaningful structural dependence; it can reflect chemistry memorization. Unlike the earlier synthetic factorial, this real panel does not eliminate chemical main effects. The tiny training size makes overfitting unsurprising. Do not conclude that the entire architecture or 3D field fails from this panel.

## Validation and remaining limitations
Independent validator reproduces all saved metrics and checks exact membership in frozen TRAIN, 64 rows per role, four distinct proteins per role with 16 rows each, group separation and finite predictions. Checkpoints and raw predictions are local and gitignored.

Residue features still use the existing 96 uniformly sampled tokens, not full proteins or verified pockets. This is deliberately a cheap fit diagnostic and does not resolve the residue-coverage issue. Assay/construct comparability remains unknown. No SPMM pretraining or GenSPARC reproduction is claimed. The cap and training objective differ from earlier residual models, so compare only the matched arms within this diagnostic.

## Next decision
Do not promote a model from this panel or tune it against these eight proteins. Before broad affinity training, improve and audit residue coverage and obtain chemically pretrained atom representations or a credible bond encoder training plan. A transferable interaction pretraining task and/or verified contact supervision is a hypothesis worth testing; more steps on the same four training proteins is not evidence of progress. Retain explicit compound-only and shuffled-structure controls. Reserved test stays unscored.
