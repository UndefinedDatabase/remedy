
## DECISION F276 D11 (2026-09-20, reviewer, round 11) — the closure is two rounds, so `accepted HEAD` names the evidence round's handback commit; and the evidence run is scoped to what this feature built

PART ONE, THE SPLIT AND WHAT `accepted HEAD` THEREFORE NAMES.
`docs/roadmap/STATUS_closure_protocol.md` step 4 asks the REVIEWER to author the STATUS
line and the worker to apply it verbatim, and that line must carry the package's
filename, its SHA-256 and its archived path. None of those exist until the package is
BUILT. Step 2 in turn requires the package to be built from a CLEAN tree after all
content commits. A single round cannot satisfy both: the reviewer would have to author a
line naming values no one has measured yet.

CHOSEN: the closure runs as TWO rounds after the integration gate is re-confirmed. The
EVIDENCE round performs the integrity check, builds the evidence job and builds the
package, and reports the package's name, SHA-256 and archived path to the reviewer. The
CLOSURE round applies the STATUS line the reviewer then authors from those measured
values, together with the README counters and SU-024's `consumed_by`, in ONE commit which
is the LAST on the branch, and opens the pull request.

CONSEQUENCE, stated plainly because it is the part a later reader will check: the package
is built after the EVIDENCE round's handback commit, so `accepted HEAD` names that commit,
and exactly ONE commit — the closure commit — exists on the branch after the reviewed head
the manifest records. That is what step 2's own sentence describes ("the final closure
commit follows the READY zip"), and the STATUS line's `accepted HEAD` segment is the
durable record of which commit the verdict and the package actually cover. The closure
commit itself is bookkeeping over `docs/roadmap/STATUS.md`, `README.md`,
`scripts/self_use_queue.json` and `.agent/` state, and it changes no file the package
reviews.

WHERE THE MEASURED VALUES LIVE BETWEEN THE TWO ROUNDS: in the evidence round's report to
the reviewer and in a `package.txt` file on disk under that round's own scratch directory.
They are not in that round's handback, because the handback commit precedes the build by
construction. Should the session end between the two rounds, the package file itself is on
disk and its SHA-256 is recomputable from it, so nothing is unrecoverable — which is the
property that makes the split safe rather than merely convenient.

PART TWO, WHAT THE EVIDENCE RUN COVERS. The verification record names six test FILES,
sorted, and no directory: `tests/cli/test_data_cmd.py`,
`tests/orchestration/test_data_footprint.py`, `tests/orchestration/test_data_reclaim.py`,
`tests/orchestration/test_disk_floor.py`, `tests/orchestration/test_staging_lifecycle.py`
and `tests/test_data_root_classes.py` — the suites this feature created, measured by the
reviewer at `512ba69c` as collecting 112 node ids, the same count the same reviewer
measured at `970f544b` before the merge D12 records. It deliberately does NOT carry a
full-suite node-id list: `len(node_ids) == selected` forbids filtering, and the packaging
metadata scan rejects the redaction-torture parametrizations whose ids embed fake secrets
by design, so a full-suite record packages BLOCKED_EVIDENCE. That is closure pitfall (d),
already on the protocol's own record. The full-suite proof rides instead in the committed
integration-gate transcript `.agent/authored/f276-closure-suite.txt`, whose contents for
this closure are the ones the re-run DECISION F276 D12 orders produces, and NOT the
pre-merge reading that path held at `fd23710f`. Nothing green is claimed that was not run.

THE BASE COMMIT IS THE FORK POINT, `43d148177efd145f179ba2d9875eaa675b1595b7`, at full
length — pitfall (e) — and after the merge D12 records, that pitfall is LIVE on this
branch rather than dormant. Re-measured by the reviewer at `512ba69c`: `git merge-base
main 512ba69c` now answers `8f129d71e311ccd58bdb01d63c78bb75dffbd382`, which is main's own
tip and is NOT the base; the first commit of `git rev-list --first-parent 512ba69c` that
`git rev-list main` also holds is still the fork point above; and `git rev-list
--ancestry-path <base>..512ba69c` and `git rev-list <base>..512ba69c` both read 59, the
equality that is the only reading able to show the base is right. Before the merge, at
`970f544b`, both read 45 and merge-base coincided with the fork point; that coincidence is
gone and the earlier wording which relied on it is superseded here rather than in place.

ALTERNATIVES: one round, with the worker composing the STATUS line from its own
measurements — rejected outright, because step 4 reserves authorship of that line to the
reviewer and a worker-authored acceptance line is the one thing this workflow exists to
prevent. Building the package before the handback commit so its values could be recorded
there — rejected because that leaves TWO commits after the reviewed head rather than one,
and the manifest's `accepted HEAD` would then name a commit two behind the branch tip.

