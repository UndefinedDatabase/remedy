## What

F023 — Semantic zoom L0–L3. The brain graph now reads at four levels driven by one pure state
machine: L0 the whole job, L1 one task with its siblings dimmed to 25% and its '+N' cluster
expanded, L2 one run with its detail card, L3 that run's evidence panel. The mouse wheel, clicks,
the breadcrumb chip and Escape all move through the same machine; the wheel's thresholds (in above
1.6 over a node, out below 0.8) leave a dead band so the level never flickers. The page URL carries
`?focus=&level=&tab=`, restored on open and kept in step with `history.replaceState`, with no
router.

## Why

The graph had one fixed picture and no way from the organism down to a run's evidence. Now the
reader can go from the whole job to one run's diff and prompts in three steps and back with
Escape, and a link reopens the same view.

## Key decisions (in `.agent/decisions.md`)

- F023 D1 — a pure machine {level, focusId, tab} goldened over its whole matrix; the hysteresis
  in the wheel adapter; focus checked against the model plus its cluster view.
- F023 D2 — the render effects as data, the camera per level under a lock, Escape and reconcile in
  the hook, the breadcrumb chip.
- F023 D3 — the run detail's missing facts as a named prerequisite: the read route
  `/api/jobs/<job>/task-runs/<task_id>/rounds`, serving only numbers, words and timestamps from the
  task's run report.
- F023 D4 — the L2 run detail: each fact a value or a plain sentence saying why it is missing;
  Rerun disabled with its reason visible.
- F023 D5 — the L3 evidence panel on the binding CSS, its shadow as a new token, its tabs lazy;
  the zoom surfaces on layer tokens.
- F023 D6 — deep links, cluster expansion at the focused task, and a camera that waits for the
  canvas, a defect found by a headless render.
- F023 D7 — the frame budget at 500 nodes over every level, with a tool that can fail, and a live
  fake job proving the run detail's round rule against real run reports.

## How to review

Start with `apps/ui/src/components/graph/semanticZoom.ts` and `zoomWheel.ts`, then `zoomView.ts`,
`useSemanticZoom.ts`, the changes to `ForceBrainGraph.tsx` and `BrainGraphStage.tsx`, then
`packages/orchestration/run_rounds_view.py` with its route in `ui_server.py`, `runDetailModel.ts`,
`RunDetailPopover.tsx`, `EvidencePanel.tsx`, `zoomDeepLink.ts` and `clusterExpansion.ts`. The Built
State of `docs/roadmap/features/T5_F023.md` names the test for each acceptance line; each round's
mutation tool is `.agent/authored/f023-r<n>-mutations.py`, and the three design-pack gaps F023
filled are its rows of `docs/ui/design_reference/assumption_log.md`.

## Verification

- The one full suite: `19158 passed, 20 skipped` at exit 0, no bad node
  (`.agent/authored/f023-closure-suite.txt`).
- Frame budget: 60 frames a second at 500 nodes at every zoom level, worst 95th-percentile frame
  16.8 ms (`.agent/authored/f023-r7-perf.txt`); the tool's red control fails.
- Evidence job `f023r9e1001` against the fork point `441f4e8e`: 706 selected tests passed at exit 0,
  the eslint, tsc and vitest nodes among them.
- Review package `remedy-review-20260925-052148-READY_FOR_REVIEW.zip`, SHA-256
  `6e041624017f41e1644f71f3d8c18ae8dd4d677b1d8df4fe6206f89b6f76b4bb`, READY_FOR_REVIEW.

## Findings and notes

None registered. The one open finding, R-1008, is owned by the next findings paydown, F285. The
run report keeps no reviewer tokens and only a task's latest run, and the run detail says so; the
chat tab says in plain words that talking about one run is not here yet.

## Runtime actuals

Ten rounds in one session; reviewer and workers ran as Claude Opus 5.5; wall clock and tokens not
measured.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
