## What

F027 — Task veto. An operator can strike one task of a job with a mandatory reason, from the CLI
(`remedy job veto-task <job> <task> --reason "<text>"`) or from the task's detail popover, whose
"Veto task" form appears only for a task that can still be vetoed. The veto is a create-only control
file per task, never a write to the job record, and the reason is kept verbatim. The linear runner
folds the veto at every safe point: an active attempt's workspace goes back to its start tree, the
task becomes `vetoed`, its unreachable downstream (`blocked_downstream` over the vetoed tasks) is
never dispatched, independent branches run on, and a run whose remaining work is all vetoed ends
`blocked` naming both sets; a task vetoed during its own provider call finishes that call first.
Every veto files one `replan_proposal` decision offering "Replan the remaining work as a new job" or
"Accept the smaller scope"; nothing replans without the answer. A replan creates an unplanned
follow-up job that nothing runs; once every veto is answered, the next run completes the job with
the reduced scope. The page strikes the node, fades its unreachable set, shows the reason on hover,
and gives the popover a Veto or Unreachable section with links to the task on the other side; the
job's report prints "Vetoed by <actor>: <reason>".

## Why

The human red line: one click and one reason stops a task the operator has judged wrong, without
stopping the job and without anything replanning behind the operator's back.

## Key decisions (in `.agent/decisions.md`)

- F027 D1 — the veto as a create-only control fact with the reason verbatim, the pure gate, the
  unreachable set, one `task_vetoed` event, no un-veto.
- F027 D2 and D3 — the linear runner's fold with the workspace restore, the in-flight veto, and the
  cycle executor withholding vetoed work.
- F027 D4 — the `replan_proposal` decision, its answers, the unplanned follow-up job, and the settled
  completion.
- F027 D5 and D6 — `job.veto-task` in the catalog, the CLI and the write door; the door answering the
  proposal; the door guard skipping type-only imports.
- F027 D7 and D8 — the dashboard's `vetoes` section, the seeded and streamed node, the report lines,
  the option labels, the fade, the hover text, the popover sections and the veto form.
- F027 D9 — the diamond end-to-end through the real CLI and a live door, both answers to their
  effects.

## How to review

Start with `packages/orchestration/task_veto.py` and `packages/orchestration/veto_proposal.py`, then
the fold in `run_job` in `packages/orchestration/pingpong_job.py` (`_fold_task_vetoes` and the
terminal accounting), the cycle executor's pick in `packages/orchestration/long_run_executor.py`, the
CLI in `apps/cli/commands/job_veto_cmd.py`, and the door's clause and `_build_veto_section` in
`packages/orchestration/ui_server.py`. The page: `apps/ui/src/api/vetoView.ts`, `vetoSend.ts`,
`components/detail/TaskVetoForm.tsx`, the popover's sections in `DetailPopover.tsx`, and the fade and
hover in `components/graph/ForceBrainGraph.tsx`. The Built State of
`docs/roadmap/features/T5_F027.md` names the test for each acceptance line; each round's mutation
tool is `.agent/authored/f027-r<n>-mutations.py`.

## Verification

- The one full suite, taken on the tree that ships after two repair rounds: `19694 passed,
  20 skipped` at exit 0, no bad node (`.agent/authored/f027-closure-suite.txt`).
- The diamond end-to-end `tests/ui_server/test_task_veto_e2e_live.py`: a veto through a live door on
  a job paused after its first task, the other branch completing through the real CLI, the job
  blocked naming the veto, the proposal open, and both answers carried to their effects, with a
  reason holding `<`, `&` and double quotes read byte for byte from the door to the report.
- Evidence job `f027r13e1001` against the fork point `557cbbcc`: 1661 selected tests passed at exit
  0, the eslint, tsc and vitest nodes among them.
- Review package `remedy-review-20260926-111715-READY_FOR_REVIEW.zip`, SHA-256
  `abb65b1df0346c8670423a7da903e3e3c6facfc4cac4602bb5a983b47b4bd993`, READY_FOR_REVIEW.

## Findings and notes

Latest verdict PASS; accepted PASS. F027 registered R-1065 to R-1072 and resolved all eight: a
retried veto's refusal shape, a directory standing where a restored file stood, the CLI naming the
wrong relaunch command, the page's event catalog missing both veto events, two shipped sentences
naming a rule and a module that do not exist, a lead-in with no list under it, a stale exact-set pin
the closure suite found, and a live pause test that failed under the suite's parallel load. No
finding is open. The closure's self-use track read `self-use NONE (queue exhausted)`: the queue held
no pending item and the ledger no open finding. A reviewer's load reproduction during the closure left
91 local branches `remedy/<id>` at `09276159` in the shared repository; they carry no commit of their
own and may be deleted by the operator.

## Runtime actuals

Fourteen rounds over two sessions, from the branch's first commit at 03:14 to the accepted head at
11:13 on 2026-09-26; reviewer and workers ran as Claude Opus 5.5; tokens not measured.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
