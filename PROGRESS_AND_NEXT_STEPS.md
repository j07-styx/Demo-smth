# DynaCPI v4 — Progress and prioritized next steps

**Last verified engineering checkpoint:** 5 November 2026. **Scientific model performance claim:** None. **Architecture:** DynaCPI v4, two predictors and support adaptation.

## Already completed

- Original archived PerceiverCPI fold-zero DAVIS inference parity: 1,148/1,148 matches.
- ESM-2 650M embeddings extracted and audited for 462 staged sequences; large tensors omitted from Git.
- GVP graph implementation and 13 sequence-exact mapped AlphaFold pilot structures, with actual nonzero ROCK2 residue offset handling.
- Full November 2026 BindingDB audit and preliminary construct/assay/chemical duplicate/sequence family screens.
- 1,146 provisional tasks usable for K=5 *by counts only*, 377 candidate K=20 tasks; 168 preliminary sequence components.
- Quarantined pre-split episodes, leak-guarded support/query loader, fail-closed scientific cohort gate, preliminary label-blind five-role allocator.
- Thirty-task metadata-only source review sheet, indexed source dossier and UniProt/reference checks. ZERO scientific approvals.
- Sequence-only DAVIS engineering pilot, three supervised epochs; geometry GVP pilot, two supervised epochs; saved checkpoints and raw histories.
- Factorial A/B/C/D frozen adapter integrated with real RDKit chemical inputs; preliminary real-affinity DAVIS support development diagnostics.
- Construct-balanced paired evaluator with synthetic 3,600-row statistical tests.
- 15/15 prior full engineering checks passed on original source machine.

## Highest-priority work queue

| Priority | Job | Input / files | Completion criteria |
| --- | --- | --- | --- |
| P0 | Validate local clone and dependencies | provenance/snapshot_file_manifest.json; REPRODUCIBILITY.md | Source and checkpoint SHA verified, environment and missing ESM cache accurately identified |
| P0 | Audit actual Kd source evidence | 30-task review CSV and source dossier | Reviewer-supported construct, protocol, measurement type, qualifiers, units and same-assay comparability; recorded references; unverified cases rejected or flagged |
| P0 | Produce scientifically valid larger cohort | Full BindingDB and source reviews | Approved exact-Kd cohort with documented inclusion/exclusion policy, complete provenance and independent secondary review |
| P0 | Freeze protein-group roles | MMseqs2 + domain homology policy | Five disjoint source-approved protein-group roles and immutable hashed manifest; no query-label-dependent selection |
| P1 | Portabilize tests and data paths | tests_v4, scripts, excluded cache | Named environment variables for external legacy baseline and ESM cache; explicit dependency skips and deterministic test report |
| P1 | Source-provenance regression tests | review gate + cross-assay overlaps | Forbidden cross-assay/query-label cases hard fail; checksum mutation fails |
| P1 | Reproduce baselines on approved splits | original PerceiverCPI, ESM foundation | Matched seeds, test episodes, preprocessing and model-selection budget; saved stage1 checkpoints |
| P1 | Train stage-2 GVP correctly | approved mapped graph cohort | Frozen sequence model, sequence-aligned N/CA/C/O geometry and missingness; independent base-validation ablations |
| P1 | Establish geometry complementarity | s vs g predictions on development roles | Analyze disagreement V, reliability vs structure quality, per-target harms and effective sample counts |
| P1 | Tune calibration and differential on adapter validation | A/B/C/D plus simple controls | No test contamination; fixed hyperparameters and support K draw identities before final test |
| P2 | Final paired evaluation | source-approved test component cohort | Task->construct->component macro metrics, paired target bootstrap CI, 3 seeds, at least 10 draws where feasible |
| P2 | Final manuscript | research/DynaCPI_Manuscript.md | True results, clear negative findings, methods, baselines, ablation tables and evidence provenance |

## Stop/go rule

If approved tasks, independent protein components, exact endpoint semantics or support assay compatibility are missing, do NOT train a headline scientific model. Keep doing unblocked engineering and manual source work, and report the blocker.

