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
