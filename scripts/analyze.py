from pathlib import Path
import sys, json, platform, itertools, warnings
import numpy as np
import pandas as pd
import scipy
from scipy import stats
import sklearn
from sklearn.metrics import cohen_kappa_score
sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate import ROOT, RATINGS, FACTORS, load, validate

def icc(y):
    y = np.asarray(y, dtype=float)
    n,k=y.shape; grand=y.mean()
    mr=k*np.sum((y.mean(axis=1)-grand)**2)/(n-1)
    mc=n*np.sum((y.mean(axis=0)-grand)**2)/(k-1)
    me=np.sum((y-y.mean(axis=1)[:,None]-y.mean(axis=0)[None,:]+grand)**2)/((n-1)*(k-1))
    return {'ICC_2_1':float((mr-me)/(mr+(k-1)*me+k*(mc-me)/n)), 'ICC_2_3':float((mr-me)/(mr+(mc-me)/n))}

def exact_signed_rank(differences):
    x=np.asarray(differences);x=x[x!=0]
    if not len(x): return 0.0, 1.0, 0
    # Rank sums multiplied by 2 are integers, including tied midranks.
    ranks2=np.rint(2*stats.rankdata(np.abs(x),method='average')).astype(int)
    observed=int(ranks2[x>0].sum()); total=int(ranks2.sum())
    distance=abs(2*observed-total)
    extreme=sum(abs(2*sum(r for r,sign in zip(ranks2, signs) if sign)-total)>=distance for signs in itertools.product([0,1],repeat=len(x)))
    return min(observed,total-observed)/2, extreme/(2**len(x)), len(x)

def run():
    validate();d=load();out=ROOT/'results';out.mkdir(exist_ok=True)
    desc=d[RATINGS].agg(['count','mean','std']).T
    desc.index.name='measure';desc.to_csv(out/'descriptives.csv')
    for f in ['hostility_intended','arousal_intended']:
        d.groupby(f)[RATINGS].agg(['count','mean','std']).to_csv(out/('descriptives_by_'+f+'.csv'))
    d.groupby(['hostility_intended','arousal_intended'])[RATINGS].agg(['count','mean','std']).to_csv(out/'factor_cells.csv')
    y=d.pivot(index='public_item_id',columns='annotator_id',values='hostility_1to7')
    reliability=icc(y.values)
    pairs=[]
    for a,b in itertools.combinations(y.columns,2):
        pairs.append({'annotator_a':a,'annotator_b':b,'n':len(y),'quadratic_kappa':cohen_kappa_score(y[a],y[b],weights='quadratic'),'mean_absolute_difference':float((y[a]-y[b]).abs().mean())})
    pd.DataFrame(pairs).to_csv(out/'pairwise_agreement.csv',index=False)
    # Integer sums provide an exact common scale for ranks and ties.
    sums=d.groupby(FACTORS)[RATINGS].sum().reset_index()
    means=d.groupby(FACTORS)[RATINGS].mean().reset_index()
    definitions=[('hostility_manipulation','hostility_intended','hostility_1to7','present','absent',None),('arousal_manipulation','arousal_intended','arousal_1to7','high','low',None),('arousal_hostility_absent','arousal_intended','hostility_1to7','high','low','absent'),('arousal_hostility_present','arousal_intended','hostility_1to7','high','low','present'),('naturalness_hostility','hostility_intended','naturalness_1to7','present','absent',None),('naturalness_arousal','arousal_intended','naturalness_1to7','high','low',None)]
    rows=[];contrasts=[]
    for name,f,v,hi,lo,subset in definitions:
        a=sums if subset is None else sums[sums.hostility_intended==subset]
        b=means if subset is None else means[means.hostility_intended==subset]
        idx=[c for c in FACTORS if c!=f]
        pa=a.pivot(index=idx,columns=f,values=v);pb=b.pivot(index=idx,columns=f,values=v)
        diff=(pa[hi]-pa[lo]).astype(int); md=diff/3
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            normal=stats.wilcoxon(diff,method='approx',correction=False,zero_method='wilcox')
            legacy=stats.wilcoxon(pb[hi]-pb[lo],method='approx',correction=False,zero_method='wilcox')
        w,p,n=exact_signed_rank(diff.values)
        use_exact=name.startswith('arousal_hostility_')
        rows.append({'comparison':name,'n_pairs':len(diff),'nonzero_pairs':n,'mean_difference':md.mean(),'sd_difference':md.std(ddof=1),'W':w,'normal_p_ties_preserved':normal.pvalue,'exact_sign_permutation_p':p,'legacy_float_normal_W':legacy.statistic,'legacy_float_normal_p':legacy.pvalue,'reporting_method':'exact_sign_permutation' if use_exact else 'normal_no_continuity_ties_preserved','reporting_p':p if use_exact else normal.pvalue})
        for key, val in diff.items():
            contrasts.append({'comparison':name,**dict(zip(idx,key if isinstance(key,tuple) else (key,))),'difference_in_rating_sums':int(val),'difference_in_item_means':val/3})
    pd.DataFrame(rows).to_csv(out/'matched_tests.csv',index=False)
    pd.DataFrame(contrasts).to_csv(out/'matched_contrasts.csv',index=False)
    stance=pd.crosstab(d.policy_stance_intended,d.policy_stance_perceived);stance.to_csv(out/'stance_confusion.csv')
    expression=pd.crosstab(d.hostility_intended,d.hostility_expression);expression.to_csv(out/'hostility_expression_counts.csv')
    targets=d.groupby('hostility_intended').target_group.agg(['count','sum']);targets['proportion']=targets['sum']/targets['count'];targets.to_csv(out/'group_target.csv')
    accuracy=float((d.policy_stance_intended==d.policy_stance_perceived).mean())
    summary={'scope':'human pilot only; not candidate-set validation or model evaluation','records':len(d),'items':32,'scenarios':4,'annotators':3,'guideline_version':'pilot-0.3','stimulus_version':'pilot-0.3','reliability':reliability,'stance_accuracy':accuracy,'software':{'python':platform.python_version(),'numpy':np.__version__,'pandas':pd.__version__,'scipy':scipy.__version__,'scikit_learn':sklearn.__version__},'statistical_caution':'Four shared scenarios; independence not established; unadjusted exploratory p-values.'}
    (out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    lines=['# Reproduced results','',f'96 annotations; 32 items; 4 scenarios; 3 annotators. Policy stance accuracy: {100*accuracy:.2f}%.', '',f"ICC(2,1) = {reliability['ICC_2_1']:.6f}; ICC(2,3) = {reliability['ICC_2_3']:.6f}.",'','## Matched comparisons (canonical ties preserved)','', '| Comparison | n | Mean difference | SD | W | Exploratory p | Method |','|---|---:|---:|---:|---:|---:|---|']
    for r in rows:lines.append(f"| {r['comparison']} | {r['n_pairs']} | {r['mean_difference']:.6f} | {r['sd_difference']:.6f} | {r['W']:.2f} | {r['reporting_p']:.9f} | {r['reporting_method']} |")
    lines+=['','These p-values do not correct for scenario dependence or multiplicity. See the reporting audit for differences from legacy floating-point calculations.']
    (out/'REPORT.md').write_text('\n'.join(lines)+'\n')
    print('\n'.join(lines))
    return summary

if __name__=='__main__': run()
