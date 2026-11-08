# BindingDB held-out-protein inner-dev: chemical novelty and controlled LR ablation

The provisional frozen component split contains 27,118 training pairs and 7,387 inner-development validation pairs. An independent train-only compound-lookup analysis found **7,227/7,387 validation pairs (97.834%) have a SMILES string absent from training**. The validation set therefore combines held-out protein components with near-complete exact-SMILES compound novelty. This is a much stronger and more complicated domain shift than a conventional protein-only holdout. It does not prove scaffold disjointness or lack of chemically similar analogues. Source/construct QC remains provisional.

## Actual training experiment (RTX 4060)

The previous DeepDTA training used AdamW lr=0.0003, weight decay 0.0001, train-only label normalization, seed 2103, 10 epochs, batch 128. A new controlled experiment changed **only learning rate** to 0.0001, retaining the identical split, model, seed, preprocessing and epoch budget. The experiment completed on GPU and saved its full history.

| Model | Epoch-10 RMSE | Best observed inner-dev RMSE | Train-mean comparator |
|---|---:|---:|---:|
| DeepDTA AdamW lr=0.0003 | 2.387794 | 2.224241 (epoch 6) | 1.803902 |
| DeepDTA AdamW lr=0.0001 | 2.344836 | 2.323641 (epoch 1) | 1.803902 |

Lowering learning rate improved the fixed epoch-10 RMSE by approximately 0.043 but **worsened the best observed inner-dev RMSE** and remained well behind the training-mean comparator. Do not promote this change as a model improvement. These exploratory validation looks are not an independent test.

## Simple train-only chemical lookup diagnostic

Only 160/7,387 validation pairs have a compound SMILES previously observed in training. Shrinkage of compound means toward the train-only global mean gave RMSE 1.802571 at pseudocount 20, versus 1.803902 for the global mean. This tiny gain is development-only and should not be overstated. It demonstrates that compound memorization alone is not a viable solution here.

## Next architectural priority

The current DeepDTA protein CNN truncates each protein to 1,000 residues and the molecular CNN truncates SMILES to 100 characters. Train-only vocab maps OOV characters to padding, and protein/chemical representations are randomly initialized. Evaluate pretrained representations and strict novelty controls under a predeclared hypothesis; do not use the reserved prospective test. Stronger sequence/protein features may matter, but the present data do not demonstrate they will improve accuracy.

All reported metrics are provisional because assay provenance and experimental constructs are not fully approved. The scientific gate remains intact.
