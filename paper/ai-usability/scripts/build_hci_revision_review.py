"""Build clean bilingual reading pages with a persistent outline."""
from pathlib import Path
import re, html, base64, sys

base = Path(__file__).resolve().parents[1]
css = '<style id="review-styles">\n@media screen{body{width:calc(100% - 300px);max-width:1060px;margin-left:280px;margin-right:20px;padding-left:36px;padding-right:36px}}\n#review-toc{position:fixed;left:16px;top:24px;bottom:24px;width:244px;z-index:1000;display:flex;flex-direction:column;background:#fff;border:1px solid #d9e0f2;border-radius:12px;box-shadow:0 4px 20px #1b29440d;font:14px/1.6 system-ui,sans-serif;color:#293346}\n#review-toc nav{flex:1;min-height:0;overflow-y:auto;overscroll-behavior:contain;padding:8px 10px 16px;scrollbar-width:thin}\n.review-toc-title{padding:16px 20px 12px;border-bottom:1px solid #edf0f5;font-weight:700;color:#344a87}\n.review-language-switch{display:flex;gap:6px;padding:10px 14px 0;font:13px/1.5 system-ui,sans-serif}\n#review-toc .review-language-switch a{flex:1;margin:0;padding:5px 8px;text-align:center;font-size:13px;font-weight:500;border:1px solid transparent}\n#review-toc .review-language-switch a[aria-current="page"]{color:#294b98;background:#edf2ff;border-color:#d5def3}\n#review-toc ol{list-style:none;margin:0;padding:0}\n#review-toc a{display:block;padding:7px 10px;border-radius:6px;color:#465069;text-decoration:none;overflow-wrap:anywhere}\n#review-toc .toc-sub a{padding-left:24px;font-size:13px;color:#697386}\n#review-toc .toc-main a{font-weight:600;margin-top:3px}\n#review-toc a:hover,#review-toc a:focus-visible{background:#f1f4fb;outline:2px solid #a9b9e2;outline-offset:-2px}\n#review-toc a[aria-current="location"]{background:#e9efff;color:#294b98;box-shadow:inset 3px 0 #5575bd}\nh2,h3{scroll-margin-top:24px}\n@media screen and (max-width:900px){#review-toc{width:196px;left:12px;top:12px;bottom:12px}body{width:calc(100% - 232px);margin-left:220px;margin-right:12px;padding-left:24px;padding-right:24px}}\n@media screen and (max-width:600px){#review-toc{width:132px;left:8px;font-size:12px}.review-toc-title{padding:12px 10px}#review-toc nav{padding:6px}#review-toc a{padding:6px}#review-toc .toc-sub a{padding-left:12px;font-size:11px}body{width:calc(100% - 156px);margin-left:148px;margin-right:8px;padding:20px 12px;font-size:14px}h1{font-size:22px}h2{font-size:20px}h3{font-size:17px}}\n@media(prefers-reduced-motion:no-preference){html{scroll-behavior:smooth}}\n@media print{#review-toc{display:none!important}body{width:auto;margin:0;padding:0}}</style>'
script = r'''<script>
(()=>{
const tocLinks=[...document.querySelectorAll('#review-toc nav a')];
const sections=tocLinks.map(a=>document.getElementById(decodeURIComponent(a.hash.slice(1))));
const params=new URLSearchParams(location.search);
let pending=false;
function updateToc(){
 let current=0;
 for(let i=0;i<sections.length;i++){if(sections[i].getBoundingClientRect().top<=110)current=i;else break;}
 tocLinks.forEach((a,i)=>{if(i===current)a.setAttribute('aria-current','location');else a.removeAttribute('aria-current');});
 pending=false;
}
window.addEventListener('scroll',()=>{if(!pending){pending=true;requestAnimationFrame(updateToc);}},{passive:true});
for(const link of document.querySelectorAll('[data-language]')){
 link.addEventListener('click',()=>{
  const target=new URL(link.href);
  const current=tocLinks.findIndex(a=>a.getAttribute('aria-current')==='location');
  if(window.scrollY>0)target.searchParams.set('section',String(Math.max(0,current)));
  link.href=target.href;
 });
}
if(params.has('section')){
 const index=Number(params.get('section'));
 if(Number.isInteger(index)&&index>=0&&index<sections.length){
  const restore=()=>{
   sections[index].scrollIntoView({block:'start',behavior:'instant'});
   updateToc();
   try{const url=new URL(location.href);url.searchParams.delete('section');url.hash=sections[index].id;history.replaceState(null,'',url);}catch(e){}
  };
  if(document.readyState==='complete')restore();else window.addEventListener('load',restore,{once:true});
 }
}
updateToc();
})();
</script>'''

def plain(fragment):
    return re.sub(r'\s+', ' ', html.unescape(re.sub('<[^>]+>', '', fragment))).strip()

def build(lang):
    source=(base/f'manuscript-{lang}-v0.2.html').read_text()
    page=source
    def embed(match):
        path=base/html.unescape(match[1])
        return 'src="data:image/svg+xml;base64,'+base64.b64encode(path.read_bytes()).decode()+'"'
    page=re.sub(r'src="(figures/[^\"]+)"',embed,page)
    name='中文审阅稿 · 当前版本' if lang=='cn' else 'English manuscript · Current version'
    page=re.sub(r'<title>.*?</title>',f'<title>{name}</title>',page,flags=re.S)
    page=re.sub(r'<div class="edition">.*?</div>',f'<div class="edition">{name}</div>',page,count=1,flags=re.S)
    entries=[]
    def heading(match):
        fragment=match[0]
        found=re.search(r'\bid="([^\"]+)"',fragment)
        anchor=html.unescape(found[1]) if found else f'review-section-{len(entries)+1}'
        if not found: fragment=fragment.replace('>',f' id="{anchor}">',1)
        level='toc-main' if match[1]=='2' else 'toc-sub'
        entries.append(f'<li class="{level}"><a href="#{html.escape(anchor,quote=True)}">{html.escape(plain(fragment))}</a></li>')
        return fragment
    page=re.sub(r'<h([23])\b[^>]*>.*?</h\1>',heading,page,flags=re.S)
    links=''.join(f'<a href="manuscript-{code}-review-changes.html" data-language="{code}"'+(' aria-current="page"' if code==lang else '')+'>'+label+'</a>' for code,label in [('cn','中文'),('en','English')])
    title='论文目录' if lang=='cn' else 'Contents'
    toc=f'<aside id="review-toc"><div class="review-toc-title">{title}</div><div class="review-language-switch" role="group" aria-label="Language">{links}</div><nav aria-label="{title}"><ol>'+''.join(entries)+'</ol></nav></aside>'
    pattern=r'<(p|h[1-6]|figcaption|table)\b[^>]*>.*?</\1>'
    assert [plain(m[0]) for m in re.finditer(pattern,source,re.S)]==[plain(m[0]) for m in re.finditer(pattern,page,re.S)]
    page=page.replace('</head>',css+'</head>').replace('</body>',toc+script+'</body>')
    (base/f'manuscript-{lang}-review-changes.html').write_text(page)
    print(f'{lang}: clean reading page, {len(entries)} outline entries')

for lang in (['en'] if '--english' in sys.argv else ['cn','en']):
    build(lang)
