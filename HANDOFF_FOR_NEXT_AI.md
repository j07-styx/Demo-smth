# DynaCPI v4 — Exhaustive handoff for the next AI engineer

**Snapshot source:** 5 November 2026. **GitHub:** https://github.com/j07-styx/Demo-smth.
**Source machine:** Windows, originally C:\Users\J0124\dynacpi_v4.
**GitHub handoff checkout:** C:\Users\J0124\Demo-smth.
**Model architecture:** DynaCPI v4.0 (two predictors with support-conditioned adaptation; NOT four MoE experts).
**State:** Software functional; preliminary DAVIS supervised pilots trained. Scientifically approved BindingDB cohort NOT established. Publication-level novel improvement NOT demonstrated.

## 0. Critical interpretation before doing anything

The repository's GitHub commits are version **0.1–0.4** solely to organize snapshots and dated uploads on 5 November 2026. They are NOT different neural architectures. DynaCPI v4 remains unchanged during repository export. Do not discard the two-predictor design to implement the older MoE because of a confusing commit name.

This repository includes source, configs, compact verification reports, preliminary BindingDB candidate manifests, small structure fixtures, three pilot model checkpoints and the research draft. It deliberately excludes large original downloads, pretrained ESM model weights and ESM feature tensors; therefore a fresh clone is **not** immediately a self-contained live-training environment. See REPRODUCIBILITY.md.

## 1. A precise goal you must preserve

Study compound–protein experimental dissociation affinity on previously unseen protein targets. The measurable question is whether the information in a small **support set of same-assay known affinities** lets us exploit geometry-vs-sequence prediction differences beyond ordinary support-residual calibration.

The primary contrast is:
- B = a shared fixed zero-shot prediction plus support-derived calibration.
- D = exactly the same baseline and support-derived calibration PLUS centered structure/sequence differential adaptation.
- All model backbones must be frozen during that adapter comparison, with equal support observations, split roles, tuning budget and query sets.
- Primary metric is component-balanced regression RMSE for K=5, with paired component bootstrap confidence intervals; 2% relative reduction was a provisional hypothesis, not a guaranteed threshold or achieved observation.
- K=0,1,2,5,10,20 curves and ablations A/B/C/D are planned. K=20 only on sufficiently large eligible tasks.

Do not mistake KIBA composite bioactivity for pKd. DAVIS may have a censoring/assay ceiling around 10,000 nM; provenance of each source must be verified before treating it as an exact quantity.

## 2. Model and math

Open these exact modules and their tests. Avoid reimplementing their algebra from prose:
- dynacpi/sequence_model.py: shared neural compound/sequence interaction predictor; ESM-2 650M embeddings projected from 1280 to 256 hidden channels.
- dynacpi/mpn.py: molecular graph feature backbone.
- dynacpi/backbone_graph.py: real backbone N/CA/C/O geometry, residue graph and masks/quality.
- dynacpi/geometry_branch.py: trainable three-layer GVP geometry path with exact missing-structure fallback.
- dynacpi/adaptation.py: analytic constrained support calibration and centered differential ridge correction.
- dynacpi/frozen_adapter.py: chirality-aware Morgan radius 2 / 2048 bit, Tanimoto power 4; immutable support/query means; four A/B/C/D outputs, and K=0.
- dynacpi/frozen_pair_predictor.py: prediction from frozen stage-1 and GVP weights with saved training label mean/std correctly restored to raw pKd.
- dynacpi/episode_data.py: split between prediction inputs with support y and evaluator-only query y.
- dynacpi/scientific_cohort_gate.py: fail-closed source-approval + frozen split artifact verifier.
- dynacpi/group_split.py: provisional label-blind component allocation.
- dynacpi/paired_evaluation.py: paired query RMSE, mean episodes per assay task, mean tasks per construct, mean constructs per protein component, then macro component average and paired bootstrap CI.

Base prediction m0 uses fixed w0 mixing of s and g. For K>0 the adapter learns analytically from support residuals and centered structure-minus-sequence disagreements, using kernel weights rather than a trainable expert router. Output D = m0 + b + delta. Data-dependent b and delta have explicit caps. When geometry is absent, g must equal s and differential delta=0. K=0 is exact zero-shot behavior. All inference inputs must be processed via a frozen-predictions map keyed by canonical compound identity.

Default engineering settings: w0=.5, lambda_b=5, lambda_theta=.1, |b| capped 2 pKd, |delta| capped 1 pKd, Tanimoto exponent 4. These are provisional and could suppress differential adaptation. Test changes ONLY on a designated adaptation validation partition.

## 3. Original baseline parity

The original PerceiverCPI checkout is preserved separately at C:\Users\J0124\OneDrive\Desktop\perceiver_cpi. It was read, not modified during v4 handoff.
- 1,148 / 1,148 archived fold-zero DAVIS predictions were exactly reproduced from FINAL_model0_best.pt using exact original preprocessing and 50-row batching.
- Six original reference source files were byte-identical at the time of verification.
- Evidence: research/legacy_checkpoint_parity.json; tests_v4/legacy_checkpoint_parity.py.
- The legacy checkpoint on the original PC may not be inside this Git repository. A fresh clone needs that original baseline checkpoint from trusted user storage to rerun parity; do not report absence as a DynaCPI implementation failure.
- IMPORTANT: the *pilot_perceiver/checkpoint.pt* in the repo is a separate three-epoch engineering checkpoint, not the legacy archived baseline above.

## 4. Protein embeddings and structures

