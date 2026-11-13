"""Exploratory 2x2 readout/scale-limit ablation; reuses verified original cell."""
import argparse,json,subprocess,sys
from pathlib import Path
import numpy as np
from evaluate_pretrained_structure_dev import sha

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--bundle-dir',required=True);ap.add_argument('--features',required=True);ap.add_argument('--previous-cv',required=True);ap.add_argument('--out',required=True);a=ap.parse_args();out=Path(a.out);out.mkdir(parents=True,exist_ok=False)
    previous=Path(a.previous_cv);old=json.loads((previous/'results.json').read_text());assert old['rows']==5808 and old['groups']==253
    protocol={'evidence':'EXPLORATORY_TRAIN_ONLY_FACTORIAL','cells':[['interaction',1.],['interaction',.3],['protein',1.],['protein',.3]],'reused_cell':'interaction_1.0','previous_results_sha256':sha(previous/'results.json'),'selection':'unchanged three-fold inner group-macro selection within each cell; same five outer folds','purpose':'isolate explicit compound products from protein main effects, and excluding scale 1 from retaining it','limitations':['Designed after examining previous CV: no confirmatory inference','Protein-only refers to added pretrained block; shared baseline still includes chemistry','No held-out test access or demo replacement'],'evaluator_sha256':sha(Path(__file__).with_name('evaluate_pretrained_structure_dev.py'))}
    (out/'protocol.json').write_text(json.dumps(protocol,indent=2));cells={'interaction_1.0':previous}
    for readout,cap in protocol['cells'][1:]:
        name=readout+'_'+str(cap);dest=out/name
        cmd=[sys.executable,'-u',str(Path(__file__).with_name('crossvalidate_pretrained_structure_dev.py')),'--bundle-dir',a.bundle_dir,'--features',a.features,'--out',str(dest),'--readout',readout,'--max-scale',str(cap)]
        subprocess.run(cmd,check=True)
        subprocess.run([sys.executable,str(Path(__file__).with_name('validate_pretrained_cv_dev.py')),'--bundle-dir',a.bundle_dir,'--results',str(dest)],check=True);cells[name]=dest
    summary={'protocol':protocol,'cells':{}}
    with np.load(previous/'oof_predictions_LOCAL.npz') as z:rows=z['source_row'];baseline=z['baseline']
    for name,path in cells.items():
        result=json.loads((path/'results.json').read_text())
        with np.load(path/'oof_predictions_LOCAL.npz') as z:
            assert np.array_equal(rows,z['source_row']);assert np.allclose(baseline,z['baseline'],atol=1e-7,rtol=0)
        summary['cells'][name]={'metrics':result['metrics'],'contrasts':result['contrasts'],'selected_scales':result['selected_scales']}
    (out/'results.json').write_text(json.dumps(summary,indent=2));print('FACTORIAL COMPLETE',json.dumps({n:r['metrics'] for n,r in summary['cells'].items()}),flush=True)
if __name__=='__main__':main()
