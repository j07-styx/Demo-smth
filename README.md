# Demo-smth — DynaCPI v4 Research Handoff

**Snapshot date:** 5 November 2026  
**Git commit labels:** Version 0.1–0.4 refer ONLY to the sequence of repository uploads; **the DynaCPI model remains v4.0 throughout**. See [CHANGELOG.md](CHANGELOG.md).  
**State:** Working engineering prototype; scientific superiority NOT established.  
**Repository:** https://github.com/j07-styx/Demo-smth (initially private)  
**Original foundation:** [PerceiverCPI (dmis-lab)](https://github.com/dmis-lab/PerceiverCPI). Preserve upstream attribution and MIT license in [LICENSE.txt](LICENSE.txt) and [UPSTREAM_README.md](UPSTREAM_README.md).

> **New AI/engineer: read [AGENTS.md](AGENTS.md) and [HANDOFF_FOR_NEXT_AI.md](HANDOFF_FOR_NEXT_AI.md) before changing code or training.** They contain the full operating instructions, verified artifacts, blockers and next actions.

## What is DynaCPI v4?

DynaCPI v4 is a **sequence-plus-geometry compound–protein binding-affinity predictor** with **support-conditioned calibration and differential geometry adaptation**. It is **NOT the earlier four-expert mixture-of-experts (MoE) design**.

1. Compound: molecular graph / D-MPNN and Morgan fingerprints from PerceiverCPI-related code.
2. Protein sequence: frozen ESM-2 650M layer-33 embeddings passed to a trainable sequence foundation.
3. Optional 3D protein geometry: 3-layer GVP-GNN using correctly mapped N/CA/C/O backbone graphs, pLDDT/PAE, and explicit sequence-only fallback.
4. Two complete affinity predictions, sequence s(c,p) and geometry-enhanced g(c,p), in raw pKd units.
5. Same-assay few-shot support: measured compound affinities, stereo-aware Morgan Tanimoto similarity raised to power 4, bounded calibration b and centered differential correction delta.
6. Controlled comparisons: **A** = zero-shot, **B** = A + calibration, **C** = A + differential, **D** = A + both.

**Primary research hypothesis:** Does D improve over B under identical support sets and genuinely unseen, source-verified protein clusters? **Not yet established.**

## Verified checkpoint — 5 November 2026

| Milestone | Evidence |
| --- | --- |
| Original PerceiverCPI | All 1,148 archived DAVIS fold-zero predictions exactly reproduced using original checkpoint and preprocessing |
| ESM feature integrity | 462/462 staged protein embedding tensors valid; 346,865 residues, 570 windows |
| Geometry mapping | 9 engineering training and 4 validation proteins with exact UniProt contiguous subsequence mapping; ROCK2 offset handled |
| Sequence training | 3 supervised epochs on 1,296 DAVIS engineering pairs; best observed target-macro validation RMSE 0.811185 (epoch 1), saved checkpoint epoch 3 |
| Geometry training | 2 supervised epochs on 486 pairs; best validation RMSE 0.935921 vs 0.925685 sequence-only, i.e. worse |
| A/B/C/D development diagnostic | Four kinase development targets, K=5 and ten draws: B and D effectively identical (~0.860139 target-macro episode RMSE) |
| BindingDB audit | Full November 2026 download verified locally; 1,146 preliminary K=5 candidate tasks in 168 preliminary protein components |
| Scientific eligibility | Zero exact-Kd tasks source-approved and no frozen five-way protein-group split |
| Engineering checks | Latest consolidated suite: **15/15 passed** |

These scores are **not independent protein-family scientific test results** and do NOT demonstrate superiority over published PerceiverCPI.

## Where everything is

| Path | Purpose |
| --- | --- |
| [AGENTS.md](AGENTS.md) | Strict AI operator behavior, stop/go gates and prohibited shortcuts |
| [HANDOFF_FOR_NEXT_AI.md](HANDOFF_FOR_NEXT_AI.md) | Detailed continuation manual, order of operations and verification commands |
| [PROGRESS_AND_NEXT_STEPS.md](PROGRESS_AND_NEXT_STEPS.md) | Prioritized backlog with acceptance criteria |
| [EXPERIMENT_LEDGER.md](EXPERIMENT_LEDGER.md) | Exact observations and negative results |
| [REPRODUCIBILITY.md](REPRODUCIBILITY.md) | Environment, data rehydration, commands and manifests |
| [CHANGELOG.md](CHANGELOG.md) | Dated version x.1 / x.2 / x.3 / x.4 commits |
| [project.md](project.md) | Original full chronological project handoff, preserved |
| [research/DynaCPI_Manuscript.md](research/DynaCPI_Manuscript.md) | Technical manuscript with honest scientific limitations |
| [research/Kd_Curation_and_Split_Protocol.md](research/Kd_Curation_and_Split_Protocol.md) | Exact-Kd eligibility and independent split requirements |
| [research/BindingDB_30_Source_Evidence_Dossier_20261105.md](research/BindingDB_30_Source_Evidence_Dossier_20261105.md) | Thirty-task, label-blind source evidence packet, none approved |
| [dynacpi/](dynacpi/) | Model, GVP, adapter, inference, cohort gate, evaluator |
| [tests_v4/](tests_v4/) | Numerical, leakage, structure and saved-model tests |
| [scripts/](scripts/) | Preprocessing, source audits, training pilots and validation commands |
| [data/audit/](data/audit/) | Compact audits and preliminary (not approved) episode manifests |
| [data/engineering_pilot/](data/engineering_pilot/) | Legacy DAVIS engineering-only labels, protocol and selected 3D graphs |
| [research/pilot_sequence/checkpoint.pt](research/pilot_sequence/checkpoint.pt) | Trained sequence pilot weights, epoch 3 |
| [research/pilot_geometry_9train_4val/best_checkpoint.pt](research/pilot_geometry_9train_4val/best_checkpoint.pt) | Trained geometry pilot weights, epoch 1 |
| [research/pilot_perceiver/checkpoint.pt](research/pilot_perceiver/checkpoint.pt) | Saved preliminary PerceiverCPI engineering checkpoint |
| [provenance/snapshot_file_manifest.json](provenance/snapshot_file_manifest.json) | Every copied file's SHA-256 and excluded-file reasons |

## Getting started

~~~powershell
git clone https://github.com/j07-styx/Demo-smth.git
cd Demo-smth
Get-Content .\AGENTS.md
Get-Content .\HANDOFF_FOR_NEXT_AI.md
# Set up Python, CUDA and the excluded ESM cache as in REPRODUCIBILITY.md.
.\.venv\Scripts\python.exe scripts\run_v4_validation_suite.py
~~~

**A fresh clone alone will not pass the full suite**: the approximately 848 MiB of generated ESM protein embedding tensors are excluded from Git and must be reconstructed using scripts/extract_esm.py or transferred from a trusted local cache after hash validation.

## Non-negotiable research integrity

Do not train on unreviewed BindingDB candidates as if they form an approved study; do not mix Kd with Ki, IC50 or KIBA; do not equate a UniProt annotation with the physical experimental construct; do not expose query labels through cross-assay support; do not reinterpret DAVIS development data as an independent test; and do not claim DynaCPI v4 has beaten the baseline.

The main blocker is scientifically approving a large enough exact-Kd cohort, then freezing protein-family-disjoint roles before matched D-vs-B experiments.

## Latest continuation — 6 November 2026

The original DynaCPI v4 workspace was resumed in VS Code without changing its two-predictor architecture or the original trained checkpoints. On a fixed four-target DAVIS development cohort (not a source-approved protein-family holdout), a new K=0/1/2/5/10/20 support-size sweep found calibration B macro RMSE improving modestly from 0.861017 at K0 to 0.857389 at K20 for original seed 1105, but **full D did not measurably improve upon B**. A three-seed geometry engineering diagnostic found best-epoch macro RMSEs 0.935921 (seed 1105), 0.920050 (1106) and 0.915971 (1107), against frozen sequence 0.925685. Seed sensitivity did **not** rescue support-based differential adaptation: D−B at K20 was approximately 2.46e-10, 2.00e-10 and 2.48e-8, respectively. These are reused development-validation targets, not independent test results.

The refreshed engineering test suite passed **17/17 checks** on 6 November. See [research/monitoring/LATEST.md](research/monitoring/LATEST.md), [research/support_k_sweep_dev/SUMMARY.md](research/support_k_sweep_dev/SUMMARY.md) and [research/pilot_geometry_seed_sweep_dev/ADAPTER_SEED_COMPARISON.md](research/pilot_geometry_seed_sweep_dev/ADAPTER_SEED_COMPARISON.md). A read-only hourly benchmark watch has been enabled while the remote computer is accessible; it does not train models. The scientific BindingDB approval gate is still **BLOCKED**: zero source-reviewed exact-Kd tasks and no frozen independent protein-cluster split.

## Latest source-evidence checkpoint — 6 November 2026

The 30-task exact-Kd source-review preparation now has a machine-generated **primary-source access index** and an immutable-human-review worklist. All 20 unique PubMed article IDs resolved to official metadata; two public open-access full texts yielded non-copying method-section indexes, 17 were metadata-only through the API, and one OA XML document was deliberately rejected because of DTD/entities. Seven candidate tasks require primary patent review and one has no usable primary-source identifier. **30/30 review tasks remain UNREVIEWED, zero approved.** The prior scientific cohort gate remains blocked. No raw paper bodies or source-unapproved affinity labels were introduced in this step.

The expanded engineering regression suite passed **18/18 checks**. See research/source_access_v4/SOURCE_ACCESS_SUMMARY.md and REVIEW_ACTIONS.md, or launch the updated source-review VS Code tasks. This source-access inventory is not an assay-validity decision and does not justify starting the main BindingDB model study.

## Source-construct alignment checkpoint — 6 November 2026

Two original method papers in the fixed thirty-task source-review queue identify physical protein regions shorter than the canonical full-length reference sequences retained in their unapproved BindingDB candidate records: P17342 NPR-C 27–541 (515 residues nominal) versus a 541-residue canonical record, and O14786 NRP1-b1 273–427 (155 nominal) versus a 923-residue canonical record. These are **possible model-input-to-experimental-construct alignment problems**, not proof individual Kd records are wrong. Exact physical sequences, measured values, qualifiers, and source-table mapping remain unverified. See [research/source_access_v4/PRELIMINARY_CONSTRUCT_ALIGNMENT_REVIEW.md](research/source_access_v4/PRELIMINARY_CONSTRUCT_ALIGNMENT_REVIEW.md). The newest regression suite is **19/19 PASS**; no scientific cohort approval.

## Latest source metadata review — 6 November 2026

A reproducible **30-assay, affinity-label-independent metadata triage** now prioritizes the existing fixed BindingDB manual review set: 4 urgent endpoint/source-ambiguity cases (P0), 12 construct/endpoint review cases (P1), and 14 standard source review cases (P2). Metadata flags include six descriptions with numeric protein-region spans shorter than the canonical reference sequences, eight with labeled/tagged reagents, and four with possible activity-endpoint wording. These are *review indicators only*, not proof a BindingDB Kd value is wrong. The protected human-review CSV is unchanged; **all 30 tasks remain UNREVIEWED, zero scientifically approved**.

Artifacts: [ASSAY_METADATA_TRIAGE.md](research/source_access_v4/ASSAY_METADATA_TRIAGE.md), [triage JSON](research/source_access_v4/assay_metadata_risk_triage_30.json), CSV and script `scripts/triage_30_assay_metadata_v4.py`. The engineering validation suite passed **20/20 checks**; the scientific main experiment is still blocked. No DynaCPI architecture or model checkpoint changed.

## P0 source-evidence crosswalk and bibliographic correction — 6 November 2026

Four previously flagged high-priority assay records now have documented external source evidence levels, outstanding verification questions, and immutable source IDs, without extracting any measured affinity values or approving a task. The carbonic-anhydrase II record was previously described as lacking a primary source identifier; that description was incomplete because the review CSV has a valid **DOI** field. The regenerated index correctly calls the task `PRIMARY_DOI_ONLY_METHODS_PENDING`, not `MISSING_PRIMARY_SOURCE_IDENTIFIER`. See [P0_SOURCE_CROSSWALK.md](research/source_access_v4/P0_SOURCE_CROSSWALK.md). The 30-task review remains unchanged and unapproved; the expanded engineering suite passed **21/21 checks**, with ten VS Code tasks and the existing read-only monitor updated. There is no model architecture change or improved prediction claim.

## New real-data source lineage audit — 6 November 2026

The original Windows workspace was reconnected and the fixed 30-UNREVIEWED-task preliminary BindingDB subset underwent a REAL technical raw-record lineage audit. The dataset has **919 grouped compound entries, 921 original BindingDB reactant IDs**, and two two-measurement groups. **921/921 original source reactants and 921/921 unaggregated candidate values were recovered**, with zero critical numerical/identity/aggregation inconsistencies. All 921 raw Kd strings were strictly numeric and their pKd conversions matched the upstream candidate records. The complete regression suite passed **23/23 checks**, including 5/5 new synthetic lineage cases and the real-data integrity check.

See research/source_access_v4/RECORD_LEVEL_PROVENANCE_30.md and record_level_provenance_30.json (aggregate-only). The new code is in scripts/audit_30_record_level_provenance_v4.py and tests_v4/record_lineage_{synthetic,real_integrity}_test.py. VS Code has 11 executable tasks; the read-only monitor now checks this artifact and reports technical flag counts.

**Crucial:** exact arithmetical Kd-field provenance is NOT evidence that the physical assay measured true Kd for the correct target construct. All thirty primary-source review tasks remain UNREVIEWED, none approved, no frozen independent protein split exists, and no scientific BindingDB model evaluation was run. The original PerceiverCPI and DynaCPI v4 model checkpoints remain unchanged.

## New private source-evidence workflow — 6 November 2026

DynaCPI v4 now has a source-record-level human-review worksheet generator for all **921 original BindingDB reactant records belonging to the 30 fixed UNREVIEWED tasks**. On the authorized Windows computer, `scripts/build_record_source_evidence_worklist_v4.py` creates a **local-only** worksheet at `data/audit/source_record_evidence_worklist_30_LOCAL_PRIVATE.csv`, with immutable task, assay and protein hashes, source identifiers, and blank experimental construct/endpoint/table-evidence fields. This local file is explicitly excluded from Git and **does not contain affinity numbers or chemical structures**.

The public [source-review readiness summary](research/source_access_v4/RECORD_SOURCE_EVIDENCE_READINESS.md) contains only counts and input SHA-256 checks. Every one of the 921 records is still UNREVIEWED; zero scientifically approved assays or frozen independent protein-family split exists. The validator rejects incomplete or contradictory evidence declarations and cannot authorize scientific training itself. Ten synthetic validation scenarios and a real-data 921-row integrity check were added to the full engineering suite, which now includes 25 checks. The existing DynaCPI v4 architecture, archived checkpoints and negative DAVIS development observations remain unchanged.

## Latest DynaCPI v4 geometry ablation — 6 November 2026

The newest work is a REAL frozen-model comparison, not another source metadata audit. Five matched variants were evaluated on the same four geometry-checkpoint-selected DAVIS development proteins: sequence-only S0, sequence-only calibrated S_B, geometry-mixture G_A, geometry-mixture calibrated G_B, and full geometry differential G_D. The experiment used three saved geometry initialization seeds (1105,1106,1107), K=0,1,2,5,10,20, ten fixed query compounds and ten label-blind support draws per target (720 correlated target-draw-K evaluations). No weights were trained or altered.

At K=5, S_B macro RMSE=0.857337 for all seeds; G_B=0.860139 (1105), 0.855587 (1106), 0.854164 (1107). G_D-G_B differences are at most 5.43e-9 RMSE. The incremental geometry-differential adapter is effectively inactive; geometry's main effect depends on initialization and target. Original frozen outputs were reproduced within 6.2e-10 RMSE. Full engineering suite: **26/26 PASS**. See research/geometry_factorial_dev/SUMMARY.md and factorial.json.

**No scientific improvement over PerceiverCPI has been established.** Only four development-selected DAVIS proteins and unverified source labels were evaluated. The independent exact-Kd cohort remains blocked at 0/30 source-approved tasks, and no family-disjoint test exists.

## Updated original-publication source evidence — 6 November 2026

Six immutable BindingDB source-review tasks (147 preliminary rows) now have primary-publication and independent assay-registry evidence checks: see research/source_access_v4/SIX_TASK_PUBLICATION_EVIDENCE.md. ANXA3 has 48 entries and an original SPR paper plus a matching-count external assay registry; three kinase-domain tasks totaling 63 rows point to an original supplementary binding Kd table but require experimental domain and individual table concordance; an NMR phosphoglycerate kinase study accounts for 18 more; and the PA-I lectin 18-row task unexpectedly cites a review article, not the original experimental source. All observations remain bibliographic/assay-level rather than per-record verification; zero scientifically approved tasks and no new BindingDB training.

## Independent protein-only family-split leakage challenge (6 November 2026)

The existing preliminary MMseqs2 grouping assigned the 30 unreviewed source-review protein sequences to **30 different components**. A new independent Biopython Smith–Waterman/BLOSUM62 scan of all **435 protein pairs** tested six sequence identity, alignment-length and coverage policies, without reading compounds or affinity labels. At a permissive 30% identity, 80% shorter-sequence coverage and 80 matched alignment positions, two cross-existing-component matches appeared. They covered only 14.5–18.2% of the longer protein, and none survived any reciprocal >=50% longer-sequence coverage criterion or more stringent identity thresholds.

See [protein-only split-leakage report](research/source_access_v4/PROTEIN_ONLY_HOMOLOGY_CHALLENGE.md). These uncertain local alignments are not confirmed biological homology; a final independent cohort will require domain/construct review in addition to a documented sequence-coverage policy. No scientific task approvals or final protein-group split were created. The script and integrity test are incorporated into the **28/28 PASS** engineering suite and the 14th VS Code task.


## 11 November 2026 — opt-in pocket interaction repair

Implemented `dynacpi/pocket_interaction_dev.py` and a matched four-arm engineering runner (`scripts/train_pocket_repair_dev.py`) on `v5-redesign`. Direct compound features, pocket-restricted distance messages, compound-conditioned attention, jointly trainable heads and exact missing-geometry fallback are implemented. The original v4 architecture/checkpoints and demo endpoints are unchanged. This is an experimental extension, not a validated replacement model.

The completed BALM descriptor probe (5 folds x 2 repeats; 5,808 TRAIN rows in 253 groups) did not establish structural benefit: pooled RMSE 1.487624 baseline vs 1.506438 with structure; group-macro delta -0.009682 with 95% CI [-0.0354, 0.0151]. Reserved test remains unscored. These are development engineering results, not approved exact-Kd cohort evidence.

Implementation, input contract, limitations and full aggregate results: [pocket repair report](research/pocket_repair_20261110/README.md). Run `python scripts/validate_pocket_repair_dev.py` for the new engineering checks; saved `validation.json` records the result and source hashes. No real-affinity pocket-model training is claimed: a provenance-backed, residue-aligned pocket feature bundle is still required. Scientific cohort review requirements remain in force.


## 11 November 2026 — v5.2 structural token interaction experiment

Implemented bidirectional atom/residue attention, direct fingerprint preservation, local invariant structural tokens, a train-only feature builder, matched four-arm training and read-only mechanism diagnostics. Completed 24 real-data engineering fits (3 seeds x 4 arms x uncapped/capped correction policies) on an internal holdout of the BALM TRAIN partition. No reserved-test scoring.

Mean pooled RMSE: ridge 1.489130; uncapped real-geometry residual 1.708872; capped real-geometry residual 1.535797; capped shuffled 1.535785. Capping reduces harm, but no reliable geometry advantage or baseline win. Compound representations remain diverse; neither chemical discrimination nor nonzero geometry sensitivity establishes useful residue correspondence. Six new engineering tests passed. This borrows an interaction-design idea from GenSPARC but does not use its pretrained SaProt/SPMM representations or claim replication.

Details, exact scope, full negative outcomes, commands and limitations: [structural token experiment](research/structural_token_trial_20261111/README.md). Core v4 inference and original checkpoints remain unchanged.
