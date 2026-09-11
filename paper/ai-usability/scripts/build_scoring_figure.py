"""Compact bilingual rubric figure; run with Matplotlib. Does not compute task scores."""
from pathlib import Path
import sys
from textwrap import wrap
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager, colors
import numpy as np
OUT=Path(__file__).resolve().parents[1]/'figures'
font_manager.fontManager.addfont('/System/Library/Fonts/Supplemental/Arial Unicode.ttf')
BLUE='#397ac0';M5_COLOR='#9869b9';M7_COLOR='#7e78c5';M8_COLOR='#a17cba';INDIGO='#239b8e';M6_COLOR='#6887c3';SLATE='#61788d'
NAMES = {}
for language in ('cn', 'en'):
 manuscript = OUT.parent / f'manuscript-{language}-v0.2.md'
 NAMES[language] = {
  fields[1].strip(): fields[2].strip()
  for line in manuscript.read_text().splitlines() if line.startswith('| M')
  for fields in [line.split('|')]
 }

def metric_label(name, lang):
 return f'{name}  {NAMES[lang][name]}'

def label_column(ax, name, lang, y, color):
 text(ax,8,y,name,8.5,color)
 label=NAMES[lang][name]
 lines=[label] if lang=='cn' else wrap(label,17,break_long_words=False,break_on_hyphens=False)
 text(ax,39,y,'\n'.join(lines),7.5 if lang=='cn' else 7,color)

def anchor_label(label,lang):
 if lang=='cn': return label
 return label.replace('Versions listed (\u22653),', '\u22653 versions listed').replace('Version irrelevant /\nat most one', 'Version irrelevant\n/ at most one')

ROWS=[
('M1',BLUE,['多轮仍难找到','换词定位／\n一轮排名>10','多轮命中／\n排名7–10','一轮排名2–6','一轮排名第1'],['Still not found','Refine query /\nrank >10','Multiple rounds /\nrank 7–10','First round: 2–6','First round: 1']),
('M2',BLUE,['robots限制','SPA正文\n获取受阻','任务相关正文\n部分可获取','服务端渲染\n正文可获取','静态正文\n可获取'],['robots restriction','SPA body\nblocked','Partial body\nretrieval','SSR body\nretrievable','Static body\nretrievable']),
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
 start=150;cw=98;text(ax,8,7+offset,'得分' if lang=='cn' else 'Score')
 for j in range(5):text(ax,start+j*cw+cw/2-5,5+offset,str(j+1),11,items[0][1],'center')
 for i,(name,color,zh,en) in enumerate(items):
  y=31+i*42+offset;label_column(ax,name,lang,y+5,color)
  for j,label in enumerate(zh if lang=='cn' else en):
   x=start+j*cw;mix=np.array(colors.to_rgb(color));strength=.2+.8*j/4
   ax.plot([x,x+cw-10],[y,y],lw=2,color=mix*strength+(1-strength))
   text(ax,x+cw/2-5,y+7,anchor_label(label,lang),7.7 if lang=='cn' else 7.1,ha='center')

def save(fig,name,lang):
 if '--official-only' in sys.argv and name!='official':
  plt.close(fig);return
 for ext in ('svg','pdf','png'):fig.savefig(OUT/f'figure-scoring-{name}-{lang}.{ext}',dpi=180)
 plt.close(fig)

for lang in ('cn','en'):
 cn=lang=='cn'
 fig,ax=canvas(lang,200);rows(ax,lang,ROWS[:4]);save(fig,'official',lang)
 fig,ax=canvas(lang,116);rows(ax,lang,ROWS[5:]);save(fig,'answers',lang)
 fig,ax=canvas(lang,310);rows(ax,lang,ROWS[4:5],offset=100)
 for pos,name,x,y,color,xlab in [([.085,38/310,.385,72/310],'M5',[0,1,2,3,4,5,6,7],[1,2,2,3,3,4,5,5],M5_COLOR,'去重来源数 n' if cn else 'Distinct third-party sources n'),([.59,38/310,.385,72/310],'M8',[0,1.5,2.5,4,6,8],[5,4,3,2,1,1],M8_COLOR,'加权成本 c' if cn else 'Weighted effort c')]:
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
  text(ax,pos[0]*650,179,metric_label(name,lang),8,color)
 # M6 separates source baselines, adjustments, and final integer grades.
 label_column(ax,'M6',lang,4,M6_COLOR)
 text(ax,150,2,'来源赋值' if cn else 'Source baselines',8.5,M6_COLOR)
 text(ax,353,2,'均值与修正' if cn else 'Mean + adjustments',8.5,M6_COLOR)
 text(ax,583,2,'最终评分' if cn else 'Final score',8.5,M6_COLOR,'center')
 labels=['聚合／转载','个人技术博客','声誉问答／专栏','云厂商文章／论文'] if cn else ['Aggregators / reposts','Personal tech blogs','Established Q&A / columns','Cloud-vendor articles / papers']
 for y,val,label in zip([23,40,57,74],[2.5,3,3.5,4],labels):
  ax.add_patch(plt.Rectangle((150,y-2),177,15,facecolor='#f0f3fa',edgecolor='none'))
  text(ax,154,y,label,6.8 if not cn else 7.5)
  text(ax,322,y,f'{val:.1f}',7.5,M6_COLOR,'right')
 for x1,x2 in [(331,346),(509,535)]:
  ax.annotate('',xy=(x2,52),xytext=(x1,52),arrowprops={'arrowstyle':'->','color':M6_COLOR,'lw':1})
 text(ax,353,27,'来源基准均值' if cn else 'Mean of baselines',7.5)
 text(ax,353,46,'＋一致性、时效、' if cn else '+ Consistency, recency,',7.0,M6_COLOR)
 text(ax,353,63,'  平台独立度修正' if cn else '  platform independence',7.0,M6_COLOR)
 text(ax,583,25,'取整并限制范围' if cn else 'Round + clamp',7.5,ha='center')
 text(ax,583,46,'1–5',18,M6_COLOR,'center')
 text(ax,583,76,'整数得分' if cn else 'Integer score',7.5,M6_COLOR,'center')
 save(fig,'support',lang)
 fig,ax=canvas(lang,42);label_column(ax,'M11',lang,7,SLATE)
 bounds=[0,.24,.45,.63,.8,1];labs=['很低','低','中','中高','高'] if cn else ['Very low','Low','Medium','Medium–high','High']
 for j,(lo,hi) in enumerate(zip(bounds,bounds[1:])):
  ax.add_patch(plt.Rectangle((150+lo*488,3),(hi-lo)*488,19,facecolor=['#f0f3f6','#d6e0e8','#b2c4d2','#8ba3b7','#61788d'][j],edgecolor='white',lw=.7));text(ax,150+(lo+hi)/2*488,7,labs[j],7.5,'white' if j==4 else '#252b39','center')
 for b in bounds:text(ax,150+b*488,26,f'{b:.2f}',7,SLATE,'center')
 save(fig,'confidence',lang)
