#!/usr/bin/env python3
"""F042 R5's mutation tool (G5): red-proofs S1 to S3 inside a disposable worktree.

Usage: python3 f042-r5-mutations.py <worktree path>

For each mutation below it edits the named production file INSIDE that worktree (asserting its
FROM text occurs exactly once there), runs the named check, restores the original bytes, and
prints one line: the mutation's label, the check's real exit code, and either the failed count
(vitest, pytest) or the harness's own "RENDER: <n> of 19 checks pass" reading with the names of
its failing checks. It runs an unmutated CONTROL of every check used, first and last, reports
"restored byte-identical: <bool>" after each restore, and ends with "ALL MUTATIONS CAUGHT AND
RESTORED CLEANLY: <bool>". It never touches any file outside the worktree it is handed.
"""
from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

PRIMARY = Path("/home/decodeux/Repos/remedy")
VITEST_BIN = PRIMARY / "apps" / "ui" / "node_modules" / ".bin" / "vitest"
VITEST_CONFIG = PRIMARY / "apps" / "ui" / "vitest.config.ts"


def _run(cmd: list[str], cwd: Path, env: dict[str, str] | None = None, timeout: int = 300) -> tuple[int, str]:
    proc = subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True, timeout=timeout, env=env)
    return proc.returncode, proc.stdout + proc.stderr


def run_pytest(worktree: Path) -> tuple[int, str]:
    env = dict(os.environ)
    existing = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = str(worktree) if not existing else f"{worktree}{os.pathsep}{existing}"
    code, out = _run(
        ["python3", "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider",
         "tests/ui_server/test_projects_route.py"],
        cwd=worktree, env=env,
    )
    m = re.search(r"(\d+)\s+failed", out)
    failed = m.group(1) if m else ("0" if code == 0 else "?")
    return code, f"failed={failed}"


def run_vitest_zoom(worktree: Path) -> tuple[int, str]:
    ui = worktree / "apps" / "ui"
    code, out = _run(
        ["node", str(VITEST_BIN), "run", "--root", str(ui), "--config", str(VITEST_CONFIG),
         "src/components/graph/zoomDeepLink.test.ts"],
        cwd=ui,
    )
    m = re.search(r"Tests\s+(\d+)\s+failed", out)
    failed = m.group(1) if m else ("0" if code == 0 else "?")
    return code, f"failed={failed}"


def run_harness(worktree: Path) -> tuple[int, str]:
    code, out = _run(
        ["python3", "-B", str(worktree / ".agent" / "authored" / "f042-r5-render_measure.py"), str(worktree)],
        cwd=worktree, timeout=300,
    )
    m = re.search(r"RENDER: \d+ of \d+ checks pass", out)
    reading = m.group(0) if m else "no RENDER line"
    if m:
        failing = [line.split(" ", 2)[1] for line in out.splitlines() if line.startswith("FAIL ")]
        if failing:
            reading = f"{reading} failing: {', '.join(failing)}"
    return code, reading


# Each mutation: a label, the file it edits (relative to the worktree), the FROM text it asserts
# occurs exactly once, the TO text it replaces that with, and the check it runs.
MUTATIONS = [
    dict(
        label="p1", file="packages/orchestration/ui_server.py", check=run_pytest,
        frm='project_id = str(getattr(job, "project_id", "") or job.metadata.get("project_id") or "")',
        to='project_id = str(job.metadata.get("project_id") or "")',
    ),
    dict(
        label="p2", file="packages/orchestration/ui_server.py", check=run_pytest,
        frm=(
            "        linked_jobs, _, _ = scoped_jobs(\n"
            '            ProjectScope(project_id=str(project.id), all_projects=False, source="dashboard")\n'
            "        )"
        ),
        to=(
            "        from packages.orchestration.pingpong_job import list_job_plans\n"
            "        linked_jobs = [j for j in list_job_plans() if str(j.job_id) in project.job_ids]"
        ),
    ),
    dict(
        label="z1", file="apps/ui/src/components/graph/zoomDeepLink.ts", check=run_vitest_zoom,
        frm=(
            '  params.delete("focus");\n'
            '  params.delete("level");\n'
            '  params.delete("tab");'
        ),
        to=(
            '  params.delete("focus");\n'
            '  params.delete("level");\n'
            '  params.delete("tab");\n'
            '  params.delete("project");'
        ),
    ),
    dict(
        label="h1", file="apps/ui/src/components/home/HomeGrid.tsx", check=run_harness,
        frm='style={card.resultTone === "none" ? undefined : { borderLeftColor: `var(--remedy-state-${card.resultTone})` }}',
        to='style={{ borderLeftColor: `var(--remedy-state-${card.resultTone})` }}',
    ),
    dict(
        label="h2", file="apps/ui/src/components/rail/SideIconDock.tsx", check=run_harness,
        frm="{...(i === 0 ? { title: OVERVIEW_TITLE, onClick: goHome } : {})}",
        to="{...(i === 0 ? { title: OVERVIEW_TITLE } : {})}",
    ),
]


def control(worktree: Path) -> bool:
    ok = True
    for name, fn in (
        ("pytest project line", run_pytest),
        ("vitest zoomDeepLink", run_vitest_zoom),
        ("harness", run_harness),
    ):
        code, reading = fn(worktree)
        print(f"CONTROL {name}: exit={code} {reading}")
        if code != 0:
            ok = False
    return ok


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
        path = worktree / mutation["file"]
        original = path.read_bytes()
        text = original.decode("utf-8")
        frm = mutation["frm"]
        occurrences = text.count(frm)
        if occurrences != 1:
            print(f"{label}: FROM text occurs {occurrences} times in {mutation['file']}, expected 1 -- ABORTING")
            return 3
        path.write_bytes(text.replace(frm, mutation["to"], 1).encode("utf-8"))
        try:
            code, reading = mutation["check"](worktree)
        finally:
            path.write_bytes(original)
        restored = path.read_bytes() == original
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
