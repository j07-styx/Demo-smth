"""Small real-data fit diagnostic. Reused TRAIN only; assay comparability unknown."""
import argparse,hashlib,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import numpy as np
import pyarrow as pa
import torch
from dynacpi.atom_residue_interaction_dev import AtomResidueInteraction
from dynacpi.molecular_graph_dev import molecular_graph,collate_graphs

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def stats(y,p,protein):
    e=y-p;within=e.copy()
    for x in np.unique(protein):within[protein==x]-=within[protein==x].mean()
    return {'rmse':float(np.sqrt(np.mean(e**2))),'within_protein_rmse':float(np.sqrt(np.mean(within**2)))}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--bundle',required=True);ap.add_argument('--residues',required=True);ap.add_argument('--source',required=True);ap.add_argument('--out',required=True);a=ap.parse_args()
    out=Path(a.out);out.mkdir(parents=True,exist_ok=False)
    root=Path(a.bundle);meta=json.loads((root/'manifest.json').read_text())
    assert meta['evidence']=='ENGINEERING_ONLY_BALM_FROZEN_TRAIN' and sha(root/'features.npz')==meta['bundle_sha256']
    with np.load(root/'features.npz') as z:d={k:z[k] for k in ['source_row','label','protein_index','compound_index','groups','protein_sha']}
    # Materialize only chemical and sequence metadata at the already verified TRAIN row indices.
    with pa.memory_map(a.source,'r') as h:
        tab=pa.ipc.open_stream(h).read_all().select(['Drug','Target']).take(pa.array(d['source_row'].astype('int64')))
    smiles=tab['Drug'].to_pylist();seq=tab['Target'].to_pylist();pi=d['protein_index']
    assert all(hashlib.sha256(s.encode()).hexdigest()==d['protein_sha'][p] for s,p in zip(seq,pi))
    graph={};eligible=[]
    for i,s in enumerate(smiles):
        if s not in graph:graph[s]=molecular_graph(s)
        # Explicit cohort eligibility, not truncation: preserve every atom in selected molecules.
        if len(graph[s][0])<=96:eligible.append(i)
    eligible=np.array(eligible);pg=d['groups'];groups=np.array(sorted(set(pg)));np.random.RandomState(4110).shuffle(groups)
    held=set(groups[::5])
    def panel(is_held):
        candidates=[p for p in sorted(set(pi[eligible])) if (pg[p] in held)==is_held]
        chosen=[];seen=set()
        for p in candidates:
            if pg[p] in seen:continue
            ix=eligible[pi[eligible]==p];unique=[];seenchem=set()
            for i in ix:
                if smiles[i] not in seenchem:unique.append(i);seenchem.add(smiles[i])
                if len(unique)==16:break
            if len(unique)==16:
                chosen.extend(unique);seen.add(pg[p])
                if len(seen)==4:break
        assert len(chosen)==64,'Insufficient eligible proteins'
        return np.array(chosen)
    tr,va=panel(False),panel(True);assert not set(pg[pi[tr]])&set(pg[pi[va]])
    idx=np.r_[tr,va];np.savez_compressed(out/'rows_LOCAL.npz',train_source_row=d['source_row'][tr],held_source_row=d['source_row'][va])
    ag,bg,am,fp=collate_graphs([graph[smiles[i]] for i in idx])
    torch.set_num_threads(2);device='cuda' if torch.cuda.is_available() else 'cpu'
    if device=='cuda':torch.cuda.set_per_process_memory_fraction(.25)
    tensors=[torch.tensor(x,device=device) for x in [ag,bg,am,fp]]
    ra,rb,mask,fingerprint=tensors
    y=d['label'][idx];mu=y[:64].mean();sd=max(y[:64].std(),1e-6)
    target=torch.tensor((y[:64]-mu)/sd,device=device)
    rm=json.loads((Path(a.residues)/'manifest.json').read_text())
    protocol={'evidence':'SMALL_REUSED_TRAIN_FIT_DIAGNOSTIC','seed':7133,'steps':200,'batch':8,'train_rows':64,'held_rows':64,'selection':'first four eligible distinct groups per role, 16 distinct SMILES per protein; at most 96 atoms, no atom truncation; no label-based selection','split':'outer fold zero, seed 4110; frozen TRAIN only','assay_comparability':'unknown; no pair-difference loss','limitations':['96 uniformly sampled residue tokens, not full protein coverage','Single seed, tiny selected panel, no performance claim','ESM vs SaProt comparison confounds pretraining with structure; SaProt shuffled is matched encoder control'],'bundle_sha256':sha(root/'features.npz'),'residue_manifest_sha256':sha(Path(a.residues)/'manifest.json'),'arms':['chemical_only','sequence','real','shuffled']}
    (out/'protocol.json').write_text(json.dumps(protocol,indent=2));print('LOCKED',flush=True)
    results={}
    for arm,name in [('chemical_only','saprot_real'),('sequence','esm2_sequence'),('real','saprot_real'),('shuffled','saprot_shuffled')]:
        path=Path(a.residues)/(name+'.npz');assert sha(path)==rm['features'][name]['sha256']
        with np.load(path) as z:
            assert np.array_equal(z['protein_sha'],d['protein_sha'])
            r=z['features'];valid=z['valid'];ptr=np.unique(pi[tr]);vals=r[ptr][valid[ptr]]
            r=(r-vals.mean(0))/np.maximum(vals.std(0),1e-4)
            r=r[pi[idx]];valid=valid[pi[idx]]
        if arm=='chemical_only':
            r=np.zeros((128,1,r.shape[-1]),np.float32);valid=np.ones((128,1),bool)
        rt=torch.tensor(r,device=device);mt=torch.tensor(valid,device=device)
        torch.manual_seed(7133);rng=np.random.RandomState(7133)
        model=AtomResidueInteraction(16,r.shape[-1],width=32).to(device)
        opt=torch.optim.AdamW(model.parameters(),lr=.001,weight_decay=.01)
        def predict(ix):return model(ra[ix],rb[ix],mask[ix],rt[ix],mt[ix],fingerprint[ix])[0]
        with torch.no_grad():initial=float(((predict(np.arange(8))-target[:8])**2).mean())
        for step in range(200):
            ix=rng.choice(64,8,replace=False);opt.zero_grad();loss=((predict(ix)-target[ix])**2).mean()
            assert torch.isfinite(loss);loss.backward();torch.nn.utils.clip_grad_norm_(model.parameters(),1.);opt.step()
        model.eval()
        with torch.no_grad():pred=np.concatenate([predict(np.arange(i,min(i+8,128))).cpu().numpy() for i in range(0,128,8)])*sd+mu
        assert np.isfinite(pred).all()
        results[arm]={'train':stats(y[:64],pred[:64],pi[tr]),'held':stats(y[64:],pred[64:],pi[va]),'initial_first_batch_standardized_mse':initial}
        torch.save(model.state_dict(),out/(arm+'_LOCAL.pt'));np.save(out/(arm+'_pred_LOCAL.npy'),pred)
        print(arm,json.dumps(results[arm]),flush=True)
    results['constant_train_mean']={'train':stats(y[:64],np.full(64,mu),pi[tr]),'held':stats(y[64:],np.full(64,mu),pi[va])}
    (out/'results.json').write_text(json.dumps(results,indent=2));print('COMPLETE',flush=True)
if __name__=='__main__':main()
