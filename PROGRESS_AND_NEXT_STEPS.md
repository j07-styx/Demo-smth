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

## Two source methods reveal concrete construct-input alignment risks (6 November 2026)

The primary paper for candidate P17342 reports receptor residues 27–541, while the candidate BindingDB sequence is the 541-residue canonical reference. Another paper reports NRP1-b1 residues 273–427 while its candidate record stores the 923-residue O14786 reference. These are primary-source **region evidence**, not full chemical/assay validation. Both records require explicit physical construct sequence mapping, tags/variant verification, original Kd table-to-record review and source assay comparability before inclusion.

The additional check brought the engineering suite to **19/19 PASS** with zero approvals; construct risk evidence and hashes are in research/source_access_v4 and data/audit. Next researcher should resolve these two documented examples, then expand systematic source review across enough independent protein families before freezing any scientific split. Never treat a reference match as evidence that the assay used the full canonical sequence.

## Latest reviewer triage priorities — 6 November 2026

The fixed 30 unapproved candidate assays are now grouped by **metadata ambiguity, not scientific validity**: P0 four, P1 twelve, P2 fourteen. Start source inspection with P0 (CFTR half-effective-concentration wording, GLP1R versus glucose assay wording, absent PD-L1 description, missing CA2 primary identifier). Then prioritize fragment/complex/endpoint interpretation, including the VHL/Elongin partner-chain numeric range; afterward review remaining primary papers and patents. Every task still requires a qualified original-source method and per-record exact-Kd check, regardless of priority or lack of metadata flags.

The triage script and results are in `scripts/triage_30_assay_metadata_v4.py` and `research/source_access_v4/ASSAY_METADATA_TRIAGE.md`. The nine-task VS Code workflow and hourly benchmark observer expose current review status. The **20/20 engineering checks** are green; the primary scientific gate is BLOCKED because zero tasks have source approval and there is no frozen protein-cluster test split. Do not present the metadata rankings as new model or benchmark performance.

## Next source-review actions after 6 November 2026 P0 evidence crosswalk

Four P0 candidate assays now have primary evidence **leads** at research/source_access_v4/P0_SOURCE_CROSSWALK.md. Their metadata source tiers are publication abstract, assay registry, DOI-only bibliographic metadata and original patent locator. None of the four has verified all source-table binding measurements or approved experimental constructs; all 30 candidate tasks remain UNREVIEWED.

1. Ask a qualified reviewer to reconcile the source assay's measured participant and endpoint with the exact candidate task record, especially the two apparent source-method/target-label disagreements; do not auto-reject records from an abstract or registry summary.
2. Source index correction: the carbonic-anhydrase task has DOI-only bibliographic provenance, **not** an absent source identifier; independently inspect its methods and original data.
3. For the patent-only review task, locate the original assay table and physical protein construct. A patent title alone is insufficient.
4. After actual physical constructs, exact-Kd source qualifiers, units, source-table identifiers and assay compatibility have been independently adjudicated across enough unrelated families, freeze the approved cohort/split and perform matched D-vs-B scientific evaluation. Until then the original fail-closed gate stays BLOCKED.
5. Review the new P0 crosswalk and run the 21-check suite from VS Code; no source-approved BindingDB training or independent gain claims exist.

The updated hourly observer reports meaningful source changes and GPU/engineering test failures but does not train or approve a dataset.

## 6 November 2026 — 921/921 raw source reactants technically reconciled

Remote execution resumed on built-diff12. The new record-lineage audit reconciled all 921 original BindingDB reactant IDs to 919 compound-group observations and 921 unaggregated candidate rows. Five independent synthetic cases and the real-audit integration check passed; the expanded engineering suite is **23/23 PASS**, zero failures. Report: research/source_access_v4/RECORD_LEVEL_PROVENANCE_30.md, including original input SHA-256 and zero critical processing discrepancies. This confirms arithmetic/data construction, NOT scientific eligibility or model predictive gain.

The scientific blocker is the same: all 30 fixed Kd candidate tasks still UNREVIEWED and not source-approved. The next work is original paper/patent method-to-measurement adjudication and experimental construct alignment, using the P0 source crosswalk and primary-source review worklist. Do not claim a solved assay mislabel from metadata alone. The project is already ready to run checks from 11 VS Code tasks and is watched by the existing hourly read-only benchmark observer. Do not enable training on these candidates until a scientifically approved cohort and independent family roles exist.

## 6 November 2026 — 921-record source evidence worksheet is ready for qualified review

All 921 raw BindingDB source records in the fixed 30-task sample now have local worksheet rows with identifiers and fields for original publication/patent method/table evidence, true experimental binding participant, assayed protein construct hash, exact Kd endpoint/qualifier, assay compatibility and reviewer approval. These are **blank review fields**; all 921 records remain UNREVIEWED. The worksheet at data/audit/source_record_evidence_worklist_30_LOCAL_PRIVATE.csv stays PRIVATE on the original Windows computer, never GitHub. The generator/validator preserves existing entries, checks source identity and supports future review updates without overwriting them; it is NOT an automatic approval authority.

Reviewers should examine the P0_SOURCE_CROSSWALK.md and ASSAY_METADATA_TRIAGE.md first, then independently inspect each paper/patent assay method and match each source record. Use `scripts/build_record_source_evidence_worklist_v4.py` to validate progress, checking the public `RECORD_SOURCE_EVIDENCE_READINESS.md`. The next source-approved cohort and frozen group split cannot be generated until enough verified independent protein groups exist. The research model results remain development-only; no new source-Kd training or test exists.

## Latest scientific design decision — three-seed factorial model evaluation, 6 November 2026

The three-seed REAL frozen geometry-versus-sequence calibration comparison is complete. See research/geometry_factorial_dev/SUMMARY.md and factorial.json. At K5 sequence-only calibration RMSE 0.857337; geometry-mixture calibrated RMSE varies 0.860139, 0.855587, 0.854164 across seeds. Differential support adaptation adds virtually zero benefit (G_D-G_B < 6e-9 at K5). Exactly 2 of 4 development targets benefit per seed, effects strongly target-dependent. This contrasts separate geometry main effect from centered support-dependent incremental correction.

**Engineering code 26/26 PASS; NO robust independent scientific evidence of model superiority.** This is an experimental negative/unstable result under unchanged model settings. The remaining scientific dependency is actual primary-source verified exact-Kd assay/construct data across enough independent protein families, then a frozen group split and paired matched D-vs-B/S_B evaluation. Do not overfit the same development quartet to create an artificial gain. If considering a redesign, preregister it and validate on genuinely new family-held-out approved targets.
