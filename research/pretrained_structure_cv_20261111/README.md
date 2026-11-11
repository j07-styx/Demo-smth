# Nested group cross-validation — 11 November 2026

ENGINEERING ONLY. This stronger follow-up does not reproduce v5.3's encouraging single-holdout advantage. All data come from the frozen BALM TRAIN bundle; the reserved test was not read.

| Arm | Out-of-fold pooled RMSE | Group-macro RMSE |
|---|---:|---:|
| Shared ridge baseline | 1.556304 | 1.362221 |
| ESM-2 sequence | 1.548379 | 1.335627 |
| Real SaProt | 1.569070 | 1.345643 |
| Shuffled SaProt | 1.561716 | 1.341636 |

## Frozen comparison
Five outer folds use shuffled sorted groups (seed 4110), round-robin assignment. All 5,808 rows across 253 groups appear in exactly one evaluation fold. Each outer training partition repeats the original three-fold inner selection over scales {0,.1,.3,1}; same ridge, features, PCA/SVD dimensions, confidence/length covariates and model caches as v5.3. Every fitted transform and target statistic uses fit rows only. Zero scale permits exact shared-baseline fallback. No new hyperparameters were selected using outer outcomes.

This is a single exploratory outer partition of an already inspected TRAIN cohort, not an independent scientific test. Protein grouping follows the existing bundle; no new homology/domain audit was performed.

## Paired results and concentration
Real minus ESM-2: pooled +0.020691, CI [-0.019755,+0.060261]; macro +0.010016, CI [-0.021456,+0.040960].
Real minus shuffled: pooled +0.007354, CI [-0.048137,+0.069316]; macro +0.004007, CI [-0.028848,+0.039342].
Real minus shared baseline: pooled +0.012766, CI [-0.059291,+0.095815]; macro -0.016578, CI [-0.059830,+0.028102].
All 95% intervals cross zero. Bootstrap resamples paired protein groups over saved OOF predictions; overlapping training fits and development selection mean these are conditional descriptive intervals, not full retraining uncertainty or confirmatory significance.

Real SaProt beats ESM-2 on pooled RMSE in only 1/5 folds and improves 122/253 groups. Against shuffled features it wins pooled RMSE in 4/5 folds but improves only 122/253 groups and loses in aggregate. The five largest absolute group SSE differences account for 38.4% of total absolute difference versus ESM-2 and 42.5% versus shuffled.

The large reversal is zero-based fold 3: baseline 1.568627, ESM-2 1.701908, real SaProt 1.755689, shuffled 1.591824. Inner tuning chose scale 1.0 for both real SaProt and ESM-2 and .3 for shuffled. Real SaProt's inner macro score was 1.325907 at scale 1 versus 1.334467 at .3. This suggests that a modest tuning gain may not transfer across protein groups. It does not establish scale choice as the cause; no alternative scale was evaluated on that outer fold after observing its failure.

## Implication for the 3D diagnosis
The old inert branch is no longer the only issue: pretrained structure features change representations and predictions, but do not reliably improve generalization. Frozen whole-protein mean pooling can discard local binding information; this remains a hypothesis, not an isolated result. SaProt vs ESM-2 also confounds pretraining. The shuffled-token arm is potentially out of distribution.

Do not call this a successful GenSPARC replication, claim all 3D models fail, or use the previous 4.78% single-holdout reduction as a headline. Preserve both outcomes. The next discriminating work is a predeclared readout ablation (protein-only pretrained block versus compound interaction products) and conservative inner-only regularization, before any more expensive residue-level architecture. Any adaptation after these results remains exploratory; the reserved test should remain locked.

## Validation and reproduction
scripts/validate_pretrained_cv_dev.py independently verifies exactly-once row coverage, one-fold-per-group membership, and all aggregate metrics. It rejects duplicate rows, missing rows and cross-fold group contamination. scripts/evaluate_pretrained_structure_dev.py now also checks cached feature hashes against provenance and fit/eval group separation.

Run scripts/crossvalidate_pretrained_structure_dev.py with --bundle-dir, --features, --out NEW_DIR. It launches the unchanged evaluator with --outer-fold 0 through 4, then aggregates all OOF predictions. Existing output directories are rejected. Runtime uses two CPU math threads; no GPU training or unrelated processes were stopped. Original model and demo defaults are untouched.

Aggregate JSON, fold protocols, selection scores and validation are versioned here. Raw prediction arrays and labels stay in the original workspace outside Git.
