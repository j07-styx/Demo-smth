# Joint structure robustness across group partitions — 13 November 2026

ENGINEERING ONLY. Unchanged v5.7 joint ridge protocol, two additional outer partition seeds 4111 and 4112. The original seed 4110 is retained, not replaced. Same frozen TRAIN cohort, 5,808 rows and 253 groups. No reserved test access.

| Split seed | Sequence pooled | Joint pooled | Sequence macro | Joint macro |
|---|---:|---:|---:|---:|
| 4110 | 1.520691 | 1.521185 | 1.325041 | 1.314274 |
| 4111 | 1.503415 | 1.494821 | 1.312661 | 1.298202 |
| 4112 | 1.418623 | 1.421547 | 1.337387 | 1.327956 |

Structure improves macro point estimates on all three partitions; pooled accuracy improves on one. These are repeated views of the same development cohort, not three independent confirmations.

## Aggregation and uncertainty
Average squared errors across repeated predictions for each row, then compute pooled RMSE and group-macro RMSE. This is neither an arithmetic average of RMSE nor an ensemble of predictions.

| Arm | Repeated-loss pooled RMSE | Repeated-loss macro RMSE |
|---|---:|---:|
| Strong sequence baseline | 1.481581 | 1.335603 |
| Baseline + duplicate ESM block | 1.486348 | 1.337699 |
| Baseline + real SaProt block | 1.479785 | 1.325785 |
| Baseline + shuffled SaProt block | 1.493017 | 1.340193 |

Real minus sequence pooled delta -0.001797, conditional 95% paired group-bootstrap CI [-0.023460,+0.018970]; macro -0.009818 [-0.027651,+0.007313]. Real minus shuffled pooled -0.013232 [-0.030770,+0.002899]; macro -0.014408 [-0.030372,+0.001837]. All paired intervals include zero. Only 126/253 groups improve versus sequence after repeated-loss aggregation.

Bootstrap resamples 253 protein groups after averaging repeat losses, so repeats do not artificially inflate the sample size. It conditions on saved overlapping CV fits and does not account for the accumulated model-development search. All findings remain exploratory.

## What this means
A small macro signal is more consistent than the pooled signal. It is insufficient for a claim that the structure extension beats a strong sequence model, much less the original PerceiverCPI paper on matched benchmarks. The extra structure block is additive protein information, not demonstrated ligand-specific geometry.

Stop using additional reshuffles of this same cohort to seek a significant result. Preserve the candidate and baseline for a separately specified independent study; keep the sequence serving default. Any future architecture experiment should address a distinct missing input or hypothesis, such as verified binding-region information, and require a new evaluation plan.

## Reproduction and validation
Both joint evaluation scripts now accept --split-seed, default 4110, with all other settings unchanged. Run crossvalidate_joint_structure_dev.py for seeds 4111 and 4112, then summarize_joint_repeats_dev.py with --bundle-dir, --runs (all three result directories), and a fresh --out directory. Source scripts and per-fold aggregate results are versioned. Raw labels, predictions and model arrays stay outside Git.

validate_pretrained_cv_dev.py independently passed for each new repeat: all 5,808 rows exactly once, all 253 groups isolated to one evaluation fold, all metrics reproduced, and three deliberately invalid partitions rejected. Summary aggregation checks exact row ordering, finite predictions and distinct partition seeds. The original run is in research/joint_structure_probe_20261113.
