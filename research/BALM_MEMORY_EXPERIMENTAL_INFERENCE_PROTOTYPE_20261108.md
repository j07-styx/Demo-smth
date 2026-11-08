# Executable experimental DynaCPI memory model: SMILES + protein sequence inference

**Date:** 2026-11-08. **Status:** runnable LOCAL RESEARCH PROTOTYPE only; supervised model fit solely on frozen BALM TRAIN. The formal scientific cohort approval gate remains BLOCKED, and no independent validation/test labels were accessed by this prototype training process.

## What was built

A reusable trained model and command-line inference path, not only a notebook or benchmark table:

1. **Chemical encoder:** chiral Morgan radius-2 2048-bit L2-normalized fingerprint for each compound.
2. **Protein encoder:** training-fold 3/4-mer TF-IDF features, plus **frozen pretrained ESM2 t6 8M 320-dimensional pooled vector** for each protein. For a novel protein not found in the 639 training sequence hashes, infer its embedding on GPU (or CPU) using the same frozen model weights; sequences longer than 1,022 amino acids use the first 1,022 residues.
3. **Regularized Ridge:** fixed alpha 1 on chemical, 0.25-scaled protein TF-IDF and 0.25-scaled ESM2 representation; training targets standardized with fit-only mean and SD. Predictions are rescaled to source label units.
4. **Shallow nonlinear booster:** HistGradientBoostingRegressor on 21 RDKit molecular descriptors and 21 amino-acid composition/length features, fixed 160 iterations, learning rate .05, max 15 leaf nodes, depth 5, minimum leaf samples 50, L2 15.
5. **Affinity memory:** top **64** most similar protein–compound training pairs, with similarity weights = positive Morgan cosine squared times positive ESM protein cosine to the power 8. Weighted TRAIN-only labels shrink 50% toward the unique-pair TRAIN label mean. If no neighbors have positive weight, fallback to that mean.
6. **Output combination:** base = 0.75 Ridge + 0.25 booster; final experimental score = 0.75 base + 0.25 shrunk affinity memory. This full-TRAIN demo uses beta=1.0 (no additional shrinkage of base), consistent with most previously nested inner-cold folds. Choosing a fixed beta on the full dataset is NOT independently validated.

The model fit over **15,538 original TRAIN records**, averaged to **12,315 unique protein/SMILES pairs** using the original BALM labels. There are **639** distinct TRAIN protein sequences. Fit-only mean label = 6.387780 and SD = 1.438339.

The fitted model was serialized to the user's local Windows research environment as:
data/models/balm_affinity_memory_prototype_exploratory_20261108.joblib

Checkpoint size about **8.13 MB** and SHA256 recorded in research/balm_affinity_memory_research_inference_manifest_20261108.json. Binary checkpoint, raw TRAIN labels, pretrained model weights and ESM cache stay LOCAL and are deliberately **not pushed to GitHub**.

## Reproduce / run on authorized Windows system

In the DynaCPI project directory, use the existing virtual environment:

    .\.venv\Scripts\python.exe -m scripts.predict_balm_affinity_memory_research_dev --smiles "CCO" --sequence "YOUR_VALID_PROTEIN_SEQUENCE_HERE"

Replace the placeholder sequence with a real, plain amino-acid sequence at least 20 residues long (letters from the 20 standard amino acids or X). For a sequence stored in a plain text file, use:

    .\.venv\Scripts\python.exe -m scripts.predict_balm_affinity_memory_research_dev --smiles "CCO" --sequence-file "my_protein_sequence.txt"

Do NOT include a FASTA header in that file. The research CLI returns JSON with the predicted SOURCE p-affinity-like label, Ridge/booster/memory component values, nearest compound fingerprint cosine, nearest ESM protein cosine, and whether protein N-terminal truncation occurred. It does NOT claim the estimate is a validated physical Kd, confidence interval, experimental measurement, or assay-specific affinity.

Rebuild the exploratory local checkpoint (after deliberately archiving prior checkpoint and manifest; the training script refuses accidental overwrite):

    .\.venv\Scripts\python.exe -m scripts.train_balm_affinity_memory_research_prototype_dev

Load joblib checkpoints only from trusted sources: joblib serialization uses pickle semantics.

## Functional verification completed

- Three TRAIN-row inference-smoke predictions were recorded in the manifest as functionality checks, **not an accuracy evaluation**. 
- A previously unseen **synthetically single-residue-mutated protein** was successfully encoded with frozen ESM2 on the RTX 4060 and passed through the full predictor, yielding finite source label estimate **5.789845** for example ethanol SMILES. This is a synthetic capability smoke, NOT biological validation.
- The CLI itself succeeded on a local known-sequence example with a finite source label output **5.807003** for ethanol; no heldout label was used.
- Unit and report tests cover source cache/checkpoint SHA, TRAIN-only sample count, input validation, prediction determinism and architectural coefficients.

## Why this architecture was chosen (and what was NOT established)

Previous TRAIN-only stricter SW alignment-group and Murcko scaffold-cold experiments found the similarity-memory branch improved pooled out-of-fold RMSE over the earlier no-memory ensemble at **both 30% and 40% protein-alignment identity thresholds**:

| Protein grouping | Previous ensemble pooled RMSE | + 64-neighbor joint memory pooled RMSE |
|---|---:|---:|
| 40% identity, 80% shorter coverage | 1.430266 | **1.399824** |
| 30% identity, 80% shorter coverage | 1.460624 | **1.420606** |

Both observed paired group bootstrap intervals for the change versus earlier ensemble excluded zero for pooled RMSE. However, **the direct protein-aware vs chemical-only memory effect was not statistically separable** at either threshold, and *both* new pooled mean-baseline comparisons still had confidence intervals crossing zero. This is exploratory development history, not confirmatory benchmark superiority.

## Non-negotiable limitations

- BALM BindingDB_filtered source records lack per-example original experimental assay DOI, method, construct metadata and measurement conditions. Same protein/compound input labels sometimes disagree by >=1 log unit.
- Alignment groups approximate homology by local Smith–Waterman identity and shorter-sequence coverage, not independently verified functional homology/orthology. Murcko exclusions do not guarantee complete analog disjointness.
- Most model design and weights follow repeatedly inspected exploratory TRAIN and development experiments. Group-bootstrap intervals do not correct this research choice multiplicity.
- The prototype's checkpoint is fit on the full TRAIN partition and has only TRAIN-row smoke checks. Those are NOT independent generalization metrics. The reserved 5,271-row prospective test remains untouched.
- Source p-affinity scores are heterogeneous and are NOT assay-harmonized physical Kd measurements.
- The scientific cohort approval gate remains BLOCKED_UNAPPROVED_NOT_TRAINING_READY; this prototype must not be presented as validated research, clinical or screening-grade inference.

Source code: dynacpi/balm_memory_predictor_dev.py, scripts/train_balm_affinity_memory_research_prototype_dev.py, scripts/predict_balm_affinity_memory_research_dev.py. Research-only manifest: research/balm_affinity_memory_research_inference_manifest_20261108.json. Tests: tests_v4/balm_affinity_memory_inference_test.py.
