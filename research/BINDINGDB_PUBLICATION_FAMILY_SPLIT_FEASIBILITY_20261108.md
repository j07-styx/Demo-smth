# Publication-source group imbalance: hypothetical split feasibility only

**No actual split was selected or frozen. No affinity labels or prediction scores used.**

The candidate PRE_SPLIT group graph changes from 168 preliminary MMseqs protein components to 142 DOI/PMID/patent-connected protein families. The larger family count might seem enough for five roles, but 530 of 1,146 tasks belong to one source-connected family. Group-quantity balancing alone can leave test or validation roles dominated by one publication-linked family.

We ran 1,000 deterministic RNG draws of RANDOM family-to-role allocations (no identities saved), distributing 60% of group counts to base training and 10% each to base validation, adaptation training, adaptation validation and test. Only resulting task-count distributions were saved.

| Source group policy / role | Number of groups allocated | Median tasks [5th, 95th percentile] | Task share 5th–95th percentile | Draws above 2× target share |
|---|---:|---|---|---:|
| Protein groups only, base_train | 100 | 782 [291, 979] | 25.4%–85.4% | 0.0% |
| Protein groups only, base_validation | 17 | 50 [26, 538] | 2.3%–46.9% | 12.8% |
| Protein groups only, adapter_train | 17 | 52 [27, 529] | 2.4%–46.2% | 10.9% |
| Protein groups only, adapter_validation | 17 | 53 [26, 537] | 2.3%–46.9% | 10.5% |
| Protein groups only, test | 17 | 53 [26, 535] | 2.3%–46.7% | 10.4% |
| Publication-linked groups, base_train | 86 | 806 [263, 1005] | 22.9%–87.7% | 0.0% |
| Publication-linked groups, base_validation | 14 | 48 [22, 568] | 1.9%–49.6% | 11.3% |
| Publication-linked groups, adapter_train | 14 | 44 [21, 564] | 1.8%–49.2% | 10.2% |
| Publication-linked groups, adapter_validation | 14 | 45 [21, 568] | 1.8%–49.6% | 10.9% |
| Publication-linked groups, test | 14 | 47 [22, 568] | 1.9%–49.6% | 11.4% |

## Interpretation

- Source-group largest family: 530 tasks, **46.2%** of the candidate task inventory.
- A fixed group fraction is not the same as a fixed data-size fraction, and assigning a single large source family to a small validation/test role yields extreme imbalance.
- Source IDs are metadata hints rather than certified true study batches. Missing DOI/PMID links can conceal additional overlap; extra group unions may also overmerge independent assays.
- These results can guide future prespecified, label-blind quota and group-size policies once real assay review has approved a source-backed cohort. They must NOT be used to select favorable heldout group identities after inspecting labels.

## Reproduction and status

- scripts/simulate_bindingdb_publication_group_balance_dev.py
- research/bindingdb_publication_family_split_feasibility_simulation_20261108.json
- tests_v4/bindingdb_publication_group_preflight_test.py
- No actual task role mapping, frozen split or approved cohort was generated.
- Scientific cohort approval remains BLOCKED_UNAPPROVED_NOT_TRAINING_READY.
