# DynaCPI v4 — Differential correction inactivity (DEV ONLY)

**No scientific performance claim.** Derived from the four-target DAVIS development experiment using fixed checkpoints, no hyperparameter change.

| K | Mean W | W/(W+lambda_b) | Mean V | V/(V+lambda_theta) | D-B RMSE |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 0 | 0 | 0 | 0 | 0 | 0 |
| 1 | 0.0012401 | 0.00024796 | 9.2696e-40 | 9.2696e-39 | 0 |
| 2 | 0.002235 | 0.0004468 | 3.4507e-12 | 3.4507e-11 | 1.87e-11 |
| 5 | 0.0062813 | 0.0012547 | 1.1514e-11 | 1.1514e-10 | 5.21e-11 |
| 10 | 0.012388 | 0.0024716 | 2.5129e-11 | 2.5129e-10 | 1.04e-10 |
| 20 | 0.028842 | 0.0057353 | 6.5045e-11 | 6.5045e-10 | 2.46e-10 |

With lambda_b=5 and lambda_theta=0.1, the evidence scales are far smaller than regularization across K=1..20.
The differential estimator also has a tiny centered support disagreement covariance in its numerator. Ratios are not direct values of theta or delta.

**Next action:** Test sequence-versus-geometry complementarity, source-verified construct alignment and support coverage on independent approved development targets before tuning or redesigning. Preserve the negative result.

Source result SHA256: 73fd5e241b282e6e89c97df77ccf74d78e9b5bf8e238e16825e1c65eab79f746
