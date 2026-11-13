"""Recompute all saved metrics and enforce baseline/correction invariants."""
import argparse,json
from pathlib import Path
import numpy as np
from evaluate_pretrained_structure_dev import metrics

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--bundle-dir',required=True);ap.add_argument('--results',required=True);ap.add_argument('--reference-cv',required=True);a=ap.parse_args();out=Path(a.results)
    with np.load(Path(a.bundle_dir)/'features.npz') as z:y=z['label'];rows=z['source_row'];g=z['groups'][z['protein_index']]
    report=json.loads((out/'results.json').read_text());runs=json.loads((out/'runs.json').read_text());assert len(runs)==40
    assert len({(r['fold'],r['seed'],r['arm']) for r in runs})==40
    with np.load(out/'predictions_LOCAL.npz') as z,np.load(Path(a.reference_cv)/'oof_predictions_LOCAL.npz') as ref:
        assert np.array_equal(rows,z['source_row']) and np.array_equal(rows,ref['source_row']);error=float(np.max(np.abs(z['baseline']-ref['baseline'])));assert error<1e-6
        for arm,expected in report['ensemble_metrics'].items():
            p=z[arm];assert p.shape==(2,len(y));assert np.isfinite(p).all();assert np.max(np.abs(p-z['baseline'][None,:]))<=.250001
            actual=metrics(y,p.mean(0),g)
            for key,value in actual.items():assert abs(value-expected[key])<1e-7
            for seed in range(2):
                for key,value in metrics(y,p[seed],g).items():assert abs(value-report['seed_metrics'][arm][seed][key])<1e-7
    print(json.dumps({'runs':40,'rows':len(y),'groups':len(set(g)),'all_metrics_reproduced':True,'baseline_reference_max_error':error,'all_corrections_within_cap':True,'model_unit_checks':report['protocol']['validation']},indent=2))
if __name__=='__main__':main()
