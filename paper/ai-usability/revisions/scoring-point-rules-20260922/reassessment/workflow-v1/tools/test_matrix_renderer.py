import json
import tempfile
import unittest
from pathlib import Path

from matrix_renderer import MODELS, _cell, _status_html, render_path

TASKS = tuple(chr(i) for i in range(ord("A"), ord("Z") + 1))


def formal_fixture(path, n=156):
    rows = []
    for model in MODELS:
        wire_model = {"glm-5.3": "glm-5_3", "deepseek-v4.1-flash": "deepseek-v4_1-flash", "kimi-k3-2": "kimi-k3-2"}[model]
        for task in TASKS:
            for ecosystem in ("cann", "cuda"):
                metrics = {f"M{i}": {"status": "scored", "score": 2} for i in range(1, 11)}
                metrics["M11"] = {"status": "scored", "score": 50.0}
                rows.append({
                    "run_id": f"{task}-{ecosystem}-{wire_model}-standard-fixture",
                    "task": task, "ecosystem": ecosystem, "model": model,
                    "metrics": metrics,
                })
    if n != len(rows):
        rows = rows[:n]
    expected = [[r["model"], r["task"], r["ecosystem"]] for r in rows]
    coverage = {f"M{i}": {"denominator_scored": len(rows),
                             "status_counts": {"scored": len(rows)},
                             "null_reasons": []} for i in range(1, 12)}
    data = {"consolidation_gate": {
                "formal": True, "universe_size": 156, "validated_receipts": 156,
                "pair_key": ["model", "task", "ecosystem"], "expected_pairs": expected,
                "main_task_count": 25, "migration_analogy_tasks": ["G"]},
            "rows": rows, "metric_coverage": coverage}
    path.write_text(json.dumps(data), encoding="utf-8")


class MatrixRendererTests(unittest.TestCase):
    def test_formal_fixture_renders_staged_main_and_g_outputs(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            source = root / "results.json"
            formal_fixture(source)
            out = root / "candidate-figures"
            paths = render_path(source, out)
            self.assertEqual(len(paths), 24)
            main = (out / "matrix-glm-cn.svg").read_text()
            migration = (out / "matrix-glm-g-cn.svg").read_text()
            self.assertIn("#F4840C", main)
            self.assertIn("M1=25", main)
            self.assertIn("status=scored", main)
            self.assertNotIn('>G</text>', main)
            self.assertIn('>G</text>', migration)
            self.assertTrue(all(p.parent == out for p in paths))
            self.assertIn("reason=missing ownership", _cell({"status": "unscorable", "score": None, "reason": "missing ownership"}, "M1", 0, 0, 72, 23))
            self.assertIn("2.35", _cell({"status": "scored", "score": 2.34567}, "M2", 0, 0, 72, 23))
            self.assertIn("50.1", _cell({"status": "scored", "score": 50.1234}, "M11", 0, 0, 118, 23))
            raw = json.loads(source.read_text())
            long_reason = "missing evidence " * 30
            raw["rows"][0]["metrics"]["M1"] = {"status": "needs_review", "score": None, "reason": long_reason}
            status_html = _status_html("glm-5.3", raw["rows"], ("A",), "en")
            self.assertIn(long_reason, status_html)
            self.assertIn("needs_review", status_html)

    def test_incomplete_gate_is_rejected_before_any_output(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            source = root / "results.json"
            formal_fixture(source, n=155)
            out = root / "candidate-figures"
            with self.assertRaises(RuntimeError):
                render_path(source, out)
            self.assertFalse(out.exists())


if __name__ == "__main__":
    unittest.main()
