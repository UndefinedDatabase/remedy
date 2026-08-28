# Plan — F037 Rendered diff viewer

Branch: feature/f037-rendered-diff-viewer, cut from `main` at `9dde5495`, the
merge commit of pull request #217 which closed F032.
`.agent/live_review.md` is the review record and the finding-id ceiling;
`.agent/decisions.md` carries the DECISION series, F037 D1 and D2.

## Goal
Changes become readable, not merely present. The server parses a unified diff
into structured JSON — files, hunks, lines, intraline spans — served as a read
endpoint, and the client renders it with a file sidebar, hunk collapse, virtual
scrolling and lazily loaded syntax bundles.
`docs/roadmap/features/T5_F037.md` holds Goal & Done, the task slicing, the
binding CSS and the design amendments that reconcile it with the source.

## Current Step
R6 opens session 2 and builds the first half of what T001 still owes: a new
module `packages/orchestration/diff_view_source.py` resolving an evidence
directory, and optionally one task run, to the right diff artifact and returning
the contract-v1 envelope with every absence named rather than raised. It also
books the R5 verdict, replaces the `Landed:` lines of `R-0717` and `R-0718` with
reviewer-authored `Done:` text, and records four reviewer-prose slips. No route
is added: the server wiring is R7's and needs the route-walk guard measured
first.

| Item | Status | Reason |
|------|--------|--------|
| C0a/C0b save and mirror the block | ordered | |
| C1 the plan | ordered | first substantive commit |
| C2 the R5 gate, both resolutions, the slips | ordered | record first |
| C3 the resolver module and its tests | ordered | refusal proved, not asserted |
| C4 the handback | ordered | |

## Next Steps
1. The two GET routes onto this module — the job scope as a handler-dict key and
   the task-run scope as a structural route — with the route walk in
   `tests/ui_server/test_command_channel.py` measured before the edit. That
   finishes T001.
2. T002 the rendering core, the binding CSS and the goldens.
3. T003 sidebar, virtual scrolling, lazy languages and the L3 tab.

## Risks
- `R-0715` is open and Low; it is a stale count in a test docstring and belongs
  to whoever next edits that file.
- `R-0711` carries a `Landed:` line and no `Done:` text because F032's branch
  ended first. It is the terminator case, not a gap for F037 to close.
- The parser still has no consumer. R6 gives it one that no HTTP layer can
  reach yet, so its corpus keeps carrying the weight until R7.
