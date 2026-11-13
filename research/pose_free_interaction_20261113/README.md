# Pose-free atom/residue prototype — 2026-11-13 (v5.14)

Status: synthetic engineering gate passed. No real affinity training or biological improvement demonstrated.

## Why this implementation
The prior experiment used one fingerprint vector to reweight protein messages. The older atom cache omits bond connectivity and truncates 195 molecules at 96 atoms. Neither is a complete atom-level molecular graph.

New opt-in modules:
- dynacpi/molecular_graph_dev.py: variable-size RDKit atom features, typed bonds including stereochemistry, and a direct normalized Morgan fingerprint. No silent atom truncation. Dynamic batch padding.
- dynacpi/atom_residue_interaction_dev.py: bond-conditioned atom messages, residue-token projection, explicit atom-residue pair value network and attention, direct chemical/protein/fingerprint paths. Pair information enters message values, not solely attention weights.
- Output is uncapped for a standardized fit-gate task; not connected to production residual inference.

The residue interface can accept structure-aware pretrained features. This module does not itself compute structure, contact distances, docking poses or pretrained SaProt/SPMM representations. Therefore it is a building block toward the pose-free approach, NOT a completed GenSPARC reproduction or a validated 3D model.

## Completed validation
Synthetic model tests passed permutation invariance, padded-input invariance, batch parity, bond sensitivity, empty-input rejection and gradients through atom, residue, bond-message and pair-value modules.

A 4x4 full factorial synthetic task has zero protein and compound marginal label means, so pure main effects cannot fit it. Fixed 400 AdamW steps reduced MSE from 0.3968288 to 0.0000149189. This is in-sample synthetic fitting, not transfer/generalization, physical contact recovery or affinity evidence.

Molecular tests preserve all 110 atoms of a long-chain test molecule, verify aromatic bonds and bond symmetry, normalized fingerprints, padding and empty-input rejection. Dense bond and pair tensors impose quadratic memory costs; large inputs require bucketing/chunking rather than truncation before broad training.

## Assay metadata finding
A schema-only read of the available public BALM Arrow source found exactly Index, Drug_ID, Drug, Target_ID, Target, Y. No assay, publication, endpoint, unit or construct fields are present. No label values were read by this check.

This does not prove mixed assays, but means this file alone cannot establish same-assay pair comparability. Recover source-level metadata before describing a panel as assay-consistent. An exploratory real-data fit diagnostic can still be labeled explicitly unverified; it must not be presented as the planned assay-consistent scientific gate.

## Remaining gates before another sweep
1. Recover complete molecule identities and typed graphs for selected frozen TRAIN rows with row/hash checks. Do not reuse the truncated atom cache.
2. Recover or verify assay/construct comparability for a small training panel. Do not infer it from Target_ID.
3. Use full or explicitly documented residue coverage with pretrained structure-aware tokens, preserving local identities. Existing uniformly sampled 96-token caches do not solve pocket coverage.
4. Run a bounded real-data training-fit diagnostic with train-only scaling and held-group comparison. Distinguish fit failure from transfer failure.
5. Only then run matched sequence/real-structure/corrupted-structure comparisons with predefined budget and criteria.

Reserved-test affinities remain unscored; other repositories and original v4 models remain unchanged.
