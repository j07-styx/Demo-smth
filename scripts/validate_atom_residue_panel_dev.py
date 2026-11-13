"""Independent saved-prediction validation for the small TRAIN-panel fit gate."""
import argparse,json
from pathlib import Path
import numpy as np

def metrics(y,p,ids):
    err=y-p
    centered=np.concatenate([err[ids==i]-err[ids==i].mean() for i in np.unique(ids)])
    return {'rmse':float(np.sqrt(np.mean(err**2))),'within_protein_rmse':float(np.sqrt(np.mean(centered**2)))}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--bundle',required=True);ap.add_argument('--run',required=True);a=ap.parse_args();root=Path(a.run)
    with np.load(Path(a.bundle)/'features.npz') as z:
        rows=z['source_row'];y=z['label'];pi=z['protein_index'];groups=z['groups']
    lookup={int(v):i for i,v in enumerate(rows)};assert len(lookup)==len(rows)
    with np.load(root/'rows_LOCAL.npz') as z:
        tr=np.array([lookup[int(v)] for v in z['train_source_row']]);va=np.array([lookup[int(v)] for v in z['held_source_row']])
    assert len(tr)==len(va)==64 and not set(tr)&set(va)
    assert not set(groups[pi[tr]])&set(groups[pi[va]])
    for ix in [tr,va]:
        assert len(np.unique(pi[ix]))==4 and all(sum(pi[ix]==p)==16 for p in np.unique(pi[ix]))
    result=json.loads((root/'results.json').read_text())
    for arm in ['chemical_only','sequence','real','shuffled','constant_train_mean']:
        pred=np.full(128,y[tr].mean()) if arm=='constant_train_mean' else np.load(root/(arm+'_pred_LOCAL.npy'))
        assert pred.shape==(128,) and np.isfinite(pred).all()
        for role,ix,p in [('train',tr,pred[:64]),('held',va,pred[64:])]:
            for key,value in metrics(y[ix],p,pi[ix]).items():
                assert abs(value-result[arm][role][key])<1e-6,(arm,role,key)
    report={'all_metrics_reproduced':True,'train_only_row_membership':True,'group_disjoint':True,'four_proteins_sixteen_rows_per_role':True,'finite_predictions':True}
    (root/'validation.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
if __name__=='__main__':main()
