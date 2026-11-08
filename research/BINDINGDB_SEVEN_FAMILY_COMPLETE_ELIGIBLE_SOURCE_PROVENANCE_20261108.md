# BindingDB seven-family: complete eligible source-provenance replay

**8 November 2026 | DynaCPI v4 | Metadata audit; NOT an assay or split approval**

## Research question

The prior cross-role source-family investigation identified **seven** DOI/PMID/patent-connected families affecting **25 protein components assigned to more than one provisional role**. However, its reviewer worksheet retained only one sampled bibliographic identifier per family, while the preliminary source-graph report aggregated 729 identifiers over the entire technically eligible inventory.

**How much assay-source provenance is associated with the seven conflicted families when the *entire original eligible task bibliography* is replayed, rather than relying on the seven examples?**

## Technical method and provenance integrity

Replayed the original `scripts/prioritize_bindingdb_component_source_review_dev.py:gather()` metadata selector and `scripts/audit_bindingdb_source_linked_protein_groups_dev.py:source_ids()` normalization over the same pre-split technical input files. The replay respects the original >=15 distinct-compound criterion and earlier technical reactant-ID exclusions; it does not change selection rules, protein components or role assignments. It accesses original source metadata for eligible technical rows: DOI, PMID, patent, Reactant_set_id, task/group identity, original construct SHA256, source category, pH and temperature.

**No numerical Kd/pKd affinity values, model outcomes, task labels or reserved-test metrics were extracted, analyzed or emitted.** The original technical JSONL records may contain measurement columns in the same serialized objects; the provenance projection ignores those values. This is a metadata-only *analysis*, not a claim that the original files contain no affinity bytes.

The script now additionally checks the original input-file SHA256 fingerprints against the earlier frozen preflight, and verifies the replay's **1,146 tasks**, **142 source families**, **729 total DOI/PMID/patent identifiers**, **26 identifiers shared across preliminary protein components**, plus exact sampled shared component witnesses. No unobserved new group link was introduced.

## Newly quantified scope

| Indicator | Count |
|---|---:|
| Technically eligible BindingDB tasks in original source graph | 1,146 |
| Distinct original source identifiers across eligible inventory | 729 |
| Shared cross-component source identifiers across the inventory | 26 |
| Preliminary source-connected families in original source graph | 142 |
| Previously flagged families crossing provisional role boundaries | **7** |
| Technically eligible tasks belonging to those seven families | **708 (61.8%)** |
| Distinct source identifiers represented within those seven families | **220** |
| — DOI identifier strings | 74 |
| — PMID identifier strings | 90 |
| — Patent identifier strings | 56 |
| Technical tasks in the seven families lacking all DOI/PMID/patent IDs | **62** |
| Independently verified original assay-record crosswalks | **0** |
| Independently verified physically assayed protein constructs | **0** |
| Scientifically approved families / tasks through this audit | **0** |

An ID count is **not a count of unique studies**: DOI and PMID may refer to the same paper, and one transitive family can contain many papers and assay types. The 708 tasks are **not** necessarily part of the 25 overlapping role-assigned components, and they are **not** 708 demonstrated leakage events. They are all technical tasks in the seven *families* identified through that overlap. Shared publication identity does not prove identical assay; large transitive joins can be conservative overmerges.

The 62 tasks without DOI, PMID or patent still sit within preliminarily source-linked families through their protein component and other eligible tasks. Their original measurement provenance **remains unresolved**, not verified through mere group membership.

## New private review artifact

`data/audit/SOURCE_FAMILY_COMPLETE_ELIGIBLE_PROVENANCE_PRIVATE_20261108.json` contains a source-family-to-identifier-to-component-to-task metadata crosswalk for all seven conflict families, with exact original DOI/PMID/patent strings. It retains the protected provisional role counts and all components in the conflict families. It **must remain local only**: never commit this file, family identities, individual role assignments, or cross-role source links to a public repo. It is unreviewed source *indexing*, not a qualified scientific decision.

The public artifact `research/bindingdb_seven_family_eligible_source_provenance_audit_20261108.json` contains only the aggregate counts above and limitations—no family IDs, publication identifiers, task IDs, component hashes, split roles, affinity values or predictions.

## Reproducible implementation and safeguards

- `scripts/reconstruct_conflicted_source_family_provenance_dev.py` does the immutable preflight-hash-checked provenance replay and refuses to overwrite the public or private output.
- `tests_v4/conflicted_source_provenance_replay_test.py` uses seven fictional source families to verify complete metadata-only reconstruction, prevention of double/fabricated identifiers, source-family misjoins, fail-closed mismatched witnesses, output privacy, zero approval and saved artifact integrity.
- The previously published public-source access readiness tiers—four abstract-only, one secondary assay annotation, one publisher supplement index, one original patent methods table—**remain unchanged**; access-tier evidence does not become source-row verification.
- The existing source-aware scientific-cohort gate remains `BLOCKED_UNAPPROVED_NOT_TRAINING_READY`; the retired provisional TransferCPI training protocol stays locked and no reserved-test metric was examined.

## Scientific consequences and next milestone

**The review burden is not seven papers.** At minimum, the new private index shows 220 source identifier strings in the seven families; review needs to disentangle DOI/PMID aliases, establish paper-versus-patent source equivalence, determine which source records actually produced numeric *direct* equilibrium Kd, and verify physical protein constructs. Some identifiers and tasks may collapse to fewer independent studies after qualified review, while other unindexed studies may emerge.

A defensible next human-review pass should begin with publication deduplication/alias reconciliation, prioritize the 62 metadata-unattributed technical tasks, trace exact experimental tables/constructs and log independently verified source evidence. Do not silently move, approve or reselect previous role assignments on the basis of observed development scores. Only an independently adjudicated cohort and newly preregistered, source- and homology-disjoint split can support formal training and final claims.
