"""Small regression checks for the workflow gate (run from repository root)."""
import json, shutil, tempfile, unittest
from pathlib import Path
import consolidate
import progress

HERE = Path(__file__).resolve()
SMOKE = HERE.parents[3] / "skill-validation-20260922" / "cli-smoke"

class WorkflowGateTests(unittest.TestCase):
    def fixture(self):
        d = Path(tempfile.mkdtemp()) / "run"; shutil.copytree(SMOKE, d)
        review = d / "review.json"; obj = json.loads(review.read_text())
        obj["review_scope"] = "Per-metric review: " + " ".join(f"M{i}" for i in range(1, 12))
        review.write_text(json.dumps(obj))
        idx = json.loads((d / "prepared" / "packet-index.json").read_text())
        ass = json.loads((d / "assessment.json").read_text())
        return d, {"packet_sha256": idx["packet_sha256"], "process_sha256": ass["process_sha256"]}

    def test_positive_and_stale_hash(self):
        d, meta = self.fixture(); consolidate.validate_run("synthetic-run-1", d, meta)
        p = d / "review.json"; obj = json.loads(p.read_text()); obj["assessment_sha256"] = "0" * 64; p.write_text(json.dumps(obj))
        with self.assertRaises(consolidate.GateError): consolidate.validate_run("synthetic-run-1", d, meta)

    def test_gate_false_pair_is_excluded_by_filter(self):
        rows = [{"task":"A", "ecosystem":"cann", "gate_passed":False, "metrics":{"M1":{"status":"scored","score":1}}}, {"task":"A", "ecosystem":"cuda", "gate_passed":False, "metrics":{"M1":{"status":"scored","score":2}}}]
        gated = [r for r in rows if r.get("gate_passed") is True]
        self.assertEqual(consolidate.paired(gated, "M1")["n"], 0)

    def test_progress_stages_and_stale_facts(self):
        d, meta = self.fixture()
        rid = "synthetic-run-1"
        self.assertEqual(progress.status(rid, None), "missing")
        self.assertEqual(progress.status(rid, d), "parent_reviewed")
        (d / "receipt.json").unlink()
        self.assertEqual(progress.status(rid, d), "mechanical_pass")
        saved = (d / "facts.json").read_bytes()
        (d / "facts.json").write_bytes(saved + b"\n")
        self.assertEqual(progress.status(rid, d), "draft")
        (d / "facts.json").write_bytes(saved)
        (d / "check.json").unlink()
        self.assertEqual(progress.status(rid, d), "draft")
        (d / "assessment.json").unlink()
        self.assertEqual(progress.status(rid, d), "prepared")

if __name__ == "__main__": unittest.main()
