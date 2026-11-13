import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import numpy as np
from dynacpi.molecular_graph_dev import molecular_graph,collate_graphs

def main():
    chain=molecular_graph('C'*110);assert len(chain[0])==110
    assert (chain[1][...,5]>0).sum()==218
    ring=molecular_graph('c1ccccc1');assert ring[1][...,1].sum()==12
    a,b,mask,fp=collate_graphs([chain,ring])
    assert mask.sum(1).tolist()==[110,6]
    assert not b[1,6:].any() and not b[1,:,6:].any()
    assert np.allclose(b,b.transpose(0,2,1,3))
    assert np.allclose(np.linalg.norm(fp,axis=1),1)
    try:molecular_graph('');raise AssertionError('Empty accepted')
    except ValueError:pass
    print(json.dumps({'complete_110_atom_molecule':True,'bond_symmetry':True,'aromatic_bonds':True,'padding':True,'normalized_fingerprint':True,'empty_rejected':True},indent=2))
if __name__=='__main__':main()
