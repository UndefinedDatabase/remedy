"""`remedy job context <id> --task <tid>` — F107 T004 part 2a.

The FIRST caller of ``packages.orchestration.context_compiler`` outside its own
tests: it compiles one task's context and renders what that task would receive
and what was left out, without sending anything to a provider and without
writing a byte to disk.

The fenced scope compiled here is exactly the task's
``inputs["flight"]["files_hint"]``. Remedy deliberately does NOT consult the
job's scope-fence globs (``remedy job fences``, F017) in this view — merging
fence allow-globs into the compiled scope is out of scope for this round, so a
reader looking for that behaviour finds this sentence instead of guessing that
it silently happened.

Exit codes:
* 0 — compiled and rendered;
* 1 — unknown job;
* 2 — the job has no usable ``target_repo``;
* 3 — the task could not be resolved (unknown, ambiguous, or several tasks and
      no ``--task``). A task is never guessed.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from typing import Any

#: Directories the rglob fallback never lists. A real git checkout excludes
#: these through the index anyway, so the fallback only has to imitate it.
_FALLBACK_PRUNED_DIRS = (".git", "__pycache__", "node_modules", ".venv", "dist")

_SOURCE_GIT = "git ls-files"
_SOURCE_RGLOB = "filesystem walk"


# WHY this walk lives in the CLI and not in the compiler: `compile_task_context`
# TAKES the candidate listing as an argument and deliberately never walks a tree
# itself (its docstring in packages/orchestration/context_compiler.py says so),
# which keeps the compiler pure and testable — so producing the listing is the
# caller's job, and this is the first caller. Two branches, and the returned
# source names WHICH ONE RAN so the rendered view never has to be guessed at:
# `git ls-files -z` when root is a git checkout (it already honours .gitignore
# and the index), and an rglob over files when it is not or when git fails.
def _repo_candidate_paths_with_source(root: Path) -> tuple[list[str], str]:
    """The candidate listing plus the name of the branch that produced it."""
    try:
        proc = subprocess.run(
            ["git", "ls-files", "-z"],
            cwd=str(root),
            capture_output=True,
            timeout=60,
            check=False,
        )
    except (OSError, subprocess.SubprocessError):
        proc = None
    if proc is not None and proc.returncode == 0:
        listed = proc.stdout.decode("utf-8", errors="replace").split("\0")
        return sorted({rel for rel in listed if rel}), _SOURCE_GIT

    walked: set[str] = set()
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(root)
        if any(part in _FALLBACK_PRUNED_DIRS for part in rel.parts):
            continue
        walked.add(rel.as_posix())
    return sorted(walked), _SOURCE_RGLOB


def list_repo_candidate_paths(root: Path) -> list[str]:
    """Every candidate file under ``root``, repo-relative, sorted and deduplicated.

    Deterministic by construction on both branches, because the compiled view
    is only reproducible if the candidate listing is.
    """
    return _repo_candidate_paths_with_source(root)[0]


def _task_flight_inputs(task: Any) -> dict:
    """The task's flight-plan block, or an empty dict when it carries none."""
    inputs = getattr(task, "inputs", None)
    flight = inputs.get("flight") if isinstance(inputs, dict) else None
    return flight if isinstance(flight, dict) else {}


def _task_planned_id(task: Any) -> str:
    """The planned id (`T001`) `map_flight_plan_to_tasks` wrote, or ""."""
    return str(_task_flight_inputs(task).get("planned_id") or "")


def _task_files_hint(task: Any) -> list[str]:
    """The task's declared write scope. An absent hint is an EMPTY scope, which
    is a real answer this command renders — not an error."""
    hint = _task_flight_inputs(task).get("files_hint")
    return [str(entry) for entry in hint] if isinstance(hint, list) else []


def _task_label(task: Any) -> str:
    """How one task is named in an error listing: planned id when it has one,
    otherwise the first 8 hex of its UUID."""
    planned = _task_planned_id(task)
    return planned if planned else str(task.id)[:8]


def resolve_task_for_context(task_ref: str | None, tasks: list) -> tuple[Any, str]:
    """Resolve ``--task`` against a job's tasks. Returns ``(task, "")`` or
    ``(None, error)``.

    Planned id (`T001`) FIRST, then a prefix of the task UUID. An ambiguous
    prefix and an unknown reference are both errors: this function never picks
    a task the caller did not unambiguously name.
    """
    if not tasks:
        return None, "job has no tasks to compile context for"

    ref = (task_ref or "").strip()
    if not ref:
        if len(tasks) == 1:
            return tasks[0], ""
        listed = ", ".join(_task_label(task) for task in tasks)
        return None, (
            f"job has {len(tasks)} tasks — name one with --task: {listed}"
        )

    by_planned = [task for task in tasks if _task_planned_id(task) == ref]
    if len(by_planned) == 1:
        return by_planned[0], ""
    if len(by_planned) > 1:
        return None, (
            f"--task {ref!r} matches {len(by_planned)} tasks by planned id"
        )

    lowered = ref.lower()
    by_prefix = [task for task in tasks if str(task.id).startswith(lowered)]
    if len(by_prefix) == 1:
        return by_prefix[0], ""
    if len(by_prefix) > 1:
        return None, (
            f"--task {ref!r} is an ambiguous task id prefix matching "
            f"{len(by_prefix)} tasks"
        )
    return None, f"no task matches --task {ref!r}"


