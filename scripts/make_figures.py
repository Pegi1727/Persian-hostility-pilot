from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import textwrap, shutil, json
from matplotlib.ticker import MaxNLocator
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent if (HERE.parent/'data/pilot/annotations.csv').exists() else HERE.parent/'persian-hostility-pilot'
OUT = HERE/'generated'
OUT.mkdir(exist_ok=True)
NUMBERS = {1: 2, 2: 3, 3: 4, 4: 5, 5: 1}
d=pd.read_csv(ROOT/'data/pilot/annotations.csv' if (ROOT/'data/pilot/annotations.csv').exists() else HERE/'pilot_annotations_source.csv')
factors=['scenario_id','policy_stance_intended','hostility_intended','arousal_intended']
a=d.groupby(['public_item_id']+factors,as_index=False)[['hostility_1to7','arousal_1to7']].mean()
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,'axes.titlesize':12,'axes.labelsize':11,'svg.fonttype':'none','pdf.fonttype':42,'savefig.facecolor':'white'})
BLUE='#2166AC';RED='#B35806';GRAY='#929292'
captions={}

def save(fig,num,title,caption):
 num=NUMBERS[num]
 stem=f'Figure_4_{num}'
 fig.suptitle(f'Figure 4.{num}. {title}',fontsize=14,fontweight='bold',y=.97)
 fig.text(.06,.025,'\n'.join(textwrap.wrap(caption,112)),fontsize=8.4,va='bottom',ha='left',linespacing=1.45)
 fig.subplots_adjust(left=.12,right=.95,top=.85,bottom=.29)
 for ext in ['png','pdf','svg','tiff']:
  kw={'dpi':300} if ext in ['png','tiff'] else {}
  if ext=='tiff':kw['pil_kwargs']={'compression':'tiff_lzw'}
  fig.savefig(OUT/f'{stem}.{ext}',**kw)
 plt.close(fig)
 captions[stem]={'title':title,'caption':caption}

# Paired comparisons: one item-mean per factorial cell, match remaining factors.
for num,factor,score,levels,labels,title,ptext in [
 (1,'hostility_intended','hostility_1to7',['absent','present'],['Absent','Present'],'Perceived hostility by intended hostility','W = 0.00; exploratory p < .001'),
 (2,'arousal_intended','arousal_1to7',['low','high'],['Low','High'],'Perceived arousal by intended arousal','W = 0.00; exploratory p < .001')]:
 keys=[x for x in factors if x!=factor]
 p=a.pivot(index=keys,columns=factor,values=score)[levels]
 assert len(p)==16 and not p.isna().any().any()
 fig,ax=plt.subplots(figsize=(8.5,6.5))
 # Matched rows ordered deterministically; tiny fixed offsets show overlapping observations.
 offsets=np.linspace(-.065,.065,len(p))
 for j,(_,row) in enumerate(p.iterrows()):
  ax.plot(np.array([0,1])+offsets[j],row.values,color=GRAY,alpha=.47,lw=1,zorder=1)
  ax.scatter(np.array([0,1])+offsets[j],row.values,c=[BLUE,RED],s=26,zorder=2,alpha=.8)
 means=p.mean()
 ax.scatter([0,1],means,s=150,c=[BLUE,RED],marker='D',edgecolor='white',lw=1.2,zorder=4)
 for x,m in enumerate(means):ax.annotate(f'M = {m:.2f}',(x,m),xytext=(15,-4),textcoords='offset points',fontweight='bold',color=[BLUE,RED][x])
 ax.set(xticks=[0,1],xticklabels=labels,xlim=(-.3,1.4),ylim=(.8,7.35),yticks=range(1,8),xlabel='Intended '+('hostility' if num==1 else 'arousal'),ylabel='Perceived '+('hostility' if num==1 else 'arousal')+' (1–7)')
 ax.grid(axis='y',alpha=.15);ax.text(.02,.98,ptext,transform=ax.transAxes,va='top',fontsize=10)
 cap=(f'Points represent mean {"hostility" if num==1 else "arousal"} ratings across three annotators for each of 32 stimuli. Lines connect 16 pairs matched on scenario, intended policy stance, and intended {"arousal" if num==1 else "hostility"}; diamonds show condition means ({means.iloc[0]:.2f} and {means.iloc[1]:.2f}). '
 'The two-sided Wilcoxon signed-rank test used a normal approximation without continuity correction, preserving tied absolute differences. The unadjusted test is exploratory: contrasts share only four scenarios and are not established as independent. No inferential error bars are shown.')
 save(fig,num,title,cap)
 p.to_csv(OUT/f'Figure_4_{NUMBERS[num]}_source.csv')

