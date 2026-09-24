## What

F015 — Interactive plan editing. Before a job's plan is approved, the human can reshape it: edit a
task's title, goal, acceptance criteria, size band or file hints; delete a task (whatever waited for
it then waits for what it waited for); reorder the tasks; merge tasks; split a task by its criteria;
and add, change or remove one criterion. Every edit is one locked transaction on the stored plan,
checked by the planner's own schema, dependency and deliverable rules, and it either lands whole
with a new plan version and a log entry or changes nothing and says why. The edits are reachable
from the CLI (`remedy job plan-show`, `remedy job plan-edit-task`, `plan-delete-task`,
`plan-reorder`, `plan-merge-tasks`, `plan-split-task`, `plan-edit-acceptance`) and through the
cockpit's single write door. An approval records the content hash of exactly the plan it approved,
and a job refuses to start if its plan or task list is not that plan.

## Why

A plan the human cannot adjust can only be accepted or rejected whole. Editing is safe only if an
edit can never race the approval, never be lost to an older copy, and never change what runs after
approval; each of those is a mechanism here, with a test that fails when the mechanism is removed.

## Key decisions (in `.agent/decisions.md`)

- F015 D1 — one locked write of the job record carries the edited plan, its `_version`, its
  whole-list `_edits` log and the regenerated task list.
- F015 D2 — both approval doors consume the approval under the same lock against the record as it
  is then; the CLI lives under `job` because `plan` is the retired roadmap word.
- F015 D3 — the write door exposes the six edits, requires `expected_version`, and answers a
  refused edit with its reason.
- F015 D4 — the approved plan's content hash is checked at every job start; because a job runs
  its tasks in plan order, an edit may not put a task before a task it waits for; an edited
  revision's `plan_v<n>.md` names its edits.
- F015 D5 — the closure suite's two bad nodes: `runtime stop` now waits out a supervisor that has
  already recorded its application's exit instead of reporting a false failure, and the CLI
  subprocess hang guard in the test helper is 30 seconds.

## How to review

Start with `packages/orchestration/plan_editing.py`, then the approval call sites in
`apps/cli/commands/decision.py` and `packages/orchestration/ui_server.py`, the CLI in
`apps/cli/commands/job_plan_cmd.py`, and the start check in `run_job`. The Built State of
`docs/roadmap/features/T5_F015.md` names the test for each acceptance line; each round's mutation
tool is `.agent/authored/f015-r<n>-mutations.py`.

## Verification

- The one full suite, re-run after one repair round: `19057 passed, 20 skipped` at exit 0, no bad
  node (`.agent/authored/f015-closure-suite.txt`).
- Evidence job `f015r8e1001` against the fork point `fce49ce0`: 922 selected tests passed at exit 0.
- Review package `remedy-review-20260924-151010-READY_FOR_REVIEW.zip`, SHA-256
  `920b9e1c3763632b86e97cb9724831e9c9e58378bbc71bac4532638e976da840`, READY_FOR_REVIEW.

## Findings

None registered. The four open findings are owned by the next findings paydown, F284.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
