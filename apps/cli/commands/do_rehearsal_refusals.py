"""F055 — `--rehearse` is refused, before any step, together with a flag that would answer,
apply, commit or push a job it deliberately never runs (DECISION F055 D1).
"""

from __future__ import annotations

from apps.cli.json_envelope import fail


# WHY: a rehearsal's whole point is a plan whose approval stays open for a person to answer; a
# flag that would approve, apply, commit or push it is refused before any step, naming the clash.
def refuse_rehearsal_conflicts(*, rehearse: bool, yes: bool, apply: bool, commit: str | None,
                               commit_auto: bool, commit_with_history: bool, push: bool,
                               json_output: bool) -> None:
    """Exit 2 before any step when `--rehearse` is given with `--yes` or a commit/apply/push flag."""
    if not rehearse:
        return
    if yes:
        fail("invalid_argument",
             "--rehearse leaves the plan's approval open for you to answer, and --yes would approve it unattended. Nothing was run.",
             json_output=json_output, exit_code=2)
    given_flags = []
    if apply:
        given_flags.append("--apply")
    if commit is not None:
        given_flags.append("--commit")
    if commit_auto:
        given_flags.append("--commit-auto")
    if commit_with_history:
        given_flags.append("--commit-with-history")
    if push:
        given_flags.append("--push")
    if given_flags:
        given = " and ".join(given_flags)
        fail("invalid_argument",
             f"--rehearse runs no job, so {given} would have nothing to apply, commit or push. Nothing was run.",
             json_output=json_output, exit_code=2)
