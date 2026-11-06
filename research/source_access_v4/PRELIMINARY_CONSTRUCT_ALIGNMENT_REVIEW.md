# Preliminary primary-source construct-alignment review flags — 6 November 2026

**Status: REQUIRES_SOURCE_ADJUDICATION. Not an approved BindingDB assay.**

This note compares two experimental-methods sections of open-access research papers with the canonical UniProt sequences recorded in the previously fixed thirty-task BindingDB review queue and sequence reference screen. It does **not** reproduce article bodies, verify individual affinity values, or modify the scientific review CSV.

| Candidate task prefix | Reference accession and length | Experimental region reported in original methods | Nominal region coverage | Source location |
| --- | --- | --- | --- | --- |
| 69f76b68cfe450d | P17342 / 541 residues | NPR-C residues 27–541, tagged construct | 515 of 541 residues | PMID 35333039, PMCID PMC9014859, Section sec4.4 |
| 83775558aead899 | O14786 / 923 residues | NRP1-b1 residues 273–427, tagged construct | 155 of 923 residues | PMID 29648813, PMCID PMC5957473, Sections sec4.2.1 and sec4.2.3 |

The first publication's methods identify an NPR-C fragment and SPR equilibrium binding endpoint. The BindingDB annotation also mentions receptor residues 27–541, but the record's candidate protein sequence is an exact *full-length UniProt reference* (541 residues). The tagged physical construct cannot be established merely from the supplied reference string.

The second publication's experimental-methods section identifies an NRP1-b1 fragment (residues 273–427) and a tagged protein. Its binding-methods section describes SPR on that fragment. The paper narrative also uses b1b2 terminology elsewhere; a reviewer must determine the construct used for each candidate record. The BindingDB task's candidate input sequence is an exact full-length UniProt reference (923 residues), not the 155-residue segment.

**Critical distinction:** These are source-supported *region and reference-input differences*, not proof that BindingDB's individual recorded Kd measurements are incorrect. Even the nominal region does not fully determine the physical assayed amino-acid sequence, tags, processing, mutations, or protein complex. All compound-to-source-table associations and Kd qualifiers are still **UNVERIFIED**.

### Mandatory next review actions

1. Verify which original paper table, figure or supplementary record corresponds to each BindingDB candidate measurement without using candidate reference metadata alone.
2. Confirm actual physical protein constructs, boundaries and tags. Treat full-length AlphaFold graphs as potentially incorrect until residue-local mapping is confirmed.
3. Verify exact Kd endpoint, unit conversion, qualifiers and assay compatibility. Keep competing binding and inhibition measurements distinct.
4. Record qualified reviewer decisions and source locators in the protected human review process; do **not** automatically approve either task based on this note.
5. Do not change source-approved cohort and protein-family split gates until the required independent scientific review is complete.

Reference evidence artifacts: data/audit/bindingdb_assay_review_30_uniprot_construct_screen.json, data/audit/bindingdb_assay_manual_review_queue_30_ENRICHED.csv, research/source_access_v4/source_access_index.json. Human review remains **30 UNREVIEWED / 0 APPROVED**.
