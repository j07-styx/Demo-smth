# DynaCPI v4 — six-source assay method and construct risk checkpoint

**9 November 2026 | Source-method evidence triage only | Zero affinity records or constructs scientifically approved**

## Why it matters for beating PerceiverCPI

It is not enough to build a model that outperforms original PerceiverCPI on a provisional data split. The earlier pilot relied on a subsequently retired split with unresolved original-publication source-family overlap and physical assay constructs. In particular, a **full-length protein identifier is not proof of the physical protein construct used in a kinase-domain binding assay**. A stronger geometry-aware model could show an apparent gain because its input representations do not match the measured assay or because missing/censored binding endpoints are treated incorrectly.

This checkpoint reviewed **publicly accessible methodological metadata and published supplementary-table descriptions** for the same six previously frozen original-source review tasks, rather than seeking new favorable development examples.

**What was inspected:** source-method descriptions, broad physical-construct descriptions, public registry target-relationship annotations, original citation class and reported endpoint class. No original numerical Kd/pKd, compounds, molecular structures, training labels, per-query predictions or protected TEST outcomes were used.

## The six-source method-risk inventory

The six previously frozen review tasks cover **147 candidate original-source records**, but no individual record is approved.

| Independent source-method annotation | Tasks | Interpretation |
|---|---:|---|
| Registry directly assigned to a target | **1** | A direct database target annotation is not a verified physical construct sequence |
| Registry target assigned by homology | **2** | The registry does not establish that the annotated full-length target sequence was the measured construct |
| No individually verified registry target relationship | **3** | Target annotation remains unresolved for this evidence stage |
| A kinase-domain assay is indicated by source metadata | **3** | Requires independent domain-boundary and sequence/construct verification |
| Published kinase Kd matrix has a missing/censoring qualification warning | **3** | Blank or unobserved entries must not be silently turned into exact affinity values |
| Recombinant-protein SPR method described in source registry | **1** | Supports review priority but does not prove individual source-row matching |
| NMR-derived method with unresolved assay-condition comparability | **1** | Method, environment and endpoint must be reviewed rather than pooled automatically |
| An original Kd study is not identified by the supplied review citation | **1** | Cannot treat a review or secondary reference as primary experimental evidence |

These categories **overlap**. The first three rows form the exclusive target-assignment breakdown (1+2+3=6); the remaining rows identify method-specific risks and must not be summed as disjoint task groups.

The source evidence includes one recombinant, tagged protein method, three kinase-domain method records, and a publicly reported kinase binding matrix that distinguishes reported measurements from blank entries. The source registry uses both *direct* and *homologous* target relationships. Crucially, these are **registry/paper-level signals**, not experimental construct sequences individually verified against original measurements.

## Evidence hierarchy: what is and is not established

**Established for review prioritization:**
- All six task references match the existing immutable human review queue by exact task, assay identity and original metadata-only source-record count.
- Public method metadata documents at least two **homologous** target assignments, and three source tasks refer to kinase-domain methods rather than verified complete protein sequences.
- Source descriptions distinguish direct binding methods from endpoints or data entries that need separate condition, censoring and citation checks.
- Source review artifacts retain every unresolved qualification; all original assay-to-record matches, actual assayed sequences and scientific approvals remain **false**.

**Not established:**
- An exact per-record original source table crosswalk for any of the 147 technical candidate records.
- Any physically assayed protein's exact amino-acid sequence or construct boundaries, even where recombinant tagging is described.
- A source-qualified exact Kd for any original candidate record, separated from inequalities, missing measurements or non-Kd endpoints.
- A legitimately source-family- and homology-disjoint new training/validation/test split.
- Any DynaCPI-vs-PerceiverCPI performance advantage on scientifically approved real data.

The correct next scientific action is **human primary-method and original supplementary-table adjudication**. The computational metadata check cannot substitute for checking the authentic assay source, experiment conditions, qualifier semantics and physical protein construct.

## Implementation and confidentiality

`scripts/triage_six_construct_endpoint_evidence_v4.py` is a **generic, public, read-only** method-risk validator. It accepts only metadata from the existing 30-task unreviewed reviewer worksheet and the previous six-source bibliographic lead snapshot. It fails closed on changed task identity, original source-record count, an H/homology annotation without an explicit warning, attempts to ignore kinase-domain risks, or attempts to change an unreviewed source into an approved task.

**Crucially, all task-to-assay/source/registry annotation relationships are kept private** in:
- `data/audit/SIX_TASK_METHOD_ANNOTATIONS_PRIVATE_20261109.json`
- `data/audit/SIX_TASK_CONSTRUCT_ENDPOINT_METHOD_TRIAGE_PRIVATE_20261109.json`

Only aggregate nonidentifying counts are emitted to `research/six_task_construct_endpoint_method_triage_20261109.json`. Neither the public script nor its synthetic tests embeds original target, assay or registry mappings. The existing source reviewer CSV is preserved byte-for-byte. Both original prior public-source metadata and private review remain unmodified.

`tests_v4/six_construct_endpoint_method_triage_test.py` uses **entirely fictional assay/target/task identities** to reject forged approvals, source-count mismatches, lost homology/kinase-domain warning flags, and leaks. It also replays the original metadata-only aggregate against its frozen local private annotations; the approval count stays zero.

## Proposed real-evaluation prerequisite

Before DynaCPI can be judged against a strong support-aware PerceiverCPI KRR baseline:
1. Independently verify the physical sequence/boundaries of protein constructs actually used in each source assay, including truncated kinase domains and tags.
2. Resolve the original source table and experimental method for each eligible row, and preserve exact, inequality-censored, missing and assay-specific endpoint distinctions.
3. Freeze an approved collection with independent study-source and homology components before training or reading any new held-out evaluation.
4. Then compare preselected PerceiverCPI KRR and the DynaCPI guarded-geometry arm using identical K-shot support panels, source-family-balanced RMSE, negative controls, calibration and paired uncertainty.

**Actual scientific gate:** `BLOCKED_UNAPPROVED_NOT_TRAINING_READY`. **Original source-row approvals: 0. Physical construct sequence verifications: 0. Real model benchmarking this turn: none.**

This is a scientific evidence-quality milestone and a stricter future training input definition; it is not yet a biological or predictive accuracy improvement.
