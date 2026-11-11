"""Experimental bidirectional atom/residue fusion; not a GenSPARC reproduction.

Inputs are sequence, confidence and invariant local structure descriptors. No
pretrained SaProt weights, poses or experimental contact labels are implied.
"""
import torch
from torch import nn


class StructuralTokenFusion(nn.Module):
    def __init__(self, sequence_dim, geometry_dim, atom_dim, width=32):
        super().__init__()
        self.fp=nn.Sequential(nn.Linear(2048,width),nn.SiLU(),nn.LayerNorm(width))
        self.atom=nn.Sequential(nn.Linear(atom_dim,width),nn.LayerNorm(width))
        self.sequence=nn.Linear(sequence_dim,width)
        self.geometry=nn.Sequential(nn.Linear(geometry_dim,width),nn.SiLU(),nn.Linear(width,width))
        self.protein_norm=nn.LayerNorm(width)
        self.atom_to_residue=nn.MultiheadAttention(width,4,batch_first=True)
        self.residue_to_atom=nn.MultiheadAttention(width,4,batch_first=True)
        self.atom_norm=nn.LayerNorm(width);self.residue_norm=nn.LayerNorm(width)
        self.head=nn.Sequential(nn.Linear(width*5,width),nn.SiLU(),nn.Linear(width,1))
        nn.init.normal_(self.head[-1].weight,std=.02);nn.init.zeros_(self.head[-1].bias)

    @staticmethod
    def mean(x,mask):
        return (x*mask[...,None]).sum(1)/mask.sum(1,keepdim=True)

    def forward(self,fp,atoms,atom_valid,sequence,geometry,residue_valid,mode='real'):
        if mode not in ('sequence','real','mean'):raise ValueError('Unknown structure mode')
        if not atom_valid.any(1).all() or not residue_valid.any(1).all():raise ValueError('Empty token set')
        # Mask padded values before projections to prevent NaN propagation.
        atoms=torch.where(atom_valid[...,None],atoms,torch.zeros_like(atoms))
        sequence=torch.where(residue_valid[...,None],sequence,torch.zeros_like(sequence))
        geometry=torch.where(residue_valid[...,None],geometry,torch.zeros_like(geometry))
        if not torch.isfinite(atoms).all() or not torch.isfinite(sequence).all():raise ValueError('Nonfinite features')
        if mode!='sequence' and not torch.isfinite(geometry).all():raise ValueError('Nonfinite geometry')
        c=self.fp(fp);a=self.atom(atoms);p=self.sequence(sequence)
        if mode!='sequence':
            if mode=='mean':geometry=self.mean(geometry,residue_valid)[:,None,:].expand_as(geometry)
            p=p+self.geometry(geometry)
        p=self.protein_norm(p)
        # Simultaneous cross-updates retain each modality via residual paths.
        a2=self.atom_norm(a+self.atom_to_residue(a,p,p,key_padding_mask=~residue_valid,need_weights=False)[0])
        p2=self.residue_norm(p+self.residue_to_atom(p,a,a,key_padding_mask=~atom_valid,need_weights=False)[0])
        ac=self.mean(a2,atom_valid);pc=self.mean(p2,residue_valid)
        return self.head(torch.cat((c,ac,pc,ac*pc,(ac-pc).abs()),-1)).squeeze(-1)
