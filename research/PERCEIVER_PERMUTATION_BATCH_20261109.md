# Perceiver support-permutation repair and acceleration
Date: 2026-11-09. Reviewed current HEAD 061e932 and changes since 83d7051.

The repository now contains the completed negative TransferCPI study (6afe3a5), historical split retirement, separate BALM multi-seed exploratory comparisons, and a Perceiver-anchored equal-support KRR/geometry family evaluator. No Python training process was running at review. This change preserves those decisions and does not retrain retired cohorts.

## Fixed failure
PermutationGuardSettings accepts budgets up to 199, but five supports have only 119 nonidentity permutations. The former implementation raised on this valid setting. Explicit geometry min_support=3 also permitted support sizes whose finite null is smaller than the default 49.

The sampler now uses all available nonidentity permutations when the requested budget exceeds that number. The add-one numerator and actual denominator remain unchanged in definition. K=3 has smallest possible value 1/6 and cannot pass the default .05 threshold; this is appropriate finite-support resolution, not an exception. Default K<5 geometry fallback remains unchanged.

## Accelerated computation
Each leave-one-support-out kernel matrix is shared across all null permutations. One multiple-right-hand-side solve replaces three solves per permutation. Centering, geometry ridge, clipping, residual caps, support-only inputs and inference outputs retain their definitions. The scalar implementation remains as a reference.

Synthetic runtime benchmark, 20 repetitions, one BLAS thread:
| Support | Nulls | Old median ms | New median ms | Kernel speedup | Maximum MSE difference |
|---|---:|---:|---:|---:|---:|
| 5 | 49 | 15.741 | 0.319 | 49.37x | 2.22e-16 |
| 10 | 49 | 31.906 | 0.665 | 47.99x | 5.77e-15 |

This is a null-kernel speed improvement, not end-to-end model speed or affinity accuracy. Matrix solve calls drop from 735 to 5 at K=5 and from 1470 to 10 at K=10.

## Verification
Random positive-definite kernels, tiny/constant/large disagreements, clipping, scalar numerical parity, solve counts, finite permutation enumeration, valid K=5 high budget, K=3/4 overrides, and existing end-to-end family integration are covered. New tests use fabricated data only. Benchmark: scripts/benchmark_perceiver_permutation_batch.py; raw aggregate: research/perceiver_permutation_batch_benchmark_20261109.json.

No query labels, source approvals, historical weights, prospective test rows or model selection were changed.
