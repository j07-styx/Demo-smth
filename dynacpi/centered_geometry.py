"""Opt-in centered GVP residual: remove protein-wide structure bias before compound gating."""
import torch
from torch import nn

class CenteredGeometry(nn.Module):
    def __init__(self,geometry):
        super().__init__()
        self.geometry=geometry

    def enhance(self,tokens,graph):
        if graph is None:
            return tokens
        idx=torch.as_tensor(graph['indices'],device=tokens.device,dtype=torch.long)
        if idx.ndim!=1 or idx.numel()==0 or idx.min()<0 or idx.max()>=len(tokens) or idx.unique().numel()!=idx.numel():
            raise ValueError('Invalid structure indices')
        delta=self.geometry.enhance(tokens,graph)-tokens
        centered=delta.index_select(0,idx)-delta.index_select(0,idx).mean(dim=0,keepdim=True)
        result=tokens.clone()
        result.index_add_(0,idx,centered)
        return result
