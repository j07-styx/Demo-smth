# DynaCPI source-family-aware scientific-cohort gate

**8 November 2026 | Engineering artifact integrity, not experimental source approval**

## Finding and motivation

The old pilot's 135 provisional protein components were assigned to train / inner-DEV / reserved test without guaranteeing publication-family independence; the prior metadata audit found **7** DOI/PMID/patent-connected study families across roles. The earlier private scientific-cohort artifact gate independently checked protein group disjointness but did not require a **frozen publication-source-family graph**. A formal future cohort could therefore pass its *technical* protein component check while still reusing source-connected studies across roles.

**Implemented remedy:** a source-family freeze gate is now included in `dynacpi/scientific_cohort_gate.py`, using `dynacpi/approved_source_family_gate.py` and the existing `dynacpi/source_publication_split_guard.py`. This is a necessary pre-training artifact check only: it cannot prove a paper's numerical Kd, protein construct, assay methodology, or the independence of source-review decisions.

## Future private manifest contract (three cryptographically tied artifacts)

Do not generate or falsely mark any of the following APPROVED without independent review.

| Private artifact | Role |
|---|---|
| `data/audit/bindingdb_source_approved_cohort.json` | Source-reviewed cohort containing task IDs, protein component IDs, human adjudication references, chemistry counts and reviewer metadata |
| `data/audit/bindingdb_frozen_protein_group_split.json` | Five-role task mapping, immutable cohort file SHA256, preregistered split policy and freeze provenance; now also **source_family_manifest_sha256** |
| `data/audit/bindingdb_frozen_source_families.json` | Source-family graph for every approved protein component with family identity hashes, the matching cohort SHA256, provenance and source-method review metadata |

The new source graph requires exact status `SOURCE_FAMILY_GRAPH_FROZEN_AND_SOURCE_REVIEWED`, `source_linkage_policy_id`, `reviewer_identity`, a 64-character `review_evidence_manifest_sha256`, and a timezone-aware `freeze_timestamp_utc`. Its `source_family_by_protein_component` maps *exactly* the cohort's protein components, with a lowercase 64-hex family identifier for each. The frozen split's `source_family_manifest_sha256` must equal the bytes of this separate graph; the graph's `cohort_sha256` must equal the approved cohort's bytes; and the frozen split itself must still match that cohort.

All five roles (`base_train`, `base_validation`, `adapter_train`, `adapter_validation`, `test`) must have at least **three independent study-source families**, with at least **25 families overall**. The existing protein-component quota (>=3 per role; >=25 overall) still applies separately. All components of a source-connected family must be assigned to one role. A publication may contain biologically distinct experiments and missing IDs can hide overlap; a qualified reviewer must address these limitations when creating the source graph. Source family grouping is not a chemistry- or compound-cold split by itself.

## Fail-closed behavior

An absent source-graph file, absent or edited digest, source manifest with unreviewed status, invalid timestamp/hash, duplicate JSON keys, unknown/extra component, multi-role source family, or inadequate independent families raises `PermissionError` before a future training script may proceed. Both source and cohort review evidence digest fields must be valid lowercase SHA256 strings. The real `current_status(ROOT)` continues to report `BLOCKED_UNAPPROVED_NOT_TRAINING_READY` because actual reviewed manifests do not exist.

The historical TransferCPI pilot has its own separate, permanent provisional-protocol retraining lock. Its previously saved pilot metrics/checkpoints remain archival and were not reproduced or rescored during this upgrade.

## Automated verification

- `tests_v4/approved_source_family_gate_test.py`: 15 synthetic-only cases covering valid fictional artifact integrity, cross-role source reuse, absent/extra mappings, malformed hashes, tampering, duplicate JSON keys, changed cohort linkage, false statuses, insufficient independent source families, timezone-freeze requirements, family deduplication and real cohort still blocked.
- `tests_v4/scientific_cohort_gate_test.py`: existing synthetic artifact gate updated to require a source-family manifest and checksum, preserving checks for protein component reuse and changed cohort.
- Existing `tests_v4/bindingdb_publication_group_preflight_test.py` and `tests_v4/provisional_transfer_training_lock_test.py` remain regressions.

All successful synthetic approvals are explicitly **fictional unit-test data** and constitute no record-level experimental approval. No source record in the real BindingDB candidate inventory was marked approved, no roles were changed, and no prospective test labels/scores were accessed.

## Scientific next action (still blocked)

Have reviewers inspect the seven flagged source families' original methods and supplementary tables, verify each experimental construct and endpoint against exact source records, document disagreement/qualifiers and review signatures, and then preregister a new independent split plan. The reviewed graph must be grounded in complete publication lineage; the old conservative metadata graph can only be replaced with documented, source-supported adjudication. Design and freeze group balance **without** optimization on outcomes or inspected development results. Only then create the three private manifests and use the artifact gate as a *necessary but insufficient* check. Future experiments still require compute-matched multiseed baselines and protected final evaluation.
