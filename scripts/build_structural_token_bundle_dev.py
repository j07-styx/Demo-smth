"""Build a TRAIN-only BALM engineering feature bundle from existing mapped AF files.

Only get_train_only materializes affinity labels. The inherited source loader
does inspect public sequence metadata to reconstruct the frozen role split.
Structure features are invariant local environments, not curated binding pockets.
"""
import argparse,gzip,hashlib,importlib.util,json
from pathlib import Path
import numpy as np
from scipy.spatial.distance import cdist
from rdkit import Chem,RDLogger
from rdkit.Chem import rdFingerprintGenerator
RDLogger.DisableLog('rdApp.*')


def module(path,name):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m


def local_geometry(ca,aa,positions):
    d=cdist(ca,ca);sep=np.abs(positions[:,None]-positions[None,:])
    eligible=(sep>=3);within=(d<20)&eligible
    radial=np.exp(-((d[:,:,None]-np.linspace(0,20,12))/(20/12))**2)
    radial=(radial*within[:,:,None]).sum(1)/np.maximum(within.sum(1,keepdims=True),1)
    contact=(d<10)&eligible
    composition=contact.astype(float)@aa/np.maximum(contact.sum(1,keepdims=True),1)
    counts=np.stack([np.log1p(contact.sum(1)),np.log1p(((d<8)&(sep>=12)).sum(1))],1)
    return np.concatenate([radial,composition,counts],1).astype('float32')


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--source-workspace',required=True);ap.add_argument('--out',required=True)
    a=ap.parse_args();root=Path(a.source_workspace);out=Path(a.out);out.mkdir(parents=True,exist_ok=False)
    public=module(root/'dynacpi/balm_public_data_dev.py','public_loader')
    sd=module(root/'dynacpi/structure_descriptors_dev.py','descriptors')
    rows=public.get_train_only()
    mf=root/'research/structure_audit_20261110/structure_manifest.json'
    manifest=json.loads(mf.read_text(encoding='utf-8'))
    bysha={hashlib.sha256(r['protein'].encode()).hexdigest():r for r in rows}
    prot={};seqs=[];geoms=[];masks=[];groups=[];hashes=[];skipped={}
    alphabet='ACDEFGHIKLMNPQRSTVWYX';L=96
    for rec in manifest['records']:
        sh=rec['sequence_sha256']
        if sh not in bysha or not rec['usable']:continue
        c=next(c for c in rec['candidates'] if c.get('pdb_file') and
               (c.get('entryId')==rec['chosen_entry'] if rec.get('chosen_entry') else c['accession']==rec['chosen_accession']))
        raw=(root/c['pdb_file']).read_bytes();assert hashlib.sha256(raw).hexdigest()==c['pdb_sha256']
        if raw[:2]==bytes([31,139]):raw=gzip.decompress(raw)
        aa,ca,cb,pl=sd.parse_pdb(raw.decode('utf-8'))
        mapping=json.loads((root/'data/structure_probe_balm_20261109/mappings'/rec['mapping_file']).read_text())
        bi=np.array(mapping['balm_idx']);ai=np.array(mapping['af_idx']);sequence=bysha[sh]['protein']
        assert all(sequence[b]==aa[i] for b,i in zip(bi,ai))
        keep=pl[ai]>=70;bi=bi[keep];ai=ai[keep]
        if len(ai)<30:skipped[sh]='insufficient_confident_residues';continue
        onehot=np.eye(21,dtype='float32')[[alphabet.index(aa[i]) if aa[i] in alphabet else 20 for i in ai]]
        geometry=local_geometry(ca[ai],onehot,bi)
        # Sequence/confidence control has the same selected residues and confidence.
        sf=np.concatenate([onehot,pl[ai,None]/100,bi[:,None]/len(sequence)],1).astype('float32')
        take=np.linspace(0,len(ai)-1,min(L,len(ai)),dtype=int)
        sp=np.zeros((L,sf.shape[1]),dtype='float32');gp=np.zeros((L,geometry.shape[1]),dtype='float32');mask=np.zeros(L,dtype=bool)
        sp[:len(take)]=sf[take];gp[:len(take)]=geometry[take];mask[:len(take)]=True
        prot[sh]=len(seqs);seqs.append(sp);geoms.append(gp);masks.append(mask);groups.append(bysha[sh]['group']);hashes.append(sh)
    rows=[r for r in rows if hashlib.sha256(r['protein'].encode()).hexdigest() in prot]
    molecules=sorted({r['smiles'] for r in rows});mi={s:i for i,s in enumerate(molecules)}
    gen=rdFingerprintGenerator.GetMorganGenerator(radius=2,fpSize=2048,includeChirality=True)
    fps=[];atoms=[];atom_masks=[];truncated=0
    for smi in molecules:
        mol=Chem.MolFromSmiles(smi);assert mol is not None
        fps.append(gen.GetFingerprintAsNumPy(mol).astype('float32'))
        vals=[]
        for atom in mol.GetAtoms():
            z=atom.GetAtomicNum();element=[float(z==x) for x in (6,7,8,9,15,16,17,35,53)]
            vals.append(element+[z/100,atom.GetDegree()/6,atom.GetFormalCharge()/3,
                atom.GetTotalNumHs()/4,float(atom.GetIsAromatic()),float(atom.IsInRing()),int(atom.GetChiralTag())/3])
        truncated+=len(vals)>96
        arr=np.zeros((96,16),dtype='float32');mask=np.zeros(96,dtype=bool);n=min(96,len(vals))
        arr[:n]=vals[:n];mask[:n]=True;atoms.append(arr);atom_masks.append(mask)
    pp=np.array([prot[hashlib.sha256(r['protein'].encode()).hexdigest()] for r in rows])
    np.savez_compressed(out/'features.npz',fp=np.stack(fps),atoms=np.stack(atoms),atom_valid=np.stack(atom_masks),
        sequence=np.stack(seqs),geometry=np.stack(geoms),residue_valid=np.stack(masks),protein_index=pp,
        compound_index=np.array([mi[r['smiles']] for r in rows]),label=np.array([r['label'] for r in rows],dtype='float32'),
        groups=np.array(groups),protein_sha=np.array(hashes),protein_sequence=np.array([bysha[h]['protein'] for h in hashes]),source_row=np.array([r['source_row_index'] for r in rows]))
    meta={'evidence':'ENGINEERING_ONLY_BALM_FROZEN_TRAIN','rows':len(rows),'proteins':len(prot),'groups':len(set(groups)),
          'compounds':len(molecules),'atom_truncated_molecules':truncated,'max_atoms':96,'max_residues':L,
          'structure_manifest_sha256':hashlib.sha256(mf.read_bytes()).hexdigest(),
          'bundle_sha256':hashlib.sha256((out/'features.npz').read_bytes()).hexdigest(),
          'source_loader_sha256':hashlib.sha256((root/'dynacpi/balm_public_data_dev.py').read_bytes()).hexdigest(),
          'notes':['No inner-dev/reserved affinity labels materialized','No binding pockets or poses inferred',
                   'AF mappings are reference alignments, not independently approved assay constructs',
                   'No pretrained SaProt or SPMM; lightweight token-fusion ablation'], 'skipped':skipped}
    (out/'manifest.json').write_text(json.dumps(meta,indent=2));print(json.dumps(meta),flush=True)


if __name__=='__main__':main()
