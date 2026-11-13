"""Audit existing completed external comparisons; never parse raw test values."""
import argparse,hashlib,json,math
from pathlib import Path

def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def sha(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--backend',required=True);ap.add_argument('--out',required=True);a=ap.parse_args();root=Path(a.backend)/'external_benchmarks_20261110/locked_external_protocol_v1';complete=root/'ALL_SIX_EXTERNAL_SAME_SPLIT_TESTS_ONCE';summary=read(complete/'COMPLETE_SIX_RESULTS.json');assert summary['status']=='ALL_SIX_EXTERNAL_MATCHED_TWO_SEED_TESTS_COMPLETE'
    assert len(summary['scenarios'])==6;assert len({(s['dataset'],s['scenario']) for s in summary['scenarios']})==6
    sources={ds:sha(root/ds/'source_features.npz') for ds in ['kiba','metz']};results=[]
    for s in summary['scenarios']:
        ds,scenario=s['dataset'],s['scenario'];folder=root/ds/scenario;scored=complete/(ds+'_'+scenario);r=read(scored/'TEST_RESULTS.json');boot=read(scored/'PAIRED_CLUSTER_BOOTSTRAP.json');split=read(folder/'SPLIT_LOCKED.json');frozen=read(folder/'dynacpi_fixed_sparse_train/VALIDATION_FROZEN.json')
        assert r['source_features_sha256']==sources[ds]==frozen['source_features_sha256'];assert r['frozen_split_sha256']==sha(folder/'SPLIT_LOCKED.json')==frozen['frozen_split_sha256']
        partitions=[set(split['pair_'+part+'_row_indices']) for part in ['train','val','test']];assert all(not partitions[i]&partitions[j] for i in range(3) for j in range(i));assert len(partitions[2])==r['n_test_pairs']
        assert sha(scored/'paired_raw_predictions_private.npz')==r['paired_raw_pred_sha256']==boot['original_raw_predictions_sha256'];assert sha(scored/'TEST_RESULTS.json')==boot['original_test_result_sha256'];assert sha(scored/'sealed_test_exact_once.csv')==r['heldout_csv_sha256']
        expected=set(r['dynacpi_checkpoint_shas'].values())|set(r['perceiver_checkpoint_shas'].values());actual={sha(p) for p in folder.rglob('*.pt')};assert expected<=actual,('Checkpoint mismatch',ds,scenario)
        for key in ['dynacpi_2seed','official_perceiver_2seed','delta_macro_dyna_minus_perceiver','delta_pooled_dyna_minus_perceiver']:assert s[key]==r[key]
        for metric in ['macro','pooled']:
            assert s[metric+'_95pct_difference_interval']==boot['bootstrap'][metric+'_delta_95pct_interval'];assert math.isclose(r['delta_'+metric+'_dyna_minus_perceiver'],r['dynacpi_2seed'][metric+'_rmse']-r['official_perceiver_2seed'][metric+'_rmse'],abs_tol=1e-12)
        for key in ['dynacpi_2seed','official_perceiver_2seed']:assert math.isclose(r[key]['pooled_mse'],r[key]['pooled_rmse']**2,rel_tol=1e-6)
        results.append({'dataset':ds,'split':scenario,'test_pairs':r['n_test_pairs'],'dyna':r['dynacpi_2seed'],'perceiver':r['official_perceiver_2seed'],'macro_ci':s['macro_95pct_difference_interval'],'pooled_ci':s['pooled_95pct_difference_interval'],'both_point_estimates_better':r['delta_macro_dyna_minus_perceiver']<0 and r['delta_pooled_dyna_minus_perceiver']<0,'both_intervals_below_zero':max(s['macro_95pct_difference_interval'])<0 and max(s['pooled_95pct_difference_interval'])<0,'checkpoint_hashes_verified':len(expected),'split_sha256':r['frozen_split_sha256']})
        print('VERIFIED',ds,scenario,flush=True)
    report={'status':'EXISTING_COMPLETED_RESULTS_INTEGRITY_PASS','aggregate_sha256':sha(complete/'COMPLETE_SIX_RESULTS.json'),'source_commit_recorded':summary['original_perceiver_source_commit'],'raw_test_values_parsed':False,'new_test_scoring':False,'model_training':False,'comparisons':results,'wins_both':sum(r['both_point_estimates_better'] for r in results),'both_intervals_favor_dyna':sum(r['both_intervals_below_zero'] for r in results),'limits':['Different published-paper dataset variants/splits and training budget','Different protein pretraining budgets; not architecture-only attribution','Two seeds, one partition per scenario; descriptive unadjusted intervals','These completed external tests belong to backend v5, not the BALM structure probe reserved test','No 3D encoder or expert routing in the winning model']}
    out=Path(a.out);out.mkdir(parents=True,exist_ok=False);(out/'results.json').write_text(json.dumps(report,indent=2));print('COMPLETE',report['wins_both'],report['both_intervals_favor_dyna'],flush=True)
if __name__=='__main__':main()
