# AGENTS.md — Mandatory instructions for a continuing AI

**Project:** DynaCPI v4. **Source snapshot:** 5 November 2026. **Repository:** j07-styx/Demo-smth, private at creation. **Evidence:** Engineering prototype; no verified improvement over PerceiverCPI.

## Read this before touching anything

1. Read README.md, HANDOFF_FOR_NEXT_AI.md, PROGRESS_AND_NEXT_STEPS.md, EXPERIMENT_LEDGER.md, REPRODUCIBILITY.md, CHANGELOG.md, project.md, research/Kd_Curation_and_Split_Protocol.md, then research/DynaCPI_Manuscript.md.
2. Inspect actual source in dynacpi/adaptation.py, frozen_adapter.py, frozen_pair_predictor.py, sequence_model.py, geometry_branch.py, backbone_graph.py, episode_data.py, scientific_cohort_gate.py, group_split.py and paired_evaluation.py. The code and tests define numerical behavior; do not replace them with inferred equations.
3. Check the git branch, status, previous commits, file hashes and local machine state before executing a command. The repository snapshot and original working directory are separate; never overwrite the original.
4. Establish what data exist on the current PC. This repository intentionally does NOT include the full BindingDB archive or the 462 ESM cache tensor files. A fresh clone cannot pass all 15 GPU/feature tests without rehydrating those dependencies.
5. Classify work as ENGINEERING CHECK, PRELIMINARY DATA AUDIT or SOURCE-APPROVED SCIENTIFIC EXPERIMENT. Never present one as another.

## Fixed architectural intent — do not silently redesign

This project implements DynaCPI **v4**, not the earlier speculative four-expert MoE. The architecture is a PerceiverCPI-derived compound–protein interaction foundation, frozen pretrained ESM-2 650M layer-33 residue features, a sequence predictor s, and an optional 3-layer GVP enhancement that yields a geometric predictor g. There are **two** full predictors, not four separately trained experts. A few-shot adapter uses experimentally measured, same-assay support affinities, Morgan radius-2/2048-bit chirality-aware fingerprints, and Tanimoto similarity raised to power 4.

Four ablation outputs share the same frozen s/g predictors:
- A: fixed zero-shot sequence/geometry combination m0.
- B: m0 plus bounded support residual calibration offset b.
- C: m0 plus bounded centered geometry differential correction delta.
- D: m0 plus b and delta.

Primary scientific claim to test: D improves over B on independently held-out protein clusters using the **same** support sets. This has not been established. Default adapter parameters (w0=0.5, lambda_b=5, lambda_theta=0.1, offset cap 2, differential cap 1 pKd) are engineering defaults, NOT validated research hyperparameters. Consult dynacpi/adaptation.py for exact equations and numerical tests. Missing structure and K=0 must preserve exact fallback.

## Non-negotiable data and scientific rules

- Kd, Ki, IC50, EC50 and KIBA scores are not the same outcome. Only source-verified exact Kd contributes to the primary pKd task; pKd = 9 − log10(Kd in nM). Keep inequalities, qualifier metadata, censoring bounds, protocols and assay provenance; do not silently treat a lower/upper bound as exact.
- Zero of the 30 sampled BindingDB assay tasks has been scientifically source-approved. Preliminary JSONL files under data/audit are **UNAPPROVED** candidate data. Never characterize their existence, sequence matches, or automated flags as approval.
- Require independently approved cohort and frozen protein-component-disjoint role artifacts before scientific BindingDB training or a headline result. dynacpi/scientific_cohort_gate.py must reject missing artifacts; a synthetic unit-test pass is not evidence that the biological data are valid.
- Same-target multi-assay overlap exists. Support labels must come only from the approved same-assay episode; query labels are evaluator-only. Do not train on held-out target queries via a duplicated assay or any alternative data source.
- Source-level publication/patent verification must establish actual experimental target construct, chain composition, domain/mutation/tag, Kd measurement semantics, qualifier, and support/query comparability. A canonical UniProt sequence match alone does not verify a physical experimental construct.
- Cluster all approved protein sequences/constructs and audit shared functional domains and sequence families, with connected components and documented threshold sensitivity. All variants must share exactly the same protein-family role split, query compounds, support draws, seeds, preprocessing and tuning budget.
- Keep independent roles: base_train, base_validation, adapter_train, adapter_validation and test; freeze split before consulting test labels or metrics. Do not use development targets selected for checkpoints as blind test data.
- For AlphaFold graphs, exact sequence-to-structure residue alignment is mandatory. Pilot ROCK2 maps to UniProt 686–1388; an unaligned full-length graph is prohibited. Missing/poor geometry must fall back to the sequence path. A predicted AlphaFold fold is not experimental ligand-bound evidence.
- Convert standardized neural outputs back to pKd using only saved training-set statistics before adaptation. Geometry must be a separate trainable branch over a frozen stage-1 foundation, following the method spec.
- Preserve every negative outcome: the two-epoch GVP pilot was worse than sequence-only, and D−B was essentially zero on the four-target DAVIS development diagnostic. Do not rewrite the manuscript to portray these as successful results.

