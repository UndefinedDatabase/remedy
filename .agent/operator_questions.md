# Operator questions — what the loop needs decodeux to know or decide

> Written per `docs/agents/self_drive_protocol.md`, operator amendment
> amend0911-feedback rule C (2026-09-11). Read by `remedy-decisions` on the
> operator's machine and by the orchestrator at every relay. Every entry's body
> stands alone in plain sentences; the heading carries the technical reference.
> Soft cap five; entries leave only by the operator's answer, recorded as a dated
> DECISION by the operator's next amendment, which deletes the entry.

### Q17 — Two sessions shared one checkout (2026-10-13, F058, round 7)

**What needs deciding.** While the loop was closing the model failover feature, a second session
working on cockpit access from the home network switched the one shared working copy to its own
branch, made two commits there and opened its own pull request. Please decide whether such side
work should run in a separate copy of the repository from now on, and whether the next loop session
may merge that pull request first, as its usual rule for a single open pull request says.

**Why it matters.** The loop and any other session read and write the same folder. A switch in the
middle of a loop step can make a test run read a mix of two branches, and two finished branches
that both change the same notes and configuration files must be brought together by hand. This
time nothing was mixed up, because the loop's evidence run had finished ten minutes before the
switch, but the loop had to stop early, and the failover feature now needs its full test run once
more after the merge.

**My recommendation.** Let the next loop session merge the cockpit pull request first, as its
normal rule already says, then bring the failover feature up to date and finish it. For future side
work while the loop runs, use a separate copy of the repository, or pause the loop first.

**What happens if you say nothing.** The recommendation is already in place and stands until you
say otherwise: the next session merges the cockpit pull request, brings the failover feature up to
date, runs the whole test collection once more and closes the feature.
