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

### Q7 — A shaky test blocks the merge (2026-10-07, F295, round 30)

**What needs deciding.** The feature that lets a program drive Remedy without a person at the
keyboard is finished, and its pull request waits to be merged into the main line. GitHub runs the
whole test suite for every pull request on two Python versions. On the newer version, one test
failed twice in a row, each time in a different way. That test starts a small job, waits until
its first step is done, then pauses the job through the browser control while the second step is
running, and checks that the job stopped exactly there. The first time, the job ended as blocked
instead of paused. The second time, the pause arrived only after the second step had finished.
The same test passes on this machine. The rules say the loop must not merge after a second failed
run and must ask you. I need to know whether the loop may repair that test on the feature's own
branch and merge if GitHub's next run is green.

**Why it matters.** Until this pull request is merged, the loop starts no new feature, because it
never builds new work beside an unmerged one. The test gives the pause only about half a second to
arrive, and on GitHub's busy machines starting the small browser server can take longer than that.
Nothing the finished feature changed lies on that test's path, so the second failure looks like a
weakness of the test, not of the product. The first failure, where the job ended as blocked, is
not explained yet, and it could hide a real fault in how a pause takes effect.

**My recommendation.** Let the loop repair the test on the feature's branch in one small reviewed
step. The pretend model inside the test should wait until the pause has really been received
instead of sleeping for a fixed time, so the pause always lands during the second step, and the
test should print the state of every step and the reason the job stopped, so that a later failure
explains itself. Nothing the test checks is made weaker. GitHub then runs the suite once more, and
the loop merges only if that run is green. If a job ever ends as blocked again, the loop treats it
as a real fault in the product and asks you again.

**What happens if you say nothing.** The recommendation is already decided and stands until you
say otherwise: this session has stopped as the rules require, and the next session repairs the
test, lets GitHub run once more, and merges only on a green run. If you want something else, say
so before the next session starts, or merge or close the pull request yourself.
