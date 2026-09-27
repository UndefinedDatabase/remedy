"""F030 R3 G5 — the red-proof tool for T003's browser half (DECISION F030 D3).

Takes a worktree path (argv[1]). For each mutation below: edits the named file INSIDE that
worktree (asserting its FROM text occurs exactly once), runs the mutation's own runner, records
the exit code, the failed count and the failing tests' names, restores the file's original
bytes, and verifies the restoration is byte-identical. Runs an unmutated control of EACH runner
first and last.

PYTHON mutations run `pytest` from the worktree's own root, after purging its `__pycache__`, over
the three Python test files this round wrote or touched. VITEST mutations run the PRIMARY
checkout's own `vitest` binary against a scratch config this tool writes under
`.remedy-wt/f030-r3-worker/`: a plain object naming the primary's `apps/ui` as `root`, a cache
directory under `.remedy-wt/`, `test.environment` `"node"`, and `test.include` the WORKTREE's
three vitest files by absolute path — so the binary is the primary's, but every relative import
the test files carry resolves inside the mutated worktree.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

PRIMARY = Path("/home/decodeux/Repos/remedy")
WORKER_DIR = PRIMARY / ".remedy-wt" / "f030-r3-worker"
VITEST_BIN = PRIMARY / "apps" / "ui" / "node_modules" / ".bin" / "vitest"

#: PYTHON's own selection: the new frame test, the steering suite it joins, and the new
#: contract test whose Python half reads `_steering_note_summary_payload` directly.
PYTHON_TESTS = [
    "tests/ui_server/test_steering_note_frame.py",
    "tests/ui_server/test_sse_stream.py",
    "tests/ui_contracts/test_steering_note_contract.py",
]

#: VITEST's own selection, by filename under the worktree's `apps/ui/src/api/`.
VITEST_TEST_NAMES = ["steeringNote.test.ts", "feedRow.test.ts", "steeringSend.test.ts"]

# label, runner, path (relative to worktree root), FROM (must occur exactly once), TO
MUTATIONS: list[tuple[str, str, str, str, str]] = [
    ("m1 the note payload leaves out text",
     "PYTHON", "packages/orchestration/ui_server.py",
     '        "text": str(meta.get("text", "")),\n',
     ""),

    ("m2 note is added to every kind's frame",
     "PYTHON", "packages/orchestration/ui_server.py",
     '    if kind == "steering_message_received":\n'
     "        note = _steering_note_summary_payload(metadata)",
     '    if True:\n'
     "        note = _steering_note_summary_payload(metadata)"),

    ("m3 the note payload also copies record_sha256",
     "PYTHON", "packages/orchestration/ui_server.py",
     '        "task_id": str(meta.get("task_id", "")),\n'
     "    }\n"
     "\n"
     "\n"
     "def _steering_ack_summary_payload",
     '        "task_id": str(meta.get("task_id", "")),\n'
     '        "record_sha256": str(meta.get("record_sha256", "")),\n'
     "    }\n"
     "\n"
     "\n"
     "def _steering_ack_summary_payload"),

    ("m4 readSteeringNote accepts a blank text",
     "VITEST", "apps/ui/src/api/steeringNote.ts",
     'typeof text !== "string" || text.trim() === ""',
     'typeof text !== "string"'),

    ("m5 steeringFocusTaskId always answers empty",
     "VITEST", "apps/ui/src/api/steeringNote.ts",
     '  const owner = tasks.find(task => task.nodeId === nodeId);\n'
     '  return owner ? owner.id : "";',
     '  return "";'),

    ("m6 steeringPlaceholder names the whole job for a task",
     "VITEST", "apps/ui/src/api/steeringNote.ts",
     '  return taskId === ""\n'
     '    ? "Note for the whole job — read at its next round"\n'
     '    : `Note for task ${taskId} — read at its next round`;',
     '  return taskId === ""\n'
     '    ? `Note for task ${taskId} — read at its next round`\n'
     '    : "Note for the whole job — read at its next round";'),

    ("m7 a note's row keeps the catalog line",
     "VITEST", "apps/ui/src/api/feedRow.ts",
     "line: note ? note.text : ack ? steeringAckLine(ack) : humanized.line,",
     "line: ack ? steeringAckLine(ack) : humanized.line,"),

    ("m8 a note's row gets no author",
     "VITEST", "apps/ui/src/api/feedRow.ts",
     '    ...(note ? { author: "operator" as const } : {}),\n',
     ""),

    ("m9 buildSteerTaskRequest sends chat.send",
     "VITEST", "apps/ui/src/api/steeringSend.ts",
     "command: STEER_TASK_COMMAND,",
     "command: CHAT_SEND_COMMAND,"),

    ("m10 buildSteerTaskRequest leaves out task_id",
     "VITEST", "apps/ui/src/api/steeringSend.ts",
     "args: { task_id: taskId, message: cleaned },",
     "args: { message: cleaned },"),

    ("m11 a 409 task_not_steerable reads as the accepted sentence",
     "VITEST", "apps/ui/src/api/steeringSend.ts",
     '  task_not_steerable: "Not recorded: this task can no longer be steered.",\n',
     '  task_not_steerable: "Your note was recorded. Task reads it at the start of its next '
     'round.",\n'),
]


def _purge_pycache(root: Path) -> None:
    for path in root.rglob("__pycache__"):
        if not path.is_dir():
            continue
        for child in sorted(path.rglob("*"), key=lambda p: len(p.parts), reverse=True):
            if child.is_file():
                child.unlink()
            elif child.is_dir():
                child.rmdir()
        path.rmdir()


def run_python(worktree: Path) -> tuple[int, int, list[str]]:
    _purge_pycache(worktree)
    proc = subprocess.run(
        [sys.executable, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider", "-rf",
         *PYTHON_TESTS],
        cwd=str(worktree), capture_output=True, text=True, timeout=120,
    )
    out = proc.stdout + proc.stderr
    failing = [line[len("FAILED "):].split(" - ")[0]
               for line in out.splitlines() if line.startswith("FAILED ")]
    return proc.returncode, len(failing), failing


def _write_vitest_config(worktree: Path) -> Path:
    ui_src = worktree / "apps" / "ui" / "src" / "api"
    includes = ",\n    ".join(json.dumps(str(ui_src / name)) for name in VITEST_TEST_NAMES)
    config = (
        "export default {\n"
        f"  root: {json.dumps(str(PRIMARY / 'apps' / 'ui'))},\n"
        f"  cacheDir: {json.dumps(str(WORKER_DIR / 'vitest-cache'))},\n"
        "  test: {\n"
        '    environment: "node",\n'
        "    include: [\n"
        f"    {includes},\n"
        "    ],\n"
        "  },\n"
        "};\n"
    )
    config_path = WORKER_DIR / "scratch.vitest.config.ts"
    config_path.write_text(config, encoding="utf-8")
    return config_path


def run_vitest(worktree: Path) -> tuple[int, int, list[str]]:
    config_path = _write_vitest_config(worktree)
    report_path = WORKER_DIR / "vitest-report.json"
    report_path.unlink(missing_ok=True)
    proc = subprocess.run(
        [str(VITEST_BIN), "run", "--config", str(config_path),
         "--reporter=json", f"--outputFile={report_path}"],
        cwd=str(PRIMARY / "apps" / "ui"), capture_output=True, text=True, timeout=60,
    )
    failed_names: list[str] = []
    failed_count = 0
    if report_path.exists():
        data = json.loads(report_path.read_text(encoding="utf-8"))
        failed_count = data.get("numFailedTests", 0)
        for test_result in data.get("testResults", []):
            for assertion in test_result.get("assertionResults", []):
                if assertion.get("status") == "failed":
                    failed_names.append(assertion.get("fullName", "?"))
    return proc.returncode, failed_count, failed_names


RUNNERS = {"PYTHON": run_python, "VITEST": run_vitest}


def _control(worktree: Path, when: str) -> bool:
    ok = True
    for runner in ("PYTHON", "VITEST"):
        exit_code, failed_count, failing = RUNNERS[runner](worktree)
        print(f"control ({when}) {runner}: exit={exit_code} failed={failed_count} "
              f"tests={failing}")
        if exit_code != 0 or failed_count != 0:
            ok = False
    return ok


def main() -> int:
    worktree = Path(sys.argv[1]).resolve()
    WORKER_DIR.mkdir(parents=True, exist_ok=True)

    if not _control(worktree, "start"):
        print("CONTROL RUN IS NOT GREEN — aborting.")
        return 1

    all_caught = True
    restored_all = True
    restored_report: list[tuple[str, bool]] = []
    for label, runner, rel_path, from_text, to_text in MUTATIONS:
        target = worktree / rel_path
        original = target.read_bytes()
        original_text = original.decode("utf-8")
        occurrences = original_text.count(from_text)
        if occurrences != 1:
            print(f"{label}: FROM text occurs {occurrences} times in {rel_path} "
                  f"(expected 1) — SKIPPED")
            all_caught = False
            continue
        mutated_text = original_text.replace(from_text, to_text, 1)
        target.write_text(mutated_text, encoding="utf-8")
        try:
            exit_code, failed_count, failing = RUNNERS[runner](worktree)
        finally:
            target.write_bytes(original)
        restored = target.read_bytes() == original
        restored_all = restored_all and restored
        restored_report.append((f"{label} ({rel_path})", restored))
        caught = exit_code != 0 and failed_count > 0 and bool(failing)
        all_caught = all_caught and caught
        print(f"{label}: runner={runner} exit={exit_code} failed={failed_count} "
              f"tests={failing} caught={caught} restored={restored}")

    if not _control(worktree, "end"):
        all_caught = False

    for label, restored in restored_report:
        print(f"restored byte-identical: {restored} ({label})")

    status = subprocess.run(["git", "status", "--porcelain"], cwd=str(PRIMARY),
                             capture_output=True, text=True)
    primary_clean = status.stdout.strip() == ""
    print("PRIMARY checkout git status --porcelain:")
    print(status.stdout if status.stdout else "(empty)")

    verdict = all_caught and restored_all and primary_clean
    print(f"ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: {verdict}")
    return 0 if verdict else 1


if __name__ == "__main__":
    raise SystemExit(main())
