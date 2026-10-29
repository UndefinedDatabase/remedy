"""What a review may hold against a builder (operator order beweis).

F326: the builder may run only the commands of `claude_cli_command.builder_allowed_commands`. A
reviewer that blocks because a command outside that list did not run blocks the builder for
something it was not allowed to do, so the reviewer's system prompt names the list
(`REVIEWER_SCOPE_RULES`) and `settle_review_findings` lowers a finding that only says such a
command did not run to `low`, decided here in code and not left to the reviewer's words.

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


def settle_review_findings(reviewer_out: ReviewerOutput, *, staged_files: list[str], is_fake: bool,
                           workspace: str | None, job_task: tuple[str, str] = ("", "")) -> ReviewerOutput:
    """REVIEWER_OUT after the rules the code decides, not the reviewer's words.

    The empty diff outvotes a verdict first (`reject_verdict_on_empty_diff`), unless JOB_TASK (the job's
    and the task's id) names a task whose work an earlier task of its job already did (F332). Then each finding
    that only says a command outside the builder's list for WORKSPACE did not run reads `low`
    (F326).
    """
    already_done = not staged_files and not is_fake and earlier_work_of(*job_task) is not None
    reviewer_out = reject_verdict_on_empty_diff(reviewer_out, staged_files=staged_files, is_fake=is_fake,
                                                already_done=already_done)
    allowed = builder_allowed_commands(workspace)
    for finding in reviewer_out.findings:
        if finding.severity != "low" and only_disallowed_command_not_run(finding, allowed):
            finding.severity = "low"
    return reviewer_out
