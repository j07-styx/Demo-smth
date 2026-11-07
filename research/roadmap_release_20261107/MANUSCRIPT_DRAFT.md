# Bounded residue fusion fails to establish geometry-specific gains in a small DynaCPI development cohort
Research manuscript draft — engineering evidence only, not ready for submission.

## Abstract
We investigated whether a bounded compound-conditioned residue readout could overcome attenuated gradients in an existing structure-augmented affinity predictor. Eighteen controlled runs on a nine-protein training and four-protein validation cohort compared six configurations across three seeds. Real structural features reduced target-macro RMSE from 0.925685 to 0.921045 on average, but a sequence-only residual reached 0.920612 and a training-only compound mean reached 0.839873. Results do not establish geometry-specific value or independent generalization.

## Introduction
Perceiver CPI integrates compound and protein representations using nested cross-attention [1]. Our extension explores structural information within a frozen sequence foundation. We ask whether gains survive sequence-only and disrupted-structure controls, rather than assuming that architectural complexity implies useful biology.

## Methods
The engineering cohort, transformations, full architecture, matched controls, seeds, optimizer settings, checkpoint selection and exact metrics are specified in REPORT.md. Local scalar structure features and rotation-invariant vector norms are fused with projected frozen ESM-derived sequence representations; no graph message passing is used in the new readout. Output corrections are bounded. We retain the frozen baseline as an epoch-zero candidate. Model selection and evaluation here use the same development validation set.

## Results
Real-structure mean RMSE was 0.921045 (sample SD 0.001718); sequence-only residual mean was 0.920612 (SD 0.001778). Shuffled structures achieved 0.921663 (SD 0.003075). Real structure was worse than sequence-only on each matched seed. Two validation proteins improved and two worsened. A descriptive target bootstrap interval for real-minus-frozen RMSE spans zero. Selective final-layer tuning never improved over epoch zero. All 18 saved checkpoints replayed within 0.000002 affinity units. The original GVP probe showed zero early-layer gradients at initialization followed by extremely small nonzero gradients.

## Discussion
The direct residual removes an indirect readout bottleneck but does not establish that geometry adds useful information. Compound means substantially outperform these neural variants, exposing the weakness of using only the frozen neural model as comparator. The geometry subset is small, its chemistry overlaps across splits, and its affinity floor is common. No causal conclusion about the usefulness of all protein structure follows from this negative result.

## Limitations
Experimental constructs and censoring semantics remain incompletely verified. No frozen family-disjoint independent holdout is available. Seeds reuse the same four validation targets and are not independent biological replicates. Bootstrap intervals are descriptive after model selection. The sequence control is not active-parameter matched. Confidence weighting removal is not complete removal of confidence metadata. The archived Perceiver comparison is a local three-epoch implementation, not a reproduction of published benchmark scores.

## Conclusion
This study supports retaining simpler baselines and repairing the evaluation foundation before promoting a geometry extension. It provides working software and falsifiable negative results, not a claim of a state-of-the-art model.

## Data and code availability
Source and aggregate reports are versioned on the dynacpi-v4 branch. Raw local records, caches and checkpoints are excluded from publication. Reproduction requires the recorded input hashes and existing local environment.

## References
[1] Nguyen et al. Perceiver CPI. https://pmc.ncbi.nlm.nih.gov/articles/PMC9848062/
[2] Davis et al. Comprehensive analysis of kinase inhibitor selectivity. https://pubmed.ncbi.nlm.nih.gov/22037378/
