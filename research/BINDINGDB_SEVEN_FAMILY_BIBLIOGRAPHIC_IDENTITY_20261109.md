# Seven conflicted BindingDB source families: independent bibliographic reconciliation

**DynaCPI v4 | 9 November 2026 | Original-source metadata only | No scientific assay approval**

## Why this is needed for the PerceiverCPI comparison

The earlier exploratory DynaCPI/TransferCPI vs original PerceiverCPI pilot used a subsequently retired provisional protein split: seven bibliographically connected source families crossed provisional role boundaries. A model gain on unresolved source/homology groups could be leakage or source-protocol memorization. Strong architecture and few-shot adaptation comparisons **cannot produce trustworthy evidence until source identity, assay and physical construct provenance are independently reviewed**.

A previous integrity-preserving metadata projection identified **1,146** technically eligible tasks in **142** preliminary source-connected families and **729** DOI/PMID/patent identifier strings globally. Of these, the **seven conflicted source families** contained **708 technical tasks** and **220 distinct identifier strings**: **74 DOI**, **90 PMID** and **56 patent**. **62 tasks** lacked all three identifier types and were associated with a family only through their preliminary protein-component linkage. None was approved for scientific model training.

## Independent Europe PMC lookup: exact citation identity only

Using the public Europe PMC RESTful bibliographic API, we performed **22 source-metadata query batches** against the MED/PubMed source. Queries used exact `EXT_ID` or exact `DOI` fields plus `SRC:MED`; only an exact returned identifier was accepted. We fetched **lite publication metadata only**, not abstracts, results, supplementary assay tables, numerical affinity data or model predictions. The script checks the SHA256 of the frozen private source index before and after lookup.

| Metadata finding, seven conflicted families | Count |
|---|---:|
| Original DOI identifier strings | **74** |
| DOI identifiers resolved to exact Europe PMC/MED record | **73** |
| Original PMID identifier strings | **90** |
| PMID identifiers resolved to exact Europe PMC/MED record | **90** |
| **DOI–PMID pairs reciprocally confirmed for the same MED article** | **72** |
| One-way unconfirmed DOI–PMID alias leads within a family | 0 |
| Candidate DOI–PMID links between previously separate source families | 0 |
| Original DOI identifiers not found exactly in MED | **1** |
| API batch network failures | **0** |
| Original patent identifiers without article equivalence evidence | **56** |

**Interpretation:** the 72 reciprocal DOI–PMID pairs refer to the same **publication**, not 72 validated experiments. They are not 72 new source-family edges or 72 assay approvals. Among the original ID strings, **2 DOI and 18 PMID strings remain without a reciprocally matched counterpart from the same family inventory**. This does not mean they represent 20 extra independent papers; bibliographic completeness and primary experimental status still need review.

A second exact DOI lookup against **Crossref** recovered the **one DOI absent from the PubMed/MED results** as a journal-article bibliographic record. Therefore **all 74 original DOI strings have an exact metadata record in at least one of these two bibliographic indexes**. This does **not** establish a PubMed identifier for the Crossref-only article, confirm that it is primary research, or prove its experimental measurements.

## Privacy and original-source holdout boundaries

Detailed article identifiers, bibliographic metadata, source-family hashes and DOI–PMID provenance remain exclusively in two pre-existing/new local reviewer files:

- `data/audit/SEVEN_FAMILY_BIBLIOGRAPHIC_ALIAS_VERIFICATION_PRIVATE_20261109.json`
- `data/audit/SEVEN_FAMILY_CROSSREF_DOI_EXCEPTION_PRIVATE_20261109.json`

The public aggregate reports include only counts and caveats, **not** individual DOI/PMID/patent strings, source-family hashes, task IDs, protein component IDs, provisional role assignments, assay compounds, affinity observations, predictions or prospective TEST metrics. The original private source index and review files are preserved; no graph merge, role reassignment or reviewed-source decision was made.

Public reproducibility paths:

- `scripts/reconcile_seven_family_bibliographic_aliases_v4.py`: exact, reciprocal Europe PMC DOI/PMID lookups with conservative matches, network-failure reporting, input SHA256 integrity, private details/public aggregate separation, output no-overwrite.
- `scripts/verify_seven_family_crossref_doi_exception_v4.py`: exact Crossref DOI lookup only for the single previously unresolved PubMed DOI, with a separate private citation record and public aggregate.
- `tests_v4/seven_family_bibliographic_alias_reconciliation_test.py`: fabricated metadata test coverage for reciprocal versus one-way aliases, cross-family alias leads, malformed source IDs, fake approval, exact MED search and privacy.
- `tests_v4/seven_family_crossref_exception_test.py`: Crossref source identity, malformed/missing metadata and source review status tests plus saved public/private artifact separation.
- `research/bindingdb_seven_family_bibliographic_alias_20261109.json` and `research/bindingdb_seven_family_crossref_exception_20261109.json`: public aggregate-only results.

## What remains before scientifically defensible model improvement claims

1. **Independent original-assay table and method review** for physically assayed constructs, pH, temperature, endpoint type (direct equilibrium Kd vs Ki, IC50, proxy or imputed values), qualifier treatment (exact vs inequality vs missing) and source-row mapping. This has **not** occurred here. Access to a bibliographic title or methods index is not source-record verification.
2. **The 62 unattributed technical tasks** still require original study/record attribution. Protein-component or family membership must not automatically provide a surrogate source citation.
3. **The 56 patent strings** require original patent-equivalence and assay-method review; neither matching assay keywords nor a PubMed DOI allows automatic patent collapse.
4. **The 2 DOI-only and 18 PMID-only source strings** remain candidates for further bibliographic triangulation; no manual alias or family merge was performed.
5. Only after independently vetted original sources/constructs and a **newly preregistered source-family- and homology-disjoint split** may the team run a fair, matched K-shot PerceiverCPI vs DynaCPI comparison. The prior provisional roles remain retired; do not reopen their reserved TEST outcome values to guide curation.

## Scientific disposition

| Approval or evaluation milestone | Status |
|---|---|
| Original DOI/PMID bibliographic identity reconciliation | **72 reciprocal pairs verified; 74/74 DOI metadata located** |
| Independently reviewed original BindingDB source-record crosswalks | **0** |
| Independently verified physically assayed protein constructs | **0** |
| Scientifically approved families or tasks | **0** |
| Training or prospective test evaluation performed here | **None** |
| Actual scientific cohort gate | **`BLOCKED_UNAPPROVED_NOT_TRAINING_READY`** |

This is concrete source-identity progress, but **does not by itself improve DynaCPI predictive performance or demonstrate any victory over PerceiverCPI**. The next valuable human science milestone is source-record/construct adjudication without using protected assay outcomes for model selection.
