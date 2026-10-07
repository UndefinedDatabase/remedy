# Operator questions — what the loop needs decodeux to know or decide

> Written per `docs/agents/self_drive_protocol.md`, operator amendment
> amend0911-feedback rule C (2026-09-11). Read by `remedy-decisions` on the
> operator's machine and by the orchestrator at every relay. Every entry's body
> stands alone in plain sentences; the heading carries the technical reference.
> Soft cap five; entries leave only by the operator's answer, recorded as a dated
> DECISION by the operator's next amendment, which deletes the entry.

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
