"""Opt-in pose-free atom/residue interaction prototype. No affinity claim."""
import torch
from torch import nn

class AtomResidueInteraction(nn.Module):
    def __init__(self, atom_dim, residue_dim, fingerprint_dim=2048, bond_dim=6, width=32):
        super().__init__()
        self.atom=nn.Linear(atom_dim,width)
        self.residue=nn.Linear(residue_dim,width)
        self.fingerprint=nn.Linear(fingerprint_dim,width)
        self.bond_message=nn.Sequential(nn.Linear(2*width+bond_dim,width),nn.GELU(),nn.Linear(width,width))
        self.atom_norm=nn.LayerNorm(width)
        self.pair_value=nn.Sequential(nn.Linear(4*width,width),nn.GELU(),nn.Linear(width,width))
        self.pair_score=nn.Linear(width,1)
        self.head=nn.Sequential(nn.Linear(4*width,width),nn.GELU(),nn.Linear(width,1))

    def forward(self, atoms, bonds, atom_mask, residues, residue_mask, fingerprint):
        if atom_mask.dtype!=torch.bool or residue_mask.dtype!=torch.bool:
            raise ValueError('Masks must be boolean')
        if not atom_mask.any(1).all() or not residue_mask.any(1).all():
            raise ValueError('Every example requires at least one real atom and residue')
        # Clear padding before projections, including padded bond features.
        am=atom_mask
        atoms=atoms.masked_fill(~am[...,None],0)
        residues=residues.masked_fill(~residue_mask[...,None],0)
        valid_bond=am[:,:,None]&am[:,None,:]
        bonds=bonds.masked_fill(~valid_bond[...,None],0)
        adjacency=(bonds.abs().sum(-1)>0)&valid_bond
        h=self.atom(atoms)
        n=h.shape[1]
        source=h[:,:,None,:].expand(-1,-1,n,-1)
        neighbor=h[:,None,:,:].expand(-1,n,-1,-1)
        message=self.bond_message(torch.cat([source,neighbor,bonds],-1))
        message=(message*adjacency[...,None]).sum(2)/adjacency.sum(2).clamp_min(1)[...,None]
        h=self.atom_norm(h+message)
        r=self.residue(residues)
        # Atom/residue features influence message VALUES as well as attention.
        aa=h[:,:,None,:].expand(-1,-1,r.shape[1],-1)
        rr=r[:,None,:,:].expand(-1,h.shape[1],-1,-1)
        pair=self.pair_value(torch.cat([aa,rr,aa*rr,(aa-rr).abs()],-1))
        mask=am[:,:,None]&residue_mask[:,None,:]
        score=self.pair_score(pair).squeeze(-1).masked_fill(~mask,-torch.inf)
        attention=score.flatten(1).softmax(1).reshape_as(score)
        interaction=(pair*attention[...,None]).sum((1,2))
        chem=(h*am[...,None]).sum(1)/am.sum(1)[:,None]
        protein=(r*residue_mask[...,None]).sum(1)/residue_mask.sum(1)[:,None]
        # Uncapped standardized output; the fit-gate is not a production residual.
        pred=self.head(torch.cat([chem,protein,interaction,self.fingerprint(fingerprint)],-1)).squeeze(-1)
        return pred,attention
