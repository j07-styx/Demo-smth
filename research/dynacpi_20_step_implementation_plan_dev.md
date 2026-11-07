# DynaCPI 20-step roadmap

Updated 7 November 2026. Development execution is not scientific completion.

| Step | Status | Evidence / limitation |
|---|---|---|
| 1 | COMPLETE | Existing registry; new study has an isolated protocol and 18 run records. |
| 2 | COMPLETE (development audit) | Exact sequence/pair/canonical compound/scaffold overlap plus 192 global alignments. Domain-family leakage remains unresolved. |
| 3 | BLOCKED (experimental verification) | 13 graph hashes verified during loading; mapping manifest reviewed; assayed constructs remain unverified. |
| 4 | BLOCKED | No source-reviewed independent cohort or frozen family-disjoint split. Existing validation has been repeatedly used. |
| 5 | IN PROGRESS | Floor counts audited; original units/censoring and record-level experimental meanings not independently verified. |
| 6 | COMPLETE (development checkpoint parity only) | Recomputed sequence baseline 0.9256850828. Full matched scientific baseline remains blocked by step 4. |
| 7 | COMPLETE (development diagnostics) | Old GVP path gradient probe plus per-layer gradients for all new trainable variants. |
| 8 | COMPLETE (development sensitivity) | Prediction changes, shuffled features, disabled geometry, rotation and permutation tests. |
| 9 | COMPLETE (development controls) | Three matched seeds for real, shuffled and sequence-only residuals, plus disabled geometry via head-only ablation. |
| 10 | COMPLETE (development analysis) | Train/validation trajectories and per-target harms recorded; two of four targets harmed by real fusion. |
| 11 | COMPLETE (development implementation) | Layer-normalized residue fusion with scalar correction bounded to 0.25 standardized label units; opt-in. |
| 12 | COMPLETE (development implementation) | Differentiable compound-query softmax residue weights; not a verified binding-site predictor. |
| 13 | COMPLETE (development implementation) | 64-dimensional compound/sequence/local-structure attention with direct output residual. |
| 14 | COMPLETE (limited development ablation) | Dropout, weight decay, anchoring and confidence value weighting tested. no_confidence removes weighting, not confidence input features. |
| 15 | COMPLETE (negative development experiment) | Last prediction-layer tuning tested with and without fusion; epoch-zero model wins all six runs. |
| 16 | COMPLETE (development ablations) | Six variants times three seeds; no claim of exhaustive architecture or parameter-matched capacity comparison. |
| 17 | COMPLETE (development multi-seed study) | Means, sample SD, paired seed effect and descriptive target bootstrap. Four targets, not independent families. |
| 18 | BLOCKED | No untouched verified holdout; no test-set evaluation performed. |
| 19 | IN PROGRESS | Archived local Perceiver predictions scored on same 216 pairs; full matched paper-baseline reproduction and independent comparison blocked. |
| 20 | IN PROGRESS | Development source/report/manuscript/reproduction package prepared; final scientific release blocked by steps 3-5,18-19. |

Evidence: research/roadmap_release_20261107/REPORT.md. New development study: research/bounded_fusion_study_20261107 (local).
