from pathlib import Path
import json
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RATINGS = ['hostility_1to7', 'arousal_1to7', 'naturalness_1to7', 'hostility_confidence_1to7']
FACTORS = ['scenario_id', 'policy_stance_intended', 'hostility_intended', 'arousal_intended']

def load():
    return pd.read_csv(ROOT / 'data/pilot/annotations.csv')

def validate():
    d = load()
    s = pd.read_csv(ROOT / 'data/pilot/stimuli.csv')
    assert len(d) == 96 and d.public_item_id.nunique() == 32
    assert len(s) == 32 and s.public_item_id.is_unique
    assert not d.duplicated(['public_item_id', 'annotator_id']).any()
    assert set(d.annotator_id) == {'ANN-01','ANN-02','ANN-03'}
    assert (d.groupby('public_item_id').size() == 3).all()
    assert (d.groupby('annotator_id').size() == 32).all()
    for c in RATINGS:
        assert d[c].notna().all() and d[c].between(1,7).all()
        assert (d[c] % 1 == 0).all()
    assert set(d.guideline_version) == {'pilot-0.3'}
    assert set(d.stimulus_version) == {'pilot-0.3'}
    expected = {'policy_stance_intended': {'support','opposition'}, 'hostility_intended': {'absent','present'}, 'arousal_intended': {'low','high'}, 'policy_stance_perceived': {'support','opposition','mixed','unclear'}, 'hostility_expression': {'explicit','implicit','not_applicable','unclear'}, 'target_status': {'identified','no_evaluation','unclear'}}
    for c, vals in expected.items():
        assert d[c].notna().all() and set(d[c]).issubset(vals)
    for c in ['target_policy','target_group','target_individual','target_other']:
        assert set(d[c].dropna()).issubset({0,1})
    assert d.target_group.notna().sum() == 94
    assert d.scenario_id.nunique() == 4
    for c in FACTORS:
        assert (d.groupby('public_item_id')[c].nunique() == 1).all()
    items = d.drop_duplicates('public_item_id')
    assert len(items.groupby(FACTORS)) == 32
    assert (items.groupby('scenario_id').size() == 8).all()
    assert (items.groupby(FACTORS[1:]).size() == 4).all()
    merged = d.merge(s, on='public_item_id', suffixes=('_a','_s'), validate='many_to_one')
    assert len(merged) == 96
    for c in FACTORS:
        assert (merged[c+'_a'] == merged[c+'_s']).all()
    assert s[['context','text']].notna().all().all()
    return {'status':'PASS','records':len(d),'items':32,'scenarios':4,'annotators':3,'principal_missing':0,'duplicate_pairs':0,'available_group_targets':94}

if __name__ == '__main__':
    result = validate()
    out = ROOT/'results'; out.mkdir(exist_ok=True)
    (out/'validation.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