REVERSE: this decision changes no code. To reverse it, close a future feature in one round
by having the reviewer author a STATUS line with the package fields left as placeholders
and a second commit filling them in; then delete this paragraph.

## DECISION F276 D12 (2026-09-20, reviewer, round 11) — the operator's merge of main into this branch invalidated the committed integration-gate transcript, so the gate is re-run ONCE on the merged tree and the transcript is replaced in place

WHAT HAPPENED, as readings and not as a summary. After round 10 ended on the STOP
sentinel, the operator merged `origin/main` into `feature/f276-data-root-hygiene` at
`512ba69c`, a merge commit whose first parent is round 10's `22e7fd95` and whose second is
main's tip `8f129d71`. It brought in the amend0920-selfuse-real work: 28 files by
`git diff --name-only 43d148177efd145f179ba2d9875eaa675b1595b7 8f129d71`, including the new
module `packages/providers/claude_planner/provider.py` and the new suite
`tests/orchestration/test_claude_planner.py`, and six of those paths are also paths this
feature changed — `.agent/decisions.md`, `.agent/live_review.md`, `.agent/plan.md`,
`apps/cli/command_catalog.py`, `packages/orchestration/config.py` and
`tests/orchestration/import_reachability_allowlist.txt`.

WHY THAT IS A CLOSURE PROBLEM. Closure precondition 2 asks that the integration-gate round
have run the full suite once and that closure "re-confirms by reading that transcript". The
transcript committed at `fd23710f` reads `17639 passed, 20 skipped` for 17659 outcomes, and
it reconciles its own bad set against the run it replaced. At `512ba69c` the reviewer's own
`python3 -m pytest -q --collect-only` reads 17740 tests collected. The two numbers describe
different trees, and 81 of the tests that exist on the branch being closed were never in the
run the transcript records — among them the whole of `tests/orchestration/test_claude_planner.py`.
Reading that transcript therefore re-confirms nothing about this tree. Two smaller readings
moved with it: `git merge-base main 512ba69c` no longer answers the fork point, which D11
re-measures above; and `python3 -m apps.cli.main integrity check --json` at `512ba69c` reads
`passed: true` with `live_review_verdict` at `pass`, where the round 10 block had recorded a
`warn: no verdict found` as expected — so that block's own expectation note is stale too.

CHOSEN: the integration gate is RE-RUN EXACTLY ONCE on the merged tree, by the worker, in
the primary checkout, with `apps/ui` built first, and its transcript REPLACES
`.agent/authored/f276-closure-suite.txt` in place. The replacement keeps the single path
closure precondition 2 reads by name, and the new transcript restates the superseded run's
summary line beside its own so a later reader can resolve both from one file. This is the
same mechanism round 8 used when it replaced round 7's red transcript at that same path,
and it is deliberately not a new one.

WHY THIS IS NOT A BREACH OF THE ONE-RUN RULE. Operator amendment amend0917-throughput rule 1
fixes the full suite at one run per FEATURE and forbids a round block from ordering it; its
purpose, stated in its own reason clause, is that round verification had re-imported a cost
the 2026-07-26 verification tiers had already excluded. That purpose is untouched here: no
ROUND is buying a suite run for its own verification, and the count this feature spends is
not rising because a round asked for reassurance. The tree the one run certifies was
replaced under it by an action outside the loop, and rule 1's own precondition — that the
transcript describes the tree being closed — cannot otherwise be met. Closing on a
transcript of a different tree would be the failure mode `docs/roadmap/STATUS_closure_protocol.md`
calls the one unforgivable one, and no rule asks for that trade.

ALTERNATIVES. Close on the `fd23710f` transcript and note the merge as a risk — rejected:
the STATUS line would carry a PASS whose evidence covers 81 fewer tests than the branch
holds, and the risk note would be a sentence standing in for a measurement that costs one
run. Revert the merge — rejected: guardrail G2 forbids rewriting this branch's history, the
merge is the operator's own act, and main's content is wanted on the branch before the pull
request. Ask the operator and wait — rejected because operator amendment amend0917-throughput
rule 5 forbids exactly that stall; the question is written to `.agent/operator_questions.md`
as Q1 and this decision is executed in the same round, which is what that rule requires.
Treat the re-run as one of the three repair rounds amend0917 rule 2 allows — rejected as a
mislabel: rule 2's repair rounds shrink a bad set, and this run has no bad set to shrink,
so calling it a repair would spend a budget on a thing it does not describe.

CONSEQUENCE FOR THE ROUNDS THAT FOLLOW. If the re-run is green, the evidence round proceeds
as D11 describes and nothing else changes. If it is red, its bad set is this feature's under
amend0917 rule 2, F276 has spent one of its three repair rounds at round 8 and has two left,
and the closure does not proceed until that rule is satisfied.

REVERSE: delete this paragraph and restore `.agent/authored/f276-closure-suite.txt` to its
`fd23710f` content, which git holds unchanged.
