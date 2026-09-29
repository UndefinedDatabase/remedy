#!/usr/bin/env python3
"""F042 R6's mutation tool (G4): red-proofs m1, m2, m3 and l1 inside a disposable worktree.

Usage: python3 f042-r6-mutations.py <worktree path>

For each mutation below it edits the named production file(s) INSIDE that worktree (asserting each
FROM text occurs exactly once there), runs the named check, restores the original bytes, and prints
one line: the mutation's label, the check's real exit code, and either the failed count (pytest) or
the live run's "LIVE: <n> of 7" reading with the names of its failing checks. It runs an unmutated
CONTROL of every check used, first and last, reports "restored byte-identical: <bool>" after each
restore, and ends with "ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>". It never touches any
file outside the worktree it is handed.
"""
from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path


def _run(cmd: list[str], cwd: Path, env: dict[str, str] | None = None, timeout: int = 600) -> tuple[int, str]:
    proc = subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True, timeout=timeout, env=env)
    return proc.returncode, proc.stdout + proc.stderr


def run_pytest(rel_file: str):
    def _check(worktree: Path) -> tuple[int, str]:
        env = dict(os.environ)
        existing = env.get("PYTHONPATH", "")
        env["PYTHONPATH"] = str(worktree) if not existing else f"{worktree}{os.pathsep}{existing}"
        code, out = _run(
            ["python3", "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider", rel_file],
            cwd=worktree, env=env,
        )
        m = re.search(r"(\d+)\s+failed", out)
        failed = m.group(1) if m else ("0" if code == 0 else "?")
        return code, f"failed={failed}"
    return _check


run_pytest_multi = run_pytest("tests/ui_server/test_multi_project_live.py")
run_pytest_projects = run_pytest("tests/ui_server/test_projects_route.py")


def run_live(worktree: Path) -> tuple[int, str]:
    code, out = _run(
        ["python3", "-B", str(worktree / ".agent" / "authored" / "f042-r6-live_measure.py"), str(worktree)],
        cwd=worktree, timeout=600,
    )
    m = re.search(r"LIVE: \d+ of \d+ checks pass", out)
    reading = m.group(0) if m else "no LIVE line"
    if m:
        failing = [line.split(" ", 2)[1] for line in out.splitlines() if line.startswith("FAIL ")]
        if failing:
            reading = f"{reading} failing: {', '.join(failing)}"
    return code, reading


# Each mutation: a label, one or more edits (file relative to the worktree, the FROM text asserted
# to occur exactly once there, and the TO text replacing it), and the check it runs.
MUTATIONS = [
    dict(
        label="m1",
        edits=[
            dict(
                file="packages/orchestration/project_cockpit.py",
                frm='scope = ProjectScope(project_id=str(project.id), all_projects=False, source="cockpit")',
                to='scope = ProjectScope(project_id=str(project.id), all_projects=True, source="cockpit")',
            ),
        ],
        check=run_pytest_multi,
    ),
    dict(
        label="m2",
        edits=[
            dict(
                file="packages/orchestration/ui_server.py",
                frm='project_id = str(getattr(job, "project_id", "") or job.metadata.get("project_id") or "")',
                to='project_id = str(job.metadata.get("project_id") or getattr(job, "project_id", "") or "")',
            ),
        ],
        check=run_pytest_projects,
    ),
    dict(
        label="m3",
        edits=[
            dict(
                file="packages/orchestration/ui_server.py",
                frm=(
                    "        linked_jobs, _, _ = scoped_jobs(\n"
                    '            ProjectScope(project_id=str(project.id), all_projects=False, source="dashboard")\n'
                    "        )"
                ),
                to=(
                    "        linked_jobs, _, _ = scoped_jobs(\n"
                    '            ProjectScope(project_id=str(project.id), all_projects=True, source="dashboard")\n'
                    "        )"
                ),
            ),
        ],
        check=run_pytest_multi,
    ),
    dict(
        label="l1",
        edits=[
            dict(
                file="apps/ui/src/RemedyApp.tsx",
                frm='<RemedyShell key={shellKeyOf(address)} dashboard={dashboard} serverToken={token} selectedNodeId={selectedNodeId} onSelectNode={setSelectedNodeId} />',
                to='<RemedyShell dashboard={dashboard} serverToken={token} selectedNodeId={selectedNodeId} onSelectNode={setSelectedNodeId} />',
            ),
            dict(
                file="apps/ui/src/RemedyApp.tsx",
                frm=(
                    "  const openAddress = useCallback((search: string) => {\n"
                    "    setDashboard(null);\n"
                    "    setError(null);"
                ),
                to=(
                    "  const openAddress = useCallback((search: string) => {\n"
                    "    setError(null);"
                ),
            ),
        ],
        check=run_live,
    ),
]


def control(worktree: Path) -> bool:
    ok = True
    for name, fn in (
        ("pytest test_multi_project_live", run_pytest_multi),
        ("pytest test_projects_route", run_pytest_projects),
        ("live run", run_live),
    ):
        code, reading = fn(worktree)
        print(f"CONTROL {name}: exit={code} {reading}")
        if code != 0:
            ok = False
    return ok


def apply_edits(worktree: Path, edits: list[dict]) -> dict[Path, bytes]:
    """Apply each edit, asserting its FROM text occurs exactly once at the moment it is
    applied, and return a per-FILE map of true original bytes (captured once, before any
    edit touches that file) so the caller can restore each file exactly once. Two edits
    naming the same file (l1) are applied in sequence against the file's live, already-
    edited text; restoring from a per-edit snapshot instead of a per-file one would
    re-apply the first edit's mutation on restore, which is the bug this fixes."""
    originals: dict[Path, bytes] = {}
    for edit in edits:
        path = worktree / edit["file"]
        if path not in originals:
            originals[path] = path.read_bytes()
        text = path.read_text(encoding="utf-8")
        occurrences = text.count(edit["frm"])
        if occurrences != 1:
            raise SystemExit(
                f"FROM text occurs {occurrences} times in {edit['file']}, expected 1 -- ABORTING"
            )
        path.write_text(text.replace(edit["frm"], edit["to"], 1), encoding="utf-8")
    return originals


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: mutations.py <worktree path>", file=sys.stderr)
        return 2
    worktree = Path(sys.argv[1]).resolve()

    print("-- control, first --")
    first_ok = control(worktree)

    all_caught = True
    for mutation in MUTATIONS:
        label = mutation["label"]
        try:
            originals = apply_edits(worktree, mutation["edits"])
        except SystemExit as exc:
            print(f"{label}: {exc}")
            return 3
        try:
            code, reading = mutation["check"](worktree)
        finally:
            for path, original in originals.items():
                path.write_bytes(original)
        restored = all(path.read_bytes() == original for path, original in originals.items())
        caught = code != 0
        print(f"{label}: exit={code} {reading} restored byte-identical: {restored}")
        if not caught or not restored:
            all_caught = False

    print("-- control, last --")
    last_ok = control(worktree)

    result = all_caught and first_ok and last_ok
    print(f"ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: {result}")
    return 0 if result else 1


if __name__ == "__main__":
    raise SystemExit(main())
