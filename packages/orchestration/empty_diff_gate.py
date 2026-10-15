"""The empty staged diff outvotes a reviewer's words (R-0999; operator amendment amend1014b, D3)."""
from __future__ import annotations

from packages.orchestration.pingpong_provider import ReviewerOutput


def reject_verdict_on_empty_diff(
    reviewer_out: ReviewerOutput, *, staged_files: list[str], is_fake: bool,
) -> ReviewerOutput:
    """The empty staged diff is the evidence; a reviewer's words cannot outvote it.

    A failing verdict with no finding takes the empty-change finding (R-0999). Since operator
    amendment amend1014b D3 a PASS on an empty diff is rejected the same way, before the task
    can complete: it becomes needs_repair, the repair loop gets its second try, and
    `no_file_changed` stays as the final defense. A fake builder is exempt, as everywhere in
    this loop, because it writes its changes after this point of a round; so is a single run
    (`remedy run`), which may still end a clean `builder_no_changes`: only a job task is
    what a job applies.
    """
    if staged_files:
        return reviewer_out
    if reviewer_out.verdict == "pass" and not is_fake:
        reviewer_out.verdict = "needs_repair"
        reviewer_out.findings = list(reviewer_out.findings) or [
            _empty_change_finding(reviewer_out.summary)]
    elif not reviewer_out.findings and reviewer_out.verdict in ("needs_repair", "fail"):
        reviewer_out.findings = [_empty_change_finding(reviewer_out.summary)]
    return reviewer_out


def _empty_change_finding(summary: str):
    # Imported when called: the loop imports this module, so a module-level import would cycle.
    from packages.orchestration.pingpong_loop import empty_change_finding

    return empty_change_finding(summary)
