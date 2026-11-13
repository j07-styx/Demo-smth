"""Aggregate repeated group CV without treating repeats as independent samples."""
import argparse,json
from pathlib import Path
import numpy as np
from evaluate_pretrained_structure_dev import sha

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--bundle-dir',required=True);ap.add_argument('--runs',nargs='+',required=True);ap.add_argument('--out',required=True);a=ap.parse_args();out=Path(a.out);out.mkdir(parents=True,exist_ok=False)
    with np.load(Path(a.bundle_dir)/'features.npz') as z:rows=z['source_row'];y=z['label'];g=z['groups'][z['protein_index']]
    names=['baseline','esm2_sequence','saprot_real','saprot_shuffled'];errors={n:[] for n in names};summaries=[]
    for run in a.runs:
        p=Path(run);r=json.loads((p/'results.json').read_text());summaries.append({'split_seed':r['protocol']['split_seed'],'metrics':r['metrics'],'results_sha256':sha(p/'results.json')})
        with np.load(p/'oof_predictions_LOCAL.npz') as z:
            assert np.array_equal(rows,z['source_row'])
            for n in names:assert np.isfinite(z[n]).all();errors[n].append((y-z[n])**2)
    assert len(set(r['split_seed'] for r in summaries))==len(summaries)
    # Average squared error for each row across splits, then form group metrics.
    errors={n:np.mean(e,axis=0) for n,e in errors.items()};u=np.unique(g);counts=np.array([sum(g==v) for v in u]);ge={n:np.array([e[g==v].mean() for v in u]) for n,e in errors.items()}
    result={'evidence':'EXPLORATORY_REPEATED_TRAIN_GROUP_CV','runs':summaries,'rows':len(y),'groups':len(u),'aggregation':'mean squared error across repeated predictions per row; root after averaging, not a prediction ensemble','uncertainty':'paired bootstrap of 253 groups, repeated-split losses averaged before resampling; conditional, no search adjustment','metrics':{n:{'pooled_rmse':float(np.sqrt(e.mean())),'group_macro_rmse':float(np.sqrt(ge[n]).mean())} for n,e in errors.items()},'contrasts':{}}
    ix=np.random.RandomState(5122).randint(len(u),size=(5000,len(u)))
    for other in ['baseline','esm2_sequence','saprot_shuffled']:
        ea,eb=ge['saprot_real'],ge[other];md=np.sqrt(ea)-np.sqrt(eb);pool=np.sqrt((ea[ix]*counts[ix]).sum(1)/counts[ix].sum(1))-np.sqrt((eb[ix]*counts[ix]).sum(1)/counts[ix].sum(1))
        result['contrasts']['real_minus_'+other]={'macro_delta':float(md.mean()),'macro_ci95':np.percentile(md[ix].mean(1),[2.5,97.5]).tolist(),'pooled_delta':float(np.sqrt(np.average(ea,weights=counts))-np.sqrt(np.average(eb,weights=counts))),'pooled_ci95':np.percentile(pool,[2.5,97.5]).tolist(),'groups_improved':int(sum(md<0))}
    (out/'results.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
if __name__=='__main__':main()
