
DECISION F277 D6 (2026-09-20, round 6) — THE ERROR BOUNDARY CATCHES `Exception`, BECAUSE THE
PROJECT EXCEPTION BASE T002 NAMES DOES NOT EXIST.

CONTEXT. `docs/roadmap/features/T2_F277.md` T002 reads: "An error boundary around dispatch in
`grouped.py` maps this project's exception base to an exit code and routes through `emit_error`
under `--json` and through the current stderr text otherwise. A traceback never reaches the
operator." The reviewer looked for that base before authoring the round and there is none.
Measured at `91034712`: `packages/` declares two dozen `*Error` classes — `RoadmapGrammarError`,
`WorktreeError`, `ReviewZipError`, `SelfUseQueueError`, `PromptSegmentError`, `ArchivePlanError`
and the rest — and each derives straight from `Exception` or from `RuntimeError`, with nothing
in common above them. There is no `RemedyError` and nothing plays that part.

CHOSEN. The boundary catches `Exception`. The sentence "a traceback never reaches the operator"
is the property T002 is really buying, and the exceptions that actually reach an operator as a
traceback are the ones nobody declared — a `KeyError` on a metadata dict, an `AttributeError` on
a `None`, an `OSError` on a path. A base-class boundary would catch the declared few and let the
undeclared many through, which is the opposite of the stated property; the spec's mechanism and
its goal point in different directions, and the goal is the half that was measured. `SystemExit`
and `KeyboardInterrupt` pass through untouched, which costs nothing because both are
`BaseException` and `except Exception` never sees them; the explicit re-raise clause is there so
that a later widening of the catch cannot silently swallow a deliberate exit or a Ctrl-C, and
the round's red control proves that clause is what saves it — widening to `BaseException` WITH
the clause removed is the only mutation that reddens the two passthrough tests. The exit code is
1, and T004 documents it with the rest of the taxonomy.

ALTERNATIVES. Introduce a `RemedyError` base and re-parent two dozen classes onto it — rejected
twice over: it is a cross-cutting refactor of `packages/` inside a slice whose change set is two
CLI files, and it would still not catch the undeclared exceptions that are the actual defect, so
it buys the wrong property at a large price. Catch `Exception` but re-raise anything not derived
from a known project class — rejected: that is the base-class boundary again, wearing a
catch-all's clothes. Leave the boundary out and fix handlers one by one — rejected: there are
several hundred handlers and the feature file's own red proof asks for a boundary.

The feature file is amended in the same round as this patch, per operator amendment
amend0917-throughput rule 3 and docs/agents/planner_reviewer_prompt.md §4 item 7: T002's
paragraph now states the real mechanism and keeps the original sentence beside it as the history
of what was assumed before the tree was read.

REVERSE: delete this paragraph, restore T002's paragraph from git history at `91034712`, and
narrow the `except Exception` in `apps/cli/grouped.py::_dispatch`. Reversing it re-admits
tracebacks from every undeclared failure, under `--json` as well, which is the state this slice
was written to end.
