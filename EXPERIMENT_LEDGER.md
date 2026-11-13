# Experiment ledger — observed evidence only

**Date of all entries:** 5 November 2026. Engineering and data-audit provenance; no source-approved BindingDB scientific benchmark.

| Stage | Actual observed result | Verifiable file | Interpretation |
| --- | --- | --- | --- |
| Original PerceiverCPI inference | 1,148 archived DAVIS fold-zero predictions reproduced exactly; max error 0.0 | research/legacy_checkpoint_parity.json | Original local checkpoint parity only; not paper-wide replication |
| ESM-2 cache | 462/462 valid FP16 feature tensors, 346,865 positions, 570 windows | data/audit/esm_cache_integrity.json | Cached inputs valid on original PC; tensors excluded from Git |
| BRAF geometry smoke | 766 residues, 18,789 directed edges, real ESM and AlphaFold mapping | research/cached_esm_gvp_pair_smoke.json | Interface working; synthetic regression targets |
| Full BindingDB data scan | 3,243,660 rows, 131,531 populated Kd, 82,481 positive exact-looking, 80,139 preliminary linked | data/audit/bindingdb_full_kd_eligibility.json | Preliminary source audit; NOT verified endpoint semantics |
| Preliminary tasks | 1,146 K5 candidates across 168 protein components; 377 K20 candidates | data/audit/bindingdb_full_kd_mmseqs_component_screen.json | Not approved split or assays |
| Episode isolation | 4,961 checks across 1,146 candidate tasks; no within-episode cross-assay support/query labels | data/audit/bindingdb_full_kd_episode_loader_validation.json | Software boundary, not proof source labeling correct |
| Manual review | 30 sampled, 30 unreviewed, 0 approved; all database sequences match UniProt metadata | data/audit/bindingdb_assay_manual_review_status.json; bindingdb_assay_review_30_uniprot_construct_screen.json | No valid scientific training cohort yet |
| Source indexing | 20 distinct PubMed records resolved, 7 patent-only tasks, 13 description clue flags | data/audit/bindingdb_assay_review_30_publication_screen.json; bindingdb_assay_review_30_construct_clues.json | Identification only, not assay verification |
| Sequence foundation | 3 DAVIS engineering epochs, target-macro validation RMSE 0.811185 / 0.813853 / 0.817272 | research/pilot_sequence/history.json | Best observed epoch 1, but checkpoint saved from epoch 3 |
| Geometry GVP | 9 train proteins/486 pairs; 4 val/216; seq 0.925685 vs geometry 0.935921 (epoch 1) and 0.963520 (epoch 2) | research/pilot_geometry_9train_4val/history.json | **Geometry worse overall** in limited development |
| Per-target geometry | FRK −.002210, MEK5 −.002194, ADCK4 +.044869, OSR1 +.000477 RMSE | research/pilot_geometry_9train_4val/checkpoint_parity.json | Two tiny gains, two losses; checked reload parity |
| A/B/C/D adapter | Development K5 macro A=.86101741, B=.86013856, C=.86101741, D=.86013856 | research/pilot_geometry_9train_4val/support_adapter_development_diagnostics.json | **D−B ≈ +5.2e−11**, essentially no differential gain |
| Chemical evidence scale | DAVIS development W roughly .003–.009; preliminary BindingDB K5 median W=.215 | development support diagnostic; data/audit/bindingdb_full_kd_support_chemical_coverage.json | Nontransferable between cohorts, not a tuned finding |
| Data split dry run | 168 component groups into 100 /17 /17 /17 /17, 1,146 tasks into 735/110/101/100/100 | data/audit/bindingdb_full_kd_group_split_dryrun_policy.json | Not final frozen split |
| Consolidated suite | 15/15 tests passed with all source-PC caches and original external baseline available | data/audit/v4_validation_suite.json | Engineering correctness, not independent model accuracy |

## Non-results and prohibited interpretations

