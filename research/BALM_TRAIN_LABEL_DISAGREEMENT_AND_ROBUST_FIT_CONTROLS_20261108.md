# BALM training-label disagreement audit and robust fit controls — 2026-11-08

**Scope:** Frozen BALM BindingDB_filtered TRAIN-only protein/compound and labels, 15,538 records. **Status:** exploratory quality audit plus predeclared training-only controls. No original inner-development or prospective test labels, sequences, or predictions accessed.

## Problem: repeated identical inputs have substantially different labels

Canonicalize compounds with RDKit isomeric canonical SMILES and define a repeated input by exact protein SHA256 plus canonical compound. Stereoisomers remain distinct.

| Attribute | BALM TRAIN |
|---|---:|
| Original rows | 15,538 |
| Unique protein/canonical compound inputs | 12,315 |
| Inputs with >=2 records | 1,305 |
| Rows inside repeated-input groups | 4,528 |
| Maximum copies of one input | 27 |
| Median within-group label range (repeated groups) | 0.706 log-affinity units |
| Repeated inputs with label span >=0.5 units | 774 |
| Repeated inputs with label span >=1 unit | **462** |
| Original rows in repeated groups with span >=1 unit | **2,542 (16.4%)** |
| Repeated inputs with span >=2 units | 152 |
| Repeated inputs with span >=3 units | 38 |
| Largest observed within-input span | 6.317 units |

**Important:** Identical protein/compound inputs need not represent identical measurements. Binding assay, target construct, buffer, temperature, assay method and original source publication were not retained in this third-party reference dataset. The observed differences might include legitimate assay heterogeneity, not just measurement error. This audit alone cannot identify which labels are correct or exclude them scientifically.

## Matched TRAIN-only sensitivity experiment

For both alignment-derived group thresholds, local Smith-Waterman protein identity >=30% or >=40%, coverage >=80% of shorter sequence, run fixed four GroupKFold outer folds. Apply the same strict RDKit Bemis–Murcko scaffold exclusion in every outer fit. All acyclic compounds share one empty-scaffold group. Models only fit TRAIN rows remaining after the corresponding heldout protein groups and scaffold cores are excluded. Original outcome Y is scored on all 15,538 heldout TRAIN rows exactly once across folds.

Compare the **same ESM2-augmented 75% protein k-mer + pretrained ESM2/Morgan Ridge and 25% ordinary joint RDKit descriptor/protein-composition booster**, with previous inner-train-selected shrinkage betas inherited unchanged. Three training-only label treatments:

1. **Original:** Average repeated exact protein/raw SMILES training labels, preserving all training inputs; current baseline.
2. **Robust median:** Median instead of mean on repeated exact protein/raw SMILES training labels, preserving all training inputs.
3. **Exclude discordant:** For each outer training fold only, remove the *entire protein+canonical-isomeric-SMILES group* when repeated log-affinity labels span >=1.0 unit, then mean-collapse remaining exact protein/raw SMILES repeats.

The 1.0 threshold was chosen as a clear predeclared sensitivity setting based on this TRAIN-only distribution audit, **not** selected to optimize a development/test score. It is NOT an independently validated biological filtering threshold.

### Alignment 40% / shorter coverage 80% (396 heldout alignment groups)

| Training label treatment | Out-of-fold pooled RMSE | Component-macro RMSE |
|---|---:|---:|
| Original mean collapsed | **1.430266** | **1.337548** |
| Median collapse | 1.433885 | 1.338730 |
| Exclude span >=1.0 | 1.435159 | 1.340964 |

Median-minus-original pooled delta +0.003619, 5,000 group-bootstrap 95% interval [-0.000999,+0.009518]; macro delta +0.001182, interval [-0.002163,+0.004732]. Exclusion-minus-original pooled delta **+0.004893**, interval **[+0.000092,+0.009428]**, worsening pooled error under this descriptive bootstrap. Exclusion macro delta +0.003416, interval [-0.001330,+0.008136] (uncertain).

### Alignment 30% / shorter coverage 80% (271 heldout alignment groups)

| Training label treatment | Out-of-fold pooled RMSE | Component-macro RMSE |
|---|---:|---:|
| Original mean collapsed | **1.460624** | 1.379023 |
| Median collapse | 1.462247 | 1.377390 |
| Exclude span >=1.0 | 1.462525 | **1.374911** |

Median-minus-original pooled delta +0.001623 (CI [-0.001455,+0.004064]) and macro delta -0.001633 (CI [-0.005140,+0.001910]). Exclusion-minus-original pooled delta +0.001901 (CI [-0.005567,+0.006332]) and macro delta -0.004112 (CI [-0.010296,+0.002319]). **All these paired intervals include zero**, so the small macro improvements are not conclusive.

## Decision

**Keep original mean aggregation as the exploratory reference.** Neither blanket deletion of all inputs with >=1-unit span nor median aggregation demonstrated a reliably better cold-start model across the two alignment rules. Removing high-variance training labels does not automatically resolve assay heterogeneity, and filtering based on mixed-assay spread can discard informative records. There was no change to the saved source dataset and no deletion of any original record.

The rigorous next step is to recover original provenance-backed Kd-only records with assay/source DOI, method and protein construct information, or find a curated benchmark with those fields. Such source reconciliation must be independently reviewed before approving the scientific cohort and using the reserved prospective test. The current scientific cohort gate remains blocked.

## Reproduction and constraints

- TRAIN-only audit: scripts/audit_balm_train_affinity_replicate_disagreement_dev.py, result research/balm_train_only_affinity_replicate_disagreement_audit_20261108.json.
- Robust training ablation: scripts/ablate_balm_sw_alignment_affinity_disagreement_train_dev.py --group-rule identity40_cover80; repeat with identity30_cover80.
- Results: research/balm_sw_identity40_cover80_affinity_disagreement_training_ablation_dev.json and identity30_cover80 counterpart.
- Tests: tests_v4/balm_train_affinity_disagreement_test.py and tests_v4/balm_sw_affinity_disagreement_report_test.py.
- Original pretrained ESM2 vectors and weights remain a local training-only cache, with fingerprints and extraction protocol in research/balm_esm2_t6_8m_train_only_feature_manifest_dev.json.
- Intervals are descriptive 5,000 bootstrap resamples of approximate protein alignment groups. Threshold choice, previous development inspection and correlated groups mean the intervals are **not independent confirmatory hypothesis testing**.
- No attempt was made to bypass the formal scientific source/split approval gate, train on reserved test labels, or claim DynaCPI outperforms PerceiverCPI.
