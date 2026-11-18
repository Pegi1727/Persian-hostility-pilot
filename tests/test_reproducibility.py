import sys
from pathlib import Path
import numpy as np
import pandas as pd
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from scripts.validate import validate, load, ROOT
from scripts.analyze import icc, exact_signed_rank, run

def test_structure_and_ranges():
    assert validate()['status']=='PASS'

def test_agreement_regression():
    d=load();y=d.pivot(index='public_item_id',columns='annotator_id',values='hostility_1to7')
    r=icc(y.values)
    assert r['ICC_2_1']==pytest.approx(0.7145049884881044)
    assert r['ICC_2_3']==pytest.approx(0.8824644549763033)

def test_principal_descriptives():
    d=load()
    assert d.hostility_1to7.mean()==pytest.approx(3.4895833333333335)
    assert (d.policy_stance_intended==d.policy_stance_perceived).sum()==92
    assert d.groupby('hostility_intended').target_group.sum().to_dict()=={'absent':8.0,'present':35.0}

def test_exact_positive_eight():
    w,p,n=exact_signed_rank([4,3,4,2,1,4,3,4])
    assert (w,p,n)==(0,0.0078125,8)

def test_exact_ties_present():
    # Six nonzero sum-differences: +3,+1,+3,-1,+3,+5.
    # Equal absolute +1/-1 differences get average rank 1.5.
    w,p,n=exact_signed_rank([3,1,0,3,-1,0,3,5])
    assert (w,p,n)==(1.5,0.09375,6)

def test_exact_sign_and_scale_invariance():
    x=np.array([3,1,0,3,-1,0,3,5])
    assert exact_signed_rank(x)==exact_signed_rank(-x)
    assert exact_signed_rank(x)==exact_signed_rank(5*x)

def test_all_zero():
    assert exact_signed_rank([0,0,0])==(0,1,0)

def test_generated_results():
    run();r=pd.read_csv(ROOT/'results/matched_tests.csv').set_index('comparison')
    assert r.loc['arousal_hostility_present','W']==1.5
    assert r.loc['arousal_hostility_present','reporting_p']==0.09375
    assert r.loc['naturalness_hostility','W']==31
    assert r.loc['naturalness_arousal','W']==29.5

def test_public_minimization():
    assert not {'timestamp_utc','notes','session_id','hostility_evidence'}.intersection(load().columns)
    assert not list((ROOT/'data').rglob('*private*'))
