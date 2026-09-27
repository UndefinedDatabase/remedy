"""F028 R3 G5 — mutation (red-proof) tool for R-1077's repair and DECISION F028 D3: the
confirmed-record field validation, the shortfall answer's refusal ladder, `shrink_task`'s and
`extend_budget`'s derived drafts, the extension's raise-never-create-never-lower rule, and the
runner's re-read of `job.budgets` after a fold that changed them.

Takes a worktree path and, for each mutation below, edits the named file INSIDE that worktree
(asserting its FROM text occurs exactly once in the file at the time of the edit — every
mutation starts from the file's own pristine bytes, restored after the previous mutation to
THAT file), runs `tests/orchestration/test_task_injection.py` and
`tests/orchestration/test_task_injection_runner.py` from the worktree's root under pytest —
after purging every `__pycache__` directory under it, so a stale bytecode file cannot hide or
fake a result — then restores the file's exact original bytes. An unmutated CONTROL run happens
first and last. Every mutation is a real behaviour change S1 to S5 forbid, and every one of
them must turn at least one node red.

Usage:
    python3 -B mutations.py <worktree_path>
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

_TEST_PATHS = (
    "tests/orchestration/test_task_injection.py",
    "tests/orchestration/test_task_injection_runner.py",
)

_TASK_INJECTION = "packages/orchestration/task_injection.py"
_PINGPONG_JOB = "packages/orchestration/pingpong_job.py"

#: (label, file, FROM text, TO text). FROM must occur exactly once in the file at the time of
#: the edit; every mutation starts from the file's own pristine bytes, restored after the
#: previous mutation to THAT file.
MUTATIONS: tuple[tuple[str, str, str, str], ...] = (
    (
        "m1_confirmed_injections_accepts_a_record_lacking_text",
        _TASK_INJECTION,
        '    for field in ("task_rationale", "text", "actor", "confirmed_at"):\n'
        '        if not isinstance(record.get(field), str):\n'
        '            raise TaskInjectionError(f"a confirmed task injection entry carries no '
        '{field}")\n',
        '    for field in ("task_rationale", "actor", "confirmed_at"):\n'
        '        if not isinstance(record.get(field), str):\n'
        '            raise TaskInjectionError(f"a confirmed task injection entry carries no '
        '{field}")\n',
    ),
    (
        "m2_apply_injection_to_job_lowers_a_higher_limit_to_the_extension",
        _TASK_INJECTION,
        '    if (extend_to_usd is not None and isinstance(job.budgets, dict)\n'
        '            and job.budgets.get("max_cost_usd") is not None\n'
        '            and job.budgets["max_cost_usd"] < extend_to_usd):\n'
        '        new_budgets = dict(job.budgets)\n'
        '        new_budgets["max_cost_usd"] = extend_to_usd\n',
        '    if (extend_to_usd is not None and isinstance(job.budgets, dict)\n'
        '            and job.budgets.get("max_cost_usd") is not None):\n'
        '        new_budgets = dict(job.budgets)\n'
        '        new_budgets["max_cost_usd"] = extend_to_usd\n',
    ),
    (
        "m3_apply_injection_to_job_creates_a_limit_on_a_job_that_has_none",
        _TASK_INJECTION,
        '    if (extend_to_usd is not None and isinstance(job.budgets, dict)\n'
        '            and job.budgets.get("max_cost_usd") is not None\n'
        '            and job.budgets["max_cost_usd"] < extend_to_usd):\n'
        '        new_budgets = dict(job.budgets)\n'
        '        new_budgets["max_cost_usd"] = extend_to_usd\n',
        '    if extend_to_usd is not None:\n'
        '        new_budgets = dict(job.budgets) if isinstance(job.budgets, dict) else {}\n'
        '        new_budgets["max_cost_usd"] = extend_to_usd\n',
    ),
    (
        "m4_answer_injection_shortfall_skips_the_needs_decision_status_check",
        _TASK_INJECTION,
        '    if record.get("status") != "needs_decision":\n'
        '        return {"outcome": "refused", "code": "draft_not_in_shortfall",\n'
        '                "detail": "this injection draft is not awaiting a shortfall '
        'decision"}\n',
        '    if False and record.get("status") != "needs_decision":\n'
        '        return {"outcome": "refused", "code": "draft_not_in_shortfall",\n'
        '                "detail": "this injection draft is not awaiting a shortfall '
        'decision"}\n',
    ),
    (
        "m5_shrink_task_derives_its_draft_at_the_old_band",
        _TASK_INJECTION,
        '    if option == "shrink_task":\n'
        '        shrink_band = seed["shrink_band"]\n'
        '        task["est_tokens_band"] = shrink_band\n'
        '        check = injection_budget_check(budgets, counters, band=shrink_band, '
        'config=config)\n',
        '    if option == "shrink_task":\n'
        '        shrink_band = seed["shrink_band"]\n'
        '        check = injection_budget_check(budgets, counters, band=shrink_band, '
        'config=config)\n',
    ),
    (
        "m6_cannot_shrink_is_checked_only_after_the_answer_file_is_published",
        _TASK_INJECTION,
        '    seed = record.get("decision_seed") or {}\n'
        '    if option == "shrink_task" and seed.get("shrink_band") is None:\n'
        '        return {"outcome": "refused", "code": "cannot_shrink",\n'
        '                "detail": "this task is already at the smallest size; it cannot '
        'shrink"}\n',
        '    seed = record.get("decision_seed") or {}\n',
    ),
    (
        "m7_the_extend_budget_draft_carries_budget_extend_to_usd_none",
        _TASK_INJECTION,
        '        shortfall = False\n'
        '        budget_extend_to_usd = extend_to_usd\n',
        '        shortfall = False\n'
        '        budget_extend_to_usd = None\n',
    ),
    (
        "m8_the_extend_budget_check_is_computed_over_the_old_limit",
        _TASK_INJECTION,
        '        extended_budgets = budgets.model_copy(update={"max_cost_usd": '
        'extend_to_usd})\n'
        '        check = injection_budget_check(\n'
        '            extended_budgets, counters, band=task["est_tokens_band"], '
        'config=config)\n',
        '        extended_budgets = budgets.model_copy(update={"max_cost_usd": '
        'extend_to_usd})\n'
        '        check = injection_budget_check(\n'
        '            budgets, counters, band=task["est_tokens_band"], config=config)\n',
    ),
    (
        "m9_confirm_task_injection_drops_budget_extend_to_usd",
        _TASK_INJECTION,
        '        "confirmed_at": now_dt.isoformat(),\n'
        '        # DECISION F028 D3 (2): carried from the draft, None when the draft never '
        'named an\n'
        '        # extension, into the fold\'s own reading of `apply_injection_to_job`.\n'
        '        "budget_extend_to_usd": record.get("budget_extend_to_usd"),\n'
        '    }\n',
        '        "confirmed_at": now_dt.isoformat(),\n'
        '    }\n',
    ),
    (
        "m10_the_extend_budget_label_names_no_amount",
        _TASK_INJECTION,
        '    option_labels = {\n'
        '        "extend_budget": f"Raise the job\'s cost limit to ${extend_to_usd:.2f} and '
        'add the task.",\n'
        '        "shrink_task": shrink_label,\n'
        '        "drop": "Drop this task and add nothing to the job.",\n'
        '    }\n',
        '    option_labels = {\n'
        '        "extend_budget": "Raise the job\'s cost limit and add the task.",\n'
        '        "shrink_task": shrink_label,\n'
        '        "drop": "Drop this task and add nothing to the job.",\n'
        '    }\n',
    ),
    (
        "m11_fold_injections_here_never_rebinds_job_budgets",
        _PINGPONG_JOB,
        '            if job.budgets != _budgets_before:\n',
        '            if False and job.budgets != _budgets_before:\n',
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
         "--tb=no", *_TEST_PATHS],
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
    all_ok = True

    exit_code, failed_count, node_ids = _run_tests(root)
    control_ok = exit_code == 0 and failed_count == 0
    all_ok = all_ok and control_ok
    print(f"control (before): exit={exit_code} failed={failed_count} nodes={node_ids}")

    originals: dict[str, bytes] = {}
    for _, rel_path, _, _ in MUTATIONS:
        if rel_path not in originals:
            originals[rel_path] = (root / rel_path).read_bytes()

    for label, rel_path, from_text, to_text in MUTATIONS:
        target = root / rel_path
        pristine = originals[rel_path]
        text = pristine.decode("utf-8")
        occurrences = text.count(from_text)
        if occurrences != 1:
            raise AssertionError(
                f"{label}: FROM text occurs {occurrences} times in {rel_path}, expected 1")
        mutated_text = text.replace(from_text, to_text, 1)
        target.write_bytes(mutated_text.encode("utf-8"))

        exit_code, failed_count, node_ids = _run_tests(root)
        caught = exit_code != 0 and failed_count >= 1
        all_ok = all_ok and caught
        print(f"{label} ({rel_path}): exit={exit_code} failed={failed_count} nodes={node_ids}")
        if not caught:
            print(f"  {label}: STAYED GREEN — not caught by the test selection")

        target.write_bytes(pristine)

    for rel_path, pristine in originals.items():
        restored = (root / rel_path).read_bytes() == pristine
        all_ok = all_ok and restored
        print(f"restored byte-identical: {restored} ({rel_path})")

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
