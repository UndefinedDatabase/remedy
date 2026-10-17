"""The versioned scale matrix: one order per case, over a disposable repository, through `remedy do`.

`run_matrix` walks each case with the counting fake planner (`scale_harness`), the fake builder and
reviewer, and records what the walk did: the lane it chose, jobs, tasks, planner calls by schema,
builder and reviewer calls, wall time, the steps' outcomes and the order's budget use. The pytest
file `tests/cli/test_do_scale_matrix.py` asserts the expectations below; the same module runs on any
checkout for a before/after table:

    PYTHONPATH=<checkout>:<dir holding tests/orchestration/scale_*.py> \
        python3 -m tests.orchestration.scale_matrix --out table.json

Edge cases appear in English and German. Fixtures hold no host path: every repository is created
under the directory the caller passes in.
"""
from __future__ import annotations

import argparse
import contextlib
import io
import json
import os
import re
import tempfile
import time
from pathlib import Path
from typing import Any

from tests.orchestration.scale_harness import (
    FakePlannerService,
    commit_repository,
    filler_files,
)

MATRIX_VERSION = 1

README = {"README.md": "# Project\n\nA project.\n"}
PY_PROJECT = {"src/add.py": "def add(a, b):\n    return a - b\n",
              "tests/test_add.py": "from src.add import add\n\n\ndef test_add():\n    assert add(1, 1) == 2\n"}
POLYGLOT = {
    "py/app.py": "def f():\n    return 1\n", "py/pyproject.toml": "[project]\nname='p'\n",
    "web/index.ts": "export const f = () => 1;\n", "web/package.json": "{}\n",
    "go/calc/calc.go": "package calc\n\nfunc Sum(n int) int { return n }\n", "go/go.mod": "module x\n",
}
MONOREPO = {
    "packages/schema/user.ts": "export type User = { id: string };\n",
    "packages/web/profile.ts": "import { User } from '../schema/user';\n",
    "packages/api/users.ts": "import { User } from '../schema/user';\n",
    "package.json": "{\"workspaces\": [\"packages/*\"]}\n",
}

