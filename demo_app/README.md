# DynaCPI Research Workbench — 9 November 2026

A one-page local showcase with live cheminformatics and **real frozen model inference** against four cached DAVIS development proteins. Created separately from training code so the original research data, checkpoints and other sessions stay unchanged.

## Open it

On the authorized Windows computer, double-click **launch_demo.bat** inside demo_app. The browser will open **http://127.0.0.1:8765**. Alternatively from C:\Users\J0124\dynacpi_v4 in PowerShell:

    .\.venv\Scripts\python.exe demo_app\server.py

The demo uses the existing Python environment (Flask, RDKit, PyTorch, CUDA) and checkpoint/caches; it cannot run from this folder alone on another computer without restoring the project's excluded ESM feature cache, mapped geometry graphs and saved checkpoint weights. The Flask server listens only on 127.0.0.1; it is not a production public deployment.

## Features demonstrated

1. Enter any valid molecular SMILES (<= 450 characters / <= 250 heavy+hydrogen atoms). The browser requests real RDKit canonicalization, 2D molecular SVG, formula, weight, LogP, polar surface area, HBD/HBA. Invalid SMILES are rejected.
2. Select FRK / MEK5 / ADCK4 / OSR1. Press **DAVIS example (selected target)** to load a real development compound without its experimental label.
3. Select K=0, 1, 2, 5, 10 or 20 same-target DAVIS observations. Press **Run frozen model**. This executes the existing sequence checkpoint plus geometry seed 1107 against cached ESM residue features and a mapped backbone graph, then runs the existing chemical-similarity few-shot adapter. No model parameters are fit, changed or written.
4. In Benchmarks, switch among seeds 1105, 1106, 1107 and inspect actual fixed K sweeps from research/geometry_factorial_dev/factorial.json. Different initialization seeds have inconsistent effects.
5. K=5 sequence+calibration RMSE 0.857337 vs geometry+calibration 0.860139 / 0.855587 / 0.854164 for the three seeds. The differential support adapter's incremental effect was practically zero.

## Science and interpretation

**DEV ONLY.** Four checkpoint-selected DAVIS validation proteins; 10 query compounds per target and 10 correlated support draws per target. Neither this UI nor the saved factorial experiment is an independent or prospective biological evaluation. Do not claim PerceiverCPI superiority or validated physical Kd values. On arbitrary new SMILES the inference is likely out-of-distribution. The remaining BindingDB source/assay approval and protein/publication-family disjoint evaluation gates are blocked.

The UI selects support observations using deterministic hashes from the original DAVIS development pool, always excludes a query with exactly matching canonical compound ID, and never exposes any selected query ground-truth pKd through the API. The interactive support selection is a demo protocol, not identical to the historical factorial benchmark's ten nested support draws. The fixed historical benchmark values are displayed directly, never relabeled as a new experiment.

The model's upstream graph implementation uses CUDA. The server uses the existing shared .gpu.lock only while loading/inferencing. It returns a busy error after 15 seconds if another GPU job has the lock. It does not interrupt research training.

## Run smoke tests

With the local server running:

    .\.venv\Scripts\python.exe -u demo_app\smoke_test.py

The smoke test covers health, 18 stored benchmark rows, real RDKit formula/SVG, invalid SMILES rejection, real K0 frozen-model output, and K5 adapter output. A passing suite is engineering evidence, not model-quality evidence.

## Short demo script

- Open the one-page UI; use the DAVIS example input for ADCK4.
- Click **Analyze molecule** to show RDKit draws/descriptors from live SMILES.
- Click **Run frozen model** to show three numerical stages (sequence, geometry and calibrated output). Values are predictions, *not experimental affinities*.
- Scroll to Benchmarks; switch 1105/1106/1107 and explain that geometry helps on two seeds and hurts one on the four-protein development cohort. Highlight that the differential adapter is not yet beneficial.
- Finish by stating the next research milestone: an independently source-approved, leakage-aware protein-family held-out evaluation.

## File map

- server.py — Flask HTTP routes and frozen model integration
- index.html — responsive dashboard and interactive benchmark charts
- smoke_test.py — non-destructive API smoke tests
- launch_demo.bat — Windows browser/server launcher

Source provenance: research/geometry_factorial_dev/factorial.json; research/pilot_sequence/checkpoint.pt; research/pilot_geometry_seed_sweep_dev/seed_1107/best_checkpoint.pt; data/engineering_pilot. This folder contains no original raw affinity database exports or secrets.
