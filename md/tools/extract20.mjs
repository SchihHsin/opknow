/**
 * 把 20_human_ai_journey.html 内嵌 <script> 的数据层（节点 / 分支 / 阶段 / 流程 / 详情 / 决策 / 终答表）
 * 端到端求值，导出成 JSON，供 gen20.py 生成 Markdown。
 *
 * 用法（在装有 jsdom 的目录下运行）：
 *   node extract20.mjs [源 HTML] [输出 JSON]
 * 默认从「本脚本所在目录」推断：源 HTML = <repo>/20_human_ai_journey.html，
 * 输出 = <脚本目录>/j20.json（该 JSON 是派生物，不入库）。
 * 依赖：npm i jsdom（本机在 /Users/hsin/.workbuddy/binaries/node/workspace）
 *
 * 注意：原脚本末尾有一句立即执行的 `setScenario("D")`，这里先掐掉，
 *      并在求值末尾自己调一次 setScenario，好让 `xi` / `dtier` 等派生字段被补齐。
 * 另外原脚本里有 `const svg = d3.select("#journey")` 之类的绘图语句，
 * 用一个「链式空壳」顶上（数据层不依赖真实 DOM）。
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const SRC = process.argv[2] || path.resolve(HERE, '..', '..', '20_human_ai_journey.html');
const OUT = process.argv[3] || path.join(HERE, 'j20.json');

const html = fs.readFileSync(SRC, 'utf8');
const js = [...html.matchAll(/<script(?![^>]*\bsrc=)[^>]*>([\s\S]*?)<\/script>/g)]
  .map(m => m[1]).reduce((a, b) => (b.length > a.length ? b : a));

const chain = new Proxy(function () { return chain; }, {
  get(t, k) {
    if (k === 'length') return 0;
    if (k === Symbol.toPrimitive) return () => '';
    if (k === Symbol.iterator) return function* () { };
    return chain;
  },
  apply: () => chain, set: () => true, has: () => true,
});

globalThis.d3 = chain;
globalThis.document = {
  querySelectorAll: () => [],
  getElementById: () => chain,
  querySelector: () => chain,
  addEventListener: () => { },
};
globalThis.window = {};

// eval 里的 const/let 出不了求值作用域，所以用 globalThis 回传结果，
// 不在 driver 里碰 fs（.mjs 是 ESM，没有 require）。
const driver = `
setScenario("D"); setScenario("TR");
globalThis.__J20 = {
  D_NODES, D_BRANCH, OWNER, D_PHASE, D_NDETAIL, D_PHASE_DETAIL, D_FLOW, D_ARCHFLOW,
  G_NODES, G_FLOW, G_BRANCH, G_PHASE, G_PHASE_DETAIL, G_NDETAIL, ARCHIVED_G,
  TR_NODES, TR_BRANCH, TR_PHASE, TR_PHASE_DETAIL, TR_FLOW, TR_NDETAIL, TR_ARCHFLOW,
  SCEN_D: SCENARIOS.D, SCEN_TR: SCENARIOS.TR, LVL,
};
`;

eval(js.split('setScenario("D")')[0] + driver);

const OUTDATA = globalThis.__J20;
if (!OUTDATA) { console.error('!! 数据层没取到，检查原脚本结构是否变了'); process.exit(1); }

fs.writeFileSync(OUT, JSON.stringify(OUTDATA, null, 1));
const q = OUTDATA;
console.log(
  'D 节点 ' + q.D_NODES.length + ' · 分支 ' + q.D_BRANCH.length +
  ' | TR 节点 ' + q.TR_NODES.length + ' · 分支 ' + q.TR_BRANCH.length +
  ' | G 节点 ' + q.G_NODES.length + ' | LVL ' + q.LVL.length +
  ' | D_NDETAIL 键 ' + Object.keys(q.D_NDETAIL).length);
console.log('已写出', OUT);
