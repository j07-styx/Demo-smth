# Structural node-feature shuffling: negative controls on numeric Kd development cohort

Two paired engineering controls reran the same seed-2103 frozen numeric-only sequence checkpoint, 106 numeric Kd training rows, 71 numeric Kd validation rows, four fixed epochs. The control **permuted node scalar/vector features together within each graph**, leaving graph connectivity, edge features, residue indices, and protein identities unchanged. This is a partial correspondence-destruction control, **not** a fully randomized protein structure: graph topology and edge attributes remain authentic and may still leak structural signal. Deterministic permutation seed 20261107; isolated outputs and no original graph mutation on disk.

| Configuration | Real graph epoch-4 numeric pooled RMSE | Shuffled node features epoch-4 numeric pooled RMSE | Frozen sequence |
|---|---:|---:|---:|
| Unblocked low-gain attention (scale 0.1, lr 3e-4) | 1.021699271 | 1.021698984 | 1.021683942 |
| High-gain attention (scale 1.0, lr 1e-3) | 1.064493019 | 1.035332558 | 1.021683942 |

Low-gain differences are tiny; its apparent graph contribution is functionally negligible at this metric scale. High-gain models react differently but both underperform the frozen sequence baseline. **No evidence of useful real-geometry advantage.** The high-gain real and shuffled runs share the same initialization and seed but only one run each. Because this development validation has been repeatedly inspected and is not family-disjoint, do not interpret these as independent research benchmarks.

The upstream initialization problem was separately confirmed by a regression test: nonzero initialization of both geometry and attention projections restores gradient flow, but that alone does not create a useful structural predictor. Further structural experiments should test an explicit no-geometry control and assess matched training-protein-only selection rather than trying arbitrary gains on repeatedly observed validation.
