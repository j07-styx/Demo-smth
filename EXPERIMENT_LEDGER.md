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
