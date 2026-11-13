"""Same ESM residue features; change only spatial/sequence neighbor assignment."""
import argparse,json,hashlib
from pathlib import Path
import numpy as np
import torch
from scipy.spatial import cKDTree
from transformers import EsmModel,EsmTokenizer
from cache_pretrained_structure_dev import digest,load_module

def pool(h,xyz,pos,centers,spatial):
    k=min(16,len(pos)-1);assert k>0
    if spatial:
        candidates=cKDTree(xyz).query(xyz[centers],k=k+1)[1]
        near=np.stack([ix[ix!=c][:k] for c,ix in zip(centers,candidates)])
    else:
        distances=np.abs(pos[centers,None]-pos[None,:]).astype(float);distances[np.arange(len(centers)),centers]=np.inf;near=np.argsort(distances,axis=1,kind='stable')[:,:k]
    return .5*(h[centers]+h[near].mean(1)),near

def validate():
    rng=np.random.RandomState(6200);x=rng.randn(40,3);h=rng.randn(40,9);pos=np.arange(40);c=np.arange(0,40,2);q=np.linalg.qr(rng.randn(3,3))[0]
    a,ix=pool(h,x,pos,c,True);b,iy=pool(h,x@q+5,pos,c,True);assert np.array_equal(ix,iy) and np.allclose(a,b)
    b,_=pool(h,x[rng.permutation(40)],pos,c,True);assert not np.allclose(a,b)
    b,_=pool(h,x,pos,c,False);d,_=pool(h,x@q+5,pos,c,False);assert np.allclose(b,d)
    return {'rigid_motion_invariance':True,'coordinate_corruption_changes_pool':True,'sequence_control_ignores_coordinates':True}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--source-workspace',required=True);ap.add_argument('--cache',required=True);ap.add_argument('--out',required=True);a=ap.parse_args();root=Path(a.source_workspace);cache=Path(a.cache);out=Path(a.out);out.mkdir(parents=True,exist_ok=False)
    checks=validate();pr=json.loads((cache/'provenance.json').read_text());tokens=json.loads((cache/'tokens_LOCAL.json').read_text());hashes=tokens['protein_sha'];seqs=[''.join(t[0] for t in p) for p in tokens['real']]
    records={r['sequence_sha256']:r for r in json.loads((root/'research/structure_audit_20261110/structure_manifest.json').read_text())['records']};parser=load_module(root/'dynacpi/structure_descriptors_dev.py')
    folder=cache/'models/esm2'
    for name,h in pr['models']['esm2']['files'].items():assert digest(folder/name)==h
    torch.set_num_threads(2);device='cuda' if torch.cuda.is_available() else 'cpu'
    if device=='cuda':torch.cuda.set_per_process_memory_fraction(.25)
    state=torch.load(folder/'pytorch_model.bin',map_location='cpu',weights_only=True);model=EsmModel.from_pretrained(str(folder),state_dict=state,add_pooling_layer=False).to(device).eval();del state;tokenizer=EsmTokenizer.from_pretrained(str(folder))
    names=['sequence_neighborhood','spatial_neighborhood','shuffled_coordinates'];features={n:np.zeros((len(hashes),96,480),np.float32) for n in names};mask=np.zeros((len(hashes),96),bool);positions=np.full((len(hashes),96),-1,int);rng=np.random.RandomState(6201);overlaps=[];coverage=[];mean_error=0.
    with np.load(cache/'esm2_sequence.npz') as z:old=z['features'];assert z['protein_sha'].tolist()==hashes
    for i,(sh,seq) in enumerate(zip(hashes,seqs)):
        raw=(cache/'pdb'/(sh+'.pdb')).read_bytes();rec=records[sh];aa,ca,cb,pl=parser.parse_pdb(raw.decode());mapping=json.loads((root/'data/structure_probe_balm_20261109/mappings'/rec['mapping_file']).read_text());bi=np.array(mapping['balm_idx']);ai=np.array(mapping['af_idx']);assert all(seq[b]==aa[j] for b,j in zip(bi,ai));keep=pl[ai]>=70;bi=bi[keep];ai=ai[keep];assert len(ai)>=30
        parts=[]
        for start in range(0,len(seq),510):
            chunk=seq[start:start+510];enc=tokenizer(chunk,return_tensors='pt');assert enc['input_ids'].shape[1]==len(chunk)+2
            with torch.inference_mode():parts.append(model(**{k:v.to(device) for k,v in enc.items()}).last_hidden_state[0,1:-1].float().cpu().numpy())
        full=np.concatenate(parts);mean_error=max(mean_error,float(np.max(np.abs(full.mean(0)-old[i]))));h=full[bi];xyz=ca[ai];centers=np.unique(np.linspace(0,len(bi)-1,min(96,len(bi))).astype(int));n=len(centers);mask[i,:n]=True;positions[i,:n]=bi[centers]
        seqpool,ns=pool(h,xyz,bi,centers,False);geopool,ng=pool(h,xyz,bi,centers,True);badpool,_=pool(h,xyz[rng.permutation(len(xyz))],bi,centers,True)
        for name,value in zip(names,[seqpool,geopool,badpool]):features[name][i,:n]=value
        overlaps.extend([len(set(x)&set(y))/len(x) for x,y in zip(ns,ng)]);coverage.append(len(bi)/len(seq))
        if (i+1)%25==0:print('PROTEINS',i+1,flush=True)
    assert mean_error<1e-4
    manifest={'evidence':'LABEL_FREE_MATCHED_NEIGHBORHOOD_CACHE','encoder':'same frozen ESM2 35M for all arms','parent_provenance_sha256':digest(cache/'provenance.json'),'neighbors':16,'center_weight':.5,'neighbor_mean_weight':.5,'centers':'up to 96 uniform among mapped pLDDT>=70 residues, shared all arms','mean_sequence_spatial_neighbor_overlap':float(np.mean(overlaps)),'mean_confident_sequence_coverage':float(np.mean(coverage)),'old_mean_max_error':mean_error,'unit_checks':checks,'features':{},'limitations':['Uniform centers, not binding-pocket annotations','Protein-only coordinates, no ligand pose','Reference structure mappings not verified assay constructs','One fixed coordinate permutation per protein']}
    for name,values in features.items():
        p=out/(name+'.npz');np.savez_compressed(p,features=values,valid=mask,positions=positions,protein_sha=np.array(hashes));manifest['features'][name]={'sha256':digest(p)}
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2));print('COMPLETE',manifest['mean_sequence_spatial_neighbor_overlap'],flush=True)
if __name__=='__main__':main()
