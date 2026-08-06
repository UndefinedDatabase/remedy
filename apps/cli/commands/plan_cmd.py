"""CLI handlers for the ``plan`` command group (F080 T001/T002).

``remedy plan status`` and ``remedy plan next`` READ the roadmap mirror
and PROPOSE — they never start a job, never write markdown, and never
check a checkbox. The only thing they write is the generated index
under the data root (one-way mirror, see roadmap_index.py).

Rule A5 (ROADMAP.md Part C) decides what they report: an in-progress
``[~]`` line is the active feature and is reported as such; otherwise
the first ``[ ]`` line is next.
"""

from __future__ import annotations

import json
import sys
from typing import Any


def _build(args: Any):
    """Build the index for the requested repo and mirror it under the data root."""
    from packages.orchestration.roadmap_index import build_and_write_index

    repo = getattr(args, "repo", None) or None
    return build_and_write_index(repo)


def _fail_on_grammar(exc) -> None:
    """Grammar is the only hard failure — print file:line violations, exit 2."""
    print("Error: roadmap grammar violations", file=sys.stderr)
    for violation in exc.violations:
        print(f"  {violation}", file=sys.stderr)
    sys.exit(2)


def _milestone_line(index, feature) -> str:
    for milestone in index.milestones:
        if milestone["id"] == feature.milestone:
            return f"{milestone['id']} — {milestone['name']} ({milestone['features']})"
    return feature.milestone or "unassigned"


def _feature_block(index, feature, label: str) -> list[str]:
    from packages.orchestration.roadmap_index import blocker_states

    lines = [f"{label}: {feature.id} — {feature.title}  [{feature.status}]",
             f"  File: {feature.file or '(no feature file)'}",
             f"  Milestone: {_milestone_line(index, feature)}"]
    blockers = blocker_states(index, feature)
    if blockers:
        lines.append("  Blockers:")
        lines.extend(f"    {b['id']} — {b['title'] or 'unknown feature'}  [{b['status']}]"
                     for b in blockers)
    else:
        lines.append("  Blockers: none")
    return lines


def _consistency_lines(index) -> list[str]:
    """Render the report-only consistency findings (T002)."""
    if not index.inconsistencies:
        return ["Consistency: no findings"]
    lines = [f"Consistency: {len(index.inconsistencies)} finding(s) (reported, not fatal)"]
    lines.extend(f"  {c['kind']}: {c['id']} — {c['detail']}" for c in index.inconsistencies)
    return lines


def _cmd_plan_status(args: Any) -> None:
    """Show the active/next roadmap feature, its blockers and its milestone."""
    from packages.orchestration.roadmap_index import (
        RoadmapGrammarError,
        next_feature,
        proposed_feature,
    )

    try:
        index, index_file = _build(args)
    except RoadmapGrammarError as exc:
        _fail_on_grammar(exc)
        return

    feature, reason = proposed_feature(index)
    upcoming = next_feature(index)

    if getattr(args, "json", False):
        from packages.orchestration.roadmap_index import blocker_states
        payload = {
            "reason": reason,
            "feature": feature.as_dict() if feature else None,
            "blockers": blocker_states(index, feature) if feature else [],
            "next_unchecked": upcoming.as_dict() if upcoming else None,
            "feature_count": len(index.features),
            "scheduled_count": len(index.order),
            "inconsistencies": [dict(c) for c in index.inconsistencies],
            "index_file": str(index_file),
            "started": False,
        }
        print(json.dumps(payload, indent=2))
        return

    lines: list[str] = []
    if feature is None:
        lines.append("No open feature — every STATUS line is done or blocked.")
    else:
        label = "Active" if reason == "in_progress" else "Next"
        lines.extend(_feature_block(index, feature, label))
        if reason == "in_progress" and upcoming is not None:
            lines.append(f"Next unchecked: {upcoming.id} — {upcoming.title}")
    lines.append(f"Roadmap: {len(index.features)} features · {len(index.order)} scheduled in STATUS")
    lines.extend(_consistency_lines(index))
    lines.append(f"Mirror: {index_file} (generated, never committed)")
    print("\n".join(lines))


def _cmd_plan_next(args: Any) -> None:
    """Propose the next feature to work on. Proposes — starts nothing."""
    from packages.orchestration.roadmap_index import RoadmapGrammarError, proposed_feature

    try:
        index, index_file = _build(args)
    except RoadmapGrammarError as exc:
        _fail_on_grammar(exc)
        return

    feature, reason = proposed_feature(index)

    if getattr(args, "json", False):
        print(json.dumps({
            "reason": reason,
            "feature": feature.as_dict() if feature else None,
            "file": feature.file if feature else "",
            "index_file": str(index_file),
            "started": False,
        }, indent=2))
        return

    if feature is None:
        print("No open feature — every STATUS line is done or blocked.")
        return

    where = f"docs/roadmap/STATUS.md:{feature.status_line}" if feature.status_line else "not in STATUS.md"
    state = "in progress (Rule A5: the active line)" if reason == "in_progress" else "unchecked (Rule A5: first open line)"
    print("\n".join([
        f"{feature.id} — {feature.title}",
        f"File: {feature.file or '(no feature file)'}",
        f"State: {state} · {where}",
        "Proposal only — nothing was started.",
    ]))


COMMAND_HANDLERS = {
    "plan.status": lambda args: _cmd_plan_status(args),
    "plan.next": lambda args: _cmd_plan_next(args),
}
