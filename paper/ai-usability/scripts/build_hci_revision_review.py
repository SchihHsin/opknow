"""Compare the pre-HCI snapshot with the latest manuscript; retain all manuscript content."""
from pathlib import Path
import re,html,json,difflib,subprocess,base64,sys
root=Path(__file__).resolve().parents[3]; base=root/'paper/ai-usability'
a=(base/'manuscript-cn-before-29c87cc.html').read_text()
# Regenerate from the current reading edition; never use the annotated output as input.
historical='--historical' in sys.argv
b=subprocess.check_output(['git','show','a7beaea:paper/ai-usability/manuscript-cn-after-f5e6f83.html'],text=True,cwd=root) if historical else (base/'manuscript-cn-v0.2.html').read_text()
def embed(match):
 path=base/html.unescape(match[1])
 assert path.suffix=='.svg',path
 return 'src="data:image/svg+xml;base64,'+base64.b64encode(path.read_bytes()).decode()+'"'
b=re.sub(r'src="(figures/[^\"]+)"',embed,b)
b=re.sub(r'<title>.*?</title>','<title>最新中文审阅版 · 修改高亮与改前对照</title>',b,flags=re.S)
b=re.sub(r'<div class="edition">.*?</div>','<div class="edition">最新中文全文 · 修改高亮　|　<a href="manuscript-cn-before-29c87cc.html">查看改前全文</a>　|　<a href="manuscript-cn-v0.2.html">无标记阅读版</a></div>',b,count=1,flags=re.S)
# Apply the approved label cleanup to embedded historical artwork as well.
if historical:
 def clean_historical_image(match):
  svg=base64.b64decode(match[1]).decode()
  svg=svg.replace('CUDA‡','CUDA').replace('‡ For G','For G').replace('‡ G 的','G 的')
  headers=re.findall(r'<rect x="([0-9]+)" y="66" width="186"',svg)
  if headers:
   row_width=max(map(int,headers))+186-12
   svg=re.sub(r'(<rect x="12" y="[0-9]+" width=")1074(" height=)',lambda m:m[1]+str(row_width)+m[2],svg)
  return 'src="data:image/svg+xml;base64,'+base64.b64encode(svg.encode()).decode()+'"'
 b=re.sub(r'src="data:image/svg\+xml;base64,([^"]+)"',clean_historical_image,b)
pattern=re.compile(r'<(p|h[1-6]|figcaption)\b[^>]*>.*?</\1>',re.S)
def plain(s):return re.sub(r'\s+',' ',html.unescape(re.sub('<[^>]+>','',s))).strip()
def key(s):return re.sub(r'\s+','',plain(s))
aa=list(pattern.finditer(a));bb=list(pattern.finditer(b));changes={};items=[]
sm=difflib.SequenceMatcher(None,[key(m[0]) for m in aa],[key(m[0]) for m in bb],autojunk=False)
for op,i,j,k,l in sm.get_opcodes():
 if op=='equal':continue
 old='\n\n'.join(plain(m[0]) for m in aa[i:j])
 if k==l:
  raise RuntimeError('Deletion needs a separate visible marker')
 for n in range(k,l):
  items.append({'kind':'新增段落' if i==j else '修改段落','old':old or '此处为新增内容，改前没有对应段落。'})
  changes[n]=len(items)-1
def underline_changes(fragment, old):
 # Map visible non-whitespace characters back to their original HTML tokens.
 tokens=re.findall(r'<[^>]*>|&(?:#[xX][0-9a-fA-F]+|#[0-9]+|[a-zA-Z][a-zA-Z0-9]+);|.',fragment,re.S)
 visible=''.join(html.unescape(t) for t in tokens if not t.startswith('<'))
 new=re.sub(r'\s+','',visible)
 marked=set()
 for op,_,__,start,end in difflib.SequenceMatcher(None,re.sub(r'\s+','',old),new,autojunk=False).get_opcodes():
  if op in ('insert','replace'):marked.update(range(start,end))
 out=[];buffer=[];state=False;pos=0
 def flush():
  if buffer:
   text=''.join(buffer);out.append('<u class="review-word">'+text+'</u>' if state else text);buffer.clear()
 for token in tokens:
  if token.startswith('<'):
   flush();out.append(token);continue
  value=html.unescape(token);length=len(re.sub(r'\s+','',value))
  highlight=any(i in marked for i in range(pos,pos+length)) if length else state
  if highlight!=state:flush();state=highlight
  buffer.append(token);pos+=length
 flush()
 assert pos==len(new)
 return ''.join(out)
