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
