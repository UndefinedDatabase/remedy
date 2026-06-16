"""CLI handlers for the Token-Aware Repair Loop v1/v2 (Step 1930).

`item-create-from-failure/review`, `policy-set`, and `evaluate` write safe metadata; everything else is
read-only. No provider/model/worker execution, no apply/approval, no arbitrary command execution, no raw
logs/candidates/diffs. JSON-safe; no tracebacks.
"""

from __future__ import annotations

import json
import sys
from collections.abc import Callable
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    import argparse


def _print(data: Any, args: Any, line: str) -> None:
    if getattr(args, "json", False):
        print(json.dumps(data, indent=2))
    else:
        print(line)


def _cmd_item_create_from_failure(args: Any) -> None:
    from packages.orchestration.repair_loop_v2 import (
        create_repair_item_from_failure_artifact,
        export_repair_work_item_json,
    )
    item = create_repair_item_from_failure_artifact(
        str(args.job_id), str(args.failure_artifact_id),
        test_run_id=getattr(args, "test_run_id", "") or "")
    if item is None:
        print("Error: failure artifact not found", file=sys.stderr)
        sys.exit(1)
    d = export_repair_work_item_json(item)
    _print(d, args, f"Repair item {d['repair_id']} ({d['status']}) from failure {str(args.failure_artifact_id)[:8]}")


def _cmd_item_create_from_review(args: Any) -> None:
    from packages.orchestration.repair_loop_v2 import (
        create_repair_item_from_review_finding,
        export_repair_work_item_json,
    )
    item = create_repair_item_from_review_finding(str(args.job_id), str(args.finding_id))
    if item is None:
        print("Error: finding not found, not open, or below required severity (Done is not Resolved)",
              file=sys.stderr)
        sys.exit(1)
    d = export_repair_work_item_json(item)
    _print(d, args, f"Repair item {d['repair_id']} ({d['status']}) from finding {args.finding_id}")


def _cmd_item_show(args: Any) -> None:
    from packages.orchestration.repair_loop_v2 import (
        export_repair_work_item_json,
        load_repair_work_item,
    )
    item = load_repair_work_item(str(args.repair_id))
    if item is None:
        print("Error: repair item not found", file=sys.stderr)
        sys.exit(1)
    d = export_repair_work_item_json(item)
    _print(d, args, f"Repair item {d['repair_id']}: status={d['status']} source={d['source_type']}")


def _cmd_item_list(args: Any) -> None:
    from packages.orchestration.repair_loop_v2 import list_repair_work_items
    items = list_repair_work_items(job_id=str(args.job_id))
    out = {"job_id": str(args.job_id), "count": len(items),
           "items": [{"repair_id": i.get("repair_id"), "status": i.get("status"),
                      "source_type": i.get("source_type")} for i in items]}
    _print(out, args, f"Repair items for {str(args.job_id)[:8]}: {len(items)}")


def _cmd_context_pack(args: Any) -> None:
    from packages.orchestration.repair_loop_v2 import build_repair_context_pack
    pack = build_repair_context_pack(str(args.repair_id))
    if pack.get("status") == "blocked":
        print(f"Error: {pack.get('blocker', 'context unavailable')}", file=sys.stderr)
        sys.exit(1)
    _print(pack, args, f"Context pack {pack.get('context_pack_id')}: status={pack.get('status')} "
                       f"rec={pack.get('recommendation')}")


def _cmd_route_recommend(args: Any) -> None:
    from packages.orchestration.repair_loop_v2 import recommend_repair_route
    rec = recommend_repair_route(str(args.repair_id))
    if rec.get("status") == "blocked":
        print(f"Error: {rec.get('blocker', 'route unavailable')}", file=sys.stderr)
        sys.exit(1)
    _print(rec, args, f"Route: {rec.get('recommended_route_kind')} "
                      f"approval={rec.get('requires_human_approval')}")


def _cmd_evaluate(args: Any) -> None:
    from packages.orchestration.repair_loop_v2 import (
        evaluate_repair_loop,
        export_repair_evaluation_json,
    )
    ev = evaluate_repair_loop(str(args.repair_id))
    d = export_repair_evaluation_json(ev)
    _print(d, args, f"Repair {d['repair_id']}: status={d['status']} satisfied={d['satisfied']}")


