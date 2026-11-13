"""Explicit ligand-conditioned edge attention with matched controls.
Fixed five epochs, two seeds, five TRAIN-only group folds; no model selection.
"""
import argparse,json,hashlib,os
os.environ.setdefault('OMP_NUM_THREADS','2')
from pathlib import Path
import numpy as np
import torch
from torch import nn
from scipy.sparse import csr_matrix,hstack
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import normalize,StandardScaler
from sklearn.linear_model import Ridge
from threadpoolctl import threadpool_limits
from evaluate_pretrained_structure_dev import metrics,sha

class ResidueHead(nn.Module):
    def __init__(self):
        super().__init__();self.chem=nn.Sequential(nn.Linear(2048,32),nn.GELU());self.res=nn.Sequential(nn.Linear(480,32),nn.LayerNorm(32));self.edge=nn.Sequential(nn.Linear(16,8),nn.Tanh());self.eq=nn.Linear(32,8);self.eb=nn.Linear(8,1);self.nq=nn.Linear(32,32);self.nk=nn.Linear(32,32);self.msg=nn.Linear(32,32);self.norm=nn.LayerNorm(32);self.q=nn.Linear(32,32);self.k=nn.Linear(32,32);self.head=nn.Sequential(nn.Linear(128,64),nn.GELU(),nn.Linear(64,1));nn.init.normal_(self.head[-1].weight,std=.01);nn.init.zeros_(self.head[-1].bias)
    def forward(self,fp,r,mask,mode='attention'):
        raw,attributes,neighbors=r;c=self.chem(fp);p=self.res(raw);batch=torch.arange(len(p),device=p.device)[:,None,None];v=p[batch,neighbors.long()];e=self.edge(attributes.float())
        score=(self.nq(p)[:,:,None,:]*self.nk(v)).sum(-1)/(32**.5)+self.eb(e).squeeze(-1)+(self.eq(c)[:,None,None,:]*e).sum(-1)/(8**.5)
        neighbor_valid=mask[batch,neighbors.long()];score=score.masked_fill(~neighbor_valid,-1e9);weights_local=score.softmax(-1);message=(weights_local[...,None]*v).sum(2);p=self.norm(p+.1*self.msg(message))
        w=mask.to(p.dtype);mean=(p*w[:,:,None]).sum(1)/w.sum(1,keepdim=True);logits=(self.q(c)[:,None,:]*self.k(p)).sum(-1)/(32**.5);weights=logits.masked_fill(~mask,-1e9).softmax(-1)
        context=(p*weights[:,:,None]).sum(1);delta=.25*torch.tanh(self.head(torch.cat([c,mean,context,c*context],-1)).squeeze(-1));return delta,weights