- These development figures are not external scientific validation.
- No measured DynaCPI v4 improvement over original PerceiverCPI is established.
- No external blind protein-family test has been run.
- No source-verified exact-Kd BindingDB approved cohort exists.
- No publication-quality novelty or impact claim has been demonstrated.
- A large number of processed rows, high GPU utilization, or 15 passed tests is not evidence of predictive benefit.

The next person must append genuine new observations rather than rewrite this historical ledger. When correcting a prior measurement, add an explicit correction note and retain original evidence.

## Additional engineering-only experiments — 6 November 2026

| Stage | Actual observed outcome | Evidence | Interpretation |
| --- | --- | --- | --- |
| Original-seed support K sweep | B macro RMSE 0.861017 (K0), 0.860792 (K1), 0.860613 (K2), 0.860139 (K5), 0.859361 (K10), 0.857389 (K20); D essentially identical | research/support_k_sweep_dev/results.json | Same 4 development targets; no source-approved holdout |
| K20 kernel/variance scale | Mean W=0.028842, mean V=6.50e-11, fixed lambda_b=5 and lambda_theta=.1 | research/support_k_sweep_dev/identifiability.json | Tiny data/regularizer scale; not a tuned estimator or proof a change helps |
| Geometry seed comparison | Best geometry macro RMSE seed 1105=0.935921, 1106=0.920050, 1107=0.915971; frozen seq=0.925685 | research/pilot_geometry_seed_sweep_dev/seed_variability.json | Two seeds look better on reused development-val targets, one worse; generalization unknown |
| Three seed D-versus-B at K20 | D−B +2.46e-10 (1105), +2.00e-10 (1106), +2.48e-8 (1107) | research/pilot_geometry_seed_sweep_dev/adapter_seed_comparison.json | Essentially no support-dependent geometry correction across seeds |
| Regression suite | 17/17 PASS on original machine | data/audit/v4_validation_suite.json | Engineering integrity only, not independent predictive utility |
| Monitoring | Local status artifacts and hourly condition-watch notification enabled | research/monitoring/latest.json, LATEST.md | Observer only; no ongoing GPU training promised |

**New constraints:** Do not hide the development-only geometry result or optimize hyperparameters on these same checkpoint-selected targets to claim scientific gains. The BindingDB main study remains blocked pending primary-source exact-Kd adjudication and family-disjoint split freeze.

## 6 November 2026 — Bibliographic source-access audit (not a predictive experiment)

| Audit | Verified engineering outcome | Evidence | Limits |
| --- | --- | --- | --- |
| Thirty-task review worklist | 30 tasks, all UNREVIEWED and 0 approved; original source CSV unchanged by SHA | research/source_access_v4/worklist_manifest.json | No experimental construct or Kd evidence independently reviewed |
| Publication metadata access | All 20 unique PubMed identifiers matched public bibliographic records | research/source_access_v4/source_access_index.json | PMID equality is not Kd measurement verification |
| Open-access method-section indexing | 2 public OA XML indexed; 17 metadata-only; 1 OA XML rejected due to DTD/entities | research/source_access_v4/SOURCE_ACCESS_SUMMARY.md | Does not copy article body or decide assay semantics |
| Task-level review routing | 2 OA indexed, 20 additional source article access, 7 primary patents, 1 source identifier missing | research/source_access_v4/REVIEW_ACTIONS.md | Work routing only; does not imply source approval |
| Integrity regressions | 18/18 PASS, 0 failed | data/audit/v4_validation_suite.json | Software and provenance gates, not biological validity |

Retain the source-review blocker and zero-approval status until an independently documented human adjudication produces a real eligible cohort and immutable split.

## 6 November 2026 — source-method construct discrepancy screen (review support, NOT predictive data)

| Candidate accession | Canonical reference length | Original paper-reported segment | Nominal region length | Primary source location | Approval |
| --- | ---: | --- | ---: | --- | --- |
| P17342 | 541 aa | 27–541 | 515 aa | PMC9014859, sec4.4 | UNREVIEWED |
| O14786 | 923 aa | 273–427 | 155 aa | PMC5957473, sec4.2.1 and sec4.2.3 | UNREVIEWED |

