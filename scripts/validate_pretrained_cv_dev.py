"""Independently audit outer-CV coverage, group isolation and reported metrics."""
import argparse,json
from pathlib import Path
import numpy as np
from evaluate_pretrained_structure_dev import metrics,ARMS

def assert_partition(parts,groups,n):
    seen=np.zeros(n,int);owners={}
    for fold,ix in enumerate(parts):
        assert len(ix)==len(set(ix.tolist()))
        seen[ix]+=1
        for group in set(groups[ix]):
            assert group not in owners
            owners[group]=fold
    assert (seen==1).all()

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--bundle-dir',required=True);ap.add_argument('--results',required=True);a=ap.parse_args();out=Path(a.results)
    with np.load(Path(a.bundle_dir)/'features.npz') as z:rows=z['source_row'];g=z['groups'][z['protein_index']];y=z['label']
    lookup={r:i for i,r in enumerate(rows.tolist())};parts=[]
    for fold in range(5):
        with np.load(out/('fold_'+str(fold))/'predictions_LOCAL.npz') as z:parts.append(np.array([lookup[r] for r in z['source_row'].tolist()]))
    assert_partition(parts,g,len(rows))
    rejected=0
    for parts_bad,groups_bad in [([np.array([0,1]),np.array([1,2])],np.array(['a','b','c'])),([np.array([0]),np.array([2])],np.array(['a','b','c'])),([np.array([0]),np.array([1,2])],np.array(['a','a','b']))]:
        try:assert_partition(parts_bad,groups_bad,3)
        except AssertionError:rejected+=1
        else:raise AssertionError('Invalid partition accepted')
    report=json.loads((out/'results.json').read_text())
    with np.load(out/'oof_predictions_LOCAL.npz') as z:
        assert np.array_equal(rows,z['source_row'])
        for arm in ['baseline']+ARMS:
            actual=metrics(y,z[arm],g)
            for metric,value in actual.items():assert abs(value-report['metrics'][arm][metric])<1e-6
    print(json.dumps({'rows_exactly_once':len(rows),'groups_in_exactly_one_fold':len(set(g)),'negative_partition_controls_rejected':rejected,'all_reported_metrics_reproduced':True},indent=2))
if __name__=='__main__':main()