## Actual evidence as of 5 November 2026

- Original PerceiverCPI: all 1,148 fold-zero archived DAVIS prediction values reproduced exactly with reference checkpoint, preprocessing, batch boundaries and six unchanged reference modules. Not equivalent to reproducing all published benchmarks.
- Real ESM-2 650M feature extraction: 462/462 staged sequences verified, 346,865 residue positions, 570 windows; tensors excluded from Git.
- Full November 2026 BindingDB: source archive downloaded to original PC and checked by ZIP CRC, 3,243,660 source rows, 80,139 preliminary assay-linked Kd candidates; 1,146 preliminary K5 tasks, 168 preliminary protein components, with ZERO source-approved final tasks. These counts are NOT an accepted benchmark.
- 15/15 engineering and numerical validation checks passed on original PC with all dependencies present. See data/audit/v4_validation_suite.json.
- DAVIS sequence foundation: three epochs (1,296 train pairs, 432 validation pairs); target-macro RMSE 0.811185 / 0.813853 / 0.817272. Saved checkpoint is **epoch 3**, though epoch 1 was the best observed validation epoch.
- AlphaFold engineering mapping: 30/32 pilot targets exact reference subsequence matches; 13 usable 3D graphs selected (9 train, 4 validation) using coordinates and PAE.
- GVP engineering pilot: 486 train pairs / 216 validation pairs. Sequence-only 0.925685 target-macro RMSE; best geometry epoch-1 0.935921, worse. 2 of 4 development proteins improved slightly, 2 worsened.
- K=5 A/B/C/D four-target development check, ten support draws: A≈0.861017, B≈0.860139, C≈0.861017, D≈0.860139. Differential D−B≈+5.2e−11, effectively absent. Kernel weights W≈0.003–0.009; this does not establish performance on BindingDB.

## Mandatory execution procedure

For each task:
1. Confirm the exact question being tested and the split/evidence status. State the expected observable pass/fail criterion.
2. Open source and existing tests, read the most recent checkpoint report and inspect dependencies.
3. Make small reversible changes; preserve prior outputs, raw logs, checkpoint checksums and negative results.
4. Run positive AND negative validation tests. Check support/query isolation, chemistry identity, construct mapping and fallbacks.
5. For engineering tests, label results ENGINEERING ONLY. For science, require frozen independent split, correctly approved assays, matched controls and target-cluster paired uncertainty estimates.
6. Never fabricate progress, model gains, citations, reviewer decisions, source agreements or publication readiness.
7. Update project.md, manuscript, experiment ledger and dated CHANGELOG with actual results; push meaningful verified commits.
8. Verify the remote Git commit SHA after pushing. GitHub upload milestone labels (0.1, 0.2, 0.3, 0.4) are **not model architecture versions**.

## Privacy and safety of the repository

Preserve upstream copyright/license in LICENSE.txt and UPSTREAM_README.md. Never commit API keys, browser credentials, tokens, .env files, local venv, full raw archive, huge ESM embeddings or user secrets. The existing pilot checkpoint .pt files are trusted only if their SHA-256 and provenance match the record; do not load arbitrary untrusted torch serialization. Preserve private visibility unless owner changes it.

**Actual next scientific gate:** source-adjudicate exact-Kd measurements and protein constructs across enough independent target families; then freeze final study roles before matched training. No alternate shortcut provides legitimate research evidence.

## Source-access audit gate — 6 November 2026

Before any review or experimental work, inspect research/source_access_v4/source_access_index.json, REVIEW_ACTIONS.md, and the immutable canonical review CSV. Twenty PubMed IDs were identified and two OA article section indexes prepared, but the full original source/assay constructs have not been approved. Automated evidence keyword counts and DOI/PMID metadata do not constitute a valid source review. Zero of thirty tasks has approval. Never change a task to APPROVE, write approved BindingDB cohort artifacts, or freeze a scientific split based solely on this index or a manuscript title. The new integrity check is tests_v4/source_access_index_integrity_test.py; the engineering suite now has 18 checks. Review publication bodies only through permitted sources; never copy copyrighted paper text into the repository.

## New mandatory construct-alignment review rule — 6 November 2026

Original publication methods can identify a protein fragment instead of the canonical full-length UniProt sequence. Two examples (P17342 27–541 versus 541 reference; O14786 273–427 versus 923 reference) are flagged in research/source_access_v4/PRELIMINARY_CONSTRUCT_ALIGNMENT_REVIEW.md. Never feed an entire reference structure as the experimentally verified assayed construct solely because BindingDB stores that canonical accession. First independently verify the source measurement's actual protein region and exact physical sequence, tags, mutations, processing and group-split provenance. Existing tags and region numbers are reviewer leads only; 30/30 source tasks remain UNREVIEWED, no cohort approved. Run the latest 19-check suite and preserve all negative DAVIS development observations.

