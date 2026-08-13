# Context — F045 Loop definitions

## Active Branch
feature/f045-loop-definitions, cut from main at cb3ef34f after the F115
closure PR #195 and the amend0813 PR #196 were both merged. F045 is claimed
`[~]` under Rule A5 as the first `[ ]` line of docs/roadmap/STATUS.md
(Package 1 Self-Use, Tier 2).

## Scope
In: a declarative LOOP — trigger, scope, action, budgets, stop rules — living
as `[[loop]]` array-of-tables in the project's remedy.toml, a loader that
validates every spec with the loop's name in each message, and a runner that
materializes a loop as an ordinary job/mission carrying loop_ref provenance.
Budgets reuse the F018/F104 budget field names; actions reuse the golden path
and missions. Nothing here executes work by itself.

Out, per the feature file's Do-not-touch: scheduling and cron, the routine
library, notifications. Schedule and event triggers are parsed and validated
but explicitly inert until the scheduler feature; running one says so.

## Constraints
- SPLIT rounds are mandatory: this feature touches packages/ and apps/, and
  production code never merges self-certified
  (docs/agents/planner_reviewer_prompt.md §3).
- The main session writes nothing in the work tree; a delegated worker subagent
  makes every commit (docs/agents/self_drive_protocol.md).
- Merges only at the Open PR Gate; never force-push; never touch main.
- A round pushes after EVERY commit, not once at its last step (R-0289).
- Verification is pytest, scoped per round, plus the canary
  tests/cli/test_golden_path.py. A round touching docs/roadmap/ also runs
  tests/docs/. The full suite runs only at the integration gate, with
  `-n auto`. Destructive and mutation checks run only inside a disposable git
  worktree, so resource safety stays intact and no background pytest process is
  ever left running.
- Loops are configuration, NOT a new directory convention: they live inside
  the existing config file and add no second config location.
- A loop never implies `--yes`. Unattended execution is an explicit, audited
  field of the spec.

## Steps
R1 claim, state reset and T001 spec model → T002 run materialization and
loop_ref provenance → T003 CLI, last-run display and the fixture loop →
integration gate → closure.
