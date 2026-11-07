# BindingDB DAVIS source-cell reconciliation

Mechanical evidence only; all review decisions remain UNREVIEWED.

The three queued DAVIS assays contain 63 source records. Exact canonical isomeric SMILES linked through the local CID reference and cached PubChem synonyms maps 23 records to named columns in Supplementary Table 4 of DOI 10.1038/nbt.1990. All 23 have exactly matching numeric Kd values in nM; none of these mapped values disagreed.

| Target | Exact structure mapping and numeric match | Unresolved mapping |
|---|---:|---:|
| RIOK2 | 9 | 11 |
| IRAK3 | 9 | 15 |
| SRPK3 | 5 | 14 |

A separate connectivity-only diagnostic found that 18 of the 40 unresolved records match a legacy reference only after stereochemical information is removed. The remaining 22 have no connectivity match in that reference. These are mapping gaps, not proof of incorrect BindingDB structures. No stereochemistry was discarded for acceptance, and no match was inferred from affinity values. Resolving those records requires an independent chemical identity source.

The dated JSON report records the publisher workbook and synonym-cache hashes. The detailed per-record evidence remains local in data/audit/davis_primary_20261107/bindingdb_source_cells_LOCAL_PRIVATE.json. The original review queue and reviewer-owned worksheet were hashed before and after execution and were unchanged.

Numeric agreement does not verify the physical construct or assay conditions. None of the three tasks yet has 15 exact-mapped records under this conservative procedure, and no new training cohort or test split was created. The immediate next work is independent compound identity resolution, followed by physical construct and source-method review.

Validation: tests_v4/bindingdb_davis_source_cells_test.py passed blank-cell, inequality, nonfinite-number, stereochemistry-preservation and 63-record consistency checks. Reconciliation refuses to overwrite existing evidence.
