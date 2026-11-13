"""Five outer group folds; unchanged three-fold inner scale selection."""
import argparse,json,subprocess,sys,hashlib
from pathlib import Path
import numpy as np
from evaluate_pretrained_structure_dev import ARMS,metrics,sha

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--bundle-dir',required=True);ap.add_argument('--features',required=True);ap.add_argument('--out',required=True);ap.add_argument('--readout',choices=['interaction','protein'],default='interaction');ap.add_argument('--max-scale',type=float,choices=[.3,1.],default=.3);ap.add_argument('--split-seed',type=int,default=4110);a=ap.parse_args()
    out=Path(a.out);out.mkdir(parents=True,exist_ok=False)
    protocol={'evidence':'ENGINEERING_ONLY_TRAIN_NESTED_GROUP_CV','outer_folds':5,'split_seed':a.split_seed,'assignment':'shuffled sorted groups, round robin','inner_folds':3,'scale_grid':[s for s in [0,.1,.3,1] if s<=a.max_scale],'readout':a.readout,'max_scale':a.max_scale,'arms':['baseline']+ARMS,'selection':'fixed ESM interaction scale .3, tune added protein block using inner group-macro RMSE only; esm2_sequence arm is duplicate ESM control','decision':'real must improve both pooled and macro versus baseline, ESM2 and shuffled; intervals reported without claiming independent-test significance','limitations':['TRAIN cohort already used for exploratory development','Group bootstrap conditions on overlapping CV fits; not full retraining uncertainty','Single outer partition and one shuffled token realization','No reserved test is read'],'evaluator_sha256':sha(Path(__file__).with_name('evaluate_joint_structure_dev.py'))}
    (out/'protocol.json').write_text(json.dumps(protocol,indent=2))
    for fold in range(5):
        cmd=[sys.executable,'-u',str(Path(__file__).with_name('evaluate_joint_structure_dev.py')),'--bundle-dir',a.bundle_dir,'--features',a.features,'--out',str(out/('fold_'+str(fold))),'--outer-fold',str(fold),'--readout',a.readout,'--max-scale',str(a.max_scale),'--split-seed',str(a.split_seed)]
        print('START OUTER',fold,flush=True);subprocess.run(cmd,check=True);print('DONE OUTER',fold,flush=True)
    with np.load(Path(a.bundle_dir)/'features.npz',allow_pickle=False) as z:
        rows=z['source_row'];y=z['label'];g=z['groups'][z['protein_index']]
    assert len(set(rows.tolist()))==len(rows)
    pos={v:i for i,v in enumerate(rows.tolist())};pred={arm:np.full(len(y),np.nan) for arm in protocol['arms']};seen=np.zeros(len(y),int);fold_results=[]
    for fold in range(5):
        fold_results.append(json.loads((out/('fold_'+str(fold))/'results.json').read_text()))
        with np.load(out/('fold_'+str(fold))/'predictions_LOCAL.npz') as z:
            ix=np.array([pos[v] for v in z['source_row'].tolist()]);seen[ix]+=1
            for arm in pred:pred[arm][ix]=z[arm]
    assert (seen==1).all();assert all(np.isfinite(p).all() for p in pred.values())
    result={'protocol':protocol,'rows':len(y),'groups':len(set(g)),'metrics':{arm:metrics(y,p,g) for arm,p in pred.items()},'fold_metrics':[r['metrics'] for r in fold_results],'selected_scales':[r['selected_scales'] for r in fold_results],'contrasts':{}}
    groups=np.unique(g);counts=np.array([sum(g==v) for v in groups]);errors={arm:np.array([np.mean((y[g==v]-p[g==v])**2) for v in groups]) for arm,p in pred.items()};rng=np.random.RandomState(5122);ix=rng.randint(len(groups),size=(5000,len(groups)))
    for other in ['baseline','esm2_sequence','saprot_shuffled']:
        ea,eb=errors['saprot_real'],errors[other];delta=np.sqrt(ea)-np.sqrt(eb);macro=delta[ix].mean(1);pool=np.sqrt((ea[ix]*counts[ix]).sum(1)/counts[ix].sum(1))-np.sqrt((eb[ix]*counts[ix]).sum(1)/counts[ix].sum(1));sse=(ea-eb)*counts;order=np.argsort(np.abs(sse))[::-1]
        result['contrasts']['real_minus_'+other]={'macro_delta':float(delta.mean()),'macro_ci95':np.percentile(macro,[2.5,97.5]).tolist(),'pooled_delta':result['metrics']['saprot_real']['pooled_rmse']-result['metrics'][other]['pooled_rmse'],'pooled_ci95':np.percentile(pool,[2.5,97.5]).tolist(),'groups_improved':int(sum(delta<0)),'groups_worsened':int(sum(delta>0)),'top5_absolute_sse_share':float(np.abs(sse[order[:5]]).sum()/max(np.abs(sse).sum(),1e-12)),'fold_pooled_wins':sum(r['metrics']['saprot_real']['pooled_rmse']<r['metrics'][other]['pooled_rmse'] for r in fold_results),'fold_macro_wins':sum(r['metrics']['saprot_real']['group_macro_rmse']<r['metrics'][other]['group_macro_rmse'] for r in fold_results)}
    np.savez_compressed(out/'oof_predictions_LOCAL.npz',**pred,source_row=rows)
    (out/'results.json').write_text(json.dumps(result,indent=2));print('COMPLETE',json.dumps(result['metrics']),flush=True)
if __name__=='__main__':main()
