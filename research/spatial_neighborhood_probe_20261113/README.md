# Same-encoder spatial-neighborhood probe — 13 November 2026

ENGINEERING ONLY. All changes and new outputs are confined to Demo-smth; existing dynacpi_v4 public-data/encoder caches were read only. dynacpi-better-version/DynaCPI-Backend was neither read nor modified in this experiment. The objective is incremental value attributable to 3D, not the separate 2D benchmark wins.

## Controlled change
Every arm uses the same frozen ESM-2 35M residue embeddings and the same confidently mapped residues (pLDDT>=70). Up to 96 uniformly spaced centers are shared across arms. For each center, retain half of its embedding and add half the average of 16 neighbors:
- spatial: nearest C-alpha positions;
- sequence: nearest sequence indices;
- corrupted: nearest positions after a fixed within-protein coordinate permutation.
Neighbors exclude the center; no labels enter this preprocessing. A fourth model uses uniform pooling of real spatial features instead of compound-conditioned attention.

Spatial and sequence neighborhoods overlap by 59.38% on average: approximately 40.62% of members differ. Mean confident reference-sequence coverage is 77.61%. This is not a binding-pocket extractor and does not supply a ligand pose. Coordinates influence neighbor assignment, not explicit learned distance/orientation edge features.

## Results
Forty fits, five TRAIN group folds, two seeds, four arms. Same fixed five-epoch, bounded +/-0.25 residual protocol as v5.6, against the same group-cross-fitted shared ridge baseline. Reported metrics average the two seed predictions before scoring.

| Arm | Pooled RMSE | Group-macro RMSE |
|---|---:|---:|
| Shared ridge baseline | 1.556304 | 1.362221 |
| Sequence-neighbor attention | 1.545216 | 1.348271 |
| Spatial-neighbor attention | 1.544658 | 1.347727 |
| Scrambled-coordinate attention | 1.546621 | 1.348250 |
| Spatial-neighbor uniform pooling | 1.545643 | 1.345651 |

Spatial minus sequence: pooled -0.000559, conditional 95% paired group-bootstrap CI [-0.002064,+0.000610]; macro -0.000544 [-0.002584,+0.001589].
Spatial minus scrambled: pooled -0.001963 [-0.006632,+0.002151]; macro -0.000523 [-0.003667,+0.002627].
Spatial attention minus spatial uniform pooling: pooled -0.000985 [-0.006147,+0.004872]; macro +0.002076 [-0.001050,+0.005405].

All paired intervals cross zero. The numerical improvement over sequence is too small and uncertain to claim meaningful geometry utility. Attention still averages broadly: effective coverage averages 95.64%, ranging 81.92%-99.49% across ten spatial fold/seed runs.

## Interpretation and next boundary
This removes the earlier SaProt-vs-ESM pretraining confound and changes genuine 3D connectivity, but changing neighborhood membership scarcely changes predictive accuracy. Local averaging of contextual embeddings is not enough in this pilot. The results do not prove 3D is uninformative; short training, uniform centers, absent ligand geometry, indirect use of distances and frozen encoders constrain the test.

Do not launch another sweep of this pooling design. A materially different next experiment should preserve explicit contact/edge geometry or introduce label-independent binding-region information with ligand-conditioned interactions. It must retain this same-encoder sequence and coordinate-corruption control. Any further development on this repeatedly inspected cohort remains exploratory; keep the reserved test untouched.

## Validation and reproducibility
cache_spatial_neighborhood_dev.py passed rigid rotation/translation invariance, coordinate-corruption sensitivity, and sequence-control coordinate-independence checks. All pooled caches reproduce the source protein order and masks; source encoder file hashes checked against the existing provenance. Full ESM mean reconstruction matches prior caches within 5.73e-6.

train_spatial_neighborhood_dev.py passes the inherited model masking, permutation, compound-dependence, uniform pooling, gradient and correction-bound checks. validate_residue_attention_probe_dev.py independently reproduced all seed/ensemble metrics, checked 40 unique fold/seed/arm runs and bounded corrections, and matched the original shared baseline exactly. All 5,808 rows and 253 groups retain the frozen TRAIN-only partitioning.

Source scripts and aggregate JSON are versioned. New feature arrays, weights, predictions and logs are in gitignored research_local inside Demo-smth. No model defaults or reserved-test scores changed.
