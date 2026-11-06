# Reproducibility and data rehydration — Windows / NVIDIA GPU

**Status:** Snapshot from 5 November 2026. This Git checkout is intentionally not fully self-contained. Do not describe a test as passed without actually running it in the current environment.

## 1. Environment and source provenance

Original machine: Windows/PowerShell, RTX 4060 Laptop GPU. ESM-2 650M extraction required compatible NVIDIA CUDA PyTorch. The original isolated code project was C:\Users\J0124\dynacpi_v4; handoff checkout is C:\Users\J0124\Demo-smth. The external old PerceiverCPI reproduction resides under C:\Users\J0124\OneDrive\Desktop\perceiver_cpi.

The historical environment used Python 3.9.13 initially and a local project virtual environment; do not assume a new machine's package versions. See environment.yml and source imports for dependencies such as torch, rdkit, numpy, scipy, pandas, BioPython, tape-proteins, fair-esm, and the included upstream PerceiverCPI code. Verify installed versions and GPU/CUDA compatibility before making package changes.

### Minimal inspection and setup

~~~powershell
git clone https://github.com/j07-styx/Demo-smth.git
cd Demo-smth
git log -4 --oneline
git status --short
Get-Content .\AGENTS.md
Get-Content .\HANDOFF_FOR_NEXT_AI.md
py -3.9 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
# Install compatible torch/CUDA and other dependencies according to environment.yml,
# plus scripts' exact imports. Do not assume environment.yml is a complete Windows lockfile.
~~~

Avoid changing the baseline source to make arbitrary test failures disappear. Test on copies, with patches recorded separately. Verify any licensed pretrained assets before redownloading.

## 2. Snapshot integrity

Inspect provenance/snapshot_file_manifest.json. It contains an inclusion list with SHA-256 for all copied original files and an exclusion list with reasons. Do not compare newly added documentation files against that original snapshot manifest (they were authored for this GitHub export); Git provides their history.

~~~powershell
.\.venv\Scripts\python.exe -c "import json,hashlib,pathlib; m=json.load(open('provenance/snapshot_file_manifest.json',encoding='utf-8')); bad=[]; [(bad.append(x['path']) if not pathlib.Path(x['path']).is_file() or hashlib.sha256(pathlib.Path(x['path']).read_bytes()).hexdigest()!=x['sha256'] else None) for x in m['files']]; print('Snapshot files checked:',len(m['files']),'mismatches:',bad[:20]); assert not bad"
~~~

Note: Git checkout may normalize newline endings depending on core.autocrlf; use a binary checkout or compare source files before format conversion if the manifest reports mismatches. This provenance check is an additional guard and not a replacement for Git SHA.

## 3. Important excluded assets

- Full BindingDB_All_202611_tsv.zip original archive: ~594 MB compressed / ~9 GB source TSV. Original source can be fetched through scripts/resume_bindingdb_full.py, with source hash/ZIP-CRC verification. The server's companion MD5 endpoint returned HTTP 404 at original download. Never silently mark archive as publisher-MD5-verified.
- BindingDB intermediate whole-source provenance and raw joined candidate JSONL files: omitted for size; regeneration scripts are in scripts/audit_* and scripts/materialize_*.
- ESM-2 650M pretrained official model weights and **462 cached residue embedding .pt files**, ~848 MiB total: intentionally excluded from Git. Restore from a trusted original machine or run scripts/fetch_esm.py then scripts/extract_esm.py after validating stage sequence dictionary and settings. Confirm 462/462 with scripts/audit_esm_cache.py.
- Archived original PerceiverCPI fold-zero checkpoint and source training environment: not included; legacy_checkpoint_parity.py refers to the preserved external workspace on the original PC. This test requires trusted original artifacts.
- Local machine's virtual environment, credentials, Docker caches and other generated state are intentionally excluded.
- Selected small engineering checkpoints ARE included: research/pilot_sequence/checkpoint.pt; research/pilot_perceiver/checkpoint.pt; research/pilot_geometry_9train_4val/best_checkpoint.pt. A checkpoint can be loaded safely only from a trusted verified copy; pickle-based torch deserialization is unsafe for untrusted files.

