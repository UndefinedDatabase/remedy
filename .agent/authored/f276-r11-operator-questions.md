# Operator questions — what the loop needs decodeux to know or decide

> Written per `docs/agents/self_drive_protocol.md`, operator amendment
> amend0911-feedback rule C (2026-09-11). Read by `remedy-decisions` on the
> operator's machine and by the orchestrator at every relay. Every entry's body
> stands alone in plain sentences; the heading carries the technical reference.
> Soft cap five; entries leave only by the operator's answer, recorded as a dated
> DECISION by the operator's next amendment, which deletes the entry.

### Q1 — Re-running the closure test suite (2026-09-20, F276, round 11)

**What needs deciding.** You merged the main line back into the data-root feature
branch after its final test run had already been recorded. The rule we normally work
under says the whole test suite runs once per feature and that the closure reads back
the recorded result rather than running it again. I have run the suite a second time
instead, because the recording no longer describes the code being shipped. You can tell
me that was the wrong call and that a recorded run should stand even when the branch
moves underneath it.

**Why it matters.** The saved result counted 17659 test outcomes. The branch as it now
stands offers 17740 tests, because the merge brought in a new planning service and its
own tests along with it. Eighty-one of the tests that exist on the branch had therefore
never been run in the result the closure was about to certify, and three of the files
the merge touched are files this feature also changed. Accepting the feature on that
recording would have put a pass on the permanent record covering code nobody had run.
The cost of the second run is roughly five minutes of machine time and no extra round.

**My recommendation.** Keep the second run. The rule that limits the suite to one run
per feature exists to stop individual rounds buying reassurance they do not need, and
that is not what happened here — the tree the single run certified was replaced by an
action from outside the loop. Where that happens, the honest reading of the rule is
that the one run belongs to the code actually being shipped, and I would like to treat
this as the standing answer rather than re-asking it the next time you merge into an
open branch.

**What happens if you say nothing.** The recommendation is already executed and stands
until you say otherwise. The suite has been re-run, the new result has replaced the old
one at the same location, and the old one remains recoverable from the history. The
feature closes on the new reading.