for n in reversed(range(len(bb))):
 if n not in changes:continue
 m=bb[n];s=m[0];idx=changes[n]
 s=underline_changes(s, "" if items[idx]["kind"]=="新增段落" else items[idx]["old"])
 s=re.sub(r'^(<\w+)',r'\1 class="review-change" tabindex="0" data-review="'+str(idx)+'"',s,count=1)
 b=b[:m.start()]+s+b[m.end():]
# Embedded figure changes are compared independently of captions.
fig=re.compile(r'<figure\b[^>]*>.*?</figure>',re.S)
oldfig=list(fig.finditer(a));newfig=list(fig.finditer(b))
assert len(oldfig)==len(newfig)==15
for i in reversed(range(15)):
 oldimg=re.search(r'<img\b[^>]*>',oldfig[i][0],re.S)[0]
 newimg=re.search(r'<img\b[^>]*>',newfig[i][0],re.S)[0]
 if re.search(r'src="([^"]+)"',oldimg)[1]!=re.search(r'src="([^"]+)"',newimg)[1]:
  idx=len(items);items.append({'kind':f'图 {i+1} 已修改','old':'改前图示如下，可与正文中的改后图对照。','image':oldimg})
  m=newfig[i];s=m[0];s=s.replace('>',f'><button type="button" class="review-figure" data-review="{idx}">图 {i+1} 有修改 · 悬浮查看改前图</button>',1)
  b=b[:m.start()]+s+b[m.end():]
