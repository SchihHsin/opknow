# -*- coding: utf-8 -*-
"""
roi_counterfactual.py — 19_findings_ux_synthesis.html §5 欠账③「改进建议量化 ROI 排序」
====================================================================================
方法：对 §3 供给侧的每条改进做**反事实推演**——假设该改进落地后会把哪些 CANN 格的
哪个指标抬到多少，代回 score_metrics.py 的 ⑪ 噪声-OR 公式重算 26 格，按
「26 格 ⑪ 平均抬升量」排序。

诚实声明（与 19 §5 同步展示）：
- 基线 ①–⑩ 全部取 score_metrics.py 实测公式分；**反事实侧的目标值是假设**，
  每条假设在 SCENARIOS 里写明、可质疑可改。
- ⑨⑩ 不进 ⑪ 公式（因变量），故不做反事实。
- 改进 7（①–⑩ 当文档验收清单）是元改进、不直接抬任何格，不进本表。

用法：python3 roi_counterfactual.py
"""
import score_metrics as sm

BLK = sm.BLK

def lift(s, idx, to):
    """把指标 idx(0-based) 抬到 to（受阻也按 to 解除）；只抬不降。"""
    cur = s[idx]
    if cur == BLK or cur < to:
        s = list(s); s[idx] = to
    return s

def plus1(s, idx, cap=5):
    cur = s[idx]
    if cur == BLK:           # 受阻格不适用「+1」类改进（先要能抓到）
        return s
    s = list(s); s[idx] = min(cap, cur + 1)
    return s

# 每个场景：name, note(假设口径), fn(task, scores)->scores'
SCENARIOS = [
    ("1 版本一站收口",
     "假设：canonical 版本 + 配套查询器落地 → 全部 CANN 格 ④版本清晰 抬到 5。",
     lambda t, s: lift(s, 3, 5)),
    ("2 错误码一码一页",
     "假设：EZ9999 等兜底页拆成逐条着陆页 → 仅 E ③详尽 2→5（其他任务不受益）。",
     lambda t, s: lift(s, 2, 5) if t == "E" else s),
    ("3 opdevg 静态化",
     "假设：D 的核心 how-to 链路(devguide/opdevg)可抓 → D ②2→5、③受阻→4（保守取 4，对齐 A/B 上修先例）。",
     lambda t, s: lift(lift(s, 1, 5), 2, 4) if t == "D" else s),
    ("4 llms.txt·机器可读出口",
     "假设：全站 llms-full.txt/纯文本出口 → 全部格 ②抓取 抬到 5；受阻格 ③ 同步解除→4（llms-full 含正文）。",
     lambda t, s: lift(lift(s, 1, 5), 2, 4) if s[2] == BLK else lift(s, 1, 5)),
    ("5 页面组织可抓取性规范",
     "假设：正文进首屏/命令禁截图/一页收完主路径 → 已可抓格(②≥4)的 ③详尽 +1(封顶5)；受阻格不适用。",
     lambda t, s: plus1(s, 2) if (s[1] != BLK and s[1] >= 4 and s[2] != BLK) else s),
    ("6 二手生态扶持",
     "假设：多平台扶持(选 Agent 可抓平台) → 全部格 ⑤二手量 +1、⑥二手信 +1（各封顶 5）。",
     lambda t, s: plus1(plus1(s, 4), 5)),
    ("8 训练语料供给(长期)",
     "假设：权威语料以易收录形态存在(公开仓 markdown/英文版) → 下一代模型 ⑦自带 +1（封顶 5）。慢变量、跨模型代际见效。",
     lambda t, s: plus1(s, 6)),
]

def main():
    base = sm.compute()
    rows = []
    for name, note, fn in SCENARIOS:
        tot, ups, best, best_t = 0.0, 0, 0.0, ""
        for t in sm.TASKS:
            s0 = base[t]["cann"]["scores"][:10]
            sc0, band0, _ = sm.score11_overall(s0)
            s1 = fn(t, list(s0))
            sc1, band1, _ = sm.score11_overall(s1)
            d = sc1 - sc0
            tot += d
            if band1[1] > band0[1]:
                ups += 1
            if d > best:
                best, best_t = d, t
        rows.append((name, note, tot / len(sm.TASKS), ups, best, best_t))

    rows.sort(key=lambda r: -r[2])
    print("§5-3 供给侧改进反事实 ROI（26 个 CANN 格，⑪ 噪声-OR 公式重算）")
    print("=" * 86)
    print(f'{"改进（按 ROI 排序）":<26}{"平均⑪抬升":>9}{"翻档格数":>7}{"最大单格抬升":>11}')
    for name, note, avg, ups, best, best_t in rows:
        print(f"{name:<28}{avg:>+9.3f}{ups:>9}{best:>+10.2f} ({best_t})")
    print()
    for name, note, *_ in rows:
        print(f"· {name}：{note}")

if __name__ == "__main__":
    main()
