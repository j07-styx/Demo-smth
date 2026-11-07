# DAVIS source-review triage after additional GPT-6 experiments

The latest model development results do **not** demonstrate neural or structural superiority. On training-only leave-one-protein-identifier-out numeric Kd data, the chemical Tanimoto kernel scored 0.8540 macro RMSE, whereas a compact neural head with real protein features scored 1.0224 and a zero-protein ablation 0.9098. In an unseen-compound challenge, the chemical kernel's advantage over its training-mean comparator was small and its target-bootstrap interval included zero. No independent test was scored.

To advance dataset readiness rather than tune another architecture on repeatedly inspected development data, this change combines two *existing* independent mechanical evidence summaries: 63 publisher-source records and the subsequent registry lookup of the 40 unresolved records. It does not alter any source-review decision.

| Source target | Exact structure and numeric match | Additional registry link (stereo unverified) | No unique registry link | Conditional total |
|---|---:|---:|---:|---:|
| IRAK3 | 9 | 7 | 8 | 16 |
| RIOK2 | 9 | 4 | 7 | 13 |
| SRPK3 | 5 | 8 | 6 | 13 |

**IRAK3 is the first review priority:** only if at least six of its seven registry links are independently verified could it reach the 15-compound minimum. This is not a declaration that it is eligible: stereo identity, direct Kd endpoint, physical construct, source methods, and conditions remain unreviewed. RIOK2 and SRPK3 would still need at least two additional independent compound identity mappings even if all existing registry links were verified. These counts assume each source record represents a distinct usable compound; reviewer confirmation of unique structures is required.

The aggregate machine-readable report `research/davis_source_review_priority_20261107.json` explicitly records **zero approvals** and refuses to equate registry links with source-verified identities. The script checks that registry records are exactly the previously unresolved universe and that per-target partitions conserve records. The scientific cohort gate remains blocked. No final test set or new model checkpoint was produced.