This screen demonstrates reference-input versus reported assay-region differences; it does **not** check per-compound labels, prove a database mistake, or establish exact physical mutant/tag sequence. The review queue SHA and source ID/length metadata were cross-checked by scripts/check_primary_construct_flags_v4.py and new risk integrity test. The 19/19 engineering checks pass. Zero source-approved tasks and no frozen family-disjoint test cohort.

## 6 November 2026 — Fixed 30-assay metadata triage (NOT a binding-affinity experiment)

| Evidence | Observed engineering result | Artifact |
| --- | --- | --- |
| Reviewer workload grouping | 4 P0, 12 P1, 14 P2; 30 distinct candidate tasks, zero human approvals | research/source_access_v4/assay_metadata_risk_triage_30.json |
| Metadata language warnings | 6 numeric source regions smaller than canonical; 8 tagged/labeled; 4 possible activity endpoint; 4 competition/displacement | research/source_access_v4/ASSAY_METADATA_TRIAGE.md |
| Specific ambiguity examples | CFTR half-effective concentration vs Kd field; GLP-1R target vs glucose assay; PD-L1 no description; CA2 source ID missing | research/source_access_v4/assay_metadata_risk_triage_30.csv |
| Multiprotein assignment caveat | Elongin-C metadata's 54–213 range appears to belong to partner VHL; cannot assign to named Elongin-C automatically | research/source_access_v4/ASSAY_METADATA_TRIAGE.md |
| Integrity regression | 20/20 PASS; original review source SHA unchanged; 0 scientific approvals | data/audit/v4_validation_suite.json |

All outputs are metadata-only review leads, not source-reviewed exact-Kd assays or independent model performance.

## 6 November 2026 — four P0 source metadata leads and DOI correction (not science benchmark)

| Source evidence tier | Review finding | Scientific status |
| --- | --- | --- |
| Publication abstract | CFTR candidate linked to a cellular functional transport assay; direct Kd relationship not yet verified for record | UNREVIEWED |
| Registered assay | GLP-1 receptor candidate indexed with a glucose/colorimetric assay; target vs measured participant unresolved | UNREVIEWED |
| DOI bibliography | Carbonic-anhydrase II has a source DOI (contrary to original missing-ID classification), but its individual binding experiment remains unreviewed | UNREVIEWED |
| Patent locator | PD-L1 source patent identified; original assay description missing and method-to-record correspondence unresolved | UNREVIEWED |

The deterministic crosswalk retains original task hashes, source evidence tiers, zero recorded affinity values and explicit unresolved questions. The source-index category for the DOI-only task was corrected and all downstream source worklists/metadata triage regenerated. The engineering suite now passed **21/21**. Original 30 review records unchanged; zero scientific approvals and zero final independent test findings. Evidence: `research/source_access_v4/p0_source_crosswalk.json`, `P0_SOURCE_CROSSWALK.md` and `data/audit/v4_validation_suite.json`.

## 6 November 2026 — real 30-task BindingDB raw-record technical lineage audit

| Technical quantity | Observed result |
| --- | ---: |
| Fixed review tasks | 30 |
| Preliminary compound-level groups | 919 |
| Distinct raw BindingDB Reactant_set IDs | 921 |
| Matched original raw source rows | 921 / 921 |
| Matched unaggregated preliminary candidate rows | 921 / 921 |
| Duplicate original/unaggregated raw IDs | 0 / 0 |
| Strictly positive numeric Kd source strings | 921 |
| Multi-source-record compound groups | 2 |
| Technical critical source conversion/sequence/assay/median discrepancies | 0 |
| Scientifically source-approved tasks | 0 |
| Full engineering regression suite | 23 / 23 PASS |

Run scripts/audit_30_record_level_provenance_v4.py, then consult research/source_access_v4/record_level_provenance_30.json. Synthetic tests: 5/5. Source audit reports may not be interpreted as proof that the reported Kd numeric field is a true direct protein-compound equilibrium measurement or that the physically assayed construct equals the canonical UniProt reference. No new trained model, approved cohort or frozen independent test.

