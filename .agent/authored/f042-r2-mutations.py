"""F042 R2 C6 — the round's mutation tool: red-proofs for S1 to S3 (DECISION F042 D2).

Takes a worktree path (``sys.argv[1]``). For each mutation below it edits the named
production file INSIDE that worktree (asserting its FROM text occurs exactly once
there), runs the named test file — a Python test through ``pytest`` with the
worktree as the working directory and the worktree's own root first on
``PYTHONPATH``, or the vitest file through the PRIMARY checkout's vitest binary
rooted at the worktree's ``apps/ui`` — restores the original bytes, and prints one
line per mutation: its label, the exit code and the failed count. It runs an
unmutated control of every distinct test file the mutations name, first and last,
prints ``restored byte-identical: True`` after each restore, and ends with one
final line stating whether every mutation was caught and every restore was clean.

Usage: ``python3 -B .agent/authored/f042-r2-mutations.py <worktree-path>``
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

PRIMARY = Path("/home/decodeux/Repos/remedy")

COCKPIT_PROD = "packages/orchestration/project_cockpit.py"
UI_SERVER_PROD = "packages/orchestration/ui_server.py"
SCOPE_PROD = "apps/ui/src/api/projectScope.ts"
REMEDY_API_PROD = "apps/ui/src/api/remedyApi.ts"

COCKPIT_TEST = "tests/orchestration/test_project_cockpit.py"
ROUTES_TEST = "tests/ui_server/test_projects_route.py"
VITEST_FILE = "src/api/projectScope.test.ts"

PYTEST_CONTROL_FILES = [COCKPIT_TEST, ROUTES_TEST]

MUTATIONS = [
    {
        "label": "v1 a switch ticket stays current while the gate's current key equals its "
        "own key, rather than until the next begin",
        "kind": "vitest",
        "prod": SCOPE_PROD,
        "from": "isCurrent: () => ticketGeneration === generation",
        "to": "isCurrent: () => key === nextKey",
    },
    {
        "label": "v2 switchProject calls apply without asking whether its ticket is current",
        "kind": "vitest",
        "prod": SCOPE_PROD,
        "from": "  if (!ticket.isCurrent()) return false;\n  apply({ slug, jobId: switchTargetJob(summary), summary });\n  return true;\n",
        "to": "  apply({ slug, jobId: switchTargetJob(summary), summary });\n  return true;\n",
    },
    {
        "label": "v3 a switch keeps the focus parameter",
        "kind": "vitest",
        "prod": SCOPE_PROD,
        "from": 'export const JOB_SCOPED_PARAMS: readonly string[] = ["job", "job_id", "focus", "level", "tab"];',
        "to": 'export const JOB_SCOPED_PARAMS: readonly string[] = ["job", "job_id", "level", "tab"];',
    },
    {
        "label": "v4 resolveActiveProject never takes the address's project",
        "kind": "vitest",
        "prod": SCOPE_PROD,
        "from": '  if (urlProject !== "") {',
        "to": "  if (false) {",
    },
    {
        "label": "v5 the card decoder reads a null value_usd as 0",
        "kind": "vitest",
        "prod": SCOPE_PROD,
        "from": 'value_usd: numberOrNull(obj["value_usd"]),',
        "to": 'value_usd: numberOrNull(obj["value_usd"]) ?? 0,',
    },
    {
        "label": "v6 switcherVisible answers true for every view that is not null",
        "kind": "vitest",
        "prod": SCOPE_PROD,
        "from": "  return view !== null && !view.single_project && view.projects.length > 1;",
        "to": "  return view !== null;",
    },
    {
        "label": "v7 decodeJobProject accepts a scope outside the three",
        "kind": "vitest",
        "prod": SCOPE_PROD,
        "from": '  if (scope !== "project" && scope !== "unscoped" && scope !== "orphaned") return null;',
        "to": "  if (false) return null;",
    },
    {
        "label": "v8 loadProjectsView lets a failed read throw instead of answering null",
        "kind": "vitest",
        "prod": REMEDY_API_PROD,
        "from": (
            "export async function loadProjectsView(\n"
            "  request: { token: string; baseUrl?: string },\n"
            "  fetchPayload: ProjectFetcher = fetchJson,\n"
            "): Promise<ProjectsView | null> {\n"
            "  try {\n"
            "    return decodeProjectsView(await fetchPayload(projectsViewPath(request)));\n"
            "  } catch {\n"
            "    return null;\n"
            "  }\n"
            "}"
        ),
        "to": (
            "export async function loadProjectsView(\n"
            "  request: { token: string; baseUrl?: string },\n"
            "  fetchPayload: ProjectFetcher = fetchJson,\n"
            "): Promise<ProjectsView | null> {\n"
            "  return decodeProjectsView(await fetchPayload(projectsViewPath(request)));\n"
            "}"
        ),
    },
    {
        "label": 'p1 job_project_view labels a job with no project "project"',
        "kind": "pytest",
        "prod": COCKPIT_PROD,
        "test": COCKPIT_TEST,
        "from": '"scope": "unscoped", "project": None}',
        "to": '"scope": "project", "project": None}',
    },
    {
        "label": "p2 the project entry is removed from do_GET's endpoint dict",
        "kind": "pytest",
        "prod": UI_SERVER_PROD,
        "test": ROUTES_TEST,
        "from": '                "project": _build_job_project_json,\n',
        "to": "",
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


def _run_vitest(worktree: Path) -> tuple[int, str]:
    vitest_bin = PRIMARY / "apps" / "ui" / "node_modules" / ".bin" / "vitest"
    config = PRIMARY / "apps" / "ui" / "vitest.config.ts"
    ui_root = worktree / "apps" / "ui"
    proc = subprocess.run(
        [str(vitest_bin), "run", "--root", str(ui_root), "--config", str(config), VITEST_FILE],
        cwd=str(ui_root),
        capture_output=True,
        text=True,
    )
    return proc.returncode, proc.stdout + proc.stderr


def _failed_count(output: str) -> int:
    m = re.search(r"(\d+) failed", output)
    if m:
        return int(m.group(1))
    m = re.search(r"Tests\s+(\d+) failed", output)
    return int(m.group(1)) if m else 0


def main() -> int:
    worktree = Path(sys.argv[1]).resolve()
    all_ok = True

    exit_code, output = _run_pytest(worktree, PYTEST_CONTROL_FILES)
    print(f"control pytest (first): exit={exit_code} failed={_failed_count(output)}")
    if exit_code != 0:
        all_ok = False

    exit_code, output = _run_vitest(worktree)
    print(f"control vitest (first): exit={exit_code} failed={_failed_count(output)}")
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

        if mutation["kind"] == "pytest":
            exit_code, output = _run_pytest(worktree, [mutation["test"]])
        else:
            exit_code, output = _run_vitest(worktree)
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

    exit_code, output = _run_pytest(worktree, PYTEST_CONTROL_FILES)
    print(f"control pytest (last): exit={exit_code} failed={_failed_count(output)}")
    if exit_code != 0:
        all_ok = False

    exit_code, output = _run_vitest(worktree)
    print(f"control vitest (last): exit={exit_code} failed={_failed_count(output)}")
    if exit_code != 0:
        all_ok = False

    print(f"ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: {all_ok}")
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
