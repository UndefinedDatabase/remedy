"""F042 R1 C6 — the round's mutation tool: red-proofs for S1 to S5 (DECISION F042 D1).

Takes a worktree path (``sys.argv[1]``). For each mutation below it edits the
named production file INSIDE that worktree, asserting its FROM text occurs
exactly once there, runs the reviewer's named test file in that worktree
(cwd = the worktree, PYTHONPATH prefixed with the worktree's own root), then
restores the original bytes and checks the restore is byte-identical. It runs
an unmutated control of every test file the mutations name, first and last,
and ends with one final line stating whether every mutation was caught and
every restore was clean.

Usage: ``python3 -B .agent/authored/f042-r1-mutations.py <worktree-path>``
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

COCKPIT_PROD = "packages/orchestration/project_cockpit.py"
UI_SERVER_PROD = "packages/orchestration/ui_server.py"
COCKPIT_TEST = "tests/orchestration/test_project_cockpit.py"
ROUTES_TEST = "tests/ui_server/test_projects_route.py"

CONTROL_TEST_FILES = [COCKPIT_TEST, ROUTES_TEST]

MUTATIONS = [
    {
        "label": "m1 a recorded folder counts as reachable without the directory check",
        "prod": COCKPIT_PROD,
        "test": COCKPIT_TEST,
        "from": "    reachable = Path(repo).is_dir()\n",
        "to": "    reachable = True\n",
    },
    {
        "label": "m2 the summary's scope is built with all_projects=True",
        "prod": COCKPIT_PROD,
        "test": COCKPIT_TEST,
        "from": 'all_projects=False, source="cockpit")',
        "to": 'all_projects=True, source="cockpit")',
    },
    {
        "label": "m3 an unmeasured call no longer makes the basis lower_bound",
        "prod": COCKPIT_PROD,
        "test": COCKPIT_TEST,
        "from": "elif total_row.unmeasured_calls > 0:",
        "to": "elif False:",
    },
    {
        "label": "m4 the cost query loses its until bound",
        "prod": COCKPIT_PROD,
        "test": COCKPIT_TEST,
        "from": "report = query_cost(project_id=project.id, since=since, until=until)",
        "to": "report = query_cost(project_id=project.id, since=since)",
    },
    {
        "label": "m5 the decision loop skips every job job_is_terminal calls terminal",
        "prod": COCKPIT_PROD,
        "test": COCKPIT_TEST,
        "from": (
            "    for job in jobs:\n"
            "        try:\n"
            "            events = load_run_events(resolve_data_root(), str(job.job_id))"
        ),
        "to": (
            "    for job in jobs:\n"
            "        if job_is_terminal(job.state):\n"
            "            continue\n"
            "        try:\n"
            "            events = load_run_events(resolve_data_root(), str(job.job_id))"
        ),
    },
    {
        "label": "m6 the last result is taken from the oldest scoped job",
        "prod": COCKPIT_PROD,
        "test": COCKPIT_TEST,
        "from": "newest = jobs[0]",
        "to": "newest = jobs[-1]",
    },
    {
        "label": "m7 the default project is resolved from the folder alone, so REMEDY_PROJECT is ignored",
        "prod": COCKPIT_PROD,
        "test": COCKPIT_TEST,
        "from": "        project, source = select_project(None, cwd)\n",
        "to": (
            "        from packages.orchestration.project_registry import (\n"
            "            resolve_project as _folder_only_resolve,\n"
            "        )\n"
            "        _p = _folder_only_resolve(cwd)\n"
            "        if _p is None:\n"
            "            raise ProjectNotFoundError(cwd=cwd)\n"
            "        project, source = _p, \"cwd\"\n"
        ),
    },
    {
        "label": "m8 single_project reads len(projects) <= 1",
        "prod": COCKPIT_PROD,
        "test": COCKPIT_TEST,
        "from": '"single_project": len(entries) == 1,',
        "to": '"single_project": len(entries) <= 1,',
    },
    {
        "label": "m9 do_GET's literal /api/projects route no longer matches that path",
        "prod": UI_SERVER_PROD,
        "test": ROUTES_TEST,
        "from": '        if path == "/api/projects":\n',
        "to": '        if path == "/api/projects-disabled":\n',
    },
    {
        "label": "m10 _build_project_summary_json answers (200, {}) for a selector that names no project",
        "prod": UI_SERVER_PROD,
        "test": ROUTES_TEST,
        "from": '    if project is None:\n        return _safe_error(404, "project not found")\n',
        "to": "    if project is None:\n        return (200, {})\n",
    },
]


def _run_pytest(worktree: Path, test_files: list[str]) -> tuple[int, str]:
    env = dict(os.environ)
    existing = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = str(worktree) + (os.pathsep + existing if existing else "")
    proc = subprocess.run(
        [sys.executable, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider", *test_files],
        cwd=str(worktree),
        env=env,
        capture_output=True,
        text=True,
    )
    return proc.returncode, proc.stdout + proc.stderr


def _failed_count(output: str) -> int:
    m = re.search(r"(\d+) failed", output)
    return int(m.group(1)) if m else 0


def main() -> int:
    worktree = Path(sys.argv[1]).resolve()
    all_ok = True

    exit_code, output = _run_pytest(worktree, CONTROL_TEST_FILES)
    print(f"control (first): exit={exit_code} failed={_failed_count(output)}")
    if exit_code != 0:
        all_ok = False

    for mutation in MUTATIONS:
        prod_path = worktree / mutation["prod"]
        original = prod_path.read_bytes()
        original_text = original.decode("utf-8")
        occurrences = original_text.count(mutation["from"])
        if occurrences != 1:
            print(
                f"{mutation['label']}: FROM text occurs {occurrences} times in "
                f"{mutation['prod']}, expected exactly 1"
            )
            return 1
        mutated_text = original_text.replace(mutation["from"], mutation["to"], 1)
        prod_path.write_bytes(mutated_text.encode("utf-8"))

        exit_code, output = _run_pytest(worktree, [mutation["test"]])
        failed = _failed_count(output)
        print(f"{mutation['label']}: exit={exit_code} failed={failed}")
        if exit_code == 0:
            all_ok = False

        prod_path.write_bytes(original)
        restored = prod_path.read_bytes()
        identical = restored == original
        print(f"restored byte-identical: {identical}")
        if not identical:
            all_ok = False

    exit_code, output = _run_pytest(worktree, CONTROL_TEST_FILES)
    print(f"control (last): exit={exit_code} failed={_failed_count(output)}")
    if exit_code != 0:
        all_ok = False

    print(f"ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: {all_ok}")
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