css='''<style id="review-styles">
.review-change{background:rgba(240,255,70,.28);border:0;cursor:help;transition:background .15s}.review-change:hover,.review-change:focus{background:rgba(240,255,70,.36);outline:none}.review-word{text-decoration:underline;text-decoration-style:dashed;text-decoration-color:currentColor;text-decoration-thickness:1px;text-underline-offset:3px}.review-figure{border:1px solid #abb6e1;border-radius:6px;background:#eef2ff;color:#394d85;padding:7px 12px;cursor:help;font:13px system-ui;margin-bottom:12px}.review-toolbar{background:#f5f7ff;border:1px solid #d9e0f2;border-radius:8px;padding:13px 16px;margin:0 0 24px;font:14px/1.6 system-ui;color:#48536d}.review-toolbar p{margin:0}.review-toolbar button{font:inherit;color:#344a87;background:white;border:1px solid #c4cde5;border-radius:5px;padding:3px 9px;margin:9px 8px 0 0;cursor:pointer}#review-tip{position:fixed;z-index:9999;width:min(540px,calc(100vw - 32px));max-height:70vh;overflow:auto;background:#fff;border:1px solid #c5cde0;border-radius:10px;padding:18px 20px;box-shadow:0 12px 48px #1b294433;font:15px/1.8 system-ui;color:#293346}#review-tip[hidden]{display:none}#review-tip strong{color:#4659a0;display:block;margin-bottom:8px}#review-tip .old-text{white-space:pre-wrap}#review-tip img{width:100%;height:auto}#review-tip button{float:right;border:0;background:#f0f3f8;border-radius:4px;cursor:pointer;padding:3px 8px}.review-muted .review-change{background:transparent;border-color:transparent}.review-current{background:rgba(240,255,70,.40)!important;outline:none!important}.review-muted .review-word{text-decoration:none}@media print{.review-toolbar,#review-tip,.review-figure{display:none}.review-change{background:transparent;border:0;padding:0;margin-left:0}}
/* Reserve a separate comparison column so the source paragraph stays visible. */
@media screen and (min-width:1100px){body{width:calc(100% - 420px);max-width:1060px;margin-left:max(20px,calc((100vw - 1480px)/2));margin-right:400px;padding-left:44px;padding-right:44px}#review-tip{position:fixed;right:20px;top:24px;width:360px;max-height:calc(100vh - 48px)}}
@media screen and (max-width:1099px){#review-tip{position:static;width:100%;max-height:420px;margin:16px 0 24px;box-shadow:0 4px 18px #1b294414}}
@media print{body{width:auto;margin:0;padding:0}}
</style>'''
bar=f'''<aside class="review-toolbar"><p><strong>人机交互叙述调整 · 前后对照</strong>　大改之前 → 当前最新版</p><p>荧光黄色标出修改或新增段落，下划线标出具体新增或替换的文字。悬浮、点击或按 Tab 聚焦可查看改前内容；宽屏在右侧并排显示，窄屏在当前段落下方展开，不遮挡正文。按 Esc 关闭。共 {len(changes)} 处段落变动及 {len(items)-len(changes)} 处图示变动。正文采用当前最新版，包含之后已确认的摘要、相关工作及岗位措辞等修订；悬浮内容来自大改之前的版本。</p><button id="review-prev">上一处</button><button id="review-next">下一处</button><button id="review-toggle">隐藏高亮</button><span id="review-position"></span></aside>'''
b=b.replace('</head>',css+'</head>')
b=b.replace('<h1',bar+'<h1',1)
b=b.replace('</body>','''<div id="review-tip" role="dialog" aria-label="改前内容" hidden><button aria-label="关闭">×</button><strong></strong><div class="old-text"></div><div class="old-image"></div></div>
<script id="review-data" type="application/json">'''+json.dumps(items,ensure_ascii=False).replace('</','<\/')+'''</script>
<script>
(()=>{const data=JSON.parse(document.getElementById('review-data').textContent),tip=document.getElementById('review-tip'),nodes=[...document.querySelectorAll('[data-review]')];let active=null,timer,index=-1;
function hide(){tip.hidden=true;active=null}
function show(el){clearTimeout(timer);active=el;const d=data[+el.dataset.review];tip.querySelector('strong').textContent=d.kind+' · 改前';tip.querySelector('.old-text').textContent=d.old;tip.querySelector('.old-image').innerHTML=d.image||'';if(innerWidth>=1100){document.body.appendChild(tip)}else{el.insertAdjacentElement('afterend',tip)}tip.hidden=false}

for(const el of nodes){el.addEventListener('mouseenter',()=>show(el));el.addEventListener('focus',()=>show(el));el.addEventListener('click',()=>show(el));}
tip.addEventListener('mouseenter',()=>clearTimeout(timer));tip.querySelector('button').onclick=hide;document.addEventListener('keydown',e=>{if(e.key==='Escape')hide()});document.addEventListener('click',e=>{if(!tip.contains(e.target)&&!e.target.closest('[data-review]'))hide()});window.addEventListener('resize',()=>{if(active)show(active)});
function go(delta){index=(index+delta+nodes.length)%nodes.length;nodes.forEach(n=>n.classList.remove('review-current'));const el=nodes[index];el.classList.add('review-current');el.scrollIntoView({block:'center',behavior:'smooth'});document.getElementById('review-position').textContent=(index+1)+' / '+nodes.length}
document.getElementById('review-next').onclick=()=>go(1);document.getElementById('review-prev').onclick=()=>go(-1);document.getElementById('review-toggle').onclick=e=>{document.body.classList.toggle('review-muted');e.target.textContent=document.body.classList.contains('review-muted')?'显示高亮':'隐藏高亮'};
})();
</script></body>''')
if historical:
 b=b.replace('大改之前 → 当前最新版','29c87cc → f5e6f83 · 历史对照')
 b=b.replace('正文采用当前最新版，包含之后已确认的摘要、相关工作及岗位措辞等修订；悬浮内容来自大改之前的版本。','本页是历史快照；<a href="manuscript-cn-review-changes.html">查看包含后续修订的最新高亮审阅版</a>。')
 b=b.replace('<title>最新中文审阅版 · 修改高亮与改前对照</title>','<title>历史中文审阅版 · f5e6f83 · 高亮对照</title>')
 b=b.replace('最新中文全文 · 修改高亮','历史中文全文 · f5e6f83 · 修改高亮')
(base/('manuscript-cn-after-f5e6f83.html' if historical else 'manuscript-cn-review-changes.html')).write_text(b)
print('Annotated',len(changes),'text blocks and',len(items)-len(changes),'figures')
# All original paragraph content and all embedded current images are unchanged.
assert [key(m[0]) for m in pattern.finditer(b.split('<div id="review-tip"')[0]) if '人机交互叙述调整' not in m[0] and '荧光黄色标出' not in m[0]]==[key(m[0]) for m in bb]