## 6 November 2026 — evidence-review readiness (source governance, NOT a trained model experiment)

| Check | Observed result |
| --- | ---: |
| Original source-reactant evidence rows initialized privately | 921 |
| Original preselected BindingDB tasks | 30 |
| Private records still UNREVIEWED | 921 |
| Individual source records independently scientifically approved | 0 |
| Source-approved tasks | 0 |
| Approved protein-family-independent split | None |
| Synthetic evidence-validator cases | 10/10 PASS |
| Real private-worklist identity checks | PASS |
| Scientific training permission | BLOCKED |

Commit only aggregate counts and provenance hashes in `research/source_access_v4/record_source_evidence_readiness_30.json` and `RECORD_SOURCE_EVIDENCE_READINESS.md`, never the local-only worksheet or original reactant IDs. `scripts/build_record_source_evidence_worklist_v4.py` rejects altered source anchors, missing reviewers, unqualified or non-Kd endpoints, inconsistent review status and missing method/table/construct evidence on proposed approvals. Full suite now contains 25 engineering checks (verify completed outcome in the suite report). All original model weights and scientific claims are unchanged.

## 6 November 2026 — Frozen geometry/sequence factorial with three real model seeds

| Geometry seed | K | S_B (sequence calibrated) RMSE | G_B (geometry-mixture calibrated) RMSE | G_B-S_B | G_D-G_B |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 1105 | 5 | 0.857337 | 0.860139 | +0.002801 | +5.20e-11 |
| 1106 | 5 | 0.857337 | 0.855587 | -0.001750 | +4.21e-11 |
| 1107 | 5 | 0.857337 | 0.854164 | -0.003173 | +5.42e-9 |

Four checkpoint-selected legacy DAVIS development proteins, ten fixed query compounds/protein, ten nested support draws, K=[0,1,2,5,10,20]. 720 correlated target-draw-K cells, NOT 720 independent proteins. Two proteins improve with geometry each seed, and ADCK4 sign flips. Near-zero D-G_B is explained by strongly regularized tiny centered sequence/geometry disagreement variance. Reproduced original three-seed geometry-mixture K sweeps within 6.16e-10 macro RMSE. No training or hyperparameter updates. Real frozen model evidence: research/geometry_factorial_dev/factorial.json and SUMMARY.md. Engineering suite now 26/26 PASS; scientifically approved BindingDB source tasks 0. Conclusions limited to development; no independent/perceiver paper superiority.

## 6 November 2026 — six publication-source task evidence checks (research provenance, not model metrics)

| Source-level category | Preliminary records |
| --- | ---: |
| Recombinant ANXA3 SPR publication + externally indexed assay | 48 |
| Three kinases with published Kd supplementary table; domain identity pending | 63 |
| Original PGK NMR-binding bibliography, method detail pending | 18 |
| PA-I lectin original PMID points to review rather than experimental report | 18 |
| **Total inspected (unapproved)** | **147** |

All six task identifiers/PMIDs/counts matched original review CSV; zero numeric source-value rows authenticated, zero task approvals. See research/source_access_v4/six_task_publication_evidence.json and SIX_TASK_PUBLICATION_EVIDENCE.md. No changes to model weights, no training, no new independent model performance result.

## 6 November 2026 — 30-reference protein-only pairwise homology challenge (NOT model fitting)

| Finding | Count |
| --- | ---: |
| Review candidate reference protein sequences | 30 |
| Existing MMseqs source-review components | 30 |
| Independent Smith-Waterman local protein pair alignments | 435 |
| Weak >=30% local identity/80% shorter-coverage cross-component pairs | 2 |
| Cross-component pairs with >=40% identity, >=70% shorter coverage | 0 |
| Cross-component pairs with >=30% identity and >=50% longer coverage | 0 |
| New scientifically source-approved task count | 0 |
| New frozen scientifically independent protein-group test split | None |

