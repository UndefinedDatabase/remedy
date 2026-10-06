# Operator questions — what the loop needs decodeux to know or decide

> Written per `docs/agents/self_drive_protocol.md`, operator amendment
> amend0911-feedback rule C (2026-09-11). Read by `remedy-decisions` on the
> operator's machine and by the orchestrator at every relay. Every entry's body
> stands alone in plain sentences; the heading carries the technical reference.
> Soft cap five; entries leave only by the operator's answer, recorded as a dated
> DECISION by the operator's next amendment, which deletes the entry.

### Q5 — Two features share one number (2026-10-06, F290, Open PR Gate)

**What needs deciding.** Every planned piece of work in Remedy has a number in the feature list.
Your change of 6 October, which reordered the list around the Luna gates, was merged into the main
line and gave the number 295 to the new feature for a machine client and 296 to the new feature
for escalating to a stronger model. On the same day, the loop finished the sixth round of paying
down open findings on its own branch, and its closing step gave the same number 295 to the next
paydown, the seventh. Because of this, the pull request that carries the finished sixth paydown can
no longer be merged: four files disagree, namely the feature list, the README, the test that counts
the features, and the decisions file. The decisions file is only the expected case where both sides
added text at the end, and your own note already says to keep both. The other three are a real
clash over one number. I need you to say which feature keeps the number 295.

**Why it matters.** The loop may not merge a pull request with conflicts, and it may not start any
new work while that pull request is open. Until this is settled, every session will stop at the
same place. Choosing the number also fixes where the seventh paydown sits in your new order and
which feature the two findings still open after the sixth paydown point to.

**My recommendation.** Keep 295 and 296 as you registered them on the main line, and give the
seventh paydown the next free number, 297. The loop would then merge the main line into the branch,
keep both sets of decisions with the paydown's first, place the seventh paydown five open lines
below the sixth in your new order as the paydown rule requires, point the two open findings at 297,
set the feature count to 297, and record all of it as one decision you can reverse. Because the
branch has changed since its final full test run, the loop would run the full test suite once more
on the merged result before the pull request is merged. The old commit messages that say 295 for
the paydown stay as they are, because history is never rewritten.

**What happens if you say nothing.** Nothing moves. Unlike other questions, this recommendation is
not already carried out, because the repository's top rule says a pull request with conflicts stops
the loop until the conflict is reported and settled. Each new session will stop again at this pull
request. If you answer "do what you recommend", the next session carries it out as described above.
