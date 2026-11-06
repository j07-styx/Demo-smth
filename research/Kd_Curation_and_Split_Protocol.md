# DynaCPI v4 — Kd data eligibility and protein-group split protocol

**Status:** DRAFT / PRE-SPLIT. Do not use this document as evidence that an assay or a target construct has been approved. Latest local checkpoint: 5 November 2026.

## Research question

Does a small target-specific support set provide evidence that changes the incremental usefulness of reliable protein geometry beyond calibration-only adaptation? Evaluate the DynaCPI v4 sequence predictor and geometry-enhanced predictor with the same support observations and independent protein groups.

## Required data provenance

Source is the November 2026 full BindingDB export, archived under `data/bindingdb_202611` with local ZIP CRC and SHA-256. The main endpoint is **experimentally verified Kd**, converted from nM using `pKd = 9 - log10(Kd_nM)`. Ki, IC50, EC50, KIBA scores and generic potency estimates are ineligible for pooled exact-Kd regression unless treated as explicitly separate endpoints.

An exact-looking numeric Kd field is **not proof** of an experimentally exact dissociation constant. Source record qualifier, measurement technique, assay description, target/construct, and potential inferred or derived measurements require review. Preserve raw source IDs, qualifiers, article/patent identifiers, original target sequence, and all recorded assay conditions. Do not upgrade a bound to an exact observation.

## Human-review gate (fail closed)

The metadata-only review sheet is `data/audit/bindingdb_assay_manual_review_queue_30_ENRICHED.csv`. It contains thirty review targets from distinct preliminary protein components selected without affinity labels. It has NOT been adjudicated.

A reviewer must record an identity, review date, source or publication evidence, and a substantive reason. Approval requires explicit YES for:
1. the experimental protein construct/variant matches the sequence and reported target;
2. source evidence supports the Kd measurement's exact/qualified semantics;
3. the support and query observations within the assay task are comparable.

Unknown or missing information is not silently treated as success. Missing pH/temperature is a review flag, not automatically proof of incompatibility. Conflicting replicate values require source review; median aggregation is a technical convenience, not a license to collapse incompatible assays.

`scripts/validate_assay_reviews.py` verifies review declarations and rejects tampering with copied metadata. **Review declarations still require independent scientific audit.** An approved cohort manifest and frozen split are separate subsequent milestones.

## Compound and protein identity

Use RDKit canonical isomeric SMILES for preliminary identity checks; implement and document a chemically justified parent/salt and stereochemistry standardization policy before final benchmark release. Keep duplicates and replicate provenance. Do not silently merge molecular forms.

Confirm sequence-to-assay construct alignment with accession, mutations, domains and chain identity. Full-length canonical sequences cannot be substituted for experimental mutants. For structural variants, map N/CA/C/O positions and missing residues exactly, and treat low-coverage or mismatched structures as unavailable.

Cluster **all eligible protein constructs** using connected-component grouping of MMseqs2 local matches at a predeclared initial threshold of >=30% aligned identity covering >=80% of the shorter sequence. Domain-homology sensitivity checks are required; the current 4,157-sequence screen is preliminary and can miss similarities. Keep all assays from the same protein component within one experimental role.

## Episode identity and leakage control

For each approved construct-assay task, require >=15 distinct compounds for the primary K=5 / 10-query protocol. Use candidate support sizes 0, 1, 2, 5, 10 and 20 only where enough eligible compounds exist. Select support and query identities without using affinity labels or model predictions. Never reveal query labels to predictors, routers, support encoders or hyperparameter tuning. Support may contain only approved observations from the same task/assay. Test labels stay evaluator-only.

`dynacpi/episode_data.py` enforces the task-specific prediction input boundary; `tests_v4/episode_data_real_manifest_test.py` checked 4,961 preliminary episodes without cross-assay support or query-label exposure. This software test is not scientific eligibility.

Cross-assay repetitions of an identical compound are common: an identity-only scan found 114 multi-assay sequences sharing compounds across tasks. Similar compound identities in different assays do not prove identical measurements. Prevent labels for held-out queries from becoming training or adaptation inputs via another task. Apply the same leak policy to all competing models.

## Final split protocol (after approval ONLY)

Intended five roles: base train 60%, base validation 10%, adapter training 10%, adapter validation 10%, final test 10%, partitioned by **protein components**, not independent pair rows. The task count can be extremely imbalanced: the largest preliminary component held 492 K=5 tasks. Balance role task counts using predeclared label-blind constraints while preserving component exclusivity, and report cohort composition.

`dynacpi/group_split.py` provides a deterministic **dry-run** group allocator; `tests_v4/group_split_dryrun_test.py` validates component exclusivity and label rejection. Do not promote its preliminary output to a final split. Freeze final role assignments, dataset hashes, inclusion policy, and preprocessing before examining held-out test labels or results.

## Outcome metrics and primary comparison

Use task-wise RMSE, averaged first within construct and then equally across independent protein clusters. Report MAE, rank correlation, per-task harm, calibration and target/component counts separately. All variants see identical support/query episodes; report K=0 and K=5 prominently.

The primary contrast is v4 geometry differential adaptation versus an identical calibration-only support adapter with frozen sequence and geometry predictors. Match tuning and capacity where applicable. Require a preregistered meaningful effect (initial proposal >=2% relative target-cluster RMSE reduction) and a paired cluster-bootstrap 95% interval excluding zero. Three training seeds and at least ten fixed support draws are planned; statistical power depends on independent clusters, not total pair count.

