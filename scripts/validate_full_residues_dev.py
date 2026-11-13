"""Validate complete caches against sequence lengths and original sampled tokens."""
import argparse,json,hashlib
from pathlib import Path
import numpy as np
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--full',required=True);ap.add_argument('--sampled',required=True);ap.add_argument('--bundle',required=True);a=ap.parse_args()
    root=Path(a.full);manifest=json.loads((root/'manifest.json').read_text())
    assert set(manifest['features'])=={'saprot_real','saprot_shuffled','esm2_sequence'}
    with np.load(Path(a.bundle)/'features.npz') as z:lengths=np.array([len(s) for s in z['protein_sequence']]);hashes=z['protein_sha']
    reports={}
    for name,rec in manifest['features'].items():
        file=root/(name+'.npz');assert sha(file)==rec['sha256']
        with np.load(file) as z,np.load(Path(a.sampled)/(name+'.npz')) as old:
            r=z['features'];off=z['offsets'];assert np.array_equal(hashes,z['protein_sha']) and np.array_equal(hashes,old['protein_sha'])
            assert np.array_equal(np.diff(off),lengths) and off[0]==0 and off[-1]==len(r)
            assert r.shape==(int(lengths.sum()),480) and np.isfinite(r).all()
            err=0.
            for i in range(len(lengths)):
                mask=old['valid'][i];pos=old['positions'][i][mask]
                err=max(err,float(np.max(np.abs(r[off[i]+pos]-old['features'][i][mask]))))
            assert err<1e-4
            reports[name]={'all_positions_present':True,'finite':True,'sampled_token_max_error':err}
    report={'proteins':len(lengths),'residues_per_arm':int(lengths.sum()),'arms':reports,'label_values_loaded':False}
    (root/'validation.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
if __name__=='__main__':main()
