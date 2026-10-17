"""`remedy run show` never calls a run without a test result "tests failed" (lab add() order, 2026-10-17)."""
from __future__ import annotations

import pytest

from apps.cli.commands.run_report_cmd import _print_text_report


@pytest.mark.parametrize(("test_passed", "words"), [
    (None, "Remedy verification: tests not run in this run"),
    (True, "Remedy verification: tests passed"),
    (False, "Remedy verification: tests failed"),
])
def test_the_verification_line_says_what_the_run_measured(capsys, test_passed, words):
    _print_text_report("r1", {"goal": "g", "final_status": "staged_review_passed",
                              "rounds": [{"builder": {}, "test_passed": test_passed}]})

    assert words in capsys.readouterr().out.splitlines()