The two weak pairs were CFTR/ANXA3 and PDE6D/ENPP1 with only 18.2% and 14.5% coverage of the longer protein, respectively. Such low coverage is not verified biological homology. Record is a sequence-clustering policy sensitivity analysis only. Inputs were the unchanged protein-only FASTA and canonical 30-task source metadata, not compounds or affinity records. Evidence `research/source_access_v4/protein_only_review30_pairwise_audit.json`.


## 11 November 2026 — opt-in pocket interaction repair

Implemented `dynacpi/pocket_interaction_dev.py` and a matched four-arm engineering runner (`scripts/train_pocket_repair_dev.py`) on `v5-redesign`. Direct compound features, pocket-restricted distance messages, compound-conditioned attention, jointly trainable heads and exact missing-geometry fallback are implemented. The original v4 architecture/checkpoints and demo endpoints are unchanged. This is an experimental extension, not a validated replacement model.

The completed BALM descriptor probe (5 folds x 2 repeats; 5,808 TRAIN rows in 253 groups) did not establish structural benefit: pooled RMSE 1.487624 baseline vs 1.506438 with structure; group-macro delta -0.009682 with 95% CI [-0.0354, 0.0151]. Reserved test remains unscored. These are development engineering results, not approved exact-Kd cohort evidence.

Implementation, input contract, limitations and full aggregate results: [pocket repair report](research/pocket_repair_20261110/README.md). Run `python scripts/validate_pocket_repair_dev.py` for the new engineering checks; saved `validation.json` records the result and source hashes. No real-affinity pocket-model training is claimed: a provenance-backed, residue-aligned pocket feature bundle is still required. Scientific cohort review requirements remain in force.


## 11 November 2026 — v5.2 structural token interaction experiment

Implemented bidirectional atom/residue attention, direct fingerprint preservation, local invariant structural tokens, a train-only feature builder, matched four-arm training and read-only mechanism diagnostics. Completed 24 real-data engineering fits (3 seeds x 4 arms x uncapped/capped correction policies) on an internal holdout of the BALM TRAIN partition. No reserved-test scoring.

Mean pooled RMSE: ridge 1.489130; uncapped real-geometry residual 1.708872; capped real-geometry residual 1.535797; capped shuffled 1.535785. Capping reduces harm, but no reliable geometry advantage or baseline win. Compound representations remain diverse; neither chemical discrimination nor nonzero geometry sensitivity establishes useful residue correspondence. Six new engineering tests passed. This borrows an interaction-design idea from GenSPARC but does not use its pretrained SaProt/SPMM representations or claim replication.

Details, exact scope, full negative outcomes, commands and limitations: [structural token experiment](research/structural_token_trial_20261111/README.md). Core v4 inference and original checkpoints remain unchanged.


## 2026-11-11 v5.3 — frozen pretrained structural probe (engineering only)

Completed ESM-2 35M versus SaProt 35M real/shuffled 3Di on the reused TRAIN-only internal holdout (4,982 fit / 826 eval rows, 50 held groups). Shared ridge baseline pooled/macro RMSE 1.480541/1.267409; ESM-2 1.478252/1.266147; real SaProt 1.409843/1.230320; shuffled SaProt 1.504710/1.240530. All paired group-bootstrap intervals cross zero. This is a promising point estimate, not an independent geometry win. Real vs shuffled pooled delta -0.094868, CI [-0.206812,+0.011850]. All 298 protein caches and three deliberately corrupted token controls passed validation. Readout includes explicit compound-protein products and train-only inner-fold transforms; each arm selected scale .3. Original model/demo defaults and reserved test remain unchanged. Full protocol, provenance, limitations and reproduction: research/pretrained_structure_probe_20261111/README.md. Next: fixed-protocol TRAIN-only outer group CV; no reserved-test scoring.


## 2026-11-11 v5.4 — nested TRAIN group CV reverses the single-holdout impression

