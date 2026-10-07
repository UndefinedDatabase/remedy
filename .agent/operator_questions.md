# Operator questions — what the loop needs decodeux to know or decide

> Written per `docs/agents/self_drive_protocol.md`, operator amendment
> amend0911-feedback rule C (2026-09-11). Read by `remedy-decisions` on the
> operator's machine and by the orchestrator at every relay. Every entry's body
> stands alone in plain sentences; the heading carries the technical reference.
> Soft cap five; entries leave only by the operator's answer, recorded as a dated
> DECISION by the operator's next amendment, which deletes the entry.

### Q6 — Another program used the loop's checkout (2026-10-07, F295, round 24)

**What needs deciding.** The loop builds Remedy in one folder on your machine, the main copy of
the repository. This morning, while the loop was running Remedy's whole test suite one last time
before closing the current feature, something outside the loop switched that folder to the main
line and then to a new branch about documenting the Claude subscription binding. That happened 14
seconds before the test run ended. The loop's helper noticed it afterwards. It put its own saved
result back on the loop's branch, and it moved that new branch back to the exact point where it
had been created, so the new branch lost nothing and was never sent to the server. I need to know
whether you or another tool now work in that same folder, so that the loop does not trip over it
again.

**Why it matters.** Two programs that work in one folder at the same time change each other's
files without warning. The test run was green, but for its last seconds it partly tested the main
line's code instead of the code that will ship, so the loop does not count it as the final run.
The steps still ahead, the repeated test run and the review package, would be spoiled the same way
by another switch. The loop also moved a branch that was not its own, which it normally never
does, even though it only undid its own stray change there.

**My recommendation.** Do other work in a second folder of the repository instead of the loop's
folder; git can make one with its worktree command. The loop will repeat the final test run once,
in a quiet folder, and check before and after the run that nobody switched branches.

**What happens if you say nothing.** The recommendation is already executed and stands until you
say otherwise: the next session repeats the final test run once, watches for another switch, and
stops again with a note if it sees one. Nothing else waits for you.
