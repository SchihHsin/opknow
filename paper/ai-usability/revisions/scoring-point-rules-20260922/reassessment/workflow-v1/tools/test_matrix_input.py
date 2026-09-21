import json, tempfile, unittest
from pathlib import Path
import shutil
import build_matrix_input
from test_workflow import SMOKE
from unittest.mock import patch
from matrix_input import MatrixInputError, load_complete

class MatrixInputTests(unittest.TestCase):
    def test_incomplete_universe_is_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "results.json"
            p.write_text(json.dumps({"rows": [], "consolidation_gate": {"formal": True, "universe_size": 155, "validated_receipts": 155}}))
            with self.assertRaises(MatrixInputError): load_complete(p)

    def test_missing_null_coverage_is_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "results.json"
            p.write_text(json.dumps({"rows": [{}] * 156, "consolidation_gate": {"formal": True, "universe_size": 156, "validated_receipts": 156, "pair_key": ["model", "task", "ecosystem"], "main_task_count": 25, "migration_analogy_tasks": ["G"]}, "metric_coverage": {}}))
            with self.assertRaises(MatrixInputError): load_complete(p)

    def test_duplicate_rows_and_invalid_scores_are_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "results.json"
            gate = {"formal": True, "universe_size": 156, "validated_receipts": 156, "pair_key": ["model", "task", "ecosystem"], "main_task_count": 25, "migration_analogy_tasks": ["G"], "expected_pairs": [["m", "A", "cann"]]}
            rows = [{"run_id": "same", "model": "m", "task": "A", "ecosystem": "cann", "metrics": {f"M{i}": {"status": "scored", "score": 99} for i in range(1, 12)}}] * 156
            p.write_text(json.dumps({"rows": rows, "consolidation_gate": gate, "metric_coverage": {}}))
            with self.assertRaises(MatrixInputError): load_complete(p)

    def test_failed_validation_does_not_overwrite_existing_output(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "results.json"; p.write_text("sentinel")
            bad = Path(d) / "bad.json"; bad.write_text(json.dumps({"rows": [], "consolidation_gate": {}}))
            with self.assertRaises(MatrixInputError): load_complete(bad)
            self.assertEqual(p.read_text(), "sentinel")

    def test_incomplete_workflow_is_rejected_before_formal_output(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d) / "workflow"; run = root / "batch" / "synthetic-run-1"
            run.parent.mkdir(parents=True); shutil.copytree(SMOKE, run)
            manifest = Path(d) / "manifest.json"
            manifest.write_text(json.dumps({"records": [{"run_id": "synthetic-run-1"}]}))
            out = Path(d) / "out"; out.mkdir(); (out / "results.json").write_text("sentinel")
            with self.assertRaises(Exception): build_matrix_input.build(root, manifest, out)
            self.assertEqual((out / "results.json").read_text(), "sentinel")

    def test_success_path_uses_run_id_manifest_shape(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d) / "workflow"; manifest = Path(d) / "manifest.json"; out = Path(d) / "out"
            records = []
            models = ["glm-5_3", "deepseek-v4_1-flash", "kimi-k3-2"]
            rows = []
            for model in models:
                for task in [chr(i) for i in range(65, 91)]:
                    for eco in ("cann", "cuda"):
                        rid = f"{task}-{eco}-{model}-standard-20260921T000000"
                        records.append({"run_id": rid, "packet_sha256": "p", "process_sha256": "q"})
                        rows.append({"run_id": rid, "model": model.replace("glm-5_3", "glm-5.3").replace("deepseek-v4_1-flash", "deepseek-v4.1-flash"), "task": task, "ecosystem": eco, "metrics": {**{f"M{i}": {"status": "scored", "score": 3} for i in range(1, 11)}, "M11": {"status": "scored", "score": 50.0}}})
            manifest.write_text(json.dumps({"records": records}))
            def fake_consolidate(_root, _manifest, temp):
                temp.mkdir(parents=True, exist_ok=True)
                (temp / "results.json").write_text(json.dumps({"rows": rows}))
            with patch.object(build_matrix_input.consolidate, "consolidate", fake_consolidate):
                build_matrix_input.build(root, manifest, out)
            result = json.loads((out / "results.json").read_text())
            self.assertEqual(len(result["rows"]), 156)
            for label, mutate in {
                "identity": lambda x: x["rows"][0].update({"run_id": x["rows"][0]["run_id"].replace("A-cann", "Z-cuda")}),
                "score": lambda x: x["rows"][0]["metrics"].update({"M1": {"status": "scored", "score": 2.5}}),
                "coverage": lambda x: x["metric_coverage"]["M1"].update({"denominator_scored": 0}),
                "migration": lambda x: x["consolidation_gate"].update({"migration_analogy_tasks": []}),
            }.items():
                bad = Path(d) / f"{label}.json"; candidate = json.loads(json.dumps(result)); mutate(candidate); bad.write_text(json.dumps(candidate))
                with self.assertRaises(Exception): load_complete(bad)
            sentinel = out / "results.json"; sentinel.write_text("sentinel")
            def invalid_consolidate(_root, _manifest, temp):
                temp.mkdir(parents=True, exist_ok=True); broken = json.loads(json.dumps(rows)); broken[0]["metrics"]["M1"]["score"] = 2.5; (temp / "results.json").write_text(json.dumps({"rows": broken}))
            with patch.object(build_matrix_input.consolidate, "consolidate", invalid_consolidate):
                with self.assertRaises(Exception): build_matrix_input.build(root, manifest, out)
            self.assertEqual(sentinel.read_text(), "sentinel")
