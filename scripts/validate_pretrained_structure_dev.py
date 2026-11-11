"""Validate cached paired-token controls and encoder feature integrity, no labels."""
import argparse,hashlib,json
from pathlib import Path
import numpy as np

def validate_pairs(real,shuffled):
    assert len(real)==len(shuffled)>0
    assert [t[0] for t in real]==[t[0] for t in shuffled]
    assert [t[1]=='#' for t in real]==[t[1]=='#' for t in shuffled]
    assert sorted(t[1] for t in real)==sorted(t[1] for t in shuffled)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--features',required=True);a=ap.parse_args();p=Path(a.features)
    t=json.loads((p/'tokens_LOCAL.json').read_text());pr=json.loads((p/'provenance.json').read_text());hashes=t['protein_sha']
    assert len(hashes)==len(set(hashes))==pr['protein_count']
    changed=0
    for real,shuffled in zip(t['real'],t['shuffled']):validate_pairs(real,shuffled);changed+=real!=shuffled
    for bad in [['Cx','By'],['A#','By'],['Ax','Bx']]:
        try:validate_pairs(['Ax','By'],bad)
        except AssertionError:pass
        else:raise AssertionError('Negative control was accepted')
    result={'proteins':len(hashes),'proteins_with_changed_3di':changed,'negative_controls_rejected':3,'features':{}}
    for name,expected in pr['feature_sha256'].items():
        assert hashlib.sha256((p/name).read_bytes()).hexdigest()==expected
        with np.load(p/name,allow_pickle=False) as z:
            assert z['protein_sha'].tolist()==hashes;f=z['features'];assert f.shape==(len(hashes),480);assert np.isfinite(f).all()
            result['features'][name]={'shape':list(f.shape),'mean_feature_sd':float(f.std(axis=0).mean())}
    with np.load(p/'saprot_real.npz') as r,np.load(p/'saprot_shuffled.npz') as s:
        delta=r['features']-s['features'];assert np.linalg.norm(delta)>0;result['real_shuffled_feature_rms']=float(np.sqrt(np.mean(delta**2)))
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
