# BindingDB provisional split: publication-source leakage preflight

**8 November 2026 | DynaCPI v4 | Label-blind technical audit, NOT scientific approval**

## Question and method

Does the provisional 82-train / 20-inner-DEV / 33-reserved-test *protein-component* split also separate source-linked DOI/PMID/patent families?

The audit joins the already-recorded 168 protein-component -> 142 source-family mapping from `bindingdb_publication_connected_protein_review_preflight_20261108.json` to the separate provisional role manifest `bindingdb_frozen_component_split_manifest_dev.json`. It considers all mapped components in each role and flags a family whenever its components appear in two or more roles. Families are defined conservatively by transitive DOI/PMID/patent linkage over the eligible pre-split task inventory.

**Only the two existing metadata JSON files were read for the aggregate analysis.** No raw assay values, candidate labels, SMILES, sequence embeddings, experimental outcomes, reserved-test labels/predictions or model scores were accessed. The existing role manifest and scientific gate were not changed.

## Result

| Existing split role | Protein components | Distinct source-connected families |
|---|---:|---:|
| Train | 82 | 74 |
| Inner development | 20 | 17 |
| Reserved prospective test | 33 | 33 |

117 unique source families occur among the 135 assigned protein components. **Seven families span more than one role**, involving **25 protein components** overall: 13 in training, 8 in inner-DEV, 4 in reserved-test.

| Role pair | Source families shared | Components in first role within those families | Components in second role |
|---|---:|---:|---:|
| Train vs inner-DEV | 3 | 10 | 6 |
| Train vs reserved-test | 2 | 3 | 2 |
| Inner-DEV vs reserved-test | 2 | 2 | 2 |

No family spans all three roles in these source-family metadata. The seven cross-role families are distinct. Two source families cross training/test; two cross DEV/test; three cross training/DEV.

**Decision: the provisional split FAILS publication-source family independence under the existing conservative metadata definition.** Different protein-component IDs are not sufficient to claim independence from shared studies, assays, source batches or compound libraries. This is *potential* batch/source leakage, NOT proof that predictions exploited leakage.

## Reproducibility and private reviewer handoff

Public aggregate machine-readable result: `research/bindingdb_provisional_role_source_overlap_audit_20261108.json`.

Source script: `scripts/audit_provisional_bindingdb_source_split_dev.py`. Tests: `tests_v4/provisional_source_split_leakage_test.py`, including synthetic three-role/transitive checks, fail-closed missing mapping/reused component cases, and a real manifest-hash replay.

A **private local-only reviewer worklist**, containing the 25 relevant source-family hashes, component hashes and provisional role assignments, was produced at `data/audit/PROVISIONAL_SOURCE_SPLIT_REVIEW_PRIVATE_20261108.csv` by `scripts/build_provisional_source_overlap_private_review_dev.py`. The worklist contains **no compound identity, protein sequence, affinity values, prediction scores or human approval**. Never commit the private CSV or reveal its role memberships when reporting a blind test.

Both scripts refuse overwriting their existing outputs; preserve those records. The source-families and original split SHA256 fingerprints are recorded in the JSON. This is a deterministic report on fixed inputs, not a new split or approval.

## Scientific next steps and constraints

1. **Keep the original prospective test quarantined.** Do not score it, retune after seeing it, or claim that the current split meets publication-disjointness. Do not silently move components to improve metrics; doing so would invalidate the original prospectivity assumptions.
2. An independent reviewer should examine each source family in the local conflict worksheet, tracing the exact DOI/PMID/patent, measured endpoint, method, original assay record and protein construct. A shared publication may contain distinct assays; conservatism is intentional and can overmerge unrelated studies. Missing identifiers can conceal additional links.
3. Independently adjudicate the existing `UNREVIEWED` BindingDB Kd assays and record precise, source-supported decisions. Do not auto-approve on keyword matches or DOI presence.
4. Only after approved assay records and an independently checked protein-homology graph exist, **pre-register a new source-family- and protein-homology-constrained split policy** with class balance and group-size constraints defined without looking at labels or model predictions. Freeze its membership and hashes before retraining or comparing reference models.
5. Fit and tune all candidate models on approved train/inner-validation roles only; use a matched budget, multiple seeds, mean/chemical controls and predefined pooled/macro reporting. A later genuinely independent evaluation needs a properly protected holdout and a one-time protocol.

The scientific cohort gate remains `BLOCKED_UNAPPROVED_NOT_TRAINING_READY`. A programming/test pass or a DOI/PMID match is not biological validation.
