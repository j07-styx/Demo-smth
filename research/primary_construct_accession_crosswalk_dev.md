# DAVIS primary accession-to-AlphaFold provenance crosswalk

The primary DAVIS supplementary table identifies **16 selected protein rows** by NCBI protein accessions. The existing structural manifest contains **13 mapped AlphaFold v6 UniProt models**; the three selected proteins without mapped structures are **IRAK3, RIOK2, and SRPK3**.

The new read-only audit (`scripts/audit_primary_construct_accessions_dev.py`) joins all 13 mapped proteins by their selected source protein names, preserving each NCBI protein accession, UniProt model accession, reference residue range, sequence length and structural coverage. It explicitly marks every experimental construct as **unverified**.

A primary NCBI accession and an AlphaFold UniProt accession belong to different identifier systems. A successful gene-name join, an exact sequence substring, and a structurally intact graph do **not** establish that the assay reagent had the same domain boundaries, sequence variant, mutations, or post-translational state. Before a scientific independent evaluation, resolve accession-to-isoform mappings and assay construct bounds from primary or reagent documentation, and freeze the reviewed provenance table.

Reproduce: `python scripts/audit_primary_construct_accessions_dev.py` and `python tests_v4/primary_construct_accession_audit_test.py`. No source files, graph data, or checkpoints are modified.
