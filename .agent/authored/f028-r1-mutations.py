"""F028 R1 G5 — mutation (red-proof) tool for the draft pass of a task injection
(DECISION F028 D1): S3's control-character admission, S4's terminal gate, the injected
id, S5's placement, S6's band mapping and shortfall-seed rounding, S7's fence flags, the
structured call's retry budget, and the unknown-`after` check's ordering before any call.

Takes a worktree path and, for each mutation below, edits
`packages/orchestration/task_injection.py` INSIDE that worktree (asserting its FROM text
occurs exactly once in the file at the time of the edit — every mutation starts from the
file's own pristine bytes, restored after the previous mutation), runs
`tests/orchestration/test_task_injection.py` from the worktree's root under pytest — after
purging every `__pycache__` directory under it, so a stale bytecode file cannot hide or
fake a result — then restores the file's exact original bytes. An unmutated CONTROL run
happens first and last. Every mutation is a real behaviour change the specification (S1 to
S8) forbids, and every one of them must turn at least one node red.

Usage:
    python3 -B mutations.py <worktree_path>
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

_TEST_PATH = "tests/orchestration/test_task_injection.py"
_MODULE = "packages/orchestration/task_injection.py"

#: (label, FROM text, TO text). FROM must occur exactly once in the file at the time of
#: the edit; every mutation starts from the file's own pristine bytes, restored after the
#: previous mutation.
MUTATIONS: tuple[tuple[str, str, str], ...] = (
    (
        "m1_s3_admits_bel_x07",
        '_CONTROL_CHAR_RE = re.compile(r"[\\x00-\\x08\\x0b-\\x1f\\x7f]")\n',
        '_CONTROL_CHAR_RE = re.compile(r"[\\x00-\\x06\\x08\\x0b-\\x1f\\x7f]")\n',
    ),
    (
        "m2_s4_answers_none_for_a_terminal_job",
        "    if job_is_terminal(job_state):\n",
        "    if False and job_is_terminal(job_state):\n",
    ),
    (
        "m3_next_injected_task_id_always_answers_inj1",
        "        if candidate not in existing:\n"
        "            return candidate\n"
        "        k += 1\n",
        '        return f"{INJECTED_TASK_ID_PREFIX}1"\n',
    ),
    (
        "m4_s5_ignores_after",
        "    if after is not None:\n"
        "        if after not in ids:\n",
        "    if False and after is not None:\n"
        "        if after not in ids:\n",
    ),
    (
        "m5_s5_never_finds_a_content_overlap",
        "    if overlap_ids:\n"
        "        return {\n"
        '            "depends_on": list(overlap_ids),\n',
        "    if False and overlap_ids:\n"
        "        return {\n"
        '            "depends_on": list(overlap_ids),\n',
    ),
    (
        "m6_xl_reads_as_token_band_high",
        '    "XL": TokenBand.UNKNOWN,\n',
        '    "XL": TokenBand.HIGH,\n',
    ),
    (
        "m7_a_shortfall_answer_carries_the_draft_id_as_its_confirm_token",
        '        "confirm_token": None if shortfall else draft_id,\n',
        '        "confirm_token": draft_id,\n',
    ),
    (
        "m8_extend_to_usd_rounds_down",
        '                Decimal("0.01"), rounding=ROUND_CEILING))\n',
        '                Decimal("0.01"), rounding="ROUND_FLOOR"))\n',
    ),
    (
        "m9_read_injection_draft_refuses_only_strictly_after_expires_at",
        "        if now_dt >= expires_dt:\n",
        "        if now_dt > expires_dt:\n",
    ),
    (
        "m10_s7_never_flags_a_deny_glob",
        "        if deny_glob is not None:\n",
        "        if False and deny_glob is not None:\n",
    ),
    (
        "m11_the_structured_call_runs_with_allow_parse_retry_false",
        "    outcome = run_structured_call(InjectedTaskDraft, prompt, call_fn)\n",
        "    outcome = run_structured_call(InjectedTaskDraft, prompt, call_fn, "
        "allow_parse_retry=False)\n",
    ),
    (
        "m12_the_unknown_after_check_runs_after_the_call_instead_of_before_it",
        "    try:\n"
        "        place_injected_task(plan.tasks, [], after=after)\n"
        "    except TaskInjectionRefused as exc:\n"
        '        return {"outcome": "refused", "code": exc.code, "detail": exc.detail}\n'
        "\n"
        "    if call_fn is None:\n"
        '        return {"outcome": "refused", "code": "planner_unavailable",\n'
        '                "detail": "no planner call is available to draft this task"}\n'
        "\n"
        "    prompt = compose_injection_prompt(validated_text, plan.tasks, after=after)\n"
        "    outcome = run_structured_call(InjectedTaskDraft, prompt, call_fn)\n"
        "    if not outcome.ok:\n"
        '        return {"outcome": "refused", "code": "draft_unparseable",\n'
        '                "detail": "the planner\'s draft reply could not be parsed as a '
        'task"}\n',
        "    if call_fn is None:\n"
        '        return {"outcome": "refused", "code": "planner_unavailable",\n'
        '                "detail": "no planner call is available to draft this task"}\n'
        "\n"
        "    prompt = compose_injection_prompt(validated_text, plan.tasks, after=after)\n"
        "    outcome = run_structured_call(InjectedTaskDraft, prompt, call_fn)\n"
        "    if not outcome.ok:\n"
        '        return {"outcome": "refused", "code": "draft_unparseable",\n'
        '                "detail": "the planner\'s draft reply could not be parsed as a '
        'task"}\n'
        "\n"
        "    try:\n"
        "        place_injected_task(plan.tasks, [], after=after)\n"
        "    except TaskInjectionRefused as exc:\n"
        '        return {"outcome": "refused", "code": exc.code, "detail": exc.detail}\n',
    ),
)


def _purge_pycache(root: Path) -> None:
    for cache_dir in root.rglob("__pycache__"):
        if cache_dir.is_dir():
            for child in sorted(cache_dir.rglob("*"), reverse=True):
                if child.is_file():
                    child.unlink()
                else:
                    child.rmdir()
            cache_dir.rmdir()


def _run_tests(root: Path) -> tuple[int, int, list[str]]:
    """Run the fixed test selection from `root`. Returns (exit_code, failed_count, node_ids)."""
    _purge_pycache(root)
    result = subprocess.run(
        [sys.executable, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider",
         "--tb=no", _TEST_PATH],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )
    failed_ids = [
        line[len("FAILED "):].split(" ", 1)[0]
        for line in result.stdout.splitlines()
        if line.startswith("FAILED ")
    ]
    return result.returncode, len(failed_ids), failed_ids


def main(worktree: str) -> bool:
    root = Path(worktree).resolve()
    target = root / _MODULE
    all_ok = True

    exit_code, failed_count, node_ids = _run_tests(root)
    control_ok = exit_code == 0 and failed_count == 0
    all_ok = all_ok and control_ok
    print(f"control (before): exit={exit_code} failed={failed_count} nodes={node_ids}")

    original_bytes = target.read_bytes()

    for label, from_text, to_text in MUTATIONS:
        text = original_bytes.decode("utf-8")
        occurrences = text.count(from_text)
        if occurrences != 1:
            raise AssertionError(
                f"{label}: FROM text occurs {occurrences} times in {_MODULE}, expected 1")
        mutated_text = text.replace(from_text, to_text, 1)
        target.write_bytes(mutated_text.encode("utf-8"))

        exit_code, failed_count, node_ids = _run_tests(root)
        caught = exit_code != 0 and failed_count >= 1
        all_ok = all_ok and caught
        print(f"{label}: exit={exit_code} failed={failed_count} nodes={node_ids}")
        if not caught:
            print(f"  {label}: STAYED GREEN — not caught by the test selection")

        target.write_bytes(original_bytes)

    restored = target.read_bytes() == original_bytes
    all_ok = all_ok and restored
    print(f"restored byte-identical: {restored} ({_MODULE})")

    exit_code, failed_count, node_ids = _run_tests(root)
    control_ok_after = exit_code == 0 and failed_count == 0
    all_ok = all_ok and control_ok_after
    print(f"control (after): exit={exit_code} failed={failed_count} nodes={node_ids}")

    print(f"ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: {all_ok}")
    return all_ok


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: mutations.py <worktree_path>")
    ok = main(sys.argv[1])
    raise SystemExit(0 if ok else 1)
