"""Label-free, ragged full-residue cache. All protein positions, no sampling."""
import argparse,json
from pathlib import Path
import numpy as np
import torch
from transformers import EsmModel,EsmTokenizer
from cache_pretrained_structure_dev import digest

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--cache',required=True);ap.add_argument('--sampled',required=True);ap.add_argument('--out',required=True);a=ap.parse_args()
    root=Path(a.cache);out=Path(a.out);out.mkdir(parents=True,exist_ok=False)
    pr=json.loads((root/'provenance.json').read_text());tokens=json.loads((root/'tokens_LOCAL.json').read_text())
    hashes=tokens['protein_sha'];seqs=[''.join(t[0] for t in p) for p in tokens['real']]
    offsets=np.r_[0,np.cumsum([len(s) for s in seqs])]
    torch.set_num_threads(2);device='cuda' if torch.cuda.is_available() else 'cpu'
    if device=='cuda':torch.cuda.set_per_process_memory_fraction(.25)
    manifest={'evidence':'LABEL_FREE_FULL_RESIDUE_CACHE','parent_provenance_sha256':digest(root/'provenance.json'),'proteins':len(seqs),'residues':int(offsets[-1]),'layout':'features[offsets[i]:offsets[i+1]] follows exact protein sequence order','limitations':['510-residue nonoverlapping encoder windows; no context across window boundaries','Preserving all sequence positions does not verify assayed constructs or structural confidence','No affinity labels used'],'features':{}}
    (out/'protocol.json').write_text(json.dumps(manifest,indent=2))
    for kind in ['saprot','esm2']:
        folder=root/'models'/kind
        for name,h in pr['models'][kind]['files'].items():assert digest(folder/name)==h
        state=torch.load(folder/'pytorch_model.bin',map_location='cpu',weights_only=True)
        model=EsmModel.from_pretrained(str(folder),state_dict=state,add_pooling_layer=False).to(device).eval();del state
        tokenizer=EsmTokenizer.from_pretrained(str(folder))
        for mode in (['real','shuffled'] if kind=='saprot' else ['sequence']):
            name=kind+'_'+mode
            features=np.zeros((int(offsets[-1]),480),np.float32)
            with np.load(root/(name+'.npz')) as z:means=z['features']
            with np.load(Path(a.sampled)/(name+'.npz')) as z:
                sampled=z['features'];valid=z['valid'];positions=z['positions']
                assert np.array_equal(z['protein_sha'],hashes)
            mean_error=0.;sample_error=0.
            for i,seq in enumerate(seqs):
                units=tokens[mode][i] if kind=='saprot' else list(seq);parts=[]
                assert len(units)==len(seq)
                for j in range(0,len(units),510):
                    chunk=units[j:j+510];enc=tokenizer(''.join(chunk),return_tensors='pt')
                    assert enc['input_ids'].shape[1]==len(chunk)+2
                    with torch.inference_mode():
                        h=model(**{k:v.to(device) for k,v in enc.items()}).last_hidden_state[0,1:-1].float().cpu().numpy()
                    parts.append(h)
                r=np.concatenate(parts);assert len(r)==len(seq) and np.isfinite(r).all()
                features[offsets[i]:offsets[i+1]]=r
                mean_error=max(mean_error,float(np.max(np.abs(r.mean(0)-means[i]))))
                sample_error=max(sample_error,float(np.max(np.abs(r[positions[i][valid[i]]]-sampled[i][valid[i]]))))
                if (i+1)%50==0:print(name,i+1,'/',len(seqs),flush=True)
            assert mean_error<1e-4 and sample_error<1e-4,(mean_error,sample_error)
            dest=out/(name+'.npz')
            np.savez_compressed(dest,features=features,offsets=offsets,protein_sha=np.array(hashes))
            manifest['features'][name]={'sha256':digest(dest),'mean_max_error':mean_error,'sampled_token_max_error':sample_error}
            (out/'manifest.json').write_text(json.dumps(manifest,indent=2));print('CACHED',name,flush=True)
        del model
        if device=='cuda':torch.cuda.empty_cache()
    assert len(manifest['features'])==3
    print('COMPLETE',flush=True)
if __name__=='__main__':main()
