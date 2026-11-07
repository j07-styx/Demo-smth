# Centered compound-conditioned geometry: mechanism diagnostics (development only)

Seed **1125**, fixed selected DAVIS engineering cohort (486 training and 216 validation pairs). This is not an independent scientific benchmark. Baseline validation target-macro RMSE: **0.9256850780053539**.

| Epoch | Covered-residue gate mean | Token residual RMS | Mean absolute prediction shift (label units) | Geometry target-macro RMSE |
|---|---:|---:|---:|---:|
| 1 | 0.02921070 | 0.00008443 | 0.0000009433 | 0.9256854390 |
| 2 | 0.02938569 | 0.00049671 | 0.0000105891 | 0.9256890632 |
| 3 | 0.02947772 | 0.00111376 | 0.0000252397 | 0.9256946087 |
| 4 | 0.03003035 | 0.00323753 | 0.0001379698 | 0.9257365800 |
| 5 | 0.03179282 | 0.00418341 | 0.0004258286 | 0.9258448493 |

Early stopping at epoch 5; best epoch 1. Covered-residue gate means are batch/pair-weighted and exclude uncovered residues; token residual RMS and prediction shifts are batch/pair-weighted, not globally pooled squared errors. The gate starts near sigmoid(-3.5)=0.0293 and stays close to that value. The geometry residual grows during training but validation error worsens.

**Interpretation:** Geometry corrections barely influence frozen-sequence predictions at the selected checkpoint. Later epochs amplify prediction changes while worsening validation performance. The experiment does not isolate whether this comes from poor structural features, limited data, frozen readout sensitivity, or gate initialization.

**Next:** Inspect per-protein prediction deltas and gradients; compare structurally informed vs shuffled-geometry controls on an independently verified cohort. Avoid claims of improved generalization.

Local checkpoint/history: `research/pilot_compound_conditioned_geometry_centered_diagnostics_dev/seed_1125/` (not committed).
