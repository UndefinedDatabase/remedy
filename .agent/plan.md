# Plan — F037 Rendered diff viewer

Branch: feature/f037-rendered-diff-viewer, cut from `main` at `9dde5495` (the
merge of PR #217, which closed F032). `.agent/decisions.md` holds F037 D1 to D9.

## Goal
Changes become readable, not merely present. The server parses a unified diff
into structured JSON — files, hunks, lines, intraline spans — served as a read
endpoint, and the client renders it with a file sidebar, hunk collapse, virtual
scrolling and lazily loaded syntax bundles.
`docs/roadmap/features/T5_F037.md` holds Goal & Done, the task slicing, the
binding CSS and the design amendments A1 through A5.

## Current Step
R17 opens T003 at the seam T002 stopped short of: the DOOR the client fetches a
diff envelope through. `remedyApi.ts` gains a URL builder and a loader for the
two scopes `packages/orchestration/ui_server.py` really routes — a job's diff
and one task run's — and every payload leaves that loader through
`readDiffEnvelope`, so a 403, a dead socket and a junk body all degrade to the
same total envelope rather than three shapes the viewer would have to know
about. A Python guard pins the client's URL template against the server's own
route conditions, which is the agreement vitest cannot see. Nothing is mounted.

| Item | Status | Reason |
|------|--------|--------|
| C0a/C0b save and mirror the block | ordered | |
| C1 the plan | ordered | first substantive commit |
| C2 the R16 verdict | ordered | record first |
| C3 the envelope door and its vitest tests | ordered | the fetch seam |
| C4 the cross-language guard and the polarity test | ordered | vitest sees no routes |
| C5 the handback | ordered | |

## Next Steps
1. Mount the viewer: the "Open diff" button `component_spec.md:113-116` puts in
   `DetailPopover`, the state holding the opened task, and `DiffView` behind it.
2. The file sidebar over `buildDiffFileSummaries`, then virtual scrolling beyond
   two thousand lines, the lazy language bundles and the perf fixture.

## Risks
- Round 17 of a 25-round soft limit, session 5 of 7. The named pieces of T003
  still open are the mount, the sidebar, the virtual scrolling, the lazy
  language bundles, the perf fixture and the L3 tab integration, so a round
  closing none of them is the one to stop and re-scope after.
- No TypeScript mutation red-proof is orderable anywhere here. The `.ts` layer
  is covered by vitest in the primary checkout and by text guards; the `.tsx`
  layer by `tsc --noEmit` and text guards, and by nothing else.
