#!/usr/bin/env python3
"""Mutation tool for F025 R6: U1 (the pause request module, `pauseSend.ts`), U2 (the
pure pause view, `pauseView.ts`), U3-U5 (the control and its mounts) and T3 (the
round's contract guard).

Given a worktree path, runs an unmutated control of BOTH runners first and last, and
between them applies each mutation below (every FROM must occur exactly once in its
file), runs the relevant runner(s), restores the file BYTE-IDENTICAL, and reports each
mutation's label, runner, exit code, failed count and failing test names. A mutation
is caught when its runner goes red.

Python mutations (m8-m10) run `python3 -B -m pytest -q -p no:cacheprovider` over T3
(tests/ui_contracts/test_pause_controls_contract.py) FROM THE WORKTREE ROOT, after
purging __pycache__ — so a stale bytecode cache can never serve a previous mutation's
module.

TypeScript mutations (m1-m7) run vitest over the worktree's changed `.test.ts` files
by the SAME route `.agent/authored/f025-r5-mutations.py` uses: vitest runs from the
PRIMARY `apps/ui` (a worktree has no node_modules), against a scratch config naming
the WORKTREE's copies of the changed test files, with its own cacheDir.

Usage: python3 -B f025-r6-mutations.py <worktree_root>
"""
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

HELPER_DIR = Path("/home/decodeux/Repos/remedy/.remedy-wt/f025-r6-mutscratch")
HELPER_DIR.mkdir(parents=True, exist_ok=True)
PRIMARY_UI = Path("/home/decodeux/Repos/remedy/apps/ui")
VITEST_BIN = PRIMARY_UI / "node_modules" / ".bin" / "vitest"

PAUSE_SEND_REL = "apps/ui/src/api/pauseSend.ts"
PAUSE_VIEW_REL = "apps/ui/src/api/pauseView.ts"
PANEL_REL = "apps/ui/src/components/panels/RightLivePanel.tsx"
STAGE_REL = "apps/ui/src/components/graph/BrainGraphStage.tsx"

PY_TEST_FILES = [
    "tests/ui_contracts/test_pause_controls_contract.py",
]

# Every `.test.ts` file this round's diff changed — the same fixed set is run for
# every TypeScript mutation, exactly as f025-r5-mutations.py runs its own fixed set.
TS_TEST_FILES = [
    "apps/ui/src/api/pauseSend.test.ts",
    "apps/ui/src/api/pauseView.test.ts",
]

