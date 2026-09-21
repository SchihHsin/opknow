#!/usr/bin/env python3
"""Validate point-assessment structure and M2's equal-document mean.

This does not verify quotation authenticity, technical meaning, or M11's formula.
Observation/channel-state objects retain facts and unknowns; their meaning is not
validated here and they must not be used to introduce new score intervals.
No network, model calls, or assessment-file writes are performed.
"""

import argparse
import json
import math
from pathlib import Path
import re
import sys


RULE_VERSION = "point-rubric-20260922-v1"
METRICS = tuple(f"M{i}" for i in range(1, 12))
STATUSES = frozenset({
    "scored", "not_applicable", "blocked", "needs_review", "unscorable",
    "not_assessed",
})
FORBIDDEN_FIELDS = frozenset({
    "lower", "upper", "candidate_score", "display_interval",
})
METRIC_FIELDS = frozenset({
    "status", "score", "reason", "evidence", "event_refs", "derived_from",
    "documents", "observations",
})


class AssessmentInputError(ValueError):
    """Malformed JSON, including duplicate keys and non-finite constants."""


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise AssessmentInputError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _reject_constant(value):
    raise AssessmentInputError(f"non-finite JSON constant: {value}")


def load_assessment(path):
    """Read JSON without silently accepting duplicate keys or NaN/Infinity."""
    with Path(path).open(encoding="utf-8") as stream:
        return json.load(
            stream, object_pairs_hook=_unique_object,
            parse_constant=_reject_constant,
        )