def _included_json(compiled: Any) -> list[dict]:
    """The included files as JSON-ready dicts, straight off ``SelectedFile``."""
    return [
        {
            "path": selected.rel_path,
            "tier": selected.tier,
            "rendering": selected.rendering,
            "estimated_tokens": selected.estimated_tokens,
        }
        for selected in compiled.included
    ]


def _print_text_view(result: dict) -> None:
    """The text view. Every value printed here also appears in ``--json``."""
    print(
        f"Task context for job {result['job_id'][:8]} "
        f"task {result['task_label']} ({result['task_id'][:8]})"
    )
    fenced = result["fenced_paths"]
    if fenced:
        print(f"  Fenced paths ({len(fenced)}):")
        for rel_path in fenced:
            print(f"    {rel_path}")
    else:
        print("  Fenced paths (0): the task declares no files_hint")
    print(f"  Candidates: {result['candidate_count']} ({result['candidate_source']})")
    budget = (
        f"  Budget: {result['estimated_tokens']} / {result['budget_tokens']} tokens"
    )
    if result["over_budget"]:
        budget += " (OVER BUDGET)"
    print(budget)

    included = result["included"]
    print(f"  Included ({len(included)}):")
    if not included:
        print("    none")
    last_tier = None
    for entry in included:
        if entry["tier"] != last_tier:
            print(f"    Tier {entry['tier']}:")
            last_tier = entry["tier"]
        print(
            f"      {entry['path']}  {entry['rendering']}  "
            f"{entry['estimated_tokens']} tokens"
        )

    omissions = result["omissions"]
    print(f"  Omissions ({len(omissions)}):")
    if not omissions:
        print("    none")
    for entry in omissions:
        print(
            f"    {entry['path']}  tier {entry['tier']}  "
            f"{entry['reason']}  {entry['outcome']}"
        )


def _cmd_job_context(
    job_id_str: str,
    *,
    task_ref: str | None = None,
    json_output: bool = False,
) -> None:
    """Compile and render one task's context (F107 T004 part 2a). READ-ONLY."""
    import json as _json

    from packages.orchestration.context_compiler import (
        compile_task_context,
        export_omitted_context_json,
    )
    from packages.orchestration.data_paths import resolve_job_id
    from packages.orchestration.storage import JobNotFoundError, load_job

    try:
        job = load_job(resolve_job_id(job_id_str))
    except JobNotFoundError:
        print(f"Job not found: {job_id_str}", file=sys.stderr)
        sys.exit(1)

    repo_str = job.metadata.get("target_repo", "") or ""
    if not repo_str:
        print(f"Job {job_id_str[:8]} has no target_repo attached", file=sys.stderr)
        sys.exit(2)
    repo_root = Path(repo_str)
    if not repo_root.is_dir():
        print(f"Target repo does not exist: {repo_str}", file=sys.stderr)
        sys.exit(2)

    task, error = resolve_task_for_context(task_ref, list(job.tasks))
    if task is None:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(3)

    fenced_paths = _task_files_hint(task)
    candidates, candidate_source = _repo_candidate_paths_with_source(repo_root)
    compiled = compile_task_context(repo_root, fenced_paths, candidates)

    result = {
        "job_id": str(job.id),
        "task_id": str(task.id),
        "task_label": _task_label(task),
        "fenced_paths": fenced_paths,
        "candidate_count": len(candidates),
        "candidate_source": candidate_source,
        "estimated_tokens": compiled.estimated_tokens,
        "budget_tokens": compiled.budget_tokens,
        "over_budget": compiled.over_budget,
        "line_cap": compiled.line_cap,
        "included": _included_json(compiled),
        "omissions": export_omitted_context_json(compiled),
    }

    if json_output:
        print(_json.dumps(result, indent=2))
    else:
        _print_text_view(result)


COMMAND_HANDLERS = {
    "job.context": lambda args: _cmd_job_context(
        getattr(args, "job_id", "") or "",
        task_ref=getattr(args, "task", None),
        json_output=bool(getattr(args, "json", False)),
    ),
}