MUTATIONS = [
    # --- U1: the builder and the submit (m1, m2) --------------------------------
    {"id": "m1", "runner": "ts",
     "name": "the builder drops task from args",
     "file": PAUSE_SEND_REL,
     "from": '      args: taskId === undefined ? {} : { task: taskId },\n',
     "to": '      args: {},\n'},
    {"id": "m2", "runner": "ts",
     "name": "the submit answers body: null for every reply",
     "file": PAUSE_SEND_REL,
     "from": (
         '  return { outcome: reply.ok ? "accepted" : "refused", status: reply.status,\n'
         '           body: parsedObjectOrNull(parsed) };\n'
     ),
     "to": (
         '  return { outcome: reply.ok ? "accepted" : "refused", status: reply.status,\n'
         '           body: null };\n'
     )},
    # --- U1: the mapping (m3) ---------------------------------------------------
    {"id": "m3", "runner": "ts",
     "name": "a 409 maps to the generic refusal sentence",
     "file": PAUSE_SEND_REL,
     "from": (
         '    case 409:\n'
         '      return { tone, sentence: ENDED_SENTENCE };\n'
     ),
     "to": ""},
    # --- U2: "by you", the banner order and the two actions (m4-m7) -------------
    {"id": "m4", "runner": "ts",
     "name": 'by you" accepts any source',
     "file": PAUSE_VIEW_REL,
     "from": '  return typeof source === "string" && PAUSE_OWNER_SOURCES.includes(source);\n',
     "to": '  return typeof source === "string";\n'},
    {"id": "m5", "runner": "ts",
     "name": "the banner checks requested before parked",
     "file": PAUSE_VIEW_REL,
     "from": (
         '  if (jobIsParked(dashboard)) {\n'
         '    return {\n'
         '      badge: "PAUSED",\n'
         '      text: pausedByYou(dashboard)\n'
         '        ? "Paused by you. Nothing runs until you resume it."\n'
         '        : "Paused. Nothing runs until it is resumed.",\n'
         '      command: `${PARKED_COMMAND_PREFIX}${dashboard.jobId}`,\n'
         '      tone: "warn",\n'
         '    };\n'
         '  }\n'
         '  if (pause.requested) {\n'
         '    return {\n'
         '      badge: "PAUSING",\n'
         '      text: "Pause requested. The job stops before its next step.",\n'
         '      command: "",\n'
         '      tone: "warn",\n'
         '    };\n'
         '  }\n'
     ),
     "to": (
         '  if (pause.requested) {\n'
         '    return {\n'
         '      badge: "PAUSING",\n'
         '      text: "Pause requested. The job stops before its next step.",\n'
         '      command: "",\n'
         '      tone: "warn",\n'
         '    };\n'
         '  }\n'
         '  if (jobIsParked(dashboard)) {\n'
         '    return {\n'
         '      badge: "PAUSED",\n'
         '      text: pausedByYou(dashboard)\n'
         '        ? "Paused by you. Nothing runs until you resume it."\n'
         '        : "Paused. Nothing runs until it is resumed.",\n'
         '      command: `${PARKED_COMMAND_PREFIX}${dashboard.jobId}`,\n'
         '      tone: "warn",\n'
         '    };\n'
         '  }\n'
     )},
    {"id": "m6", "runner": "ts",
     "name": "jobPauseAction answers pause whatever live.running reads",
     "file": PAUSE_VIEW_REL,
     "from": (
         '  if (dashboard.live.running) {\n'
         '    return "pause";\n'
         '  }\n'
         '  return null;\n'
         '}\n'
         '\n'
         '/** One task\'s own action'
     ),
     "to": (
         '  return "pause";\n'
         '}\n'
         '\n'
         '/** One task\'s own action'
     )},
    {"id": "m7", "runner": "ts",
     "name": "taskPauseAction answers pause for a done task",
     "file": PAUSE_VIEW_REL,
     "from": (
         '  if (taskState !== "done") {\n'
         '    return "pause";\n'
         '  }\n'
         '  return null;\n'
         '}\n'
         '\n'
         '/** Every action\'s label'
     ),
     "to": (
         '  return "pause";\n'
         '}\n'
         '\n'
         '/** Every action\'s label'
     )},
    # --- T3's own guard: sources, the panel mount, the stage banner (m8-m10) ----
    {"id": "m8", "runner": "py",
     "name": "PAUSE_OWNER_SOURCES gains system",
     "file": PAUSE_VIEW_REL,
     "from": 'export const PAUSE_OWNER_SOURCES: readonly string[] = ["cli", "ui"];\n',
     "to": 'export const PAUSE_OWNER_SOURCES: readonly string[] = ["cli", "ui", "system"];\n'},
    {"id": "m9", "runner": "py",
     "name": "the panel's PauseControl mount is deleted",
     "file": PANEL_REL,
     "from": '      <PauseControl target={{ jobId: dashboard.jobId, serverToken }} scope="job" action={jobPauseAction(dashboard)} />\n',
     "to": ""},
    {"id": "m10", "runner": "py",
     "name": "the stage's pause banner is deleted",
     "file": STAGE_REL,
     "from": (
         '      {banner && (\n'
         '        <div className={styles.pauseBanner} role="status" data-ui="pause-banner">\n'
         '          <span className={styles.pauseBadge}>{banner.badge}</span>\n'
         '          <span>{banner.text}</span>\n'
         '          {banner.command !== "" && <code>{banner.command}</code>}\n'
         '        </div>\n'
         '      )}\n'
     ),
     "to": ""},
]


def sha256_of(path: Path) -> str:
    import hashlib
    return hashlib.sha256(path.read_bytes()).hexdigest()


def purge_pycache(worktree: Path) -> None:
    for d in worktree.rglob("__pycache__"):
        shutil.rmtree(d, ignore_errors=True)


def run_pytest(worktree: Path) -> dict:
    purge_pycache(worktree)
    proc = subprocess.run(
        [sys.executable, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider", "--tb=no", "-rf"]
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
        print("usage: f025-r6-mutations.py <worktree_root>", file=sys.stderr)
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
