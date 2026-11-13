"""Label-free uniform residue cache from verified frozen pretrained encoders."""
import argparse,json,hashlib
from pathlib import Path
import numpy as np
import torch
from transformers import EsmModel,EsmTokenizer
from cache_pretrained_structure_dev import digest

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--cache',required=True);ap.add_argument('--out',required=True);a=ap.parse_args();root=Path(a.cache);out=Path(a.out);out.mkdir(parents=True,exist_ok=False)
    pr=json.loads((root/'provenance.json').read_text());tokens=json.loads((root/'tokens_LOCAL.json').read_text());hashes=tokens['protein_sha'];seqs=[''.join(t[0] for t in p) for p in tokens['real']]
    torch.set_num_threads(2);device='cuda' if torch.cuda.is_available() else 'cpu'
    if device=='cuda':torch.cuda.set_per_process_memory_fraction(.25)
    manifest={'evidence':'LABEL_FREE_RESIDUE_CACHE','parent_provenance_sha256':digest(root/'provenance.json'),'positions':'up to 96 uniformly spaced residues across full sequence, same positions in every arm','features':{},'device':device}
    for kind in ['saprot','esm2']:
        folder=root/'models'/kind
        for name,h in pr['models'][kind]['files'].items():assert digest(folder/name)==h
        state=torch.load(folder/'pytorch_model.bin',map_location='cpu',weights_only=True);model=EsmModel.from_pretrained(str(folder),state_dict=state,add_pooling_layer=False).to(device).eval();del state
        tokenizer=EsmTokenizer.from_pretrained(str(folder))
        for mode in (['real','shuffled'] if kind=='saprot' else ['sequence']):
            features=np.zeros((len(hashes),96,480),np.float32);valid=np.zeros((len(hashes),96),bool);positions=np.full((len(hashes),96),-1,int);max_error=0.
            with np.load(root/(kind+'_'+mode+'.npz')) as z:means=z['features']
            for i,seq in enumerate(seqs):
                units=tokens[mode][i] if kind=='saprot' else list(seq);parts=[]
                for j in range(0,len(units),510):
                    chunk=units[j:j+510];enc=tokenizer(''.join(chunk),return_tensors='pt');assert enc['input_ids'].shape[1]==len(chunk)+2
                    with torch.inference_mode():h=model(**{k:v.to(device) for k,v in enc.items()}).last_hidden_state[0,1:-1].float().cpu().numpy()
                    parts.append(h)
                residues=np.concatenate(parts);max_error=max(max_error,float(np.max(np.abs(residues.mean(0)-means[i]))));ix=np.unique(np.linspace(0,len(seq)-1,min(96,len(seq))).astype(int));n=len(ix)
                features[i,:n]=residues[ix];valid[i,:n]=True;positions[i,:n]=ix
            assert max_error<1e-4,('Previous mean cache mismatch',max_error)
            name=kind+'_'+mode;dest=out/(name+'.npz');np.savez_compressed(dest,features=features,valid=valid,positions=positions,protein_sha=np.array(hashes));manifest['features'][name]={'sha256':digest(dest),'mean_cache_max_error':max_error};print('CACHED',name,max_error,flush=True)
        del model
        if device=='cuda':torch.cuda.empty_cache()
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2))
if __name__=='__main__':main()
