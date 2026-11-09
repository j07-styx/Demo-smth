# Unattributed assay-task source-neighbor review: frozen pre-split metadata

**DynaCPI v4 | 9 November 2026 | Source-review prioritization only**

## Reason for the checkpoint

A scientifically defensible DynaCPI-versus-PerceiverCPI comparison requires
original assay, physical protein construct and source-family approval. The
existing seven conflicted publication-linked source families contain
**708 technically eligible tasks**. **62 tasks** have no direct original DOI,
PMID or patent identifier. Those missing citations cannot be supplied simply
from their neighbors without verifying the experiment that produced the data.

This audit asks only: *Are citations available on other tasks that share the
same preliminary protein component or original assay key?* The resulting
candidates are **review leads, not source attribution**.

## Reproduced source-identity finding

| Original source-identity review tier | Unattributed tasks |
|---|---:|
| Another task with same component **and** same assay key has source metadata | **0** |
| Another task with same component but **different** assay key has source metadata | **62** |
| Same assay key only, from a different component | **0** |
| Only more distant source-family bibliography | **0** |
| **Total with no direct DOI, PMID or patent** | **62** |

Thus every unresolved task has some source-annotated neighbor within its
protein component, but **not one has a same-assay bibliographic witness** in
the frozen, originally eligible task set.

This is specifically **not evidence that all 62 came from the neighboring
papers**. A single component can be associated with multiple physical
constructs, sources and binding protocols. No reference was copied into an
unattributed task, and all remain unapproved.

## Data access and integrity

`scripts/build_unattributed_task_source_neighbor_review_v4.py` uses exactly
the **eleven-field original PRE_SPLIT task metadata** (task ID, component ID,
assay key, technical counts and hashes), not the original assay measurement
or chemical identity records. The reader uses an exact field allowlist and
requires the previously frozen original file SHA256 to match; if a potency
field appears, the script fails closed.

It cross-checks the **1,146** eligible task/component assignments against the
frozen original **142** source-family graph, the original seven-family
private source-index witnesses, and the 708-task / 62-unsourced partition.
Neither numerical affinities, original TEST metrics, model predictions,
support/query labels nor provisional split-role assignments are read.

Public output: `research/bindingdb_unattributed_task_neighbor_summary_20261109.json`
contains only aggregate counts and warning flags.

Detailed task/component/assay/source-neighbor leads are stored exclusively
in the local private file:
`data/audit/UNATTRIBUTED_TASK_NEIGHBOR_LEADS_PRIVATE_20261109.json`.
It **must never be committed to a public repository**. Every reviewer row has
`source_record_verified=False`, `construct_verified=False`,
`training_eligible=False`, and `assay_approved=False`.

`tests_v4/unattributed_task_source_neighbor_review_test.py` checks all four
tiers on invented metadata, protects the source/task partition, rejects
forged approval and mismatched hashes, rejects nonmetadata fields, and verifies
the public aggregate exposes no original private task, component, family or
source strings.

## Decision

**Original source records verified: 0. Physical constructs verified: 0.
Scientifically approved new tasks: 0.**

The next step is independent original-method and source-table review of
the 62 unresolved tasks; the private review leads are a navigation aid,
not authorization to infer values or train a model. Source-family membership,
role allocation and protected prospective TEST outcomes remain unchanged.

**Actual scientific gate: `BLOCKED_UNAPPROVED_NOT_TRAINING_READY`.**
No real DynaCPI improvement over PerceiverCPI is claimed.
