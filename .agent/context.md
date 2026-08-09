# Context — F104 Hard budget enforcement

## Active Branch
feature/f104-hard-budget-enforcement, cut from main at 94f69b0f after PR #187 —
the F103 closure — was merged at the Open PR Gate. F104 is claimed `[~]` in
docs/roadmap/STATUS.md; it is the first `[ ]` entry after F103, which is what
Rule A5 names.

## Scope
In: `max_cost_usd` as an additive `JobBudgets` field with the F018 precedence
rules (CLI flag > env > project TOML > no limit); budget counters that read
cost actuals from the F103 per-project SQLite ledger through `query_cost`; the
unpriced notation propagating into every budget figure; a predictive stop at
the task-dispatch safe point with the reason `predicted_budget_exhausted:
<limit>` and a decision entry carrying spent, expected and basis; `remedy job
budget` showing spent, remaining and the next-task expectation with its basis
label.

Out, per the feature file's Do-not-touch: calibration from history,
per-task-class caps, burn-rate anomaly detection. Prices are never invented — a
cost figure exists only where a provider reported one.

## Constraints
- SPLIT rounds are mandatory: this feature touches packages/ and apps/, and
  production code never merges self-certified
  (docs/agents/planner_reviewer_prompt.md §3).
- The main session writes nothing in the work tree; a delegated worker subagent
  makes every commit (docs/agents/self_drive_protocol.md).
- Merges only at the Open PR Gate; never force-push; never touch main.
- Verification is pytest, scoped per round, plus the canary
  tests/cli/test_golden_path.py. A round touching docs/roadmap/ also runs
  tests/docs/. The full suite runs only at the integration gate, with
  `-n auto`. Destructive and mutation checks run only inside a disposable git
  worktree, so resource safety stays intact and no background pytest process is
  ever left running.
- An unmeasured or unpriced figure is NULL and prints as such; a measured zero
  and an unknown are never the same value (P6).

## Steps
Renumbered by DECISION F104 D7 after R5 became a repair round: R1 claim +
candidate sweep + T001 usd limit and ledger bridge → R2 T002 predictive engine
(fix R-0222) → R3 fix R-0224, the cost-side counter split → R4 T002 part 2, the
predictive stop wired at the live safe point → R5 fix R-0225/R-0226, the F012
manifest budget schema and the terminal-state pins → R6 T003 display, docs and
estimate labels → R7 integration gate → R8 closure.
