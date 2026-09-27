"""F029 R4 C6a — the mutation tool (G5): red-proves S1, S2, S3 and S4's eight claims.

Usage: python3 -B .agent/authored/f029-r4-mutations.py <worktree-path>

For each mutation, edits the named module INSIDE the given worktree (its FROM
text must occur exactly once), runs the round's four test files from the
worktree's root after purging __pycache__, restores the original bytes, and
prints the mutation's label, the exit code, the failed count and the failing
node ids. Runs an unmutated control first and last.
"""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

TEST_ARGS = [
    "tests/ui_server/test_rerun_subtree_door.py",
    "tests/ui_server/test_dashboard_task_attempts.py",
    "tests/orchestration/test_subtree_rerun_prepare.py",
    "tests/ui_server/test_dashboard_task_origin.py",
]

SR_PATH = "packages/orchestration/subtree_rerun.py"
UI_PATH = "packages/orchestration/ui_server.py"

# (label, relative path, FROM text, TO text)
MUTATIONS: list[tuple[str, str, str, str]] = [
    (
        "m1 S1 prepares over an unavailable estimate without confirm_cost",
        SR_PATH,
        "    if is_expensive and not confirm_cost:",
        "    if False and is_expensive and not confirm_cost:",
    ),
    (
        "m2 S1 answers needs_confirmation even with confirm_cost",
        SR_PATH,
        "    if is_expensive and not confirm_cost:",
        "    if is_expensive:",
    ),
    (
        "m3 S1 passes no model to the preparation",
        SR_PATH,
        "        record = prepare_subtree_rerun(job.job_id, task_id, model_override=model, actor=actor)",
        '        record = prepare_subtree_rerun(job.job_id, task_id, model_override="", actor=actor)',
    ),
    (
        "m4 S2 writes no event",
        SR_PATH,
        "            RunLogWriter(job_id).log(",
        "            if False: RunLogWriter(job_id).log(",
    ),
    (
        "m5 S3 leaves attempts out of the task item",
        UI_PATH,
        '            "attempts": [dict(a) for a in t.attempts if isinstance(a, dict)],\n'
        '            "origin": _task_origin(t),',
        '            "origin": _task_origin(t),',
    ),
    (
        "m6 S3 places attempt after origin",
        UI_PATH,
        '            "attempt": int(t.attempt),\n'
        '            "attempts": [dict(a) for a in t.attempts if isinstance(a, dict)],\n'
        '            "origin": _task_origin(t),',
        '            "attempts": [dict(a) for a in t.attempts if isinstance(a, dict)],\n'
        '            "origin": _task_origin(t),\n'
        '            "attempt": int(t.attempt),',
    ),
    (
        "m7 S4's branch answers a refusal as a 200",
        UI_PATH,
        '        if payload["command"] == JOB_RERUN_SUBTREE_COMMAND_ID:\n'
        '            try:\n'
        '                accepted_body = self._dispatch_rerun_subtree(job, payload)\n'
        '            except (OSError, RuntimeError, ValueError, TypeError):\n'
        '                # D18, clause four: an effect that RAISED is neither `accepted`,\n'
        '                # which would be false, nor unaudited, which would break D6.\n'
        '                self._audit_attempt(str(job.job_id), "rejected_effect", create=True,\n'
        '                                    payload=payload)\n'
        '                self._send_json(*_safe_error(500, COMMAND_EFFECT_FAILED_MESSAGE))\n'
        '                return\n'
        '            if accepted_body.get("outcome") == "refused":',
        '        if payload["command"] == JOB_RERUN_SUBTREE_COMMAND_ID:\n'
        '            try:\n'
        '                accepted_body = self._dispatch_rerun_subtree(job, payload)\n'
        '            except (OSError, RuntimeError, ValueError, TypeError):\n'
        '                # D18, clause four: an effect that RAISED is neither `accepted`,\n'
        '                # which would be false, nor unaudited, which would break D6.\n'
        '                self._audit_attempt(str(job.job_id), "rejected_effect", create=True,\n'
        '                                    payload=payload)\n'
        '                self._send_json(*_safe_error(500, COMMAND_EFFECT_FAILED_MESSAGE))\n'
        '                return\n'
        '            if False:',
    ),
    (
        "m8 _read_command_payload accepts a confirm_cost that is not a bool",
        UI_PATH,
        "            if confirm_cost_arg is not None and not isinstance(confirm_cost_arg, bool):",
        "            if False:",
    ),
]


def _purge_pycache(root: Path) -> None:
    for cache_dir in root.rglob("__pycache__"):
        shutil.rmtree(cache_dir, ignore_errors=True)


def _run_tests(root: Path) -> tuple[int, str]:
    proc = subprocess.run(
        [sys.executable, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider", *TEST_ARGS],
        cwd=str(root), capture_output=True, text=True,
    )
    return proc.returncode, proc.stdout + proc.stderr


def _parse_result(output: str) -> tuple[int, list[str]]:
    failing = sorted({
        line.split(" ", 1)[1].split(" - ", 1)[0].strip()
        for line in output.splitlines()
        if line.startswith("FAILED ")
    })
    failed_count = 0
    for line in output.splitlines():
        if " failed" in line and ("passed" in line or "error" in line or line.strip().endswith("failed")):
            for token in line.split(","):
                token = token.strip()
                if token.endswith("failed"):
                    failed_count = int(token.split()[0])
    return failed_count, failing


def main() -> int:
    worktree = Path(sys.argv[1]).resolve()
    all_ok = True

    def _report(label: str, code: int, failed: int, nodes: list[str]) -> None:
        nodes_str = ", ".join(nodes) if nodes else "(none)"
        print(f"{label}: exit={code} failed={failed} nodes=[{nodes_str}]")

    _purge_pycache(worktree)
    code, out = _run_tests(worktree)
    failed, nodes = _parse_result(out)
    _report("control (unmutated, first)", code, failed, nodes)
    if code != 0:
        all_ok = False

    originals: dict[str, bytes] = {}
    for _label, rel_path, _from, _to in MUTATIONS:
        if rel_path not in originals:
            originals[rel_path] = (worktree / rel_path).read_bytes()

    for label, rel_path, from_text, to_text in MUTATIONS:
        target = worktree / rel_path
        original = originals[rel_path]
        text = original.decode("utf-8")
        occurrences = text.count(from_text)
        if occurrences != 1:
            print(f"{label}: FROM text occurs {occurrences} times in {rel_path}, expected 1")
            all_ok = False
            continue
        mutated = text.replace(from_text, to_text, 1)
        target.write_text(mutated, encoding="utf-8")

        _purge_pycache(worktree)
        code, out = _run_tests(worktree)
        failed, nodes = _parse_result(out)
        _report(label, code, failed, nodes)
        if code == 0:
            all_ok = False

        target.write_bytes(original)

    restored_ok = True
    for rel_path, original in originals.items():
        current = (worktree / rel_path).read_bytes()
        if current != original:
            restored_ok = False
            print(f"RESTORE FAILED for {rel_path}")

    print(f"restored byte-identical: {restored_ok}")
    all_ok = all_ok and restored_ok

    _purge_pycache(worktree)
    code, out = _run_tests(worktree)
    failed, nodes = _parse_result(out)
    _report("control (unmutated, last)", code, failed, nodes)
    if code != 0:
        all_ok = False

    print(f"ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: {all_ok}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
