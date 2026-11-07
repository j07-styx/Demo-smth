# Evaluation-axis feasibility, 2026-11-07

Status: UNAPPROVED_METADATA_FEASIBILITY_ONLY. No model training, frozen split, source approval, or test prediction was produced.

## Result

The metadata-filtered BindingDB candidate pool contains 1,041 tasks, 158 preliminary protein components, 12,784 compounds, 5,392 Murcko scaffold groups and 30,038 task-compound pairs. All 59 acyclic compounds stay in one group.

Counts below require at least 15 compounds per task within the assigned role (five support plus ten query). They do not establish experimental validity.

| Axis | Base train | Base validation | Adapter train | Adapter validation | Test |
|---|---:|---:|---:|---:|---:|
| Protein components | 703 | 28 | 24 | 161 | 125 |
| Chemical scaffolds | 419 | 71 | 18 | 22 | 25 |
| Both simultaneously | 272 | 3 | 1 | 4 | 3 |

The joint assignment drops 18,200 cross-axis pairs. Its nominal test role contains only three eligible tasks in three components, and adapter training only one eligible task. This particular allocation is unsuitable for a broad joint-generalization claim. It does not prove that every possible allocation is infeasible. No seed search was performed.

## Method and boundaries

The planner accepts only task, component, compound and scaffold identities. It rejects label fields, duplicate pairs and inconsistent identity mappings. A single deterministic seed (1105) orders groups by SHA-256; proportions are 60/10/10/10 percent with remaining groups in test. Protein and scaffold groups are allocated independently; joint mode retains pairs only when both roles agree. The algorithm balances numbers of groups, not tasks or pairs; the observed task imbalance must be considered before selecting a final protocol.

The loader excludes predefined metadata hard flags, some of which summarize replicate disagreement. Therefore cohort filtering is not wholly label-independent, although allocation uses no affinity values. Source approval remains absent. Preliminary protein components need a defensible homology/domain definition. Scaffold separation does not guarantee low chemical similarity. These checks separate roles; they do not enforce scaffold-disjoint support versus query within a task.

Only aggregate counts and assignment digests are exported. No memberships are frozen or published. Existing scientific-cohort checks remain blocking. The three modes are candidate evaluation regimes, not three validated benchmarks.

## Consequence for research

Preserve the numeric-only sequence development baseline. Do not tune new fusion architectures against the repeatedly inspected DAVIS validation set. Source-level assay and construct verification is the next prerequisite. A protein-disjoint study appears more plausible on current metadata; strict joint evaluation needs a different justified allocation or a larger approved pool. Any revised allocation must use identities/counts only and be fixed before model outcomes are inspected.

## Verification

Run `.venv\Scripts\python.exe tests_v4\evaluation_axes_test.py` and `.venv\Scripts\python.exe tests_v4\scientific_cohort_gate_test.py` from the repository. The first tests order invariance, forbidden labels, conflicting identities, acyclic grouping, explicit leakage detection and retained/excluded pair conservation. The second verifies the existing approval gate. The runner refuses to overwrite its dated JSON output.
