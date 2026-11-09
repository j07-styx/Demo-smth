# DynaCPI: assay-context triage for the 62 citation-unattributed tasks

**9 November 2026 | Metadata-only original-source audit | All tasks still unapproved**

## Purpose

The original DynaCPI–PerceiverCPI pilot split was retired because
publication-linked source-family overlap and original assay identities had
not been independently verified. Seven affected preliminary source families
contained 708 technically eligible tasks. Sixty-two of those tasks were
missing every direct DOI/PMID/patent identifier; the preceding source-neighbor
audit established that all 62 had bibliographic neighbors on the same
preliminary protein component but **different** assay keys. Such nearby
citations must not be assigned to the missing-source task.

This checkpoint asks a more specific question: *What broad assay methods
do the original 62 source-unattributed tasks actually describe?* It does
not claim to retrieve their original physical assay constructs or measure
a binding endpoint.

## Replayed original task-to-assay-context metadata

The original frozen task metadata was joined to the frozen assay-context
metadata by **exact protein-sequence SHA256 and assay key** for each of
the 62 unidentified-source technical tasks. All 62 matched one and only
one context. Exactly two preliminary protein components were involved.

| Reported assay-context category | Tasks |
|---|---:|
| Generic kinase inhibitor selectivity profiling | **54** |
| D3R challenge-series contexts | 4 |
| OctetRed-labeled methods | 3 |
| Thermofluor-labeled method | 1 |
| Other / unidentified context type | 0 |
| **Total** | **62** |

All **62** original contexts have `article_doi_count=0`. The original
description-classifier flags `kd` and `ic50` are also false for all 62.
**Neither fact proves that the underlying records lack experimental binding
data.** These are only signals emitted by a previously frozen, narrow
metadata classifier; a false flag or generic description cannot establish
experimental endpoint identity or potency semantics.

The 54 kinase-profiling tasks share a **generic context category**, but
this is not evidence that they share the same original source article,
individual assay rows, physical constructs or actual method conditions.
In particular, a kinome-screening context name is not equivalent to a
verified direct equilibrium Kd endpoint.

The four challenge-series and four other named-method contexts each
require their own direct publication, endpoint, species, construct and
condition checks. No one context type was automatically included,
reclassified or excluded from a scientific training set.

## Immutable data and privacy controls

`scripts/triage_unattributed_assay_contexts_v4.py` reads only:

1. The original **eleven-field PRE_SPLIT task-metadata** JSONL, which has
   task IDs, sequence digests, assay keys and technical counts but no binding
   affinity or molecule structures.
2. The original frozen assay-context JSONL, with broad method descriptions,
   DOI counts and keyword flags, but no per-query numeric labels.
3. The existing immutable **private** 62-task source-neighbor worklist and
   source-graph preflight with original SHA256 file checksums.

Both JSONL inputs have exact field allowlists. Changed checksums,
unexpected measurement/potency fields, duplicate contexts, reordered
source identities, earlier reviewer approvals or source/assay mismatches
fail closed.

Individual source-neighbor IDs, task IDs, assay names and keys, protein
sequence digests, context-description hashes and protein components
remain only in:
`data/audit/UNATTRIBUTED_TASK_ASSAY_CONTEXT_PRIVATE_20261109.json`.
**Do not publish or commit that file.**

The public aggregate
`research/bindingdb_unattributed_assay_context_20261109.json`
reports only category counts, approval status and caveats. The tests use
fictional task/assay identities to validate the grouping and confirm
that no confidential source or task IDs appear in public deliverables.

## Scientific disposition

- Exact original experimental assay-row source attributions approved: **0**
- Exact Kd endpoint identity verified in this checkpoint: **0**
- Physically tested target construct sequences approved: **0**
- Unattributed tasks admitted to model fitting or evaluation: **0**
- Protected prospective TEST outcome access: **none**
- Real DynaCPI accuracy improvement over PerceiverCPI: **not measured**

The next meaningful step is to verify **original method papers or registry
provenance for the assay-context groups**, especially the 54 generic
kinase-profiling entries, before constructing a new source-family-independent
evaluation cohort. Do not interpret similar assay labels as a license to
copy a citation or convert censored/missing measures into exact Kd.

**Actual science gate: `BLOCKED_UNAPPROVED_NOT_TRAINING_READY`.**
