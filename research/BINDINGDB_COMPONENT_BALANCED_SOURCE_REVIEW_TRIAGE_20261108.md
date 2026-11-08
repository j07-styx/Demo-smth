# Component-balanced BindingDB source-review priorities

**Unreviewed metadata screen — NOT an approved affinity cohort, not experimental validation.**

- Source: full November 2026 BindingDB *pre-split*, technically screened exact-looking-Kd candidate pool; 1146 eligible tasks from 168 preliminary MMseqs protein components.
- Complete source ID lineage: 43,629 eligible reactant IDs joined to original bibliographic and construct metadata; none missing.
- Candidate tasks with single DOI: 780; with single PMID: 870; with SPR/ITC/BLI keywords: 189.
- Candidate tasks with any reported pH: 64; temperature: 39. Missing conditions are a warning rather than automatic proof of incompatibility.
- Selected 40 review leads from 40 distinct protein components; overlap with previous unreviewed 30-task queue: 4.
- Ranking uses only source documentation, sequence metadata and unique molecular identity counts. It DOES NOT use numeric Kd/pKd labels, prediction scores, or holdout performance.

## Top review leads (metadata evidence only)

| Rank | Task ID prefix | Component prefix | Unique compounds | Source DOI | Explicit SPR/ITC/BLI clue | Flags |
|---:|---|---|---:|---|---|---|
| 1 | a4a24fc28851 | 5de81f208e71 | 149 | 10.1016/j.bmc.2008.05.004 | SPR | temperature_missing_or_inconsistent |
| 2 | 703929adb99f | 37034eceadf1 | 83 | 10.1021/acs.jmedchem.1c01307 | SPR | ph_missing_or_inconsistent,temperature_missing_or_inconsistent |
| 3 | f9674ae2f7e2 | 4defde59a1d7 | 60 | 10.1016/j.ejmech.2019.111656 | SPR | ph_missing_or_inconsistent,temperature_missing_or_inconsistent |
| 4 | f842ffbba31e | 17751c0357a6 | 44 | 10.1021/jm0707424 | ITC | ph_missing_or_inconsistent,temperature_missing_or_inconsistent |
| 5 | 1632cad14818 | c6c68b0fd0d9 | 42 | 10.1016/j.ejmech.2019.111656 | SPR | ph_missing_or_inconsistent,temperature_missing_or_inconsistent |
| 6 | e495c6d81baa | 85340f1c02b3 | 41 | 10.1021/acs.jmedchem.6b00002 | SPR | ph_missing_or_inconsistent,temperature_missing_or_inconsistent |
| 7 | 5b04c3024617 | 7b8d960f96e4 | 40 | 10.1021/acs.jmedchem.3c00332 | ITC | ph_missing_or_inconsistent,temperature_missing_or_inconsistent |
| 8 | 5424dcc1f75f | 14dbf9627717 | 35 | 10.1021/acs.jmedchem.9b01492 | SPR | ph_missing_or_inconsistent,temperature_missing_or_inconsistent |
| 9 | 360fc623c062 | 1745754698cf | 31 | 10.1021/ml100224d | SPR | ph_missing_or_inconsistent,temperature_missing_or_inconsistent |
| 10 | 7af4c3526746 | 0549a3a6ebe7 | 29 | 10.1021/acs.jmedchem.9b00096 | ITC | ph_missing_or_inconsistent,temperature_missing_or_inconsistent |
| 11 | fd68476242bd | 00faf52e877f | 28 | 10.1016/j.bmc.2013.02.021 | SPR | ph_missing_or_inconsistent,temperature_missing_or_inconsistent |
| 12 | 339ce3f0626b | 23d8ef29b75d | 26 | 10.1016/j.bmc.2010.11.049 | ITC | ph_missing_or_inconsistent,temperature_missing_or_inconsistent |
| 13 | 83775558aead | 1d2551ade453 | 26 | 10.1021/acs.jmedchem.8b00210 | SPR | ph_missing_or_inconsistent,temperature_missing_or_inconsistent |
| 14 | 4c1e5aafd326 | 9a06387610ed | 25 | 10.1016/j.ejmech.2021.113887 | SPR | ph_missing_or_inconsistent,temperature_missing_or_inconsistent |
| 15 | a6769954d814 | 905879029f76 | 25 | 10.1016/j.bmcl.2012.08.001 | SPR | ph_missing_or_inconsistent,temperature_missing_or_inconsistent |
| 16 | 53fbde01df4d | 24e3b138fc0a | 24 | 10.1016/j.bmcl.2012.08.001 | SPR | ph_missing_or_inconsistent,temperature_missing_or_inconsistent |
| 17 | f7367fa4e1bf | 030ef1b42438 | 24 | 10.1021/acs.jmedchem.2c02132 | SPR | ph_missing_or_inconsistent,temperature_missing_or_inconsistent |
| 18 | 017471a8d9dc | 3501ff1a2c34 | 22 | 10.1016/j.ejmech.2012.02.050 | ITC | ph_missing_or_inconsistent,temperature_missing_or_inconsistent |
| 19 | 0eed22a59fce | 2b786a6db716 | 22 | 10.1016/j.bmcl.2019.01.035 | SPR | ph_missing_or_inconsistent,temperature_missing_or_inconsistent |
| 20 | 16c9bfd381f4 | 19fad6122957 | 22 | 10.1021/acs.jmedchem.3c00960 | SPR | ph_missing_or_inconsistent,temperature_missing_or_inconsistent |

## Manual verification required before a source can be approved

1. Open the original publication or patent and identify the exact table, supplementary cell or deposited result for the BindingDB reactant IDs.
2. Confirm experimental Kd as a directly measured equilibrium dissociation constant, not IC50, Ki, EC50, competition-derived estimate, mixture, censored bound or imputed value.
3. Establish compound structure, salt/stereochemistry/tautomer equivalence between publication and BindingDB source for all task records.
4. Confirm experimentally assayed protein construct, truncations, variants, post-translational modifications and sequence relative to UniProt/candidate source.
5. Assess assay-method comparability, experimental conditions and within-task replicate discrepancies. Require explicit evidence for acceptance.
6. Have an independent reviewer adjudicate each task, then validate source evidence manifest and protein/chemical split before an approval artifact is possible.

## Files and integrity

- Machine-readable metadata evidence: research/bindingdb_component_balanced_source_review_priority_20261108.json.
- Review queue CSV: research/bindingdb_component_balanced_source_review_priority_20261108.csv. Its reviewer_decision column is initialized UNREVIEWED; this is NOT an authorized gate artifact.
- Reproduce via scripts/prioritize_bindingdb_component_source_review_dev.py.
- This work does NOT write data/audit/bindingdb_source_approved_cohort.json or a frozen protein split and does not change the scientific cohort gate.
