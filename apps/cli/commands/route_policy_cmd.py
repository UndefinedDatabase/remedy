"""CLI handlers for the Worker Registry + User-Selectable Route Policy v0 (Steps 1725).

``worker registry-list`` / ``worker registry-show`` expose the replaceable route-policy worker
specs (distinct from the legacy provider-adapter ``worker list``/``worker show``). ``route-policy
show/set/evaluate`` inspect and constrain the per-job route policy. NONE of these execute a worker,
start work, or call a provider/model/Ollama/cloud service — they are metadata + recommendation only.
No raw prompts/secrets/absolute paths in any output.
"""

from __future__ import annotations

import json
import sys
from typing import Any, Callable, TYPE_CHECKING

if TYPE_CHECKING:
    import argparse


# ---------------------------------------------------------------------------
# Worker Registry
# ---------------------------------------------------------------------------


def _cmd_worker_registry_list(args: Any) -> None:
    from packages.orchestration.worker_registry import list_worker_specs, load_worker_registry
    specs = list_worker_specs(load_worker_registry())
    out = {
        "version": 1,
        "worker_count": len(specs),
        "enabled_count": sum(1 for s in specs if s.enabled),
        "user_selectable_count": sum(1 for s in specs if s.user_selectable),
        "workers": [s.to_dict() for s in specs],
    }
    if getattr(args, "json", False):
        print(json.dumps(out, indent=2))
        return
    print(f"Worker Registry: {len(specs)} worker spec(s)")
    for s in specs:
        flag = "+" if s.enabled else "~"
        ph = " [placeholder]" if s.to_dict()["is_placeholder"] else ""
        print(f"  {flag} {s.worker_id} ({s.kind})  cost={s.cost_tier} risk={s.risk_tier}{ph}")


def _cmd_worker_registry_show(args: Any) -> None:
    from packages.orchestration.worker_registry import get_worker_spec, load_worker_registry
    spec = get_worker_spec(str(args.worker_id), load_worker_registry())
    if spec is None:
        print(f"Error: unknown worker_id: {args.worker_id}", file=sys.stderr)
        sys.exit(1)
    data = spec.to_dict()
    if getattr(args, "json", False):
        print(json.dumps(data, indent=2))
        return
    print(f"Worker {data['worker_id']} — {data['label']}")
    print(f"  kind: {data['kind']}  enabled: {data['enabled']}  user_selectable: {data['user_selectable']}")
    print(f"  cost: {data['cost_tier']}  risk: {data['risk_tier']}  execution_mode: {data['execution_mode']}")
    print(f"  placeholder (not executable): {data['is_placeholder']}")
    if data.get("notes"):
        print(f"  notes: {data['notes']}")


# ---------------------------------------------------------------------------
# Route Policy
# ---------------------------------------------------------------------------


def _cmd_worker_registry_integrity(args: Any) -> None:
    from packages.orchestration.worker_registry import worker_registry_integrity
    data = worker_registry_integrity()
    if getattr(args, "json", False):
        print(json.dumps(data, indent=2))
        return
    print(f"Worker registry integrity: passed={data['passed']} "
          f"violations={data['violation_count']} "
          f"workers={data['worker_count']} policies={data['policy_count']}")


def _cmd_route_policy_show(args: Any) -> None:
    from packages.orchestration.worker_registry import export_route_policy_json, load_route_policy
    policy = load_route_policy(str(args.job_id))
    data = export_route_policy_json(policy)
    if getattr(args, "json", False):
        print(json.dumps(data, indent=2))
        return
    print(f"Route policy for {str(args.job_id)[:8]} ({data['policy_id']})")
    print(f"  selected: {data['user_selected_worker_ids']}  preferred: {data['preferred_worker_ids']}")
    print(f"  blocked: {data['blocked_worker_ids']}")
    print(f"  max_cost_tier: {data['max_cost_tier']}  max_risk_tier: {data['max_risk_tier']}")
    print(f"  prefer_local_for_cheap_tasks: {data['prefer_local_for_cheap_tasks']}  "
          f"prefer_ollama_for_cheap_tasks: {data['prefer_ollama_for_cheap_tasks']}")


