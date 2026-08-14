# Context — F077 Autonomy watchdog

## Active Branch
feature/f077-autonomy-watchdog, cut from main after PR #199 merged. F077 is
claimed `[~]` in docs/roadmap/STATUS.md and stays claimed until closure. No PR
exists for this branch yet; one is created at closure, not before.

## Scope
In: a new `packages/orchestration/watchdog.py` and
`tests/orchestration/test_watchdog.py`; `packages/orchestration/config.py` for
the four `watchdog.*` threshold keys (`watchdog.no_progress_repeats`,
`watchdog.burn_window`, `watchdog.burn_min_samples`,
`watchdog.burn_multiplier`); the pause seam in
`packages/orchestration/orchestrator_loop.py`, plus `.agent/**` round state and
the one claimed STATUS line.

Out: repair logic, class-expectation anomaly detection and loop policy — the
F077 feature file's Do-not-touch list. The watchdog never modifies plans, jobs
or dossiers; that independence is an acceptance criterion, not a preference.

## Constraints
- The main session writes nothing in the work tree; a delegated worker subagent
  makes every commit (docs/agents/self_drive_protocol.md).
- Merges only at the Open PR Gate; never force-push; never work on main.
- Verification is pytest, scoped per round, plus the canary
  tests/cli/test_golden_path.py. A round touching docs/roadmap/** also gates
  tests/docs/. Destructive and red-proof checks run only inside a disposable
  git worktree under .remedy-wt/, so resource safety stays intact.
- Repository-wide `ruff check` is RED on main with pre-existing errors and is
  NOT a round gate (R-0364); ruff is gated scoped to the files F077 owns.
- Reviewer blocks stay at or under 240 lines so the block-save commit stays
  inside the 500-insertion cap (R-0381).

## Steps
R1 merge PR #199, claim F077, reset the record, register R-0380 and R-0381 ✅ →
R2 the T001 inventory ✅ → R3 record the R2 verdict and close the session ✅ →
R4 T001 the three evaluators, their config keys and their tests → R5 T002 pause
and decision → R6 T003 CLI and report → R7 integration gate then closure.