## Current exact state

Full archive downloaded and ZIP-CRC verified. Preliminary candidate tasks, support/query identity checks, reference checkpoint parity, ESM-2 cache integrity, and GVP input integration have been checked. **Zero manual assays have been approved. No frozen scientific split or v4 held-out binding-affinity benchmark exists.** Do not use engineering-only DAVIS pilot validation results as scientific conclusions.

## Source-access audit and manual-review readiness — 6 November 2026

The project now includes `scripts/audit_primary_source_access_v4.py` and `scripts/build_primary_source_review_worklist_v4.py`. The access stage is READ-ONLY with respect to the human-curation spreadsheet and experimental affinity records. For the fixed 30-task review queue, Europe PMC confirmed 20 exact publication metadata matches; two openly accessible article section indexes were created without copying full article bodies; seventeen publications lack public open-access full text via this route; one XML document was rejected due to DTD/entities. At the task level, seven primary patents require review, twenty tasks need original-article access, two have publicly indexed sections and one lacks usable primary source identifiers. **ALL THIRTY TASKS REMAIN UNREVIEWED.** The output is a reviewer worklist, not a source-approved dataset.

The canonical source is still `data/audit/bindingdb_assay_manual_review_queue_30_ENRICHED.csv`; its SHA-256 must agree with the source access index before any review list is used. The formal review validator must not accept claims derived merely from keyword hits, article titles or UniProt matching. A qualified reviewer must inspect original experimental methods/supplements, document the physical protein construct, measurement semantics/qualifiers, source location and assay compatibility, and then record supported decisions. Do not invent authorizations or create approved cohort and split artifacts from this machine-generated index. The original source-access stage passed 18/18 checks, including XML entity rejection and protection of the human review CSV; the subsequent construct-alignment risk test extended the latest suite to 19/19. See `research/source_access_v4/` and `data/audit/source_access_index_integrity.json`.

## Two primary-source construct-alignment risk flags — 6 November 2026

Among the fixed 30 still-unapproved BindingDB tasks, two open-access primary papers explicitly identify physical protein regions shorter than the canonical full-length UniProt sequences stored in the candidate records: NPR-C (P17342) reference length 541 versus reported receptor residues 27–541 (515 amino acids) from PMID 35333039 / PMC9014859, and NRP1 (O14786) reference length 923 versus the reported NRP1-b1 region 273–427 (155 amino acids) from PMID 29648813 / PMC5957473. The NRP1 paper narrative uses both b1 and b1b2 terminology in different contexts, so particular measurement-to-construct association still needs manual verification. These findings are **source-reported region differences, not proof that any BindingDB Kd is wrong**. Exact tagged/processed construct sequence, individual label provenance and comparator assay conditions remain unverified.

The independently checked candidate full-length reference spans and immutable review CSV hash are recorded in `research/source_access_v4/construct_alignment_risk_screen.json` and `PRELIMINARY_CONSTRUCT_ALIGNMENT_REVIEW.md`. `scripts/check_primary_construct_flags_v4.py` and `tests_v4/construct_alignment_risk_integrity_test.py` fail closed if those metadata or original review decisions change. The engineering regression suite now passes **19/19**, but **zero source-approved assays** and **no frozen protein-group split** exist. These two records should not enter a scientific training or test cohort until the experimental construct is independently matched to a verified sequence/structure representation and the exact Kd records have been adjudicated.

## All-thirty candidate metadata-triage readiness — 6 November 2026

A deterministic, label-independent metadata screen was added as `scripts/triage_30_assay_metadata_v4.py`, covering exactly the thirty candidate tasks originally selected for primary-source review. It combines only the original unmodified review queue, canonical-reference sequence lengths, metadata source-access categories and two published fragment-method locators. **None of the thirty tasks has source review approval; no Kd labels were accessed or new cohort released.** The machine-generated reviewer priorities are P0 (endpoint/source metadata ambiguity) 4, P1 (construct/endpoint/source complexity) 12 and P2 (standard original-paper review) 14; these are effort-routing categories, NOT experimental defect judgments, exclusion decisions or model-training eligibility.

The screen flags six descriptions with numeric regions shorter than the canonical target reference, eight with tagged/labeled reagents, four with potentially surrogate activity-endpoint language and four with competition/displacement methodology. Examples for urgent manual clarification include a CFTR record whose description calls its Kd field a half-effective concentration and a GLP-1 receptor record with a glucose colorimetric assay description. A VHL/Elongin multi-protein record contains a VHL 54–213 span exceeding the Elongin-C 112-residue canonical reference; this range **must not be assigned to the Elongin-C chain without individual source mapping**. Every record must still be checked for actual source Kd, qualifiers, construct, physical sequence, chain identity, matching assay conditions and compound-to-original-table identity regardless of missing flags.

Results and warnings: `research/source_access_v4/assay_metadata_risk_triage_30.json`, `.csv`, and `ASSAY_METADATA_TRIAGE.md`; independent test `tests_v4/metadata_risk_triage_integrity_test.py`. The protected manual-review CSV SHA-256 remains unchanged and `scientific_cohort_gate.py` must remain blocked. The source-review task should use these priority counts solely to plan human adjudication, not to replace it.

## Next eligibility milestone

Independent source-level adjudication of the review queue and establishment of sufficiently many verified Kd tasks from diverse protein groups. Only then release an approved cohort, freeze the group split, implement source-traceable real geometry alignment, and train matched baselines on scientifically defensible data.
