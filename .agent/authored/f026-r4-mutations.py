#!/usr/bin/env python3
"""F026 R4 G5 — the red proofs.

Given a worktree path, runs an unmutated control of BOTH runners first and last, and
between them applies each mutation below (every FROM must occur exactly once in its
file), runs the relevant runner, restores the file BYTE-IDENTICAL, and reports each
mutation's label, runner, exit code, failed count and failing test names. A mutation
is caught when its runner goes red.

Python mutations (m1, m8) run
`python3 -B -m pytest -q -p no:cacheprovider tests/orchestration/test_redaction_patterns.py
tests/ui_contracts/test_task_edit_controls_contract.py` FROM THE WORKTREE ROOT, after
purging `__pycache__` — so a stale bytecode cache can never serve a previous mutation's
module. m8 mutates a `.tsx` file, but the test that catches it is the PYTHON contract
test `test_task_edit_controls_contract.py`, which reads `DetailPopover.tsx`'s own source
text rather than executing it — no DOM harness exists in this repo (see that test's own
header), so the contract is checked as text, not as a render.

TypeScript mutations (m2-m7) run vitest over the worktree's changed `.test.ts` files by
the SAME route `.agent/authored/f026-r3-mutations.py` uses (which itself copies
`f025-r6-mutations.py`'s route): vitest runs from the PRIMARY `apps/ui` (a worktree has
no `node_modules`), against a scratch config naming the WORKTREE's copies of the changed
test files, with its own cacheDir.

Usage: python3 -B f026-r4-mutations.py <worktree_root>
"""
from __future__ import annotations

import hashlib
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

HELPER_DIR = Path("/home/decodeux/Repos/remedy/.remedy-wt/f026-r4-mutscratch")
HELPER_DIR.mkdir(parents=True, exist_ok=True)
PRIMARY_UI = Path("/home/decodeux/Repos/remedy/apps/ui")
VITEST_BIN = PRIMARY_UI / "node_modules" / ".bin" / "vitest"

REDACTION_REL = "packages/orchestration/redaction_patterns.py"
TASK_SPEC_VIEW_REL = "apps/ui/src/api/taskSpecView.ts"
TASK_EDIT_SEND_REL = "apps/ui/src/api/taskEditSend.ts"
DETAIL_POPOVER_REL = "apps/ui/src/components/detail/DetailPopover.tsx"

PY_TEST_FILES = [
    "tests/orchestration/test_redaction_patterns.py",
    "tests/ui_contracts/test_task_edit_controls_contract.py",
]

# Every `.test.ts` file this round's diff changed — the same fixed set is run
# for every TypeScript mutation, exactly as f026-r3-mutations.py runs its own.
TS_TEST_FILES = [
    "apps/ui/src/api/taskSpecView.test.ts",
    "apps/ui/src/api/taskEditSend.test.ts",
    "apps/ui/src/components/graph/brainReducer.test.ts",
]

MUTATIONS = [
    # --- S1: the secret detector (m1) --------------------------------------
    {"id": "m1", "runner": "py",
     "name": "the sk- alternative loses its R-1060 boundary",
     "file": REDACTION_REL,
     "from": '    r"(?:(?<![A-Za-z0-9])sk-[a-zA-Z0-9_-]{8,})"     # OpenAI-style (R-1060: only at a token start)\n',
     "to": '    r"(?:sk-[a-zA-Z0-9_-]{8,})"     # OpenAI-style (R-1060: only at a token start)\n'},
    # --- S2: the pure view (m2-m4) ------------------------------------------
    {"id": "m2", "runner": "ts",
     "name": 'taskEditAction answers an action for an editState of ""',
     "file": TASK_SPEC_VIEW_REL,
     "from": 'const EDITABLE_STATES: ReadonlySet<string> = new Set(["waiting", "paused", "failed"]);',
     "to": 'const EDITABLE_STATES: ReadonlySet<string> = new Set(["", "waiting", "paused", "failed"]);'},
    {"id": "m3", "runner": "ts",
     "name": "changedTaskFields returns every field, changed or not",
     "file": TASK_SPEC_VIEW_REL,
     "from": (
         '  if (draft.title !== current.title) {\n'
         '    out.title = draft.title;\n'
         '  }\n'
         '  if (draft.goal !== current.goal) {\n'
         '    out.goal = draft.goal;\n'
         '  }\n'
         '  const acceptance = draftLines(draft.acceptance);\n'
         '  if (acceptance.join("\\n") !== current.acceptance.join("\\n")) {\n'
         '    out.acceptance = acceptance;\n'
         '  }\n'
         '  if (draft.band !== current.estTokensBand) {\n'
         '    out.est_tokens_band = draft.band;\n'
         '  }\n'
         '  const files = draftLines(draft.files);\n'
         '  if (files.join("\\n") !== current.filesHint.join("\\n")) {\n'
         '    out.files_hint = files;\n'
         '  }\n'
     ),
     "to": (
         '  out.title = draft.title;\n'
         '  out.goal = draft.goal;\n'
         '  const acceptance = draftLines(draft.acceptance);\n'
         '  out.acceptance = acceptance;\n'
         '  out.est_tokens_band = draft.band;\n'
         '  const files = draftLines(draft.files);\n'
         '  out.files_hint = files;\n'
     )},
    {"id": "m4", "runner": "ts",
     "name": "changedTaskFields keeps blank lines",
     "file": TASK_SPEC_VIEW_REL,
     "from": (
         'function draftLines(text: string): string[] {\n'
         '  return text.split("\\n").map((line) => line.trim()).filter((line) => line !== "");\n'
         '}\n'
     ),
     "to": (
         'function draftLines(text: string): string[] {\n'
         '  return text.split("\\n").map((line) => line.trim());\n'
         '}\n'
     )},
    # --- S3: the send module (m5-m7) ----------------------------------------
    {"id": "m5", "runner": "ts",
     "name": "buildTaskEditRequest sends job.plan-edit-task",
     "file": TASK_EDIT_SEND_REL,
     "from": "      command: JOB_EDIT_TASK_COMMAND_ID,\n",
     "to": '      command: "job.plan-edit-task",\n'},
    {"id": "m6", "runner": "ts",
     "name": "buildTaskEditRequest omits expected_version",
     "file": TASK_EDIT_SEND_REL,
     "from": "    args: { task_id: taskId, fields, expected_version: expectedVersion },\n",
     "to": "    args: { task_id: taskId, fields },\n"},
    {"id": "m7", "runner": "ts",
     "name": "describeTaskEditResult drops the relaunch sentence for a failed task",
     "file": TASK_EDIT_SEND_REL,
     "from": (
         '  if (body?.state === "failed") {\n'
         '    return { tone: "ok", sentence: `${sentence} ${RELAUNCH_SENTENCE}` };\n'
         '  }\n'
         '  return { tone: "ok", sentence };\n'
     ),
     "to": '  return { tone: "ok", sentence };\n'},
    # --- S4: the popover's mount condition (m8) -----------------------------
    {"id": "m8", "runner": "py",
     "name": "the popover mounts <TaskEditForm without the taskEditAction condition",
     "file": DETAIL_POPOVER_REL,
     "from": "      {task && serverToken && editAction && (\n",
     "to": "      {task && serverToken && (\n"},
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
        print("usage: f026-r4-mutations.py <worktree_root>", file=sys.stderr)
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