def validate_assessment(data):
    """Return structural errors; an empty list means these checks passed."""
    errors = []

    def fail(path, message):
        errors.append(f"{path}: {message}")

    def nonempty(value):
        return isinstance(value, str) and bool(value.strip())

    def fields(obj, allowed, required, path):
        for key in sorted(set(obj) - set(allowed), key=str):
            if key in FORBIDDEN_FIELDS:
                fail(path, f"interval/candidate field {key!r} is forbidden")
            else:
                fail(path, f"unexpected field {key!r}")
        for key in sorted(set(required) - set(obj)):
            fail(path, f"missing required field {key!r}")

    def object_field(obj, name, path):
        if name in obj and not isinstance(obj[name], dict):
            fail(f"{path}.{name}", "must be an object")

    def score_check(value, low, high, integer, path):
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            fail(path, "must be a finite number")
            return False
        try:
            finite = math.isfinite(value)
        except OverflowError:
            finite = False
        if not finite:
            fail(path, "must be a finite number")
            return False
        if not low <= value <= high:
            fail(path, f"must be between {low} and {high}")
            return False
        if integer and value != int(value):
            fail(path, "must be an integer")
            return False
        return True

    def status_check(obj, path):
        status = obj.get("status")
        if not isinstance(status, str) or status not in STATUSES:
            fail(path + ".status", "must be an allowed single-value status")
        if status != "scored" and obj.get("score") is not None:
            fail(path + ".score", "must be null when status is not scored")
        return status

    def evidence_check(value, path):
        if not isinstance(value, list):
            fail(path, "must be an array")
            return False
        valid = bool(value)
        for index, item in enumerate(value):
            item_path = f"{path}[{index}]"
            if not isinstance(item, dict):
                fail(item_path, "must be an object")
                valid = False
                continue
            fields(item, {"event_id", "quote"}, {"event_id", "quote"}, item_path)
            for key in ("event_id", "quote"):
                if not nonempty(item.get(key)):
                    fail(f"{item_path}.{key}", "must be a non-empty string")
                    valid = False
        return valid

    def references_check(value, path, derived=False):
        if not isinstance(value, list):
            fail(path, "must be an array")
            return False
        valid = bool(value)
        for index, item in enumerate(value):
            if not nonempty(item):
                fail(f"{path}[{index}]", "must be a non-empty string")
                valid = False
            elif derived and item not in METRICS[:8]:
                fail(f"{path}[{index}]", "must name one of M1-M8")
                valid = False
        if derived and all(isinstance(x, str) for x in value):
            if len(value) != len(set(value)):
                fail(path, "must not contain duplicate metric names")
                valid = False
        return valid

    if not isinstance(data, dict):
        fail("$", "must be an object")
        return errors
    top_fields = {"rule_version", "run_id", "process_sha256", "metrics"}
    fields(data, top_fields | {"observations", "channel_states"}, top_fields, "$")
    object_field(data, "observations", "$")
    object_field(data, "channel_states", "$")
    if data.get("rule_version") != RULE_VERSION:
        fail("$.rule_version", f"must equal {RULE_VERSION!r}")
    if not nonempty(data.get("run_id")):
        fail("$.run_id", "must be a non-empty string")
    digest = data.get("process_sha256")
    if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-fA-F]{64}", digest):
        fail("$.process_sha256", "must be a 64-character SHA-256 hex digest")
    metrics = data.get("metrics")
    if not isinstance(metrics, dict):
        fail("$.metrics", "must be an object keyed by M1-M11")
        return errors
    fields(metrics, METRICS, METRICS, "$.metrics")
    for name in METRICS:
        if name not in metrics:
            continue
        metric = metrics[name]
        path = f"$.metrics.{name}"
        if not isinstance(metric, dict):
            fail(path, "must be an object")
            continue
        allowed_fields = METRIC_FIELDS | ({"missing_inputs"} if name == "M11" else set())
        fields(metric, allowed_fields, {"status", "score", "reason"}, path)
        object_field(metric, "observations", path)
        if name == "M11" and "missing_inputs" in metric:
            references_check(metric["missing_inputs"], path + ".missing_inputs", derived=True)
        status = status_check(metric, path)
        if not nonempty(metric.get("reason")):
            fail(path + ".reason", "must be a non-empty string")
        valid_score = False
        if status == "scored":
            valid_score = score_check(
                metric.get("score"), 0 if name == "M11" else 1,
                100 if name == "M11" else 5, name not in {"M2", "M11"},
                path + ".score",
            )
        evidence = event_refs = derived_from = False
        if "evidence" in metric:
            evidence = evidence_check(metric["evidence"], path + ".evidence")
        if "event_refs" in metric:
            event_refs = references_check(metric["event_refs"], path + ".event_refs")
        if "derived_from" in metric:
            derived_from = references_check(
                metric["derived_from"], path + ".derived_from", derived=True,
            )
        if status == "scored" and not (
            evidence or (name == "M8" and event_refs)
            or (name == "M11" and derived_from)
        ):
            fail(path, "scored metric needs evidence (M8: event_refs; M11: derived_from also allowed)")

        if name == "M2" and status == "scored" and "documents" not in metric:
            fail(path + ".documents", "required for scored M2")
        if "documents" not in metric:
            continue
        documents = metric["documents"]
        if not isinstance(documents, list):
            fail(path + ".documents", "must be an array")
            continue
        if name == "M2" and status == "scored" and not documents:
            fail(path + ".documents", "scored M2 requires at least one document")
        document_scores = []
        document_ids = set()
        for index, document in enumerate(documents):
            doc_path = f"{path}.documents[{index}]"
            if not isinstance(document, dict):
                fail(doc_path, "must be an object")
                continue
            fields(document, {"id", "status", "score", "observations"}, {"id", "status", "score"}, doc_path)
            object_field(document, "observations", doc_path)
            doc_id = document.get("id")
            if not nonempty(doc_id):
                fail(doc_path + ".id", "must be a non-empty string")
            elif doc_id in document_ids:
                fail(doc_path + ".id", "duplicate independent-document id")
            else:
                document_ids.add(doc_id)
            doc_status = status_check(document, doc_path)
            if doc_status == "scored":
                if score_check(document.get("score"), 1, 5, True, doc_path + ".score"):
                    document_scores.append(document["score"])
            elif name == "M2" and status == "scored":
                fail(doc_path, "all documents must be scored before M2 can be averaged")
        if name == "M2" and status == "scored" and valid_score and documents:
            if len(document_scores) == len(documents):
                mean = sum(document_scores) / len(documents)
                if not math.isclose(metric["score"], mean, rel_tol=0.0, abs_tol=1e-9):
                    fail(path + ".score", f"must equal all-document mean {mean!r}")
    return errors


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("files", nargs="+", type=Path, help="assessment JSON files")
    args = parser.parse_args(argv)
    failed = False
    for path in args.files:
        try:
            errors = validate_assessment(load_assessment(path))
        except (OSError, ValueError) as exc:
            errors = [str(exc)]
        if errors:
            failed = True
            print(f"FAIL {path}", file=sys.stderr)
            for error in errors:
                print(f"  {error}", file=sys.stderr)
        else:
            print(f"PASS {path} (structure and M2 mean only)")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
