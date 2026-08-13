# Context — F115 Prompt breakdown & cost report

## Active Branch
feature/f115-prompt-cost-report, cut from main after PR #194 (the F111
closure) was merged at the Open PR Gate. F115 is claimed `[~]` under Rule A5
as the first `[ ]` line of docs/roadmap/STATUS.md (Package 1 Self-Use,
Tier 2).

## Scope
In: joining what already exists. The prompt-segment registry records a
manifest (segment names, ranks, hashes) into call evidence and the token
ledger stores per-call actuals; F115 persists the manifest alongside the
ledger row additively, aggregates over it, and renders `remedy stats report`
as markdown and json. No new capture and no new numbers — aggregation and
presentation only.

Out, per the feature file's Do-not-touch: pricing tables, calibration, UI
rendering and scheduled reporting. The report is on demand; this feature adds
no scheduler and no background job. Report generation is read-only: the state
snapshot before and after a run must be equal.

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
- Every number in the report is traceable to a ledger row. A period with
  missing data says so (P6); interpolation is a defect, not a fallback.

## Steps
R1 claim, state reset and shape inventory → T001 manifest-alongside-actuals
persistence → T002 aggregation queries, pure renderer and goldens → T003 CLI,
period comparison and json schema → integration gate → closure.
