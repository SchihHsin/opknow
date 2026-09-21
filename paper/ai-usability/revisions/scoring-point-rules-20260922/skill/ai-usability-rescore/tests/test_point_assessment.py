"""Boundary tests for the structure validator; no assessed data is changed."""

import copy
import json
import math
from pathlib import Path
import tempfile
import unittest

from validate_point_assessment import (
    AssessmentInputError, RULE_VERSION, load_assessment, validate_assessment,
)


def complete_example():
    metrics = {
        f"M{i}": {
            "status": "scored", "score": 4, "reason": "Recorded evidence supports this grade.",
            "evidence": [{"event_id": "event-1", "quote": "Example recorded text."}],
        }
        for i in range(1, 12)
    }
    metrics["M2"].update(score=4.5, documents=[
        {"id": "document-1", "status": "scored", "score": 4},
        {"id": "document-2", "status": "scored", "score": 5},
    ])
    metrics["M8"].pop("evidence")
    metrics["M8"]["event_refs"] = ["search-1", "fetch-1"]
    metrics["M11"].pop("evidence")
    metrics["M11"].update(score=75.0, derived_from=[f"M{i}" for i in range(1, 9)])
    return {
        "rule_version": RULE_VERSION, "run_id": "synthetic-structure-example",
        "process_sha256": "0" * 64, "metrics": metrics,
    }


