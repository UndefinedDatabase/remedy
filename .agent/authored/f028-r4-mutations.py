"""F028 R4 G5 — mutation (red-proof) tool for the command line: `job inject`,
`job inject-confirm`, `job inject-answer`, the `--yes` audit mark, the shared budget and
planner helpers, and the extension's amount recomputed at answer time.

Takes a worktree path and, for each mutation below, edits the named file INSIDE that
worktree (asserting its FROM text occurs exactly once in the file at the time of the edit
— every mutation starts from the file's own pristine bytes, restored after the previous
mutation to THAT file), runs `tests/cli/test_job_inject.py` and
`tests/orchestration/test_task_injection.py` from the worktree's root under pytest — after
purging every `__pycache__` directory under it, so a stale bytecode file cannot hide or
fake a result — then restores the file's exact original bytes. An unmutated CONTROL run
happens first and last. Every mutation is a real behaviour change S1 to S5 forbid, and
every one of them must turn at least one node red.

Usage:
    python3 -B mutations.py <worktree_path>
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

_TEST_PATHS = (
    "tests/cli/test_job_inject.py",
    "tests/orchestration/test_task_injection.py",
)

_JOB_INJECT_CMD = "apps/cli/commands/job_inject_cmd.py"
_TASK_INJECTION = "packages/orchestration/task_injection.py"

#: (label, file, FROM text, TO text). FROM must occur exactly once in the file at the time of
#: the edit; every mutation starts from the file's own pristine bytes, restored after the
#: previous mutation to THAT file.
MUTATIONS: tuple[tuple[str, str, str, str], ...] = (
    (
        "m1_text_invalid_leaves_the_usage_class",
        _JOB_INJECT_CMD,
        '    "text_required", "text_too_long", "text_invalid", "unknown_task",\n'
        '    "unknown_option", "cannot_shrink",\n',
        '    "text_required", "text_too_long", "unknown_task",\n'
        '    "unknown_option", "cannot_shrink",\n',
    ),
    (
        "m2_draft_unknown_leaves_the_not_ready_class",
        _JOB_INJECT_CMD,
        '    "budget_unreadable", "draft_unknown", "draft_expired", "draft_needs_decision",\n',
        '    "budget_unreadable", "draft_expired", "draft_needs_decision",\n',
    ),
    (
        "m3_yes_over_a_shortfall_exits_0",
        _JOB_INJECT_CMD,
        '        if yes:\n'
        '            fail("draft_needs_decision",\n',
        '        if False:\n'
        '            fail("draft_needs_decision",\n',
    ),
    (
        "m4_yes_confirms_with_unseen_false",
        _JOB_INJECT_CMD,
        '            job, answer["confirm_token"], actor=CLI_ACTOR, unseen=True)\n',
        '            job, answer["confirm_token"], actor=CLI_ACTOR, unseen=False)\n',
    ),
    (
        "m5_after_passes_the_entrys_own_id_instead_of_its_planned_id",
        _JOB_INJECT_CMD,
        '    planned_id = (entry.inputs.get("plan") or {}).get("planned_id")\n'
        '    return planned_id if planned_id else after_arg\n',
        '    return resolved\n',
    ),
    (
        "m6_the_drafted_output_omits_the_confirm_line",
        _JOB_INJECT_CMD,
        '    token = answer["confirm_token"]\n'
        '    print(f"Confirm it with: remedy job inject-confirm {job_id} {token}")\n',
        '    token = answer["confirm_token"]\n'
        '    _ = token  # the confirm line is not printed\n',
    ),
    (
        "m7_the_confirmation_stores_confirmed_unseen_false_always",
        _TASK_INJECTION,
        '        # DECISION F028 D4 (2): True only for an unattended `--yes` confirmation.\n'
        '        "confirmed_unseen": bool(unseen),\n',
        '        # DECISION F028 D4 (2): True only for an unattended `--yes` confirmation.\n'
        '        "confirmed_unseen": False,\n',
    ),
    (
        "m8_the_injection_block_omits_confirmed_unseen",
        _TASK_INJECTION,
        '        # DECISION F028 D4 (2): carried from the confirmation, False for one lacking '
        'the\n'
        '        # key at all (a record round 2 or round 3 wrote, before this field existed).\n'
        '        "confirmed_unseen": record.get("confirmed_unseen", False),\n'
        '        "dod_resync_pending": dod_resync_pending,\n',
        '        "dod_resync_pending": dod_resync_pending,\n',
    ),
    (
        "m9_extend_budget_takes_the_seeds_amount_alone",
        _TASK_INJECTION,
        '        if fresh_spent is not None and fresh_expected is not None:\n'
        '            recomputed_extend_to_usd = float(\n'
        '                Decimal(repr(round(fresh_spent + fresh_expected, 6))).quantize(\n'
        '                    Decimal("0.01"), rounding=ROUND_CEILING))\n'
        '            extend_to_usd = max(recomputed_extend_to_usd, seed["extend_to_usd"])\n'
        '        else:\n'
        '            extend_to_usd = seed["extend_to_usd"]\n',
        '        extend_to_usd = seed["extend_to_usd"]\n',
    ),
    (
        "m10_injection_budget_inputs_answers_budgetcounters_for_undecodable_actuals",
        _TASK_INJECTION,
        '    except (ValidationError, budget_guard.BudgetCounterError, ValueError, '
        'TypeError) as exc:\n'
        '        raise TaskInjectionRefused(\n'
        '            "budget_unreadable", f"this job\'s budget state cannot be read: '
        '{exc}") from exc\n',
        '    except (ValidationError, budget_guard.BudgetCounterError, ValueError, TypeError):\n'
        '        counters = budget_guard.BudgetCounters()\n',
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
