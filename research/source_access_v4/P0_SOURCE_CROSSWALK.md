# Four P0 BindingDB source-evidence crosswalk (6 November 2026)

**Source-level leads, not researcher-approved experimental data.** No compound-level affinity values were read. All thirty canonical review decisions are unchanged and UNREVIEWED.

| Candidate | Source evidence level | Verification concern |
| --- | --- | --- |
| Cystic fibrosis transmembrane conductance regulator | PUBMED_PUBLICATION_ABSTRACT | FUNCTIONAL_RESPONSE_COULD_BE_MISREPRESENTED_AS_KD |
| Carbonic anhydrase 2 | CROSSREF_BIBLIOGRAPHIC_METADATA | PRIMARY_METHODS_NOT_REVIEWED_AND_KD_SEMANTICS_UNVERIFIED |
| Programmed cell death 1 ligand 1 | PRIMARY_PATENT_METADATA | MISSING_ASSAY_PROTOCOL_AND_RECORD_SOURCE_METHOD_MAPPING |
| Glucagon-like peptide 1 receptor | PUBCHEM_BINDINGDB_ASSAY_REGISTRY | ASSAY_PARTICIPANT_OR_TARGET_ASSOCIATION_REQUIRES_SOURCE_RECONCILIATION |

## Source-specific observations and next checks

### Cystic fibrosis transmembrane conductance regulator

Source identifiers: PMID:12852954, DOI:10.1016/S0960-894X(03)00482-7
Source locator: pubmed.ncbi.nlm.nih.gov/12852954

The corresponding publication abstract describes a cell-based functional transport response and half-maximal stimulation, not a directly demonstrated equilibrium Kd for the selected records.

Unresolved review requirements:
- Verify which original published table matches the exact BindingDB reactant IDs.
- Determine whether any independent biochemical binding Kd assay exists.
- Reconcile recorded protein species and experimental construct with target sequence.

**Approved: NO. Individual Kd measurements verified: NO.**

### Carbonic anhydrase 2

Source identifiers: DOI:10.1016/0960-894X(96)00069-8
Source locator: doi.org/10.1016/0960-894X(96)00069-8

The DOI in the original review queue resolves to a 1996 publication about carbonic-anhydrase binding-site probes. This is an existing DOI-only source locator, not a missing source identifier.

Unresolved review requirements:
- Obtain and inspect the publication methods and tables legally.
- Verify how the individual values were determined and whether they are directly measured exact Kd.
- Verify actual protein construct and comparable measurement conditions.

**Approved: NO. Individual Kd measurements verified: NO.**

### Programmed cell death 1 ligand 1

Source identifiers: US20240010642
Source locator: patents.google.com/patent/US20240010642A1/en

The primary patent titled Modulators of programmed death-ligand-1 is located; the candidate assay description remains missing from the original review record.

Unresolved review requirements:
- Locate the specific patent example and measurement table for the candidate assay.
- Verify primary experimental method, construct and Kd endpoint.
- Resolve record-level provenance and qualifying inequalities.

**Approved: NO. Individual Kd measurements verified: NO.**

### Glucagon-like peptide 1 receptor

Source identifiers: US11767332, PUBCHEM_AID:1919769, BINDINGDB_ASSAY:11490_1
Source locator: pubchem.ncbi.nlm.nih.gov/bioassay/1919769

The registry explicitly links to BindingDB assay 11490_1 but describes a colorimetric glucose-binding experiment involving boronate/carbohydrate, while the candidate target is recorded as GLP-1 receptor.

Unresolved review requirements:
- Verify whether GLP-1 receptor was physically present in the measured mixture.
- Check the original patent method and per-record table for the exact binding participant.
- Verify whether the Kd quantity represents carbohydrate interaction rather than GLP-1 receptor binding.

**Approved: NO. Individual Kd measurements verified: NO.**

## Corrected bibliographic interpretation

The carbonic anhydrase II row has a DOI but no PMID/patent field. A prior metadata-only index incorrectly called it missing a source identifier. The corrected index assigns PRIMARY_DOI_ONLY_METHODS_PENDING; this does not imply the actual article methods have been reviewed.

Do not automatically reject the CFTR or GLP-1 receptor rows without original table-to-record checks. Their source-level red flags warrant urgent review, not an inferred numeric validation result.

No source body text, compounds, potency values, or affinity-label arrays appear in this artifact.
