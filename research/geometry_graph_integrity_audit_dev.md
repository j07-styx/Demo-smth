# DAVIS engineering geometry graph integrity audit

**Result:** 13/13 mapped graph records passed the implemented structural integrity checks (9 training, 4 validation). No graph integrity failures were detected.

Checks: SHA-256 of graph files against the frozen manifest; source sequence lengths; pilot split consistency; nonempty, unique and in-range residue indices; node scalar/vector feature counts; edge index bounds; edge scalar/vector feature counts; manifest node and edge counts.

Residue coverage across selected graphs: minimum 
1
, maximum 
1
.

**Critical limitation:** The graph audit does **not** establish that the AlphaFold reference is the exact assayed protein construct. It does not independently verify sequence source provenance, structural biological relevance, ligand binding sites, or protein-family-disjoint train/validation splits. These records remain **ENGINEERING_ONLY**, and no additional data is approved for training.

Reproduce: `python scripts/audit_geometry_mapping_dev.py`. Detailed local audit output: `research/geometry_graph_integrity_audit_dev.json`.

Next gate before scientific evaluation: independent experimental construct verification and an approved, protein-family-disjoint holdout.
