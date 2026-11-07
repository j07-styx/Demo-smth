# DynaCPI development research release — 7 November 2026
## Decision
Do not promote the geometry extension. It improves the frozen sequence pilot by 0.50%, but the sequence-only residual is better on every matched seed. A training-only compound mean is substantially stronger than both. No independent scientific superiority is established.
## Results
Frozen sequence baseline: 0.925685083.
| Variant | Mean macro RMSE | Sample SD | Relative reduction vs frozen |
|---|---:|---:|---:|
| real | 0.921045407 | 0.001717676 | 0.501% |
| shuffled | 0.921662938 | 0.003074576 | 0.435% |
| sequence | 0.920611544 | 0.001777817 | 0.548% |
| no_confidence | 0.921771765 | 0.002927643 | 0.423% |
| head_only | 0.925685083 | 0.000000000 | -0.000% |
| real_head | 0.925685083 | 0.000000000 | -0.000% |

Training-only global mean RMSE: 0.910885500.
Training-only compound mean RMSE: 0.839873400.
Archived local Perceiver CPI common-cohort RMSE: 0.906174614. This is a three-epoch engineering comparator, not a paper benchmark or a fresh retraining.
Real minus sequence residual paired-seed mean: 0.000433862 (positive is worse).
Real-versus-frozen descriptive target-bootstrap interval: [-0.02737681764459232, 0.01809746525663289]. It includes zero. Checkpoint selection used these same validation targets, so this is not an independent inference.
## Data
486 mapped training pairs (nine proteins), 216 validation pairs (four proteins), 54 shared compounds. Exact protein and pair overlap is zero. 368 training and 138 validation labels equal 5.
Global pairwise alignment screening found no pair satisfying both 30% paired identity and 80% bilateral coverage; this does not exclude conserved domain or family leakage. The full pilot contains 24/8 proteins, 1296/432 pairs, and was used for the frozen foundation.
All graph hashes matched. Manifest coverage is 100% for 13 mapped proteins; experimental construct identity is unresolved.
## Architecture and training
The optional new branch projects frozen 256-dimensional protein and compound features to 64 dimensions. Local structural inputs comprise 14 scalar graph-node features and three vector magnitudes. It does not use graph edges and is not a replacement GVP topology model. Softmax compound queries attend over normalized sequence-plus-structure residue features. An MLP produces a tanh-bounded correction of at most 0.25 standardized label units.
All other backbone weights are frozen. Two ablations selectively train only the copied final prediction layer. AdamW uses learning rate 0.001 and weight decay 0.01, eight epochs, batch size eight, anchor coefficient 0.25. Seeds are 1201–1203. Epoch zero is eligible, preventing a worse trained model from replacing the baseline.
The shuffled control permutes node scalars and vectors together within each protein. The sequence-only control omits structural values but retains the same covered residues; active parameter counts are not matched. The confidence ablation removes explicit value weighting but retains confidence as an input feature. No binding-pocket localization claim is made.
## Verification
18 saved checkpoints replayed on all 216 validation pairs; maximum absolute prediction discrepancy 4.76837158203e-07. Numerical differences arise from equivalent reduction paths.
Tests passed for zero-init identity, absent-geometry fallback, bounded corrections, batch independence, residue permutation, rotation invariance and query/structure gradients.
The old GVP gradient probe found zero early-layer gradients before the first update, then nonzero but tiny norms after updates. This is attenuation, not a permanently disconnected path.
## Roadmap
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
## Next scientific decision
Stop treating the frozen three-epoch neural checkpoint as the only meaningful baseline. Retain training-only compound means and sequence-only capacity controls. Repair data viability and freeze an independent domain/family protocol before further model selection. Do not create a test split by relabeling these repeatedly observed validation proteins.
## Reproduction
Use the existing Windows environment and local caches; Python environment inventory is in environment.json. Data and checkpoints are intentionally not in Git.
From the repository root:
```powershell
.\.venv\Scripts\python.exe tests_v4\bounded_structural_fusion_test.py
.\.venv\Scripts\python.exe scripts\audit_roadmap_foundations_dev.py --output research\foundations_new.json
.\.venv\Scripts\python.exe scripts\run_bounded_fusion_study_dev.py --output research\bounded_fusion_study_new
```
Study creation refuses an existing output directory. Analysis/replay scripts currently target the dated study path; change the explicit study path for a new run. Existing caches, source records and old checkpoints are preserved. GVP diagnostic additionally requires the existing installed gvp dependency.
## References and comparison boundaries
Perceiver CPI uses nested cross-attention and was evaluated on Davis, KIBA and Metz; its published benchmark settings differ from this engineering study [1]. Davis et al. is the original kinase-selectivity source [2]. These references do not independently certify our record mappings.
1. Nguyen et al. Perceiver CPI. Bioinformatics, btac731. https://pmc.ncbi.nlm.nih.gov/articles/PMC9848062/
2. Davis et al. Comprehensive analysis of kinase inhibitor selectivity. 2011. https://pubmed.ncbi.nlm.nih.gov/22037378/