# Descriptive four-cell profile, scenario trajectories not inferential CI.
fig,ax=plt.subplots(figsize=(8.5,6.5))
rows=[]
for h,col,marker in [('absent',BLUE,'o'),('present',RED,'s')]:
 sub=a[a.hostility_intended==h]
 for scenario,g in sub.groupby('scenario_id'):
  sm=g.groupby('arousal_intended').hostility_1to7.mean().reindex(['low','high'])
  ax.plot([0,1],sm,color=col,alpha=.24,lw=1,marker=marker,ms=4)
 m=sub.groupby('arousal_intended').hostility_1to7.mean().reindex(['low','high'])
 ax.plot([0,1],m,color=col,lw=2.8,marker=marker,ms=9,label=f'Intended hostility {h}')
 for x,v in enumerate(m):ax.annotate(f'{v:.2f}',(x,v),xytext=(10,8),textcoords='offset points',color=col,fontweight='bold')
 for ar,v in m.items():rows.append({'hostility_intended':h,'arousal_intended':ar,'mean_hostility':v,'stimuli':8,'ratings':24})
ax.set(xticks=[0,1],xticklabels=['Low','High'],xlabel='Intended arousal',ylabel='Perceived hostility (1–7)',ylim=(.8,7.2),yticks=range(1,8),xlim=(-.15,1.25))
ax.legend(loc='upper left',frameon=False);ax.grid(axis='y',alpha=.15)
save(fig,3,'Descriptive hostility profiles across arousal conditions','Thick lines show mean hostility ratings for each intended hostility × arousal cell (eight stimuli and 24 ratings per cell). Faint lines show the four scenario-level profiles, each averaged over intended policy stance and annotators. The high-minus-low arousal contrasts were 1.04 for intended-hostility-absent stimuli and 0.58 for intended-hostility-present stimuli. These are descriptive profiles, not evidence of a confirmed interaction. The corresponding unadjusted, exploratory exact signed-rank p-values were .008 and .094; differing significance levels do not establish an interaction. No confidence intervals are implied.')
pd.DataFrame(rows).to_csv(OUT/f'Figure_4_{NUMBERS[3]}_source.csv',index=False)

# Stance confusion counts, no automated model classification.
cols=['support','opposition','mixed','unclear'];rs=['support','opposition']
c=pd.crosstab(d.policy_stance_intended,d.policy_stance_perceived).reindex(index=rs,columns=cols,fill_value=0)
assert np.trace(c.iloc[:,:2].values)==92
fig,ax=plt.subplots(figsize=(8.5,6.5))
im=ax.imshow(c.values,cmap='Blues',vmin=0,vmax=48,aspect='auto')
for i in range(2):
 for j in range(4):
  n=int(c.iloc[i,j]);ax.text(j,i,f'{n}/48\n({n/48*100:.1f}%)',ha='center',va='center',fontsize=12,color='white' if n>24 else '#222222')
ax.set(xticks=range(4),xticklabels=[s.capitalize() for s in cols],yticks=range(2),yticklabels=[s.capitalize() for s in rs],xlabel='Human-perceived policy stance',ylabel='Intended policy stance')
ax.set_title('Intended–perceived correspondence: 92/96 ratings (95.8%)',fontsize=11,pad=15)
ax.spines[['left','bottom']].set_visible(False)
save(fig,4,'Human identification of intended policy stance','Cells show annotation counts and row percentages for intended versus human-perceived policy stance. Each intended-stance row contains 48 ratings (16 stimuli × three annotators). Intended and perceived stance corresponded in 92 of 96 ratings (95.8%); the remaining ratings were mixed (n = 2) or unclear (n = 2). This is human annotation correspondence, not automated-model accuracy. Ratings are nested within stimuli and annotators; the 96 records are not 96 independent participants.')
c.to_csv(OUT/f'Figure_4_{NUMBERS[4]}_source.csv')

