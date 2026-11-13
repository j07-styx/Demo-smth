"""Complete, variable-size RDKit graphs for the opt-in interaction prototype."""
import numpy as np
from rdkit import Chem
from rdkit.Chem import rdFingerprintGenerator

def molecular_graph(smiles):
    mol=Chem.MolFromSmiles(smiles)
    if mol is None or mol.GetNumAtoms()==0:
        raise ValueError('Expected a valid nonempty molecule')
    atoms=[]
    for a in mol.GetAtoms():
        z=a.GetAtomicNum()
        atoms.append([float(z==v) for v in (6,7,8,9,15,16,17,35,53)]+
                     [z/100,a.GetDegree()/6,a.GetFormalCharge()/3,
                      a.GetTotalNumHs()/4,float(a.GetIsAromatic()),
                      float(a.IsInRing()),int(a.GetChiralTag())/3])
    bonds=np.zeros((len(atoms),len(atoms),6),dtype=np.float32)
    for b in mol.GetBonds():
        i,j=b.GetBeginAtomIdx(),b.GetEndAtomIdx()
        bonds[i,j]=bonds[j,i]=[b.GetBondTypeAsDouble()/3,float(b.GetIsAromatic()),
                             float(b.GetIsConjugated()),float(b.IsInRing()),
                             int(b.GetStereo())/6,1.]
    fp=rdFingerprintGenerator.GetMorganGenerator(radius=2,fpSize=2048,includeChirality=True).GetFingerprintAsNumPy(mol).astype(np.float32)
    fp/=max(float(np.linalg.norm(fp)),1.)
    return np.asarray(atoms,dtype=np.float32),bonds,fp

def collate_graphs(graphs):
    if not graphs:raise ValueError('Empty batch')
    n=max(len(g[0]) for g in graphs)
    atoms=np.zeros((len(graphs),n,16),np.float32)
    bonds=np.zeros((len(graphs),n,n,6),np.float32)
    mask=np.zeros((len(graphs),n),bool)
    for i,(a,b,_) in enumerate(graphs):
        count=len(a);atoms[i,:count]=a;bonds[i,:count,:count]=b;mask[i,:count]=True
    return atoms,bonds,mask,np.stack([g[2] for g in graphs])
