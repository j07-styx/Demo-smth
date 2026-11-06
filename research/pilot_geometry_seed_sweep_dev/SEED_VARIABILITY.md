# DynaCPI v4 — GVP seed sensitivity (development only)

**Not an independent held-out test.** Same 9-train/4-validation structure-mapped DAVIS pilot targets, two epochs, fixed parameters.

| Seed | Best epoch | Sequence RMSE | Geometry RMSE | Geometry − sequence |
| ---: | ---: | ---: | ---: | ---: |
| 1105 | 1 | 0.925685 | 0.935921 | +0.010236 |
| 1106 | 2 | 0.925685 | 0.920050 | -0.005635 |
| 1107 | 1 | 0.925685 | 0.915971 | -0.009714 |

Mean best-epoch difference across three seeds: -0.001705 RMSE.
Sample SD: 0.010540.
Two seeds are lower-error than the frozen sequence predictor, one higher-error on *these exact development targets*. This is initialization sensitivity, not evidence of generalizable gain.

Next: check whether fixed A/B/C/D differential adaptation becomes identifiable with these alternate geometry checkpoints, without changing support/query identities or regularizers. Leave any source-approved test untouched.
