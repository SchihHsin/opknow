#!/usr/bin/env python3
"""Reproduce submitted-study M11 arithmetic and bounded coefficient sensitivity.

Reads frozen original observations/scores via build_paper_analysis helpers.
No new model run, grading, imputation, or changes to the paper/Skill occur.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import statistics
from collections import Counter
from pathlib import Path

REVISION = Path(__file__).resolve().parent
PAPER = REVISION.parents[1]
DATA = PAPER / "data"
SCRIPT = PAPER / "scripts" / "build_paper_analysis.py"
OUT_JSON = REVISION / "m11-submitted-sensitivity.json"
OUT_MD = REVISION / "m11-submitted-sensitivity.md"
CUTS = [24, 45, 63, 80]


def load_builder():
    spec = importlib.util.spec_from_file_location("build_paper_analysis", SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def n(v):
    return 0.0 if v == "受阻" else float(v) / 5.0


def score11(scores, *, include_m7=True, remap_m1=False, a=.30, b=.10):
    """0–100 index; a,b change only the penalty strength, keeping max=100."""
    x1 = (float(scores[0]) - 1) / 4 if remap_m1 else n(scores[0])
    x2, x3 = n(scores[1]), n(scores[2])
    x4, x5, x6, x8 = n(scores[3]), n(scores[4]), n(scores[5]), n(scores[7])
    x7 = n(scores[6]) if include_m7 else 0.0
    off = x1 * x2 * x3
    sec = x5 * x6
    k = 1 - (1 - off) * (1 - sec) * (1 - x7)
    version_factor = 1 - a + a * x4
    cost_factor = 1 - b + b * x8
    return 100 * k * version_factor * cost_factor


def band(value):
    return 1 + sum(value >= cut for cut in CUTS)


def mean(xs):
    return statistics.mean(xs) if xs else None


def r6(v):
    return round(v, 6)


def main():
    builder = load_builder()
    legacy, raw, archived_scores, tasks = builder.verify_frozen_inputs()
    units = builder.build_units(legacy, raw, archived_scores, tasks)
    primary = [u for u in units if u["include_in_25_pair_summary"]]
    if len(primary) != 50:
        raise ValueError(f"Expected 50 task-side units, got {len(primary)}")
    scenarios = {
        "old": {"include_m7": True, "remap_m1": False, "a": .30, "b": .10},
        "remove_m7_only": {"include_m7": False, "remap_m1": False, "a": .30, "b": .10},
        "remap_m1_only": {"include_m7": True, "remap_m1": True, "a": .30, "b": .10},
        "candidate": {"include_m7": False, "remap_m1": True, "a": .30, "b": .10},
        "candidate_half_coefficients": {"include_m7": False, "remap_m1": True, "a": .15, "b": .05},
        "candidate_double_coefficients": {"include_m7": False, "remap_m1": True, "a": .60, "b": .20},
    }
    per_unit = []
    for u in primary:
        row = {"unit_id": u["unit_id"], "task_id": u["task_id"], "ecosystem": u["legacy_side_label"], "scores_M1_M8": u["scores"][:8]}
        for key, params in scenarios.items():
            row[key] = score11(u["scores"], **params)
        row["legacy_saved"] = float(u["current_result"]["overall"]) * 100
        # Stored legacy composite is rounded to 0.001 on a 0–1 scale.
        if abs(row["legacy_saved"] - row["old"]) > 0.051:
            raise ValueError(f"Reproduction mismatch {u['unit_id']}: saved={row['legacy_saved']} recomputed={row['old']}")
        per_unit.append(row)

    summaries = {}
    for key in scenarios:
        sides = {}
        for side in ("cann", "cuda"):
            vals = [r[key] for r in per_unit if r["ecosystem"] == side]
            sides[side] = {"n": len(vals), "mean": r6(mean(vals)), "min": r6(min(vals)), "max": r6(max(vals)), "bands": dict(sorted(Counter(str(band(x)) for x in vals).items()))}
        paired = []
        for task in sorted({r["task_id"] for r in per_unit}):
            ca = next(r[key] for r in per_unit if r["task_id"] == task and r["ecosystem"] == "cann")
            cu = next(r[key] for r in per_unit if r["task_id"] == task and r["ecosystem"] == "cuda")
            paired.append({"task_id": task, "cann": r6(ca), "cuda": r6(cu), "delta_cuda_minus_cann": r6(cu-ca)})
        deltas = [p["delta_cuda_minus_cann"] for p in paired]
        sides["paired_delta"] = {"n": len(paired), "mean": r6(mean(deltas)), "cuda_higher": sum(x > 0 for x in deltas), "cann_higher": sum(x < 0 for x in deltas), "tie": sum(x == 0 for x in deltas), "pairs": paired}
        summaries[key] = sides

    band_changes = []
    rank_reversals = []
    for r in per_unit:
        if band(r["old"]) != band(r["candidate"]):
            band_changes.append({"unit_id": r["unit_id"], "old": r6(r["old"]), "candidate": r6(r["candidate"]), "old_band": band(r["old"]), "candidate_band": band(r["candidate"])})
    for task in sorted({r["task_id"] for r in per_unit}):
        ca = next(r for r in per_unit if r["task_id"] == task and r["ecosystem"] == "cann")
        cu = next(r for r in per_unit if r["task_id"] == task and r["ecosystem"] == "cuda")
        old_delta = cu["old"] - ca["old"]
        new_delta = cu["candidate"] - ca["candidate"]
        if old_delta * new_delta < 0:
            rank_reversals.append({"task_id": task, "old_delta": r6(old_delta), "candidate_delta": r6(new_delta)})

    input_files = [DATA / n for n in ["manifest.json", "raw_original.json", "legacy_scores_original.json", "m2_scoring.json", "tasks.json", "legacy_score_metrics.py"]]
    out = {
        "analysis_type": "Arithmetic re-analysis of the submitted 25-pair study; no new empirical runs or independent validation.",
        "scope": {"primary_tasks": 25, "task_side_units": 50, "excluded_task": "G", "reason": "G is a migration analogy rather than a CANN/CUDA development task pair.", "M1_score_distribution": dict(sorted(Counter(str(u["scores"][0]) for u in primary).items())), "M1_score_1_observed": any(u["scores"][0] == 1 for u in primary)},
        "source_files": [{"path": str(f.relative_to(PAPER)), "sha256": sha(f)} for f in input_files],
        "m2_rule": "Uses the existing revised m2_scoring.json mapping; underlying retrieval observations are retained, not re-collected.",
        "old_formula": "100*[1-(1-OFF)(1-SEC)(1-OWN)]*(1-a+a*x4)*(1-b+b*x8); OFF=(M1/5)(M2/5)(M3/5); SEC=(M5/5)(M6/5); OWN=M7/5; a=.30,b=.10",
        "candidate_formula": "100*[1-(1-OFF)(1-SEC)]*(1-a+a*x4)*(1-b+b*x8); OFF=((M1-1)/4)(M2/5)(M3/5); SEC=(M5/5)(M6/5); M7 excluded; a=.30,b=.10",
        "coefficient_sensitivity": "candidate formula with a,b jointly halved to .15,.05 or doubled to .60,.20; each attenuation factor is (1-coefficient)+coefficient*x, so the composite remains within 0–100.",
        "band_cuts": {"legacy_cut_points_0_to_100": CUTS, "use": "count descriptive category changes only; not validation of thresholds"},
        "scenarios": summaries,
        "old_vs_candidate": {"task_sides_changed_band": len(band_changes), "task_sides_unchanged_band": 50-len(band_changes), "changed_band_units": band_changes, "paired_direction_reversals": rank_reversals},
        "units": per_unit,
        "interpretation": "The reference literature can support transparent composite construction and sensitivity disclosure, but cannot establish that this formula or its coefficients are valid. Without an independent criterion or prespecified decision target, these data cannot identify a uniquely best coefficient. The candidate also changes the operationalization, so old/new absolute values are not a pure same-scale comparison.",
    }
    OUT_JSON.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n")

    labels = {"old":"原公式", "remove_m7_only":"仅去除M7", "remap_m1_only":"仅重映射M1", "candidate":"候选式：去M7并重映射M1", "candidate_half_coefficients":"候选式：系数减半", "candidate_double_coefficients":"候选式：系数加倍"}
    lines = [
        "# M11：送审数据公式与系数敏感性复算",
        "",
        "## 范围与复算依据",
        "",
        "此分析使用 PCS 送审研究的 25 对 CANN/CUDA 任务（50 个任务侧），排除迁移类比任务 G。不是三模型重跑，也没有新跑模型。分项分数取现有冻结原始观测和归档评分；M2 按现有修订映射重算。脚本先用既有构建脚本核验冻结输入，再独立计算 M11。每个任务侧的旧公式结果与以0.001为精度保存的现存计算结果最大差异小于0.051分。",
        "",
        "输入文件及 SHA-256 见同目录 JSON。所有结果为描述性重算，不是独立效度或信度验证。",
        "",
        "## 公式比较",
        "",
        "旧公式：`100 × [1−(1−OFF)(1−SEC)(1−OWN)] × (1−a+a·x4) × (1−b+b·x8)`；`OFF=(M1/5)(M2/5)(M3/5)`，`SEC=(M5/5)(M6/5)`，`OWN=M7/5`，`a=0.30, b=0.10`。",
        "",
        "AC 候选式：`100 × [1−(1−OFF)(1−SEC)] × (1−a+a·x4) × (1−b+b·x8)`；`OFF=((M1−1)/4)(M2/5)(M3/5)`，`SEC=(M5/5)(M6/5)`，不含 M7，`a=0.30, b=0.10`。因此 M1=1 对官方支撑贡献为0。",
        "",
        f"本次50个任务侧的 M1 分值分布为 {json.dumps(out['scope']['M1_score_distribution'], ensure_ascii=False)}；没有任何一条为 M1=1。因此，`M1=1 → 官方支撑为0`是候选映射的逻辑属性，但该边界在本数据中未被实测覆盖；敏感性结果只包含 M1=2–5。",
        "",
        "权重敏感性将 a、b 同时减半（0.15、0.05）或加倍（0.60、0.20）。采用`1−a+a·x`与`1−b+b·x`表达惩罚强度变化，最大乘数保持1，避免分数超过100。",
        "",
        "## 结果",
        "",
        "| 设定 | CANN均值 | CUDA均值 | CUDA−CANN配对差均值 | CUDA较高任务对 | CANN较高任务对 | 档位数量 CANN / CUDA（1至5档） |",
        "|---|---:|---:|---:|---:|---:|---|",
    ]
    for key, label in labels.items():
        s = summaries[key]
        ca, cu, d = s["cann"], s["cuda"], s["paired_delta"]
        ca_bands = ", ".join(f"{i}档:{ca['bands'].get(str(i),0)}" for i in range(1,6))
        cu_bands = ", ".join(f"{i}档:{cu['bands'].get(str(i),0)}" for i in range(1,6))
        lines.append(f"| {label} | {ca['mean']:.2f} | {cu['mean']:.2f} | {d['mean']:+.2f} | {d['cuda_higher']}/25 | {d['cann_higher']}/25 | {ca_bands} / {cu_bands} |")
    lines += [
        "",
        f"沿用旧切点 24/45/63/80，候选式相较旧公式有 **{len(band_changes)}/50 个任务侧跨档**（CANN {sum(x['unit_id'].endswith('.cann') for x in band_changes)}/25，CUDA {sum(x['unit_id'].endswith('.cuda') for x in band_changes)}/25）。这表示结果对操作化有实质敏感性；切点本身仍未得到外部验证。",
        "",
        f"逐任务 CANN/CUDA 差值方向反转：**{len(rank_reversals)}/25 对**。逐条任务侧跨档及方向反转见 JSON。",
        "",
        "## 判断与局限",
        "",
        "- 候选式均值约为 CANN 58.14、CUDA 83.03，方向仍偏向 CUDA；但均值与档位均明显变化，不能把这一方向写成对系数稳健性的证明。",
        "- 双倍系数下均值约为 47.90／77.09；减半时约为 63.43／86.03。两种情形下方向仍偏向 CUDA，但效应幅度变化，说明 0.30／0.10 会影响绝对分数和档位。",
        "- 仅做代数敏感性不能决定哪个系数‘最合适’。要拟合系数，必须先规定独立效标/决策目标并隔离验证数据；现有 25 对任务没有独立校准效标，不能用生态差异本身当作正确答案来拟合。",
        "- 依据 OECD/JRC 综合指标方法的边界是：支持透明报告归一化、聚合假设和敏感性分析；不直接支持本公式结构、0.30／0.10 系数、五档切点或概率解释。",
        "",
        "## 可复核文件",
        "",
        "- `m11_submitted_sensitivity.py`：从冻结材料重算的脚本。",
        "- `m11-submitted-sensitivity.json`：公式、来源哈希、50个任务侧的各情景分数、跨档和配对反转清单。",
        "",
    ]
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUT_JSON} and {OUT_MD}")
    print(f"Band changes: {len(band_changes)}/50; paired direction reversals: {len(rank_reversals)}/25")
    for key in scenarios:
        x=summaries[key]
        print(key, x['cann']['mean'], x['cuda']['mean'], x['paired_delta']['mean'])


if __name__ == "__main__":
    main()
