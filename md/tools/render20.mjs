/**
 * 用 20_human_ai_journey.html 自己的 d3 代码渲染出真实时序图 SVG。
 * 不重写绘制逻辑 —— 把原页内联 <script> 端到端跑起来，再序列化 #journey。
 * 每个配置用一套全新的 JSDOM（原脚本里有顶层 `let curLvl`，同域重跑会重复声明）。
 *
 * 用法：node render20.mjs
 * 依赖：npm i d3 jsdom（本机在 /Users/hsin/.workbuddy/binaries/node/workspace）
 * 产物写入 <repo>/md/figs/：20-seq-{D-l0,D-l1,D-l2,TR-l0}.svg
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { createRequire } from 'node:module';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const SRC = path.resolve(HERE, '..', '..', '20_human_ai_journey.html');
const OUTDIR = path.resolve(HERE, '..', 'figs');
fs.mkdirSync(OUTDIR, { recursive: true });

// ESM 的包解析只看「脚本自己所在的目录」，而 jsdom / d3 装在本机的公共目录里，
// 所以显式从 NODE_WS 去 require（Node 22 已支持 require(esm)）；失败再退回本地 import。
const WS = process.env.NODE_WS || '/Users/hsin/.workbuddy/binaries/node/workspace';
let JSDOM, d3;
try {
  const req = createRequire(path.join(WS, 'noop.cjs'));
  ({ JSDOM } = req('jsdom'));
  d3 = req('d3');
} catch (e) {
  ({ JSDOM } = await import('jsdom'));
  d3 = await import('d3');
}

const html = fs.readFileSync(SRC, 'utf8');
const js = [...html.matchAll(/<script(?![^>]*\bsrc=)[^>]*>([\s\S]*?)<\/script>/g)]
  .map(m => m[1]).reduce((a, b) => (b.length > a.length ? b : a));

function renderOnce(scen, lvl, tag) {
  const dom = new JSDOM(`<!DOCTYPE html><html><body>
<svg id="journey"></svg>
<input type="range" id="lvl" value="0">
<div id="lvlDesc"></div><div id="tip"></div><div id="tipmask"></div>
<div id="dscore"></div><div id="sctabs"></div><div id="conclbox"></div>
</body></html>`, { pretendToBeVisual: true, runScripts: 'outside-only' });

  const w = dom.window;
  global.window = w; global.document = w.document;
  try { Object.defineProperty(global, 'navigator', { value: w.navigator, configurable: true }); } catch (e) { }
  global.getComputedStyle = w.getComputedStyle;
  if (!w.SVGElement.prototype.getBBox) {
    w.SVGElement.prototype.getBBox = function () { return { x: 0, y: 0, width: 40, height: 14 }; };
  }
  w.d3 = d3;

  const driver = `setScenario(${JSON.stringify(scen)}); curLvl = ${lvl}; draw();`;
  try {
    w.eval(js + '\n;' + driver);
  } catch (e) {
    console.log(`!!! ${tag} 求值报错：`, e.message);
    return null;
  }
  const svg = w.document.getElementById('journey');
  // 源页的中文字体来自 body{font-family:'Noto Sans SC',sans-serif}，序列化后不会带上，
  // 这里补到根节点上，保证图在任何渲染器（含 GitHub / VS Code 预览）里字形一致。
  const FONT = "font-family:'Noto Sans SC','PingFang SC','Microsoft YaHei',sans-serif";
  const out = svg.outerHTML
    .replace('<svg ', '<svg xmlns="http://www.w3.org/2000/svg" ' +
      'xmlns:xlink="http://www.w3.org/1999/xlink" ')
    .replace(/(<svg\b[^>]*?)style="/, `$1style="${FONT};`)
    .replace(/<svg\b(?![^>]*style=)/, `<svg style="${FONT}" `);
  fs.writeFileSync(path.join(OUTDIR, `20-seq-${tag}.svg`), out, 'utf8');
  const texts = (out.match(/<text/g) || []).length;
  console.log(`  [${tag}] ${svg.getAttribute('width')}x${svg.getAttribute('height')}  ` +
    `text=${texts}  bytes=${out.length}`);
  return { tag, bytes: out.length, texts };
}

const done = [
  renderOnce('D', 0, 'D-l0'),
  renderOnce('D', 1, 'D-l1'),
  renderOnce('D', 2, 'D-l2'),
  renderOnce('TR', 0, 'TR-l0'),
];
console.log('完成', done.filter(Boolean).length, '张');