#: Each case: id, size class, files, order, flags and the expectations the new code must meet.
CASES: list[dict[str, Any]] = [
    {"id": "tiny-readme", "klass": "tiny", "files": README,
     "order": "Add a usage section to README.md.",
     "expect": {"lane": "bounded", "planner_calls": 0, "jobs": 1, "tasks": 1}},
    {"id": "small-typo-plain", "klass": "small", "files": {**README, **filler_files(40)},
     "order": "Fix the typo in README.md",
     "expect": {"lane": "bounded", "planner_calls": 0, "jobs": 1, "tasks": 1}},
    {"id": "small-typo-structured", "klass": "small", "files": {**README, **filler_files(40)},
     "order": "Task:\n- Fix the typo in README.md;\n- run npm test",
     "expect": {"lane": "bounded", "planner_calls": 0, "jobs": 1, "tasks": 1}},
    {"id": "small-typo-german", "klass": "small", "files": {**README, **filler_files(40)},
     "order": "Korrigiere den Tippfehler in README.md. Ändere keine anderen Dateien. Führe npm test aus.",
     "expect": {"lane": "bounded", "planner_calls": 0, "jobs": 1, "tasks": 1}},
    {"id": "small-typo-no-suffix", "klass": "small", "files": {**README, **filler_files(40)},
     "order": "Fix the typo in the readme",
     "expect": {"lane": "bounded", "planner_calls": 0, "jobs": 1, "tasks": 1}},
    {"id": "small-bug-and-regression-test", "klass": "small", "files": {**PY_PROJECT, **filler_files(30)},
     "order": "Fix the off-by-one bug in src/add.py and add a regression test.",
     "expect": {"lane": "bounded", "planner_calls": 0, "jobs": 1, "tasks": 1, "with_tests": True}},
    {"id": "medium-api-endpoint", "klass": "medium",
     "files": {"src/api/routes.py": "routes = []\n", "src/api/app.py": "app = None\n",
               "tests/test_api.py": "def test_ok():\n    pass\n", **filler_files(300)},
     "order": "Add a GET /health endpoint in src/api/routes.py, register it in src/api/app.py and "
              "extend tests/test_api.py.",
     "expect": {"lane": "full", "no_check_only_job": True, "max_planner_calls": 7}},
    {"id": "large-readme-edit", "klass": "large", "files": {**README, **filler_files(10_000, per_dir=200)},
     "order": "Fix the typo in README.md",
     "expect": {"lane": "bounded", "planner_calls": 0, "jobs": 1, "tasks": 1}},
    {"id": "large-one-file-auth-migration", "klass": "large",
     "files": {"src/auth.ts": "export {}\n", **filler_files(10_000, per_dir=200)},
     "order": "Migrate the password hashing in src/auth.ts from md5 to argon2.",
     "expect": {"lane": "full", "never_tiny": True, "max_planner_calls": 7}},
    {"id": "polyglot-go-fix", "klass": "polyglot", "files": POLYGLOT,
     "order": "Fix the off-by-one in go/calc/calc.go",
     "expect": {"lane": "bounded", "planner_calls": 0, "jobs": 1, "tasks": 1}},
    {"id": "monorepo-schema-change", "klass": "monorepo", "files": MONOREPO,
     "order": "Change the user schema in packages/schema/user.ts and update the consumers in "
              "packages/web/profile.ts and packages/api/users.ts.",
     "expect": {"lane": "full", "no_check_only_job": True, "max_planner_calls": 7}},
    {"id": "ambiguous-vague-target", "klass": "ambiguous", "files": {**PY_PROJECT, **README},
     "order": "Fix the bug.", "flags": [],
     "expect": {"lane": "full", "run_needs_approval": True}},
    {"id": "ambiguous-bare-readme", "klass": "ambiguous",
     "files": {"src/a.py": "x = 1\n", "docs/README.md": "# d\n", "web/README.md": "# w\n"},
     "order": "Fix the typo in README.md.",
     "expect": {"lane": "hold", "jobs": 0, "planner_calls": 0}},
    {"id": "wrong-path-root-readme", "klass": "wrong-path", "files": {**README, "docs/README.md": "# d\n"},
     "order": "Change only README.md: fix the typo.",
     "expect": {"lane": "bounded", "deliverable": "README.md", "planner_calls": 0, "jobs": 1, "tasks": 1}},
    {"id": "deliverable-report-file", "klass": "deliverable", "files": {**README, "package.json": "{}\n"},
     "order": "Write a report of the npm test results to TEST_REPORT.md. Change no other files.",
     "expect": {"lane": "bounded", "deliverable": "TEST_REPORT.md", "jobs": 1, "tasks": 1}},
    {"id": "failure-planner-timeout", "klass": "failure", "files": {**PY_PROJECT, **README},
     "order": "Improve error handling everywhere in the project.", "planner_error": "TimeoutError",
     "expect": {"lane": "full", "honest_failure": True}},
]

_LANE = re.compile(r"lane: (\w+)")


def _run_case(case: dict[str, Any], root: Path) -> dict[str, Any]:
    import pytest

    from apps.cli.grouped import main
    from packages.orchestration.pingpong_provider import FakeProvider

    repo = commit_repository(root / case["id"] / "work", case["files"])
    builds = {"builder": 0, "reviewer": 0}
    with pytest.MonkeyPatch.context() as patch:
        patch.setenv("REMEDY_DATA_DIR", str(root / case["id"] / "data"))
        patch.chdir(repo)
        planner = FakePlannerService(
            target=next(iter(case["files"])),
            error=TimeoutError("planner timed out") if case.get("planner_error") else None)
        planner.install(patch)
        for method, name in (("build", "builder"), ("review", "reviewer")):
            original = getattr(FakeProvider, method)

            def counted(self, *args, _original=original, _name=name, **kwargs):
                builds[_name] += 1
                return _original(self, *args, **kwargs)
            patch.setattr(FakeProvider, method, counted)
        argv = ["do", case["order"], "--repo", ".", "--builder-provider", "fake",
                "--reviewer-provider", "fake", "--json", "--no-ui", *case.get("flags", ["--run-unattended"])]
        out, began = io.StringIO(), time.monotonic()
        with contextlib.redirect_stdout(out), contextlib.suppress(SystemExit):
            main(argv)
        elapsed = time.monotonic() - began
        data = json.loads(out.getvalue())
        from packages.orchestration.pingpong_job import load_job_plan
        jobs = [job for job in (load_job_plan(j) for j in data.get("job_ids", [])) if job is not None]
    steps = {s["name"]: s for s in data.get("steps", [])}
    plan_detail = steps.get("plan", {}).get("detail", "")
    study_detail = steps.get("study", {}).get("detail", "")
    lane = ("hold" if steps.get("study", {}).get("status") == "stopped" and "nothing was planned" in study_detail
            else (_LANE.search(plan_detail) or [None, "?"])[1])
    tasks = [t for job in jobs for t in job.tasks]
    return {
        "id": case["id"], "klass": case["klass"], "files": len(case["files"]), "lane": lane,
        "shape": data.get("shape"), "jobs": len(jobs), "tasks": len(tasks),
        "deliverables": [t.inputs.get("deliverable") for t in tasks],
        "task_types": sorted({str(t.inputs.get("task_type")) for t in tasks}),
        "with_tests": any(t.inputs.get("with_tests") for t in tasks),
        "planner_calls": planner.count(), "planner_by_schema": planner.by_schema(),
        "builder_calls": builds["builder"], "reviewer_calls": builds["reviewer"],
        "elapsed_s": round(elapsed, 2),
        "steps": {name: step["status"] for name, step in steps.items()},
        "failed_detail": next((s["detail"][:160] for s in data.get("steps", []) if s["status"] == "failed"),
                              str(data.get("message") or "")[:160]),
        "run_detail": steps.get("run", {}).get("detail", "")[:160],
        "order_budget_calls": (data.get("order_budget") or {}).get("planner_calls"),
        "rationale": plan_detail.split("lane: ", 1)[-1].split("; no contract")[0][:200] if plan_detail else study_detail[:200],
    }