ENGINEERING ONLY: completed five outer protein-group folds with the unchanged v5.3 three-fold inner scale selection. All 5,808 frozen-TRAIN rows receive exactly one out-of-fold prediction across 253 groups. Pooled/macro RMSE: baseline 1.556304/1.362221; ESM-2 1.548379/1.335627; real SaProt 1.569070/1.345643; shuffled SaProt 1.561716/1.341636. No reproducible 3D advantage: real-minus-ESM2 pooled delta +0.020691, 95% conditional group-bootstrap CI [-0.019755,+0.060261]. All paired intervals cross zero. Real SaProt beats shuffled pooled RMSE in 4/5 folds but loses in aggregate due to a large reversal in fold 3 (zero-based); inner selection chose scale 1.0 there. This suggests sensitivity to transfer/regularization, not proof of its cause. Preserved v5.3's positive single-holdout result alongside this negative stronger check. Validation independently reproduced metrics and rejected duplicate/missing-row and cross-fold-group controls. No reserved test scored, no demo default changed. Protocol, per-fold scores, selection and details: research/pretrained_structure_cv_20261111/README.md.


## 2026-11-13 v5.5 — pretrained readout/strength factorial

ENGINEERING ONLY: completed 15 new nested outer-fold evaluations plus the prior matched cell. Limiting interaction-feature scale to .3 improves real SaProt pooled/macro RMSE from 1.569070/1.345643 to 1.529681/1.320468; capped ESM-2 remains better pooled at 1.520691 (macro 1.325041). Removing compound products yields real SaProt 1.530454/1.324015 (max scale 1), so explicit products add little to the current structure representation. Protein-only max .3 real beats shuffled in all five folds on pooled RMSE; conditional exploratory paired pooled delta -0.040778 CI [-0.074428,-0.007199], macro -0.025002 CI [-0.049271,-0.001170]. This is primarily additive protein information, not proven ligand-specific structure learning. No confirmed advantage over ESM-2; reused development cohort and unadjusted intervals. All new cells passed coverage, group-isolation and metric checks; shared baseline predictions match across cells. Reserved test and demo defaults untouched. See research/pretrained_readout_factorial_20261113/README.md.


## 2026-11-13 v5.6 — bounded ligand-conditioned residue attention pilot

ENGINEERING ONLY. Completed 40 fits (5 TRAIN group folds x 2 seeds x sequence attention / real SaProt attention / shuffled SaProt attention / uniform real pooling). Two-seed averaged pooled/macro RMSE: ESM attention 1.553666/1.350400; real attention 1.539896/1.337485; shuffled attention 1.566139/1.346996; uniform real pooling 1.534368/1.338142. Real attention coverage averages 95.2%; no demonstrated localization benefit over averaging. Paired real-minus-uniform pooled delta +0.005528 CI [-0.000721,+0.012377]. No confirmed advantage over matched sequence or shuffled controls; v5.5 capped ridge remains stronger. Residue-cache mean reconstruction, model invariance/gradient checks and independent metric/correction audits passed. Original baseline reproduced exactly. Reserved test/demo unchanged; bounded five-epoch pilot is exploratory, not exhaustive architecture training. See research/residue_attention_probe_20261113/README.md.


## 2026-11-13 v5.7 — joint sequence + protein-structure ridge

ENGINEERING ONLY. Completed five nested TRAIN group folds combining fixed .3 ESM interaction features with an added protein-only block tuned on inner folds. Strong sequence pooled/macro RMSE 1.520691/1.325041; joint real SaProt 1.521185/1.314274; duplicate ESM control 1.523027/1.326797; shuffled structure 1.527305/1.330895. Macro point estimate improves 0.81%, pooled is marginally worse; paired macro delta -0.010767 CI [-0.029351,+0.007495], pooled +0.000494 CI [-0.021483,+0.021797]. All paired intervals include zero. Joint structure contributes additive protein information, not demonstrated ligand-specific geometry. Outer predictions cover all 5,808 rows/253 groups; all metrics independently reproduced, strong sequence baseline exactly reproduced. Prior results preserved; serving default and reserved test unchanged. See research/joint_structure_probe_20261113/README.md.


## 2026-11-13 v5.8 — repeated protein-group split robustness