# Pairwise heatmaps avoid overplotting and provide ordinal rating distribution.
pairs=[('ANN-01','ANN-02'),('ANN-01','ANN-03'),('ANN-02','ANN-03')]
w=d.pivot(index='public_item_id',columns='annotator_id',values='hostility_1to7')
k=pd.read_csv(ROOT/'results/pairwise_agreement.csv' if (ROOT/'results/pairwise_agreement.csv').exists() else HERE/'pairwise_agreement_source.csv')
fig,axes=plt.subplots(1,3,figsize=(10.5,6.5))
source=[]
vmax=max(pd.crosstab(w[x],w[y]).to_numpy().max() for x,y in pairs)
for ax,(x,y) in zip(axes,pairs):
 tab=pd.crosstab(w[y],w[x]).reindex(index=range(1,8),columns=range(1,8),fill_value=0)
 ax.imshow(tab.values,origin='lower',extent=(.5,7.5,.5,7.5),vmin=0,vmax=vmax,cmap='Blues')
 ax.plot([.5,7.5],[.5,7.5],ls='--',lw=.8,color='#777777')
 for yi in range(1,8):
  for xi in range(1,8):
   val=int(tab.loc[yi,xi]);source.append({'annotator_x':x,'annotator_y':y,'rating_x':xi,'rating_y':yi,'count':val})
   if val:ax.text(xi,yi,str(val),ha='center',va='center',fontsize=8,color='white' if val>vmax*.55 else '#222222')
 kval=k[(k.annotator_a==x)&(k.annotator_b==y)].quadratic_kappa.iloc[0]
 ax.set_title(f'{x} vs. {y}\nQuadratic weighted κ = {kval:.3f}',fontsize=10)
 ax.set(xticks=range(1,8),yticks=range(1,8),xlabel=x+' rating',ylabel=y+' rating')
 ax.tick_params(labelsize=8)
fig.text(.5,.255,'Hostility ratings: ICC(2,1) = .715; ICC(2,3) = .882',ha='center',fontsize=11,fontweight='bold')
save(fig,5,'Inter-annotator agreement on hostility ratings','Each panel cross-tabulates hostility ratings (1–7) from a pair of annotators for the same 32 stimuli. Cell numbers are stimulus counts; darker shading indicates more stimuli, with a common color scale across panels. The dashed diagonal denotes exact agreement. Quadratic weighted Cohen’s kappa was .709, .801, and .638 across the three pairs. Two-way random-effects absolute-agreement reliability was ICC(2,1) = .715 for a single rating and ICC(2,3) = .882 for the mean of three ratings. These coefficients describe this pilot and do not establish full construct validity.')
pd.DataFrame(source).to_csv(OUT/f'Figure_4_{NUMBERS[5]}_source.csv',index=False)
(OUT/'CAPTIONS.md').write_text('# Results figures — captions\n\n'+'\n\n'.join(f'## {key.replace("_", " ").replace("4 ", "4.")}\n**{v["title"]}.** {v["caption"]}' for key,v in sorted(captions.items()))+'\n',encoding='utf-8')
(OUT/'README.txt').write_text('Five Chapter 4 figures based only on the human pilot: 32 stimuli, three annotators, four scenarios, 96 ratings.\nPNG and TIFF: 300 dpi. PDF and SVG: vector. Every figure includes its number and caption. Full captions also supplied in CAPTIONS.md. CSVs contain the numerical plotting data. No confidence intervals, automated-model results, or candidate-set validation are implied.\nReproduce: install numpy, pandas, matplotlib, pillow; run make_figures.py with the input CSVs beside the script or from a scripts/ directory in the pilot repository.\n',encoding='utf-8')
if (ROOT/'data/pilot/annotations.csv').exists():
 shutil.copy(ROOT/'data/pilot/annotations.csv',OUT/'pilot_annotations_source.csv')
 shutil.copy(ROOT/'results/pairwise_agreement.csv',OUT/'pairwise_agreement_source.csv')
print('Created five figures in four formats, captions and plotting-data CSVs.')
