## What

F026 — Task edit at runtime. A task of an approved plan can be edited while its job is not running,
when the task is waiting, paused or failed: from the CLI (`remedy job edit-task <job> <task>
--spec-version N --goal … --acceptance …`) or from the task's detail popover, whose "Edit task" form
appears only for an editable task. The edit is the plan editor's own `plan_edit_task`, so it is
revalidated exactly as before approval and logged in the same edit log; the task gains a spec
version, its prior spec is archived create-only in the evidence export, the approval seal follows
the edit, and a failed task returns to pending together with the tasks its block skipped. The next
run's prompt trace carries the edit. The graph shows a `v<n>` chip beside an edited task, and the
popover lists the versions with the fields each one changed. `remedy job plan-show` prints each
task's spec version and status.

## Why

Course correction without restarting the world: a task that failed on a wrong goal or acceptance
could only be fixed by abandoning the job. Now the operator edits it and relaunches, and nothing
already done is run again.

## Key decisions (in `.agent/decisions.md`)

- F026 D1 — the runtime edit is `plan_edit_task` on one task of an approved plan while no run holds
  the record; the editable states are exactly waiting, paused and failed (`failed` or `blocked`);
  the task entry is updated in place with a per-task `spec_version`; the prior spec is archived; the
  approval hash follows the edit; a failed task and the tasks its block skipped return to pending.
- F026 D2 — `job.edit-task` in the catalog, the CLI and the write door, the task named by its job or
  plan id, the spec version as the conflict check, and the trace proof on a fake run.
- F026 D3 — the dashboard's `task_specs` section, the `v<n>` chip on the node and in the popover,
  and the popover's Versions list.
- F026 D4 — the edit form for eligible tasks only, its send module, the popover's scroll, and the
  live end-to-end through the CLI and the real door.

## How to review

Start with `packages/orchestration/task_edit_runtime.py` and `TaskEntry.spec_version` in
`packages/orchestration/pingpong_job.py`, then `job.edit-task` in `apps/cli/command_catalog.py`,
`apps/cli/commands/job_plan_cmd.py` and the door's clause in `packages/orchestration/ui_server.py`
(with `_build_task_spec_section`), then the UI: `apps/ui/src/api/taskSpecView.ts`,
`taskEditSend.ts`, `components/detail/TaskVersionList.tsx`, `TaskEditForm.tsx`, and the chip in
`components/graph/renderers/paintNode.ts`. The Built State of `docs/roadmap/features/T5_F026.md`
names the test for each acceptance line; each round's mutation tool is
`.agent/authored/f026-r<n>-mutations.py`.

## Verification

- The one full suite, taken on the repaired tree: `19411 passed, 20 skipped` at exit 0, no bad node
  (`.agent/authored/f026-closure-suite.txt`).
- The trace proof: `TestTracePreservesTheEdit` and the live `tests/ui_server/test_task_edit_e2e_live.py`
  fail a planned job, edit it, relaunch it, and read the edited text in the new run's prompt trace and
  no remnant of the old; the live test goes through the real CLI and a real UI server's door and
  reads the second run in the server's `events-since` frames.
- Evidence job `f026r7e1001` against the fork point `90555849`: 1543 selected tests passed at exit
  0, the eslint, tsc and vitest nodes among them.
- Review package `remedy-review-20260925-224758-READY_FOR_REVIEW.zip`, SHA-256
  `8a9aa2d963b00ecad738490efc6df69df72dc782252a2c0f9f16d6cfb9cd6bc8`, READY_FOR_REVIEW.

## Findings and notes

Latest verdict PASS; accepted PASS. F026 registered R-1059 to R-1064 and resolved five of them:
R-1059 (a relaunched blocked job kept its stale error), R-1060 (the secret detector read
"task-edit-runtime" as a key), R-1061 (the relaunch sentence showed a placeholder), R-1062 (the edit
log did not note a pending DoD re-sync) and R-1063 (the DoD import pulled subprocess code into the
write door's reach). R-1064, the same missing boundary in the stream-evidence redactor, lies outside
this feature and is owned by F285, the next findings paydown, which also owns the four findings open
at the claim: R-1008, R-1055, R-1057 and R-1058. The closure's self-use run reproduced R-1057 (it
stopped on its cost cap after one call).

## Runtime actuals

Eight rounds in one session, from the branch's first commit at 18:43 to the accepted head at 22:44
on 2026-09-25; reviewer and workers ran as Claude Opus 5.5; tokens not measured. The closure's
self-use run spent 1.40 dollars on `claude-cli` at `claude-sonnet-4-6`.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
