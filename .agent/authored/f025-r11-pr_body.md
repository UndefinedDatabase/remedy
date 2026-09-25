## What

F025 — Pause/resume (global & per node). A running job can be paused as a whole or one task at a
time, from the CLI (`remedy job pause <id> [--task T]`, `remedy job unpause`) or from the browser
through the single write channel. The provider call in flight finishes and nothing new starts; the
job persists as `paused` with its pause record and the process exits, so no daemon waits. The
relaunch (`remedy job run <id>`) is the resume: it carries on exactly where the job stood and never
re-runs a finished task. A task pause withholds that task and what comes after it on the linear
runner, and on the graph runner only that task and its dependents while siblings proceed. A stop beats a pause, and the deadline keeps counting through one. In the browser: an
orange PAUSED banner in the graph's chrome, the NowCard's "Paused by you", a `paused` node state
with a two-bar pause mark, and pause/resume buttons for the job and for each pending task.

## Why

There was no calm way to hold a run: the only control was the kill switch, which ends the job. Now
an operator can hold a job or a branch and continue it later with nothing lost and nothing left
running.

## Key decisions (in `.agent/decisions.md`)

- F025 D1 — a pause is a control fact beside the stop, read at the stop's own safe points; the park
  persists `paused` and exits; the relaunch is the resume; a stop beats a pause.
- F025 D2 — `job.pause` and `job.unpause`, each with an optional task, in the catalog, the CLI and
  the write door; the door starts no process, so a browser resume of a parked job shows the relaunch
  command (operator question Q4 records this for the operator to overturn).
- F025 D3 — the dashboard's `pause` object and the graph's `paused` node state and mark.
- F025 D4 — the banner, the NowCard line and the buttons, through a request module that reads the
  door's answer.
- F025 D5 — the live end-to-end against an unpaused control run; provider-session reuse across a
  park is out of scope (R-1055, owned by F285).
- F025 D6 — the run manifest's new status `paused`, so a relaunched job writes its manifest over
  both episodes (the repair of R-1056).

## How to review

Start with `packages/orchestration/pause_control.py`, then the pause wiring in `run_job` and
`_park_job` (`packages/orchestration/pingpong_job.py`) and in `run_cycles`
(`packages/orchestration/long_run_executor.py`), then `apps/cli/commands/job_pause_cmd.py` and the
door's two clauses in `packages/orchestration/ui_server.py`, then the `paused` manifest status in
`packages/orchestration/run_manifest.py`, then the UI: `apps/ui/src/api/pauseSend.ts`,
`pauseView.ts`, `components/panels/PauseControl.tsx` and the `paused` state in
`components/graph/`. The Built State of `docs/roadmap/features/T5_F025.md` names the test for each
acceptance line; each round's mutation tool is `.agent/authored/f025-r<n>-mutations.py`.

## Verification

- The one full suite: `19312 passed, 20 skipped` at exit 0, no bad node
  (`.agent/authored/f025-closure-suite.txt`).
- Live end-to-end: `tests/ui_server/test_pause_e2e_live.py` pauses a fake-provider job of both
  scopes through the real door, relaunches it with the real `python3 -m apps.cli.main job run`, and
  matches an unpaused control run by normalized record, workspace bytes and task event order.
- Evidence job `f025r10e1001` against the fork point `49624d5c`: 1033 selected tests passed at exit
  0, the eslint, tsc and vitest nodes among them.
- Review package `remedy-review-20260925-174026-READY_FOR_REVIEW.zip`, SHA-256
  `5202e21aed884f7ae6a8b79a852d2c4683436f2220d1a910d072cec01ac38e6f`, READY_FOR_REVIEW.

## Findings and notes

Latest verdict PASS; accepted PASS_WITH_RISKS. F025 registered R-1049 to R-1058 and resolved seven of
them. Four findings are open, all owned by the next findings paydown, F285: R-1008 (the
self-use track has not yet landed a repair), R-1055 (the Done clause's provider-session reuse
across a park is not met: an interrupted task's AI session starts afresh at the relaunch), R-1057
(the self-use path's cost cap is smaller than its smallest run) and R-1058 (the self-use generator's
acceptance lets a ledger note pass as a repair, which this closure's run did).

## Runtime actuals

Eleven rounds over two sessions, from the branch's first commit at 10:16 to the accepted head at
17:36 on 2026-09-25; reviewer and workers ran as Claude Opus 5.5; tokens not measured. The closure's
self-use run spent 1.14 dollars on `claude-cli` at `claude-sonnet-4-6`.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
