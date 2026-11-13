"""Explicit edges between sampled residues; identical raw ESM node features."""
import argparse,json,hashlib
from pathlib import Path
import numpy as np
import torch
from scipy.spatial import cKDTree
from transformers import EsmModel,EsmTokenizer
from cache_pretrained_structure_dev import digest,load_module

def graph(xyz,pos,spatial):
    d=np.linalg.norm(xyz[:,None,:]-xyz[None,:,:],axis=-1) if spatial else np.abs(pos[:,None]-pos[None,:])*3.8
    ranked=d.copy();np.fill_diagonal(ranked,np.inf);ix=np.argsort(ranked,axis=1,kind='stable')[:,:16];v=np.take_along_axis(d,ix,axis=1)
    radial=np.exp(-((v[...,None]-np.linspace(2,32,12))/3)**2)
    attr=np.concatenate([radial,np.log1p(v)[...,None]/np.log(101),np.stack([v<8,v<12,v<20],axis=-1)],axis=-1)
    return ix,attr.astype('float32')

def validate():
    rng=np.random.RandomState(6300);x=rng.randn(40,3)*10;pos=np.arange(40);q=np.linalg.qr(rng.randn(3,3))[0]
    ix,a=graph(x,pos,True);iy,b=graph(x@q+5,pos,True);assert np.array_equal(ix,iy) and np.allclose(a,b,atol=1e-5)
    iy,b=graph(x[rng.permutation(40)],pos,True);assert not np.array_equal(ix,iy)
    ix,a=graph(x,pos,False);iy,b=graph(x@q+5,pos,False);assert np.array_equal(ix,iy) and np.allclose(a,b)
    assert a.shape==(40,16,16);assert not (ix==np.arange(40)[:,None]).any()
    return {'rigid_motion_invariance':True,'coordinate_corruption_changes_graph':True,'sequence_control_ignores_coordinates':True,'no_self_edges':True}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--source-workspace',required=True);ap.add_argument('--cache',required=True);ap.add_argument('--out',required=True);a=ap.parse_args();root=Path(a.source_workspace);cache=Path(a.cache);out=Path(a.out);out.mkdir(parents=True,exist_ok=False)
    checks=validate();pr=json.loads((cache/'provenance.json').read_text());tokens=json.loads((cache/'tokens_LOCAL.json').read_text());hashes=tokens['protein_sha'];seqs=[''.join(t[0] for t in p) for p in tokens['real']]
    records={r['sequence_sha256']:r for r in json.loads((root/'research/structure_audit_20261110/structure_manifest.json').read_text())['records']};parser=load_module(root/'dynacpi/structure_descriptors_dev.py')
    folder=cache/'models/esm2'
    for name,h in pr['models']['esm2']['files'].items():assert digest(folder/name)==h
    torch.set_num_threads(2);device='cuda' if torch.cuda.is_available() else 'cpu'
    if device=='cuda':torch.cuda.set_per_process_memory_fraction(.25)
    state=torch.load(folder/'pytorch_model.bin',map_location='cpu',weights_only=True);model=EsmModel.from_pretrained(str(folder),state_dict=state,add_pooling_layer=False).to(device).eval();del state;tokenizer=EsmTokenizer.from_pretrained(str(folder))
    names=['sequence_neighborhood','spatial_neighborhood','shuffled_coordinates'];edges={n:np.zeros((len(hashes),96,16,16),np.float16) for n in names};indices={n:np.zeros((len(hashes),96,16),np.int16) for n in names};features={n:np.zeros((len(hashes),96,480),np.float32) for n in names};mask=np.zeros((len(hashes),96),bool);positions=np.full((len(hashes),96),-1,int);rng=np.random.RandomState(6201);overlaps=[];coverage=[];mean_error=0.
    with np.load(cache/'esm2_sequence.npz') as z:old=z['features'];assert z['protein_sha'].tolist()==hashes
    for i,(sh,seq) in enumerate(zip(hashes,seqs)):
        raw=(cache/'pdb'/(sh+'.pdb')).read_bytes();rec=records[sh];aa,ca,cb,pl=parser.parse_pdb(raw.decode());mapping=json.loads((root/'data/structure_probe_balm_20261109/mappings'/rec['mapping_file']).read_text());bi=np.array(mapping['balm_idx']);ai=np.array(mapping['af_idx']);assert all(seq[b]==aa[j] for b,j in zip(bi,ai));keep=pl[ai]>=70;bi=bi[keep];ai=ai[keep];assert len(ai)>=30
        parts=[]
        for start in range(0,len(seq),510):
            chunk=seq[start:start+510];enc=tokenizer(chunk,return_tensors='pt');assert enc['input_ids'].shape[1]==len(chunk)+2
            with torch.inference_mode():parts.append(model(**{k:v.to(device) for k,v in enc.items()}).last_hidden_state[0,1:-1].float().cpu().numpy())
        full=np.concatenate(parts);mean_error=max(mean_error,float(np.max(np.abs(full.mean(0)-old[i]))));h=full[bi];xyz=ca[ai];centers=np.unique(np.linspace(0,len(bi)-1,min(96,len(bi))).astype(int));n=len(centers);mask[i,:n]=True;positions[i,:n]=bi[centers]
        coords=xyz[centers];perm=rng.permutation(n)
        graphs=[graph(coords,bi[centers],False),graph(coords,bi[centers],True),graph(coords[perm],bi[centers],True)]
        for name,(neighbors,edge) in zip(names,graphs):
            features[name][i,:n]=h[centers];indices[name][i,:n]=neighbors;edges[name][i,:n]=edge
        overlaps.extend([len(set(x)&set(y))/len(x) for x,y in zip(graphs[0][0],graphs[1][0])]);coverage.append(len(bi)/len(seq))
        if (i+1)%25==0:print('PROTEINS',i+1,flush=True)
    assert mean_error<1e-4
    manifest={'evidence':'LABEL_FREE_MATCHED_NEIGHBORHOOD_CACHE','encoder':'same frozen ESM2 35M for all arms','parent_provenance_sha256':digest(cache/'provenance.json'),'neighbors':16,'edge_features':'12 distance RBFs, log distance, contacts at 8/12/20 angstrom; sequence control uses 3.8*index separation','centers':'up to 96 uniform among mapped pLDDT>=70 residues, shared all arms','mean_sequence_spatial_neighbor_overlap':float(np.mean(overlaps)),'mean_confident_sequence_coverage':float(np.mean(coverage)),'old_mean_max_error':mean_error,'unit_checks':checks,'features':{},'limitations':['Uniform centers, not binding-pocket annotations','Protein-only coordinates, no ligand pose','Reference structure mappings not verified assay constructs','One fixed coordinate permutation per protein']}
    for name,values in features.items():
        p=out/(name+'.npz');np.savez_compressed(p,features=values,edges=edges[name],neighbors=indices[name],valid=mask,positions=positions,protein_sha=np.array(hashes));manifest['features'][name]={'sha256':digest(p)}
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2));print('COMPLETE',manifest['mean_sequence_spatial_neighbor_overlap'],flush=True)
if __name__=='__main__':main()
