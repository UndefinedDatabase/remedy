"""CLI handlers for `remedy token` and `remedy context-pack` — Token Economy + Context Budget
Optimizer v0 (Step 1765).

`token budget-show/budget-set` inspect/configure a job's token budget profile; `token estimate` and
`token economy-report` produce safe ESTIMATES; `context-pack recommend` recommends a safe, bounded
context pack. ESTIMATES + METADATA only — none execute a worker, call a provider/model/Ollama/cloud
service, or claim real pricing. No raw context/prompts/secrets/absolute paths in any output.
"""

from __future__ import annotations

import json
import sys
from typing import Any, Callable, TYPE_CHECKING

if TYPE_CHECKING:
    import argparse


def _parse_pos_int(raw: Any, label: str) -> int:
    try:
        v = int(raw)
    except (TypeError, ValueError):
        print(f"Error: {label} must be an integer", file=sys.stderr)
        sys.exit(1)
    if v <= 0:
        print(f"Error: {label} must be > 0", file=sys.stderr)
        sys.exit(1)
    return v


def _cmd_token_budget_show(args: Any) -> None:
    from packages.orchestration.token_economy import (
        export_token_budget_profile_json, load_token_budget_profile,
    )
    profile = load_token_budget_profile(str(args.job_id))
    data = export_token_budget_profile_json(profile)
    if getattr(args, "json", False):
        print(json.dumps(data, indent=2))
        return
    print(f"Token budget for {str(args.job_id)[:8]} ({data['profile_id']})")
    print(f"  max_context_tokens: {data['max_context_tokens']}  "
          f"max_generation_tokens: {data['max_generation_tokens']}")
    print(f"  max_total_estimated_tokens: {data['max_total_estimated_tokens']}")
    print(f"  prefer_local_under_tokens: {data['prefer_local_under_tokens']}  "
          f"require_human_approval_over_tokens: {data['require_human_approval_over_tokens']}")


def _cmd_token_budget_set(args: Any) -> None:
    from packages.orchestration.token_economy import (
        export_token_budget_profile_json, load_token_budget_profile, save_token_budget_profile,
    )
    profile = load_token_budget_profile(str(args.job_id))
    if getattr(args, "max_context_tokens", None) is not None:
        profile.max_context_tokens = _parse_pos_int(args.max_context_tokens, "--max-context-tokens")
    if getattr(args, "max_generation_tokens", None) is not None:
        profile.max_generation_tokens = _parse_pos_int(args.max_generation_tokens, "--max-generation-tokens")
    if getattr(args, "max_total_estimated_tokens", None) is not None:
        profile.max_total_estimated_tokens = _parse_pos_int(
            args.max_total_estimated_tokens, "--max-total-estimated-tokens")
    if getattr(args, "prefer_local_under_tokens", None) is not None:
        profile.prefer_local_under_tokens = _parse_pos_int(
            args.prefer_local_under_tokens, "--prefer-local-under-tokens")
    if getattr(args, "require_human_approval_over_tokens", None) is not None:
        profile.require_human_approval_over_tokens = _parse_pos_int(
            args.require_human_approval_over_tokens, "--require-human-approval-over-tokens")
    ok = save_token_budget_profile(profile)
    data = export_token_budget_profile_json(profile)
    data["saved"] = ok
    if getattr(args, "json", False):
        print(json.dumps(data, indent=2))
        return
    print(f"Token budget {'saved' if ok else 'NOT saved'} for {str(args.job_id)[:8]} ({data['profile_id']})")
    print(f"  max_total_estimated_tokens: {data['max_total_estimated_tokens']}  "
          f"prefer_local_under_tokens: {data['prefer_local_under_tokens']}")


def _cmd_token_estimate(args: Any) -> None:
    from packages.orchestration.token_economy import (
        estimate_context_budget, export_context_budget_estimate_json,
    )
    est = estimate_context_budget(
        str(args.job_id), task_id=getattr(args, "task_id", None) or "",
        route_id=getattr(args, "route_id", None) or "")
    data = export_context_budget_estimate_json(est)
    if getattr(args, "json", False):
        print(json.dumps(data, indent=2))
        return
    print(f"Token estimate for {str(args.job_id)[:8]} (estimate, not verified)")
    print(f"  input~{data['estimated_input_tokens']}  output~{data['estimated_output_tokens']}  "
          f"total~{data['estimated_total_tokens']}  confidence={data['confidence']}")
    if data["warnings"]:
        print(f"  warnings: {', '.join(data['warnings'])}")


def _cmd_token_economy_report(args: Any) -> None:
    from packages.orchestration.token_economy import token_economy_report
    data = token_economy_report(
        str(args.job_id), task_id=getattr(args, "task_id", None) or "",
        route_id=getattr(args, "route_id", None) or "")
    if getattr(args, "json", False):
        print(json.dumps(data, indent=2))
        return
    dec = data["decision"]
    print(f"Token economy report for {str(args.job_id)[:8]} (estimate)")
    print(f"  recommended_worker: {dec['recommended_worker_id'] or '(none)'}  "
          f"approval: {dec['requires_human_approval']}")
    print(f"  token_band: {dec['estimated_token_band']}  budget_status: {dec['budget_status']}  "
          f"pack: {dec['context_pack_kind']}")


def _cmd_context_pack_recommend(args: Any) -> None:
    from packages.orchestration.token_economy import (
        export_context_pack_recommendation_json, recommend_context_pack,
    )
    rec = recommend_context_pack(
        str(args.job_id), task_id=getattr(args, "task_id", None) or "",
        route_id=getattr(args, "route_id", None) or "")
    data = export_context_pack_recommendation_json(rec)
    if getattr(args, "json", False):
        print(json.dumps(data, indent=2))
        return
    print(f"Context pack recommendation for {str(args.job_id)[:8]}")
    print(f"  kind: {data['recommended_pack_kind']}  included: {len(data['included_context_refs'])}  "
          f"excluded: {len(data['excluded_context_refs'])}")
    print(f"  estimated_token_savings: {data['estimated_token_savings'].get('saved_tokens')} "
          f"(band={data['estimated_token_savings'].get('band')})")
    print(f"  memory_candidates: {len(data['memory_candidates'])} (suggestions only, not persisted)")
    print(f"  next: {data['next_safe_action']}")


COMMAND_HANDLERS: dict[str, Callable[["argparse.Namespace"], None]] = {
    "token.budget-show": _cmd_token_budget_show,
    "token.budget-set": _cmd_token_budget_set,
    "token.estimate": _cmd_token_estimate,
    "token.economy-report": _cmd_token_economy_report,
    "context-pack.recommend": _cmd_context_pack_recommend,
}
