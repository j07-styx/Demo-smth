# Structural token interaction trial — 11 November 2026

Status: completed engineering experiment, negative for a reliable geometry advantage.
24 neural fits completed: 4 arms x 3 seeds x 2 correction policies. No production model replaced.

## What changed
The new StructuralTokenFusion module replaces a single compound query with individual atom tokens and bidirectional atom-to-residue / residue-to-atom attention. Both updates preserve their input representations via residual connections. A direct Morgan fingerprint pathway reaches the joint prediction head. Protein tokens combine amino-acid identity, confidence/position, and invariant local structural environment descriptors. Heads and fusion train together.

This borrows the interaction-level design motivation of GenSPARC, NOT its implementation or pretrained representations. GenSPARC uses SaProt structure-aware pretraining and SPMM/GCN compound representations. This experiment uses neither those weights nor Foldseek structural tokens, experimental contact labels, docked poses or curated pocket annotations. Atom tokens are simple RDKit features; full fingerprints retain molecular topology. It is not an equivariant atomic GNN or GenSPARC reproduction.
Primary paper: https://www.nature.com/articles/s42004-025-01844-0

## Data and fixed experiment
- All label-bearing data originate in the existing BALM frozen TRAIN partition.
- 5,808 pairs, 298 structure-covered proteins, 253 approximate protein groups, 3,405 compounds.
- Fixed internal split seed 4110: 4,982 fit rows; 826 evaluation rows in 50 groups.
- Neither official inner-dev nor reserved-test affinity labels were materialized or scored.
- Existing loader reconstructs frozen roles using public sequence metadata across the source table.
- AF reference-to-residue mappings verified exactly at retained indices, stored-byte SHA256 checked, gzip PDBs decoded.
- pLDDT >=70 residues only; up to 96 uniformly spaced retained residues. Local descriptors are computed using the full retained mapped set before sampling.
- 12 distance-RBF means, 21 contact-neighbour amino-acid composition features, and 2 contact-density features per residue.
- Maximum 96 atoms per molecule; 195 molecules are truncated for atom attention, while fingerprints still cover the full molecule.
- Sequence/confidence arm gets identical selected residues, pLDDT and normalized sequence positions.
- Assayed constructs and labels are not independently source-adjudicated here. This is public-reference development engineering, not the approved exact-Kd scientific study.

## Strong baseline and training
A ridge on normalized Morgan fingerprints plus train-fitted char 3–4mer protein TF-IDF (weight 0.25) is the anchor. Training residual targets use 3-fold group-cross-fitted ridge predictions; held-out groups do not contribute labels to fitting. Geometry normalization uses distinct fit proteins only.

The residual neural predictor is trained for 5 fixed epochs, at most 64 batches of 32 per epoch, AdamW lr 3e-4, weight decay .01, clip norm 1, width 32. Seeds 4111/4112/4113 and identical pair order/initialization are shared across arms. This is a bounded compute trial, not training to convergence. No epoch is selected on evaluation results. CPU threads=2; existing GPU KIBA work was not stopped or changed.

Arms:
1. sequence: no structural descriptors;
2. real: residue-matched local descriptors;
3. mean: the per-protein mean descriptor repeated at every residue;
4. shuffled: the same local descriptors permuted within each protein.

The shuffle preserves structural marginals and is a partial correspondence corruption, not total removal of structural information. The mean control distinguishes localized correspondence from a global summary.

## Results
Numbers below are arithmetic means of per-seed metrics, NOT ensemble predictions.

| Policy / arm | Mean pooled RMSE | Mean group-macro RMSE |
|---|---:|---:|
| Ridge anchor | 1.489130 | 1.269206 |
| Uncapped sequence residual | 1.719486 | 1.414723 |
| Uncapped real structure | 1.708872 | 1.396593 |
| Uncapped mean structure | 1.735625 | 1.407944 |
| Uncapped shuffled structure | 1.707268 | 1.398250 |
| Capped sequence residual | 1.536322 | 1.287137 |
| Capped real structure | 1.535797 | 1.276776 |
| Capped mean structure | 1.539183 | 1.270515 |
| Capped shuffled structure | 1.535785 | 1.276459 |

Uncapped head outputs use a 0.25 multiplier in standardized label units. That multiplier does NOT bound corrections; learned outputs compensated for it. After inspecting early uncapped outcomes, a single exploratory follow-up was fixed: tanh-bounded corrections of at most +/-0.25 RAW target units. This second experiment reuses the internal evaluation split; it is not an independent confirmation or an original preregistered result. Both complete runs are retained.

