# Reconciled DAVIS label-stratified baseline audit

Read-only analysis of the separate 650-pair source-reconciled development subset. Compound means were computed from the 450 training rows only, then applied to 200 validation rows from four different proteins.

| Label category | Validation pairs | Pooled RMSE |
|---|---:|---:|
| Primary numeric Kd | 71 | 1.4474619807671647 |
| Primary screen-negative / weak binding | 129 | 0.35236313924633095 |
| All retained rows | 200 | 0.9076673153046052 |

Overall target-macro RMSE: 0.8365181844053747. All four targets contribute 50 rows each, but numeric Kd proportions differ (27, 31, 7, and 6). This uneven mixture materially affects the pooled and macro error interpretation. The baseline's low error on weak/negative-screening rows is not evidence of precise quantitative Kd prediction. Screen-negative cells are not exact measured Kd values, and these descriptive errors should not be used as the definitive scientific objective.

This analysis uses the existing repeatedly accessed development validation set. No family-disjoint holdout, construct verification, or clean neural retraining was performed. The input is verified by the SHA256 in the reconciled subset manifest. The source files and local generated data remain unmodified.

Reproduce: `python scripts/audit_reconciled_baseline_dev.py` and `python tests_v4/reconciled_label_stratification_test.py`.
