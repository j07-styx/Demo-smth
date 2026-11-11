"""Matched experimental arms on an explicit TRAIN/DEV pocket feature bundle.

No automatic pocket discovery or loading of reserved-test arrays. NPZ contract
and manifest are documented in research/pocket_repair_20261110/README.md.
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import numpy as np
import torch
from dynacpi.pocket_interaction_dev import PocketInteractionRepair, shuffled_coordinates


def load_bundle(path, manifest_path):
    manifest=json.loads(Path(manifest_path).read_text(encoding='utf-8'))
    if manifest.get('evidence_status') != 'ENGINEERING_ONLY':
        raise ValueError('This runner accepts ENGINEERING_ONLY bundles only')
    if not manifest.get('pocket_source') or manifest.get('pocket_selection_uses_labels') is not False:
        raise ValueError('Require documented label-independent pocket source')
    digest=hashlib.sha256(Path(path).read_bytes()).hexdigest()
    if digest != manifest.get('npz_sha256'): raise ValueError('Bundle checksum mismatch')
    with np.load(path,allow_pickle=False) as z:
        required={'compound','residues','valid','coords','pocket','protein_index','label','role','group'}
        if set(z.files)!=required: raise ValueError('Unexpected bundle arrays (reserved-test arrays forbidden)')
        d={k:z[k].copy() for k in z.files}
    if d['label'].ndim!=1: raise ValueError('Labels must be a vector')
    n=len(d['label']);p=len(d['residues'])
    if d['role'].shape!=(n,) or set(d['role'].tolist())!={'train','dev'}:
        raise ValueError('Bundle must contain train/dev only')
    ix=d['protein_index']
    if ix.shape!=(n,) or ix.dtype.kind not in 'iu' or (ix<0).any() or (ix>=p).any():
        raise ValueError('Invalid protein indices')
    if d['compound'].ndim!=2 or len(d['compound'])!=n or d['group'].shape!=(p,):
        raise ValueError('Pair/protein count mismatch')
    if d['residues'].ndim!=3 or d['valid'].shape!=d['residues'].shape[:2] or d['pocket'].shape!=d['valid'].shape or d['coords'].shape!=(*d['valid'].shape,3):
        raise ValueError('Misaligned residue arrays')
    if d['valid'].dtype!=bool or d['pocket'].dtype!=bool:
        raise ValueError('Masks must be boolean')
    if not np.isfinite(d['label']).all() or not np.isfinite(d['compound']).all():
        raise ValueError('Nonfinite labels/chemistry')
    tr=d['role']=='train';dv=~tr
    if set(d['group'][ix[tr]]) & set(d['group'][ix[dv]]): raise ValueError('Protein-group leakage')
    return d,manifest,digest


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--bundle',required=True);ap.add_argument('--manifest',required=True)
    ap.add_argument('--out',required=True);ap.add_argument('--epochs',type=int,default=5)
    ap.add_argument('--seeds',type=int,nargs='+',default=[2931,2932,2933])
    ap.add_argument('--width',type=int,default=64);ap.add_argument('--device',default='cpu')
    args=ap.parse_args()
    if args.epochs<1 or args.width<1 or len(set(args.seeds))!=len(args.seeds):
        ap.error('Positive epochs/width and distinct seeds required')
    d,manifest,digest=load_bundle(args.bundle,args.manifest)
    out=Path(args.out);out.mkdir(parents=True,exist_ok=False)
    torch.set_num_threads(1)
    device=torch.device(args.device)
    tensor={k:torch.as_tensor(d[k],device=device,dtype=torch.bool if k in ('valid','pocket') else torch.long if k=='protein_index' else torch.float32)
            for k in ('compound','residues','valid','pocket','coords','protein_index','label')}
    train=np.flatnonzero(d['role']=='train');dev=np.flatnonzero(d['role']=='dev')
    mean=float(d['label'][train].mean());std=max(float(d['label'][train].std()),1e-6)
    shuffled=shuffled_coordinates(tensor['coords'],tensor['pocket'])
    report={'evidence_status':'ENGINEERING_ONLY','bundle_sha256':digest,'manifest':manifest,
            'args':vars(args),'selection':'fixed final epoch, no dev checkpoint selection',
            'label_mean_train':mean,'label_std_train':std,'runs':[]}
    for seed in args.seeds:
        for arm,mode,xyz in [('base','base',tensor['coords']),('pocket_sequence','sequence',tensor['coords']),
                             ('real_geometry','geometry',tensor['coords']),('shuffled_geometry','geometry',shuffled)]:
            torch.manual_seed(seed)
            model=PocketInteractionRepair(d['compound'].shape[1],d['residues'].shape[2],args.width).to(device)
            opt=torch.optim.AdamW(model.parameters(),lr=3e-4,weight_decay=1e-4)
            rng=np.random.RandomState(seed)
            def predict(ids):
                ids=torch.as_tensor(ids,device=device,dtype=torch.long);p=tensor['protein_index'][ids]
                return model(tensor['compound'][ids],tensor['residues'][p],tensor['valid'][p],xyz[p],tensor['pocket'][p],mode)
            for _ in range(args.epochs):
                model.train();order=rng.permutation(train)
                for start in range(0,len(order),16):
                    ids=order[start:start+16];opt.zero_grad()
                    loss=((predict(ids)['prediction']-(tensor['label'][ids]-mean)/std)**2).mean()
                    loss.backward();torch.nn.utils.clip_grad_norm_(model.parameters(),5.);opt.step()
            model.eval()
            with torch.no_grad():
                pred=torch.cat([predict(dev[j:j+16])['prediction'] for j in range(0,len(dev),16)]).cpu().numpy()*std+mean
            err=(pred-d['label'][dev])**2;groups=d['group'][d['protein_index'][dev]]
            run={'seed':seed,'arm':arm,'rmse':float(np.sqrt(err.mean())),
                 'group_macro_rmse':float(np.mean([np.sqrt(err[groups==g].mean()) for g in sorted(set(groups))])),
                 'parameters':sum(x.numel() for x in model.parameters())}
            torch.save({'state_dict':model.state_dict(),'label_mean':mean,'label_std':std,'run':run,
                        'compound_dim':d['compound'].shape[1],'residue_dim':d['residues'].shape[2],
                        'width':args.width,'bundle_sha256':digest},out/f'{arm}_{seed}.pt')
            np.savez_compressed(out/f'{arm}_{seed}_dev.npz',prediction=pred,row_index=dev)
            report['runs'].append(run);(out/'results.json').write_text(json.dumps(report,indent=2))
            print(json.dumps(run),flush=True)


if __name__=='__main__':main()