ENGINEERING ONLY. Repeated the fixed v5.7 joint protocol with outer seeds 4111 and 4112 (10 new nested outer folds), retaining seed 4110. Joint structure improves macro RMSE on 3/3 partitions but pooled RMSE on only 1/3. After averaging per-row squared errors across splits before rooting, sequence pooled/macro RMSE is 1.481581/1.335603 and joint real structure 1.479785/1.325785. Paired group-bootstrap macro delta -0.009818 CI [-0.027651,+0.007313]; pooled -0.001797 CI [-0.023460,+0.018970]. All paired intervals versus sequence, duplicate sequence and shuffled controls include zero. No confirmed 3D superiority or comparison win against the base paper. Every repeat passed independent coverage/group/metric audits. Reserved test and serving defaults unchanged. See research/joint_repeats_20261113/README.md.


## 2026-11-13 v5.9 — correction: separate backend already has six matched external wins

Read-only integrity audit reconciled the completed dynacpi-better-version external benchmark program with this branch's separate 3D probes. Existing sequence-based LowRankDynaCPI v5 beats tested original PerceiverCPI two-seed runs on pooled AND macro RMSE in all six KIBA/Metz cold-split comparisons; all three KIBA splits and Metz double-cold have both descriptive paired intervals below zero. All six data/split/result/bootstrap links and 24 checkpoint hashes verified; no test values parsed, rescoring, training or serving changes. This is not a gain from our 3D work and not exact original-paper-fold replication. Earlier blanket statements that no PerceiverCPI win existed were too broad. Older backend prose listing three pending scenarios is superseded by its completed aggregate. BALM structure-probe reserved test remains untouched. See research/external_benchmark_reconciliation_20261113/README.md and results.json. Current performance priority: preserve and report existing matched wins; require a new matched evaluation protocol for any further tuned system.


## 2026-11-13 v5.10 — same-encoder 3D neighborhood controls (Demo-smth only)

ENGINEERING ONLY. Forty fits compare actual 3D nearest-neighbor pooling with sequence neighbors and permuted coordinates using identical ESM-2 residue features. Spatial pooled/macro RMSE 1.544658/1.347727 vs sequence 1.545216/1.348271, shuffled 1.546621/1.348250, spatial uniform pooling 1.545643/1.345651. Spatial-minus-sequence pooled delta -0.000559 CI [-0.002064,+0.000610]; no demonstrated meaningful geometry benefit. Neighbor membership differs by 40.62% but attention remains broad (95.64% mean effective coverage). All 40 result audits, exact baseline reproduction, geometric invariance and model checks passed. Stop repeating this local-average design; next changes must preserve explicit edge/contact information or binding-region relevance. Scope is ONLY additional 3D gains in Demo-smth, not the separate 2D wins. dynacpi-better-version untouched. New local arrays/checkpoints are gitignored under research_local; reserved test untouched. Details: research/spatial_neighborhood_probe_20261113/README.md.


## 2026-11-13 — v5.11 explicit contact-graph engineering probe

Completed 30 matched fits on the reused frozen BALM TRAIN cohort (5,808 pairs, 253 groups), with identical ESM2 features and explicit compound-conditioned distance messages. Pooled RMSE: sequence graph 1.542909, real geometry 1.542005, scrambled geometry 1.542276. Real-minus-scrambled delta -0.000271 has descriptive 95% interval [-0.000964, +0.000311]: no clear geometry-specific gain. Zeroing edge attributes changes predictions by mean RMS 0.000182 versus total correction RMS 0.203545; the trained distance pathway remains weak despite passing nonzero-gradient and sensitivity checks. All 30 fits and saved metrics independently validated. Reserved test remains unscored. See [full protocol, results and next experiment](research/contact_graph_probe_20261113/README.md). This is an opt-in research implementation, not a change to the original v4 core architecture.


## 2026-11-13 — v5.12 objective diagnosis and paired-loss experiment