## 4. Local cache and model replay

Ensure the restored ESM directory exactly matches data/esm2_t33_650M_layer33_w1000_o128_fp16/settings.json and has a hash-named .pt file for every staged sequence in data/staging/sequences.json. Check shapes [L,1280], finite FP16 values, window coverage and sequence hash identity. Some integration tests require an actual NVIDIA CUDA device and hardcoded original paths; if those paths are unavailable, report a dependency issue and port paths carefully before proceeding.

On the original machine with the preserved source and cache:

~~~powershell
.\.venv\Scripts\python.exe scripts\audit_esm_cache.py
.\.venv\Scripts\python.exe scripts\run_v4_validation_suite.py
~~~

Do not immediately rerun training to "verify" the repo: the suite is separate and non-destructive, whereas training scripts may create or overwrite pilot outputs if used in-place.

## 5. Existing data and experiment gates

The following data/audit JSONL files are reproducible preliminary data, NOT a final experimental benchmark:
- bindingdb_full_kd_candidate_tasks_PRE_SPLIT.jsonl
- bindingdb_full_kd_candidate_episodes_PRE_SPLIT.jsonl
- bindingdb_full_kd_compound_median_candidates.jsonl

No human-reviewed task has been approved. Source reports in data/audit/bindingdb_assay_manual_review_queue_30_ENRICHED.csv are original inputs for manual curation. Never overwrite them after adjudication. Current scientific_cohort_gate.current_status(root) is BLOCKED_UNAPPROVED_NOT_TRAINING_READY.

When a real approved cohort is available, require separate files carrying an approved source-review evidence manifest and frozen protein-group task role assignments with matching hashes, reviewed by a researcher; only then may any scientific script read the main affinity labels.

## 6. Model experiment and verification artifacts

Engineering model histories:
- research/pilot_sequence/history.json: three epochs, checkpoint saved from epoch 3.
- research/pilot_geometry_9train_4val/history.json: two epochs, best geometry from epoch 1.
- research/pilot_geometry_9train_4val/checkpoint_parity.json: independent saved model reproduction.
- research/pilot_geometry_9train_4val/support_adapter_development_diagnostics.json: four-target K=5 A/B/C/D observations.
- data/audit/v4_validation_suite.json: 15 prior engineering tests, with individual logs under research/validation_suite_logs.

Never compare geometry values from the four-target subset with sequence values across the full eight-target development set and claim a fair win or loss. The existing reported geometry comparison already uses the matched four-target cohort.

## 7. GitHub maintenance

The repository is j07-styx/Demo-smth and was created private. The dates and version numbers on Git commits are **upload milestones** (0.1 code, 0.2 research, 0.3 data, 0.4 AI handoff), not four versions of the DynaCPI model. Preserve the research architecture identifier **v4.0**.

Commit meaningful, isolated changes with experiment evidence and exact observations. Never add raw model pretraining files or large source data; record dataset URL, version, hashes and regeneration steps instead. Verify remote HEAD after pushing.

## 6 November 2026: reproducing original BindingDB reactant lineage checks

Authorized Windows workspace: C:\Users\J0124\dynacpi_v4. Uses its existing Python 3.9 virtual environment, does not require conda, and does not train models. The source JSONL assets already exist on the original PC but were excluded from the GitHub snapshot due to size. GitHub clone alone cannot execute the real integration test until all three original source files and the canonical human-review CSV are restored.

PowerShell command on the original PC:
    .\.venv\Scripts\python.exe scripts\audit_30_record_level_provenance_v4.py

Five synthetic regression scenarios:
    .\.venv\Scripts\python.exe tests_v4\record_lineage_synthetic_test.py

Full engineering suite, including real integration and archived baseline parity:
    .\.venv\Scripts\python.exe scripts\run_v4_validation_suite.py

Read-only benchmark/source status:
    .\.venv\Scripts\python.exe scripts\monitor_benchmarks_v4.py

