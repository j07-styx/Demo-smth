# DAVIS primary-screening floor: hypothetical inequality sensitivity

A **hypothetical**, not assay-validated, alternative to treating screening-negative/weak-binding benchmark code 5 as an exact numeric pKd is to penalize only predictions above 5: `max(0, prediction - 5)^2`. The 71 numeric Kd observations retain squared error. The published source's screening-negative/weak-binding semantics have not been shown to justify this bound for every blank cell; this is a sensitivity exercise, **not a benchmark**.

On the 129 screening-negative development validation rows, the train-only compound-average model exceeds 5 for 87 rows; the archived sequence checkpoint exceeds 5 for all 129. Consequently, for these two particular predictors, the hypothetical one-sided hinge errors equal their existing squared errors on the screening-negative rows. Numeric-Kd RMSE remains 1.447462 (compound-average) versus 1.641753 (archived sequence). The hypothetical combined RMSE is 0.907667 versus 1.012486, respectively.

The lack of a changed ranking does **not** validate the floor assumption. It shows only that this one-sided transformation cannot distinguish these two predictors on the present screening-negative rows, because their predictions are not below the code floor. Future modeling requires explicit primary assay reporting semantics, source-verified construct and chemical identity, and a held-out cohort. Do not use this score for tuning.

Reproduce: `python scripts/sensitivity_floor_inequality_dev.py` and `python tests_v4/floor_inequality_sensitivity_test.py`.
