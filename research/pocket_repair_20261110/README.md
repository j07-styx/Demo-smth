# Pocket interaction repair — 10 November 2026

**Status: implemented and engineering-tested; no biological accuracy improvement demonstrated.**
This is an opt-in experimental architecture on the v5-redesign branch, not a replacement for v4 inference or its checkpoints.

## Completed descriptor experiment
The earlier corrected descriptor probe finished all 5 outer protein-group folds and 2 repeats. It evaluated 5,808 covered TRAIN rows in 253 groups; repeated rows are not independent replicates. The reserved test and the optional inner-dev scoring stage were not scored.

| Arm | Pooled RMSE | Group-macro RMSE |
|---|---:|---:|
| Sequence/chemistry ridge, covered training cohort | 1.487624 | 1.362952 |
| + structural descriptors | 1.506438 | 1.353270 |
| + compound-by-structure descriptor products | 1.487919 | 1.366733 |
| Baseline trained on all eligible training rows | 1.452235 | 1.330204 |

Structure vs baseline group-macro delta -0.009682, 95% group-bootstrap CI [-0.0354, 0.0151]. No reliable structural advantage. Pooled error worsens by 0.018814. The full aggregate report is probe_results_cv_audit_full.json. This is development engineering evidence on the BALM reference split, not a source-approved exact-Kd study and not the current DAVIS v6 benchmark. Baseline here is the ridge component, not the locked ensemble.

The underlying audited implementation is preserved in the original workspace:
C:\Users\J0124\dynacpi_v4\scripts\run_balm_structure_probe_audited_dev.py
and research/structure_audit_20261110/source_snapshot.
Those scripts have dependencies on that newer workspace; this checkout does not pretend to reproduce them merely by copying the JSON.

## Implemented neural experiment
dynacpi/pocket_interaction_dev.py contains PocketInteractionRepair:
1. Direct molecular feature projection preserves a compound path to both prediction heads.
2. Trainable residue projection and whole-sequence mean supply the sequence fallback.
3. Explicit label-independent, residue-aligned pocket masks restrict quadratic geometry operations to the pocket.
4. Distance radial-basis features and residue messages encode geometry; no raw Cartesian axes enter the predictor.
5. Compound-conditioned attention pools pocket tokens.
6. The residual head receives compound, pocket, their elementwise product and absolute difference.
7. Small nonzero initialization permits immediate upstream gradient flow. Fusion and readout train together.
8. Missing, empty, single-residue or incomplete-coordinate pockets return the exact current sequence prediction.

This is a compact invariant distance-message model, not a new GVP implementation, docking system or demonstrated binding-pose model. It does not infer a pocket automatically. Relative domain orientation/pose uncertainty is not resolved. All-residue masks must not be represented as independently validated pockets. The synthetic fixture uses arbitrary masks solely to test software.

Four arms share initialization, optimizer, batch order, final-epoch budget, labels and row splits:
- base: sequence/compound predictor;
- pocket_sequence: same pocket and neural modules, constant geometric inputs;
- real_geometry: mapped coordinates;
- shuffled_geometry: a fixed per-protein coordinate permutation, breaking residue-coordinate correspondence.

All arms allocate the same parameters. The base disables the residual and the constant-input control has reduced effective geometric expressivity, so equal allocated parameter counts do not establish perfectly equal effective capacity. Shuffling retains the point cloud and is a partial corruption; the explicit sequence control remains necessary. Rigid transforms and consistent graph relabelings are invariance checks, not negative geometry controls.

## Run engineering tests
From C:\Users\J0124\Demo-smth:
~~~powershell
$env:PYTHONPATH=$PWD.Path
$env:PYTHONDONTWRITEBYTECODE='1'
$python='C:\Users\J0124\dynacpi_v4\.venv\Scripts\python.exe'
& $python tests_v4\pocket_interaction_repair_test.py
& $python tests_v4\pocket_repair_training_test.py
~~~

Tests cover rigid-transform/relabeling invariance, corrupted correspondence, chemical sensitivity, first-step gradients, fallback, padding/batch parity, invalid mappings, synthetic fitting, train/dev group isolation, checksum changes, reserved-role rejection, and all four training/checkpoint prediction round trips. They do not measure real affinity generalization.

## Training input contract
scripts/train_pocket_repair_dev.py is a portable, opt-in engineering runner. It accepts a non-pickle NPZ with exactly:
- compound: float [N,F], for example chirality-aware Morgan fingerprints;
- residues: float [P,L,D], correctly ordered protein residue embeddings;
- valid: boolean [P,L], true only for real residues;
- coords: float [P,L,3], CA positions in the SAME residue order;
- pocket: boolean [P,L], a subset of valid;
- protein_index: integer [N], mapping each pair to a protein;
- label: finite float [N], one consistent endpoint/scale;
- role: Unicode [N], only train or dev;
- group: Unicode [P], predeclared protein-family/group identity.

The accompanying JSON must contain evidence_status=ENGINEERING_ONLY, npz_sha256, pocket_source (mapping/selection provenance), and pocket_selection_uses_labels=false. These declarations/checks are technical safeguards, not independent biological approval. Do not use this engineering entrypoint to bypass the repository's scientific cohort gate. No reserved-test arrays are accepted; overlapping training/dev groups are rejected. Label normalization uses training rows only.

~~~powershell
& $python scripts\train_pocket_repair_dev.py --bundle PATH_TO_FEATURES.npz --manifest PATH_TO_MANIFEST.json --out LOCAL_OUTPUT_DIRECTORY --epochs 5 --seeds 2931 2932 2933
~~~

The output directory must not already exist. The runner saves fixed-final-epoch checkpoints, training label scale, per-arm parameter counts, dev predictions and pooled/group-macro RMSE. It does not select checkpoints on dev and does not push weights. The actual mapped pocket feature bundle has not yet been prepared; no new real-affinity neural training run is claimed by this commit.

Before real-data fitting, supply a label-independent pocket source and mapping (e.g. curated kinase-pocket positions), document structure coverage and construct limitations, and compare all arms on identical groups. Continue retaining examples with unavailable structures in the sequence path. Check within-protein ligand ranking as well as RMSE; attention weights alone are not evidence of physical contacts.

## Scope
The original v4 model, adapter, frontend/API, checkpoints, scientific gate and other working directories are unchanged. The older current checkout and newer origin/dynacpi-v4 have divergent histories; this work is published on v5-redesign without replacing either main or dynacpi-v4.
