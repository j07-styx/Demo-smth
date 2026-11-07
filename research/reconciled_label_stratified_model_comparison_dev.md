# Reconciled DAVIS: archived sequence versus compound-average by label kind

The archived frozen sequence checkpoint was scored against a train-target-only compound-average baseline on the **same 200 filtered development validation pairs**. No new model training was performed; the sequence checkpoint predates the chemical identity reconciliation and therefore cannot be considered a cleanly trained model on this subset.

| Source label kind | N | Sequence pooled RMSE | Compound-average pooled RMSE |
|---|---:|---:|---:|
| All rows | 200 | 1.0124856914085334 | 0.9076673153046052 |
| Numeric Kd | 71 | 1.6417527175626958 | 1.4474619807671647 |
| Screening-negative / weak-binding | 129 | 0.3253556680214338 | 0.35236313924633095 |

The sequence model performs better on screening-negative/weak-binding rows but worse on the 71 numeric Kd rows. This is **not evidence** that the neural model is intrinsically better at negative screening, because screening-negative rows are not exact quantitative Kd observations. Numeric-only RMSE is descriptive and sensitive to subset selection; a scientifically defensible objective must account for assay semantics and censoring, with independent validation.

Reproduce: `python scripts/compare_reconciled_label_strata_dev.py` (read-only). Original data, checkpoints and local predictions remain unchanged.
