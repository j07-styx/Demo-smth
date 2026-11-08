# DynaCPI: seven-family primary-source evidence access audit

**8 November 2026 | Metadata and public-source-access triage only | No scientific approvals**

## Purpose

The existing provisional BindingDB protein-component roles contain seven DOI/PMID/patent-connected source families spanning training, inner development, and reserved-test components. A publication identifier or method keyword alone cannot certify that an individual BindingDB affinity record was measured with the claimed experimental construct or direct binding endpoint.

This continuation distinguishes **what source evidence has been located** from **which experiments have been independently verified**. It uses the previously created private conflict reviewer queue and separately annotated public bibliographic/method access. It does not read quarantined raw potency records, provisional training labels, prediction files, or reserved-test outcomes.

## Results

| Evidence access level | Source families | Meaning |
|---|---:|---|
| Original patent binding-assay methods table located | 1 | Original multi-target assay table includes qualified, inequality-censored and missing entries; per-record crosswalk still required |
| Publisher supplementary-information index located | 1 | Index identifies distinct physical binding methods and protein preparation sections; specific source rows and constructs still unverified |
| Secondary public assay annotation | 1 | Describes an experimental protein fragment; source-paper construct identity and record matching still unresolved |
| Article abstracts only | 4 | Bibliography and a brief assay claim; original method, construct and row still unverified |
| **Total** | **7** | All seven have one bibliographic/method source anchor, **none is an approved task or verified affinity record** |

These access tiers are deliberately conservative. Reading an original patent method table does not approve its measurements, and a publisher's supplementary-material *index* does not mean that its underlying supplementary tables have been verified. A transitive source-family group may be connected to many publications; **one example source identifier is not an exhaustive literature inventory**.

The original patent material visibly distinguishes exact observations, inequalities and unmeasured entries. This motivates a hard source-review requirement to preserve the qualifier rather than silently turning a lower/upper bound or missing measurement into an exact numerical Kd. It is a **methodology finding only**, not a record-level comparison or retrospective test evaluation.

## Reproducibility, separation and safeguards

- Public aggregate result: `research/bindingdb_seven_family_primary_access_readiness_20261108.json`.
- Generation: `scripts/build_seven_family_source_access_ledger_dev.py`.
- Regression: `tests_v4/seven_family_source_access_readiness_test.py` (8 synthetic/integrity cases) plus the prior private source-queue and scientific gate suites.
- Private source-family/role assignment and access notes: `data/audit/SOURCE_FAMILY_PRIMARY_ACCESS_LEDGER_PRIVATE_20261108.json`. **Never commit or publish this file.**
- The pre-existing 921-record, 30-task human-review worksheet is preserved unchanged. Its earlier report documented 0 approved tasks; this continuation does not touch the worksheet.

The script refuses to overwrite existing reports. It requires exactly seven distinct known conflict families with a single pre-existing cited source anchor per family, rejects a family whose review state has changed from UNREVIEWED, and projects **only tier counts** into the public artifact. It does not emit source-family IDs, DOI/patent identifiers, target names, split role memberships, measured affinity values, compounds, sequences or predictions in the public output.

## Immediate evidence requirements for independent reviewers

A qualified reviewer must perform a separate source-row crosswalk against each publication's original table and methods, document directly measured vs inferred or proxy endpoints, capture exact measurement qualifiers, verify the physically assayed protein construct and assay comparability, and record evidence/decision in the established controlled human-review worksheet. No review decision is automatically generated.

After the original source measurements and protein constructs have been adjudicated, the team may preregister a **new** study-source-family- and independently certified protein-homology-disjoint evaluation policy. The prior reserved-test component assignments remain archived and untouched; no new model selection, training, promotion or test scoring occurred.

**Gate:** `BLOCKED_UNAPPROVED_NOT_TRAINING_READY`. Technical source access and passing unit tests are never substitutes for source-level biological validation.
