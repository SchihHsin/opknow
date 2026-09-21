"""Gated adapter/renderer for the new workflow matrix.

The CLI never touches the working manuscript or its existing figures.  It
accepts only a formal 156-row consolidation and writes SVGs below the caller's
explicit staging directory.
"""
from __future__ import annotations
import argparse, html, json
from collections import Counter
from pathlib import Path
from matrix_input import METRICS, load_complete

MAIN_TASKS = tuple(chr(i) for i in range(ord("A"), ord("Z") + 1) if chr(i) != "G")
MODELS = ("glm-5.3", "deepseek-v4.1-flash", "kimi-k3-2")
PALETTE = ("#E02128", "#F4840C", "#058358", "#127180", "#3979F9")
SIDE_COLORS = {"cann": "#087e79", "cuda": "#5366c4"}
STATUS_LABELS = {"not_applicable": "N/A", "blocked": "B", "needs_review": "NR",
                 "unscorable": "U", "not_assessed": "P"}


def _esc(value):
    return html.escape(str(value), quote=True)


def _tone(score, metric):
    if metric == "M11":
        return PALETTE[min(4, max(0, int(float(score) // 20)))]
    return PALETTE[max(0, min(4, int(float(score) + 0.5) - 1))]


def _value(metric, metric_id):
    score = metric.get("score")
    if score is not None:
        # Keep exact numeric value in the title; constrain the cell label to
        # avoid overflowing the fixed matrix cell.
        if metric_id == "M11":
            return f"{float(score):.1f}".rstrip("0").rstrip(".")
        if metric_id == "M2":
            return f"{float(score):.2f}".rstrip("0").rstrip(".")
        return str(int(score)) if float(score).is_integer() else f"{float(score):.0f}"
    return STATUS_LABELS.get(metric.get("status"), "?")


def _cell(metric, metric_id, x, y, width, height):
    value = _value(metric, metric_id)
    status = metric.get("status", "unknown")
    reason = metric.get("reason") or metric.get("missing_reason") or ""
    score = metric.get("score")
    if score is not None:
        color = _tone(score, metric_id)
        shape = (f'<rect x="{x+1}" y="{y+1}" width="{width-2}" height="{height-2}" '
                 f'rx="3" fill="{color}" fill-opacity=".05" stroke="{color}" stroke-opacity=".1"/>')
        text_color = color
    else:
        shape = (f'<rect x="{x+1}" y="{y+1}" width="{width-2}" height="{height-2}" '
                 'fill="#f2f3f5" stroke="#d5dfe0" stroke-width=".6"/>')
        text_color = "#596474"
    raw_score = "" if score is None else f"; raw_score={score!r}"
    title = f"{metric_id}: status={status}{raw_score}; reason={reason}"
    fs = 12 if len(value) > 8 else 13
    return (f"<g><title>{_esc(title)}</title>{shape}"
            f'<text x="{x+width/2}" y="{y+height/2+4}" font-size="{fs}" '
            f'fill="{text_color}" text-anchor="middle">{_esc(value)}</text></g>')


def _svg(model, rows, tasks, language, coverage):
    cn = language == "cn"
    label = {"glm-5.3": "GLM-5.3", "deepseek-v4.1-flash": "DeepSeek V4.1 Flash", "kimi-k3-2": "Kimi kimi-k3-2"}[model]
    title = f"{label}：任务 × 指标矩阵" if cn else f"{label}: task × indicator matrix"
    is_g = tasks == ("G",)
    subtitle = (("G为迁移类比：CANN侧与CUDA侧（ROCm/HIP），不将CUDA侧解释为普通CUDA事实。" if cn else
                 "G is a migration analogy: CANN-side and CUDA-side (ROCm/HIP); the CUDA-side is not ordinary CUDA evidence.") if is_g else
                ("每题两行：CANN在上、CUDA在下；G单独输出。" if cn else
                 "Two rows per task: CANN above CUDA; G is rendered separately."))
    x0, y0, rh = (220 if is_g else 133), 104, 23
    canvas_width = x0 + 862
    widths = [72] * 10 + [118]
    h = y0 + len(tasks) * 51 + 145
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{canvas_width}" height="{h}" viewBox="0 0 {canvas_width} {h}" role="img">',
             '<rect width="100%" height="100%" fill="white"/>',
             '<g font-family="Arial, PingFang SC, sans-serif">',
             f'<text x="20" y="29" font-size="23" font-weight="700" fill="#263945">{_esc(title)}</text>',
             f'<text x="20" y="54" font-size="14" fill="#263945">{_esc(subtitle)}</text>',
             f'<text x="35" y="85" font-size="14" fill="#263945">{"任务" if cn else "Task"}</text>',
             f'<text x="93" y="85" font-size="14" fill="#263945">{"生态" if cn else "Side"}</text>']
    x = x0
    for i, width in enumerate(widths, 1):
        parts.append(f'<text x="{x+width/2}" y="85" font-size="15" font-weight="700" text-anchor="middle" fill="#263945">M{i}</text>')
        x += width
    ix = {(r["model"], r["task"], r["ecosystem"]): r for r in rows}
    for k, task in enumerate(tasks):
        y = y0 + k * (rh * 2 + 5)
        parts.append(f'<text x="32" y="{y+28}" font-size="15" font-weight="700" text-anchor="middle" fill="#263945">{task}</text>')
        for side_index, ecosystem in enumerate(("cann", "cuda")):
            row = ix[(model, task, ecosystem)]
            yy = y + side_index * rh
            if is_g:
                side = ("CANN侧" if cn else "CANN-side") if ecosystem == "cann" else ("CUDA侧（ROCm/HIP）" if cn else "CUDA-side (ROCm/HIP)")
            else:
                side = "CANN" if ecosystem == "cann" else "CUDA"
            parts.append(f'<text x="{(130 if is_g else 92)}" y="{yy+16}" font-size="11" text-anchor="middle" fill="{SIDE_COLORS[ecosystem]}">{side}</text>')
            x = x0
            metrics = row["metrics"]
            if isinstance(metrics, list):
                metrics = {m["id"]: m for m in metrics}
            for metric_id, width in zip(METRICS, widths):
                parts.append(_cell(metrics[metric_id], metric_id, x, yy, width, rh))
                x += width
    footer = y0 + len(tasks) * 51 + 16
    parts.append(f'<text x="20" y="{footer}" font-size="13" fill="#263945">{_esc("数字为确定分数；N/A不适用，B无评价对象，NR待复核，U证据不足，P尚未评价。" if cn else "Numbers: scores; N/A: not applicable; B: blocked; NR: needs review; U: unscorable; P: not assessed.")}</text>')
    parts.append(f'<text x="20" y="{footer+22}" font-size="13" fill="#263945">M1–M10: 1–5; M11: 0–100. {_esc("G另列。" if cn else "G is separate.")}</text>')
    scoped_rows = [r for r in rows if r.get("model") == model and r.get("task") in tasks]
    denominators = {}
    status_counts = {}
    for ecosystem in ("cann", "cuda"):
        erows = [r for r in scoped_rows if r.get("ecosystem") == ecosystem]
        denominators[ecosystem] = []
        status_counts[ecosystem] = []
        for metric_id in METRICS:
            values = [(r["metrics"] if isinstance(r["metrics"], dict) else {m["id"]: m for m in r["metrics"]})[metric_id] for r in erows]
            denominators[ecosystem].append(f"{metric_id}={sum(v.get('status') == 'scored' for v in values)}")
            counts = Counter(v.get("status", "unknown") for v in values if v.get("status") != "scored")
            if counts:
                status_counts[ecosystem].append(f"{metric_id}:" + ",".join(f"{k}×{v}" for k, v in sorted(counts.items())))
    scope_label = "有效分母" if cn else "Scored denominators"
    for line, ecosystem in enumerate(("cann", "cuda")):
        side = "CANN" if ecosystem == "cann" else "CUDA"
        parts.append(f'<text x="20" y="{footer+46+line*17}" font-size="10" fill="{SIDE_COLORS[ecosystem]}">{_esc(scope_label+" "+side+"：" if cn else scope_label+" "+side+": ")}{_esc("; ".join(denominators[ecosystem]))}</text>')
    parts.append(f'<text x="20" y="{footer+88}" font-size="11" fill="#596474">{_esc("逐项状态和完整原因见配套状态表；颜色仅帮助阅读分档。" if cn else "See companion status table for all statuses/reasons; colors aid reading only.")}</text>')
    parts.append("</g></svg>")
    return "".join(parts)


def render_staged(data, out_dir: Path, languages=("cn", "en")):
    """Render candidate SVGs only; caller supplies a gate-validated object."""
    out_dir.mkdir(parents=True, exist_ok=True)
    rows = data["rows"]
    coverage = data.get("metric_coverage", {})
    outputs = []
    for model in MODELS:
        key = {"glm-5.3": "glm", "deepseek-v4.1-flash": "deepseek", "kimi-k3-2": "kimi"}[model]
        for language in languages:
            main_name = f"matrix-{key}-{language}.svg"
            (out_dir / main_name).write_text(_svg(model, rows, MAIN_TASKS, language, coverage), encoding="utf-8")
            outputs.append(out_dir / main_name)
            g_name = f"matrix-{key}-g-{language}.svg"
            (out_dir / g_name).write_text(_svg(model, rows, ("G",), language, coverage), encoding="utf-8")
            outputs.append(out_dir / g_name)
            for scope, scope_tasks in (("main", MAIN_TASKS), ("g", ("G",))):
                status_name = f"matrix-{key}-{scope}-{language}-status.html"
                (out_dir / status_name).write_text(_status_html(model, rows, scope_tasks, language), encoding="utf-8")
                outputs.append(out_dir / status_name)
    return outputs


def _status_html(model, rows, tasks, language):
    """Readable companion for full reasons; SVG titles remain concise."""
    cn = language == "cn"
    label = {"glm-5.3": "GLM-5.3", "deepseek-v4.1-flash": "DeepSeek V4.1 Flash", "kimi-k3-2": "Kimi kimi-k3-2"}[model]
    title = f"{label}：状态与原因" if cn else f"{label}: statuses and reasons"
    parts = [f'<!doctype html><html lang="{"zh-CN" if cn else "en"}"><meta charset="utf-8"><title>{_esc(title)}</title>',
             '<style>body{font:14px/1.6 system-ui,sans-serif;color:#263945;max-width:1400px;margin:24px auto;padding:0 20px}table{border-collapse:collapse;width:100%}th,td{border:1px solid #d5dfe0;padding:7px;text-align:left;vertical-align:top}th{background:#edf3f2}td.reason{white-space:pre-wrap;overflow-wrap:anywhere;min-width:360px}</style>',
             f"<h1>{_esc(title)}</h1>",
             f"<p>{_esc('G为迁移类比，CUDA侧采用ROCm/HIP语境。' if cn and tasks == ('G',) else 'G is a migration analogy; CUDA-side entries use ROCm/HIP context.' if tasks == ('G',) else '主比较任务 A–F/H–Z。' if cn else 'Main comparison tasks: A–F/H–Z.')}</p>",
             '<table><thead><tr><th>Task</th><th>Side</th><th>Metric</th><th>Status</th><th>Score</th><th>Reason</th></tr></thead><tbody>']
    ix = {(r["model"], r["task"], r["ecosystem"]): r for r in rows}
    for task in tasks:
        for ecosystem in ("cann", "cuda"):
            row = ix[(model, task, ecosystem)]
            metrics = row["metrics"] if isinstance(row["metrics"], dict) else {m["id"]: m for m in row["metrics"]}
            for metric_id in METRICS:
                metric = metrics[metric_id]
                reason = metric.get("reason") or metric.get("missing_reason") or ""
                side = ("CANN侧" if cn else "CANN-side") if ecosystem == "cann" else (("CUDA侧（ROCm/HIP）" if cn else "CUDA-side (ROCm/HIP)") if task == "G" else ("CUDA" if cn else "CUDA"))
                parts.append(f"<tr><td>{task}</td><td>{_esc(side)}</td><td>{metric_id}</td><td>{_esc(metric.get('status','unknown'))}</td><td>{_esc(metric.get('score',''))}</td><td class=\"reason\">{_esc(reason)}</td></tr>")
    parts.append('</tbody></table></html>')
    return "".join(parts)


def render_path(input_path: Path, out_dir: Path):
    return render_staged(load_complete(input_path), out_dir)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True, help="new staging directory; never the working figures directory")
    args = parser.parse_args(argv)
    outputs = render_path(args.input, args.out)
    print(f"rendered {len(outputs)} staged SVGs under {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
