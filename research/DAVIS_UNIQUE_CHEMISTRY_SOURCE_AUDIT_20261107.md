# DAVIS source chemistry identity-count audit

Follow-up to `5786975`: independently verify whether the source-review count thresholds are inflated by multiple reactant records referring to one BindingDB monomer. This audit joins the existing 63-record private source evidence, the 40-record private registry lookup and the original BindingDB provenance stream. Only aggregate counts are exported. No compound, monomer, reactant or affinity values are committed.

| Target | Distinct exact-match BindingDB monomers | Distinct monomers with conditional registry leads | Minimum still needed after conditional leads |
|---|---:|---:|---:|
| IRAK3 | 9 | 16 | 0 |
| RIOK2 | 9 | 13 | 2 |
| SRPK3 | 5 | 13 | 2 |

There are zero duplicate exact-match reactant records by BindingDB MonomerID in these three targets. This supports the *arithmetic* of the earlier prioritization. It does **not** prove stereochemical uniqueness, verify source compound structures, validate the physical construct or assay endpoint, or authorize use of any of these rows for scientific training. All conditional registry leads remain unapproved.

Implementation refuses missing monomer provenance, duplicate source reactant IDs, missing/misaligned registry evidence, and mismatched registry universes. Synthetic regression tests include a deliberately duplicated monomer. The source-review gate remains blocked and the project does not have an independently frozen test set.
