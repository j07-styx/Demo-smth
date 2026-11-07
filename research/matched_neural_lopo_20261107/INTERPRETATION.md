# Matched neural experiment: 81 fits

Nine held-out training target identifiers x three seeds x three feature modes, 300 full-batch updates each: 24,300 optimizer steps. Fixed final epoch, no hyperparameter search or validation scoring. All 106 numeric training observations are held out once per seed/mode. CPU execution avoided an already busy GPU.

| Model | Mean seed/target RMSE | Final standardized training MSE |
|---|---:|---:|
| Chemical Tanimoto kernel | 0.8540 | not measured here |
| Neural, zero protein inputs | 0.9098 | 0.587025 |
| Neural, real protein inputs | 1.0224 | 0.000359 |
| Neural, deranged protein inputs | 1.0616 | 0.000094 |

The real-protein head worsens RMSE relative to its matched zero-protein ablation by 0.1126, target-bootstrap interval [0.0361, 0.1930]. Only two of nine targets improve. All three seed-level averages worsen. Compared with the kernel, the difference is +0.1685, interval [0.0946, 0.2403]. Real versus deranged features gives -0.0391, interval [-0.1523, 0.0623].

Near-zero training loss with both real and deranged protein features, coupled with worse held-out predictions, indicates overfitting in this compact head. Arbitrary distinct target embeddings support training-set memorization. This does not prove protein features are useless. The head is a diagnostic Morgan/mean-ESM network, not the existing SequenceFoundation; no claim about matched superiority over that architecture is made.

## Reusable baseline implemented

`dynacpi/tanimoto_regressor.py` provides validated fit/predict/save/load operations and versioned JSON artifacts. It explicitly ignores protein identity. The exporter checks all nine historical fold scores (maximum discrepancy 4.44e-16), then fits the 106 numeric training rows. Saved artifact: `data/development_models/numeric_chemical_tanimoto_20261107.json`. This remains a local development comparator, not a deployed predictor or source-approved scientific model.

Tests verify held-out-label independence by changing query labels to 99999, deterministic fitting, train-loss decrease, analytic ridge solutions, binary feature validation, overwrite protection and save/load prediction parity. All 38 training compound fingerprints independently match regenerated RDKit features.

Decision: retain the chemical comparator and existing sequence checkpoint; do not promote either new protein head. Broader verified training targets are needed before pursuing further high-capacity architecture selection. Nine identifiers are not nine independent protein families; repeated development use, numeric-only ascertainment and unverified constructs limit conclusions. No test split or source approval was changed.
