"""Label-free token-retention audit; not a binding-pocket coverage assay."""
import argparse,json,hashlib
from pathlib import Path
import numpy as np
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--bundle',required=True);ap.add_argument('--cache',required=True);ap.add_argument('--out',required=True);a=ap.parse_args()
    with np.load(Path(a.bundle)/'features.npz') as z:seq=z['protein_sequence'];hashes=z['protein_sha']
    with np.load(Path(a.cache)/'saprot_real.npz') as z:
        assert np.array_equal(hashes,z['protein_sha'])
        valid=z['valid'];positions=z['positions']
    lengths=np.array([len(s) for s in seq]);retained=valid.sum(1);fractions=retained/lengths
    gaps=[]
    for i in range(len(seq)):
        p=positions[i][valid[i]];assert len(np.unique(p))==len(p) and (p>=0).all() and (p<lengths[i]).all()
        gaps.append(int(np.diff(p).max()) if len(p)>1 else 0)
    out={'evidence':'LABEL_FREE_RESIDUE_RETENTION','proteins':len(seq),'total_residues':int(lengths.sum()),'retained_residues':int(retained.sum()),'retained_fraction_micro':float(retained.sum()/lengths.sum()),'retained_fraction_median':float(np.median(fractions)),'proteins_below_quarter_retention':int(sum(fractions<.25)),'longest_sequence':int(lengths.max()),'largest_sample_spacing':max(gaps),'limits':'Token retention is not information retention: contextual embeddings incorporate neighboring sequence. Pocket coverage and lost affinity information are not measured.'}
    Path(a.out).write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
if __name__=='__main__':main()