Group-paired bootstrap averages seed SSE per group before taking the square root; it resamples the 50 groups, not seeds as independent samples. Thus its point estimate can differ slightly from the arithmetic per-seed means above.
- Uncapped real-minus-sequence macro delta -0.01853, CI [-0.07055, +0.03588].
- Uncapped real-minus-shuffled -0.00112, CI [-0.00616, +0.00365].
- Capped real-minus-sequence -0.01038, CI [-0.02621, +0.00583].
- Capped real-minus-shuffled +0.00029, CI [-0.00049, +0.00110].
- Capped real-minus-mean +0.00627, CI [+0.00031, +0.01300], favouring the simpler global summary in this exploratory contrast.

No reliable residue-level structural advantage. Capping reduces deterioration versus the uncapped network, but the ridge anchor still wins. These unadjusted exploratory intervals are not a multiplicity-controlled scientific claim.

## Mechanism checks
Read-only interventions use a 16-protein x 16-compound cross-product from held-out INPUTS, with no affinity labels. Removing geometry within a geometry-trained model is an out-of-distribution intervention and must not be interpreted as an accuracy ablation.
- Uncapped compound embeddings: mean cosine 0.131–0.206; centered effective rank 15.1–16.2. The historical chemical collapse is absent in these representations.
- After subtracting additive protein and compound effects from the geometry-removal response, the interaction component accounts for only 0.16–0.43% of its squared magnitude.
- Under the capped policy the analogous fraction rises to 19.7–43.8%, but tanh itself can induce statistical nonadditivity. The failure to outperform shuffled geometry shows why nonadditivity is not proof of physical interaction learning.
- Sensitivity units in mechanism JSON are head-response units (uncapped) or normalized tanh response (capped), NOT pKd.

## Interpretation and next discriminating experiment
The new pathway is trainable, chemically discriminative and structurally responsive. These properties alone do not make its structural correspondence useful. Learned corrections overfit or transfer poorly, and changing correspondence barely affects predictive accuracy. More gain or another attention block is not supported as the next fix.

A more faithful GenSPARC-inspired follow-up should isolate pretrained structure-aware protein representations from token fusion: compare a pretrained sequence encoder against SaProt on identical protein rows and compound features, with matching structure-token corruption and compute/selection budgets. This experiment did not test pretraining, so its failure cannot rule it out. A curated pocket/construct cohort is another distinct hypothesis; current uniform residue sampling can dilute small binding regions.

## Reproduction
On the authorized PC, run from C:\Users\J0124\Demo-smth using the existing dynacpi_v4 Python environment:
~~~powershell
$py='C:\Users\J0124\dynacpi_v4\.venv\Scripts\python.exe'
& $py tests_v4\structural_token_fusion_test.py
& $py scripts\build_structural_token_bundle_dev.py --source-workspace C:\Users\J0124\dynacpi_v4 --out NEW_FEATURE_DIRECTORY
& $py scripts\run_structural_token_trial_dev.py --bundle-dir NEW_FEATURE_DIRECTORY --out NEW_UNCAPPED_DIRECTORY
& $py scripts\run_structural_token_trial_dev.py --bundle-dir NEW_FEATURE_DIRECTORY --out NEW_CAPPED_DIRECTORY --correction-cap 0.25
& $py scripts\diagnose_structural_tokens_dev.py --bundle-dir NEW_FEATURE_DIRECTORY --trial NEW_CAPPED_DIRECTORY
~~~

Output directories must be new. Six engineering tests passed: geometry-control independence, correspondence-sensitive real branch, invariant mean control, first-step gradients to chemistry/geometry, consistent token relabeling, rigid-transform descriptor invariance, and empty-token rejection (some tests cover multiple assertions).

Local artifacts:
- data/structural_token_trial_20261111 in dynacpi_v4: NPZ inputs and manifest.
- research/structural_token_trial_20261111 and research/structural_token_capped_20261111 in dynacpi_v4: checkpoints, split arrays, predictions and full result JSONs.
Checkpoints are neural residual heads, not standalone deployed affinity models; reproduction also requires the documented ridge fit and normalization. No frontend model registry was changed.

Only code, aggregate results, protocol, hashes and documentation are published. Labels, arrays and weights remain local.
