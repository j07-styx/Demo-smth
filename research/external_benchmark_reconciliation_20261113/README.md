# Corrected benchmark status — 13 November 2026

## Conclusion
The existing sequence-based LowRankDynaCPI v5 system in the separate dynacpi-better-version backend already beats the tested original PerceiverCPI implementation on pooled and target-macro RMSE in all SIX completed KIBA/Metz held-out comparisons. Four comparisons have descriptive paired-cluster intervals wholly favoring DynaCPI on both metrics.

Earlier statements in this chat that we had not established any win against PerceiverCPI were too broad. They described the new BALM structure probes, not the separate completed external benchmark program. This document reconciles the two research lines; it does not claim a new training improvement.

## Audited completed results
| Dataset / split | Dyna pooled | Original pooled | Dyna macro | Original macro | Both paired intervals favor Dyna |
|---|---:|---:|---:|---:|---|
| KIBA protein cold | 0.608841 | 0.694440 | 0.647370 | 0.753914 | Yes |
| KIBA compound cold | 0.646767 | 0.814341 | 0.668404 | 0.808298 | Yes |
| KIBA double cold | 0.810435 | 0.926680 | 0.745177 | 0.863034 | Yes |
| Metz protein cold | 0.735788 | 0.772058 | 0.751161 | 0.777072 | No |
| Metz compound cold | 0.781367 | 0.804360 | 0.748509 | 0.764061 | No |
| Metz double cold | 0.890669 | 1.018738 | 0.885922 | 1.058008 | Yes |

Lower is better. KIBA and Metz have different label definitions; do not compare their absolute RMSE values to each other. Both systems use two-seed ensembles on matching observed test rows per scenario. Descriptive bootstrap intervals are not corrected for multiple comparisons, nor proof of universal performance.

## Integrity verification performed now
scripts/reconcile_external_benchmarks_dev.py reads already-completed aggregate JSON only and hashes protected files as opaque bytes. It verifies:
- source-feature and split hashes against frozen training and test records;
- pair partition disjointness and held-out row counts;
- all 24 recorded model checkpoint hashes;
- raw prediction-file and exported held-out CSV hashes, without parsing values;
- bootstrap linkage to original result/prediction hashes;
- complete-suite aggregate consistency, metric differences and MSE/RMSE arithmetic.

All six pass. No models retrained, no test rescoring, no raw held-out values parsed, no serving changes. Audit output is results.json alongside this file. Historical November 11 backend prose lists three tests as pending; the completed all-six aggregate is newer and authoritative for current completion status.

## What the wins mean
Supported: better same-split held-out performance than the tested unmodified PerceiverCPI runs under our recorded experimental protocol.

Not supported: reproducing and exceeding every published PerceiverCPI table on exactly its original folds; architecture-only improvements under equal protein pretraining; universal superiority; gains attributable to 3D or expert routing.

The winning system uses frozen ESM-2 650M protein features, Morgan fingerprints, a training-derived chemical-neighbor affinity prior and a low-rank two-tower residual. It has no 3D encoder or expert routing. The official baseline was pinned at 755f076ef51099a90332fd1ec8437f94e3750c0b and trained for 30 epochs. The upstream README gives a 150-epoch example; our runs are not an exact reproduction of all published optimization budgets. Source: https://github.com/dmis-lab/PerceiverCPI

Protocol amendment: all six DynaCPI selections were frozen before external testing, but not all 12 original checkpoints had completed before the first scenario was scored. Each scenario's original checkpoints were selected before its own one-time test. The existing records disclose that scheduling amendment; it must remain in publications.

## Research paths and next decision
1. Use these completed sequence-model comparisons as the current performance evidence. Preserve original checkpoint selections and all six test outcomes.
2. Keep the BALM 3D experiments separate: modest exploratory macro signals, no confirmed independent geometry advantage. Their reserved test remains untouched; these are different tests from the already completed KIBA/Metz program.
3. For an exact published-benchmark claim, obtain and verify original source variants, fold identities, label processing, model-selection rules and full baseline budget before running a new matched study. Different folds cannot be fixed by comparing only numerical RMSE.
4. For architectural attribution, predeclare controls that separate ESM pretraining, chemical-neighbor priors and the learned residual on training/validation only. Any newly adapted model needs new independent evaluation; these exposed six tests must not become tuning targets.
5. Do not spend another 3D sweep trying to create a claim the existing sequence model already supports more directly.
