
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
