# BALM low-rank explicit compound–protein interaction: train-CV-selected development experiment

## Method

- Public BALM BindingDB provisional source: **12,315 unique training protein-compound pairs**, **3,891 unaggregated inner-development observations**. Held-out protein groups use the existing frozen protein 3–4-mer similarity graph; this is not a verified alignment-based homology split.
- Morgan radius-2 chiral fingerprints (2048 bits), L2-normalized; training-fold fitted protein TF-IDF character 3–4-mer representation (up to 4096 features) scaled by 0.25.
- **New architectural feature**: fit separate rank-16 truncated SVD representations for molecules and proteins **on training only**, normalize each, then generate the 16 × 16 = **256-dimensional explicit outer-product interaction**. Fit Ridge on both additive and interaction features, using training-only label standardization.
- Three training-only protein-group-held-out folds; select alpha from [1, 10] and interaction coefficient from [0, 0.25, 1] with mean-fold pooled and macro RMSE, normalized by the mean-baseline values.
- Only after selection, fit the full training split and evaluate exploratory frozen inner-development. **No reserved test outcomes accessed.**

## Results

| Model | Frozen inner-dev pooled RMSE | Protein-group macro RMSE |
|---|---:|---:|
| Training-only global mean | 1.589844 | 1.464093 |
| Additive Morgan+protein Ridge alpha1, no interaction | **1.405092** | 1.269216 |
| Train-CV selected interaction Ridge alpha1, interaction coefficient 0.25 | 1.410125 | **1.257924** |
| Stronger interaction Ridge alpha1, interaction coefficient 1.0 (diagnostic only) | 1.423299 | 1.249413 |

Training CV selected alpha1, interaction scale0.25 with mean fold pooled RMSE **1.313563** and macro RMSE **1.167497**. The selected interaction improves macro RMSE by **0.011293 (~0.89%)** over matched additive Ridge but worsens pooled RMSE by **0.005033 (~0.36%)**.

Interpretation: interaction learning carries some protein-group-level signal, but pooled predictive superiority **was not established**. Comparing to the stronger interaction scale1 on the same dev is descriptive only; it was not the train-CV selected option.

## Limitations

The BALM source has unresolved assay-context and construct provenance; protein grouping is an approximate trigram proxy; training-group folds overlap; the exploratory inner-dev has been inspected repeatedly. These development results are not independent tests and cannot justify paper-level superiority claims. The prospective test remains quarantined.
