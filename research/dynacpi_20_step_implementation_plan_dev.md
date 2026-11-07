# DynaCPI 20-step implementation roadmap (development)

Objective: reproducible, scientifically defensible improvement on an independent, approved evaluation cohort. No promise of a win; report negative findings.

| Step | Task | Evidence required | State |
|---|---|---|---|
| 1 | Reproducible experiment registry | Unique run IDs, metrics, incomplete-run visibility, tests | COMPLETE |
| 2 | Leakage audit | Exact sequence/compound overlaps and documented family-leakage limits | PENDING |
| 3 | Protein-to-structure provenance | Graph integrity plus independent construct verification status | PENDING |
| 4 | Protein-family-disjoint split | Approved immutable split and disjointness proof | BLOCKED: approval/provenance |
| 5 | Affinity-label audit | Reporting floor and censoring policy | PENDING |
| 6 | Reproduce sequence baseline | Matching metrics on approved common cohort | PENDING |
| 7 | Gradient diagnostics | Per-component gradient norm and dead-path checks | PENDING |
| 8 | Structural sensitivity | Prediction shifts and readout sensitivity | PENDING |
| 9 | Matched-seed controls | Genuine, shuffled and disabled structure with same seed | PENDING |
| 10 | Train/validation divergence | Learning curves and early-stop analysis | PENDING |
| 11 | Normalized structural residual | Unit-tested bounded residual | PENDING |
| 12 | Compound-conditioned residue selection | Differentiable, tested selection module | PENDING |
| 13 | Cross-attention fusion | Tested compound/sequence/geometry integration | PENDING |
| 14 | Confidence-aware regularization | Ablation with geometry confidence and control | PENDING |
| 15 | Constrained backbone adaptation | Frozen vs selective tuning comparison | PENDING |
| 16 | Architecture ablations | Component contribution matrix | PENDING |
| 17 | Multi-seed reproducibility | Means, variability and effect sizes | PENDING |
| 18 | Independent evaluation | One-time evaluation on untouched approved holdout | BLOCKED: step 4 |
| 19 | Matched PerceiverCPI comparison | Identical data, metrics, splits and source references | BLOCKED: step 18 |
| 20 | Research release | Reproduction guide, results, limitations and paper draft | PENDING |

Step 1 result: `scripts/build_experiment_registry_dev.py` enumerates existing `pilot_*_dev/seed_*` run histories without touching datasets or checkpoints. At implementation time, 18 runs were indexed and 1 lacked a manifest. Local generated registry: `research/experiment_registry_dev.json` (not committed). Run `python scripts/build_experiment_registry_dev.py --output <new-path>` to regenerate without overwriting existing records; run `python tests_v4/experiment_registry_test.py` for verification.

All existing DAVIS geometry pilots are engineering-only; experimental construct identity and family-disjoint independent evaluation remain unresolved.
