"""Synthetic engineering checks for token fusion and invariant feature extraction."""
import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import numpy as np
import torch
from dynacpi.structural_token_fusion_dev import StructuralTokenFusion
from scripts.build_structural_token_bundle_dev import local_geometry


class TokenTests(unittest.TestCase):
    def setUp(self):
        torch.manual_seed(41)
        self.m=StructuralTokenFusion(23,35,16).eval()
        self.fp=torch.rand(3,2048);self.at=torch.randn(3,7,16);self.av=torch.ones(3,7,dtype=torch.bool)
        self.s=torch.randn(3,9,23);self.g=torch.randn(3,9,35);self.rv=torch.ones(3,9,dtype=torch.bool)
    def pred(self,mode='real',g=None):
        return self.m(self.fp,self.at,self.av,self.s,self.g if g is None else g,self.rv,mode)
    def test_sequence_control_ignores_geometry(self):
        self.assertTrue(torch.equal(self.pred('sequence'),self.pred('sequence',torch.randn_like(self.g))))
    def test_mean_control_ignores_correspondence(self):
        perm=torch.randperm(9)
        torch.testing.assert_close(self.pred('mean'),self.pred('mean',self.g[:,perm]),atol=1e-6,rtol=1e-6)
        self.assertGreater(float((self.pred()-self.pred(g=self.g[:,perm])).abs().max()),1e-7)
    def test_geometry_receives_gradient(self):
        self.pred().square().sum().backward()
        self.assertGreater(float(self.m.geometry[0].weight.grad.norm()),0)
        self.assertGreater(float(self.m.atom[0].weight.grad.norm()),0)
        self.assertGreater(float(self.m.fp[0].weight.grad.norm()),0)
    def test_consistent_relabeling(self):
        p=torch.randperm(9);a=torch.randperm(7)
        other=self.m(self.fp,self.at[:,a],self.av[:,a],self.s[:,p],self.g[:,p],self.rv[:,p])
        torch.testing.assert_close(self.pred(),other,atol=1e-6,rtol=1e-6)
    def test_rigid_feature_invariance(self):
        r=np.random.RandomState(31);x=r.normal(size=(15,3))*4;aa=np.eye(21)[r.randint(0,21,15)];pos=np.arange(15)
        q,_=np.linalg.qr(r.normal(size=(3,3)))
        np.testing.assert_allclose(local_geometry(x,aa,pos),local_geometry(x@q+42,aa,pos),atol=1e-6)
    def test_empty_mask_rejected(self):
        self.av[0]=False
        with self.assertRaises(ValueError):self.pred()


if __name__=='__main__':
    torch.set_num_threads(1);unittest.main()
