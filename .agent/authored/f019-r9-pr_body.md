## What

F019 — Live node materialization. The brain graph in the cockpit now grows while a job runs. A
pure reducer (`brainReducer.ts`) folds the event stream's frames into a graph model — the job core,
its task ring seeded from the dashboard, and a node for each builder attempt, review and check —
and `buildBrainLayout` lays that model out deterministically. The rewritten `ForceBrainGraph.tsx`
paints it on react-force-graph-2d with birth animations, particles on active links and reduced-
motion handling, and `BrainGraphStage.tsx` mounts it by default, keeping the older SVG picture as a
"Simple view" and as the empty state. The stage reads a ledger merged from `events-since` pages and
the live stream's ring and draws only the complete prefix of it, so a gap (a dropped connection, a
tab that slept) is read back before anything past it is drawn.

## Why

The graph is the product's face, and it was a static picture of the dashboard. Now it shows the
job's real progress as it happens, from the same event stream every other live surface reads, and
it never draws a result the stream did not report.

## Key decisions (in `.agent/decisions.md`)

- F019 D1 — the reducer reads the envelope the server really writes; a run node is keyed by the
  frame that birthed it; the task ring is seeded from the dashboard's task list.
- F019 D2 — T002's pure half first: the deterministic layout and the birth schedule from the
  design reference's motion tokens.
- F019 D3 — the force renderer is the default; the SVG picture stays as the simple view with the
  prompt dots; a click selects the task's dashboard `nodeId`.
- F019 D4 — the decorative dashboard builder is removed with its pins; the demo recording is a
  captured fake-provider job.
- F019 D5 — the graph folds the complete prefix of a ledger merged from `events-since` pages and
  the live ring; a hole is filled by paging from its first missing seq.
- F019 D6 — a live fake job is checked against the demo recording in the suite; the stage-1 frame
  budget is measured on a committed fixture in headless Chrome.

## How to review

Start with `apps/ui/src/components/graph/brainReducer.ts` and its goldens in
`brainReducer.fixtures.ts`, then `buildForceBrainModel.ts` (`buildBrainLayout`), `brainLedger.ts`,
`BrainGraphStage.tsx` and `ForceBrainGraph.tsx`. The Built State of
`docs/roadmap/features/T5_F019.md` names the test for each acceptance line; each round's mutation
tool is `.agent/authored/f019-r<n>-mutations.py`, and the frame-rate tool is
`.agent/authored/f019-r6-perf-*`.

## Verification

- The one full suite: `19092 passed, 20 skipped` at exit 0, no bad node
  (`.agent/authored/f019-closure-suite.txt`).
- Evidence job `f019r8e1001` against the fork point `92b7f5f1`: 718 selected tests passed at exit 0,
  the eslint, tsc and vitest nodes among them.
- Frame budget: 200 and 500 nodes held 60 fps with a 95th-percentile frame of at most 16.8 ms in
  headless Chrome (the reading shows no dropped frame at the 60 Hz pace, not the headroom).
- Review package `remedy-review-20260924-204836-READY_FOR_REVIEW.zip`, SHA-256
  `d0340a1a2ed77a6472e2d3f3469a4e5bf590674fd21e4d229b9c4d52d01263ff`, READY_FOR_REVIEW.

## Findings and notes

None registered. The four open findings are owned by the next findings paydown, F284. Operator
notes Q2 (test and repair runs draw no node until the stream carries their task and outcome) and
Q3 (prompt dots live in the simple view) stand with their recommendations executed.

## Runtime actuals

Nine rounds over two sessions; reviewer and workers ran as Claude Opus 5.5; wall clock and tokens
not measured.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
