#!/usr/bin/env python3
"""F026 R3 G5 — the red proofs.

Given a worktree path, runs an unmutated control of BOTH runners first and last, and
between them applies each mutation below (every FROM must occur exactly once in its
file), runs the relevant runner, restores the file BYTE-IDENTICAL, and reports each
mutation's label, runner, exit code, failed count and failing test names. A mutation
is caught when its runner goes red.

Python mutations (m1-m3, `packages/orchestration/ui_server.py`) run
`python3 -B -m pytest -q -p no:cacheprovider tests/ui_server/test_dashboard_task_specs.py`
FROM THE WORKTREE ROOT, after purging `__pycache__` — so a stale bytecode cache can
never serve a previous mutation's module.

TypeScript mutations (m4-m9) run vitest over the worktree's changed `.test.ts` files
by the SAME route `.agent/authored/f025-r6-mutations.py` uses (which itself copies
`f025-r5-mutations.py`'s route): vitest runs from the PRIMARY `apps/ui` (a worktree
has no `node_modules`), against a scratch config naming the WORKTREE's copies of the
changed test files, with its own cacheDir.

Usage: python3 -B f026-r3-mutations.py <worktree_root>
"""
from __future__ import annotations

import hashlib
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

HELPER_DIR = Path("/home/decodeux/Repos/remedy/.remedy-wt/f026-r3-mutscratch")
HELPER_DIR.mkdir(parents=True, exist_ok=True)
PRIMARY_UI = Path("/home/decodeux/Repos/remedy/apps/ui")
VITEST_BIN = PRIMARY_UI / "node_modules" / ".bin" / "vitest"

UI_SERVER_REL = "packages/orchestration/ui_server.py"
REMEDY_API_REL = "apps/ui/src/api/remedyApi.ts"
TASK_SPEC_VIEW_REL = "apps/ui/src/api/taskSpecView.ts"
PAINT_NODE_REL = "apps/ui/src/components/graph/renderers/paintNode.ts"
BUILD_FORCE_BRAIN_MODEL_REL = "apps/ui/src/components/graph/buildForceBrainModel.ts"
BRAIN_VIEW_REL = "apps/ui/src/components/graph/brainView.ts"

PY_TEST_FILES = [
    "tests/ui_server/test_dashboard_task_specs.py",
]

# Every `.test.ts` file this round's diff changed for S4/S5 — the same fixed set is
# run for every TypeScript mutation, exactly as f025-r6-mutations.py runs its own.
TS_TEST_FILES = [
    "apps/ui/src/api/remedyApi.test.ts",
    "apps/ui/src/api/taskSpecView.test.ts",
    "apps/ui/src/components/graph/brainView.test.ts",
    "apps/ui/src/components/graph/buildForceBrainModel.test.ts",
    "apps/ui/src/components/graph/renderers/paintNode.test.ts",
]

