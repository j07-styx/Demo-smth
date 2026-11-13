"""Label-free same-checkpoint edge interventions, not a performance comparison."""
import argparse,json
from pathlib import Path
import numpy as np
import torch
from sklearn.preprocessing import normalize
from train_contact_graph_dev import ResidueHead

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--bundle-dir',required=True);ap.add_argument('--features',required=True);ap.add_argument('--runs',required=True);a=ap.parse_args();torch.set_num_threads(2);device='cuda' if torch.cuda.is_available() else 'cpu'
    if device=='cuda':torch.cuda.set_per_process_memory_fraction(.25)
    with np.load(Path(a.bundle_dir)/'features.npz') as z:fp=z['fp'];pi=z['protein_index'];ci=z['compound_index'];pg=z['groups']
    gs=np.array(sorted(set(pg)));np.random.RandomState(4110).shuffle(gs);g=pg[pi];t={}
    for name in ['spatial_neighborhood','sequence_neighborhood','shuffled_coordinates']:
        with np.load(Path(a.features)/(name+'.npz')) as z:
            t[name]=(torch.tensor(z['edges'],device=device),torch.tensor(z['neighbors'].astype('int64'),device=device));raw=z['features'];mask=z['valid']
    tfp=torch.tensor(normalize(fp),device=device);tm=torch.tensor(mask,device=device);records=[]
    for fold in range(5):
        held=set(gs[fold::5]);tr=np.flatnonzero([x not in held for x in g]);va=np.flatnonzero([x in held for x in g]);ptr=np.unique(pi[tr]);vals=raw[ptr][mask[ptr]];r=torch.tensor((raw-vals.mean(0))/np.maximum(vals.std(0),1e-4),device=device)
        for seed in [6111,6112]:
            model=ResidueHead().to(device);model.load_state_dict(torch.load(Path(a.runs)/(str(fold)+'_spatial_attention_'+str(seed)+'_LOCAL.pt'),map_location=device,weights_only=True));model.eval();outputs={n:[] for n in ['real','zero_edges','sequence_edges','shuffled_edges']}
            with torch.no_grad():
                for start in range(0,len(va),32):
                    ix=va[start:start+32];p=pi[ix]
                    for mode,key in [('real','spatial_neighborhood'),('zero_edges','spatial_neighborhood'),('sequence_edges','sequence_neighborhood'),('shuffled_edges','shuffled_coordinates')]:
                        e,ne=t[key];edge=e[p] if mode!='zero_edges' else torch.zeros_like(e[p]);d,_=model(tfp[ci[ix]],(r[p],edge,ne[p]),tm[p]);outputs[mode].extend(d.cpu().numpy())
            outputs={k:np.array(v) for k,v in outputs.items()};real=outputs['real'];record={'fold':fold,'seed':seed,'correction_rms':float(np.sqrt(np.mean(real**2))),'interventions':{}}
            for mode in ['zero_edges','sequence_edges','shuffled_edges']:
                delta=real-outputs[mode];record['interventions'][mode]={'prediction_difference_rms':float(np.sqrt(np.mean(delta**2))),'max_abs_difference':float(np.max(np.abs(delta)))}
            records.append(record)
    report={'label_values_loaded':False,'meaning':'same trained real-geometry model, change only edge inputs; interventions may be out of distribution','records':records,'mean_correction_rms':float(np.mean([r['correction_rms'] for r in records])),'mean_intervention_rms':{m:float(np.mean([r['interventions'][m]['prediction_difference_rms'] for r in records])) for m in records[0]['interventions']}}
    (Path(a.runs)/'mechanism.json').write_text(json.dumps(report,indent=2));print(json.dumps({k:v for k,v in report.items() if k!='records'},indent=2))
if __name__=='__main__':main()
