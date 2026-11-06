# Geometry contribution vs calibration: three-seed DAVIS engineering DEV

**NOT independent source-approved validation.** Checkpoint-selected development targets and repeated draws only.

S_B = sequence-only + calibration; G_B = sequence+geometry mixture + calibration; G_D = G_B + differential support correction.

| Seed | K | S_B RMSE | G_B RMSE | G_D RMSE | G_B - S_B | G_D - G_B |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1105 | 0 | 0.858202 | 0.861017 | 0.861017 | +0.00281508 | +0 |
| 1105 | 1 | 0.857979 | 0.860792 | 0.860792 | +0.00281305 | +0 |
| 1105 | 2 | 0.857802 | 0.860613 | 0.860613 | +0.00281125 | +1.869e-11 |
| 1105 | 5 | 0.857337 | 0.860139 | 0.860139 | +0.00280114 | +5.205e-11 |
| 1105 | 10 | 0.856572 | 0.859361 | 0.859361 | +0.00278906 | +1.036e-10 |
| 1105 | 20 | 0.854643 | 0.857389 | 0.857389 | +0.00274621 | +2.461e-10 |
| 1106 | 0 | 0.858202 | 0.856443 | 0.856443 | -0.00175958 | +0 |
| 1106 | 1 | 0.857979 | 0.856220 | 0.856220 | -0.00175826 | +0 |
| 1106 | 2 | 0.857802 | 0.856045 | 0.856045 | -0.00175714 | +1.542e-11 |
| 1106 | 5 | 0.857337 | 0.855587 | 0.855587 | -0.00175034 | +4.215e-11 |
| 1106 | 10 | 0.856572 | 0.854830 | 0.854830 | -0.00174216 | +8.593e-11 |
| 1106 | 20 | 0.854643 | 0.852930 | 0.852930 | -0.00171281 | +1.998e-10 |
| 1107 | 0 | 0.858202 | 0.855010 | 0.855010 | -0.00319253 | +0 |
| 1107 | 1 | 0.857979 | 0.854789 | 0.854789 | -0.00318986 | +0 |
| 1107 | 2 | 0.857802 | 0.854615 | 0.854615 | -0.00318755 | +2.065e-09 |
| 1107 | 5 | 0.857337 | 0.854164 | 0.854164 | -0.00317327 | +5.422e-09 |
| 1107 | 10 | 0.856572 | 0.853416 | 0.853416 | -0.00315630 | +1.056e-08 |
| 1107 | 20 | 0.854643 | 0.851547 | 0.851547 | -0.00309549 | +2.48e-08 |

Negative G_B - S_B indicates the geometry mixture beats sequence-only calibration on that same checkpoint-selected DEV cohort, NOT in any independent study.
G_D - G_B isolates the added differential support adapter after the geometry contribution is already in the base prediction.
The original 3-seed benchmark outputs were reproduced exactly to within 1e-6 RMSE.

Repeated draws are nested within four targets. Three initialization seeds are not independent proteins.
No scientific cohort approval, final BindingDB test, or code/weight updates occurred.