def _cmd_route_policy_set(args: Any) -> None:
    from packages.orchestration.worker_registry import (
        WorkerCostTier, WorkerRiskTier, export_route_policy_json, get_worker_spec,
        load_route_policy, load_worker_registry, save_route_policy,
    )
    job_id = str(args.job_id)
    policy = load_route_policy(job_id)
    registry = load_worker_registry()

    def _check_worker(wid: str) -> None:
        spec = get_worker_spec(wid, registry)
        if spec is None:
            print(f"Error: unknown worker_id: {wid}", file=sys.stderr)
            sys.exit(1)

    sel = getattr(args, "select_worker", None)
    if sel:
        _check_worker(sel)
        spec = get_worker_spec(sel, registry)
        if spec is not None and not spec.enabled:
            print(f"Error: worker '{sel}' is disabled and cannot be selected", file=sys.stderr)
            sys.exit(1)
        if sel not in policy.user_selected_worker_ids:
            policy.user_selected_worker_ids.append(sel)
    pref = getattr(args, "prefer_worker", None)
    if pref:
        _check_worker(pref)
        if pref not in policy.preferred_worker_ids:
            policy.preferred_worker_ids.append(pref)
    blk = getattr(args, "block_worker", None)
    if blk:
        _check_worker(blk)
        if blk not in policy.blocked_worker_ids:
            policy.blocked_worker_ids.append(blk)

    mct = getattr(args, "max_cost_tier", None)
    if mct:
        valid = {WorkerCostTier.FREE, WorkerCostTier.CHEAP, WorkerCostTier.STANDARD,
                 WorkerCostTier.EXPENSIVE}
        if mct not in valid:
            print(f"Error: invalid --max-cost-tier: {mct}", file=sys.stderr)
            sys.exit(1)
        policy.max_cost_tier = mct
    mrt = getattr(args, "max_risk_tier", None)
    if mrt:
        valid = {WorkerRiskTier.LOW, WorkerRiskTier.MEDIUM, WorkerRiskTier.HIGH}
        if mrt not in valid:
            print(f"Error: invalid --max-risk-tier: {mrt}", file=sys.stderr)
            sys.exit(1)
        policy.max_risk_tier = mrt

    if getattr(args, "prefer_local_for_cheap_tasks", False):
        policy.prefer_local_for_cheap_tasks = True
    if getattr(args, "prefer_ollama_for_cheap_tasks", False):
        policy.prefer_ollama_for_cheap_tasks = True
    if getattr(args, "require_human_approval_for_expensive", False):
        policy.require_human_approval_for_expensive = True

    ok = save_route_policy(policy)
    data = export_route_policy_json(policy)
    data["saved"] = ok
    if getattr(args, "json", False):
        print(json.dumps(data, indent=2))
        return
    print(f"Route policy {'saved' if ok else 'NOT saved'} for {job_id[:8]} ({data['policy_id']})")
    print(f"  selected: {data['user_selected_worker_ids']}  blocked: {data['blocked_worker_ids']}")
    print(f"  max_cost_tier: {data['max_cost_tier']}  max_risk_tier: {data['max_risk_tier']}")


def _cmd_route_policy_evaluate(args: Any) -> None:
    from packages.orchestration.worker_registry import (
        WorkerSelectionRequest, evaluate_worker_selection,
    )
    job_id = str(args.job_id)
    task_type = getattr(args, "task_type", None) or ""
    result = evaluate_worker_selection(
        WorkerSelectionRequest(job_id=job_id, task_type=task_type))
    data = result.to_dict()
    if getattr(args, "json", False):
        print(json.dumps(data, indent=2))
        return
    print(f"Route evaluation for {job_id[:8]} (task={task_type or 'any'})")
    print(f"  recommended: {data['recommended_worker_id'] or '(none)'}")
    print(f"  reason: {data['recommended_reason']}")
    print(f"  requires_human_approval: {data['requires_human_approval']}")
    print(f"  next: {data['next_safe_action']}")


COMMAND_HANDLERS: dict[str, Callable[["argparse.Namespace"], None]] = {
    "worker.registry-list": _cmd_worker_registry_list,
    "worker.registry-show": _cmd_worker_registry_show,
    "worker.registry-integrity": _cmd_worker_registry_integrity,
    "route-policy.show": _cmd_route_policy_show,
    "route-policy.set": _cmd_route_policy_set,
    "route-policy.evaluate": _cmd_route_policy_evaluate,
}
