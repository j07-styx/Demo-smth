# Low-rank compound-protein interaction head: matched-seed negative result

Implemented an opt-in `BilinearSequenceFoundation` with rank-32 projected compound/protein representations, elementwise product, layer normalization, and a small additive prediction residual (scale 0.1). This tests a lightweight explicit cross-modal interaction head without requiring 3D structural graphs. Base `SequenceFoundation` remains unchanged.

Three fresh independent training runs (seeds 2103, 2104, 2105), four fixed epochs each, use the exact same source-reconciled numeric-only training cohort (106 measured numeric-Kd pairs), optimization and validation cohort (71 measured numeric-Kd pairs) as the matched-seed original SequenceFoundation experiments. Reported metric is numeric-Kd validation pooled RMSE at **predeclared epoch 4**. The scripts' legacy all-200-row pooled metrics mix screening-negative proxy labels with numeric-Kd and are **not** the metric used below.

| Seed | SequenceFoundation numeric-Kd RMSE | BilinearSequenceFoundation numeric-Kd RMSE |
|---|---:|---:|
| 2103 | 1.02168394 | 1.02762679 |
| 2104 | 1.05024488 | 1.05481641 |
| 2105 | 1.01609269 | 1.04700607 |
| Mean | **1.02934050** | 1.04314976 |

**Decision:** Do not promote the bilinear head. It underperforms the original sequence architecture on all three development seeds. The cohort is small, not family-disjoint, repeatedly inspected, and lacks an independently frozen test set; these are engineering findings, not a published PerceiverCPI benchmark comparison.

Next priority is source-verified independent evaluation, with no additional architecture selection against this development split.
