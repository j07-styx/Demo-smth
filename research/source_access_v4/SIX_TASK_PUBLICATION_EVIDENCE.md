# Six candidate binding-assay tasks: publication-source verification (6 November 2026)

**Source-level public research only. Not an independent per-record Kd audit; zero of 30 tasks scientifically approved.**

The fixed research review queue contains 147 original source rows across the six inspected tasks. No chemical structures or numeric affinities were used.

| Candidate source | Original records | Source-evidence decision |
| --- | ---: | --- |
| Annexin A3 | 48 | PROMISING_SPR_SOURCE_RECORD_TABLE_MAPPING_PENDING |
| Serine/threonine-protein kinase RIO2 | 20 | PUBLISHED_KD_ASSAY_METHOD_LOCATED_DOMAIN_CONSTRUCT_UNVERIFIED |
| SRSF protein kinase 3 | 19 | PUBLISHED_KD_ASSAY_METHOD_LOCATED_DOMAIN_CONSTRUCT_UNVERIFIED |
| Interleukin-1 receptor-associated kinase 3 | 24 | PUBLISHED_KD_ASSAY_METHOD_LOCATED_DOMAIN_CONSTRUCT_UNVERIFIED |
| Phosphoglycerate kinase | 18 | BINDING_NMR_SOURCE_FOUND_NUMERIC_METHODS_UNVERIFIED |
| PA-I galactophilic lectin | 18 | ORIGINAL_PER_RECORD_SOURCE_NOT_IDENTIFIED_REVIEW_CITATION_RED_FLAG |

## Specific source-level findings

### Annexin A3

- Original source: https://pubs.acs.org/doi/10.1021/acs.jmedchem.4c02403
- Additional registry/context: https://pubchem.ncbi.nlm.nih.gov/bioassay/2234142/
- Local assay key: 50023141_1
- Original candidate records: 48

Original article studies ANXA3 binding and lists supporting SPR data. Independently indexed PubChem assay describes a human recombinant ANXA3 C-terminal 6xHis-tagged SPR dissociation-constant experiment and 48 results, matching the fixed local 48-record assay count.

**Still unresolved:** Original paper/SI numeric rows and individual experimental construct, charge state, assay conditions, source-row correspondence and qualifiers still need independent verification.

**Approved for scientific model fitting:** NO.

### Serine/threonine-protein kinase RIO2

- Original source: https://www.nature.com/articles/nbt.1990
- Additional registry/context: https://pubmed.ncbi.nlm.nih.gov/22037378/
- Local assay key: 50034019_161
- Original candidate records: 20

Original 2011 kinase interaction paper has supplementary Table 4 reporting binding Kd in nM across 72 molecules and 442 kinase assays. Local record is annotated RIOK2 kinase domain, not necessarily full-length protein.

**Still unresolved:** Match each of 20 raw records to the original supplementary table and exact kinase domain, sequence and assay protocol; determine source qualifiers.

**Approved for scientific model fitting:** NO.

### SRSF protein kinase 3

- Original source: https://www.nature.com/articles/nbt.1990
- Additional registry/context: https://pubmed.ncbi.nlm.nih.gov/22037378/
- Local assay key: 50034019_51
- Original candidate records: 19

Same original Davis 2011 binding-Kd supplementary table. Local records refer specifically to SRPK3 kinase domain.

**Still unresolved:** Verify original supplementary numeric row mapping, real recombinant kinase-domain sequence, truncations and assay equivalence for all 19 entries.

**Approved for scientific model fitting:** NO.

### Interleukin-1 receptor-associated kinase 3

- Original source: https://www.nature.com/articles/nbt.1990
- Additional registry/context: https://pubmed.ncbi.nlm.nih.gov/22037378/
- Local assay key: 50034019_522
- Original candidate records: 24

Same original Davis 2011 supplementary Kd table, but local rows describe IRAK3 kinase domain rather than a source-verified complete protein.

**Still unresolved:** Reconcile 24 raw records against published values and physical kinase-domain construct before scientific inclusion.

**Approved for scientific model fitting:** NO.

### Phosphoglycerate kinase

- Original source: https://pubmed.ncbi.nlm.nih.gov/9804684/
- Additional registry/context: https://pubs.acs.org/doi/10.1021/jm970839y
- Local assay key: 50036674_1
- Original candidate records: 18

1998 original study describes ligand binding to phosphoglycerate kinase and NMR-based binding analysis; local assay reports Kd varying across pH 3-11, requiring condition-specific mapping.

**Still unresolved:** Independent original full paper table/method review is needed to determine whether 18 numerical Kd values are measured, derived, pH-comparable and construct-aligned.

**Approved for scientific model fitting:** NO.

### PA-I galactophilic lectin

- Original source: https://pubmed.ncbi.nlm.nih.gov/26804741/
- Additional registry/context: https://pubmed.ncbi.nlm.nih.gov/27488655/
- Local assay key: 50018971_9
- Original candidate records: 18

The exact PMID cited in the local raw review metadata (26804741) resolves to a 2016 review article about Pseudomonas infection treatment strategies, NOT an original 18-record LecA Kd study. A different 2016 LecA competitive binding paper is PMID 27488655 and discusses IC50; it cannot be silently substituted as the original Kd source.

**Still unresolved:** Locate actual original experimental citation for assay 50018971_9 and verify direct Kd rather than potency or comparative IC50. Do not mark the existing task approved or replace its original PMID silently.

**Approved for scientific model fitting:** NO.

## Explicit priority decision

Start with ANXA3 SPR source methods and individual measurement/table-to-row matching because it has a coherent 48-entry public assay registry and original 2025 SPR supporting data, but do not claim record-level approval from a match in counts.

Next map kinase-domain assays to the Davis et al. 2011 supplementary binding-Kd table and the real physical kinase domain sequences. Distinguish domain constructs from full-length UniProt references.

The LecA/PA-I task source PMID 26804741 is a review, not primary experimental data. This is an explicit citation-provenance anomaly and the direct assay source needs discovery; the separate competitive LecA PMID 27488655 must NOT be conflated with the cited review.

No assay source review or data approval was modified; no model weights were retrained, scientific cohort released, or independent protein-group split frozen.

All findings are metadata/publication-level and are not scientific validation of an independent model-performance result.
