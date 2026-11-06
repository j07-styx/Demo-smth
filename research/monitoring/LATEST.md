# DynaCPI v4 — local benchmark monitor

Updated (UTC): 2026-11-06T03:28:03.137112+00:00

**Status:** ENGINEERING ONLY. No scientifically approved BindingDB cohort or frozen protein-group split.

**GPU:** NVIDIA GeForce RTX 4060 Laptop GPU, 397, 8188, 0

**Last consolidated regression check:** 20/20; status PASS_ENGINEERING_ONLY

**Scientific gate:** BLOCKED_UNAPPROVED_NOT_TRAINING_READY

**Scientific source review:** 30 tasks unreviewed; 0 approved; 30 access records indexed (metadata only).

**Construct-to-reference alignment flags:** 2 source-located tasks needing physical construct verification; 0 approved by this check.

**30-task metadata triage (not approval):** P0_REVIEW_METADATA_SEMANTICS=4, P1_REVIEW_CONSTRUCT_AND_ENDPOINT=12, P2_STANDARD_PRIMARY_SOURCE_REVIEW=14.

| Support K | Calibration B RMSE | Full D RMSE | D−B RMSE | Mean kernel W | Mean disagreement V |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 0 | 0.86101741 | 0.86101741 | 0 | 0 | 0 |
| 1 | 0.86079179 | 0.86079179 | 0 | 0.0012401133 | 9.2696196e-40 |
| 2 | 0.86061335 | 0.86061335 | 1.8695046e-11 | 0.0022349736 | 3.4506788e-12 |
| 5 | 0.86013856 | 0.86013856 | 5.2050586e-11 | 0.0062813437 | 1.1514249e-11 |
| 10 | 0.85936112 | 0.85936112 | 1.0356305e-10 | 0.012388401 | 2.5129096e-11 |
| 20 | 0.85738896 | 0.85738896 | 2.4608127e-10 | 0.028841821 | 6.5044579e-11 |

This is a same-four-target development diagnostic and does not show independent cold-family improvement.

## Geometry training seed variability (DEV only)

| Seed | Best epoch | Geometry minus sequence RMSE |
| ---: | ---: | ---: |
| 1105 | 1 | +0.010236 |
| 1106 | 2 | -0.005635 |
| 1107 | 1 | -0.009714 |

## K20 B-versus-D by geometry seed (DEV only)

| Seed | B RMSE | D RMSE | D−B |
| ---: | ---: | ---: | ---: |
| 1105 | 0.8573890 | 0.8573890 | 2.46e-10 |
| 1106 | 0.8529299 | 0.8529299 | 2e-10 |
| 1107 | 0.8515473 | 0.8515473 | 2.48e-08 |

Changed watched artifacts since prior run: data/audit/v4_validation_suite.json
