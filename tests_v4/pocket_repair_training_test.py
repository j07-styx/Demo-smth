"""Check loader isolation and execute all four training arms on synthetic data."""
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
import numpy as np
import torch
from dynacpi.pocket_interaction_dev import PocketInteractionRepair, shuffled_coordinates
from scripts.train_pocket_repair_dev import load_bundle


class TrainingTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)
        self.bundle=self.root/'features.npz';self.manifest=self.root/'manifest.json'
        rng=np.random.RandomState(92)
        self.data=dict(compound=rng.normal(size=(12,8)).astype('float32'),
            residues=rng.normal(size=(4,6,12)).astype('float32'),valid=np.ones((4,6),dtype=bool),
            coords=rng.normal(size=(4,6,3)).astype('float32')*4,pocket=np.ones((4,6),dtype=bool),
            protein_index=np.repeat(np.arange(4),3),label=rng.normal(size=12).astype('float32'),
            role=np.array(['train']*9+['dev']*3),group=np.array(['a','b','c','d']))
        self.save()

    def tearDown(self): self.tmp.cleanup()

    def save(self):
        np.savez_compressed(self.bundle,**self.data)
        self.manifest.write_text(json.dumps(dict(evidence_status='ENGINEERING_ONLY',
            pocket_source='synthetic fixture, NOT biological pockets',pocket_selection_uses_labels=False,
            npz_sha256=hashlib.sha256(self.bundle.read_bytes()).hexdigest())))

    def test_group_overlap_rejected(self):
        self.data['group'][3]='a';self.save()
        with self.assertRaisesRegex(ValueError,'leakage'):load_bundle(self.bundle,self.manifest)

    def test_reserved_role_rejected(self):
        self.data['role']=np.array(['train']*9+['reserved_test']*3);self.save()
        with self.assertRaisesRegex(ValueError,'train/dev'):load_bundle(self.bundle,self.manifest)

    def test_changed_file_rejected(self):
        self.bundle.write_bytes(self.bundle.read_bytes()+b'changed')
        with self.assertRaisesRegex(ValueError,'checksum'):load_bundle(self.bundle,self.manifest)

    def test_all_arms_checkpoint_and_prediction_roundtrip(self):
        out=self.root/'output'
        p=subprocess.run([sys.executable,str(ROOT/'scripts/train_pocket_repair_dev.py'),
            '--bundle',str(self.bundle),'--manifest',str(self.manifest),'--out',str(out),
            '--epochs','2','--seeds','91','--width','16'],cwd=ROOT,capture_output=True,text=True)
        self.assertEqual(p.returncode,0,p.stderr)
        report=json.loads((out/'results.json').read_text())
        self.assertEqual(len(report['runs']),4)
        self.assertEqual(len({r['parameters'] for r in report['runs']}),1)
        for run in report['runs']:
            self.assertTrue(np.isfinite(run['rmse']))
            with np.load(out/(run['arm']+'_91_dev.npz')) as z:
                np.testing.assert_array_equal(z['row_index'],[9,10,11])
                self.assertEqual(z['prediction'].shape,(3,))
            ck=torch.load(out/(run['arm']+'_91.pt'),weights_only=True)
            model=PocketInteractionRepair(8,12,16).eval();model.load_state_dict(ck['state_dict'])
            xyz=torch.tensor(self.data['coords'])
            pocket=torch.tensor(self.data['pocket'])
            if run['arm']=='shuffled_geometry':xyz=shuffled_coordinates(xyz,pocket)
            mode={'base':'base','pocket_sequence':'sequence'}.get(run['arm'],'geometry')
            pi=self.data['protein_index'][9:]
            with torch.no_grad():
                pred=model(torch.tensor(self.data['compound'][9:]),torch.tensor(self.data['residues'][pi]),
                    torch.tensor(self.data['valid'][pi]),xyz[pi],pocket[pi],mode)['prediction'].numpy()
            pred=pred*ck['label_std']+ck['label_mean']
            with np.load(out/(run['arm']+'_91_dev.npz')) as z:
                np.testing.assert_allclose(pred,z['prediction'],atol=1e-6)


if __name__=='__main__':unittest.main()
