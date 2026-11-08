# Matched multi-seed PerceiverCPI baseline vs locked BALM ensemble (2026-11-08)

**STATUS: IN PROGRESS. No win has been established. Read the "Decision rules" before interpreting any number.**

## Why this exists
On the frozen BALM BindingDB cold-protein inner-dev split (3,891 rows, 173 protein groups) the
single existing upstream PerceiverCPI run (seed 2103, 10 epochs) scored pooled 1.450 / macro 1.293
(final epoch) and 1.432 / 1.291 (best epoch picked on dev). The locked ridge+explicit-interaction
ensemble scored 1.384 / 1.247 (see BALM_EXPLICIT_INTERACTION_ENSEMBLE_POSITIVE_DEV_20261108.md).
That gap is suggestive only: PerceiverCPI had ONE seed and its per-row predictions were not saved,
so no paired uncertainty could be computed. This work removes both gaps.

## What was added (all dev-only; the reserved 5,271-row test is NOT touched)
- `scripts/train_balm_perceivercpi_multiseed_dev.py --seed S --epochs E`: unchanged upstream
  PerceiverCPI on the identical train/dev rows, optimizer and schedule as
  `train_balm_bindingdb_upstream_perceivercpi_10epoch_dev.py`; saves per-row dev predictions for
  EVERY epoch; runs behind `scripts/gpu_lease.py`. Output:
  `research/balm_perceiver_multiseed_dev_20261108/perceiver_seed{S}_ep{E}.json`.
- `scripts/save_balm_ensemble_dev_predictions.py`: refits the ALREADY-LOCKED ensemble on TRAIN only and
  saves dev predictions (`research/balm_ensemble_dev_predictions_20261108.json`). The model choice is
  read from the existing report (`ridge_interaction_blend_0.25`); nothing is re-selected.
- `scripts/compare_balm_perceiver_vs_ensemble_dev.py [--epochs E]`: paired protein-group bootstrap
  (5000 draws, seed 20261108, seeds averaged inside each draw). Verifies dev-row SHA256 equality.
- `tests_v4/balm_paired_bootstrap_test.py`: 4 synthetic checks (zero delta for identical models, negative CI
  for a clearly better model, metric parity, reproducibility). Passing.

## Runs launched (background, serialized by the GPU lease)
1. Perceiver seeds 2601-2605, 10 epochs (~9 min each on the RTX 4060 laptop GPU).
2. Perceiver seeds 2601-2602, 30 epochs (robustness: the earlier note warned 10 epochs may underfit,
   so a stronger baseline schedule must also be beaten before any claim).
Logs are `*_LOCAL.log` in the output folder (not committed).

## Decision rules (fixed BEFORE results were seen)
- PRIMARY comparison: locked ensemble vs PerceiverCPI FINAL epoch of each seed. No dev-based epoch choice.
- OPTIMISTIC comparison: PerceiverCPI best-dev epoch per seed (favours PerceiverCPI; reported, not primary).
- A dev-level "win" is claimed ONLY if the PRIMARY 95% bootstrap interval for BOTH pooled and
  group-macro RMSE lies entirely below zero (delta = ensemble - perceiver) AND the 30-epoch
  baseline does not reverse the sign. Otherwise report it as inconclusive/negative. Do not hide it.
- The dev split has been inspected many times, so even a dev win is not a test result. If, and only
  if, the rule above is met: lock model choice, seeds and epoch rule, then score the reserved test
  ONCE with both systems and report whatever comes out.
- DeepDTA best dev (~1.372 pooled) is still below the ensemble; any paper claim must include it.

## To finish (next model: start here)
```
.venv\Scripts\python.exe -m scripts.compare_balm_perceiver_vs_ensemble_dev            # 10-epoch, needs 5 seed files
.venv\Scripts\python.exe -m scripts.compare_balm_perceiver_vs_ensemble_dev --epochs 30  # needs 30-epoch seed files
```
Then add the observed numbers (including negatives) to this file and commit. Stage files explicitly;
other sessions also commit in this repo. Push only to remote `demo`, never `origin` (upstream PerceiverCPI).

## Honest scope
This compares a lightweight Ridge/boosting ensemble to a deep model under a strict cold-protein split. It
supports a benchmarking statement ("simple similarity-based models are competitive under cold-protein
splits"), not a claim that a new deep architecture beats PerceiverCPI. BALM lacks per-record assay
provenance and the protein grouping is an approximate k-mer graph, not verified homology.
