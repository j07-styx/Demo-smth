# Completed DeepDTA + PerceiverCPI matched BALM development comparison

**2026-11-08 | Repeatedly inspected BALM inner DEV; NOT a prospective test result.**

All models share frozen original BALM TRAIN (15,538 raw pairs / 12,315 duplicate-mean collapsed) and original 3,891 DEV rows, 173 approximate 3-mer protein graph groups. There are six paired 10-epoch seeds (2103, 2601–2605) and two paired 30-epoch seeds (2601–2602). DeepDTA-inspired 1.94M parameter CNN and upstream PerceiverCPI ~4.67M parameter InteractionModel differ in input lengths and compute requirements. Epoch counts are not equivalent GPU-time budgets.

## Final epoch comparison (lower RMSE is better)

| Model | 10-epoch pooled | 10-epoch macro | 30-epoch pooled | 30-epoch macro |
|---|---:|---:|---:|---:|
| Locked Ridge + interaction booster | 1.383743 | 1.247098 | 1.383743 | 1.247098 |
| deepdta: mean over individual seed scores | 1.439208 | 1.336294 | 1.447531 | 1.319417 |
| perceivercpi: mean over individual seed scores | 1.512232 | 1.372680 | 1.589725 | 1.412739 |

## Paired 5,000-draw protein-group bootstrap deltas

| Comparison (A minus B) | Pooled RMSE delta [95% CI] | Macro RMSE delta [95% CI] |
|---|---|---|
| 10 ep: Locked vs DeepDTA final | -0.05546 [-0.11583, +0.00410] | -0.08920 [-0.13509, -0.04161] |
| 10 ep: Locked vs DeepDTA DEV-best optimistic | -0.00924 [-0.07790, +0.05206] | -0.06002 [-0.10201, -0.01646] |
| 10 ep: ESM+memory vs DeepDTA final | -0.05648 [-0.11029, -0.00040] | -0.09632 [-0.13723, -0.05381] |
| 10 ep: DeepDTA vs Perceiver final | -0.07302 [-0.14067, -0.01167] | -0.03639 [-0.09900, +0.02538] |
| 30 ep: Locked vs DeepDTA final | -0.06379 [-0.15401, +0.02283] | -0.07232 [-0.12279, -0.02117] |
| 30 ep: Locked vs DeepDTA DEV-best optimistic | -0.00608 [-0.05864, +0.04738] | -0.04094 [-0.08327, +0.00241] |
| 30 ep: ESM+memory vs DeepDTA final | -0.06480 [-0.15714, +0.02543] | -0.07944 [-0.12618, -0.03241] |
| 30 ep: DeepDTA vs Perceiver final | -0.14219 [-0.30479, -0.00235] | -0.09332 [-0.17761, -0.01176] |

**Negative deltas favor A.** A confidence interval crossing zero is inconclusive under this group bootstrap. Even an interval excluding zero does not correct repeated development-data inspection or guarantee new-cohort generalization.

## DeepDTA individual seed behavior

| Budget | Seed | Final pooled | Final macro | Best-dev epoch / pooled |
|---:|---:|---:|---:|---|
| 10 | 2103 | 1.447055 | 1.283269 | 9 / 1.380596 |
| 10 | 2601 | 1.432781 | 1.310894 | 5 / 1.413977 |
| 10 | 2602 | 1.467917 | 1.387723 | 4 / 1.421576 |
| 10 | 2603 | 1.404237 | 1.354704 | 5 / 1.377125 |
| 10 | 2604 | 1.488065 | 1.345944 | 4 / 1.369417 |
| 10 | 2605 | 1.395192 | 1.335228 | 10 / 1.395192 |
| 30 | 2601 | 1.416879 | 1.300522 | 26 / 1.384253 |
| 30 | 2602 | 1.478183 | 1.338311 | 12 / 1.395388 |

## Scientific qualifications and next gates

- Previous separate DeepDTA single-seed run achieved pooled DEV-best RMSE 1.371757 (epoch 8), numerically better than locked ensemble 1.383743, though DEV-selected epochs are optimistic. Preserve this counterexample.
- Current model family and hyperparameters were explored repeatedly on DEV. These comparisons are not independent significance tests. Best-DEV-epoch selection is explicitly labeled optimistic.
- Protein homology grouping uses an approximate 3-mer graph; subsequent exhaustive TRAIN Smith-Waterman alignment found cross-group related proteins. The original DEV split does not enforce Murcko scaffold exclusions.
- BALM affinity labels have missing assay DOI, method, and protein construct provenance, as well as contradictory same-input observations. Scientific cohort approval gate remains blocked.
- Full original paper training schedules and tuned computation-matched configurations of DeepDTA and PerceiverCPI were NOT reproduced. Do not claim paper-level architecture superiority.
- Frozen prospective test remained untouched. Obtain reviewed source/assay provenance, validated split, and registered analysis protocol before attempting test.

## Reproduction

Scripts: scripts/train_balm_deepdta_multiseed_matched_dev.py; scripts/compare_balm_deepdta_multiseed_matched_dev.py --epochs 10 or --epochs 30. Inputs: research/balm_deepdta_multiseed_dev_20261108/deepdta_seed*_ep*.json and equivalent PerceiverCPI seed files. Outputs: research/balm_deepdta_vs_perceiver_and_cpi_paired_dev_20261108_ep10.json and ep30.json. Integrity checks: tests_v4/balm_deepdta_multiseed_matched_test.py.

## Same-seed epoch-budget replay caveat

The 10- and 30-epoch DeepDTA jobs for seeds 2601 and 2602 used the same split, seed, initialization and hyperparameters. Their epoch-1 predictions matched exactly, but saved predictions diverged starting at epoch 2. The maximum 10-epoch prediction difference reached 2.03643 and 1.48081, respectively. Therefore these independently launched runs are separate stochastic trajectories, NOT verified identical training histories continued to epoch 30. The cause was not isolated; it should not be automatically attributed to CUDA. Full diagnostics: research/balm_deepdta_budget_replay_divergence_audit_20261108.json. Do not describe changes from 10 to 30 epochs as a pure training-duration causal effect.

Separately, the earlier standalone DeepDTA seed-2103 10-epoch run and this new multi-seed seed-2103 run differ slightly despite the same nominal seed. These findings reinforce that the observed neural variance and incomplete reproducibility must be disclosed.
