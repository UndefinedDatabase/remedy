"""Task plan evidence — structured artifact recording a task decomposition plan.

Deterministic, read-only: no provider calls, no target-repo mutation.

Public API:
    build_task_plan_evidence(goal, step_range, tasks, ...) -> dict
"""
from __future__ import annotations

_DEFAULT_COMPLETION_CRITERIA = [
    "all tasks pass review",
    "all tests pass",
    "no blocked gates",
]


def build_task_plan_evidence(
    goal: str,
    step_range: str,
    tasks: list[dict],
    risks: list[str] | None = None,
    review_strategy: str = "per-task",
    repair_strategy: str = "per-task-up-to-limit",
    completion_criteria: list[str] | None = None,
    source_root: str = "",
) -> dict:
    """Return a structured task plan evidence dict."""
    risk_tags = list(risks) if risks else []
    criteria = list(completion_criteria) if completion_criteria else list(_DEFAULT_COMPLETION_CRITERIA)

    dep_graph: dict[str, list[str]] = {}
    all_files: list[str] = []
    normalised_tasks: list[dict] = []

    for t in tasks:
        tid = t["id"]
        deps = list(t.get("dependencies", []))
        exp_files = list(t.get("expected_files", []))
        exp_tests = list(t.get("expected_tests", []))
        dep_graph[tid] = deps
        all_files.extend(exp_files)
        normalised_tasks.append({
            "id": tid,
            "summary": t.get("summary", ""),
            "dependencies": deps,
            "expected_files": exp_files,
            "expected_tests": exp_tests,
            "risk_tags": [],
        })

    seen: set[str] = set()
    deduped_files: list[str] = []
    for f in all_files:
        if f not in seen:
            seen.add(f)
            deduped_files.append(f)

    return {
        "schema_version": 1,
        "package_goal": goal,
        "step_range": step_range,
        "source_root": source_root,
        "task_count": len(normalised_tasks),
        "tasks": normalised_tasks,
        "task_dependency_graph": dep_graph,
        "expected_changed_areas": deduped_files,
        "risk_tags": risk_tags,
        "review_strategy": review_strategy,
        "repair_strategy": repair_strategy,
        "completion_criteria": criteria,
        "open_risks": list(risk_tags),
    }
