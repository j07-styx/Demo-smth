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
