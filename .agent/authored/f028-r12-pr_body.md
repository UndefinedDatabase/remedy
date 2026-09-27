## What

F028 — Task injection. The "+ Add Task" row of the cockpit is real additive control: the operator's
text is drafted into a task by the planner, placed, budget-checked and fence-checked, and applied to
the running job only when a second call confirms the draft, with provenance end to end.

- **T001, the draft pass.** `packages/orchestration/task_injection.py`: one structured planner call
  drafts the task (title, goal, testable acceptance, band, files hint); placement is computed by code
  (appended at the end, after the task the operator named, else after tasks sharing a path, else
  after the frontier) with a written rationale; the budget check is F104's prediction over the
  draft's band; a shortfall carries a three-option decision seed instead of a token; fence conflicts
  are flagged up front. The draft is a create-only control file that expires after 900 seconds.
- **T002, confirm and apply.** A confirmation is a second create-only file; `run_job` folds confirmed
  injections at four safe points through the new edit kind `plan_add_task`, with
  `origin=human_injected`, the placement rationale and an edit-log entry; the shortfall's three
  answers (`extend_budget`, `shrink_task`, `drop`) derive a new draft or end the old one; each fold
  writes a `task_injected` run-log event.
- **T003, the surfaces.** `remedy job inject`, `inject-confirm` and `inject-answer` (`--yes` confirms
  unseen and is recorded as such); the write door's `job.inject`, `job.inject-confirm` and
  `job.inject-answer`; the Add Task sheet, rendered through a portal; the "Added by you" pill in the
  task list and the detail popover, the "added" canvas chip, and the origin clause in the final
  report. A live end-to-end test injects through the door and through `--yes`.

## Why

T5_F028 asks for human additive control of a running job without a second approval machinery: the
draft-confirm round trip is the P2 shape, and a budget shortfall becomes a clarification rather than
a silent squeeze.

## Key decisions (in `.agent/decisions.md`)

- F028 D1 — the draft pass, the control file and its time to live, code-computed placement.
- F028 D2 — the confirmation file, the four-point fold, `plan_add_task`, parking a late fold paused.
- F028 D3 — the shortfall's three answers and the budget extension the fold applies.
- F028 D4 — the three commands, the audited `--yes`, the shared budget and planner helpers.
- F028 D5 — the three door commands and the `task_injected` event.
- F028 D6 — the "Added by you" pill and the dashboard's `origin`.
- F028 D7 — the "+ Add Task" row replacing the retired propose button, the sheet, the canvas chip.
- F028 D8 — the sheet's portal and the report's origin clause.

## How to review

Start with `packages/orchestration/task_injection.py`, then `_fold_task_injections` in
`packages/orchestration/pingpong_job.py`, `apps/cli/commands/job_inject_cmd.py`,
`_dispatch_injection` in `packages/orchestration/ui_server.py`, and
`apps/ui/src/components/panels/AddTaskSheet.tsx` with `apps/ui/src/api/injectSend.ts`. The Built
State of `docs/roadmap/features/T5_F028.md` names the test for each acceptance line; the live proof
is `tests/ui_server/test_task_injection_e2e_live.py`. Each building round's mutation tool is
`.agent/authored/f028-r<n>-mutations.py` (round 9's is `f028-r9-probes.py`).

## Changed files

49 files outside `.agent/` against the fork point `ceb90b8a`, counted by `git diff --name-only`
before the closure commit plus `README.md`: 9 under `packages/` and `apps/cli/`, 21 under `apps/ui/`
for the send and view modules, the sheet, the pills, the canvas chip and their vitest suites, 13
under `tests/` — 12 Python test files and the import-reachability allowlist — and 6 others — `docs/guides/exit-codes.md`,
`docs/ui/design_reference/assumption_log.md`, the feature file, the checklist's consolidation
paragraph in `docs/agents/planner_reviewer_prompt.md`, `docs/roadmap/STATUS.md` and `README.md`.
`git diff --stat ceb90b8a..HEAD` lists them.

## Verification

- The one full suite on the tree that ships: `20018 passed, 20 skipped` at exit 0, no bad node
  (`.agent/authored/f028-closure-suite.txt`).
- The reviewer's headless-Chrome renders of the sheet, the pills and the canvas chip at rounds 7 and
  8, the second measuring the sheet 24 pixels inside the viewport's edges after R-1079's repair.
- The closure's self-use item: none — the queue held no pending item and the generator found no
  source (`self-use NONE (queue exhausted)`).
- Evidence job `f028r11e1001` against the fork point `ceb90b8a`: 1362 selected tests passed at exit 0.
- Review package `remedy-review-20260927-132129-READY_FOR_REVIEW.zip`, SHA-256
  `904723bf332d1f076cdfde262f84609fada02ca86635f3ef09a88c3d025692fe`, READY_FOR_REVIEW.

## Findings and notes

Latest verdict PASS; accepted PASS. F028 registered R-1076, R-1077, R-1078 and R-1079 and resolved
all four. No finding is open.

## Runtime actuals

Twelve rounds in two sessions, from the branch's first commit at 07:26 to the accepted head at 13:18
on 2026-09-27; reviewer and workers ran as Claude Opus 5.5; tokens and cost not measured.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