Outputs: research\source_access_v4\record_level_provenance_30.json and RECORD_LEVEL_PROVENANCE_30.md; consolidated suite data\audit\v4_validation_suite.json; latest monitor research\monitoring\latest.json and LATEST.md.

Expected verified counts at original source versions: fixed 30 tasks, 919 compound groups, 921 distinct source reactant IDs, all 921 raw source and unaggregated candidate records found, no critical technical inconsistencies, five synthetic unit cases passed, and 23 total engineering checks passed. The audit hash-checks and records input files. If source files or human review decisions change, reconcile the inputs instead of forcing old expected counts.

This audit cannot approve any source assay or create a scientific training cohort. It does not validate true experimental equilibrium Kd or physical protein construct identity; the scientific cohort gate remains blocked.

## 6 November 2026 — reproducing private source-evidence readiness

On the authorized original Windows PC, from C:\Users\J0124\dynacpi_v4, run:
    .\.venv\Scripts\python.exe scripts\build_record_source_evidence_worklist_v4.py

This command creates `data\audit\source_record_evidence_worklist_30_LOCAL_PRIVATE.csv` **only if it does not exist**, otherwise validates the existing reviewer worklist without overwriting it. Expected initial state: 921 source-reactant records across 30 fixed tasks, ALL UNREVIEWED and no scientifically approved task. Source data JSONL and human review CSV must be present and unchanged.

Run synthetic and real integrity cases:
    .\.venv\Scripts\python.exe tests_v4\record_source_evidence_synthetic_test.py
    .\.venv\Scripts\python.exe tests_v4\record_source_evidence_real_integrity_test.py

Aggregate outputs only (safe for Git): `research\source_access_v4\record_source_evidence_readiness_30.json` and `RECORD_SOURCE_EVIDENCE_READINESS.md`. Never copy the private worksheet or reviewer notes to the repository, and never use self-reported review declarations as final scientific approvals. All model training remains blocked until independent primary-source review, signed source evidence manifest and frozen protein-family split.

## New frozen geometry factorial (6 November 2026)

On authorized Windows C:\Users\J0124\dynacpi_v4 with existing local DAVIS engineering data, ESM embeddings, graph fixtures and three saved geometry checkpoints, run (PowerShell):

    .\.venv\Scripts\python.exe scripts\benchmark_geometry_factorial_dev.py

No model fitting, parameter selection, or source-unapproved BindingDB affinity data is used. Script checks exact sequence checkpoint and geometry graph hashes, identical fixed query/support sets and baseline parity. Outputs research\geometry_factorial_dev\factorial.json and SUMMARY.md with 720 correlated target-draw-K trials; four unique checkpoint-selected DAVIS DEV targets. Original G_A/G_B/G_D values must agree with preexisting K-sweep macro values within 1e-6.

Check integrity without rerunning GPU inference:

    .\.venv\Scripts\python.exe tests_v4\geometry_factorial_dev_integrity_test.py

Full engineering suite:

    .\.venv\Scripts\python.exe scripts\run_v4_validation_suite.py

Verified as 26/26 PASS on 6 November 2026; not scientific model validation. K5 sequence-only calibrated baseline RMSE 0.857337 and geometry-mixture calibrated per seed 0.860139, 0.855587, 0.854164; differential gain approximately zero. The real primary exact-Kd project cannot proceed to blinded family-held-out training before source review and frozen split.

## Publication-level source-evidence crosswalk (6 November 2026)

From the original Windows DynaCPI v4 project run:
    .\.venv\Scripts\python.exe scripts\verify_six_primary_source_leads_v4.py
    .\.venv\Scripts\python.exe tests_v4\six_publication_source_evidence_integrity_test.py

Inputs: immutable fixed canonical human-review queue 30 ENRICHED CSV (only bibliographic/source IDs and counts). Outputs: research/source_access_v4/six_task_publication_evidence.json and SIX_TASK_PUBLICATION_EVIDENCE.md. The crosswalk was checked against exact original source identities and has six tasks/147 records, zero scientific approvals. It contains source metadata/provenance only; no compound structures, raw Reactant_set identifiers or numerical binding affinity values. These are research article citations and external method descriptions, not verified original source measurements.
