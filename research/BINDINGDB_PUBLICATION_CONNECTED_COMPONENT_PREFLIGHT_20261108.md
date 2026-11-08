# Publication-linked protein-group preflight for BindingDB

**Quarantined metadata-only evidence / 2026-11-08. No source or assay approved. No prospective test touched.**

## Why protein-disjoint alone is insufficient

Different protein components can share a BindingDB Article DOI, PubMed ID or patent: a nominally target-disjoint evaluation then reuses study-level assay, publication and library metadata across splits. This does not prove prediction leakage, but must be examined before declaring independent generalization.

## Resulting candidate independence structure

- 1,146 technically eligible source-linked tasks at >=15 distinct compound identities (not scientifically reviewed).
- 168 preliminary MMseqs protein components joined into **142 conservative study families** using matching DOI/PMID/patent identifiers.
- **26 net protein-component merges** arising from shared source identifiers; largest source family has 17 original protein components and 530 tasks.
- Original 40-component-only metadata shortlist had **2 repeated source-family positions**. The revised 40-lead queue has **40 distinct protein components AND 40 distinct study-source families**.
- Revised shortlist has 40 single-DOI leads, 34 text mentions of SPR/ITC/BLI, and 0 indirect, kinetic or construct-review keywords.

## Source-linked review leads

| Rank | Task prefix | Protein component prefix | Study family prefix | Unique compounds | Source DOI | Method hint |
|---:|---|---|---|---:|---|---|
| 1 | a4a24fc28851 | 5de81f208e71 | 570352e38422 | 149 | 10.1016/j.bmc.2008.05.004 | SPR |
| 2 | 703929adb99f | 37034eceadf1 | 041ed02c8527 | 83 | 10.1021/acs.jmedchem.1c01307 | SPR |
| 3 | f9674ae2f7e2 | 4defde59a1d7 | 424fae22b070 | 60 | 10.1016/j.ejmech.2019.111656 | SPR |
| 4 | f842ffbba31e | 17751c0357a6 | e41025c9bf5a | 44 | 10.1021/jm0707424 | ITC |
| 5 | e495c6d81baa | 85340f1c02b3 | 3bbb49f20268 | 41 | 10.1021/acs.jmedchem.6b00002 | SPR |
| 6 | 5b04c3024617 | 7b8d960f96e4 | a00434fc1e8e | 40 | 10.1021/acs.jmedchem.3c00332 | ITC |
| 7 | 5424dcc1f75f | 14dbf9627717 | a0ef52e68dbb | 35 | 10.1021/acs.jmedchem.9b01492 | SPR |
| 8 | 360fc623c062 | 1745754698cf | fa461161a578 | 31 | 10.1021/ml100224d | SPR |
| 9 | 7af4c3526746 | 0549a3a6ebe7 | 5a37ad6356db | 29 | 10.1021/acs.jmedchem.9b00096 | ITC |
| 10 | fd68476242bd | 00faf52e877f | 3aef3838b285 | 28 | 10.1016/j.bmc.2013.02.021 | SPR |
| 11 | 339ce3f0626b | 23d8ef29b75d | 97cfed04ab38 | 26 | 10.1016/j.bmc.2010.11.049 | ITC |
| 12 | 83775558aead | 1d2551ade453 | 0ae215d1f865 | 26 | 10.1021/acs.jmedchem.8b00210 | SPR |
| 13 | 4c1e5aafd326 | 9a06387610ed | 5ce5e61cf605 | 25 | 10.1016/j.ejmech.2021.113887 | SPR |
| 14 | a6769954d814 | 905879029f76 | 013631b028ab | 25 | 10.1016/j.bmcl.2012.08.001 | SPR |
| 15 | f7367fa4e1bf | 030ef1b42438 | edf1a3fb3e7d | 24 | 10.1021/acs.jmedchem.2c02132 | SPR |
| 16 | 017471a8d9dc | 3501ff1a2c34 | 5b0985a8bbec | 22 | 10.1016/j.ejmech.2012.02.050 | ITC |
| 17 | 0eed22a59fce | 2b786a6db716 | b55dd963074e | 22 | 10.1016/j.bmcl.2019.01.035 | SPR |
| 18 | 16c9bfd381f4 | 19fad6122957 | 0a7696b8b4d4 | 22 | 10.1021/acs.jmedchem.3c00960 | SPR |
| 19 | ba29c0985a8a | 0451c5f5ef05 | 9620642dd84d | 22 | 10.1021/acs.jmedchem.0c02051 | SPR |
| 20 | e457bb9e52c1 | 3bb208c70fae | a7f4549ac281 | 22 | 10.1021/jm100834y | SPR |

## Important interpretation limits

Publication links are a **conservative source independence guard**, not a proof that all records sharing a DOI are the same assay. PMID, DOI and patent links may merge genuinely distinct assays; missing IDs permit unrecognized source overlap. The groups still require wet-lab construct, assay, chemistry and protein homology certification, and a reviewer-approved split.

No affinity value or DEV/test score was used to select these 40 leads. All task decisions stay **UNREVIEWED**. Do not use this queue as a training cohort, a validation set or a source approval manifest.

## Reproduction

- scripts/audit_bindingdb_source_linked_protein_groups_dev.py
- research/bindingdb_publication_connected_protein_review_preflight_20261108.json
- research/bindingdb_publication_disjoint_source_review_queue_20261108.csv
- tests_v4/bindingdb_publication_group_preflight_test.py
- All source JSONL input checksums recorded in the JSON output; original raw assay records and affinity values remain in local quarantined data/audit and are not committed.
