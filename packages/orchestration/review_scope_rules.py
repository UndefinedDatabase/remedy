"""What a review may hold against a builder (operator order beweis).

F326: the builder may run only the commands of `claude_cli_command.builder_allowed_commands`. A
reviewer that blocks because a command outside that list did not run blocks the builder for
something it was not allowed to do, so the reviewer's system prompt names the list
(`REVIEWER_SCOPE_RULES`) and `settle_review_findings` lowers a finding that only says such a
command did not run to `low`, decided here in code and not left to the reviewer's words.

F333: a finding only about tests that already failed on the job's base commit reads `low` too
(`only_preexisting_failures`); the reviewer is told them as a fact in the round's test summary.

F330: the same rules ask the reviewer to say, by a finding of kind `not_in_this_repository`, when
the task's work does not belong in this repository at all (`job_wrong_repository`).
"""
from __future__ import annotations

import re

from packages.orchestration.claude_cli_command import (
    BUILDER_CHECK_SCRIPT_PREFIXES,
    BUILDER_PYTHON_CHECKERS,
    builder_allowed_commands,
    builder_command_allowed,
)
from packages.orchestration.empty_diff_gate import reject_verdict_on_empty_diff
from packages.orchestration.job_task_already_done import earlier_work_of
from packages.orchestration.job_wrong_repository import NOT_IN_THIS_REPOSITORY
from packages.orchestration.pingpong_provider import ReviewerOutput
from packages.orchestration.project_test_baseline import preexisting_failures_in

#: F326: the reviewer's rule on the builder's commands; F330: the finding kind for work not in this repository.
REVIEWER_SCOPE_RULES = (
    "The builder may run only the project's test commands, git status, git diff, git log, ls, cat, "
    "head, tail, wc, grep, rg, py_compile, the package.json scripts whose names begin with "
    + ", ".join(BUILDER_CHECK_SCRIPT_PREFIXES[:-1]) + f" or {BUILDER_CHECK_SCRIPT_PREFIXES[-1]}, tsc, and "
    + ", ".join(BUILDER_PYTHON_CHECKERS[:-1]) + f" or {BUILDER_PYTHON_CHECKERS[-1]} when pyproject.toml "
    "names them. A command outside this list that did not run is no finding against the builder.\n"
    "When the task's work does not belong in this repository at all, answer the verdict blocked with one "
    f"finding whose kind is {NOT_IN_THIS_REPOSITORY} and whose summary names the repository it belongs in "
    "and why.\n"
)

#: A finding's words that say a command did not run.
_NOT_RUN = re.compile(
    r"\b(?:not|never|no|without|didn't|did not|wasn't|was not|were not|hasn't|has not|missing)\b"
    r"[^.;]{0,60}?\b(?:run|ran|executed|invoked|output|evidence)\b"
    r"|\b(?:run|execute)\b[^.;]{0,40}?\bbefore\b", re.IGNORECASE)
#: The commands a finding names: a span in backticks, else a runner word with what follows it.
_BACKTICKED = re.compile(r"`([^`\n]{2,120})`")
_RUNNER_WORDS = re.compile(
    r"\b((?:pnpm|npm|npx|yarn|tsc|ruff|mypy|pyright|eslint|make|cargo|go|pytest|vitest|playwright)"
    r"(?:\s+(?:run|exec))?(?:\s+[\w:./-]+)?)")


def finding_named_commands(text: str) -> list[str]:
    """The commands TEXT names: its spans in backticks, else the runner words it uses."""
    spans = [span.strip() for span in _BACKTICKED.findall(text)]
    return spans or [match.strip() for match in _RUNNER_WORDS.findall(text)]


def only_disallowed_command_not_run(finding: object, allowed: tuple[str, ...]) -> bool:
    """True when FINDING says a command did not run and every command it names is outside ALLOWED."""
    text = " ".join(str(getattr(finding, name, "") or "") for name in ("summary", "required_fix"))
    if not _NOT_RUN.search(text):
        return False
    named = finding_named_commands(text)
    return bool(named) and not any(builder_command_allowed(command, allowed) for command in named)


#: F333: a finding's words that say the tests or the test command fail.
_TESTS_RED = re.compile(
    r"\b(?:tests?|test command|test suite|vitest|pytest|jest)\b[^.;]{0,80}?"
    r"\b(?:fail\w*|red|exit(?:s|ed)?\s+(?:with\s+)?(?:code\s+)?[1-9]\d*)", re.IGNORECASE)


def only_preexisting_failures(finding: object, preexisting: frozenset[str]) -> bool:
    """F333: True when FINDING is about failing tests every one of which already failed on the job's
    base commit (PREEXISTING, the last red run of the workspace): its file is one of their files, its
    words name one of them, or its words only say the tests fail."""
    if not preexisting:
        return False
    files = {name.split("::")[0].split(" > ")[0].strip() for name in preexisting}
    text = " ".join(str(getattr(finding, name, "") or "") for name in ("summary", "details", "required_fix"))
    if str(getattr(finding, "file", "") or "") in files or any(part in text for part in files | preexisting):
        return True
    return bool(_TESTS_RED.search(text))


def settle_review_findings(reviewer_out: ReviewerOutput, *, staged_files: list[str], is_fake: bool,
                           workspace: str | None, job_task: tuple[str, str] = ("", "")) -> ReviewerOutput:
    """REVIEWER_OUT after the rules the code decides, not the reviewer's words.

    The empty diff outvotes a verdict first (`reject_verdict_on_empty_diff`), unless JOB_TASK (the job's
    and the task's id) names a task whose work an earlier task of its job already did (F332). Each
    finding that only says a command outside the builder's list for WORKSPACE did not run reads `low`
    (F326), and so does one only about tests already red on the job's base commit (F333); both are
    read before the empty diff, so a task already done whose only findings were those passes.
    """
    allowed = builder_allowed_commands(workspace)
    preexisting = preexisting_failures_in(workspace)
    for finding in reviewer_out.findings:
        if finding.severity != "low" and (only_disallowed_command_not_run(finding, allowed)
                                          or only_preexisting_failures(finding, preexisting)):
            finding.severity = "low"
    already_done = not staged_files and not is_fake and earlier_work_of(*job_task) is not None
    return reject_verdict_on_empty_diff(reviewer_out, staged_files=staged_files, is_fake=is_fake,
                                        already_done=already_done)