Existing real-graph corrections are 99.8697% protein-mean energy; within-protein error MSE worsens by 0.000979 while protein-mean error MSE improves by 0.045282. These are post-hoc decompositions of reused TRAIN-CV predictions, not inference-time label calibration. 61 of 298 proteins have one observation, contributing no within-protein information. 46.04% of per-seed corrections exceed 95% of the 0.25 cap. This supports protein-offset dominance but does not isolate its cause or separate compound main effects from interactions.

Implemented scripts/train_contact_pair_objective_dev.py: adds unit-weight same-protein pair-difference residual MSE to the existing absolute residual MSE. Distinct row partners come exclusively from the current outer training fold; singleton proteins retain absolute loss only. Independent pairing RNG preserves anchor minibatch schedules. Same architecture, cap, epochs, seeds and three geometry controls; additional forward computation means compute is not matched to the previous objective. Thirty fits launched; no performance result yet. Existing synthetic architecture checks run before training, and runtime assertions enforce partner identity and fold separation. Reserved test remains unscored.


## 2026-11-13 — v5.13 paired-objective result (negative)

All 30 paired-loss fits finished and independently validated. Real-geometry pooled/macro RMSE 1.551390/1.345115 is worse than the previous absolute-only objective 1.542005/1.343510. Within-protein correction energy increased about 10.6-fold, but within-protein error MSE worsened from 1.282811 to 1.288251. Protein-wide correction energy remains 98.629%; 46.30% of corrections remain near the cap. Real-minus-scrambled pooled delta -0.000356 has descriptive 95% interval [-0.001232, +0.000437]. Do not promote this objective. This reused TRAIN-only engineering result is not an independent superiority claim; the reserved test remains unscored. Same-protein pairs are not verified same-assay pairs. Full results: research/contact_pair_objective_20261113/README.md. Next diagnostic should distinguish training-fit failure from held-group generalization and audit pair assay comparability before further loss tuning.


## 2026-11-13 — v5.14 pose-free interaction engineering gate

Implemented opt-in complete molecular-graph preprocessing and a bond-aware atom/residue pair-value model. Synthetic interaction fit MSE 0.396829 -> 0.000014919 in 400 fixed steps; permutation, padding, batch, gradients, bond sensitivity and complete 110-atom preprocessing tests pass. No real affinity training or demonstrated 3D gain. The model accepts residue features but does not itself implement SaProt/SPMM or docking; it is not a GenSPARC reproduction. Schema-only inspection finds no assay/construct/provenance columns in the public BALM Arrow file, so same-protein pairs cannot be certified same-assay from it. See research/pose_free_interaction_20261113/README.md for limitations and remaining fit/data gates. Reserved test untouched.


## 2026-11-13 — v5.15 real-data atom/residue fit diagnostic

Completed and independently validated four fixed-budget fits on a tiny frozen-TRAIN panel (64 fit rows/four proteins, 64 held rows/four other groups). Complete molecular graphs are recovered from source metadata; pretrained ESM2/real SaProt/shuffled SaProt residues are hash verified. Real-structure train RMSE 0.259692 vs constant 1.762829, but held RMSE 1.952780 vs constant 1.741742; sequence 1.934855 and shuffled 1.773211 also beat real on held pooled error. Chemical-only train RMSE 0.279797 indicates training fit alone does not establish interactions. All learned arms lose to the constant held baseline. Conclusion: successful training fit, poor transfer, no 3D gain. One seed, tiny reused panel, unknown assay comparability, existing uniformly sampled residues; no broad scientific conclusion. Details: research/atom_residue_panel_20261113/README.md. No full sweep launched.


## 2026-11-13 — v5.16 full-residue preprocessing repair

Label-free audit: prior uniform cache retains 28,604/157,568 positions (18.1534%) across 298 proteins; 180 retain under 25%. This is token retention, not measured information loss or pocket coverage. Implemented full ragged residue caches for real SaProt, shuffled SaProt and ESM2, with model/feature hashes and old sampled-token/global-mean agreement checks. Generation launched; independent validator requires all three completed arms before training use. No new affinity result. Details and completion evidence: research/full_residue_cache_20261113/README.md.
