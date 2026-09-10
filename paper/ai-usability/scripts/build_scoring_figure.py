"""Compact bilingual rubric figure; run with Matplotlib. Uses the existing scoring function for the M6 worked example."""
from pathlib import Path
import argparse
import importlib.util
from statistics import median

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--only', choices=['official', 'support', 'answers', 'confidence'])
args = parser.parse_args()
score_path = Path(__file__).resolve().parents[3] / 'score_metrics.py'
spec = importlib.util.spec_from_file_location('scoring', score_path)
scoring = importlib.util.module_from_spec(spec)
spec.loader.exec_module(scoring)
example = scoring.RAW['A']['cann']
baselines = [scoring.SOURCE_CRED[k] for k in example['sources']]
mean = sum(baselines) / len(baselines)
adjustments = [scoring.CONSIST[example['consist']],
               scoring.recency_factor(example['dates']),
               scoring.independence_factor(example['platforms'])]
median_age = median(scoring._age_months(d) for d in example['dates'] if d)
platform_count = len(set(example['platforms']))
final_score = scoring.score6_sec_cred(example)

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager, colors
import numpy as np
OUT=Path(__file__).resolve().parents[1]/'figures'
font_manager.fontManager.addfont('/System/Library/Fonts/Supplemental/Arial Unicode.ttf')
BLUE='#397ac0';M5_COLOR='#9869b9';M7_COLOR='#7e78c5';M8_COLOR='#a17cba';INDIGO='#239b8e';M6_COLOR='#6887c3';SLATE='#61788d'
ROWS=[
('M1',BLUE,['多轮仍难找到','换词定位／\n一轮排名>10','多轮命中／\n排名7–10','一轮排名2–6','一轮排名第1'],['Still not found','Refine query /\nrank >10','Multiple rounds /\nrank 7–10','First round: 2–6','First round: 1']),
('M2',BLUE,['robots限制','SPA受阻','—','服务端渲染／\n部分返回','静态正文'],['robots restriction','SPA blocked','—','SSR /\npartial return','Static body']),
('M3',BLUE,['无任务细节','少量任务片段','概述／主路径\n无命令代码','主路径＋代码／\n完整参考无代码','完整参考＋\n命令代码'],['No task details','A few task\nfragments','Overview / main\npath, no code','Main path + code /\nfull ref., no code','Full reference\n+ commands/code']),
('M4',BLUE,['版本标识缺失','版本已列（≥3）\n配套未明','芯片与框架可锁／\n其他情况','官方支持矩阵','版本无关／\n至多1个版本'],['Version IDs\nmissing','Versions listed (≥3),\npairing unclear','Chip–framework\npairing / other','Support matrix','Version irrelevant /\nat most one']),
('M7',M7_COLOR,['几乎依赖现查','知识有限，\n命令需查','概念熟悉，\n细节需查','流程熟悉，\n可给骨架','可凭已有知识\n作答（自评）'],['Relies on lookup','Limited knowledge;\nlook up commands','Concepts familiar;\nlook up details','Workflow familiar;\ncan outline steps','Can answer from\nprior (self-rating)']),
('M9',INDIGO,['无具体版本','有版本线索','范围或部分明确','基本确定','确切版本'],['No specific version','Version clues','Range / partial','Largely specified','Exact versions']),
('M10',INDIGO,['零散示意','主要流程骨架','需小幅修改','需替换参数','可直接采用'],['Isolated fragments','Main workflow\noutline','Minor edits','Replace parameters','Directly usable'])]

def canvas(lang,height):
 cn=lang=='cn';plt.rcParams.update({'font.family':'Arial Unicode MS' if cn else 'DejaVu Sans','svg.fonttype':'none','pdf.fonttype':42,'font.size':8,'text.color':'#252b39','axes.labelcolor':'#536574','xtick.color':'#536574','ytick.color':'#536574'})
 fig=plt.figure(figsize=(6.5,height/100),facecolor='white');ax=fig.add_axes([0,0,1,1]);ax.set(xlim=(0,650),ylim=(height,0));ax.axis('off')
 return fig,ax

def text(ax,x,y,s,sz=8,c='#252b39',ha='left'):
 ax.text(x,y,s,fontsize=sz,color=c,va='top',ha=ha,linespacing=1.2)

def rows(ax,lang,items,offset=0):
 start=63;cw=115;text(ax,8,7+offset,'得分' if lang=='cn' else 'Score')
 for j in range(5):text(ax,start+j*cw+cw/2-3,5+offset,str(j+1),11,items[0][1],'center')
 for i,(name,color,zh,en) in enumerate(items):
  y=31+i*42+offset;text(ax,8,y+7,name,8.5,color)
  for j,label in enumerate(zh if lang=='cn' else en):
   x=start+j*cw;mix=np.array(colors.to_rgb(color));strength=.2+.8*j/4
   ax.plot([x,x+cw-10],[y,y],lw=2,color='#e5eaf0' if name=='M2' and j==2 else mix*strength+(1-strength))
   text(ax,x+cw/2-5,y+7,label,8 if lang=='cn' else 7.6,ha='center')

def save(fig,name,lang):
 if args.only and name != args.only:
  plt.close(fig)
  return
 for ext in ('svg','pdf','png'):fig.savefig(OUT/f'figure-scoring-{name}-{lang}.{ext}',dpi=180)
 plt.close(fig)

