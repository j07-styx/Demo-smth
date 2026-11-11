"""Predeclared bounded token-fusion engineering trial, on frozen TRAIN groups only."""
import argparse,hashlib,json,sys,time
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import numpy as np
import torch
from scipy.sparse import csr_matrix,hstack
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import normalize
from sklearn.linear_model import Ridge
from dynacpi.structural_token_fusion_dev import StructuralTokenFusion


def metrics(y,p,groups):
    err=(y-p)**2
    return dict(pooled_rmse=float(np.sqrt(err.mean())),group_macro_rmse=float(np.mean([np.sqrt(err[groups==g].mean()) for g in sorted(set(groups))])))


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--bundle-dir',required=True);ap.add_argument('--out',required=True)
    ap.add_argument('--seeds',type=int,nargs='+',default=[4111,4112,4113]);ap.add_argument('--epochs',type=int,default=5)
    ap.add_argument('--steps-per-epoch',type=int,default=64);ap.add_argument('--threads',type=int,default=2)
    ap.add_argument('--correction-cap',type=float,default=None,help='Optional positive tanh cap in raw target units')
    a=ap.parse_args();out=Path(a.out);out.mkdir(parents=True,exist_ok=False)
    if a.correction_cap is not None and a.correction_cap<=0:raise ValueError('Cap must be positive')
    b=Path(a.bundle_dir);meta=json.loads((b/'manifest.json').read_text())
    assert meta['evidence']=='ENGINEERING_ONLY_BALM_FROZEN_TRAIN'
    assert hashlib.sha256((b/'features.npz').read_bytes()).hexdigest()==meta['bundle_sha256']
    with np.load(b/'features.npz',allow_pickle=False) as z:d={k:z[k].copy() for k in z.files}
    # Freeze split and arm choices before evaluating any prediction.
    rng=np.random.RandomState(4110);groups=np.array(sorted(set(d['groups'])));rng.shuffle(groups)
    held=set(groups[:max(1,len(groups)//5)])
    pi=d['protein_index'];ci=d['compound_index'];rowgroups=d['groups'][pi]
    tr=np.flatnonzero([g not in held for g in rowgroups]);va=np.flatnonzero([g in held for g in rowgroups])
    y=d['label'];mu=float(y[tr].mean());std=float(y[tr].std())
    # Reference ridge plus group-cross-fitted training residuals avoids fitting
    # a correction to artificially tiny in-sample ridge residuals.
    def ridge(train,test):
        vec=TfidfVectorizer(analyzer='char',ngram_range=(3,4),max_features=4096,sublinear_tf=True,dtype=np.float32)
        text=d['protein_sequence'][pi]
        pt=vec.fit_transform(text[train]);pv=vec.transform(text[test])
        fp=normalize(csr_matrix(d['fp'][ci]))
        xt=hstack([fp[train],.25*pt],format='csr');xv=hstack([fp[test],.25*pv],format='csr')
        m=float(y[train].mean());s=float(y[train].std())
        reg=Ridge(alpha=1,solver='lsqr');reg.fit(xt,(y[train]-m)/s)
        return reg.predict(xv)*s+m
    baseline=ridge(tr,va);oof=np.full(len(y),np.nan,dtype='float32')
    tg=np.array(sorted(set(rowgroups[tr])));np.random.RandomState(4114).shuffle(tg)
    folds={g:i%3 for i,g in enumerate(tg)}
    for f in range(3):
        fit=np.array([i for i in tr if folds[rowgroups[i]]!=f]);ev=np.array([i for i in tr if folds[rowgroups[i]]==f])
        oof[ev]=ridge(fit,ev)
    assert np.isfinite(oof[tr]).all()
    # Normalize geometry on distinct fit proteins, never held-out proteins.
    ptrain=np.unique(pi[tr]);valid=d['residue_valid']
    vals=d['geometry'][ptrain][valid[ptrain]];gm=vals.mean(0);gs=np.maximum(vals.std(0),1e-6)
    geo=(d['geometry']-gm)/gs;geo[~valid]=0
    shuffled=geo.copy();rg=np.random.RandomState(4115)
    for p in range(len(geo)):
        ix=np.flatnonzero(valid[p]);shuffled[p,ix]=geo[p,rg.permutation(ix)]
    t={k:torch.as_tensor(d[k],dtype=torch.bool if k.endswith('valid') else torch.float32)
       for k in ('fp','atoms','atom_valid','sequence','residue_valid')}
    tgeo=torch.tensor(geo);tshuffle=torch.tensor(shuffled)
    torch.set_num_threads(a.threads)
    protocol={'evidence':'ENGINEERING_ONLY_TRAIN_INTERNAL_HOLDOUT','feature_manifest':meta,'args':vars(a),
              'split_seed':4110,'train_rows':len(tr),'dev_rows':len(va),'dev_groups':len(held),
              'selection':'fixed final epoch; uncapped scale 0.25 or explicitly declared cap; no epoch selection','baseline':metrics(y[va],baseline,rowgroups[va]),
              'arms':['sequence','real','mean','shuffled'],'source_row_train_sha256':hashlib.sha256(d['source_row'][tr].tobytes()).hexdigest(),
              'source_row_dev_sha256':hashlib.sha256(d['source_row'][va].tobytes()).hexdigest(),'runs':[]}
    (out/'protocol.json').write_text(json.dumps(protocol,indent=2))
    np.savez_compressed(out/'split_LOCAL.npz',train=tr,dev=va,geometry_mean=gm,geometry_std=gs)
    print('LOCKED',json.dumps({k:protocol[k] for k in ('train_rows','dev_rows','dev_groups','baseline')}),flush=True)
    for seed in a.seeds:
        for arm in protocol['arms']:
            torch.manual_seed(seed);rng=np.random.RandomState(seed)
            model=StructuralTokenFusion(d['sequence'].shape[-1],geo.shape[-1],d['atoms'].shape[-1])
            opt=torch.optim.AdamW(model.parameters(),lr=3e-4,weight_decay=.01)
            geometry=tshuffle if arm=='shuffled' else tgeo;mode='real' if arm=='shuffled' else arm
            def predict(ix):
                p=pi[ix];c=ci[ix]
                return model(t['fp'][c],t['atoms'][c],t['atom_valid'][c],t['sequence'][p],geometry[p],t['residue_valid'][p],mode)
            def correction(raw):
                return .25*raw if a.correction_cap is None else (a.correction_cap/std)*torch.tanh(raw)
            start=time.monotonic()
            for epoch in range(a.epochs):
                model.train();order=rng.permutation(tr)
                for step in range(min(a.steps_per_epoch,(len(order)+31)//32)):
                    ix=order[step*32:(step+1)*32];opt.zero_grad()
                    target=torch.tensor((y[ix]-oof[ix])/std)
                    loss=((correction(predict(ix))-target)**2).mean();loss.backward()
                    torch.nn.utils.clip_grad_norm_(model.parameters(),1.);opt.step()
                print(seed,arm,'epoch',epoch+1,'loss',float(loss),flush=True)
            model.eval()
            with torch.no_grad():delta=np.concatenate([correction(predict(va[i:i+32])).numpy() for i in range(0,len(va),32)])*std
            if a.correction_cap is not None:assert np.max(np.abs(delta))<=a.correction_cap+1e-6
            pred=baseline+delta;run=dict(seed=seed,arm=arm,**metrics(y[va],pred,rowgroups[va]),correction_sd=float(delta.std()),
                correction_mean=float(delta.mean()),seconds=time.monotonic()-start)
            np.savez_compressed(out/f'{arm}_{seed}_pred_LOCAL.npz',pred=pred,delta=delta,source_row=d['source_row'][va])
            torch.save({'state_dict':model.state_dict(),'run':run,'feature_manifest':meta},out/f'{arm}_{seed}_LOCAL.pt')
            protocol['runs'].append(run);(out/'results.json').write_text(json.dumps(protocol,indent=2));print(json.dumps(run),flush=True)
    # Paired group bootstrap averages seed SSE before resampling groups.
    ug=sorted(set(rowgroups[va]));arm_errors={}
    for arm in protocol['arms']:
        errors=[]
        for seed in a.seeds:
            with np.load(out/f'{arm}_{seed}_pred_LOCAL.npz') as z:err=(y[va]-z['pred'])**2
            errors.append([float(err[rowgroups[va]==g].mean()) for g in ug])
        arm_errors[arm]=np.sqrt(np.mean(errors,axis=0))
    contrasts={};rg=np.random.RandomState(4116)
    for other in ('sequence','mean','shuffled'):
        diff=arm_errors['real']-arm_errors[other]
        boot=[float(diff[rg.randint(0,len(ug),len(ug))].mean()) for _ in range(5000)]
        contrasts['real_minus_'+other]={'group_macro_delta':float(diff.mean()),'ci95':np.percentile(boot,[2.5,97.5]).tolist()}
    protocol['paired_group_contrasts']=contrasts
    (out/'results.json').write_text(json.dumps(protocol,indent=2));print('COMPLETE',json.dumps(contrasts),flush=True)


if __name__=='__main__':main()
