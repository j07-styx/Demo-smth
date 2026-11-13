# Full-residue feature repair — 2026-11-13 (v5.16)

Label-free engineering work. The existing 96-position cache retains 28,604 of 157,568 residue positions across 298 proteins (18.1534%). Median per-protein retention is 23.3293%; 180 proteins retain less than one quarter. Maximum sequence length is 2,671 and sampled indices can be 29 residues apart.

This measures direct token retention, NOT lost information or binding-pocket coverage. The sampled embeddings contain sequence context. These numbers alone do not establish the cause of poor affinity generalization.

Implemented scripts/cache_full_residues_dev.py to preserve all residue embeddings in ragged arrays with offsets. It uses exactly the existing pinned ESM2 and SaProt encoders and real/shuffled token inputs, so matching sampled positions can be checked numerically. Three arms: saprot_real, saprot_shuffled, esm2_sequence. Model hashes, sequence ordering, finite values, existing global means and sampled-token agreement are checked. Affinity labels are not used.

The independent validator requires all three arms, exact full sequence lengths, hashes and reproduction of sampled tokens. It must pass before the cache is used for training. Full cache generation has been launched; completion and validation are recorded separately when available. Raw embeddings remain gitignored under research_local/full_residues_20261113.

Limitations: encoder windows remain 510 residues without cross-window context. All sequence positions does not mean all positions have reliable structural information. This does not verify assay constructs or locate binding pockets. Dense atom-residue tensors should be processed in chunks before long-sequence training; silently truncating them would undo this repair.

No new affinity fits launched. The next controlled comparison should change residue coverage only, keeping compounds, training budget, seeds and feature encoders fixed. Pretrained chemical features remain a separate planned change, not an implemented component.
