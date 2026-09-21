"""Regression tests for mechanical rescore gates.

The fixture deliberately keeps ownership/relevance classifications explicit;
the tests assert that the program checks those mappings and never invents them.
"""

from __future__ import annotations

import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import rescore  # noqa: E402
from point_math import score_m11  # noqa: E402
from validate_point_assessment import RULE_VERSION  # noqa: E402


class RescoreTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.base = Path(self.tmp.name)
        self.packet_path = self.base / "packet.json"
        self.facts_path = self.base / "facts.json"
        self.assessment_path = self.base / "assessment.json"
        self.report_path = self.base / "check-report.json"
        self.review_path = self.base / "review.json"
        self.receipt_path = self.base / "receipt.json"
        self.packet = self.make_packet()
        self.packet_path.write_text(json.dumps(self.packet, ensure_ascii=False, indent=2), encoding="utf-8")
        self.facts = self.make_facts()
        self.facts_path.write_text(json.dumps(self.facts, ensure_ascii=False, indent=2), encoding="utf-8")
        self.assessment = self.make_assessment()
        self.assessment_path.write_text(json.dumps(self.assessment, ensure_ascii=False, indent=2), encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def make_packet(self):
        search_text = (
            "## 1. [Official guide](https://official.example/doc)\n\n"
            "Official result summary\n\n**URL:** https://official.example/doc\n\n"
            "## 2. [Community guide](https://third.example/post)\n\n"
            "third-party result body\n\n**URL:** https://third.example/post\n"
        )
        return {
            "run_name": "synthetic-run-1", "task_id": "A", "question": "Install the toolkit",
            "metadata": {"run_id": "synthetic-run-1", "process_sha256": "a" * 64},
            "applicability": {"M4": {"applicable": True}, "M9": {"applicable": True}, "M10": {"applicable": True}},
            "prior": [{"event_id": "prior-1", "text": "Prior answer text."}],
            "sources": [
                {"event_id": "search-1", "request_id": "req-search", "role": "search", "url": None, "text": search_text},
                {"event_id": "fetch-1", "request_id": "req-fetch", "role": "fetch", "url": "https://official.example/doc#section", "text": "Official body text: PATH and LD_LIBRARY_PATH."},
            ],
            "final": "Final answer text.", "final_event_ids": ["final-1"],
            "dispatch_events": [
                {"id": "req-search.dispatch", "type": "tool_dispatch", "request_id": "req-search"},
                {"id": "req-fetch.dispatch", "type": "tool_dispatch", "request_id": "req-fetch"},
            ],
        }

    def make_facts(self):
        search_text = self.packet["sources"][0]["text"]
        body = self.packet["sources"][1]["text"]
        return {
            "run_id": "synthetic-run-1", "packet_sha256": "placeholder",
            "question": "Install the toolkit",
            "task_requirements": {"main": ["install"], "secondary": [], "version_relations": []},
            "source_items": [
                {"source_id": "search-event", "event_id": "search-1", "url": None, "ownership": "unknown", "relevant": None, "content_group": "", "evidence": {"event_id": "search-1", "quote": search_text}},
                {"source_id": "official-result", "event_id": "search-1", "url": "https://official.example/doc", "ownership": "official", "relevant": True, "content_group": "official-doc", "query_index": 1, "rank": 1, "evidence": {"event_id": "search-1", "quote": "## 1. [Official guide](https://official.example/doc)\n\nOfficial result summary\n\n**URL:** https://official.example/doc\n\n"}},
                {"source_id": "third-result", "event_id": "search-1", "url": "https://third.example/post", "ownership": "third_party", "relevant": True, "content_group": "community-post", "query_index": 1, "rank": 2, "evidence": {"event_id": "search-1", "quote": "## 2. [Community guide](https://third.example/post)\n\nthird-party result body\n\n**URL:** https://third.example/post\n"}},
                {"source_id": "official-fetch", "event_id": "fetch-1", "url": "https://official.example/doc#section", "ownership": "official", "relevant": True, "content_group": "official-doc", "evidence": {"event_id": "fetch-1", "quote": body}},
            ],
            "fetches": [{"request_url": "https://official.example/doc", "event_id": "fetch-1", "ownership": "official", "target_match": "matched", "representation": "body", "observed_defect": False, "evidence": {"event_id": "fetch-1", "quote": body}}],
            "m1": {"first_query": 1, "first_rank": 1, "first_hit_source_id": "official-result", "decisive_records_verified": True, "budget_exhausted": False},
            "m5": {"possible_counts": [1]},
            "m4": {"missing_relations": [], "conflicts": [], "mode": "direct"},
            "m6": {"checked_event_ids": ["search-1", "fetch-1"], "no_third_party_material": False, "claims": [{"source_id": "third-result", "claim": "The community post describes the install.", "claim_evidence": [{"event_id": "search-1", "quote": "third-party result body"}], "support_evidence": [{"event_id": "fetch-1", "quote": body}], "verdict": "supported", "independent_crosscheck": True}]},
            "m10": {"content_repairs": [], "environment_substitutions": [], "content_check_complete": True},
        }

    def make_assessment(self):
        q = lambda event, quote: {"event_id": event, "quote": quote}
        body = self.packet["sources"][1]["text"]
        metrics = {}
        for i in range(1, 12):
            metrics[f"M{i}"] = {"status": "scored", "score": 4, "reason": "Reviewed fact.", "evidence": [q("fetch-1", body)]}
        metrics["M1"].update(score=5, evidence=[q("search-1", "## 1. [Official guide](https://official.example/doc)")])
        metrics["M2"].update(score=5, documents=[{"id": "fetch-1", "status": "scored", "score": 5}], evidence=[q("fetch-1", body)])
        metrics["M5"].update(score=2, evidence=[q("search-1", "third-party result body")])
        metrics["M6"].update(score=5, evidence=[q("fetch-1", body)])
        metrics["M7"].update(evidence=[q("prior-1", "Prior answer text.")])
        metrics["M9"].update(evidence=[q("final-1", "Final answer text.")])
        metrics["M10"].update(evidence=[q("final-1", "Final answer text.")])
        metrics["M8"].pop("evidence"); metrics["M8"]["event_refs"] = ["search-1", "fetch-1"]; metrics["M8"]["score"] = 5
        metrics["M11"].pop("evidence")
        metrics["M11"]["derived_from"] = [f"M{i}" for i in range(1, 9)]
        metrics["M11"]["score"] = score_m11(metrics)["score"]
        return {"rule_version": RULE_VERSION, "run_id": "synthetic-run-1", "process_sha256": "a" * 64, "metrics": metrics}

    def write_facts(self, facts=None):
        self.facts = copy.deepcopy(self.facts if facts is None else facts)
        self.facts["packet_sha256"] = rescore.sha256_file(self.packet_path)
        self.facts_path.write_text(json.dumps(self.facts, ensure_ascii=False, indent=2), encoding="utf-8")

    def write_assessment(self, assessment=None):
        self.assessment = copy.deepcopy(self.assessment if assessment is None else assessment)
        self.assessment_path.write_text(json.dumps(self.assessment, ensure_ascii=False, indent=2), encoding="utf-8")

    def run_check(self):
        self.write_facts()
        self.write_assessment()
        return rescore.check_command(self.packet_path, self.assessment_path, self.facts_path, self.report_path), json.loads(self.report_path.read_text())

    def test_valid_positive_and_prepare_unknown_template(self):
        out = self.base / "prepared"
        self.assertEqual(rescore.prepare(self.packet_path, out), out / "facts.json")
        prepared = json.loads((out / "facts.json").read_text())
        self.assertTrue(prepared["fetches"])
        for row in prepared["source_items"] + prepared["fetches"]:
            self.assertTrue(rescore.quote_exists(rescore.event_index(self.packet), row["evidence"]))
        self.assertTrue(all(x["ownership"] == "unknown" for x in prepared["fetches"]))
        self.write_facts(); self.write_assessment()
        self.assertEqual(rescore.check_command(self.packet_path, self.assessment_path, self.facts_path, self.report_path), 0)
        self.assertTrue(json.loads(self.report_path.read_text())["mechanical_pass"])

    def test_quote_requires_existing_exact_substring(self):
        with self.assertRaises(rescore.GateError): rescore.exact_quote(rescore.event_index(self.packet), "fetch-1", "fabricated")

    def test_empty_main_requirements_fail(self):
        facts = copy.deepcopy(self.facts); facts["task_requirements"]["main"] = []
        self.write_facts(facts); code, report = self.run_check()
        self.assertNotEqual(code, 0); self.assertTrue(any(x["code"] == "facts.requirements.main" for x in report["issues"]))

    def test_scored_final_metrics_require_final_evidence(self):
        for name in ("M9", "M10"):
            assessment = copy.deepcopy(self.assessment); assessment["metrics"][name]["evidence"] = [{"event_id": "fetch-1", "quote": "Official body text: PATH and LD_LIBRARY_PATH."}]
            self.write_assessment(assessment); code, report = self.run_check()
            self.assertNotEqual(code, 0); self.assertTrue(any(x["code"] == f"{name.lower()}.final_evidence" for x in report["issues"]))

    def test_scored_m7_requires_prior_evidence(self):
        assessment = copy.deepcopy(self.assessment); assessment["metrics"]["M7"]["evidence"] = [{"event_id": "fetch-1", "quote": "Official body text: PATH and LD_LIBRARY_PATH."}]
        self.write_assessment(assessment); code, report = self.run_check()
        self.assertNotEqual(code, 0); self.assertTrue(any(x["code"] == "m7.prior_evidence" for x in report["issues"]))

    def test_not_applicable_metrics_are_exempt(self):
        packet = copy.deepcopy(self.packet); packet["applicability"]["M9"] = {"applicable": False}; packet["applicability"]["M10"] = {"applicable": False}
        self.packet_path.write_text(json.dumps(packet, ensure_ascii=False, indent=2), encoding="utf-8")
        assessment = copy.deepcopy(self.assessment)
        for name in ("M9", "M10"):
            assessment["metrics"][name] = {"status": "not_applicable", "score": None, "reason": "Packet applicability", "evidence": []}
        self.write_assessment(assessment); code, report = self.run_check()
        self.assertEqual(code, 0, report)

    def test_m6_claim_and_support_cannot_self_cite_same_event_quote(self):
        facts = copy.deepcopy(self.facts); claim = facts["m6"]["claims"][0]; claim["support_evidence"] = copy.deepcopy(claim["claim_evidence"])
        self.write_facts(facts); code, report = self.run_check()
        self.assertNotEqual(code, 0); self.assertTrue(any(x["code"] == "m6.self_support" for x in report["issues"]))

    def test_m6_claim_evidence_must_be_array(self):
        facts = copy.deepcopy(self.facts); facts["m6"]["claims"][0]["claim_evidence"] = {"event_id": "search-1", "quote": "third-party result body"}
        self.write_facts(facts); code, report = self.run_check()
        self.assertNotEqual(code, 0); self.assertTrue(any(x["code"] == "m6.claim_evidence" for x in report["issues"]))

    def test_m6_malformed_evidence_shapes_fail_without_exception(self):
        for field, value in (("claim_evidence", None), ("support_evidence", None), ("claim_evidence", ["bad"]), ("support_evidence", ["bad"])):
            facts = copy.deepcopy(self.facts); facts["m6"]["claims"][0][field] = value
            self.write_facts(facts); code, report = self.run_check()
            self.assertNotEqual(code, 0); self.assertTrue(any(x["code"] in {"m6.claim_evidence", "m6.support_evidence"} for x in report["issues"]))

    def test_excerpt_cannot_score_as_body_5(self):
        facts = copy.deepcopy(self.facts); facts["fetches"][0]["representation"] = "excerpt"
        self.write_facts(facts); code, report = self.run_check()
        self.assertNotEqual(code, 0); self.assertTrue(any(x["code"] in {"m2.document_score", "m2.mean"} for x in report["issues"]))

    def test_nonexistent_assessment_quote_fails(self):
        assessment = copy.deepcopy(self.assessment); assessment["metrics"]["M1"]["evidence"][0]["quote"] = "not in packet"
        self.write_assessment(assessment); code, report = self.run_check()
        self.assertNotEqual(code, 0); self.assertTrue(any(x["code"] == "quote.missing" for x in report["issues"]))

    def test_official_claim_labeled_third_party_fails(self):
        facts = copy.deepcopy(self.facts); facts["source_items"][2]["url"] = "https://official.example/doc"
        self.write_facts(facts); code, report = self.run_check()
        self.assertNotEqual(code, 0); self.assertTrue(any(x["code"] == "m6.claim_source" for x in report["issues"]))

    def test_unresolved_claim_cannot_receive_three(self):
        facts = copy.deepcopy(self.facts); facts["m6"]["claims"][0]["verdict"] = "unresolved"
        assessment = copy.deepcopy(self.assessment); assessment["metrics"]["M6"]["score"] = 3
        self.write_facts(facts); self.write_assessment(assessment); code, report = self.run_check()
        self.assertNotEqual(code, 0); self.assertTrue(any(x["code"] == "m6.unresolved" for x in report["issues"]))

    def test_missing_version_relation_blocks_four_or_five(self):
        facts = copy.deepcopy(self.facts); facts["m4"]["missing_relations"] = ["toolkit-driver"]
        self.write_facts(facts); code, report = self.run_check()
        self.assertNotEqual(code, 0); self.assertTrue(any(x["code"] == "m4.missing_relations" for x in report["issues"]))

    def test_unknown_fetch_cannot_be_omitted(self):
        packet = copy.deepcopy(self.packet); packet["sources"].append({"event_id": "fetch-unknown", "request_id": "req-unknown", "role": "fetch", "url": "https://unknown.example/doc", "text": "unknown return"}); packet["dispatch_events"].append({"id": "req-unknown.dispatch", "type": "tool_dispatch", "request_id": "req-unknown"})
        self.packet_path.write_text(json.dumps(packet), encoding="utf-8"); code, report = self.run_check()
        self.assertNotEqual(code, 0); self.assertTrue(any(x["code"] == "m2.coverage" for x in report["issues"]))

    def test_dispatch_without_saved_return_fails_closed(self):
        packet = copy.deepcopy(self.packet); packet["dispatch_events"].append({"id": "missing.dispatch", "type": "tool_dispatch", "request_id": "req-missing"})
        self.packet_path.write_text(json.dumps(packet), encoding="utf-8"); code, report = self.run_check()
        self.assertNotEqual(code, 0); self.assertTrue(any(x["code"] == "dispatch.return" for x in report["issues"]))

    def test_missing_or_malformed_facts_writes_failure_report(self):
        self.facts_path.write_text(json.dumps({"m5": []}), encoding="utf-8")
        code = rescore.check_command(self.packet_path, self.assessment_path, self.facts_path, self.report_path)
        self.assertNotEqual(code, 0)
        report = json.loads(self.report_path.read_text())
        self.assertFalse(report["mechanical_pass"])

    def test_m8_uses_actual_dispatch_count(self):
        assessment = copy.deepcopy(self.assessment); assessment["metrics"]["M8"]["score"] = 3
        self.write_assessment(assessment); code, report = self.run_check()
        self.assertNotEqual(code, 0); self.assertTrue(any(x["code"] == "M8.score" for x in report["issues"]))

    def test_old_fetch_return_is_not_used_when_later_return_exists(self):
        packet = copy.deepcopy(self.packet)
        packet["sources"].append({"event_id": "fetch-2", "request_id": "req-fetch-2", "role": "fetch", "url": "https://official.example/doc#later", "text": "error page"})
        packet["dispatch_events"].append({"id": "req-fetch-2.dispatch", "type": "tool_dispatch", "request_id": "req-fetch-2"})
        self.packet_path.write_text(json.dumps(packet), encoding="utf-8")
        code, report = self.run_check()
        self.assertNotEqual(code, 0); self.assertTrue(any(x["code"] in {"m2.coverage", "m2.last_return"} for x in report["issues"]))

    def test_supported_without_support_quote_fails_even_for_nonindependent_four(self):
        facts = copy.deepcopy(self.facts); facts["m6"]["claims"][0]["support_evidence"] = []; facts["m6"]["claims"][0]["independent_crosscheck"] = False
        assessment = copy.deepcopy(self.assessment); assessment["metrics"]["M6"]["score"] = 4
        self.write_facts(facts); self.write_assessment(assessment); code, report = self.run_check()
        self.assertNotEqual(code, 0); self.assertTrue(any(x["code"] == "m6.support" for x in report["issues"]))

    def test_invalid_m6_verdict_and_empty_claim_inventory_fail(self):
        facts = copy.deepcopy(self.facts); facts["m6"]["claims"][0]["verdict"] = "maybe"
        self.write_facts(facts); code, report = self.run_check()
        self.assertNotEqual(code, 0); self.assertTrue(any(x["code"] == "m6.verdict" for x in report["issues"]))
        facts = copy.deepcopy(self.facts); facts["m6"]["claims"] = []
        self.write_facts(facts); code, report = self.run_check()
        self.assertNotEqual(code, 0); self.assertTrue(any(x["code"] == "m6.claims" for x in report["issues"]))

    def test_m6_four_is_valid_with_supported_claim_without_independent_crosscheck(self):
        facts = copy.deepcopy(self.facts); facts["m6"]["claims"][0]["independent_crosscheck"] = False
        assessment = copy.deepcopy(self.assessment); assessment["metrics"]["M6"]["score"] = 4
        assessment["metrics"]["M11"]["score"] = score_m11(assessment["metrics"])["score"]
        self.write_facts(facts); self.write_assessment(assessment); code, report = self.run_check()
        self.assertEqual(code, 0, report)

    def test_m9_five_requires_version_relation_fact(self):
        assessment = copy.deepcopy(self.assessment); assessment["metrics"]["M9"]["score"] = 5
        self.write_assessment(assessment); code, report = self.run_check()
        self.assertNotEqual(code, 0); self.assertTrue(any(x["code"] == "m9.facts" for x in report["issues"]))

    def test_source_and_fetch_ownership_disagreement_fails(self):
        facts = copy.deepcopy(self.facts); facts["fetches"][0]["ownership"] = "third_party"
        self.write_facts(facts); code, report = self.run_check()
        self.assertNotEqual(code, 0); self.assertTrue(any(x["code"] == "m2.ownership" for x in report["issues"]))

    def test_m11_missing_input_cannot_be_saturated(self):
        assessment = copy.deepcopy(self.assessment); assessment["metrics"]["M6"] = {"status": "unscorable", "score": None, "reason": "missing"}; assessment["metrics"]["M11"]["score"] = 100
        self.write_assessment(assessment); code, report = self.run_check()
        self.assertNotEqual(code, 0); self.assertTrue(any(x["code"] == "M11.status" for x in report["issues"]))

    def test_review_rejects_old_hash(self):
        code, report = self.run_check(); self.assertEqual(code, 0)
        review = {"reviewer": "human", "review_scope": "packet and assessment", "findings_resolved": True, "assessment_sha256": rescore.sha256_file(self.assessment_path), "facts_sha256": rescore.sha256_file(self.facts_path), "packet_sha256": rescore.sha256_file(self.packet_path), "check_report_sha256": rescore.sha256_file(self.report_path), "limitations": "Manual semantic review remains required."}
        self.review_path.write_text(json.dumps(review), encoding="utf-8")
        self.assertEqual(rescore.review_command(self.packet_path, self.assessment_path, self.facts_path, self.report_path, self.review_path, self.receipt_path), 0)
        self.facts_path.write_text(self.facts_path.read_text() + "\n", encoding="utf-8")
        self.assertNotEqual(rescore.review_command(self.packet_path, self.assessment_path, self.facts_path, self.report_path, self.review_path, self.receipt_path), 0)




class M5CandidateTests(unittest.TestCase):
    def test_candidate_assignments_preserve_duplicate_url_binding(self):
        facts = {"source_items": [{"url":"https://x.test/fixed","ownership":"third_party","relevant":True,"content_group":"same"},{"url":"https://x.test/a#one","ownership":"third_party","relevant":None,"content_group_candidates":["same","new"]},{"url":"https://x.test/a#two","ownership":"third_party","relevant":None,"content_group_candidates":["same","new"]}]}
        issues=[]; self.assertEqual(rescore.derive_m5_counts(facts, issues), [1,2]); self.assertEqual(issues, [])
    def test_fixed_same_url_constrains_candidate_and_inconsistent_rejects(self):
        fixed={"url":"https://x.test/same","ownership":"third_party","relevant":True,"content_group":"g"}
        candidate={"url":"https://x.test/same#frag","ownership":"third_party","relevant":None,"content_group_candidates":["g","new"]}
        self.assertEqual(rescore.derive_m5_counts({"source_items":[fixed,candidate]}, []), [1])
        bad={"url":"https://x.test/same#other","ownership":"third_party","relevant":None,"content_group_candidates":["other"]}
        issues=[]; self.assertIsNone(rescore.derive_m5_counts({"source_items":[fixed,bad]}, issues)); self.assertTrue(issues)

    def test_four_fixed_plus_ambiguous_group(self):
        items=[{"url":f"https://x.test/{i}","ownership":"third_party","relevant":True,"content_group":f"g{i}"} for i in range(4)]
        items.append({"url":"https://x.test/uncertain","ownership":"third_party","relevant":None,"content_group_candidates":["g0","g-new"]})
        self.assertEqual(rescore.derive_m5_counts({"source_items":items}, []), [4,5])
    def test_same_score_band_collapses_to_m5_three(self):
        items=[{"url":f"https://x.test/{i}","ownership":"third_party","relevant":True,"content_group":f"g{i}"} for i in range(3)]
        items.append({"url":"https://x.test/uncertain","ownership":"third_party","relevant":None,"content_group_candidates":["g0","g-new"]})
        possible=rescore.derive_m5_counts({"source_items":items}, []); self.assertEqual(possible,[3,4]); self.assertEqual(rescore.score_m5(possible),3)
    def test_two_units_selecting_same_new_group_count_once(self):
        items=[{"url":"https://x.test/a","ownership":"third_party","relevant":True,"content_group_candidates":["new"]},{"url":"https://x.test/b","ownership":"third_party","relevant":True,"content_group_candidates":["new"]}]
        self.assertEqual(rescore.derive_m5_counts({"source_items":items}, []), [1])


if __name__ == "__main__":
    unittest.main()
