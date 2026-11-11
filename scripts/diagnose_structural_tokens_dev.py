"""Read-only chemistry and correspondence sensitivity of saved trial checkpoints.

Uses a synthetic cross-product of held-out group inputs; no affinity labels are
used in this diagnostic. Interventions may be out of distribution.
"""
import argparse,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import numpy as np
import torch
from dynacpi.structural_token_fusion_dev import StructuralTokenFusion

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--bundle-dir',required=True);ap.add_argument('--trial',required=True)
    a=ap.parse_args();root=Path(a.trial);result=json.loads((root/'results.json').read_text())
    with np.load(Path(a.bundle_dir)/'features.npz',allow_pickle=False) as z:
        d={k:z[k].copy() for k in z.files if k!='label'}
    with np.load(root/'split_LOCAL.npz') as z:
        dev=z['dev'];gm=z['geometry_mean'];gs=z['geometry_std']
    pp=np.unique(d['protein_index'][dev])[:16];cc=np.unique(d['compound_index'][dev])[:16]
    geo=(d['geometry']-gm)/gs;geo[~d['residue_valid']]=0
    shuffled=geo.copy();rng=np.random.RandomState(712)
    for p in pp:
        ix=np.flatnonzero(d['residue_valid'][p]);shuffled[p,ix]=geo[p,rng.permutation(ix)]
    pidx=np.repeat(pp,len(cc));cidx=np.tile(cc,len(pp));torch.set_num_threads(2)
    t={k:torch.as_tensor(d[k],dtype=torch.bool if k.endswith('valid') else torch.float32)
       for k in ('fp','atoms','atom_valid','sequence','residue_valid')}
    outputs=[]
    for seed in result['args']['seeds']:
        ck=torch.load(root/f'real_{seed}_LOCAL.pt',map_location='cpu',weights_only=True)
        m=StructuralTokenFusion(d['sequence'].shape[-1],geo.shape[-1],d['atoms'].shape[-1]);m.load_state_dict(ck['state_dict']);m.eval()
        def pred(mode,geometry):
            values=[]
            with torch.no_grad():
                for j in range(0,len(pidx),32):
                    p=pidx[j:j+32];c=cidx[j:j+32]
                    raw=m(t['fp'][c],t['atoms'][c],t['atom_valid'][c],t['sequence'][p],torch.tensor(geometry[p]),t['residue_valid'][p],mode)
                    # Report dimensionless head response for uncapped runs and
                    # normalized bounded response for capped runs; not pKd.
                    if result['args'].get('correction_cap') is not None:raw=torch.tanh(raw)
                    values.extend(raw.tolist())
            return np.array(values).reshape(len(pp),len(cc))
        real=pred('real',geo);without=pred('sequence',geo);scrambled=pred('real',shuffled)
        effect=real-without
        interaction=effect-effect.mean(0,keepdims=True)-effect.mean(1,keepdims=True)+effect.mean()
        with torch.no_grad():
            emb=m.fp(t['fp'][np.unique(d['compound_index'][dev])[:256]]).numpy()
        norm=emb/np.maximum(np.linalg.norm(emb,axis=1,keepdims=True),1e-12);cos=norm@norm.T
        s=np.linalg.svd(emb-emb.mean(0),compute_uv=False)**2;prob=s/max(s.sum(),1e-12)
        outputs.append({'seed':seed,'compound_cosine_mean':float(cos[~np.eye(len(cos),dtype=bool)].mean()),
            'compound_centered_effective_rank':float(np.exp(-(prob*np.log(prob+1e-12)).sum())),
            'geometry_effect_rms':float(np.sqrt(np.mean(effect**2))),
            'correspondence_shuffle_rms':float(np.sqrt(np.mean((real-scrambled)**2))),
            'interaction_fraction_of_geometry_effect_energy':float(np.sum(interaction**2)/max(np.sum(effect**2),1e-12))})
    report={'scope':'READ_ONLY_INTERVENTION_NO_LABELS_NO_ACCURACY_CLAIM','proteins':len(pp),'compounds':len(cc),'runs':outputs}
    (root/'mechanism.json').write_text(json.dumps(report,indent=2));print(json.dumps(report),flush=True)
if __name__=='__main__':main()
