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
R7 finishes T001 by making the resolver reachable over HTTP: a job-scope route
as a key in the `do_GET` handlers dict, which enters the route walk for free,
and a task-run-scope route spelled out structurally because it needs a second
path segment. An unknown task run answers 200 with a named absence rather than
404, because absence is data in this envelope. The round also repairs `R-0715`,
a stale numeral in the docstring of the very route-walk guard it edits, by
deleting the numeral as that finding's counter-measure requires.

| Item | Status | Reason |
|------|--------|--------|
| C0a/C0b save and mirror the block | ordered | |
| C1 the plan | ordered | first substantive commit |
| C2 the R6 gate | ordered | record first |
| C3 the two routes | ordered | no new literal route |
| C4 the walk registration and `R-0715` | ordered | the guard must see the new route |
| C5 the endpoint tests | ordered | |
| C6 the handback | ordered | |

## Next Steps
1. T002 the rendering core: lines, intraline emphasis, hunk heads and collapse,
   against the binding CSS in `docs/roadmap/features/T5_F037.md`, with goldens
   per fixture shape.
2. T003 sidebar, virtual scrolling, lazy language bundles, the 10k-line perf
   fixture and the L3 evidence-panel tab.
3. The integration-gate round before closure, then the closure sequence.

## Risks
- `R-0711` carries a `Landed:` line and no `Done:` text because F032's branch
  ended first. It is the terminator case, not a gap for F037 to close.
- The endpoint tests start a real server on a free port. Run the suites
  serially: two pytest processes at once produce false reds in this directory.
- T002 is the first UI work of this feature, so the design reference in
  `docs/ui/design_reference/` becomes binding from the next round on.