def _cmd_attempts(args: Any) -> None:
    from packages.orchestration.repair_loop_v2 import list_repair_attempts
    attempts = list_repair_attempts(str(args.repair_id))
    out = {"repair_id": str(args.repair_id), "count": len(attempts),
           "attempts": [{"attempt_id": a.get("attempt_id"), "attempt_index": a.get("attempt_index"),
                         "route_id": a.get("route_id"), "retest_status": a.get("retest_status")}
                        for a in attempts]}
    _print(out, args, f"Repair attempts for {str(args.repair_id)[:8]}: {len(attempts)}")


def _cmd_policy_show(args: Any) -> None:
    from packages.orchestration.repair_loop_v2 import (
        export_repair_policy_json,
        load_repair_loop_policy,
    )
    d = export_repair_policy_json(load_repair_loop_policy(str(args.job_id)))
    _print(d, args, f"Repair policy: max_attempts={d['max_attempts']} max_retests={d['max_retests']}")


def _parse_int(val: Any, default: int) -> int:
    try:
        return int(str(val))
    except (TypeError, ValueError):
        return default


def _parse_bool(val: Any, default: bool) -> bool:
    if val is None:
        return default
    return str(val).strip().lower() in ("1", "true", "yes", "on")


def _cmd_policy_set(args: Any) -> None:
    from packages.orchestration.repair_loop_v2 import (
        export_repair_policy_json,
        load_repair_loop_policy,
        save_repair_loop_policy,
    )
    policy = load_repair_loop_policy(str(args.job_id))
    if getattr(args, "max_attempts", None) is not None:
        policy.max_attempts = _parse_int(args.max_attempts, policy.max_attempts)
    if getattr(args, "max_retests", None) is not None:
        policy.max_retests = _parse_int(args.max_retests, policy.max_retests)
    if getattr(args, "max_tokens_per_attempt", None) is not None:
        policy.max_estimated_tokens_per_attempt = _parse_int(
            args.max_tokens_per_attempt, policy.max_estimated_tokens_per_attempt)
    if getattr(args, "require_reviewer_pass", None) is not None:
        policy.require_reviewer_pass = _parse_bool(args.require_reviewer_pass, policy.require_reviewer_pass)
    if getattr(args, "require_tests_green", None) is not None:
        policy.require_tests_green = _parse_bool(args.require_tests_green, policy.require_tests_green)
    if getattr(args, "require_apply_proof", None) is not None:
        policy.require_apply_proof = _parse_bool(args.require_apply_proof, policy.require_apply_proof)
    if getattr(args, "prefer_local", None) is not None:
        policy.prefer_local_for_small_repairs = _parse_bool(
            args.prefer_local, policy.prefer_local_for_small_repairs)
    save_repair_loop_policy(policy)
    d = export_repair_policy_json(policy)
    _print(d, args, f"Repair policy updated: max_attempts={d['max_attempts']} "
                    f"require_reviewer_pass={d['require_reviewer_pass']}")


def _cmd_integrity(args: Any) -> None:
    from packages.orchestration.repair_loop_v2 import repair_loop_integrity
    data = repair_loop_integrity()
    _print(data, args, f"Repair loop integrity: passed={data['passed']} "
                       f"violations={data['violation_count']}")


COMMAND_HANDLERS: dict[str, Callable[[argparse.Namespace], None]] = {
    "repair.item-create-from-failure": _cmd_item_create_from_failure,
    "repair.item-create-from-review": _cmd_item_create_from_review,
    "repair.item-show": _cmd_item_show,
    "repair.item-list": _cmd_item_list,
    "repair.context-pack": _cmd_context_pack,
    "repair.route-recommend": _cmd_route_recommend,
    "repair.evaluate": _cmd_evaluate,
    "repair.attempts": _cmd_attempts,
    "repair.policy-show": _cmd_policy_show,
    "repair.policy-set": _cmd_policy_set,
    "repair.integrity": _cmd_integrity,
}