The original workflow downloaded official ESM-2 650M model weights and generated 462 cached protein sequence embeddings. Cache settings live at data/esm2_t33_650M_layer33_w1000_o128_fp16/settings.json; cache files are excluded from Git because they total roughly 848 MiB.
- Stage sequence dictionary: data/staging/sequences.json; sequence hashes are SHA-256 of full amino-acid strings.
- Extractor: scripts/extract_esm.py; integrity checker: scripts/audit_esm_cache.py.
- Previous full check: 462/462 feature files, 346,865 amino-acid positions, 570 windows, no missing or nonfinite values.
- A new machine must restore correct model weights and embeddings with matching content, shapes, FP16 dtype, window coverage and extractor metadata.
- One canonical BRAF AlphaFold structure was checked with 766 residues, 18,789 directed graph edges, real PAE, correct nonzero geometry gradients and exact fallbacks. See research/cached_esm_gvp_pair_smoke.json and research/full_inference_real_3d_synthetic_labels_test.json.
- Pilot target mapping: data/engineering_pilot/uniprot_exact_subsequence_survey.json. 30 of 32 DAVIS pilot proteins exactly mapped to a contiguous human UniProt reference region. ROCK2 pilot sequence is residues 686–1388 of reference O75116. Do not reuse full-length sequence coordinates without offset mapping.
- Limited pilot AlphaFold v6 graphs were staged for nine train and four val targets, stored in data/engineering_pilot/structure_graphs/<sequence-hash>/graph.pt; source PDB/PAE source provenance and graph SHA in each local manifest. 100% mapped complete-backbone coverage was reported for these 13 selected regions.
- Official reference match is NOT scientific verification of the actual construct used in an assay.

## 5. BindingDB dataset audit — precise status

