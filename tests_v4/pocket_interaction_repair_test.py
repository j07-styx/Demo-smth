"""Engineering checks; synthetic tensors do not establish affinity accuracy."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import unittest
import torch
from dynacpi.pocket_interaction_dev import PocketInteractionRepair, shuffled_coordinates


class PocketRepairTests(unittest.TestCase):
    def setUp(self):
        torch.manual_seed(31)
        self.model = PocketInteractionRepair(8, 12, 16).eval()
        self.c = torch.randn(4, 8)
        self.h = torch.randn(4, 7, 12)
        self.v = torch.ones(4, 7, dtype=torch.bool)
        self.p = self.v.clone(); self.p[:, -2:] = False
        self.x = torch.randn(4, 7, 3) * 5

    def run_model(self, **kw):
        args = dict(compounds=self.c, residues=self.h, valid=self.v, coords=self.x, pocket=self.p)
        args.update(kw)
        return self.model(**args)

    def test_rigid_transform_and_node_relabeling(self):
        a = self.run_model()['prediction']
        q, _ = torch.linalg.qr(torch.randn(3, 3))
        b = self.run_model(coords=self.x @ q + 30)['prediction']
        torch.testing.assert_close(a, b, atol=2e-6, rtol=2e-6)
        perm = torch.randperm(7)
        b = self.run_model(residues=self.h[:, perm], valid=self.v[:, perm],
                           coords=self.x[:, perm], pocket=self.p[:, perm])['prediction']
        torch.testing.assert_close(a, b, atol=2e-6, rtol=2e-6)

    def test_missing_empty_and_nonfinite_geometry_fallback(self):
        for kw in [dict(coords=None), dict(pocket=torch.zeros_like(self.p)),
                   dict(coords=torch.full_like(self.x, float('nan')))]:
            r = self.run_model(**kw)
            self.assertTrue(torch.equal(r['prediction'], r['sequence']))
            self.assertFalse(r['available'].any())

    def test_corruption_changes_geometry_not_sequence_control(self):
        corrupted = shuffled_coordinates(self.x, self.p)
        a = self.run_model()['prediction']; b = self.run_model(coords=corrupted)['prediction']
        self.assertGreater(float((a-b).abs().max()), 1e-7)
        a = self.run_model(mode='sequence')['prediction']
        b = self.run_model(mode='sequence', coords=corrupted)['prediction']
        self.assertTrue(torch.equal(a, b))

    def test_compound_specific_correction_and_gradients(self):
        r = self.run_model(residues=self.h[:1].expand(4,-1,-1), coords=self.x[:1].expand(4,-1,-1),
                           pocket=self.p[:1].expand(4,-1))
        self.assertGreater(float(r['correction'].std()), 1e-5)
        r['prediction'].square().sum().backward()
        for layer in (self.model.compound[0], self.model.edge[0], self.model.pocket_head[-1]):
            self.assertGreater(float(layer.weight.grad.norm()), 0)

    def test_padding_and_batch_invariance(self):
        a = self.run_model()['prediction']
        h = torch.cat((self.h, torch.full((4,3,12), float('nan'))),1)
        v = torch.cat((self.v, torch.zeros(4,3,dtype=torch.bool)),1)
        p = torch.cat((self.p, torch.zeros(4,3,dtype=torch.bool)),1)
        x = torch.cat((self.x, torch.full((4,3,3), float('nan'))),1)
        torch.testing.assert_close(a, self.run_model(residues=h, valid=v, pocket=p, coords=x)['prediction'])
        b = torch.cat([self.model(self.c[i:i+1],self.h[i:i+1],self.v[i:i+1],self.x[i:i+1],self.p[i:i+1])['prediction'] for i in range(4)])
        torch.testing.assert_close(a,b)

    def test_invalid_mapping_rejected(self):
        with self.assertRaises(ValueError): self.run_model(coords=self.x[:,:-1])
        v = self.v.clone(); v[:,0] = False
        with self.assertRaises(ValueError): self.run_model(valid=v)

    def test_joint_readout_can_fit_synthetic_interactions(self):
        # Fixed protein, different compounds: checks chemistry is not discarded.
        torch.manual_seed(7)
        opt = torch.optim.Adam(self.model.parameters(),lr=.015)
        y = torch.tensor([-1.,.2,.7,1.4])
        before = float(((self.run_model()['prediction']-y)**2).mean())
        for _ in range(100):
            opt.zero_grad(); loss = ((self.run_model()['prediction']-y)**2).mean()
            loss.backward(); opt.step()
        after = float(((self.run_model()['prediction']-y)**2).mean())
        self.assertLess(after,before*.02)


if __name__ == '__main__':
    torch.set_num_threads(1)
    unittest.main()
