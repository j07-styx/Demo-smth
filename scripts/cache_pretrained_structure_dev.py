"""Cache pinned ESM2/SaProt features for the previous TRAIN-only cohort.

Requires Transformers 4.44.2, torch, WSL Foldseek on Windows. No affinity labels
are loaded; the NPZ reader projects protein sequences/hashes only.
"""
import argparse,gzip,hashlib,importlib.util,json,subprocess,time,urllib.request
from pathlib import Path
import numpy as np
import torch
from transformers import EsmConfig,EsmModel,EsmTokenizer

MODELS={'saprot':('westlake-repl/SaProt_35M_AF2','316cd4017d29f4657b959365f24b57f1ee278912'),
        'esm2':('facebook/esm2_t12_35M_UR50D','6fbf070e65b0b7291e7bbcd451118c216cff79d8')}

def digest(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def linux(path):
    p=Path(path).resolve();return '/mnt/'+p.drive[0].lower()+p.as_posix()[2:]
def load_module(path):
    spec=importlib.util.spec_from_file_location('structure_parser',path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--source-workspace',required=True);ap.add_argument('--bundle-dir',required=True)
    ap.add_argument('--out',required=True);ap.add_argument('--foldseek',required=True)
    ap.add_argument('--device',default='cpu');a=ap.parse_args()
    root=Path(a.source_workspace);out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
    with np.load(Path(a.bundle_dir)/'features.npz',allow_pickle=False) as z:
        hashes=z['protein_sha'].tolist();sequences=z['protein_sequence'].tolist()
    mf=root/'research/structure_audit_20261110/structure_manifest.json'
    manifest=json.loads(mf.read_text(encoding='utf-8'));records={r['sequence_sha256']:r for r in manifest['records']}
    sd=load_module(root/'dynacpi/structure_descriptors_dev.py');pdbdir=out/'pdb';pdbdir.mkdir(exist_ok=True)
    arrays={};sources={}
    for sh,seq in zip(hashes,sequences):
        assert hashlib.sha256(seq.encode()).hexdigest()==sh
        rec=records[sh];c=next(c for c in rec['candidates'] if c.get('pdb_file') and
            (c.get('entryId')==rec['chosen_entry'] if rec.get('chosen_entry') else c['accession']==rec['chosen_accession']))
        raw=(root/c['pdb_file']).read_bytes();assert hashlib.sha256(raw).hexdigest()==c['pdb_sha256']
        if raw[:2]==bytes([31,139]):raw=gzip.decompress(raw)
        (pdbdir/(sh+'.pdb')).write_bytes(raw)
        aa,ca,cb,pl=sd.parse_pdb(raw.decode('utf-8'))
        mapping=json.loads((root/'data/structure_probe_balm_20261109/mappings'/rec['mapping_file']).read_text())
        arrays[sh]=(aa,pl,mapping);sources[sh]=c['pdb_sha256']
    version=subprocess.check_output(['wsl','-d','Ubuntu','-e',a.foldseek,'version'],text=True).strip()
    # Directory conversion avoids hundreds of WSL startup calls.
    tsv=out/'foldseek.tsv'
    if not tsv.exists():
        subprocess.run(['wsl','-d','Ubuntu','-e',a.foldseek,'structureto3didescriptor',linux(pdbdir),linux(tsv),
                        '--threads','2','--chain-name-mode','1','-v','1'],check=True)
    converted={}
    for line in tsv.read_text().splitlines():
        name,aa,ss=line.split('\t')[:3];sh=name.split('.')[0]
        if sh not in arrays:raise ValueError('Unrecognized Foldseek identifier '+name)
        if sh in converted:raise ValueError('Multiple chains not supported')
        assert aa==arrays[sh][0],('Foldseek residue mismatch',sh)
        assert len(ss)==len(aa)
        converted[sh]=ss
    assert set(converted)==set(hashes)
    pairs=[];shuffle_pairs=[];rng=np.random.RandomState(5120);mask_counts=[]
    for sh,seq in zip(hashes,sequences):
        aa,pl,mp=arrays[sh];ss=converted[sh];struc=['#']*len(seq)
        for bi,ai in zip(mp['balm_idx'],mp['af_idx']):
            assert seq[bi]==aa[ai]
            if pl[ai]>=70:struc[bi]=ss[ai].lower()
        ix=[i for i,s in enumerate(struc) if s!='#'];perm=rng.permutation(ix);scrambled=struc.copy()
        for i,j in zip(ix,perm):scrambled[i]=struc[j]
        pairs.append([x+y for x,y in zip(seq,struc)])
        shuffle_pairs.append([x+y for x,y in zip(seq,scrambled)])
        mask_counts.append(len(seq)-len(ix))
    (out/'tokens_LOCAL.json').write_text(json.dumps({'protein_sha':hashes,'real':pairs,'shuffled':shuffle_pairs}))
    torch.set_num_threads(2);device=torch.device(a.device)
    if device.type=='cuda':torch.cuda.set_per_process_memory_fraction(.25)
    provenance={'status':'FROZEN_TRAIN_PROTEIN_FEATURES_NO_LABELS','foldseek_version':version,
        'foldseek_tsv_sha256':digest(tsv),'structure_manifest_sha256':digest(mf),'models':{},
        'source_pdb_hashes':sources,'protein_count':len(hashes),'mask_counts':mask_counts,
        'window_residues':510,'pooling':'residue-weighted mean of final-layer embeddings over nonoverlapping windows',
        'control':'ESM2 sequence baseline; SaProt real vs shuffled only unmasked 3Di letters; masks/AA fixed',
        'limitations':['Frozen 35M probe, not full GenSPARC or encoder fine-tuning','Reference AF structures are not verified assay constructs',
                      'Possible overlap with public foundation-model pretraining; no novelty guarantee','Long-range LM context is broken at window boundaries']}
    for kind,(repo,revision) in MODELS.items():
        folder=out/'models'/kind;folder.mkdir(parents=True,exist_ok=True)
        for filename in ('config.json','pytorch_model.bin','special_tokens_map.json','tokenizer_config.json','vocab.txt'):
            dest=folder/filename
            if not dest.exists():
                print('DOWNLOAD',kind,filename,flush=True)
                tmp=dest.with_suffix(dest.suffix+'.partial')
                urllib.request.urlretrieve('https://huggingface.co/'+repo+'/resolve/'+revision+'/'+filename,str(tmp));tmp.replace(dest)
        provenance['models'][kind]={'repo':repo,'revision':revision,'files':{p.name:digest(p) for p in folder.iterdir() if p.is_file()}}
        state=torch.load(folder/'pytorch_model.bin',map_location='cpu',weights_only=True)
        model=EsmModel.from_pretrained(str(folder),state_dict=state,add_pooling_layer=False).to(device).eval();del state
        tokenizer=EsmTokenizer.from_pretrained(str(folder))
        modes=['real','shuffled'] if kind=='saprot' else ['sequence']
        for mode in modes:
            dest=out/(kind+'_'+mode+'.npz')
            if dest.exists():
                with np.load(dest,allow_pickle=False) as cached:
                    assert cached['protein_sha'].tolist()==hashes
                    assert cached['features'].shape==(len(hashes),480) and np.isfinite(cached['features']).all()
                print('CACHED',dest.name,flush=True);continue
            vectors=[];started=time.monotonic()
            for i,(sh,seq) in enumerate(zip(hashes,sequences)):
                units=(pairs if mode=='real' else shuffle_pairs)[i] if kind=='saprot' else list(seq)
                total=None;n=0
                for j in range(0,len(units),510):
                    chunk=units[j:j+510];text=''.join(chunk)
                    encoded=tokenizer(text,return_tensors='pt')
                    assert encoded['input_ids'].shape[1]==len(chunk)+2,('Tokenization length mismatch',kind,sh)
                    assert not (encoded['input_ids']==tokenizer.unk_token_id).any(),('Unknown token',sh)
                    encoded={k:v.to(device) for k,v in encoded.items()}
                    with torch.inference_mode():
                        h=model(**encoded).last_hidden_state[0,1:-1].float().sum(0).cpu().numpy()
                    total=h if total is None else total+h;n+=len(chunk)
                vectors.append(total/n)
                if (i+1)%10==0:print(kind,mode,i+1,'/',len(hashes),'seconds',round(time.monotonic()-started,1),flush=True)
            np.savez_compressed(dest,features=np.stack(vectors),protein_sha=np.array(hashes))
        del model,tokenizer
        if device.type=='cuda':torch.cuda.empty_cache()
    provenance['feature_sha256']={p.name:digest(p) for p in out.glob('*.npz')}
    (out/'provenance.json').write_text(json.dumps(provenance,indent=2));print('COMPLETE',flush=True)

if __name__=='__main__':main()
