"""Opt-in pocket interaction repair. Experimental; no production checkpoint changes.

Coordinates and pocket masks must already be mapped to residue features. Pocket
selection is external and label-independent; this module does not discover poses.
Only distances enter geometry, so affinity is invariant to rigid transforms.
"""
import math
import torch
from torch import nn


class PocketInteractionRepair(nn.Module):
    def __init__(self, compound_dim=2048, residue_dim=1280, width=64, residual_scale=0.1):
        super().__init__()
        self.compound = nn.Sequential(nn.Linear(compound_dim, width), nn.SiLU(), nn.LayerNorm(width))
        self.sequence = nn.Sequential(nn.Linear(residue_dim, width), nn.LayerNorm(width))
        self.edge = nn.Sequential(nn.Linear(16, width), nn.SiLU(), nn.Linear(width, width))
        self.message = nn.Linear(width, width)
        self.node_norm = nn.LayerNorm(width)
        self.base_head = nn.Sequential(nn.Linear(width * 4, width), nn.SiLU(), nn.Linear(width, 1))
        self.pocket_head = nn.Sequential(nn.Linear(width * 4, width), nn.SiLU(), nn.Linear(width, 1))
        # Nonzero initialization permits gradient flow on the first update.
        nn.init.normal_(self.pocket_head[-1].weight, std=0.02)
        nn.init.zeros_(self.pocket_head[-1].bias)
        self.register_buffer('centers', torch.linspace(0, 20, 16))
        self.residual_scale = float(residual_scale)

    @staticmethod
    def pair(c, p):
        return torch.cat((c, p, c * p, (c - p).abs()), -1)

    def forward(self, compounds, residues, valid, coords=None, pocket=None, mode='geometry'):
        if mode not in ('base', 'sequence', 'geometry'):
            raise ValueError('mode must be base, sequence or geometry')
        if residues.ndim != 3 or valid.shape != residues.shape[:2] or valid.dtype != torch.bool:
            raise ValueError('Expected residues [B,L,D] and boolean valid [B,L]')
        if not valid.any(1).all() or not torch.isfinite(residues[valid]).all():
            raise ValueError('Empty or nonfinite residue features')
        if compounds.ndim != 2 or compounds.shape[0] != len(residues) or not torch.isfinite(compounds).all():
            raise ValueError('Invalid compound features')
        c = self.compound(compounds)
        h = self.sequence(torch.where(valid[..., None], residues, torch.zeros_like(residues)))
        mean = (h * valid[..., None]).sum(1) / valid.sum(1, keepdim=True)
        base = self.base_head(self.pair(c, mean)).squeeze(-1)
        correction = torch.zeros_like(base)
        attention = torch.zeros_like(valid, dtype=h.dtype)
        available = torch.zeros(len(h), dtype=torch.bool, device=h.device)
        if mode == 'base' or pocket is None:
            return dict(prediction=base, sequence=base, correction=correction, attention=attention, available=available)
        if pocket.shape != valid.shape or pocket.dtype != torch.bool or (pocket & ~valid).any():
            raise ValueError('Pocket mask must select existing aligned residues')
        selected = pocket & valid
        if mode == 'geometry':
            if coords is None:
                return dict(prediction=base, sequence=base, correction=correction, attention=attention, available=available)
            if coords.shape != (*valid.shape, 3):
                raise ValueError('Coordinate mapping shape mismatch')
            # Incomplete pocket geometry falls back for that protein; no silent remapping.
            finite = torch.isfinite(coords).all(-1)
            available = selected.sum(1).ge(2) & (~selected | finite).all(1)
        else:
            available = selected.sum(1).ge(2)
        # Compact pocket tensors avoid quadratic work over the full protein.
        for b in available.nonzero(as_tuple=True)[0].tolist():
            ix = selected[b].nonzero(as_tuple=True)[0]
            hp = h[b, ix]
            if mode == 'geometry':
                d = torch.cdist(coords[b, ix], coords[b, ix])
            else:
                # Same trainable modules, constant geometric input: pocket-sequence control.
                d = hp.new_zeros((len(ix), len(ix)))
            rbf = torch.exp(-((d[..., None] - self.centers) / (20 / 16)) ** 2)
            neighbours = ~torch.eye(len(ix), device=h.device, dtype=torch.bool)
            messages = self.message(hp)[None, :, :] + self.edge(rbf)
            messages = (messages * neighbours[..., None]).sum(1) / neighbours.sum(1, keepdim=True)
            hp = self.node_norm(hp + messages)
            weights = torch.softmax(hp @ c[b] / math.sqrt(hp.shape[-1]), dim=0)
            p = (weights[:, None] * hp).sum(0)
            correction[b] = self.residual_scale * self.pocket_head(self.pair(c[b], p)).squeeze(-1)
            attention[b, ix] = weights
        return dict(prediction=base + correction, sequence=base, correction=correction,
                    attention=attention, available=available)


def shuffled_coordinates(coords, pocket, seed=20261110):
    """Break residue-coordinate correspondence, retaining each pocket's point cloud.

    This is a partial geometry corruption, not a geometry-free null. Use the
    explicit sequence control too. Generate once per protein, not once per pair.
    """
    out = coords.clone()
    generator = torch.Generator(device='cpu').manual_seed(seed)
    for b in range(len(coords)):
        idx = pocket[b].nonzero(as_tuple=True)[0]
        perm = torch.randperm(len(idx), generator=generator).to(idx.device)
        out[b, idx] = coords[b, idx[perm]]
    return out