def validate_model():
    torch.manual_seed(6110);m=ResidueHead().eval();fp=torch.randn(3,2048);raw=torch.randn(3,7,480);mask=torch.ones(3,7,dtype=torch.bool);mask[:,-1]=False;e=torch.randn(3,7,3,16);neighbors=torch.tensor([[(i+j+1)%6 for j in range(3)] for i in range(7)])[None].repeat(3,1,1)
    with torch.no_grad():
        a,w=m(fp,(raw,e,neighbors),mask);perm=torch.randperm(7);inv=torch.argsort(perm);b,_=m(fp,(raw[:,perm],e[:,perm],inv[neighbors[:,perm]]),mask[:,perm]);assert torch.allclose(a,b,atol=1e-6)
        bad=raw.clone();bad[:,-1]=10000;b,_=m(fp,(bad,e,neighbors),mask);assert torch.allclose(a,b,atol=1e-6)
        b,_=m(fp,(raw,e*0,neighbors),mask);assert not torch.allclose(a,b,atol=1e-8)
        _,wb=m(fp.flip(0),(raw,e,neighbors),mask);assert not torch.allclose(w,wb);assert (a.abs()<=.25).all()
    m.train();m(fp,(raw,e,neighbors),mask)[0].sum().backward();assert m.edge[0].weight.grad.abs().sum()>0 and m.eq.weight.grad.abs().sum()>0
    return {'consistent_graph_permutation':True,'masked_residue_invariance':True,'edge_changes_output':True,'ligand_changes_attention':True,'nonzero_edge_and_ligand_edge_gradients':True,'bounded_correction':True}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--bundle-dir',required=True);ap.add_argument('--features',required=True);ap.add_argument('--global-cache',required=True);ap.add_argument('--out',required=True);a=ap.parse_args();out=Path(a.out);out.mkdir(parents=True,exist_ok=False)
    checks=validate_model();torch.set_num_threads(2);device='cuda' if torch.cuda.is_available() else 'cpu'
    if device=='cuda':torch.cuda.set_per_process_memory_fraction(.25)
    b=Path(a.bundle_dir);meta=json.loads((b/'manifest.json').read_text());assert meta['evidence']=='ENGINEERING_ONLY_BALM_FROZEN_TRAIN';assert sha(b/'features.npz')==meta['bundle_sha256']
    with np.load(b/'features.npz') as z:d={k:z[k] for k in ['fp','protein_sequence','protein_sha','protein_index','compound_index','label','source_row','groups']}
    fm=json.loads((Path(a.features)/'manifest.json').read_text());features={};edge={};near={};masks=None
    for name in ['sequence_neighborhood','spatial_neighborhood','shuffled_coordinates']:
        p=Path(a.features)/(name+'.npz');assert sha(p)==fm['features'][name]['sha256']
        with np.load(p) as z:
            assert np.array_equal(z['protein_sha'],d['protein_sha']);features[name]=z['features'];edge[name]=torch.tensor(z['edges'],device=device);near[name]=torch.tensor(z['neighbors'].astype('int64'),device=device);mask=z['valid']
            if masks is not None:assert np.array_equal(masks,mask)
            masks=mask
    arms={'sequence_attention':('sequence_neighborhood','attention'),'spatial_attention':('spatial_neighborhood','attention'),'shuffled_attention':('shuffled_coordinates','attention')};seeds=[6111,6112]
    pi,ci,y=d['protein_index'],d['compound_index'],d['label'];groups=d['groups'][pi];ug=np.array(sorted(set(d['groups'])));np.random.RandomState(4110).shuffle(ug)
    pr=json.loads((Path(a.global_cache)/'provenance.json').read_text());common=np.column_stack([np.array(pr['mask_counts'])/np.array([len(s) for s in d['protein_sequence']]),np.log1p([len(s) for s in d['protein_sequence']])]);fp=normalize(csr_matrix(d['fp']))
    protocol={'evidence':'EXPLORATORY_TRAIN_GROUP_CV','cache_semantics':'Same raw ESM nodes; learned ligand-conditioned edge messages; 16 spatial vs sequence neighbors vs coordinate permutation','arms':arms,'seeds':seeds,'epochs':5,'batches_per_epoch_max':64,'batch_size':32,'optimizer':'AdamW lr .0003 decay .01; grad clip 1','residual_cap':.25,'target':'raw-unit residual to three-fold group-cross-fitted shared ridge baseline','selection':'fixed final epoch, no validation tuning','outer_split_seed':4110,'device':device,'validation':checks,'bundle_sha256':sha(b/'features.npz'),'feature_manifest_sha256':sha(Path(a.features)/'manifest.json'),'limitations':['Reused TRAIN cohort, exploratory','96 uniformly sampled contextual residue embeddings, not verified binding pockets','Frozen encoders, no ligand pose','Bounded short training pilot; negative result does not exhaust architecture']}
    (out/'protocol.json').write_text(json.dumps(protocol,indent=2));print('LOCKED',flush=True)
    def ridge(fit,ev):
        vec=TfidfVectorizer(analyzer='char',ngram_range=(3,4),max_features=4096,sublinear_tf=True,dtype=np.float32);pt=vec.fit_transform(d['protein_sequence'][pi[fit]]);pv=vec.transform(d['protein_sequence'][pi[ev]])
        sc=StandardScaler().fit(common[np.unique(pi[fit])]);co=sc.transform(common).astype('float32')*.1;xt=hstack([fp[ci[fit]],.25*pt,csr_matrix(co[pi[fit]])],format='csr');xv=hstack([fp[ci[ev]],.25*pv,csr_matrix(co[pi[ev]])],format='csr');mu=y[fit].mean();sd=y[fit].std();reg=Ridge(alpha=1,solver='lsqr',tol=1e-5).fit(xt,(y[fit]-mu)/sd);return reg.predict(xv)*sd+mu
    base=np.full(len(y),np.nan);pred={arm:np.full((2,len(y)),np.nan) for arm in arms};runs=[];seen=np.zeros(len(y),int)
    tfp=torch.tensor(fp.toarray(),device=device);tm=torch.tensor(masks,device=device)
    for fold in range(5):
        held=set(ug[fold::5]);tr=np.flatnonzero([g not in held for g in groups]);va=np.flatnonzero([g in held for g in groups]);assert not set(groups[tr])&set(groups[va]);seen[va]+=1;base[va]=ridge(tr,va)
        tg=np.array(sorted(set(groups[tr])));np.random.RandomState(4114).shuffle(tg);inner={g:i%3 for i,g in enumerate(tg)};oof=np.full(len(y),np.nan)
        for k in range(3):
            fit=np.array([i for i in tr if inner[groups[i]]!=k]);ev=np.array([i for i in tr if inner[groups[i]]==k]);oof[ev]=ridge(fit,ev)
        assert np.isfinite(oof[tr]).all();target=torch.tensor((y[tr]-oof[tr]).astype('float32'),device=device);ptr=np.unique(pi[tr]);normalized={}
        for name,r in features.items():
            vals=r[ptr][masks[ptr]];mu=vals.mean(0);sd=np.maximum(vals.std(0),1e-4);normalized[name]=torch.tensor((r-mu)/sd,device=device)
        for si,seed in enumerate(seeds):
            for arm,(name,mode) in arms.items():
                torch.manual_seed(seed);rng=np.random.RandomState(seed);model=ResidueHead().to(device);opt=torch.optim.AdamW(model.parameters(),lr=3e-4,weight_decay=.01);r=normalized[name]
                for epoch in range(5):
                    order=rng.permutation(len(tr));model.train()
                    for start in range(0,min(len(tr),64*32),32):
                        j=order[start:start+32];ix=tr[j];opt.zero_grad();delta,_=model(tfp[ci[ix]],(r[pi[ix]],edge[name][pi[ix]],near[name][pi[ix]]),tm[pi[ix]],mode);loss=((delta-target[j])**2).mean();loss.backward();nn.utils.clip_grad_norm_(model.parameters(),1);opt.step()
                model.eval();deltas=[];coverage=[]
                with torch.no_grad():
                    for start in range(0,len(va),32):
                        ix=va[start:start+32];delta,w=model(tfp[ci[ix]],(r[pi[ix]],edge[name][pi[ix]],near[name][pi[ix]]),tm[pi[ix]],mode);deltas.extend(delta.cpu().numpy());coverage.extend((-(w*w.clamp_min(1e-12).log()).sum(1)).exp().div(tm[pi[ix]].sum(1)).cpu().numpy())
                pred[arm][si,va]=base[va]+np.array(deltas);run={'fold':fold,'seed':seed,'arm':arm,**metrics(y[va],pred[arm][si,va],groups[va]),'attention_effective_coverage':float(np.mean(coverage)),'correction_sd':float(np.std(deltas))};runs.append(run);torch.save(model.state_dict(),out/(str(fold)+'_'+arm+'_'+str(seed)+'_LOCAL.pt'));print(json.dumps(run),flush=True)
        (out/'runs.json').write_text(json.dumps(runs,indent=2))
    assert (seen==1).all() and np.isfinite(base).all();assert all(np.isfinite(p).all() for p in pred.values())
    means={arm:p.mean(0) for arm,p in pred.items()};result={'protocol':protocol,'rows':len(y),'groups':len(set(groups)),'baseline':metrics(y,base,groups),'ensemble_metrics':{arm:metrics(y,p,groups) for arm,p in means.items()},'seed_metrics':{arm:[metrics(y,p,groups) for p in ps] for arm,ps in pred.items()},'contrasts':{}}
    u=np.unique(groups);counts=np.array([sum(groups==g) for g in u]);err={arm:np.array([np.mean((y[groups==g]-p[groups==g])**2) for g in u]) for arm,p in dict(means,baseline=base).items()};ix=np.random.RandomState(5122).randint(len(u),size=(5000,len(u)))
    for other in ['baseline','sequence_attention','shuffled_attention']:
        ea,eb=err['spatial_attention'],err[other];md=np.sqrt(ea)-np.sqrt(eb);pool=np.sqrt((ea[ix]*counts[ix]).sum(1)/counts[ix].sum(1))-np.sqrt((eb[ix]*counts[ix]).sum(1)/counts[ix].sum(1));result['contrasts'][other]={'macro_delta':float(md.mean()),'macro_ci95':np.percentile(md[ix].mean(1),[2.5,97.5]).tolist(),'pooled_delta':float(np.sqrt(np.average(ea,weights=counts))-np.sqrt(np.average(eb,weights=counts))),'pooled_ci95':np.percentile(pool,[2.5,97.5]).tolist()}
    np.savez_compressed(out/'predictions_LOCAL.npz',**pred,baseline=base,source_row=d['source_row']);(out/'results.json').write_text(json.dumps(result,indent=2));print('COMPLETE',json.dumps(result['ensemble_metrics']),flush=True)
if __name__=='__main__':
    with threadpool_limits(limits=2):main()
