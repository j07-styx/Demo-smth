# DynaCPI v4 — Three geometry seeds, fixed support adaptation

**Development only, not independent family generalization.** Geometry checkpoint selected on the same four DAVIS development proteins.

| Geometry seed | K | B macro RMSE | D macro RMSE | D−B | Mean V |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 1105 | 0 | 0.86101741 | 0.86101741 | 0 | 0 |
| 1105 | 5 | 0.86013856 | 0.86013856 | 5.21e-11 | 1.15e-11 |
| 1105 | 20 | 0.85738896 | 0.85738896 | 2.46e-10 | 6.5e-11 |
| 1106 | 0 | 0.85644275 | 0.85644275 | 0 | 0 |
| 1106 | 5 | 0.85558708 | 0.85558708 | 4.21e-11 | 1.1e-11 |
| 1106 | 20 | 0.85292993 | 0.85292993 | 2e-10 | 6.13e-11 |
| 1107 | 0 | 0.85500981 | 0.85500981 | 0 | 0 |
| 1107 | 5 | 0.85416415 | 0.85416416 | 5.42e-09 | 1.1e-09 |
| 1107 | 20 | 0.85154725 | 0.85154728 | 2.48e-08 | 6.1e-09 |

The geometry branch is sensitive to training seed, but geometry-informed differential support correction is almost zero in all three predeclared seed trials. Results are fixed-regularizer engineering observations; no scientifically approved Kd test has been performed.
