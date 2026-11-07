# Fresh reconciled sequence model: matched-seed label objective experiment

Six independently initialized four-epoch SequenceFoundation training runs completed on the source-reconciled DAVIS **development** subset: seeds 2103, 2104 and 2105, each with mixed-label training (450 pairs) and numeric-Kd-only training (106 pairs). Architecture, optimizer, epoch budget, initialization seed within each pair, and 200-row development validation cohort were matched. Different training set sizes are intrinsic to this objective comparison. The evaluation below uses **predeclared epoch 4**; no validation-selected checkpoint.

| Seed | Mixed-label numeric-Kd RMSE | Numeric-only numeric-Kd RMSE |
|---|---:|---:|
| 2103 | 1.565499 | 1.021684 |
| 2104 | 1.638813 | 1.050245 |
| 2105 | 1.619371 | 1.016093 |
| Mean | **1.607894** | **1.029341** |
| Sample standard deviation | 0.037980 | 0.018318 |

These scores refer to the **71 measured numeric-Kd validation pairs**, not the full mixed-label benchmark. The compound-average baseline on these pairs is 1.447462 RMSE. Numeric-only neural training beats both the mixed-label neural training and the compound-average baseline on this repeatedly used development numeric subset for all three matched seeds. This is a replicated development signal about the **training objective**, not evidence of superior 3D architecture or independently validated generalization. Screening-negative/weak-binding observations are not exact numeric Kd labels, and numeric-only training does not solve their prediction. The cohort is not family-disjoint, and source constructs remain unverified.

Reproduce by running `scripts/train_reconciled_{mixed,numeric}_sequence_seed_{2103,2104,2105}_dev.py sequence` in fresh isolated output folders; `python scripts/compare_matched_label_seeds_dev.py` summarizes the saved epoch-4 predictions. Checkpoints and data are local and excluded from Git.

Next: a fixed-protocol matched-seed comparison of numeric-only sequence against numeric-only geometry, with frozen pre-specified epochs and per-target numeric error. Do not tune against the already inspected development validation cohort.