class PointAssessmentTests(unittest.TestCase):
    def setUp(self):
        self.data = complete_example()

    def assert_invalid(self, data=None, contains=None):
        errors = validate_assessment(self.data if data is None else data)
        self.assertTrue(errors)
        if contains:
            self.assertTrue(any(contains in error for error in errors), errors)

    def load_text(self, text):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "example.json"
            path.write_text(text, encoding="utf-8")
            return load_assessment(path)

    def test_complete_example_passes(self):
        self.assertEqual(validate_assessment(self.data), [])
        self.assertEqual(validate_assessment(self.load_text(json.dumps(self.data))), [])

    def test_interval_fields_and_bounded_status_rejected(self):
        for field in ("lower", "upper", "candidate_score", "display_interval"):
            with self.subTest(field=field):
                data = copy.deepcopy(self.data)
                data["metrics"]["M2"][field] = 4
                self.assert_invalid(data, "forbidden")
        self.data["metrics"]["M2"]["status"] = "bounded"
        self.assert_invalid(contains="status")

    def test_all_non_scored_statuses_require_null(self):
        for status in ("not_applicable", "blocked", "needs_review", "unscorable", "not_assessed"):
            with self.subTest(status=status):
                data = copy.deepcopy(self.data)
                data["metrics"]["M3"] = {"status": status, "score": None, "reason": "No usable evidence."}
                self.assertEqual(validate_assessment(data), [])
                data["metrics"]["M3"]["score"] = 3
                self.assert_invalid(data, "must be null")

    def test_missing_m11_rejected(self):
        del self.data["metrics"]["M11"]
        self.assert_invalid(contains="M11")

    def test_duplicate_metric_json_rejected(self):
        text = json.dumps(self.data)
        text = text.replace('"M1": {', '"M1": {}, "M1": {', 1)
        with self.assertRaisesRegex(AssessmentInputError, "duplicate JSON key: M1"):
            self.load_text(text)

    def test_list_metrics_and_unknown_metric_rejected(self):
        data = copy.deepcopy(self.data)
        data["metrics"] = list(data["metrics"].values())
        self.assert_invalid(data, "must be an object keyed")
        self.data["metrics"]["M12"] = {}
        self.assert_invalid(contains="unexpected field")

    def test_m2_unknown_document_cannot_be_ignored(self):
        metric = self.data["metrics"]["M2"]
        metric["documents"][1].update(status="needs_review", score=None)
        metric["score"] = 4
        self.assert_invalid(contains="all documents must be scored")

    def test_m2_mean_must_use_all_documents(self):
        self.assertEqual(validate_assessment(self.data), [])
        self.data["metrics"]["M2"]["score"] = 4
        self.assert_invalid(contains="all-document mean 4.5")

    def test_m2_documents_required_integer_unique(self):
        for documents in ([], None, [
            {"id": "d", "status": "scored", "score": 4.5},
        ], [
            {"id": "d", "status": "scored", "score": 4},
            {"id": "d", "status": "scored", "score": 5},
        ]):
            with self.subTest(documents=documents):
                data = copy.deepcopy(self.data)
                data["metrics"]["M2"]["documents"] = documents
                self.assert_invalid(data)
        del self.data["metrics"]["M2"]["documents"]
        self.assert_invalid(contains="required for scored M2")

    def test_nonfinite_numeric_and_boolean_scores_rejected(self):
        for value in (math.nan, math.inf, -math.inf, True, 10 ** 1000):
            with self.subTest(value=str(value)[:20]):
                data = copy.deepcopy(self.data)
                data["metrics"]["M11"]["score"] = value
                self.assert_invalid(data, "finite number")

    def test_nonfinite_json_tokens_rejected(self):
        for token in ("NaN", "Infinity", "-Infinity"):
            with self.subTest(token=token):
                with self.assertRaisesRegex(AssessmentInputError, "non-finite"):
                    self.load_text('{"score": ' + token + '}')
        data = self.load_text(json.dumps(self.data).replace('"score": 75.0', '"score": 1e999'))
        self.assert_invalid(data, "finite number")

    def test_score_ranges_and_integer_metrics(self):
        for name, value in (("M1", 3.5), ("M3", 0), ("M10", 6), ("M11", 101), ("M11", -1)):
            with self.subTest(name=name, value=value):
                data = copy.deepcopy(self.data)
                data["metrics"][name]["score"] = value
                self.assert_invalid(data)

    def test_reason_and_scored_evidence_required(self):
        for field, value in (("reason", "  "), ("evidence", []), ("evidence", [{"event_id": "e", "quote": ""}])):
            with self.subTest(field=field, value=value):
                data = copy.deepcopy(self.data)
                data["metrics"]["M1"][field] = value
                self.assert_invalid(data)
        self.data["metrics"]["M1"].pop("evidence")
        self.data["metrics"]["M1"]["event_refs"] = ["event-1"]
        self.assert_invalid(contains="scored metric needs evidence")

    def test_m8_m11_alternatives_must_be_nonempty(self):
        for name, field in (("M8", "event_refs"), ("M11", "derived_from")):
            with self.subTest(name=name):
                data = copy.deepcopy(self.data)
                data["metrics"][name][field] = []
                self.assert_invalid(data, "scored metric needs evidence")

    def test_m11_reference_names_valid_and_unique(self):
        for refs in (["M9"], ["M1", "M1"], [None]):
            with self.subTest(refs=refs):
                data = copy.deepcopy(self.data)
                data["metrics"]["M11"]["derived_from"] = refs
                self.assert_invalid(data)

    def test_provenance_and_required_score_fields(self):
        for field, value in (("rule_version", "old"), ("run_id", ""), ("process_sha256", "short")):
            with self.subTest(field=field):
                data = copy.deepcopy(self.data)
                data[field] = value
                self.assert_invalid(data)
        self.data["metrics"]["M3"] = {"status": "blocked", "reason": "No body."}
        self.assert_invalid(contains="missing required field 'score'")

    def test_optional_observations_and_missing_inputs_pass(self):
        self.data["observations"] = {"tool_provider": "unknown"}
        self.data["channel_states"] = {"official": {"status": "unknown"}}
        self.data["metrics"]["M2"]["observations"] = {"ownership": "official", "reference_status": "unknown"}
        self.data["metrics"]["M2"]["documents"][0]["observations"] = {
            "representation": "direct_body", "independent_completeness_check": "unknown",
            "defects": ["truncated"], "event_id": "fetch-1",
        }
        self.data["metrics"]["M11"]["missing_inputs"] = []
        self.assertEqual(validate_assessment(self.data), [])
        self.data["metrics"]["M11"] = {
            "status": "needs_review", "score": None,
            "reason": "Input requires review.", "missing_inputs": ["M7"],
        }
        self.assertEqual(validate_assessment(self.data), [])

    def test_optional_observation_fields_require_objects(self):
        for location in ("top_observations", "channel_states", "metric", "document"):
            for value in (None, [], "unknown", 1):
                with self.subTest(location=location, value=value):
                    data = copy.deepcopy(self.data)
                    if location == "top_observations":
                        data["observations"] = value
                    elif location == "channel_states":
                        data["channel_states"] = value
                    elif location == "metric":
                        data["metrics"]["M2"]["observations"] = value
                    else:
                        data["metrics"]["M2"]["documents"][0]["observations"] = value
                    self.assert_invalid(data, "must be an object")

    def test_missing_inputs_m11_only_valid_names_no_duplicates(self):
        for value in (None, "M7", ["M9"], ["M7", "M7"], [None]):
            with self.subTest(value=value):
                data = copy.deepcopy(self.data)
                data["metrics"]["M11"]["missing_inputs"] = value
                self.assert_invalid(data)
        self.data["metrics"]["M2"]["missing_inputs"] = []
        self.assert_invalid(contains="unexpected field 'missing_inputs'")


if __name__ == "__main__":
    unittest.main()
