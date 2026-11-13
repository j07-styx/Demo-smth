"""Descriptive decomposition of existing TRAIN-CV predictions; no model selection."""
import argparse,json
from pathlib import Path
import numpy as np

def decompose(x,ids):
    counts=np.bincount(ids)
    means=np.bincount(ids,weights=x)/np.maximum(counts,1)
    between=means[ids]
    within=x-between
    assert np.allclose(x,between+within)
    assert abs(float(np.dot(between,within)))<1e-7*max(1,float(np.dot(x,x)))
    total=float(np.mean(x*x))
    return {'total_mse':total,'protein_mean_mse':float(np.mean(between**2)),
            'within_protein_mse':float(np.mean(within**2)),
            'protein_mean_energy_fraction':float(np.mean(between**2)/max(total,1e-20))}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--bundle',required=True);ap.add_argument('--runs',required=True);ap.add_argument('--out',required=True);a=ap.parse_args()
    # Positive and negative examples distinguish offsets from interactions.
    ids=np.array([0,0,1,1])
    assert decompose(np.array([2.,2.,-3.,-3.]),ids)['within_protein_mse']==0
    assert decompose(np.array([2.,-2.,3.,-3.]),ids)['protein_mean_mse']==0
    with np.load(a.bundle) as z:y=z['label'];pi=z['protein_index'];rows=z['source_row']
    with np.load(Path(a.runs)/'predictions_LOCAL.npz') as z:
        assert np.array_equal(rows,z['source_row'])
        base=z['baseline'];baseline=decompose(y-base,pi);arms={}
        for arm in ['sequence_attention','spatial_attention','shuffled_attention']:
            pred=z[arm];delta=pred-base[None,:]
            err=decompose(y-pred.mean(0),pi)
            arms[arm]={'error':err,'correction':decompose(delta.mean(0),pi),
                'fraction_individual_corrections_above_95pct_cap':float(np.mean(np.abs(delta)>.2375)),
                'mean_tanh_derivative_factor':float(np.mean(1-(delta/.25)**2)),
                'total_mse_reduction':baseline['total_mse']-err['total_mse'],
                'protein_mean_mse_reduction':baseline['protein_mean_mse']-err['protein_mean_mse'],
                'within_protein_mse_reduction':baseline['within_protein_mse']-err['within_protein_mse']}
    counts=np.bincount(pi)
    report={'evidence':'EXPLORATORY_REUSED_TRAIN_CV_DIAGNOSTIC',
        'interpretation':'Post-hoc error decomposition, not deployable protein-label calibration; protein means use evaluation labels only for scoring. Does not separate compound main effects from true interactions.',
        'rows':len(y),'proteins':int(np.sum(counts>0)),
        'singleton_proteins':int(np.sum(counts==1)),
        'validation':{'offset_and_within_positive_controls':True,'exact_source_row_alignment':True,'orthogonal_decomposition':True},
        'baseline_error':baseline,'arms':arms}
    Path(a.out).write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
if __name__=='__main__':main()