for lang in ('cn','en'):
 cn=lang=='cn'
 fig,ax=canvas(lang,200);rows(ax,lang,ROWS[:4]);save(fig,'official',lang)
 fig,ax=canvas(lang,116);rows(ax,lang,ROWS[5:]);save(fig,'answers',lang)
 fig,ax=canvas(lang,300);rows(ax,lang,ROWS[4:5],offset=100)
 for pos,name,x,y,color,xlab in [([.085,.1266667,.385,.2666667],'M5',[0,1,2,3,4,5,6,7],[1,2,2,3,3,4,5,5],M5_COLOR,'去重来源数 n' if cn else 'Distinct third-party sources n'),([.59,.1266667,.385,.2666667],'M8',[0,1.5,2.5,4,6,8],[5,4,3,2,1,1],M8_COLOR,'加权成本 c' if cn else 'Weighted effort c')]:
  a=fig.add_axes(pos);a.step(x,y,where='post',color=color,lw=1.3)
  dense=np.linspace(0,x[-1],1601); heights=np.array(y)[np.clip(np.searchsorted(x,dense,side='right')-1,0,len(y)-1)]
  for lo,hi in zip(np.linspace(1,5,45)[:-1],np.linspace(1,5,45)[1:]):a.fill_between(dense,lo,np.minimum(heights,hi),where=heights>lo,step='post',color=(*colors.to_rgb(color),.025+.34*(hi-1)/4),linewidth=0)
  if name=='M8':
   for k in range(1,len(x)-1):
    a.plot(x[k],y[k-1],'o',ms=3,mfc=color,mec=color,zorder=4)
    a.plot(x[k],y[k],'o',ms=3,mfc='white',mec=color,mew=.7,zorder=4)
  else:a.plot(x,y,'o',ms=2.5,color=color)
  a.set(ylim=(.8,5.2),xlim=(0,x[-1]),yticks=[1,3,5],xticks=[0,1,3,5,6,7] if name=='M5' else [0,1.5,2.5,4,6,8]);a.tick_params(labelsize=7,length=2,pad=2,colors=color);a.grid(axis='y',color='#e5eaf0',lw=.5)
  a.spines[['top','right']].set_visible(False)
  for sp in ['left','bottom']:a.spines[sp].set_color('#d3dce5')
  a.set_xlabel(xlab,fontsize=7.5,labelpad=2)
  text(ax,pos[0]*650-34,180,name,8.5,color)
 # M6: apply the unchanged scoring method to task A's recorded inputs.
 text(ax,8,4,'M6',8.5,M6_COLOR)
 text(ax,63,2,'任务A · ATC转换' if cn else 'Task A · ATC conversion',8.5,M6_COLOR)
 text(ax,301,2,f'均值 {mean:.1f} ＋ 修正' if cn else f'Mean {mean:.1f} + adjustments',8.5,M6_COLOR)
 text(ax,517,2,'最终评分' if cn else 'Final score',8.5,M6_COLOR)
 labels=['知乎 · 专栏','阿里云 · 技术文章','博客园 · 博客 ×2','CSDN · 博客'] if cn else ['Zhihu · column','Aliyun · technical article','Cnblogs · blogs ×2','CSDN · blog']
 values=[f'{baselines[0]:.1f}',f'{baselines[1]:.1f}',f'{baselines[2]:.1f} ×2',f'{baselines[4]:.1f}']
 for y,val,label in zip([23,40,57,74],values,labels):
  ax.add_patch(plt.Rectangle((63,y-2),201,15,facecolor='#f0f3fa',edgecolor='none'))
  text(ax,68,y,label,7.3 if not cn else 8)
  text(ax,257,y,val,7.5,M6_COLOR,'right')
 for x1,x2 in [(270,293),(481,509)]:
  ax.annotate('',xy=(x2,52),xytext=(x1,52),arrowprops={'arrowstyle':'->','color':M6_COLOR,'lw':1})
 consist_label={'high':('一致性高','High consistency'),'mid':('一致性中','Medium consistency'),'low':('一致性低','Low consistency')}[example['consist']][0 if cn else 1]
 reasons=[consist_label,
          f'中位月龄 {median_age:g} 个月' if cn else f'Median age: {median_age:g} months',
          f'{platform_count} 平台 / {len(baselines)} 条来源' if cn else f'{platform_count} platforms / {len(baselines)} sources']
 for y,label,value in zip([27,48,69],reasons,adjustments):
  text(ax,301,y,label,7.5)
  text(ax,475,y,f'{value:+g}' if value else '0',8,M6_COLOR,'right')
 text(ax,577,25,f'{mean:.1f} + {adjustments[0]:g} + {adjustments[1]:g} + {adjustments[2]:g} = {mean+sum(adjustments):.1f}',7.5,ha='center')
 text(ax,577,43,str(final_score),21,M6_COLOR,'center')
 text(ax,577,76,'取整 · 1–5分' if cn else 'Rounded · 1–5 scale',7.5,M6_COLOR,'center')
 save(fig,'support',lang)
 fig,ax=canvas(lang,42);text(ax,8,7,'M11',8.5,SLATE)
 bounds=[0,.24,.45,.63,.8,1];labs=['很低','低','中','中高','高'] if cn else ['Very low','Low','Medium','Medium–high','High']
 for j,(lo,hi) in enumerate(zip(bounds,bounds[1:])):
  ax.add_patch(plt.Rectangle((63+lo*575,3),(hi-lo)*575,19,facecolor=['#f0f3f6','#d6e0e8','#b2c4d2','#8ba3b7','#61788d'][j],edgecolor='white',lw=.7));text(ax,63+(lo+hi)/2*575,7,labs[j],7.5,'white' if j==4 else '#252b39','center')
 for b in bounds:text(ax,63+b*575,26,f'{b:.2f}',7,SLATE,'center')
 save(fig,'confidence',lang)
