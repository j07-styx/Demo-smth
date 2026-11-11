"""Matched frozen encoder probe. All transforms fit inside TRAIN group folds."""
import argparse, hashlib, json, os
os.environ.setdefault('OMP_NUM_THREADS','2')
os.environ.setdefault('OPENBLAS_NUM_THREADS','2')
from pathlib import Path
import numpy as np
from scipy.sparse import csr_matrix,hstack
from sklearn.decomposition import PCA,TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler,normalize
from sklearn.linear_model import Ridge
from threadpoolctl import threadpool_limits

ARMS=['esm2_sequence','saprot_real','saprot_shuffled']
SCALES=[0.,.1,.3,1.]
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def metrics(y,p,g):
    e=(y-p)**2
    return {'pooled_rmse':float(np.sqrt(e.mean())), 'group_macro_rmse':float(np.mean([np.sqrt(e[g==k].mean()) for k in np.unique(g)]))}
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--bundle-dir',required=True);ap.add_argument('--features',required=True);ap.add_argument('--out',required=True);a=ap.parse_args()
    out=Path(a.out);out.mkdir(parents=True,exist_ok=False);b=Path(a.bundle_dir);f=Path(a.features)
    meta=json.loads((b/'manifest.json').read_text());assert meta['evidence']=='ENGINEERING_ONLY_BALM_FROZEN_TRAIN';assert sha(b/'features.npz')==meta['bundle_sha256']
    with np.load(b/'features.npz',allow_pickle=False) as z:d={k:z[k] for k in ['protein_sha','protein_sequence','protein_index','compound_index','groups','fp','label','source_row']}
    features={}
    for arm in ARMS:
        with np.load(f/(arm+'.npz'),allow_pickle=False) as z:
            assert np.array_equal(z['protein_sha'],d['protein_sha']);features[arm]=z['features'].copy();assert np.isfinite(features[arm]).all()
    pi,ci,y=d['protein_index'],d['compound_index'],d['label'];g=d['groups'][pi]
    ug=np.array(sorted(set(d['groups'])));np.random.RandomState(4110).shuffle(ug);held=set(ug[:len(ug)//5]);tr=np.flatnonzero([x not in held for x in g]);va=np.flatnonzero([x in held for x in g])
    tg=np.array(sorted(set(g[tr])));np.random.RandomState(4114).shuffle(tg);fold={x:i%3 for i,x in enumerate(tg)}
    prov=json.loads((f/'provenance.json').read_text());conf=np.array(prov['mask_counts'])/np.array([len(s) for s in d['protein_sequence']]);common=np.column_stack([conf,np.log1p([len(s) for s in d['protein_sequence']])])
    protocol={'evidence':'ENGINEERING_ONLY_FROZEN_TRAIN_INTERNAL_HOLDOUT','arms':ARMS,'scales':SCALES,'selection':'3 inner group folds; macro RMSE; tie favors lower scale; alpha=1; fixed PCA/SVD seed 5121','split_seed':4110,'fit_rows':len(tr),'eval_rows':len(va),'eval_groups':len(held),'bundle_sha256':sha(b/'features.npz'),'feature_hashes':{arm:sha(f/(arm+'.npz')) for arm in ARMS},'design':'Morgan L2 + sequence 3/4mer TFIDF*.25 + shared mask fraction/log length*.1; pretrained PCA32 and compound SVD32 outer product scaled by block dimension; train-only unique-molecule and unique-protein transforms','limitations':['Previously inspected holdout; exploratory, not independent test','Frozen pooled 35M representations, not full GenSPARC','SaProt vs ESM2 confounds pretraining; real vs shuffled is the within-model structural control','Shuffled tokens can be out of distribution']}
    (out/'protocol.json').write_text(json.dumps(protocol,indent=2));print('PROTOCOL LOCKED',flush=True)
    fp=normalize(csr_matrix(d['fp']))
    def blocks(fit,ev):
        # Match original reference TFIDF row weighting; vocabulary only fit rows.
        vec=TfidfVectorizer(analyzer='char',ngram_range=(3,4),max_features=4096,sublinear_tf=True,dtype=np.float32)
        pt=vec.fit_transform(d['protein_sequence'][pi[fit]]);pv=vec.transform(d['protein_sequence'][pi[ev]])
        ps=StandardScaler().fit(common[np.unique(pi[fit])]);co=ps.transform(common).astype('float32')*.1
        bt=hstack([fp[ci[fit]],.25*pt,csr_matrix(co[pi[fit]])],format='csr');bv=hstack([fp[ci[ev]],.25*pv,csr_matrix(co[pi[ev]])],format='csr')
        sv=TruncatedSVD(n_components=32,random_state=5121).fit(fp[np.unique(ci[fit])]);chem=sv.transform(fp);cs=StandardScaler().fit(chem[np.unique(ci[fit])]);chem=cs.transform(chem).astype('float32')
        extras={}
        for arm in ARMS:
            raw=features[arm];ps=StandardScaler().fit(raw[np.unique(pi[fit])]);p=ps.transform(raw)
            pc=PCA(n_components=32,svd_solver='full').fit(p[np.unique(pi[fit])]);p=pc.transform(p);pstd=StandardScaler().fit(p[np.unique(pi[fit])]);p=pstd.transform(p).astype('float32')
            def ext(ix):
                interaction=np.einsum('bi,bj->bij',chem[ci[ix]],p[pi[ix]]).reshape(len(ix),-1)/32
                return csr_matrix(np.concatenate([p[pi[ix]]/np.sqrt(32),interaction],axis=1))
            extras[arm]=(ext(fit),ext(ev))
        return bt,bv,extras
    def predict(bt,bv,fit,ext=None,scale=0.):
        if scale:bt=hstack([bt,ext[0]*scale],format='csr');bv=hstack([bv,ext[1]*scale],format='csr')
        mu=y[fit].mean();sd=y[fit].std();reg=Ridge(alpha=1,solver='lsqr',tol=1e-5);reg.fit(bt,(y[fit]-mu)/sd);return reg.predict(bv)*sd+mu
    scores={arm:{str(s):[] for s in SCALES} for arm in ARMS}
    for k in range(3):
        fit=np.array([i for i in tr if fold[g[i]]!=k]);ev=np.array([i for i in tr if fold[g[i]]==k]);bt,bv,ex=blocks(fit,ev);base=predict(bt,bv,fit)
        for arm in ARMS:
            for s in SCALES:
                p=base if s==0 else predict(bt,bv,fit,ex[arm],s)
                # Store per-group errors to weight groups equally across folds.
                scores[arm][str(s)].extend([float(np.sqrt(np.mean((y[ev][g[ev]==v]-p[g[ev]==v])**2))) for v in np.unique(g[ev])])
        print('INNER FOLD',k+1,flush=True)
    chosen={arm:min(SCALES,key=lambda s:(np.mean(scores[arm][str(s)]),s)) for arm in ARMS}
    (out/'selection.json').write_text(json.dumps({'chosen':chosen,'scores':{arm:{s:float(np.mean(v)) for s,v in vals.items()} for arm,vals in scores.items()}},indent=2))
    bt,bv,ex=blocks(tr,va);pred={'baseline':predict(bt,bv,tr)}
    for arm in ARMS:pred[arm]=predict(bt,bv,tr,ex[arm],chosen[arm])
    result={'protocol':protocol,'selected_scales':chosen,'metrics':{arm:metrics(y[va],p,g[va]) for arm,p in pred.items()},'contrasts':{}}
    groups=np.unique(g[va]);counts=np.array([np.sum(g[va]==v) for v in groups]);errors={arm:np.array([np.mean((y[va][g[va]==v]-p[g[va]==v])**2) for v in groups]) for arm,p in pred.items()};rng=np.random.RandomState(5122);ix=rng.randint(len(groups),size=(5000,len(groups)))
    for other in ['baseline','esm2_sequence','saprot_shuffled']:
        ea,eb=errors['saprot_real'],errors[other];macro=(np.sqrt(ea[ix])-np.sqrt(eb[ix])).mean(1);pool=np.sqrt((ea[ix]*counts[ix]).sum(1)/counts[ix].sum(1))-np.sqrt((eb[ix]*counts[ix]).sum(1)/counts[ix].sum(1))
        result['contrasts']['real_minus_'+other]={'macro_delta':float((np.sqrt(ea)-np.sqrt(eb)).mean()),'macro_ci95':np.percentile(macro,[2.5,97.5]).tolist(),'pooled_delta':result['metrics']['saprot_real']['pooled_rmse']-result['metrics'][other]['pooled_rmse'],'pooled_ci95':np.percentile(pool,[2.5,97.5]).tolist()}
    np.savez_compressed(out/'predictions_LOCAL.npz',**pred,source_row=d['source_row'][va]);(out/'results.json').write_text(json.dumps(result,indent=2));print(json.dumps(result['metrics']),flush=True)
if __name__=='__main__':
    with threadpool_limits(limits=2):main()
