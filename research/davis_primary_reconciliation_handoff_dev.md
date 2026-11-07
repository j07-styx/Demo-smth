# DAVIS primary-source reconciliation: resumed handoff

The local primary-source audit reports a CID 4908365 identity conflict: benchmark JNJ-7777120 (C14H16ClN3O) differs from primary-study JNJ-28312141 parent (C26H32N6O2). Source evidence is retained locally under `data/audit/davis_primary_20261107/`; source PDF locator is physical page 15, Supplementary Table 2.

A separate name-and-label-reconciled engineering subset under `data/engineering_pilot_primary_reconciled_20261107/` contains 650 pairs (450 train, 200 validation), 50 compounds, and excludes 52 pairs across four unresolved or mismatched compounds. Of the retained labels, 473 correspond to screening-negative/weak-binding cells and 177 to numeric Kd cells; blank screening cells are not exact quantitative affinities.

The previously trained sequence checkpoint scores target-macro RMSE 0.9268938221392184 on this filtered development validation cohort; the training-only compound-average baseline scores 0.8365181844053746. The checkpoint was trained on legacy data including excluded entries, so these are filtered diagnostics, not clean retraining. Kinase group STE appears in both train and validation. There is no approved independent holdout or verified construct-disjoint split.

The original pilot remains untouched. `scripts/build_primary_reconciled_pilot_dev.py` is one-shot and refuses to overwrite its output directory. Source files, PubChem caches, generated data and predictions remain local and are not included in Git.

Next: verify unresolved chemical identities and experimental constructs; define a defensible family-disjoint cohort; distinguish screening negatives from measured affinities; then retrain matched baselines. Do not claim neural superiority from current development metrics.
