# DynaCPI KRR-first geometry guard: an explicit stronger-baseline hypothesis

**9 November 2026 | No approved binding-affinity experiment | Synthetic engineering only**

## Why this branch exists

Original PerceiverCPI remained stronger than the earlier TransferCPI architecture replacement in the five-epoch provisional development experiment. Subsequent source audit invalidated the old provisional split for scientific claims. Our previous Perceiver-anchored D5 design used support-calibrated PerceiverCPI as its base; an adversarial **fabricated** eight-family example correctly revealed that a support-aware PerceiverCPI *kernel ridge* (P5-KR) could beat D5.

This checkpoint changes the model-performance strategy: **start from the strongest same-support P5-KR predictor, then add geometry only if the very same support panel gives evidence that geometry is better.** No new neural backbone, no additional measured affinity information and no optimization on the protected test. This is a proposed model, not a claim that it beats real PerceiverCPI.

## Implemented new inference-only model

`dynacpi/perceiver_krr_geometry_guard.py` exposes `compare_krr_geometry_with_support_validation(...)`. It uses the original `perceiver_equal_support_controls.py` module for **exact** P5-KR predictions, with fixed stereo-aware Morgan-Tanimoto^4 chemistry kernel and the same K assay-compatible support measurements.

For support residuals `r_i = y_i - Perceiver(i)`, geometry disagreement `d_i = FrozenGeometry(i) - Perceiver(i)`, and chemical kernel matrix `K`:

1. For each support compound, temporarily leave that compound out. On the other K−1 samples, fit the fixed-regularization original chemical KRR and a geometry-augmented residualized KRR. Compare the two predictions on only the withheld **support** compound.
2. Estimate LOO mean-squared error of both methods. If geometry fails to improve support LOO error by at least a fixed relative and absolute margin, set **geometry gate=0**.
3. If support LOO advantage is positive, shrink the final geometry update by its fractional LOO gain (bounded [0,1]). Fit the geometry residual coefficient on all K support compounds and evaluate the query using **only** frozen Perceiver and frozen geometry predictions.
4. The chemical KRR baseline is always unchanged. The geometry term is capped to ±0.5 pKd, and structure absence, K<5 or near-constant disagreement trigger exact KRR fallback.

The geometry coefficient is residualized against the chemical kernel and its disagreement values are centered. This targets geometry's **incremental** information after the same-support chemical KRR, rather than counting global calibration as a geometry gain. These prototype hyperparameters are unapproved and must be frozen from permitted development data *before* any independent future evaluation.

No query labels are accepted in the module interface. The estimator uses pretrained/frozen prediction numbers only. It does not load any experimental data or fit a neural model.

## Noise-stress experiment (fabricated, never measured CPI)

`scripts/stress_perceiver_krr_guard_synthetic.py` generated **128 fictional trials per scenario**, with 5 or 6 same-assay synthetic support compounds, invented query labels, and known generated geometry signal strength. The separate geometry-shuffled negative control was also tested at identical support budget.

| Fabricated scenario | K | Perceiver KRR RMSE | KRR+geometry RMSE | KRR+shuffled geometry RMSE | Geometry gate active |
|---|---:|---:|---:|---:|---:|
| Geometry genuinely contributes to manufactured labels | 5 | 0.572994 | **0.486068** | 0.573997 | 128/128 |
| Geometry genuinely contributes to manufactured labels | 6 | 0.461030 | **0.400476** | 0.461648 | 128/128 |
| Geometry has no relationship to manufactured labels | 5 | 0.275628 | 0.275212 | 0.276460 | 28/128 |
| Geometry has no relationship to manufactured labels | 6 | **0.279612** | 0.279909 | 0.279859 | 23/128 |

These are **not measurements from any assay or downloaded dataset**; their success in the known-signal branch follows from the deliberately planted relationship between synthetic geometry and invented labels. The tiny null-case changes are noise, **not evidence of improvement or inferiority in CPI**.

The null scenarios expose an important limitation: with just five support observations, the leave-one-out geometry gate can respond to random correlations roughly **22%** of the time (K=5; 28/128). K=6 produced ~18% false activations (23/128). **The gate is not a guarantee of safety or out-of-sample improvement.** Research next should add a source-independent, support-only permutation-calibrated null test or stronger preregistered guard; judge any guard with truly held-out tasks rather than tuning it to this fabricated noise benchmark.

## Evidence and model selection rules

The current comparison is **P5-KR versus KRR+geometry with identical frozen predictions and K support labels**. The experiment design needs both KRR+shuffled geometry and zero-geometry controls. On a future source-review-approved, protein-homology-disjoint, fixed split: compare K=0,5,10 where available, macro-aggregate by *independent original source family*, paired source-family bootstrap, pooled RMSE and MAE, and multiple held-out frozen predictor seeds. Direct geometric/sequence ablations and true protein-structure availability remain independent checks.

Do not fit or select the neural backbone, thresholds, support panels, source families or residual corrections using the previous repeatedly inspected inner-DEV as if it were unseen, or any reserved prospective TEST records. The existing separate family-clustered evaluator supports the previous seven arms; **this new KRR-guarded arm is not yet wired into that formal evaluator**, and must not be advertised as benchmark-ready until aligned score records and guard-negative controls are added.

## Files and integrity

- `dynacpi/perceiver_krr_geometry_guard.py`: frozen two-expert KRR extension with support-only leave-one-out reliability gate.
- `tests_v4/perceiver_krr_geometry_guard_test.py`: synthetic baseline-preservation, no-geometry/K0/K1–4 fallback, constant disagreement, calibration-only, permutation, cap and metadata identity tests.
- `scripts/stress_perceiver_krr_guard_synthetic.py`: completely invented chemistry-episode labels; fixed seed and deterministic test design; refuses to overwrite output.
- `tests_v4/perceiver_krr_guard_synthetic_stress_test.py`: pure synthetic stress and public report integrity checks.
- `research/perceiver_krr_guard_fabricated_noise_stress_20261109.json`: aggregate **fabricated** results only, no private source-family hashes, original assay rows, held-out scores or model checkpoints.

**Scientific approval remains `BLOCKED_UNAPPROVED_NOT_TRAINING_READY`.** No user/private affinity training, no independent measured superiority, no changed original provisional split and no reserved-test outcomes were inspected.