MUTATIONS = [
    # --- S2: the dashboard's task_specs section (m1-m3) --------------------------
    {"id": "m1", "runner": "py",
     "name": "the section's versions is always []",
     "file": UI_SERVER_REL,
     "from": '                "versions": versions,\n',
     "to": '                "versions": [],\n'},
    {"id": "m2", "runner": "py",
     "name": "the section lets a PauseControlError escape instead of reporting it",
     "file": UI_SERVER_REL,
     "from": (
         '    except (PauseControlError, StopControlError, OSError, ValueError) as exc:\n'
         '        return {"tasks": {}, "error": str(exc)}\n'
     ),
     "to": (
         '    except (StopControlError, OSError, ValueError) as exc:\n'
         '        return {"tasks": {}, "error": str(exc)}\n'
     )},
    {"id": "m3", "runner": "py",
     "name": "a PlanEditRefused makes edit_state read \"waiting\"",
     "file": UI_SERVER_REL,
     "from": (
         '            except PlanEditRefused as exc:\n'
         '                edit_state = ""\n'
         '                not_editable_because = exc.detail\n'
     ),
     "to": (
         '            except PlanEditRefused as exc:\n'
         '                edit_state = "waiting"\n'
         '                not_editable_because = exc.detail\n'
     )},
    # --- S3: the client mapping (m4) ---------------------------------------------
    {"id": "m4", "runner": "ts",
     "name": "normalizeTaskSpecs drops spec_version, so every task reads 1",
     "file": REMEDY_API_REL,
     "from": (
         '    plannedId: typeof r.planned_id === "string" ? r.planned_id : "",\n'
         '    specVersion: normalizeSpecVersionNumber(r.spec_version),\n'
     ),
     "to": (
         '    plannedId: typeof r.planned_id === "string" ? r.planned_id : "",\n'
         '    specVersion: normalizeSpecVersionNumber(undefined),\n'
     )},
    # --- S4: the pure view (m5, m6) ----------------------------------------------
    {"id": "m5", "runner": "ts",
     "name": "versionChipLabel gives v1 for version 1",
     "file": TASK_SPEC_VIEW_REL,
     "from": '  if (!spec || spec.specVersion < 2) return null;\n',
     "to": '  if (!spec || spec.specVersion < 1) return null;\n'},
    {"id": "m6", "runner": "ts",
     "name": "specVersionRows compares every row against the FIRST row instead of the previous one",
     "file": TASK_SPEC_VIEW_REL,
     "from": (
         '  const rows: TaskSpecVersionRow[] = [];\n'
         '  let previous: RemedyTaskSpecFields | null = null;\n'
         '  for (const version of spec.versions) {\n'
         '    rows.push({\n'
         '      specVersion: version.specVersion,\n'
         '      current: false,\n'
         '      state: version.state,\n'
         '      archivedAt: version.archivedAt,\n'
         '      changes: changesFrom(previous, version),\n'
         '    });\n'
         '    previous = version;\n'
         '  }\n'
     ),
     "to": (
         '  const rows: TaskSpecVersionRow[] = [];\n'
         '  const previous: RemedyTaskSpecFields | null = spec.versions[0] ?? null;\n'
         '  for (const version of spec.versions) {\n'
         '    rows.push({\n'
         '      specVersion: version.specVersion,\n'
         '      current: false,\n'
         '      state: version.state,\n'
         '      archivedAt: version.archivedAt,\n'
         '      changes: changesFrom(previous, version),\n'
         '    });\n'
         '  }\n'
     )},
    # --- S5: the canvas chip (m7, m8, m9) -----------------------------------------
    {"id": "m7", "runner": "ts",
     "name": "the painter paints a chip for a non-task kind",
     "file": PAINT_NODE_REL,
     "from": '  if (node.kind === "task" && node.chip) {\n',
     "to": '  if (node.chip) {\n'},
    {"id": "m8", "runner": "ts",
     "name": "buildBrainLayout ignores meta.specVersion",
     "file": BUILD_FORCE_BRAIN_MODEL_REL,
     "from": (
         '  const version = task.meta.specVersion;\n'
         '  return typeof version === "number" && version >= 2 ? `v${version}` : undefined;\n'
     ),
     "to": '  return undefined;\n'},
    {"id": "m9", "runner": "ts",
     "name": "dashboardBrainSeeds drops specVersion",
     "file": BRAIN_VIEW_REL,
     "from": (
         '    title: t.label,\n'
         '    ...(Object.prototype.hasOwnProperty.call(specVersions, t.id) ? { specVersion: specVersions[t.id] } : {}),\n'
         '  }));\n'
     ),
     "to": (
         '    title: t.label,\n'
         '  }));\n'
     )},
]


