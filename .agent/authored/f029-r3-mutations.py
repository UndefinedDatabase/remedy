"""F029 R3 C6a — the mutation tool (G5): red-proves S1, S2 and S3's ten claims.

Usage: python3 -B .agent/authored/f029-r3-mutations.py <worktree-path>

For each mutation, edits the named module INSIDE the given worktree (its FROM
text must occur exactly once), runs the round's two test files from the
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
    "tests/cli/test_job_rerun_subtree.py",
    "tests/orchestration/test_subtree_rerun_prepare.py",
]

SR_PATH = "packages/orchestration/subtree_rerun.py"
CMD_PATH = "apps/cli/commands/job_rerun_cmd.py"

# (label, relative path, FROM text, TO text)
MUTATIONS: list[tuple[str, str, str, str]] = [
    (
        "m1 S1 (a) is skipped",
        SR_PATH,
        'if (evidence_root / dest_rel).exists():',
        'if False and (evidence_root / dest_rel).exists():',
    ),
    (
        "m2 S1 (b) never calls retain_for_recovery",
        SR_PATH,
        '                    W.retain_for_recovery(handle, f"{type(exc_value).__name__}: {exc_value}")',
        '                    pass',
    ),
    (
        "m3 S2 skips a task without a band instead of making the estimate unavailable",
        SR_PATH,
        '            available = False\n            unpriced.append(task_id)\n            continue',
        '            unpriced.append(task_id)\n            continue',
    ),
    (
        "m4 S2 counts the root task alone",
        SR_PATH,
        '    for task_id in subtree_ids:\n        task = tasks_by_id[task_id]\n        plan = task.inputs.get("plan")',
        '    for task_id in subtree_ids[:1]:\n        task = tasks_by_id[task_id]\n        plan = task.inputs.get("plan")',
    ),
    (
        "m5 S3 prepares the rerun after a declined preview",
        CMD_PATH,
        '    if not proceed:',
        '    if False:',
    ),
    (
        "m6 S3 exits 3 for unknown_task",
        CMD_PATH,
        '_USAGE_CODES = frozenset({"unknown_task", "model_invalid"})',
        '_USAGE_CODES = frozenset({"model_invalid"})',
    ),
    (
        "m7 S3 exits 1 for job_running",
        CMD_PATH,
        '1 if code == "job_not_found" else',
        '1 if code in ("job_not_found", "job_running") else',
    ),
    (
        "m8 S3 passes no model to prepare_subtree_rerun",
        CMD_PATH,
        '        record = SR.prepare_subtree_rerun(\n            job_id, task_id, model_override=model, actor=CLI_ACTOR)',
        '        record = SR.prepare_subtree_rerun(\n            job_id, task_id, model_override="", actor=CLI_ACTOR)',
    ),
    (
        "m9 S3 passes yes=False to the preview",
        CMD_PATH,
        'estimate, confirm_above_usd=resolve_confirm_above_usd(), yes=yes,',
        'estimate, confirm_above_usd=resolve_confirm_above_usd(), yes=False,',
    ),
    (
        "m10 S3 leaves the refusal's facts out of the envelope",
        CMD_PATH,
        '    fail(code, exc.detail, json_output=json_output, exit_code=refusal_exit,\n'
        '         job_id=job_id, task_id=task_id, facts=exc.facts)',
        '    fail(code, exc.detail, json_output=json_output, exit_code=refusal_exit,\n'
        '         job_id=job_id, task_id=task_id)',
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
