"""F289 R1 G5 — mutation (red-proof) tool for T002's specification and tests.

Takes a worktree path and, for each mutation below, edits the named module
INSIDE that worktree (asserting its FROM text occurs exactly once in the
file), runs the worktree's own
`tests/cli/test_worker_facade_cmd.py`, `tests/orchestration/test_self_use_generator.py`
and `tests/orchestration/test_diff_parser.py` under pytest from the worktree's
root — after purging every `__pycache__` directory under it, so a stale
bytecode file cannot hide or fake a result — then restores the file's exact
original bytes. An unmutated CONTROL run happens first and last. Every
mutation is a real behaviour change the specification (S2 to S6) or R-1073's
guard (S1) forbids, and every one of them must turn at least one node red.

Usage:
    python3 -B f289-r1-mutations.py <worktree_path>
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

#: Run together for the control and for every mutation, from the worktree's root.
_TEST_PATHS = (
    "tests/cli/test_worker_facade_cmd.py",
    "tests/orchestration/test_self_use_generator.py",
    "tests/orchestration/test_diff_parser.py",
)

_WORKER_FACADE = "apps/cli/commands/worker_facade_cmd.py"
_SELF_USE_GENERATOR = "packages/orchestration/self_use_generator.py"
_DIFF_PARSER = "packages/orchestration/diff_parser.py"

#: (label, relative file path, FROM text, TO text). FROM must occur exactly
#: once in the file at the time of the edit; every mutation starts from the
#: file's own pristine bytes, restored after the previous mutation.
MUTATIONS: tuple[tuple[str, str, str, str], ...] = (
    (
        "m1_doctor_warning_as_json_also_writes_subject",
        _WORKER_FACADE,
        'return {"warning": self.warning, "summary": self.summary, "detail": self.detail}',
        'return {"warning": self.warning, "summary": self.summary, "detail": self.detail, '
        '"subject": self.subject}',
    ),
    (
        "m2_dead_builtin_model_warning_carries_no_repair_path",
        _WORKER_FACADE,
        "subject=model_id, repair_path=MODEL_ALIAS_TABLE_PATH)",
        "subject=model_id)",
    ),
    (
        "m3_dead_configured_model_warning_carries_the_alias_table_repair_path",
        _WORKER_FACADE,
        "subject=value)",
        "subject=value, repair_path=MODEL_ALIAS_TABLE_PATH)",
    ),
    (
        "m4_unknown_env_variable_warning_carries_no_subject",
        _WORKER_FACADE,
        'f"{ENVIRONMENT_GUIDE_PATH}.",\n              subject=name)',
        'f"{ENVIRONMENT_GUIDE_PATH}.")',
    ),
    (
        "m5_doctor_core_report_as_json_writes_warnings_before_blockers",
        _WORKER_FACADE,
        '            "blockers": self.blockers,\n'
        '            "warnings": [warning.as_json() for warning in self.warnings],\n',
        '            "warnings": [warning.as_json() for warning in self.warnings],\n'
        '            "blockers": self.blockers,\n',
    ),
    (
        "m6_tier_3_ignores_the_keys_the_queue_already_targets",
        _SELF_USE_GENERATOR,
        "    warning = next(\n"
        "        (w for w in report.actionable_warnings()\n"
        '         if f"{w.warning}:{w.subject}" not in targeted),\n'
        "        None,\n"
        "    )\n",
        "    warning = next(\n"
        "        (w for w in report.actionable_warnings()\n"
        "         if True),\n"
        "        None,\n"
        "    )\n",
    ),
    (
        "m7_tier_3_offers_the_last_actionable_warning_instead_of_the_first",
        _SELF_USE_GENERATOR,
        "    warning = next(\n"
        "        (w for w in report.actionable_warnings()\n"
        '         if f"{w.warning}:{w.subject}" not in targeted),\n'
        "        None,\n"
        "    )\n",
        "    warning = next(\n"
        "        (w for w in reversed(report.actionable_warnings())\n"
        '         if f"{w.warning}:{w.subject}" not in targeted),\n'
        "        None,\n"
        "    )\n",
    ),
    (
        "m8_tier_3_accepts_a_detail_holding_a_heading_line",
        _SELF_USE_GENERATOR,
        '    if re.search(r"^## ", warning.detail, re.M) or re.search(\n'
        '        r"^Acceptance\\s*:", warning.detail, re.M | re.I\n'
        "    ):\n",
        "    if False or re.search(\n"
        '        r"^Acceptance\\s*:", warning.detail, re.M | re.I\n'
        "    ):\n",
    ),
    (
        "m9_tier_3_writes_the_summary_as_the_task_body_instead_of_the_detail",
        _SELF_USE_GENERATOR,
        '        "## Task 1\\n"\n'
        '        f"{warning.detail}\\n"\n',
        '        "## Task 1\\n"\n'
        '        f"{warning.summary}\\n"\n',
    ),
    (
        "m10_generate_self_use_item_tries_tier_3_before_the_ledger_tier",
        _SELF_USE_GENERATOR,
        "    ledger_result = _ledger_tier(queue_path, ledger)\n"
        "    if ledger_result is not None:\n"
        "        return ledger_result\n"
        "\n"
        "    doc_result = _doc_staleness_tier(queue_path)\n"
        "    if doc_result is not None:\n"
        "        return doc_result\n"
        "\n"
        "    return _doctor_warning_tier(queue_path)\n",
        "    doctor_result = _doctor_warning_tier(queue_path)\n"
        "    if doctor_result is not None:\n"
        "        return doctor_result\n"
        "\n"
        "    ledger_result = _ledger_tier(queue_path, ledger)\n"
        "    if ledger_result is not None:\n"
        "        return ledger_result\n"
        "\n"
        "    doc_result = _doc_staleness_tier(queue_path)\n"
        "    if doc_result is not None:\n"
        "        return doc_result\n"
        "\n"
        "    return None\n",
    ),
    (
        "m11_tier_3_offers_a_warning_that_is_not_actionable",
        _SELF_USE_GENERATOR,
        "    warning = next(\n"
        "        (w for w in report.actionable_warnings()\n"
        '         if f"{w.warning}:{w.subject}" not in targeted),\n'
        "        None,\n"
        "    )\n",
        "    warning = next(\n"
        "        (w for w in report.warnings\n"
        '         if f"{w.warning}:{w.subject}" not in targeted),\n'
        "        None,\n"
        "    )\n",
    ),
    (
        "m12_diff_parser_does_quadratic_work_per_body_line",
        _DIFF_PARSER,
        "                body_lines_appended += 1\n",
        "                body_lines_appended += 1\n"
        "                _ = sum(range(body_lines_appended))\n",
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
    for _label, rel_path, _from_text, _to_text in MUTATIONS:
        if rel_path not in originals:
            originals[rel_path] = (root / rel_path).read_bytes()

    for label, rel_path, from_text, to_text in MUTATIONS:
        target = root / rel_path
        original_bytes = originals[rel_path]
        text = original_bytes.decode("utf-8")
        occurrences = text.count(from_text)
        if occurrences != 1:
            raise AssertionError(
                f"{label}: FROM text occurs {occurrences} times in {rel_path}, expected 1"
            )
        mutated_text = text.replace(from_text, to_text, 1)
        target.write_bytes(mutated_text.encode("utf-8"))

        exit_code, failed_count, node_ids = _run_tests(root)
        caught = exit_code != 0 and failed_count >= 1
        all_ok = all_ok and caught
        print(f"{label}: exit={exit_code} failed={failed_count} nodes={node_ids}")
        if not caught:
            print(f"  {label}: STAYED GREEN — not caught by the test selection")

        target.write_bytes(original_bytes)

    for rel_path, original_bytes in originals.items():
        restored = (root / rel_path).read_bytes() == original_bytes
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
        raise SystemExit("usage: f289-r1-mutations.py <worktree_path>")
    ok = main(sys.argv[1])
    raise SystemExit(0 if ok else 1)
