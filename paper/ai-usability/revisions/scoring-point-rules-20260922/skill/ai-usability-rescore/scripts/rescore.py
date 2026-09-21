#!/usr/bin/env python3
"""Mechanical gate for the independent point-rescore evidence packet.

The command deliberately does not infer relevance, ownership, representation, or
technical meaning.  ``prepare`` only indexes a packet; ``quote`` copies an exact
substring already present in one packet event; ``check`` validates filled facts
against the packet and the point arithmetic; and ``review`` binds a human review
assertion to those exact bytes.  A mechanical pass is never a semantic pass.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import re
import sys
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import urlsplit, urlunsplit

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
from point_math import score_m1, score_m5, score_m8, score_m11  # noqa: E402
from validate_point_assessment import load_assessment, validate_assessment  # noqa: E402


FACT_KEYS = {
    "run_id", "packet_sha256", "question", "task_requirements", "source_items",
    "fetches", "m1", "m5", "m4", "m6", "m10",
}
OWNERSHIP = {"official", "third_party", "unknown"}
TARGET_MATCH = {"matched", "wrong", "unknown"}
REPRESENTATION = {"body", "excerpt", "title", "error", "unknown"}
M4_MODES = {"none", "partial", "combined", "direct", "unresolved", "not_applicable"}


class GateError(ValueError):
    pass


def read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"), parse_constant=lambda x: (_ for _ in ()).throw(ValueError(f"non-finite JSON constant: {x}")))
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        raise GateError(f"cannot read JSON {path}: {exc}") from exc


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_hash(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def ensure_separate(out: Path, inputs: Iterable[Path]) -> None:
    target = out.resolve()
    for source in inputs:
        if target == source.resolve():
            raise GateError(f"refusing to overwrite input: {out}")


def packet_run_id(packet: dict[str, Any]) -> str | None:
    metadata = packet.get("metadata")
    if isinstance(metadata, dict) and isinstance(metadata.get("run_id"), str):
        return metadata["run_id"]
    return packet.get("run_name") if isinstance(packet.get("run_name"), str) else None


def packet_process_hash(packet: dict[str, Any]) -> str | None:
    metadata = packet.get("metadata")
    if isinstance(metadata, dict) and isinstance(metadata.get("process_sha256"), str):
        return metadata["process_sha256"]
    return packet.get("process_sha256") if isinstance(packet.get("process_sha256"), str) else None


def url_without_fragment(url: Any) -> str | None:
    if not isinstance(url, str) or not url:
        return None
    p = urlsplit(url)
    return urlunsplit((p.scheme, p.netloc, p.path, p.query, ""))


def scalar_texts(obj: Any) -> list[str]:
    """Text that is permitted as quote evidence in a packet event."""
    if not isinstance(obj, dict):
        return []
    out: list[str] = []
    # These are the saved representations.  IDs/URLs are indexes, not prose.
    for key in ("text", "body", "content", "title", "quote", "message", "output", "error"):
        value = obj.get(key)
        if isinstance(value, str):
            out.append(value)
    return out


def event_index(packet: dict[str, Any]) -> dict[str, list[str]]:
    """Return event_id -> saved text representations, including prior/final."""
    result: dict[str, list[str]] = {}

    def add(event_id: Any, texts: Iterable[str]) -> None:
        if not isinstance(event_id, str) or not event_id:
            return
        values = [x for x in texts if isinstance(x, str)]
        if values:
            result.setdefault(event_id, []).extend(values)

    def walk(value: Any) -> None:
        if isinstance(value, dict):
            ids = [value.get(k) for k in ("event_id", "eventId")]
            for event_id in ids:
                add(event_id, scalar_texts(value))
            for child in value.values():
                walk(child)
        elif isinstance(value, list):
            for child in value:
                walk(child)

    # Keep the packet's saved event containers explicit.  Walking the entire
    # packet then catches nested event records without treating arbitrary IDs as
    # evidence.
    walk(packet)
    final = packet.get("final")
    if isinstance(final, str):
        add("final", [final])
        for event_id in packet.get("final_event_ids", []):
            add(event_id, [final])
    return result


def source_records(packet: dict[str, Any]) -> list[dict[str, Any]]:
    return [x for x in packet.get("sources", []) if isinstance(x, dict)] if isinstance(packet.get("sources"), list) else []


def dispatch_request_ids(packet: dict[str, Any]) -> set[str]:
    result: set[str] = set()
    for item in packet.get("dispatch_events", []) if isinstance(packet.get("dispatch_events"), list) else []:
        if isinstance(item, dict) and item.get("type") == "tool_dispatch" and isinstance(item.get("request_id"), str):
            result.add(item["request_id"])
    return result


def dispatch_sources(packet: dict[str, Any]) -> list[dict[str, Any]]:
    """Resolve responses in dispatch order; no URL or return is inferred."""
    by_request: dict[str, list[dict[str, Any]]] = {}
    for source in source_records(packet):
        request_id = source.get("request_id")
        if isinstance(request_id, str):
            by_request.setdefault(request_id, []).append(source)
    result: list[dict[str, Any]] = []
    for dispatch in packet.get("dispatch_events", []) if isinstance(packet.get("dispatch_events"), list) else []:
        if not isinstance(dispatch, dict) or dispatch.get("type") != "tool_dispatch":
            continue
        matches = by_request.get(dispatch.get("request_id"), [])
        if len(matches) == 1:
            result.append(matches[0])
    return result


def check_dispatch_integrity(packet: dict[str, Any], issues: list[dict[str, str]]) -> tuple[int, int, bool]:
    dispatches = [x for x in packet.get("dispatch_events", []) if isinstance(x, dict) and x.get("type") == "tool_dispatch"] if isinstance(packet.get("dispatch_events"), list) else []
    by_request: dict[str, list[dict[str, Any]]] = {}
    for source in source_records(packet):
        if isinstance(source.get("request_id"), str): by_request.setdefault(source["request_id"], []).append(source)
    search = fetch = 0
    valid = True
    for dispatch in dispatches:
        req = dispatch.get("request_id")
        matches = by_request.get(req, [])
        if len(matches) != 1:
            issue(issues, "dispatch.return", f"dispatch {dispatch.get('id', req)!r} resolves to {len(matches)} saved source returns; refusing to infer a count")
            valid = False; continue
        role = matches[0].get("role")
        if role == "search": search += 1
        elif role == "fetch": fetch += 1
        else:
            issue(issues, "dispatch.role", f"dispatch {req!r} has no search/fetch source role")
            valid = False
    if len(dispatches) != len(dispatch_sources(packet)):
        valid = False
    return search, fetch, valid


def actual_sources(packet: dict[str, Any], role: str | None = None) -> list[dict[str, Any]]:
    dispatched = dispatch_request_ids(packet)
    return [s for s in dispatch_sources(packet) if (role is None or s.get("role") == role) and s.get("request_id") in dispatched]


def actual_fetch_groups(packet: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    groups: dict[str, list[dict[str, Any]]] = {}
    for source in actual_sources(packet, "fetch"):
        key = url_without_fragment(source.get("url"))
        if key is None:
            # Retain malformed/unknown URL as a distinct key so it cannot vanish.
            key = f"__missing_url__:{source.get('event_id', source.get('request_id', len(groups)))}"
        groups.setdefault(key, []).append(source)
    return groups


def search_result_blocks(text: Any) -> list[dict[str, Any]]:
    """Parse saved search-result blocks without assigning ownership/relevance.

    Search providers format their headings differently.  The only facts this
    parser records are an explicit rank, URL, and the exact result block.  An
    unparseable result remains a manual inventory obligation in ``check``.
    """
    if not isinstance(text, str):
        return []
    pattern = re.compile(r"(?ms)^##\s+(\d+)\.\s+.*?(?=^##\s+\d+\.|^\*Found\b|\Z)")
    blocks: list[dict[str, Any]] = []
    for match in pattern.finditer(text):
        block = match.group(0)
        # The provider's explicit URL line is authoritative and handles URLs
        # containing parentheses (which cannot be parsed from Markdown links by
        # looking for the first closing parenthesis).
        url_match = re.search(r"(?m)^\*\*URL:\*\*\s*(https?://\S+)", block)
        url = url_match.group(1).rstrip(".,;") if url_match else None
        if not url:
            # Fallback for providers that omit the URL line.  Stop at whitespace;
            # a trailing Markdown delimiter is removed only at the very end.
            fallback = re.search(r"\]\((https?://[^\s]+)", block)
            url = fallback.group(1).rstrip(".,;") if fallback else None
            if url and url.endswith(")"):
                url = url[:-1]
        blocks.append({"rank": int(match.group(1)), "url": url, "quote": block})
    return blocks


def parse_search_results(text: Any) -> list[dict[str, Any]]:
    return [x for x in search_result_blocks(text) if x.get("url")]


def exact_quote(index: dict[str, list[str]], event_id: str, substring: str) -> str:
    if event_id not in index:
        raise GateError(f"event not found or has no saved text: {event_id}")
    if not isinstance(substring, str) or substring == "":
        raise GateError("--contains must be a non-empty exact substring")
    for text in index[event_id]:
        if substring in text:
            return substring
    raise GateError(f"exact substring is absent from event {event_id}")


def prepare(packet_path: Path, out_dir: Path) -> Path:
    ensure_separate(out_dir / "facts.json", [packet_path])
    packet = read_json(packet_path)
    if not isinstance(packet, dict):
        raise GateError("packet must be a JSON object")
    run_id = packet_run_id(packet)
    if not run_id:
        raise GateError("packet has no run_name/metadata.run_id")
    source_items = []
    search_query_order = {s.get("event_id"): n for n, s in enumerate(actual_sources(packet, "search"), 1)}
    for i, source in enumerate(source_records(packet), 1):
        event_id = source.get("event_id") if isinstance(source.get("event_id"), str) else f"source-event-{i:04d}"
        base_item = {
            "source_id": f"source-{i:04d}", "event_id": event_id,
            "url": source.get("url") if isinstance(source.get("url"), str) else None,
            "ownership": "unknown", "relevant": None, "content_group": "",
            "evidence": {"event_id": event_id, "quote": ""},
        }
        source_items.append(base_item)
        if source.get("role") == "search":
            for result in parse_search_results(source.get("text")):
                source_items.append({
                    "source_id": f"source-{i:04d}-rank-{result['rank']}",
                    "event_id": event_id, "url": result["url"], "ownership": "unknown",
                    "relevant": None, "content_group": "", "query_index": search_query_order.get(event_id),
                    "rank": result["rank"], "evidence": {"event_id": event_id, "quote": result["quote"]},
                })
    fetches = []
    for url, entries in actual_fetch_groups(packet).items():
        if not entries:
            continue
        source = entries[-1]
        fetches.append({
            "request_url": url, "event_id": source.get("event_id"), "ownership": "unknown",
            "target_match": "unknown", "representation": "unknown", "observed_defect": None,
            "evidence": {"event_id": source.get("event_id"), "quote": ""},
        })
    facts = {
        "run_id": run_id, "packet_sha256": sha256_file(packet_path),
        "question": packet.get("question") if isinstance(packet.get("question"), str) else "",
        "task_requirements": {"main": [], "secondary": [], "version_relations": []},
        "source_items": source_items, "fetches": fetches,
        "m1": {"first_query": None, "first_rank": None, "first_hit_source_id": None, "decisive_records_verified": None, "budget_exhausted": None},
        "m5": {"possible_counts": []},
        "m4": {"missing_relations": [], "conflicts": [], "mode": "none"},
        "m6": {"checked_event_ids": [], "claims": [], "no_third_party_material": None, "confirmed_unavailable": {}},
        "m10": {"content_repairs": [], "environment_substitutions": [], "content_check_complete": None},
    }
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / "facts.json"
    write_json(out, facts)
    # A small immutable index helps a reviewer see the packet boundary without
    # importing any content judgement.
    write_json(out_dir / "packet-index.json", {"run_id": run_id, "packet_sha256": facts["packet_sha256"], "source_event_ids": [x["event_id"] for x in source_items]})
    return out


def quote_command(packet_path: Path, event_id: str, substring: str) -> None:
    packet = read_json(packet_path)
    if not isinstance(packet, dict):
        raise GateError("packet must be a JSON object")
    quote = exact_quote(event_index(packet), event_id, substring)
    print(json.dumps({"event_id": event_id, "quote": quote}, ensure_ascii=False))


def issue(issues: list[dict[str, str]], code: str, message: str) -> None:
    issues.append({"code": code, "message": message})


def check_fact_shape(facts: Any, issues: list[dict[str, str]]) -> None:
    if not isinstance(facts, dict):
        issue(issues, "facts.type", "facts must be an object")
        return
    unknown = set(facts) - FACT_KEYS
    missing = FACT_KEYS - set(facts)
    for key in sorted(unknown): issue(issues, "facts.field", f"unexpected facts field: {key}")
    for key in sorted(missing): issue(issues, "facts.field", f"missing facts field: {key}")
    if not isinstance(facts.get("source_items"), list): issue(issues, "facts.source_items", "source_items must be an array")
    if not isinstance(facts.get("fetches"), list): issue(issues, "facts.fetches", "fetches must be an array")
    if not isinstance(facts.get("task_requirements"), dict): issue(issues, "facts.requirements", "task_requirements must be an object")
    for item in facts.get("source_items", []) if isinstance(facts.get("source_items"), list) else []:
        if not isinstance(item, dict): issue(issues, "facts.source_item", "source item must be an object"); continue
        for key in ("source_id", "event_id", "url", "ownership", "relevant", "content_group", "evidence"):
            if key not in item: issue(issues, "facts.source_item", f"source item missing {key}")
        if item.get("ownership") not in OWNERSHIP: issue(issues, "facts.ownership", f"invalid ownership: {item.get('ownership')!r}")
        if item.get("relevant") not in (True, False, None): issue(issues, "facts.relevant", "relevant must be true, false, or null")
        if not isinstance(item.get("evidence"), dict): issue(issues, "facts.evidence", "source evidence must be an object")
    for item in facts.get("fetches", []) if isinstance(facts.get("fetches"), list) else []:
        if not isinstance(item, dict): issue(issues, "facts.fetch", "fetch fact must be an object"); continue
        for key in ("request_url", "event_id", "ownership", "target_match", "representation", "observed_defect", "evidence"):
            if key not in item: issue(issues, "facts.fetch", f"fetch fact missing {key}")
        if item.get("ownership") not in OWNERSHIP: issue(issues, "facts.ownership", f"invalid fetch ownership: {item.get('ownership')!r}")
        if item.get("target_match") not in TARGET_MATCH: issue(issues, "facts.target_match", f"invalid target_match: {item.get('target_match')!r}")
        if item.get("representation") not in REPRESENTATION: issue(issues, "facts.representation", f"invalid representation: {item.get('representation')!r}")
        if item.get("observed_defect") not in (True, False, None): issue(issues, "facts.observed_defect", "observed_defect must be true, false, or null")
    m1 = facts.get("m1")
    if not isinstance(m1, dict): issue(issues, "facts.m1", "m1 must be an object")
    else:
        for key in ("first_query", "first_rank", "first_hit_source_id", "decisive_records_verified", "budget_exhausted"):
            if key not in m1: issue(issues, "facts.m1", f"m1 missing {key}")
        for key in ("decisive_records_verified", "budget_exhausted"):
            if m1.get(key) not in (True, False, None): issue(issues, "facts.m1", f"{key} must be true, false, or null")
    m5 = facts.get("m5")
    if not isinstance(m5, dict) or not isinstance(m5.get("possible_counts"), list): issue(issues, "facts.m5", "m5.possible_counts must be an array")
    m4 = facts.get("m4")
    if not isinstance(m4, dict): issue(issues, "facts.m4", "m4 must be an object")
    else:
        if m4.get("mode") not in M4_MODES: issue(issues, "facts.m4", f"invalid m4.mode: {m4.get('mode')!r}")
        for key in ("missing_relations", "conflicts"):
            if not isinstance(m4.get(key), list): issue(issues, "facts.m4", f"m4.{key} must be an array")
    m6 = facts.get("m6")
    if not isinstance(m6, dict): issue(issues, "facts.m6", "m6 must be an object")
    else:
        if m6.get("no_third_party_material") not in (True, False, None): issue(issues, "facts.m6", "no_third_party_material must be true, false, or null")
        if not isinstance(m6.get("claims"), list): issue(issues, "facts.m6", "claims must be an array")
        if "confirmed_unavailable" in m6 and not isinstance(m6.get("confirmed_unavailable"), dict): issue(issues, "facts.m6", "confirmed_unavailable must be an object")
    m10 = facts.get("m10")
    if not isinstance(m10, dict): issue(issues, "facts.m10", "m10 must be an object")
    else:
        if m10.get("content_check_complete") not in (True, False, None): issue(issues, "facts.m10", "content_check_complete must be true, false, or null")


def quote_exists(index: dict[str, list[str]], evidence: Any) -> bool:
    return isinstance(evidence, dict) and isinstance(evidence.get("event_id"), str) and isinstance(evidence.get("quote"), str) and bool(evidence["quote"]) and any(evidence["quote"] in text for text in index.get(evidence["event_id"], []))


def check_all_quotes(facts: dict[str, Any], assessment: dict[str, Any], index: dict[str, list[str]], issues: list[dict[str, str]]) -> None:
    def one(ev: Any, where: str) -> None:
        if not quote_exists(index, ev): issue(issues, "quote.missing", f"{where} quote is absent or not verbatim in packet event")
    for i, item in enumerate(facts.get("source_items", [])):
        if isinstance(item, dict): one(item.get("evidence"), f"facts.source_items[{i}]")
    for i, item in enumerate(facts.get("fetches", [])):
        if isinstance(item, dict): one(item.get("evidence"), f"facts.fetches[{i}]")
    m6 = facts.get("m6", {})
    for i, claim in enumerate(m6.get("claims", []) if isinstance(m6, dict) else []):
        if not isinstance(claim, dict): issue(issues, "facts.m6.claim", f"claim {i} must be object"); continue
        for name in ("claim_evidence", "support_evidence"):
            for j, ev in enumerate(claim.get(name, []) if isinstance(claim.get(name), list) else []): one(ev, f"facts.m6.claims[{i}].{name}[{j}]")
    for name, value in facts.get("m10", {}).items() if isinstance(facts.get("m10"), dict) else []:
        if isinstance(value, list):
            for i, ev in enumerate(value):
                # M10 repair/substitution strings are intentionally not treated
                # as evidence: only explicit event/quote objects are copied.
                if isinstance(ev, dict): one(ev, f"facts.m10.{name}[{i}]")
    for name, metric in assessment.get("metrics", {}).items() if isinstance(assessment.get("metrics"), dict) else []:
        if not isinstance(metric, dict): continue
        for i, ev in enumerate(metric.get("evidence", []) if isinstance(metric.get("evidence"), list) else []): one(ev, f"assessment.{name}.evidence[{i}]")


def check_search_inventory(packet: dict[str, Any], facts: dict[str, Any], issues: list[dict[str, str]], warnings: list[dict[str, str]]) -> None:
    """Ensure source_items cannot silently omit search result candidates."""
    items = facts.get("source_items", [])
    if not isinstance(items, list):
        return
    item_keys = {(url_without_fragment(x.get("url")), x.get("event_id")) for x in items if isinstance(x, dict) and x.get("url")}
    search_order = {source.get("event_id"): i for i, source in enumerate(actual_sources(packet, "search"), 1)}
    for source in actual_sources(packet, "search"):
        blocks = search_result_blocks(source.get("text"))
        results = [x for x in blocks if x.get("url")]
        if not results:
            if isinstance(source.get("text"), str) and re.search(r"\b(?:error|failed|failure)\b", source["text"], re.I):
                warnings.append({"code": "search.error", "message": f"search event {source.get('event_id')} contains an explicit saved provider error; no result ranking was inferred"})
                continue
            issue(issues, "search.inventory", f"search event {source.get('event_id')} has no parseable result blocks; manual inventory review is required")
            continue
        ranks = [x["rank"] for x in blocks]
        if len(ranks) != len(set(ranks)): issue(issues, "search.inventory", f"search event {source.get('event_id')} has duplicate result ranks")
        if any(not x.get("url") for x in blocks): issue(issues, "search.inventory", f"search event {source.get('event_id')} has a result heading whose URL could not be parsed")
        for result in results:
            key = (url_without_fragment(result["url"]), source.get("event_id"))
            if key not in item_keys:
                issue(issues, "search.inventory", f"search result rank {result['rank']} URL is missing from source_items: {result['url']}")
            matching = [x for x in items if isinstance(x, dict) and x.get("event_id") == source.get("event_id") and url_without_fragment(x.get("url")) == url_without_fragment(result["url"])]
            if matching:
                for item in matching:
                    if item.get("query_index") != search_order.get(source.get("event_id")) or item.get("rank") != result.get("rank"):
                        issue(issues, "search.inventory", f"source_items rank/query index disagrees with saved search row {result['url']}")


def source_map(facts: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {x.get("source_id"): x for x in facts.get("source_items", []) if isinstance(x, dict) and isinstance(x.get("source_id"), str)}


def derive_m5_counts(facts: dict[str, Any], issues: list[dict[str, str]]) -> list[int] | None:
    groups = facts.get("source_items", [])
    if not isinstance(groups, list): return None
    known: set[str] = set(); uncertain: set[str] = set()
    for item in groups:
        if not isinstance(item, dict): continue
        # A bare event index row (for example a search event with no URL) is
        # retained for provenance but is not a candidate source to count.
        if not item.get("url"):
            continue
        relevant = item.get("relevant")
        ownership = item.get("ownership")
        if relevant is False: continue
        group = item.get("content_group")
        if not isinstance(group, str) or not group.strip():
            issue(issues, "m5.content_group", "every potentially relevant source item needs a content_group")
            continue
        if ownership == "third_party" and relevant is True: known.add(group)
        elif ownership == "third_party" and relevant is None: uncertain.add(group)
        elif ownership == "unknown" and relevant in (True, None): uncertain.add(group)
    uncertain -= known
    return list(range(len(known), len(known) + len(uncertain) + 1))


def assessment_metric(assessment: dict[str, Any], name: str) -> dict[str, Any] | None:
    metric = assessment.get("metrics", {}).get(name) if isinstance(assessment.get("metrics"), dict) else None
    return metric if isinstance(metric, dict) else None


def compare_point(assessment: dict[str, Any], name: str, expected: Any, issues: list[dict[str, str]], *, required: bool = True) -> None:
    metric = assessment_metric(assessment, name)
    if metric is None: return
    if expected is None:
        if required and metric.get("status") == "scored": issue(issues, f"{name}.unknown", f"{name} is scored although its factual inputs are incomplete or unresolved")
        return
    if metric.get("status") != "scored":
        if required: issue(issues, f"{name}.status", f"{name} status does not reflect a mechanically computable point")
    elif not math.isclose(metric.get("score"), expected, rel_tol=0.0, abs_tol=1e-9):
        issue(issues, f"{name}.score", f"assessment score {metric.get('score')!r} != point arithmetic {expected!r}")


def check_m2(packet: dict[str, Any], facts: dict[str, Any], assessment: dict[str, Any], issues: list[dict[str, str]]) -> None:
    groups = actual_fetch_groups(packet)
    final_sources = {key: entries[-1] for key, entries in groups.items() if entries}
    fetches = facts.get("fetches", [])
    if not isinstance(fetches, list): return
    by_url: dict[str, list[dict[str, Any]]] = {}
    for fact in fetches:
        if isinstance(fact, dict): by_url.setdefault(url_without_fragment(fact.get("request_url")) or str(fact.get("request_url")), []).append(fact)
    if set(by_url) != set(final_sources):
        issue(issues, "m2.coverage", "facts.fetches must contain exactly one final fact for every dispatched fetch URL after fragment removal")
    official: list[tuple[str, int]] = []
    unresolved = False
    for url, source in final_sources.items():
        entries = by_url.get(url, [])
        if len(entries) != 1: issue(issues, "m2.duplicate", f"fetch URL has {len(entries)} fact rows: {url}"); continue
        fact = entries[0]
        if fact.get("event_id") != source.get("event_id"): issue(issues, "m2.last_return", f"fact for {url} must reference last dispatched return {source.get('event_id')}")
        if fact.get("ownership") == "unknown" or fact.get("target_match") == "unknown" or fact.get("representation") == "unknown" or fact.get("observed_defect") is None:
            unresolved = True; continue
        if fact.get("ownership") != "official": continue
        if fact.get("target_match") != "matched" or fact.get("representation") == "error": score = 1
        elif fact.get("representation") == "title": score = 2
        elif fact.get("representation") == "excerpt": score = 3
        elif fact.get("representation") == "body": score = 4 if fact.get("observed_defect") else 5
        else: unresolved = True; continue
        official.append((fact.get("event_id"), score))
    metric = assessment_metric(assessment, "M2")
    docs = metric.get("documents", []) if isinstance(metric, dict) else []
    if unresolved:
        if metric and metric.get("status") == "scored": issue(issues, "m2.unknown", "unknown ownership/representation/defect prevents an M2 point")
        return
    if not official:
        if metric and metric.get("status") == "scored": issue(issues, "m2.no_official", "M2 cannot be scored without a mechanically mapped official fetch")
        return
    expected_by_id = {event_id: score for event_id, score in official}
    used: set[str] = set()
    expected_scores: list[int] = []
    for doc in docs if isinstance(docs, list) else []:
        if not isinstance(doc, dict): continue
        doc_id = doc.get("id")
        match = next((event_id for event_id in expected_by_id if event_id == doc_id or url_without_fragment(doc_id) in final_sources and url_without_fragment(doc_id) == next((u for u, s in final_sources.items() if s.get("event_id") == event_id), None)), None)
        if match is None:
            issue(issues, "m2.document_mapping", f"M2 document {doc_id!r} is not mapped to an official fetch fact")
        else:
            used.add(match); expected_scores.append(expected_by_id[match])
            if doc.get("status") == "scored" and doc.get("score") != expected_by_id[match]: issue(issues, "m2.document_score", f"document {doc_id!r} score is not the fact-derived point")
    if used != set(expected_by_id): issue(issues, "m2.document_coverage", "every official fetch fact must map to one M2 document")
    if metric and metric.get("status") == "scored" and expected_scores:
        mean = math.fsum(expected_scores) / len(expected_scores)
        if not math.isclose(metric.get("score"), mean, rel_tol=0.0, abs_tol=1e-9): issue(issues, "m2.mean", f"M2 score must equal mapped official-document mean {mean!r}")


def check_m6(facts: dict[str, Any], assessment: dict[str, Any], issues: list[dict[str, str]]) -> None:
    smap = source_map(facts); claims = facts.get("m6", {}).get("claims", []) if isinstance(facts.get("m6"), dict) else []
    third_party_relevant = {sid for sid, item in smap.items() if item.get("ownership") == "third_party" and item.get("relevant") is True}
    unknown_relevant = any(item.get("ownership") == "unknown" and item.get("relevant") in (True, None) for item in smap.values())
    official_urls = {url_without_fragment(x.get("request_url")) for x in facts.get("fetches", []) if isinstance(x, dict) and x.get("ownership") == "official"}
    verdicts: list[dict[str, Any]] = []
    for i, claim in enumerate(claims if isinstance(claims, list) else []):
        if not isinstance(claim, dict): continue
        sid = claim.get("source_id")
        if sid not in third_party_relevant: issue(issues, "m6.claim_source", f"claim {i} must point to a relevant third-party source_item")
        elif url_without_fragment(smap[sid].get("url")) in official_urls:
            issue(issues, "m6.claim_source", f"claim {i} labels a URL already mapped as official as third-party; ownership needs semantic review")
        ce = claim.get("claim_evidence", []); se = claim.get("support_evidence", [])
        claim_events = {x.get("event_id") for x in ce if isinstance(x, dict)}
        support_events = {x.get("event_id") for x in se if isinstance(x, dict)}
        source_event = smap.get(sid, {}).get("event_id") if sid in smap else None
        if source_event and any(x.get("event_id") != source_event for x in ce if isinstance(x, dict)):
            issue(issues, "m6.claim_evidence", f"claim {i} evidence must belong to its source_item event")
        verdict = claim.get("verdict")
        if verdict not in {"supported", "unsupported", "contradicted", "unresolved"}:
            issue(issues, "m6.verdict", f"claim {i} has an invalid verdict")
        if verdict == "supported" and not support_events:
            issue(issues, "m6.support", f"supported claim {i} needs at least one packet support_evidence quote")
        if verdict == "supported" and claim.get("independent_crosscheck"):
            if not support_events or claim_events & support_events:
                issue(issues, "m6.independence", f"supported claim {i} lacks an independent support event")
            # A second source item must carry the support event; reusing a
            # mixed search event is not an independent cross-check.
            support_source_events = {x.get("event_id") for x in smap.values() if x.get("event_id") != source_event}
            if not support_events & support_source_events:
                issue(issues, "m6.independence", f"supported claim {i} support is not tied to a different source event")
        verdicts.append(claim)
    metric = assessment_metric(assessment, "M6")
    no_material = facts.get("m6", {}).get("no_third_party_material") if isinstance(facts.get("m6"), dict) else None
    if no_material is True:
        if third_party_relevant or unknown_relevant: issue(issues, "m6.no_material", "no_third_party_material conflicts with relevant third-party/unknown source items")
        if verdicts: issue(issues, "m6.no_material", "no_third_party_material cannot coexist with claims")
        return
    if not verdicts:
        if metric and metric.get("status") == "scored": issue(issues, "m6.claims", "numeric M6 requires an explicit claim inventory or confirmed no-third-party exception")
        return
    if any(c.get("verdict") == "unresolved" for c in verdicts):
        if metric and metric.get("status") == "scored": issue(issues, "m6.unresolved", "an unresolved claim cannot receive a numeric M6")
        return
    if any(c.get("verdict") == "contradicted" for c in verdicts): expected = 1
    elif all(c.get("verdict") == "supported" and c.get("independent_crosscheck") for c in verdicts): expected = 5
    elif all(c.get("verdict") == "supported" for c in verdicts): expected = 4
    elif any(c.get("verdict") == "supported" for c in verdicts): expected = 3
    else: expected = 2
    compare_point(assessment, "M6", expected, issues)


def check_m11(packet: dict[str, Any], facts: dict[str, Any], assessment: dict[str, Any], issues: list[dict[str, str]]) -> None:
    applicability = packet.get("applicability", {}) if isinstance(packet.get("applicability"), dict) else {}
    m4_app = applicability.get("M4", {}).get("applicable") if isinstance(applicability.get("M4"), dict) else None
    metric4 = assessment_metric(assessment, "M4")
    if m4_app is False and (not metric4 or metric4.get("status") != "not_applicable" or metric4.get("score") is not None): issue(issues, "applicability.M4", "packet says M4 is not applicable; assessment must use not_applicable")
    facts_m4 = facts.get("m4", {})
    if isinstance(facts_m4, dict) and facts_m4.get("missing_relations") and metric4 and metric4.get("status") == "scored" and metric4.get("score", 0) >= 4: issue(issues, "m4.missing_relations", "M4 missing relations forbid a 4/5 point")
    for name in ("M9", "M10"):
        applicable = applicability.get(name, {}).get("applicable") if isinstance(applicability.get(name), dict) else None
        metric = assessment_metric(assessment, name)
        if applicable is False and (not metric or metric.get("status") != "not_applicable" or metric.get("score") is not None): issue(issues, f"applicability.{name}", f"packet says {name} is not applicable; assessment must use not_applicable")
        if applicable is True and metric and metric.get("status") == "not_applicable": issue(issues, f"applicability.{name}", f"packet says {name} is applicable; assessment cannot mark it not_applicable")
    facts_m10 = facts.get("m10", {})
    metric10 = assessment_metric(assessment, "M10")
    if isinstance(facts_m10, dict) and metric10:
        repairs = facts_m10.get("content_repairs", [])
        if repairs and metric10.get("status") == "scored" and metric10.get("score", 0) >= 4: issue(issues, "m10.repairs", "content repairs forbid M10=4/5")
        if facts_m10.get("content_check_complete") is not True and metric10.get("status") == "scored": issue(issues, "m10.incomplete", "incomplete content check cannot be presented as a passed numeric M10")
        if facts_m10.get("environment_substitutions") and metric10.get("status") == "scored" and metric10.get("score") == 5: issue(issues, "m10.environment", "environment substitutions forbid M10=5")
    metric9 = assessment_metric(assessment, "M9")
    requirements = facts.get("task_requirements") if isinstance(facts.get("task_requirements"), dict) else {}
    m9_applicable = applicability.get("M9", {}).get("applicable") if isinstance(applicability.get("M9"), dict) else None
    if m9_applicable is True and metric9 and metric9.get("status") == "scored" and metric9.get("score") == 5 and not requirements.get("version_relations"):
        issue(issues, "m9.facts", "M9=5 requires a filled task version-relations fact set")
    metrics = assessment.get("metrics", {})
    confirmed: dict[str, Any] = {}
    if isinstance(facts.get("m6"), dict) and facts["m6"].get("no_third_party_material") is True:
        declared = facts["m6"].get("confirmed_unavailable", {})
        state = declared.get("third_party") if isinstance(declared, dict) else None
        evidence = state.get("evidence") if isinstance(state, dict) else None
        # A bare no-material observation cannot create the point_math exception;
        # it leaves M6/N11 unresolved.  Only an explicit declaration is checked
        # and passed to point_math.
        if state is not None:
            derived_counts = derive_m5_counts(facts, issues)
            if not isinstance(state, dict) or state.get("status") != "confirmed_unavailable" or state.get("budget_exhausted") is not True or derived_counts != [0] or not isinstance(state.get("reason"), str) or not state["reason"].strip() or not isinstance(evidence, list) or not evidence or any(not quote_exists(event_index(packet), ev) for ev in evidence):
                issue(issues, "m11.no_material_basis", "confirmed_unavailable third_party requires budget exhaustion, zero possible third-party counts, reason, and packet evidence")
            else:
                confirmed["third_party"] = state
    result = score_m11(metrics, confirmed_unavailable=confirmed, m4_not_applicable=(m4_app is False))
    m11 = assessment_metric(assessment, "M11")
    if m11:
        if result.get("status") != m11.get("status"): issue(issues, "M11.status", f"M11 status {m11.get('status')!r} != point_math {result.get('status')!r}")
        if result.get("status") == "scored" and not math.isclose(m11.get("score"), result.get("score"), rel_tol=0.0, abs_tol=1e-9): issue(issues, "M11.score", "M11 score does not match point_math")
        if result.get("status") != "scored" and m11.get("score") is not None: issue(issues, "M11.score", "non-scored M11 must have null score")


def check_command(packet_path: Path, assessment_path: Path, facts_path: Path, out_path: Path) -> int:
    ensure_separate(out_path, [packet_path, assessment_path, facts_path])
    packet = read_json(packet_path); facts = read_json(facts_path)
    try: assessment = load_assessment(assessment_path)
    except Exception as exc: assessment = None; assessment_error = str(exc)
    else: assessment_error = None
    issues: list[dict[str, str]] = []
    warnings: list[dict[str, str]] = []
    if not isinstance(packet, dict): issue(issues, "packet.type", "packet must be an object"); packet = {}
    if assessment_error: issue(issues, "assessment.read", assessment_error)
    elif not isinstance(assessment, dict): issue(issues, "assessment.type", "assessment must be an object")
    else:
        for error in validate_assessment(assessment): issue(issues, "assessment.schema", error)
    check_fact_shape(facts, issues)
    if isinstance(facts, dict) and packet_run_id(packet) != facts.get("run_id"): issue(issues, "run_id", "facts.run_id does not match packet run_name/metadata.run_id")
    if isinstance(facts, dict) and facts.get("packet_sha256") != sha256_file(packet_path): issue(issues, "packet_sha256", "facts packet hash is stale or mismatched")
    if isinstance(assessment, dict):
        if assessment.get("run_id") != packet_run_id(packet): issue(issues, "run_id", "assessment.run_id does not match packet run id")
        if assessment.get("process_sha256") != packet_process_hash(packet): issue(issues, "process_sha256", "assessment process hash does not match packet process hash")
    index = event_index(packet)
    if isinstance(facts, dict) and isinstance(assessment, dict):
        check_all_quotes(facts, assessment, index, issues)
        check_search_inventory(packet, facts, issues, warnings)
        check_m2(packet, facts, assessment, issues)
        # A fetch row and its source inventory row must not silently disagree
        # about ownership for the same saved event/URL.
        for fetch in facts.get("fetches", []) if isinstance(facts.get("fetches"), list) else []:
            if not isinstance(fetch, dict) or fetch.get("ownership") == "unknown":
                continue
            f_url = url_without_fragment(fetch.get("request_url"))
            for source_item in facts.get("source_items", []) if isinstance(facts.get("source_items"), list) else []:
                if not isinstance(source_item, dict) or source_item.get("event_id") != fetch.get("event_id") or source_item.get("ownership") in (None, "unknown"):
                    continue
                if f_url and url_without_fragment(source_item.get("url")) == f_url and source_item.get("ownership") != fetch.get("ownership"):
                    issue(issues, "m2.ownership", f"source_item and fetch disagree for {fetch.get('event_id')}")
        # M1 cannot be confirmed from a partially parsed search list.  A null
        # decisive_records_verified is deliberately unresolved, never false->score.
        m1 = facts.get("m1", {})
        expected_m1 = None
        if isinstance(m1, dict) and m1.get("decisive_records_verified") is True:
            sid = m1.get("first_hit_source_id")
            smap = source_map(facts)
            hit = smap.get(sid) if isinstance(sid, str) else None
            if m1.get("first_query") is not None and hit is None: issue(issues, "m1.first_hit", "M1 first_hit_source_id must map to source_items")
            elif m1.get("first_query") is not None and (hit.get("ownership") != "official" or hit.get("relevant") is not True): issue(issues, "m1.first_hit", "M1 first hit must be explicitly reviewed as relevant official")
            elif m1.get("first_query") is not None and (hit.get("query_index") != m1.get("first_query") or hit.get("rank") != m1.get("first_rank")): issue(issues, "m1.first_hit", "M1 first hit query/rank does not match its source inventory row")
            elif m1.get("first_query") is None and sid is not None: issue(issues, "m1.first_hit", "M1 no-hit record cannot have first_hit_source_id")
            else:
                if m1.get("first_query") is not None:
                    earlier = [x for x in smap.values() if x.get("ownership") == "official" and x.get("relevant") is True and isinstance(x.get("query_index"), int) and isinstance(x.get("rank"), int) and (x["query_index"], x["rank"]) < (m1["first_query"], m1["first_rank"])]
                    if earlier: issue(issues, "m1.first_hit", "M1 first hit is not the earliest reviewed official relevant result")
                    uncertain_before = [x for x in smap.values() if x.get("url") and x.get("relevant") in (True, None) and (x.get("ownership") == "unknown" or x.get("relevant") is None) and isinstance(x.get("query_index"), int) and isinstance(x.get("rank"), int) and x.get("rank") <= 5 and (x["query_index"], x["rank"]) < (m1["first_query"], m1["first_rank"])]
                    if uncertain_before:
                        # An unknown earlier row only blocks a point when it
                        # could move the result across a rubric band.  For
                        # example, unknown rank 2 vs known rank 3 in query 1
                        # remains M1=4 either way.
                        try:
                            possible = {score_m1(m1.get("first_query"), m1.get("first_rank"), decisive_records_verified=True)}
                            possible.update(score_m1(x.get("query_index"), x.get("rank"), decisive_records_verified=True) for x in uncertain_before if x.get("query_index") <= 4 and x.get("rank") <= 5)
                            if len(possible) > 1: issue(issues, "m1.uncertain_preceding", "an earlier unknown result could change the M1 score band")
                        except (TypeError, ValueError):
                            issue(issues, "m1.uncertain_preceding", "an earlier unknown result has unusable query/rank coordinates")
                if m1.get("first_query") is None:
                    known_hit = [x for x in smap.values() if x.get("url") and x.get("ownership") == "official" and x.get("relevant") is True and isinstance(x.get("query_index"), int) and isinstance(x.get("rank"), int) and x.get("query_index") <= 4 and x.get("rank") <= 5]
                    if known_hit: issue(issues, "m1.no_hit_conflict", "M1 no-hit fact conflicts with an explicitly reviewed official hit")
                try:
                    if not any(x.get("code") in {"m1.first_hit", "m1.uncertain_preceding", "m1.no_hit_conflict", "m1.inputs"} for x in issues):
                        expected_m1 = score_m1(m1.get("first_query"), m1.get("first_rank"), decisive_records_verified=True, budget_exhausted=m1.get("budget_exhausted") is True)
                except (TypeError, ValueError) as exc:
                    issue(issues, "m1.inputs", f"M1 point arithmetic rejected first-hit coordinates: {exc}")
        compare_point(assessment, "M1", expected_m1, issues)
        possible = derive_m5_counts(facts, issues)
        m5_facts = facts.get("m5") if isinstance(facts.get("m5"), dict) else {}
        provided = m5_facts.get("possible_counts")
        if possible is not None and sorted(set(provided or [])) != possible: issue(issues, "m5.counts", f"possible_counts must equal derived admissible counts {possible!r}")
        expected_m5 = score_m5(possible or []) if possible is not None else None
        compare_point(assessment, "M5", expected_m5, issues)
        searches, fetch_count, dispatch_valid = check_dispatch_integrity(packet, issues)
        expected_m8 = score_m8(searches, fetch_count, valid_complete_run=dispatch_valid and bool(packet.get("dispatch_events")))
        compare_point(assessment, "M8", expected_m8, issues)
        check_m6(facts, assessment, issues)
        try: check_m11(packet, facts, assessment, issues)
        except (ValueError, KeyError, TypeError, AttributeError) as exc: issue(issues, "M11.inputs", f"point_math could not evaluate M11: {exc}")
    report: dict[str, Any] = {
        "report_version": "ai-usability-rescore-report-v1", "mechanical_pass": not issues,
        "semantic_pass": False, "packet_sha256": sha256_file(packet_path),
        "assessment_sha256": sha256_file(assessment_path), "facts_sha256": sha256_file(facts_path),
        "run_id": packet_run_id(packet), "process_sha256": packet_process_hash(packet),
        "issues": issues, "warnings": warnings,
        "limitations": ["This report checks filled mappings and arithmetic only; it does not establish that an agent's ownership, relevance, representation, or technical classification is true. A reviewer must inspect the original packet."],
    }
    report["report_sha256"] = canonical_hash({k: v for k, v in report.items() if k != "report_sha256"})
    write_json(out_path, report)
    return 0 if not issues else 1


def review_command(packet_path: Path, assessment_path: Path, facts_path: Path, report_path: Path, review_path: Path, out_path: Path) -> int:
    ensure_separate(out_path, [packet_path, assessment_path, facts_path, report_path, review_path])
    packet = read_json(packet_path); assessment = read_json(assessment_path); facts = read_json(facts_path); report = read_json(report_path); review = read_json(review_path)
    errors: list[str] = []
    current = {"packet_sha256": sha256_file(packet_path), "assessment_sha256": sha256_file(assessment_path), "facts_sha256": sha256_file(facts_path), "check_report_sha256": sha256_file(report_path)}
    for key in ("reviewer", "review_scope", "limitations"):
        if not isinstance(review, dict) or not isinstance(review.get(key), str) or not review[key].strip(): errors.append(f"review-file.{key} must be non-empty")
    if not isinstance(review, dict) or review.get("findings_resolved") is not True: errors.append("review-file.findings_resolved must be true")
    for key in ("assessment_sha256", "facts_sha256", "packet_sha256", "check_report_sha256"):
        if not isinstance(review, dict) or review.get(key) != current[key]: errors.append(f"review-file.{key} is stale or mismatched")
    if not isinstance(report, dict) or report.get("mechanical_pass") is not True or report.get("semantic_pass") is True or report.get("issues") != []: errors.append("check report is not an acceptable mechanical pass")
    if isinstance(report, dict):
        for key in ("packet_sha256", "assessment_sha256", "facts_sha256"):
            if report.get(key) != current[key]: errors.append(f"check report {key} is stale or mismatched")
        expected_report_hash = canonical_hash({k: v for k, v in report.items() if k != "report_sha256"})
        if report.get("report_sha256") != expected_report_hash: errors.append("check report self-hash is invalid")
    receipt = {
        "receipt_version": "ai-usability-rescore-receipt-v1", "reviewer": review.get("reviewer") if isinstance(review, dict) else None,
        "review_scope": review.get("review_scope") if isinstance(review, dict) else None, "findings_resolved": True,
        "assessment_sha256": current["assessment_sha256"], "facts_sha256": current["facts_sha256"], "packet_sha256": current["packet_sha256"], "check_report_sha256": current["check_report_sha256"],
        "limitations": review.get("limitations") if isinstance(review, dict) else None,
        "mechanical_pass": not errors, "semantic_pass": False,
        "content_review_assertion": "Reviewer assertion only; this receipt is not an automatic technical proof of content correctness.",
        "errors": errors,
    }
    write_json(out_path, receipt)
    return 0 if not errors else 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("prepare"); p.add_argument("--packet", type=Path, required=True); p.add_argument("--out", type=Path, required=True)
    p = sub.add_parser("quote"); p.add_argument("--packet", type=Path, required=True); p.add_argument("--event", required=True); p.add_argument("--contains", required=True)
    p = sub.add_parser("check"); p.add_argument("--packet", type=Path, required=True); p.add_argument("--assessment", type=Path, required=True); p.add_argument("--facts", type=Path, required=True); p.add_argument("--out", type=Path, required=True)
    p = sub.add_parser("review"); p.add_argument("--packet", type=Path, required=True); p.add_argument("--assessment", type=Path, required=True); p.add_argument("--facts", type=Path, required=True); p.add_argument("--check-report", type=Path, required=True); p.add_argument("--review-file", type=Path, required=True); p.add_argument("--out", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == "prepare": prepare(args.packet, args.out); return 0
        if args.command == "quote": quote_command(args.packet, args.event, args.contains); return 0
        if args.command == "check": return check_command(args.packet, args.assessment, args.facts, args.out)
        return review_command(args.packet, args.assessment, args.facts, args.check_report, args.review_file, args.out)
    except (GateError, OSError, json.JSONDecodeError) as exc:
        print(f"rescore: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