Source: Full November 2026 BindingDB ZIP; 594,284,548 compressed bytes, roughly 9 GB TSV decompressed. Original on-disk archive integrity checked with ZIP CRC; companion publisher MD5 URL unavailable at that point; SHA-256 recorded in local manifest. The ZIP is omitted from Git.
- Scanned records: 3,243,660.
- Populated Kd fields: 131,531.
- Positive numerically exact-looking Kd values: 82,481.
- Preliminary single-chain, sequence, SMILES, assay-linked candidates: 80,139.
- Preliminary chemistry/identity-filtered observations: ~80,034, yielding 78,493 within-task canonical-compound median records.
- Preliminary task count: 15,145 construct-assay candidates. 1,146 tasks have >=15 distinct compounds, 377 >=30.
- MMseqs2 connected components over preliminary eligible sequences: 168 at K=5 cohort and 81 at K=20; the largest K=5 component contains 492/1,146 tasks.
- Source/assay identity caveats: experimental construct may differ from database reference; assay IDs/terms are not sufficient to prove same experimental method; compound source overlap and chemistry can create leakage.
- 185 protein sequences have multiple K=5-eligible assay tasks; 114 had cross-assay compound identity overlap, with 1,933 distinct query-to-other-assay-support compound identities. These identity overlaps are POTENTIAL leakage channels, not evidence of the same experimental result.
- Pre-split 1,146 candidate K5 episodes and 377 K20 tasks pass task/compound/query/support identity tests. They are **not** permitted final training examples.
- A label-blind 30-task manual evidence queue representing 30 preliminary components was prepared at data/audit/bindingdb_assay_manual_review_queue_30_ENRICHED.csv.
- Official UniProt references matched all 30 database sequences exactly; 20 distinct PubMed references resolved, seven tasks were patent-only, 13 descriptions contained extra construct/method review clues.
- ALL 30 tasks remain UNREVIEWED. ZERO have scientific source approval.
- Files: research/BindingDB_30_Source_Evidence_Dossier_20261105.md; research/Kd_Curation_and_Split_Protocol.md; data/audit/*provenance*, *review*, *cohort*, *episode*, *mmseqs* reports.
- The current source-approval gate MUST block final scientific training. This is intentional.

## 6. True implementation progress and negative results

### DAVIS engineering pilot (not a science benchmark)

Source: data/engineering_pilot/rows.json and data/engineering_pilot/protocol.json. Train and validation target identifiers are disjoint, but independent protein-family isolation and exact experimental source provenance are not established.

Sequence foundation:
- 24 train protein identifiers / 1,296 pairs.
- 8 validation identifiers / 432 pairs.
- Three supervised epochs with cached real ESM embeddings.
- Target-macro validation RMSE: epoch 1 = .811185; epoch 2 = .813853; epoch 3 = .817272.
- Saved research/pilot_sequence/checkpoint.pt is **epoch 3**, although epoch 1 had best metric. Do not describe it as an optimal early-stopped model.
- Independent checkpoint-loading test verified raw pKd transformation.

Geometry pilot:
- Frozen sequence foundation plus trainable GVP.
- Nine structure-eligible train proteins / 486 pairs; four val proteins / 216 pairs.
- Two epochs; best geometry checkpoint was epoch 1 in research/pilot_geometry_9train_4val/best_checkpoint.pt.
- Macro RMSE on same four development proteins: sequence-only .925685; geometry epoch 1 .935921, epoch 2 .963520.
- FRK and MEK5 improved very slightly (−.002210 and −.002194 RMSE); ADCK4 worsened by +.044869; OSR1 worsened +.000477. Independent best-checkpoint reload reproduced all metrics.

Few-shot development-only diagnostic:
- Same four checkpoint-selected development targets; 10 fixed query compounds per target; K=5 support, 10 deterministic support draws.
- A zero-shot RMSE .86101741; B calibration .86013856; C differential .86101741; D full .86013856.
- D−B difference +5.2e−11 RMSE, effectively zero.
- Mean Tanimoto^4 kernel weight total W only ~.003–.009; centered geometry disagreement V tiny. The differential term effectively never activates. No evidence of value from the geometric correction in this pilot.
- Unapproved BindingDB K5 candidate median W ~.215, so do not generalize this tiny DAVIS null effect to the full intended cohort.
- The pilot uses held-out *development* targets that were also used for selecting the geometry checkpoint; DO NOT label its improvements or lack thereof independent research results.

### Engineering suite

The consolidated suite scripts/run_v4_validation_suite.py ran 15 tests and all passed with full original data present. Includes 200 numerical optimizer comparisons, original baseline parity, real ESM+GVP smoke, synthetic chemistry adapter, train checkpoint reload, scientific gate negative tests, cluster-evaluator tests, and many data boundary cases. Archive report: data/audit/v4_validation_suite.json.
A fresh checkout will be missing large feature caches and the legacy archival checkpoint; reproduce dependencies before rerunning. Failure due to missing cache is not a scientific result.

## 7. Exactly what remains, in dependency order

**Stage 0 — Rehydrate and verify snapshot (engineering prerequisite)**
- Check GitHub HEAD, file manifest, source license and selected checkpoint hashes.
- Create compatible Python environment, GPU toolchain, original 462 ESM feature tensors and official model weights, and any trusted external original PerceiverCPI checkpoint.
- Verify staging sequence hashes and graph provenance. Re-run available smoke tests and document any skipped dependency.
- Never overwrite source measurements, review CSV, original baseline or previously frozen hashes.

**Stage 1 — Primary-source Kd and construct adjudication (SCIENTIFIC BLOCKER)**
- Start with thirty-task review queue; retrieve original papers/patent source details, not only titles or UniProt.
- Determine physical experimental sequence/construct (domain range, tags, mutants, chain), assay conditions, exact Kd vs surrogate/outcome, qualifier, units, and comparable support/query measurements.
- Record source page/table/supplementary evidence, reviewer decision, date and reason; flag uncertain cases, do not auto-approve.
- Scale to sufficiently many independent targets for five-way family-disjoint study. Treat task-source overlap, duplicated labels and chemistry with documented exclusion/normalization.
- Independently audit a sample of approvals.
- Only release an explicit reviewed exact-Kd cohort artifact once evidence is complete; scientific_cohort_gate.py must continue to block before that.

**Stage 2 — Final split registration**
- Cluster ALL approved constructs with reproducible MMseqs2 search and domain-level sensitivity checks; component must not cross split roles.
- Freeze five roles: base_train 60%, base_validation 10%, adapter_train 10%, adapter_validation 10%, test 10%, counting distinct protein groups; balance tasks as far as possible.
- Freeze compound preprocessing and support/query selection seed; K=0/1/2/5/10/20 only if sufficient distinct compounds, 10 fixed queries per task where possible.
- Produce immutable split manifests with hashes; exclude any test label from training, routing, checkpoint selection or tuning.
- Validate that same-compound other-assay labels cannot re-enter forbidden support context.

**Stage 3 — Matched stage-1 and stage-2 scientific training**
- Reproduce original PerceiverCPI baseline with official preprocessing and matched splits, then enhanced ESM foundation.
- Train/freeze sequence model using base_train; use only base_validation for model selection. Report source parameters, seeds and checkpoint SHA.
- Train geometry GVP atop frozen stage-1. Include low quality/missing structure mask and exact fallback. Check 3D residue alignment for every selected protein, not merely most. Use augmentation/dropout where specified; tune only base_validation.
- Run real out-of-batch performance and geometry complementarity tests. Negative 9/4 pilot suggests geometry may fail; do NOT declare gains until a matched held-out cohort demonstrates them.

**Stage 4 — Support adaptation and ablations**
- With both predictors frozen, optimize adapter settings on adapter_train and adapter_validation (not test). Compare A/B/C/D and simpler support residual corrections with identical contexts.
- First investigate whether support evidence W and centered geometric disagreement V have sufficient coverage. If not, report failure of identifiability as a scientific finding, or propose a transparently separated architecture revision and new preregistration. Do not change rules after peeking at test.
- Controls: scrambled support labels, query-only and missing-structure, equal-capacity baseline and support set seed robustness. Track per-target harms and support evidence.

**Stage 5 — Final independent evaluation and paper**
- Run one frozen test protocol on protein-component-held-out roles; calculate task -> construct -> component macro RMSE and paired component-bootstrap 95% CI. Other metrics: MAE, Pearson/Spearman, ranking, distribution/censoring separately where valid.
- Log 3 independent training seeds and >=10 support draws if feasible; avoid pretending pair count is independent replicate count.
- Predefine 2% relative D-vs-B RMSE reduction as a hypothesis threshold, not an achieved result. Report interval and target count; explain if statistical power is insufficient.
- Update manuscript tables with true model versions, datasets, explicit assay provenance, ablations, negative results and related work; no guaranteed novelty or publication claims.

## 8. Recommended next coding jobs that can be done before cohort approval

1. Make tests_v4 and scripts portable: several refer to original C:\Users\J0124 paths and require the full ESM cache. Introduce root/environment variables for artifacts, without changing original meaning; add precise missing-dependency diagnostics.
2. Add a tool to check expected vs actual snapshot SHA and dependencies for full, partial and CPU-only test profiles.
3. Implement source-review evidence aggregation with immutable adjudication records, audit trace and reviewer signoff. Do not fake human approvals.
4. Add formal split-manifest schema and frozen-role validation that hard-fails if a component or assay label can cross roles.
5. Implement contamination/permutation tests on multi-assay same-compound cases, maintaining strict query-label isolation.
6. Add ablation harness from actual prediction records with task/construct ID and support draw metadata, but keep it blocked on approved cohort input.
7. Prepare a scientific failure-mode analysis for geometry representation collapse and low support V without tuning on final test.

## 9. File path guide

Primary:
- README.md, AGENTS.md, HANDOFF_FOR_NEXT_AI.md, PROGRESS_AND_NEXT_STEPS.md, EXPERIMENT_LEDGER.md, REPRODUCIBILITY.md, CHANGELOG.md.
- project.md (original chronological full implementation handoff); research/DynaCPI_Manuscript.md.
- research/Kd_Curation_and_Split_Protocol.md; research/BindingDB_30_Source_Evidence_Dossier_20261105.md.
- data/audit/v4_validation_suite.json and research/validation_suite_logs/*.
- data/audit/bindingdb_full_kd_candidate_tasks_PRE_SPLIT.jsonl, bindingdb_full_kd_candidate_episodes_PRE_SPLIT.jsonl, bindingdb_full_kd_compound_median_candidates.jsonl; all NOT approved for main research.
- data/audit/bindingdb_assay_manual_review_queue_30_ENRICHED.csv, bindingdb_assay_manual_review_status.json.
- data/audit/bindingdb_full_kd_mmseqs_component_screen.json; bindingdb_full_kd_group_split_dryrun_policy.json.
- data/engineering_pilot/rows.json, protocol.json, limited_alpha_3d_graph_manifest.json.
- research/pilot_sequence/checkpoint.pt, research/pilot_perceiver/checkpoint.pt, research/pilot_geometry_9train_4val/best_checkpoint.pt.
- provenance/snapshot_file_manifest.json includes SHA-256 per included file plus intentionally omitted file paths.

## 10. Important communication when handing off

Tell the owner clearly:
- DynaCPI v4 has a working prototype and real supervised pilot models.
- Original checkpoint parity and software quality checks passed.
- The geometry branch and differential adaptation do not yet improve the small DAVIS development pilot.
- The full exact-Kd research study has not started because the assay/source-reviewed cohort and family-disjoint split are not approved.
- No additional model design or training should be described as research success without the source/holdout prerequisites.
- Upload commits 0.1–0.4 are Git history milestones only, NOT neural model versions.

**Do not repeat prior architectural debates as if they were new decisions. Continue from verified artifacts, disclose risks, and work against acceptance criteria.**

## 11. Continuation evidence, 6 November 2026 — read BEFORE running new experiments

**This update supersedes only the numeric engineering-test count and the DAVIS development evidence in the original 5 November handoff; it does not authorize a new DynaCPI model architecture.** The project was resumed on built-diff12 under C:\Users\J0124\dynacpi_v4, in a separate VS Code window. The original training files, earlier saved best checkpoints, source-unapproved BindingDB data and upstream PerceiverCPI checkout were preserved. VS Code task commands are in .vscode/tasks.json.

- **Engineering suite now 17/17 PASS**, with zero failed checks; source report data/audit/v4_validation_suite.json (6 November 2026). Two new regression checks validate K-sweep output/checkpoint hashes and three-seed support comparisons.
- **K=0,1,2,5,10,20 fixed DEV sweep:** ten fixed queries for each of FRK, MEK5, ADCK4, OSR1, ten deterministically nested support draws per K. Original seed-1105 B RMSEs 0.86101741 / 0.86079179 / 0.86061335 / 0.86013856 / 0.85936112 / 0.85738896. D–B at K20 +2.46e-10, effectively zero. Same original frozen sequence/GVP checkpoints and default lambda, no model changes. research/support_k_sweep_dev/results.json, aggregate.csv, SUMMARY.md and IDENTIFIABILITY.md.
- **Regularization evidence mismatch:** for seed 1105 at K20 average Tanimoto^4 kernel weight W=0.028842 and centered geometry/sequence disagreement V≈6.50e-11; with lambda_b=5 and lambda_theta=.1, the descriptive scale ratios are W/(W+lambda_b)=.005735 and V/(V+lambda_theta)≈6.50e-10. Do not interpret them as the exact ridge coefficients or proof that regularization tuning will help.
- **Geometry random initialization stability:** two new supervised, development-only GVP runs at predeclared seeds 1106 and 1107 were added, using identical nine training and four validation proteins and two epochs; original seed 1105 remains intact. The best-epoch validation target-macro geometry RMSE was 0.93592060 (seed 1105/epoch1), 0.92004961 (seed 1106/epoch2) and 0.91597119 (seed 1107/epoch1), versus frozen sequence 0.92568508. These values were SELECTED ON THE SAME FOUR VALIDATION TARGETS and are not independent generalization.
- **Support adaptation on all three geometry seeds:** same compounds, K list, draws, architecture and regularization. At K20 B versus D macro RMSE: seed 1105 0.8573889581 / 0.8573889583; seed 1106 0.8529299312 / 0.8529299314; seed 1107 0.85154725 / 0.85154728. All D−B differences are negligibly small. Seed-dependent geometry accuracy changes do not resolve v4 differential identifiability in this narrow DEV cohort. See research/pilot_geometry_seed_sweep_dev/adapter_seed_comparison.json and research/support_k_sweep_seed_dev.
- **Monitoring:** scripts/monitor_benchmarks_v4.py writes research/monitoring/latest.json, LATEST.md and events.jsonl, tracking checkpoint hash, tests, support-K results, seed effects, scientific approval gate and GPU snapshot. An hourly notification automation checks meaningful changed results or errors when built-diff12 is online. It never initiates fitting, and notifications are not proof of computer access when offline.
- **Scientific gate still hard BLOCKED**: no source-approved exact-Kd BindingDB cohort and no frozen protein-family-independent test. Next true research step is primary-source construct/Kd assay adjudication, approved cohort selection, then locked base/adapter/test roles before any credible D-vs-B claim. Do not tune the current model on the same four checkpoint-selected development proteins and interpret any resulting gains as scientific generalization.

**Useful commands on authorized original PC:**

    C:\Users\J0124\dynacpi_v4\.venv\Scripts\python.exe C:\Users\J0124\dynacpi_v4\scripts\monitor_benchmarks_v4.py
    C:\Users\J0124\dynacpi_v4\.venv\Scripts\python.exe C:\Users\J0124\dynacpi_v4\scripts\run_v4_validation_suite.py

The next agent should read the newest 6 November project.md entry and manuscript Sections 7.9–7.10, not infer current conclusions from 5 November counts.

## 12. Source-access audit and unresolved human review, 6 November 2026

The original 30-task reviewer CSV was protected by SHA-256 and NOT modified. The authoritative canonical file remains data/audit/bindingdb_assay_manual_review_queue_30_ENRICHED.csv. Europe PMC metadata queries for 20 unique source PubMed IDs matched all 20. From 20 bibliographic records, two publicly accessible open-access XML articles were safely indexed for method section IDs/headings and keyword counts, 17 provided metadata but not public OA full text via this route, and one contained DTD/entities and was rejected for safe manual review instead. Source article bodies were neither copied nor committed. Task-level access dispositions: 2 OA-indexed, 20 needing original-article access, 7 primary patent review, 1 missing usable source identifier.

**Zero source-reviewed experimental Kd tasks approved.** NO approved independent protein-group split exists. The project remains blocked for the primary scientific training and D-versus-B test. These are pointers to where a qualified source reviewer should look; matching a PMID or a keyword does not confirm the experimental physical target construct, Kd semantics, source unit and qualifier, or compatible assay conditions.

New reproducible scripts: scripts/audit_primary_source_access_v4.py (API metadata + safe OA section index) and scripts/build_primary_source_review_worklist_v4.py (read-only worklist). Outputs: research/source_access_v4/source_access_index.json, SOURCE_ACCESS_SUMMARY.md, REVIEW_ACTIONS.md, worklist_manifest.json. Regression tests: tests_v4/source_access_index_integrity_test.py; data/audit/source_access_index_integrity.json. All existing DAVIS development benchmark results from 6 November remain unchanged. The suite now passed **18/18 checks**, and VS Code has seven task commands covering benchmark checks, source access, review preparation, and scientific gate inspection. Research manuscript Section 7.11 records limitations and actual source-access counts.

**Next person MUST NOT auto-approve the two OA-indexed tasks.** They require primary-paper methods and supplementary evidence independently checked by an appropriately qualified reviewer, then explicit source-review and rationale entries in the canonical human review process. If a source cannot be accessed legally, keep the task unreviewed or exclude it rather than invent evidence. No scientific benchmark release can happen before this review.

## 13. Source-paper construct differences, 6 November 2026 — do not mistake metadata for physical assay input

Primary method sections inspected for two unapproved exact-Kd candidate tasks:
- NPR-C, PMID 35333039 / PMCID PMC9014859 / Methods sec4.4: experimental region 27–541, nominal 515 residues, tagged; candidate UniProt P17342 reference sequence is full length 541. Its assay description mentions the region, but its candidate protein feature sequence is still the canonical 541-aa string.
- NRP1-b1, PMID 29648813 / PMCID PMC5957473 / sections sec4.2.1 and sec4.2.3: paper identifies region 273–427, nominal 155 residues, in the relevant expression/binding methods; candidate UniProt O14786 reference is full-length 923. Paper narrative also discusses b1b2; individual source-table-to-assay construct association must be verified.

**DO NOT** claim these are completed scientific approvals, measured-value disputes or confirmed physical tagged sequence reconstructions. The exact paper/source structure, additional tags or processing, sequence local mapping, and per-compound Kd provenance remain unresolved. Both source tasks are UNREVIEWED, all 30 remain UNREVIEWED, and no source-approved cohort/split exists. This demonstrates why a full-length canonical protein representation is not necessarily a correct ligand-binding experimental construct.

Saved evidence: research/source_access_v4/PRELIMINARY_CONSTRUCT_ALIGNMENT_REVIEW.md and construct_alignment_risk_screen.json; independent original review metadata screen data/audit/bindingdb_assay_review_30_uniprot_construct_screen.json. New scripts/check_primary_construct_flags_v4.py cross-checks candidate reference lengths, source access identifiers, review CSV SHA and continuing blocked gate. tests_v4/construct_alignment_risk_integrity_test.py verifies fail-closed flags and nominal spans. The engineering suite now passes **19/19**. The VS Code task list is now eight items; benchmark watcher includes the two construct-alignment review flags.

**Next actual work:** qualified independent paper/assay review, exact experimental construct sequence and tagged-region resolution for each candidate, original table/measurement matching and qualifier checking. Scientific training and final D-vs-B benchmark are STILL BLOCKED. The current model checkpoints/engineering results are unchanged.

## 14. All-30 metadata triage, 6 November 2026 — current authoritative review priorities

New `scripts/triage_30_assay_metadata_v4.py` performs deterministic, **read-only metadata** review prioritization over the fixed 30-task human-review CSV, source access index, exact canonical reference-length screen and two original source-section fragment leads. It does NOT load any individual affinity value, silently approve/reject experimental tasks, change the original reviewer decisions, or release approved cohort artifacts.

Output: `research/source_access_v4/assay_metadata_risk_triage_30.json`, `.csv`, and `ASSAY_METADATA_TRIAGE.md`. Current priorities: **P0=4** immediate endpoint/source metadata clarification, **P1=12** construct and endpoint interpretation, **P2=14** routine primary-source review. Every one of the 30 remains UNREVIEWED; zero approved, gate BLOCKED. P0 examples: CFTR candidate described with "half effective concentration" despite a Kd field; GLP-1 receptor candidate described using a glucose colorimetric assay; missing PD-L1 assay description; missing original source ID for carbonic anhydrase II. These are metadata warnings, not verified mislabels.

Overlapping indicators: 6 descriptions with numeric reference-shorter regions, 8 tagged/labeled reagent mentions, 4 potential activity-endpoint mentions, 4 competition/displacement methods, 4 complex/cofactor terms. The VHL/Elongin-C task mentions residues 54–213 (VHL partner) while the named Elongin-C reference is only 112 aa; the new tool explicitly flags CHAIN ASSOCIATION REVIEW rather than silently assigning the partner segment to Elongin-C. Numerical spans for pH and temperature should never become residue coordinates.

New `tests_v4/metadata_risk_triage_integrity_test.py` verifies parser adversarial cases, immutable original CSV hash, 30 task identities, source evidence hashes, no Kd values or approval fields, and the continued blocked cohort gate. The full `scripts/run_v4_validation_suite.py` passed **20/20 tests**, all engineering-only. The local observer `scripts/monitor_benchmarks_v4.py` now tracks triage counts, and `.vscode/tasks.json` contains nine runnable tasks including metadata triage.

**Next scientific job remains human source/construct/Kd adjudication.** Do not train on the source-unapproved BindingDB candidates, split them for blind main testing or tune affinity models using review metadata. Read the priority report first and document all original source table/qualifier/physical construct findings. The original v4 sequence, geometry and adaptation weights and previous negative development results remain unchanged.

## 15. Four P0 source-evidence leads and corrected DOI classification (6 November 2026)

A high-priority **source-evidence crosswalk** was added as `scripts/build_p0_source_crosswalk_v4.py`, producing `research/source_access_v4/p0_source_crosswalk.json` and `P0_SOURCE_CROSSWALK.md`. Four P0 review candidates were matched only to structured external bibliographic or assay metadata, with explicit source evidence tiers and individually unresolved verification questions. No measured compound-level affinity values, full publication bodies or approvals were used. **The original DynaCPI v4 scientific model remains unchanged.**

- CFTR candidate: the linked publication abstract identifies a cellular functional-transport response, not a demonstrated direct equilibrium Kd for the selected candidate record. Per-record original-table and species/construct checks still needed.
- GLP-1 receptor candidate: external assay registry metadata is associated with the same BindingDB assay identifier but describes a glucose/colorimetric measurement. Its actual binding participant and target annotation require original source/record reconciliation.
- Carbonic-anhydrase II candidate: a DOI existed in the ORIGINAL reviewer CSV and resolves to a 1996 binding-site study. The initial source-access index falsely called this record missing a source identifier because it only recognized PMIDs/patent numbers; corrected to `PRIMARY_DOI_ONLY_METHODS_PENDING`. Publication methods and Kd semantics are still NOT verified.
- PD-L1 candidate: the primary patent source is identifiable, but the canonical BindingDB review record has no assay description; record-level patent experiment and exact endpoint cannot be inferred from a patent identifier alone.

The revised `scripts/audit_primary_source_access_v4.py` and `scripts/build_primary_source_review_worklist_v4.py` recognize DOI-only access and retain the original 20 PubMed source records / 2 safe open-access method-section indexes. Regenerated `scripts/triage_30_assay_metadata_v4.py` still reports P0=4, P1=12, P2=14 with a corrected DOI-only flag. The new `tests_v4/p0_source_crosswalk_integrity_test.py` checks immutable task/source IDs, source index and CSV hashes, all four unapproved states, and the blocked scientific cohort gate. **21/21 engineering tests passed**, zero failures. The monitor tracks P0 source tiers, zero approvals and zero per-record Kd-verification completions. VS Code has ten tasks, including rebuild of the non-approving P0 source evidence brief.

**Research blocker unchanged:** Human adjudication must still establish actual physical assayed protein, exact per-record Kd units and qualifiers, original source table correspondence and compatible assay conditions before approved cohort and frozen independent protein-family split. No final BindingDB model training or blind test has been run. Do not treat these metadata leads as completed source reviews or accept them as mathematical model labels. For future report writing, the source-ID correction supersedes earlier notes calling CA2's primary identifier wholly missing.

## 16. Windows reconnection, original-record lineage audit and 23-check engineering validation — 6 November 2026

A fresh remote PowerShell command succeeded on connected Windows computer built-diff12, allowing a REAL audit of the existing DynaCPI v4 data at C:\Users\J0124\dynacpi_v4. The last verified GitHub snapshot before this work was f79d38f; this new work must be read in addition to all previous source-evidence and negative geometry development results.

The newly installed script scripts/audit_30_record_level_provenance_v4.py ingests the pre-existing files data/audit/bindingdb_full_kd_compound_median_candidates.jsonl, bindingdb_full_kd_source_provenance.jsonl and bindingdb_full_kd_candidates.jsonl. It restricts processing to the fixed 30-task manual-review queue, checks each Reactant_set_id against its original source row and unaggregated candidate, strictly numeric positive Kd, 9-log10(Kd in nM) calculation, source candidate protein hashes, assay keys, reviewer raw-record counts, median/range of compound duplicates and input SHA-256. It does not extract a new set of measurements, tune models, construct cohorts or approve tasks.

**Actual run:** 30 tasks, 919 unique compound groups, 921 distinct raw source reactant IDs, 921/921 raw source records found, 921/921 unaggregated candidate rows found, 0 duplicate original IDs, 0 duplicate preliminary IDs, 921 strictly positive numeric source Kd fields, 0 critical technical lineage discrepancies. Two compound groups had two raw records each (PDE6D and ENPP1 candidate targets); median and range calculations matched. Audit artifact research/source_access_v4/record_level_provenance_30.json plus RECORD_LEVEL_PROVENANCE_30.md; output includes aggregate counts and source-file SHA but NOT original affinity values, SMILES or raw reactant IDs.

**New protections:** tests_v4/record_lineage_synthetic_test.py passed 5/5 synthetic unit cases: valid multi-source median, deliberately wrong pKd conversion flagged, missing raw source record flagged, qualified Kd rejected as numeric, and changed human-review decision blocks audit. tests_v4/record_lineage_real_integrity_test.py reruns the real audit, asserts its 30/919/921 values and 0 critical flags, protects the unmodified reviewer queue by hash and requires scientific_cohort_gate.py to report BLOCKED. Both appear in scripts/run_v4_validation_suite.py; full suite **23/23 PASS, zero failed** on 6 November 2026 including archived PerceiverCPI DAVIS parity. VS Code .vscode/tasks.json now exposes 11 tasks, including 'DynaCPI: Audit 30-task raw BindingDB record lineage'. scripts/monitor_benchmarks_v4.py now watches source recovery counts/critical flags alongside DAVIS engineering results and source review approval gate; existing hourly notification automation remains read-only.

**IMPORTANT SCIENTIFIC LIMITATION:** matching a source numerical field does NOT demonstrate it reports direct experimental Kd for the intended real construct, species and assay. The CFTR functional endpoint, GLP-1 receptor/glucose registry mismatch, NRP1-b1 fragment, NPR-C fragment and multiprotein VHL/Elongin source warnings still require independent original-paper/patent record-level adjudication. All 30 tasks are UNREVIEWED, 0 source-approved, no frozen family-disjoint test cohort. Do NOT launch the main scientific training or report model superiority. The three GVP seed and K-sweep DEV results remain as in earlier sections.

Recommended next scientific decision sequence: (1) review the four P0 source records against actual measured paper/patent table rows and physical constructs; (2) document exact numeric measurement identities, censoring, proteins, tags and assay conditions for each independently eligible task; (3) review remaining candidates across distinct target families; (4) freeze protein-cluster/compound/assay deduplication and train/adapter-val/test roles; (5) only then perform blinded D-versus-B paired evaluation with uncertainty and appropriate PerceiverCPI baselines. Preserve all metadata warnings, technical positive checks and negative model development observations.

## 17. Local per-record human primary-source review scaffold (6 November 2026)

**Read before requesting further Kd model training:** Following the successful real technical 30-task/921-reactant lineage audit, `scripts/build_record_source_evidence_worklist_v4.py` was created to make the *scientific* provenance review actionable. It generated the **PRIVATE LOCAL-ONLY** worksheet `data/audit/source_record_evidence_worklist_30_LOCAL_PRIVATE.csv` on Windows `built-diff12` under C:\Users\J0124\dynacpi_v4. The file holds original Reactant_set_id/task/assay/sequence hash and source PMID/DOI/patent/PubChem AID/organism/curator fields, but **does NOT hold original potency numbers, pKd, SMILES or chemical structures**. Do NOT copy this private worksheet or reviewer notes to GitHub or use it to populate model labels. It is explicitly excluded by Git ignore rule `data/audit/*LOCAL_PRIVATE*.csv`.

All **921/921 raw record review decisions are UNREVIEWED**, across the 30 UNREVIEWED canonical assay tasks. Original source and human review CSV files are verified by SHA-256 and unchanged. The generator never overwrites an existing local worksheet. The public output is `research/source_access_v4/record_source_evidence_readiness_30.json` and `RECORD_SOURCE_EVIDENCE_READINESS.md`, containing only aggregate state counts and source hashes.

Each potential record-level approval requires an original primary-source methods locator, table/figure row corresponding to the individual Reactant_set_id, correct measured binding participants, actual physical protein construct and sequence SHA256, method, direct equilibrium Kd (not IC50, Ki, EC50), EXACT qualifier, source-record mapping, compatible assay context, reviewer ID, review date and substantive justification. The program rejects missing evidence, inconsistent immutable metadata, duplicate/missing IDs, unsupported types, qualified values, and unsigned decisions. **Even a structurally complete self-reported APPROVE declaration NEVER automatically creates a source-approved scientific cohort or enables training.** Actual source paper/patent and biological-method adjudication remain independent requirements.

Synthetic tests `tests_v4/record_source_evidence_synthetic_test.py` passed 10/10 unit cases, including negative and positive fake signoff cases; the real-data integration `tests_v4/record_source_evidence_real_integrity_test.py` passed, reconciling all 921 records and ensuring the scientific cohort gate remains BLOCKED. `scripts/run_v4_validation_suite.py` now contains 25 checks; examine `data/audit/v4_validation_suite.json` for final completion rather than inferring from test setup. VS Code now has 12 tasks including 'DynaCPI: Validate private 921-record source review worksheet'. `scripts/monitor_benchmarks_v4.py` watches only the public aggregate review report, not the private worksheet.

**The next genuinely scientific milestone** is independent qualified source-level adjudication of the four P0 tasks (CFTR, GLP-1 receptor, PD-L1, carbonic anhydrase) and the two original method-fragment examples (NRP1-b1, NPR-C), then all eligible tasks from sufficiently many unrelated protein components. For each measurement independently reconcile actual source method/table, physical protein construct and tags/variants, exact Kd semantics/units/qualifiers, and comparable assay conditions. Only a scientifically approved and independently audited evidence manifest plus frozen five-role protein-family-disjoint split permits the main matched D-vs-B experiment. No architecture change, retraining or source-based model performance result occurred here.

## 18. DECISIVE new three-seed geometry main-effect versus support-differential comparison — 6 November 2026

STOP relying on the original near-zero D-minus-B comparison as proof geometry itself is useless. Both original B and D already used w0=0.5 sequence/geometry blended base predictions; D-B isolates the centered differential correction only. I executed scripts/benchmark_geometry_factorial_dev.py against the ACTUAL three saved frozen seed checkpoints (1105,1106,1107) and matching four structure-mapped development targets, exact immutable query identities, ten nested support draws and K=[0,1,2,5,10,20]. There are 720 correlated target-draw-K evaluations, only FOUR unique proteins, no independent held-out family cohort, no source-approved BindingDB labels, no training/tuning or checkpoint changes.

Five variants: S0 sequence, S_B sequence calibrated, G_A sequence/geometry mixture, G_B mixture calibrated, G_D mixture calibrated + differential support adaptation. At K=5, S_B RMSE=0.857337 across seeds. G_B RMSE=0.860139 (1105), 0.855587 (1106), 0.854164 (1107). Thus geometry-main-effect G_B - S_B was +0.002801 (harmful), -0.001750 and -0.003173 (favorable), respectively. Only TWO out of four development proteins improved in EACH seed, and ADCK4's geometry benefit flipped sign (+0.01249, -0.007262, -0.014007). The differential G_D - G_B was effectively ZERO (5.20e-11, 4.21e-11, 5.42e-9). At K=5 centered disagreement variance V ~1e-11 to 1e-9 vs lambda_theta=0.1; geometry correction is strongly suppressed under the current fixed ridge estimator. Previous G_A/G_B/G_D results matched to max 6.16e-10 macro RMSE across ALL three seeds and K values.

Scientific decision: Do not claim DynaCPI v4 geometry-conditioned differential adaptation improves over calibration-only or PerceiverCPI. Current incremental differential mechanism is inactive; geometry mixture seed-sensitive, not reproducible across targets. Do NOT tune on these same four checkpoint-selected proteins and represent the outcome as unbiased validation. The original method can be published only with accurately negative development results and/or a rigorously new, independently source-approved evaluation. Artifacts research/geometry_factorial_dev/factorial.json, SUMMARY.md, tests_v4/geometry_factorial_dev_integrity_test.py, paper Section 7.17. Full regression suite PASSED **26/26** and VS Code now exposes 13 tasks, including frozen three-seed factorial benchmark.

Source review remains ZERO of 30 approved; the 921-record private reviewer worksheet is LOCAL-ONLY on the Windows computer, not GitHub. No scientifically approved final split, no trained BindingDB main model, no independent valid superiority claim. Continue substantive scientific work by independently reviewing the original source experimental method and physical protein construct and creating a truly independent evaluation; do not waste cycles creating more metadata-only checklists.

## 19. Primary-publication evidence crosswalk: 6 tasks / 147 original records (6 November 2026)

THIS IS SCIENTIFIC SOURCE DISCOVERY, NOT A NEW MODEL RUN. After the 26-check geometry factor ablation, original publication evidence was examined for six real preselected BindingDB tasks. A deterministic fixed-source script, scripts/verify_six_primary_source_leads_v4.py, created research/source_access_v4/six_task_publication_evidence.json and SIX_TASK_PUBLICATION_EVIDENCE.md. It checks original task/assay/PMID/count identity and preserves review CSV SHA-256, without exporting original chemical structures, source Reactant_set_ids or numerical affinities.

ANXA3 has 48 preliminary records (assay 50023141_1) and a source SPR study (PMID 40013713, DOI 10.1021/acs.jmedchem.4c02403); PubChem AID 2234142 has a matching count of 48 recombinant ANXA3 SPR dissociation constant entries. This is high-quality experimental method corroboration, NOT proof that each record or physical construct was independently verified. Three kinase-domain assay tasks, RIO2 20 / SRPK3 19 / IRAK3 24, trace to the original 2011 Davis kinase-interaction paper (PMID 22037378), with published Supplementary Table 4 Kd values (nM); all 63 need original value-to-row and domain-to-sequence mapping. PGK18 links to original NMR binding study PMID 9804684, with pH and numeric endpoint unresolved. PA-I lectin 18 citations contain a serious provenance anomaly: **PMID 26804741 is a review article, not an original 18-record experiment**; separate PMID 27488655 reports a competitive assay and cannot be silently substituted for those candidate exact Kd values. There is an independent test tests_v4/six_publication_source_evidence_integrity_test.py asserting source identities and zero approvals.

Next work must perform original source table-to-record measurement concordance, exact assayed construct chain/sequence alignment and Kd qualifiers independently; start with the coherent ANXA3 source records, and resolve the PA-I review-article citation. Do not make automatic APPROVE decisions or run the main BindingDB training based on bibliographic evidence. Original 30 tasks are still UNREVIEWED; no source-approved scientific cohort/frozen independent protein-family split exists. Existing G_D vs G_B incremental geometry adaptation remained essentially inactive on DAVIS DEV only; do not misstate source-level evidence as improved model RMSE.
