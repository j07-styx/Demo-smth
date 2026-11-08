# DynaCPI support-only permutation guard: harder test of KRR geometry

**9 November 2026 | Engineering and fabricated-data evidence only**

## Problem and new hypothesis

The earlier KRR-anchored DynaCPI prototype keeps original PerceiverCPI's chemical kernel-ridge (KRR) adapted prediction intact and adds a bounded geometry correction if geometry appears to improve leave-one-support-out (LOO) prediction. Its original synthetic stress produced **28/128** false geometry activations with K=5 and **23/128** with K=6 even when geometry carried no label signal. The support panel is too small to trust a positive LOO improvement by itself.

We added a **second, support-only null test**. It asks whether the observed geometry LOO improvement is larger than improvements obtainable by reassigning *the same frozen geometry–Perceiver disagreements across the K support compounds*, while holding fixed the chemical KRR kernel, support affinities and original Perceiver predictions.

This is a new **inference-only proposed model**, not a verified CPI benchmark, scientific approval or discovery of an actual predictive advantage.

## Implementation

`dynacpi/perceiver_krr_support_permutation_guard.py` wraps the existing `compare_krr_geometry_with_support_validation(...)` in a separate function `compare_krr_with_support_permutation_guard(...)`.

1. Produce the identical original Perceiver P5-KRR support-adapted prediction and existing LOO-based KRR+geometry candidate, using **only K support labels** and two pre-frozen predictor caches. The original gate must first be positive.
2. Generate 49 **unique, nonidentity** support-disagreement permutations, deterministically seeded by a fixed public seed, task and assay keys, and *sorted support compound identifiers only*. No affinities, query labels, reserved split roles or test outcomes influence the permutation selection.
3. Recompute geometry-augmented support LOO MSE for each permutation, without changing the fixed chemical KRR baseline or any support label. The diagnostic uses the add-one permutation tail fraction `(1 + number of null LOO gains >= observed LOO gain) / (49 + 1)`.
4. The geometry candidate is accepted only when this fraction is **at most 0.05** *and* the earlier LOO gate passed. Otherwise the returned prediction is **exactly Perceiver P5-KRR**. The original ±0.5 pKd geometry cap is retained.

The output preserves original KRR, original geometry candidate, new guarded prediction, original gate, null tail fraction, permutation count, and acceptance flag. The null is computed only when the original LOO gate activates. K=0–4, missing geometry, constant geometry disagreement or no LOO advantage fall straight back to KRR without computing null permutations.

The null is based on *reassigning support disagreements*, **not** shuffling query labels or actual 3D molecular coordinates. Chemical similarity, support membership, geometry availability, baseline predictions, and the information budget are invariant.

**Statistical limitation:** the exchangeability needed for an exact randomization-test interpretation may be false if geometry disagreement depends on chemical similarity, series or assay bias. A low support-permutation tail fraction is only a *heuristic* for reliability—not a valid scientific significance claim or guarantee of held-out accuracy. 49 permutations give a minimum attainable add-one fraction of 0.02. We have not calibrated it against a scientifically approved source-family-independent cohort.

## Reproducible synthetic stress

The independent `scripts/stress_perceiver_krr_permutation_null_synthetic.py` reuses the identical **128 fabricated replicates per scenario** from the previous stress, with known planted/no geometry signal, synthetic noise SD 0.15, an invented constant assay shift and K=5 or K=6.

| Deliberately fabricated scenario | K | Original LOO gate activated | New permutation guard accepted | Perceiver-KRR RMSE | Old LOO+geometry RMSE | New permutation-guarded RMSE |
|---|---:|---:|---:|---:|---:|---:|
| Planted geometry signal | 5 | 128/128 | **72/128** | 0.572994 | 0.486068 | **0.520084** |
| Planted geometry signal | 6 | 128/128 | **111/128** | 0.461030 | 0.400476 | **0.406785** |
| No geometry signal | 5 | 28/128 | **6/128** | 0.275628 | 0.275212 | 0.275448 |
| No geometry signal | 6 | 23/128 | **6/128** | 0.279612 | 0.279909 | 0.279838 |

**What these fabricated outcomes demonstrate:** the added null check reduces false gate activations (under this deliberately constructed noise scenario) from 21.9% to 4.7% at K=5 and from 18.0% to 4.7% at K=6. It retains a useful planted geometry correction in 56.3% of K=5 trials and 86.7% of K=6 trials. The stricter gate sacrifices genuine-signal sensitivity, especially at K=5, while keeping synthetic RMSE lower than Perceiver-KRR in planted-signal cases. Under the null, the accuracy differences remain tiny, variable and uninformative about real binding prediction.

These trials are repeated noise draws over the **same eight synthetic small molecules and made-up geometry pattern**. They are not independent protein families, publications or target-binding assays; the activation fractions are **not validated real-world false-positive rates**. No choice of the null threshold was fitted using query labels from a real evaluation cohort.

## Reproducibility and next scientific work

- `dynacpi/perceiver_krr_support_permutation_guard.py`: opt-in 49-shuffle support-only reliability gate, preserves original Perceiver-KRR and exact fallback.
- `tests_v4/perceiver_krr_support_permutation_guard_test.py`: artificial positive/negative, K=0–4, absent geometry, support order invariance, cache integrity, deterministic seed, paired baseline and tail-score invariants.
- `scripts/stress_perceiver_krr_permutation_null_synthetic.py`: same fabricated scenarios as previous guard stress; never overwrites its output.
- `tests_v4/perceiver_krr_permutation_stress_test.py`: synthetic reproducibility, strong-baseline preservation, null-false-trigger reduction and public artifact safety checks.
- `research/perceiver_krr_support_permutation_fabricated_stress_20261109.json`: aggregate fake-data results only.

This support-only gate is **not yet integrated into the separately developed seven-arm source-family evaluator**. The scientific advancement we still require is independently reviewed publication/construct identity, a source-family- and homology-disjoint approved cohort, and a preregistered comparison on identical query/support panels against P5-KRR and appropriate shuffled-geometry, no-geometry and sequence-only controls. Prespecify bootstrap clusters at independent source-family level; do not tune the guard on reserved TEST outcomes.

**Scientific cohort status: `BLOCKED_UNAPPROVED_NOT_TRAINING_READY`. No new real affinity training, independent held-out evaluation or experimental PerceiverCPI victory has occurred.**