def run_matrix(root: Path, only: list[str] | None = None) -> list[dict[str, Any]]:
    """Run the cases (all, or those named in *only*) under *root* and return one record each."""
    os.environ.setdefault("GIT_CONFIG_GLOBAL", os.devnull)
    return [_run_case(case, root) for case in CASES if not only or case["id"] in only]


def check_expectations(case: dict[str, Any], record: dict[str, Any]) -> list[str]:
    """What the record misses of the case's expectations, one sentence each (empty: met)."""
    expect, problems = case["expect"], []
    for key in ("lane", "planner_calls", "jobs", "tasks"):
        if key in expect and record[key] != expect[key]:
            problems.append(f"{key}: expected {expect[key]!r}, got {record[key]!r}")
    if "max_planner_calls" in expect and record["planner_calls"] > expect["max_planner_calls"]:
        problems.append(f"planner_calls: {record['planner_calls']} is over {expect['max_planner_calls']}")
    if "deliverable" in expect and record["deliverables"] != [expect["deliverable"]]:
        problems.append(f"deliverables: expected [{expect['deliverable']!r}], got {record['deliverables']!r}")
    if expect.get("with_tests") and not record["with_tests"]:
        problems.append("the requested test was not kept on the task")
    if expect.get("no_check_only_job") and "deliverable_check" in record["task_types"]:
        problems.append("a check-only task was planned")
    if expect.get("never_tiny") and record["lane"] == "bounded":
        problems.append("a high-risk one-file order took the bounded lane")
    if expect.get("run_needs_approval") and record["steps"].get("run") != "stopped":
        problems.append("an ambiguous order ran without approval")
    if expect.get("honest_failure") and record["steps"].get("shape") != "failed":
        problems.append("a failing planner did not end the walk as failed")
    return problems


def format_table(records: list[dict[str, Any]]) -> str:
    head = "| case | class | files | lane | jobs | tasks | planner calls | builder | reviewer | s | run |"
    rows = [head, "|" + "---|" * 11]
    for r in records:
        rows.append(f"| {r['id']} | {r['klass']} | {r['files']} | {r['lane']} | {r['jobs']} | {r['tasks']} | "
                    f"{r['planner_calls']} {r['planner_by_schema'] or ''} | {r['builder_calls']} | "
                    f"{r['reviewer_calls']} | {r['elapsed_s']} | {r['steps'].get('run', '-')} |")
    return "\n".join(rows)


def main_cli() -> None:
    parser = argparse.ArgumentParser(description="Run the scale matrix and print its table.")
    parser.add_argument("--out", help="write the records as JSON here")
    parser.add_argument("--only", nargs="*", help="case ids")
    args = parser.parse_args()
    with tempfile.TemporaryDirectory(prefix="scale-matrix-") as tmp:
        records = run_matrix(Path(tmp), args.only)
    print(format_table(records))
    if args.out:
        Path(args.out).write_text(json.dumps({"matrix_version": MATRIX_VERSION, "records": records}, indent=1))


if __name__ == "__main__":
    main_cli()
