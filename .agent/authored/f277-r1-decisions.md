
DECISION F277 D1 (2026-09-20, round 1) — THE EVENT COLLECTOR RESOLVES SINKS BY FIXPOINT, NOT
`RunLogWriter.log` ALONE, AND RESOLVES NAMES PER SCOPE.

CONTEXT. `docs/roadmap/features/T2_F277.md` T001 specifies the AST test as collecting written
names from "the first argument of `RunLogWriter.log`, `"event"` dict keys, resolving
module-level constants and tuples", and its "Why this exists" section states that exactly two
literals are read and never written. The reviewer built that collector and ran it against
`f2494c02` before authoring this round. It reports 50 written names and FIFTEEN read-but-never-
written names, not two. The gap is not noise: this repository writes run-ledger events through
THREE sink APIs — `RunLogWriter.log`, `event_persistence.emit_important_event` and
`timeline.append_run_event` — and wraps all three in per-module private helpers, so a collector
that reads only `RunLogWriter.log` cannot see, for one example among many,
`test_execution_service.py` emitting `test_run_completed` through its own `_emit` with the name
computed in a local ternary. Thirteen of those fifteen are phantoms: names that ARE written, by
a route the specified collector does not model.

CHOSEN. The collector seeds three sinks and then takes a FIXPOINT: any function that forwards
its OWN parameter into a known sink becomes a sink at that parameter's position. A private
helper — one whose name begins with an underscore — is matched only inside its own file, because
`builder_bridge.py`, `test_execution_service.py` and `long_run_executor.py` each define `_emit`
and the event argument sits at a DIFFERENT position in `long_run_executor`'s; matching a private
helper by bare name reads the wrong argument and silently collects a `job_id`. Name resolution
is per-scope rather than flat: a flat map lets a sentinel `state = "unknown"` in one function
resolve an `{"event": name}` in another, and it did — `unknown` appeared in the vocabulary until
the scope chain removed it, and removed nothing else.

MEASURED, by the reviewer, at `f2494c02`, with the collector this round ships: 83 names written,
30 read, SIX read and never written. The count is stable across the two independent bug fixes
that produced it, and each fix is explained by a named mechanism rather than by a tuned number.

ALTERNATIVES. Ship the collector the feature file specifies and register the thirteen phantoms
as findings — rejected: they are not defects, and a gate that reports thirteen false positives
is a gate the next round learns to disbelieve. Widen `read ⊆ written` to `read ⊆ declared` and
declare the phantoms — rejected: that writes the collector's blind spot into the permanent
table, which is the opposite of what a declaration is for. Resolve names across module
boundaries — rejected as out of proportion: the strict-mode flag catches at RUNTIME what static
resolution would cost a great deal to catch statically, and the module says so in its Deliberate
absences.

REVERSE: delete this paragraph and restore the collector's `SEED_SINKS` to `RunLogWriter.log`
alone, dropping `_discover_sinks` and the scope chain in
`tests/orchestration/test_event_names.py`.


DECISION F277 D2 (2026-09-20, round 1) — THE SIX DEAD READERS ARE QUARANTINED IN A SET THAT MAY
ONLY SHRINK, AND T001'S ACCEPTANCE LINE IS AMENDED TO SAY SO.

CONTEXT. `docs/roadmap/features/T2_F277.md` Acceptance asks that "read ⊆ written ⊆ declared
holds". Measured at `f2494c02` it does NOT hold and cannot be made to hold by declaring
anything: six names are read by live code and written by nothing —
`approval_decision`, `command_discovery_completed`, `patch_intent_reverted`, `snapshot_created`,
`stop_reason_recorded` and `worker_adapters_listed`. The feature file anticipates one of them,
`worker_adapters_listed`, and rules that it must either be given a writer or deleted with its
score contribution, "and leaving the dimension permanently absent is not" correct. That ruling
is right and it applies to all six; the file simply had not measured the other five. This is a
wrong spec routed to planning under docs/agents/planner_reviewer_prompt.md §4 item 7.

CHOSEN. `event_names.py` declares TWO sets. `EVENT_NAMES` is the written vocabulary.
`READ_ONLY_EVENT_NAMES` is a QUARANTINE carrying exactly those six, each with the modules that
read it and a one-line note on what is wrong. The test makes the quarantine a ratchet that
cannot rot in either direction: a quarantined name that gains a writer fails
`test_a_read_only_name_that_gains_a_writer_leaves_the_quarantine` and must move up, and a
quarantined name that loses its last reader fails
`test_every_quarantined_name_really_has_a_reader` and must be deleted. Round 2 disposes of all
six, one commit per name, each by the feature file's own rule — a writer, or the reader deleted
together with what it feeds — and empties the set, at which point `read ⊆ written ⊆ declared`
holds as the Acceptance line asks and the quarantine becomes an empty frozenset the test still
guards. The Acceptance line is not weakened: it is reached in round 2 rather than asserted
falsely in round 1.

ALTERNATIVES. Dispose of all six in round 1 alongside the claim and the module — rejected on
size: the module and its test are already 557 insertions, over the AGENTS.md cap and split
across two commits here, and six behavioural dispositions each need their own red proof.
Assert `read ⊆ written` in round 1 and let it land red — rejected: a branch tip that ships red
to buy a tidier table is the thing R-1011 was registered for one feature ago. Declare the six
in `EVENT_NAMES` — rejected: it makes the table lie, and the test's
`test_no_declared_name_is_unused` exists to stop exactly that.

REVERSE: delete this paragraph, merge `READ_ONLY_EVENT_NAMES` into `EVENT_NAMES` and drop the
two ratchet tests.


DECISION F277 D3 (2026-09-20, round 1) — UNDER SELF-DRIVE, THE PHASE 1 OPEN PR GATE IS THE
SESSION'S OWN ACT AND NOT A DELEGATED ONE.

CONTEXT. `docs/agents/planner_reviewer_prompt.md` §0 says the planner/reviewer never merges and
that "every merge is an instruction to the worker". `docs/agents/self_drive_protocol.md` Phase 1
rule 2 instead addresses the session directly — an open non-draft `feature/*` pull request into
`main` is merged "at the Open PR Gate (AGENTS.md) before any new branch" — and guardrail G1
phrases the merge as a constraint on the SESSION. The two cannot both be followed literally,
because Phase 1 runs BEFORE any round exists and workers are one per round.

CHOSEN. The session ran the gate itself: pull request 262 was verified OPEN, non-draft, base
`main`, head `feature/*`, `mergeable: MERGEABLE`, `mergeStateStatus: CLEAN` with both hosted CI
checks at `SUCCESS`, and merged with `gh pr merge 262 --merge --delete-branch`, landing
`f2494c02`. The reason this does not weaken the single-writer rule is what that rule protects:
self-drive states it exists so that production code never merges self-certified, and this merge
certified nothing — F276's rounds were each gated by a reviewer that did not write them, and the
merge only lands what was already reviewed. No work-tree file was edited by the session.

ALTERNATIVES. Delegate the merge to round 1's worker — rejected: it puts a `gh pr merge` inside
a round whose block also creates the branch the merge must precede, and AGENTS.md forbids
creating a branch while a mergeable pull request is open. Leave the pull request open and claim
F277 anyway — rejected by the same AGENTS.md sentence.

REVERSE: delete this paragraph. It records a reading, not a change; nothing on disk depends on
it and any later relay may rule the other way for the next feature.
