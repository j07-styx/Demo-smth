# IRAK3 private seven-record source-review packet

The next step after unique-monomer counting is a **review-ready private CSV**, not another architecture experiment. `scripts/prepare_irak3_registry_review_packet_dev.py` joins the seven cached registry links against the original BindingDB provenance and publisher Supplementary Table 4. It rejects ambiguous columns, nonpositive or mismatched Kd values, duplicated reactant records, duplicated BindingDB monomers, and unexpected approvals.

The generated private packet is stored locally at:

`data/audit/davis_primary_20261107/irak3_registry_review_packet_LOCAL_PRIVATE.csv`

The CSV includes seven publisher compound names, PubChem registry identifiers, BindingDB monomer/reactant identifiers, publisher Kd values and BindingDB Kd values. **Do not commit or upload this CSV.** The committed JSON reports aggregate counts and source hashes only.

Seven of seven numeric Kd cells agree exactly and correspond to seven distinct BindingDB monomer identifiers. **Zero** have approved compound identity, stereochemistry, protein constructs, or assay methods. Registry synonym agreement and exact numeric matching do not establish identity. All review decisions remain UNREVIEWED. A human source reviewer must check structure/stereochemistry and the physical assay/construct provenance before changing the gate.

In parallel, the newly frozen BindingDB component manifest reserves 2,936 prospective test pairs, but explicitly warns that historical experiments trained on some of the reserved components. The manifest is provisional, source QC incomplete, and no test predictions were generated in this change. The new DeepDTA inner-dev normalization experiment remains worse than the train-mean comparator. Avoid further repeatedly inspected inner-dev architecture sweeps until scientific validity is improved.
