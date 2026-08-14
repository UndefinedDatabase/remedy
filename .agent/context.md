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
`packages/orchestration/orchestrator_loop.py`;
`.agent/f077_t002_inventory.md`, the read-only T002 inventory; plus `.agent/**`
round state and the one claimed STATUS line. Since R8 the module carries T002's
ACTION, `act_on_trips` — the pause, the deduped decision and the
`watchdog_tripped` ledger entry — and since R10 it is WIRED: `watchdog_pass` is
the loop's single entry point and `run_mission` calls it once per continuing
iteration, with D7's watchdog clause in both status docstrings. The four
whole-ledger guards DECISION F077 D8 predicted in
`tests/orchestration/test_mission_e2e.py` measured GREEN under the probe D9
ordered; the guard that actually broke is
`test_orchestrator_loop.py::test_one_entry_per_iteration_numbered_from_one`,
outside R10's authorised change set and left RED for R11. Open findings after
R10: NINETEEN, next free id R-0387.

Out: repair logic, class-expectation anomaly detection and loop policy — the
F077 feature file's Do-not-touch list. The watchdog never modifies plans, jobs
or dossiers; that independence is an acceptance criterion, not a preference.
Its only writes are the mission status, one escalation record on the job it
attaches to, and the ledger append.

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
- A block that asserts a PROPERTY of the code it orders — pure, read-only, no
  I/O — re-reads every function in that section against the assertion before
  emission, and narrows the assertion to the part that holds (R-0383).

## Steps
R1 merge PR #199, claim F077, reset the record, register R-0380 and R-0381 ✅ →
R2 the T001 inventory ✅ → R3 record the R2 verdict and close the session ✅ →
R4 T001 the three evaluators, their config keys and their tests ✅ → R5 record
the R4 verdict, repair R-0383 and inventory T002 ✅ → R6 record the R5 verdict
and register R-0384 ✅ → R7 record the R6 verdict, settle the eight T002
questions as DECISIONS F077 D1-D8 and repair R-0384 ✅ → R8 record the R7
verdict, register R-0385, resolve R-0384 and build T002's pause, deduped
decision and ledger entry as an UNWIRED action ✅ → R9 record the R8 verdict,
register R-0386 and close the session ✅ → R10 record the R9 verdict, register
DECISION F077 D9, wire the action into `run_mission`, write D7's docstring
clause and probe the e2e guards ✅ (one guard outside the change set left red)
→ R11 repair that guard, then T003 CLI, `mission resume` and report → R12
integration gate then closure.
