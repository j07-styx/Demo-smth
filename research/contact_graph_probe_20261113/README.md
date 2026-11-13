# Explicit contact-graph pilot — 2026-11-13 (v5.11)

ENGINEERING ONLY. Frozen BALM TRAIN cohort: 5,808 pairs, 298 proteins, 253 groups. Reserved test unscored. This cohort has been inspected repeatedly; bootstrap intervals are descriptive and unadjusted for experiment selection.

## Experiment
Thirty fits: five group folds, two seeds (6111/6112), three matched arms. Each uses identical frozen ESM2-35M residue features, up to 96 uniformly sampled confident residues, 16 neighbors, and the same compound-conditioned message and prediction heads. Real C-alpha distances, sequence-derived distances, and scrambled coordinates differ only in graph inputs. Explicit edges carry 12 radial basis features, log distance, and three contact indicators. Geometry messages have a nonzero 0.1 residual gain. Five fixed epochs, at most 64 batches per epoch; final checkpoints only. Ridge baseline residual targets use inner group-out-of-fold predictions. Corrections are capped at 0.25 raw target units.

## Results
Two-seed prediction averages, lower RMSE is better.

| Arm | Pooled RMSE | Group-macro RMSE |
| --- | ---: | ---: |
| Ridge baseline | 1.556304 | 1.362221 |
| Sequence graph | 1.542909 | 1.343882 |
| Real geometry graph | 1.542005 | 1.343510 |
| Scrambled geometry graph | 1.542276 | 1.343900 |

Real minus sequence pooled delta: -0.000904, descriptive 95% group-bootstrap interval [-0.001887, -0.000159].
Real minus scrambled pooled delta: -0.000271, interval [-0.000964, +0.000311].
The real arm has a tiny numerical advantage but does not clearly beat the stronger scrambled control. No meaningful or independently verified 3D gain is established.

## Mechanism diagnostic
For each of ten saved real-geometry models, change only graph inputs at inference. No affinity labels are loaded by this diagnostic. Mean across-model RMS correction: 0.203545. Mean RMS prediction changes:
- Zero edge attributes, retain real neighbor identities: 0.0001816.
- Substitute sequence graph: 0.0017322.
- Substitute scrambled graph: 0.0025077.

The branch is trainable and functional, yet explicit distance attributes have very little influence in these checkpoints. Neighbor identities matter more, but their predictive benefit remains unproven. These interventions can be out of distribution; they do not isolate the ultimate training failure. Shared protein/compound features can explain most of the residual improvement.

## Validation and limits
Independent validation reproduced all saved metrics, checked all 30 unique fits, exact baseline/source-row alignment, finite predictions, and correction caps. Synthetic checks cover consistent graph permutation, masked nodes, edge sensitivity, compound-conditioned attention and nonzero edge gradients. Cache checks cover rigid-motion invariance and coordinate corruption.

Uniformly sampling 96 residues can miss binding sites and short-range contacts. These are apo predicted structures without ligand poses, frozen sequence features, a shallow graph head and a short schedule. This does not show that structure is intrinsically uninformative. It also does not justify claiming that failure of a descriptor probe predicts failure of every deep 3D model.

## Next experiment decision
Prioritize a training-fold-only diagnostic of correction saturation and within-protein interaction residuals before another architecture sweep. If main effects dominate, compare a centered compound–protein interaction objective against the current residual objective with identical real/sequence/scrambled controls. Separately assess residue coverage around independently identified pockets using label-free structural evidence. Do not select pockets or hyperparameters with reserved-test affinities.

## Artifacts
Four scripts under scripts/: cache_contact_graph_dev.py, train_contact_graph_dev.py, validate_contact_graph_dev.py, diagnose_contact_graph_dev.py. This folder contains protocol, feature manifest, per-fit aggregates, final metrics, mechanism diagnostics and independent validation. Weights, predictions and graph arrays remain gitignored in Demo-smth/research_local. Original core model and other repositories are unchanged.