## Known issues to revisit

1. Geometry underperforms sequence-only in the 9/4 DAVIS development pilot: macro 0.935921 vs 0.925685.
2. Differential D and calibration B are indistinguishable in four-protein development pilot, because support kernel evidence W and centered disagreement V are extremely small.
3. Engineering validation proteins were also used to select the geometry checkpoint; all development metrics are biased if treated as a blind final test.
4. Many candidate assays lack pH/temperature or source proof, even with a matching database accession.
5. Large imbalanced protein components (one 492-task component) complicate naive task-balanced splits; use independent component-level inference.
6. Some test scripts retain old absolute Windows paths and require ESM caches excluded from this Git checkout.
7. The saved sequence checkpoint is final epoch 3, not best epoch 1.
8. Real Kd censoring and BindingDB cross-assay duplicates need scientifically correct semantics and provenance before use.

## Success criteria

A scientifically meaningful DynaCPI v4 claim requires a source-verified exact-Kd cohort, locked independent protein groups, frozen s/g predictors, matched support episodes, and an observed D-vs-B gain with a predeclared effect size and paired protein-component uncertainty. A negative result may be a valid research outcome but must not be hidden.

## Revised immediate work after 6 November 2026

The 5 November list remains scientifically applicable. The current engineering extension has tested K up to 20 and three geometry seeds, with stable *null differential* D−B on the same four development kinases, despite geometry accuracy shifting with seed. The last full suite passed 17/17.

1. **Highest priority is still independent source review**, not another lucky initialization: retrieve actual paper/patent evidence for the thirty sampled BindingDB Kd assays, verify physical construct and exact endpoint/qualifiers, record evidence and reviewer justification, reject unsupported candidates.
2. After enough construct-verified, assay-compatible tasks spanning truly independent protein families exist, freeze five family-disjoint roles and query/support draws. Ensure source overlaps and domain-level similarity cannot leak between roles.
3. On SOURCE-APPROVED development roles, investigate why s/g support disagreement covariance and weighted variance V are tiny. Include controlled structure quality and complementarity diagnostics before any model or regularizer revision.
4. Reproduce matched sequence and geometry baselines across multiple seeds, report each fixed epoch and distributions; do not select a favorable seed using final test targets.
5. Only after split and experimental design are locked, perform primary D versus calibration-only B paired cluster evaluation. Keep negative outcomes, task counts and uncertainty intervals.
6. Check source project.md and manuscript Section 7.10 for all observed 6 November development metrics. Run the VS Code status task to inspect updated benchmark files; hourly monitoring only reports meaningful changes.

## Source evidence — immediate queue status at 6 November 2026

A reproducible source-access index and read-only review-action checklist have been generated for the 30 sampled exact-Kd candidates. All 20 distinct public PubMed IDs were resolved, but only two papers had a usable public full-text section index; 17 remained metadata-only and one open-access XML was rejected for safety. At the task level the reviewer action counts are 2 OA-indexed, 20 needing source article access, 7 primary patent and 1 missing identifiers. All **30 are still unreviewed**; zero scientific approvals.

1. An authorized qualified reviewer must inspect the original source methods and necessary supplements and record the actual physical construct and outcome evidence for each task; article keyword hits are insufficient.
2. Resolve missing original publication information and any inaccessible XML using safe, permitted source-access routes; do not bypass publisher restrictions.
3. Record supported source review decisions only in the canonical human reviewed file; leave unknown or uncertain tasks quarantined.
4. Run scripts/validate_assay_reviews.py plus scripts/run_v4_validation_suite.py; the latest suite is 18/18 passed, but this is not a source approval.
5. After enough independent assay targets are actually verified, produce the source-approved cohort with traceable evidence and freeze independent protein-group roles. Only then return to model training and paired D-versus-B evaluation.

All original model checkpoints, DAVIS pilot conclusions and source metadata from the upstream PerceiverCPI clone were preserved.