def sha256_of(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def purge_pycache(worktree: Path) -> None:
    for d in worktree.rglob("__pycache__"):
        shutil.rmtree(d, ignore_errors=True)


def run_pytest(worktree: Path) -> dict:
    purge_pycache(worktree)
    proc = subprocess.run(
        [sys.executable, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider", "--tb=no", "-rfE"]
        + PY_TEST_FILES,
        cwd=str(worktree), capture_output=True, text=True, timeout=180)
    out = proc.stdout + proc.stderr
    m_failed = re.search(r"(\d+) failed", out)
    m_error = re.search(r"(\d+) error", out)
    failed = (int(m_failed.group(1)) if m_failed else 0) + (int(m_error.group(1)) if m_error else 0)
    names = re.findall(r"^FAILED (\S+)", out, re.MULTILINE) + re.findall(r"^ERROR (\S+)", out, re.MULTILINE)
    return {"exit": proc.returncode, "failed": failed, "names": names, "raw": out}


def run_vitest(worktree: Path, tag: str) -> dict:
    cache_dir = HELPER_DIR / f"cache-{tag}-{int(time.time() * 1000)}"
    config = HELPER_DIR / f"vitest.config.{tag}.mjs"
    include = ", ".join(f'"{worktree / f}"' for f in TS_TEST_FILES)
    config.write_text(
        "export default {\n"
        f'  root: "{PRIMARY_UI}",\n'
        f'  cacheDir: "{cache_dir}",\n'
        f'  test: {{ environment: "node", include: [{include}] }},\n'
        "};\n"
    )
    proc = subprocess.run([str(VITEST_BIN), "run", "--config", str(config)],
                          cwd=str(PRIMARY_UI), capture_output=True, text=True, timeout=180)
    out = proc.stdout + proc.stderr
    m = re.search(r"Tests\s+(\d+)\s+failed\s*\|\s*(\d+)\s+passed", out)
    failed = int(m.group(1)) if m else 0
    names = re.findall(r"^\s*[×✗]\s+(.+?)\s*(?:\d+ms)?$", out, re.MULTILINE)
    return {"exit": proc.returncode, "failed": failed, "names": names, "raw": out}


def run_control(worktree: Path, tag: str) -> tuple[dict, dict]:
    return run_pytest(worktree), run_vitest(worktree, tag)


def fmt_control(py: dict, ts: dict) -> str:
    return (f"pytest exit={py['exit']} failed={py['failed']} | "
            f"vitest exit={ts['exit']} failed={ts['failed']}")


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: f026-r3-mutations.py <worktree_root>", file=sys.stderr)
        return 2
    worktree = Path(sys.argv[1]).resolve()
    print(f"worktree: {worktree}")

    py0, ts0 = run_control(worktree, "control-first")
    print(f"CONTROL FIRST: {fmt_control(py0, ts0)}")
    first_green = py0["exit"] == 0 and py0["failed"] == 0 and ts0["exit"] == 0 and ts0["failed"] == 0
    if not first_green:
        print("control is not green; aborting")
        print("--- pytest output ---")
        print(py0["raw"][-4000:])
        print("--- vitest output ---")
        print(ts0["raw"][-4000:])
        return 1

    all_ok = True
    for mut in MUTATIONS:
        target = worktree / mut["file"]
        original = target.read_bytes()
        digest = sha256_of(target)
        text = original.decode("utf-8")
        count = text.count(mut["from"])
        if count != 1:
            print(f"{mut['id']}: SKIPPED, FROM occurrences {count}")
            all_ok = False
            continue
        text = text.replace(mut["from"], mut["to"], 1)
        target.write_bytes(text.encode("utf-8"))
        try:
            if mut["runner"] == "py":
                result = run_pytest(worktree)
            else:
                result = run_vitest(worktree, mut["id"])
        finally:
            target.write_bytes(original)
        restored = sha256_of(target) == digest
        caught = result["exit"] != 0 and result["failed"] > 0
        all_ok &= caught and restored
        names = ", ".join(result["names"]) if result["names"] else "(none parsed)"
        print(f"{mut['id']} ({mut['name']}) [{mut['runner']}]: exit={result['exit']} "
              f"failed={result['failed']} failing=[{names}] | caught={caught} "
              f"restored byte-identical={restored}")

    py1, ts1 = run_control(worktree, "control-last")
    print(f"CONTROL LAST: {fmt_control(py1, ts1)}")
    last_green = py1["exit"] == 0 and py1["failed"] == 0 and ts1["exit"] == 0 and ts1["failed"] == 0
    all_ok &= last_green
    print(f"ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: {all_ok}")
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
