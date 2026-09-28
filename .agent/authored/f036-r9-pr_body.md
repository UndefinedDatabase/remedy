## What

F036 — Guided result tour. A finished job now answers "what did I get?" in at most eight short
stops: how the run ended, what changed in each part of the code, the command that runs it and
whether its Definition of Done passed. Every stop is tied to a place in the job that is checked
to exist when the tour is built: a task, a changed file, a file of the job's evidence or a
recorded command. The tour reads records earlier features already write, and F036 changes none
of them.

- **T001, the stops and the mechanical tour.** `packages/orchestration/result_tour.py`: the tour
  and stop shape (`remedy.tour.v1`, at most eight stops, titles up to 80 characters and bodies up
  to 400), the anchor check against the job's own records, and `build_fallback_tour`, the tour
  built mechanically from the report's sources, the diff's file list and the Definition of Done.
- **T002, the model-written tour, storage and the command line.** `generate_result_tour` asks the
  summary role for a tour with its own schema, keeps the mechanical tour's honest first stop, and
  drops any stop that claims a number, a quoted span, a path or a denylisted word the records do
  not hold. It runs only when the operator switches on `tour.model_written`
  (`REMEDY_TOUR_MODEL_WRITTEN`), which is off by default. Every reported terminal writes a new
  version, `tour.json` then `tour_v<N>.json`, from `long_run_executor._apply_terminal`, and never
  raises. `job show --full` ends with a `tour` section, and `job show --tour` shows it alone.
- **T003, the browser.** `tour_view` is served at `/api/jobs/<id>/tour`;
  `apps/ui/src/api/resultTour.ts` decodes it whole or not at all. A "Tour" button beside
  "Lessons" opens `components/tour/TourOverlay.tsx`, portaled to the page body. It has a dimmed
  backdrop and one card with Previous, Next, "Show me" and "Close tour". "Show me" opens the
  task's detail, or the job's whole diff scrolled to the file, lifts the dim and docks the card
  over the left rail.

## Why

T5_F036 asks that a person can understand a job's result without reading its whole report and
diff. Every stop points at a real place, so the tour can be checked against the job rather than
trusted.

## Key decisions (in `.agent/decisions.md`)

- F036 D1: one module, four anchor kinds checked at build time, and the mechanical tour's order.
- F036 D2: the fifth findings paydown, F286, waits behind F036, because no finding was open.
- F036 D3: the model-written tour keeps the honest first stop, makes no new claims, and catches
  failures by name.
- F036 D4: a new version at every reported terminal, and the command line's `tour` section.
- F036 D5: one view for the route and the command line, and one pure TypeScript decoder.
- F036 D6: the overlay, its "Tour" button and "Show me".
- F036 D7: the model-written tour switched on by the operator, the docked card, and the live
  end-to-end proof. The demo recording's tour is proved through the render harness only.

## How to review

Start with `collect_tour_context`, `anchor_problem` and `build_fallback_tour` in
`packages/orchestration/result_tour.py`. Then read `generate_result_tour`, `tour_claim_problems`,
`write_result_tour` and `tour_view`, the hook in `packages/orchestration/long_run_executor.py`,
the `tour` section in `apps/cli/commands/job.py` and the route in
`packages/orchestration/ui_server.py`. On the browser side, read `apps/ui/src/api/resultTour.ts`,
`components/tour/TourOverlay.tsx` and its CSS module, and the shell's mount in
`components/shell/RemedyShell.tsx`. The Built State of `docs/roadmap/features/T5_F036.md` names
the test for each acceptance line. The live proof is `tests/ui_server/test_tour_e2e_live.py`.
Each building round's mutation tool is `.agent/authored/f036-r<n>-mutations.py`.

## Changed files

33 files outside `.agent/` against the fork point `9dc2f2a7`, counted by `git diff --name-only`
before the closure commit, plus `README.md`:
- 7 under `packages/` and `apps/cli/`.
- 7 under `apps/ui/`: the tour decoder, its vitest suite, the loader, the overlay and its CSS,
  the panel's button and the shell.
- 12 under `tests/`: 7 Python test files, 4 golden fixtures and the import-reachability
  allowlist.
- 7 others: `docs/guides/environment.md`, `docs/ui/design_reference/assumption_log.md`, the
  feature file, F286's feature file, the checklist's consolidation paragraph in
  `docs/agents/planner_reviewer_prompt.md`, `docs/roadmap/STATUS.md` and `README.md`.

`git diff --stat 9dc2f2a7..HEAD` lists them.

## Verification

- The one full suite on the tree that ships: `20375 passed, 20 skipped` at exit 0, with no bad
  node (`.agent/authored/f036-closure-suite.txt`).
- The headless-Chrome render of the overlay, eleven checks, re-run by the reviewer
  (`.agent/authored/f036-r7-render_*`).
- The closure's self-use item: none. The queue held no pending item and the generator found no
  source (`self-use NONE (queue exhausted)`).
- Evidence job `f036r8e1001` against the fork point `9dc2f2a7`: 1255 of 1258 selected tests passed,
  3 skipped, at exit 0.
- Review package `remedy-review-20260928-094901-READY_FOR_REVIEW.zip`, SHA-256
  `e2bd771b3f1c1a52fcc7e73cdae50c4fd4a837107ee5e46b76d79d8b8dffc2f4`, READY_FOR_REVIEW.

## Findings and notes

Latest verdict: PASS; the feature is accepted as PASS. F036 registered four findings: R-1087 (Low),
R-1088 (Medium), R-1089 (Medium) and R-1090 (Low). All four were its own, and all were repaired
inside it with a red-proof. No finding is open.

## Runtime actuals

Nine rounds in two sessions on 2026-09-28, from the branch's first commit at 06:16 to the accepted
head at 09:46. The reviewer and the workers ran as Claude Opus 5.5. Tokens and cost were not
measured.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
