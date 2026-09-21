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

### Q2 — Splitting the machine-contracts feature early (2026-09-21, F277, round 12)

**What needs deciding.** The machine-contracts feature has reached the seven-session
soft limit you set, and the standing rule at that limit is that the session splits the
unfinished part off as a new feature and closes what is built. I have done that. What
you can overturn is the reading that got me there: the feature has used seven sessions
but only eleven of its twenty-five allowed rounds, because five of those sessions
delivered one or two rounds each before running out of room to think. You can tell me
that a limit meant to stop a feature sprawling should not fire when the work itself has
barely moved, and that a feature in that position should keep going on its round budget
instead.

**Why it matters.** The two finished parts are real and self-contained: the vocabulary of
names the system writes into its own run record is now declared in one place and checked
by a test that reads the code, and every command that answers a machine has one shape to
answer in, including when it fails and including when something inside it crashes. The
unfinished part is the mechanical job of moving the remaining nineteen command modules
onto the helper that already exists, emptying the list of read-only commands that still
cannot answer in machine-readable form, and writing down what each exit code means. That
work is unblocked and boring, which is exactly the kind that a fresh feature carries
well. The cost of the split is one more line in the ledger and one more closing
ceremony; the cost of not splitting is that a limit you wrote stops meaning anything the
first time it is inconvenient.

**My recommendation.** Keep the split. Sessions are the scarce resource here, not rounds
— each one re-buys the whole cold start before it does any work — so a feature burning
seven of them is expensive whatever the round counter says, and the limit is measuring
the right thing. The follow-up feature sits directly behind its parent, so the next
session picks it up first and nothing is delayed by more than one closing sequence. If
you would rather the session counter only fired alongside a round count, that is a change
to the rule itself and worth making deliberately rather than by exception here.

**What happens if you say nothing.** The recommendation is already executed and stands
until you say otherwise. The follow-up feature is registered and carries the unfinished
slices word for word, the parent's file records which parts moved, and the parent is
closing at the scope it actually built. Reversing it later is a matter of deleting the
new feature's four registration edits and reopening the parent's line; no product code
depends on which of the two names the remaining work.