## All-thirty BindingDB triage scope — 6 November 2026

Before handling any of the fixed thirty candidate assays, read `research/source_access_v4/ASSAY_METADATA_TRIAGE.md`. P0=4, P1=12, P2=14 are **human review priorities only**, never mathematical exclusion rules or approved data labels. The review queue must remain unchanged unless a qualified reviewer documents primary-source evidence. CFTR, GLP1R, PD-L1 and CA2 are prioritization examples, not confirmed invalid entries. For multi-protein VHL/Elongin records do not assign a partner's residue range to the named protein reference. The 20-check suite includes an integrity test guarding source identity, affinity-label isolation and the BLOCKED scientific training gate. No new main training or test before actual approved assay/construct evidence and frozen family groups.

## Corrected source indexing and four high-priority review leads — 6 November 2026

The source-only four-task P0 crosswalk is `research/source_access_v4/P0_SOURCE_CROSSWALK.md`. It records evidence levels, not scientific approval. Source verification must explicitly distinguish measured assay participant/endpoint from a target annotation, functional cell response from direct affinity, and primary article method/record correspondence from mere DOI/patent bibliography. Do NOT auto-reject or approve candidate records from these leads or any high-level source summary. The initial CA2 source-access category was erroneous: an original DOI exists even though PMID and patent metadata are absent. Rebuild and check `PRIMARY_DOI_ONLY_METHODS_PENDING`; do not repeat the missing-source-identifier claim. The complete engineering suite now passed **21/21**, but zero of 30 tasks has independent source approval and no frozen protein-family test split exists. Keep model weights/benchmark evidence unchanged.

## Original BindingDB reactant lineage check — 6 November 2026

Before editing source data, read research/source_access_v4/RECORD_LEVEL_PROVENANCE_30.md and audit script scripts/audit_30_record_level_provenance_v4.py. On the actual Windows files, all 30 unapproved candidate tasks yielded 919 compound groups and 921 raw Reactant_set IDs with 921/921 exact source and candidate matches, zero critical technical transformation issues and two two-source-replicate groups. The engineering suite now passes 23/23 checks; synthetic tests include deliberate missing source, incorrect pKd, qualified Kd and changed-review failures.

NEVER reinterpret numeric source lineage as scientifically approved Kd chemistry, correct physical construct, or permission to train on unapproved BindingDB rows. Source reviews remain 30 UNREVIEWED/0 approved; primary-source and construct verification and a frozen disjoint split are still mandatory. Existing DynaCPI v4 architecture and original checkpoints must be preserved until a defensible scientific plan is approved.

## Private 921-reactant source-evidence worksheet — DO NOT COMMIT (6 November 2026)

`data/audit/source_record_evidence_worklist_30_LOCAL_PRIVATE.csv` exists ONLY on the original authorized Windows machine and contains 921 source reactant IDs and human-review fields. DO NOT upload it to the repo; `.gitignore` explicitly excludes `data/audit/*LOCAL_PRIVATE*.csv`. The generator/validator `scripts/build_record_source_evidence_worklist_v4.py` never overwrites completed reviewer work and exposes only aggregate counts/digests in `research/source_access_v4/record_source_evidence_readiness_30.json`. At creation all 921 rows are UNREVIEWED and zero source tasks approved. Any APPROVE in a synthetic validator is an untrusted *self-reported declaration*, not biological authentication or permission to create approved cohorts/splits. Qualified primary-source reviewers must independently confirm exact physical experimental construct, measured participant, original Kd and source row, qualifier and assay conditions. The science training gate remains BLOCKED.

## New frozen geometry factorial, do not misinterpret original B-vs-D (6 November 2026)

Both original B and D used geometry/sequence mixture w0=0.5. Thus the old near-zero D-B describes only additional differential support correction, NOT all geometry effects. New empirical experiment research/geometry_factorial_dev/factorial.json compares S0/S_B/G_A/G_B/G_D on 3 geometry checkpoints and same 4 DAVIS DEV proteins. Sequence-only calibrated S_B at K5: RMSE 0.857337. Geometry-mixture calibrated G_B 0.860139/0.855587/0.854164 (seeds 1105/1106/1107). G_D-G_B near zero; only 2/4 target improvements each seed and strong sign changes. No superior independent binding affinity performance. Preserve core model/checkpoints and negative findings, avoid re-tuning checkpoint-selected 4 proteins as a new test. Engineering suite 26/26. Scientific cohort gate still blocked (0/30 source-approved tasks).
