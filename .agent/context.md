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
`.agent/f077_t002_inventory.md` and `.agent/f077_t003_inventory.md`, the
read-only T002 and T003 inventories; plus `.agent/**` round state and the one
claimed STATUS line. Since R8 the module carries T002's
ACTION, `act_on_trips` — the pause, the deduped decision and the
`watchdog_tripped` ledger entry — and since R10 it is WIRED: `watchdog_pass` is
the loop's single entry point and `run_mission` calls it once per continuing
iteration, with D7's watchdog clause in both status docstrings. A tripped run's
ledger reads `[1, 2, 3, 3]` and that is CORRECT: an entry's `iteration` is an
ATTRIBUTION — which iteration it belongs to — and never a unique key (DECISION
F077 D11, which withdraws D10 unimplemented and resolves R-0388 as a
misdiagnosis). R12 repaired the one test that had encoded the imagined
invariant, so `tests/orchestration/test_orchestrator_loop.py` is `196 passed`
and the branch is green. R13 then inventoried T003's surface read-only and
touched no product file. R14 built the first half of T003 and widened the
in-scope set to `watchdog.evaluate_mission` — the read-only twin
`watchdog_pass` now routes through — plus the two mission verbs
`mission watchdog` (read-only) and `mission resume` (D4-scoped to the status),
and with them `apps/cli/command_catalog.py`, `apps/cli/commands/mission_cmd.py`
and `tests/cli/test_mission_cmd.py`. `apps/cli/commands/worker_facade_cmd.py`
stays OUT: two exact-set guards live there (inventory Q6). R15 finished T003
and added two more in-scope symbols: `watchdog.latest_trips_from_ledger`, the
pure reader that reconstructs the trips a ledger already RECORDS, and the trip
LEAD in `_cmd_mission_show` under DECISION F077 D12 — text and `--json`, and
`show` re-evaluates nothing, so what it reports is the trip that caused THIS
pause. `packages/orchestration/mission_state.py` stays OUT with the facade:
`render_mission_chain` takes a `Mission` and the trips live in the LEDGER that
`orchestrator_loop` owns, and `orchestrator_loop` imports `mission_state`, so
reading the ledger from the renderer would invert that dependency into the
import cycle `watchdog` keeps its imports inside function bodies to avoid. Open
findings at the session close: THIRTY, next free id R-0400.

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
- The reviewer MEASURES its block mechanically on the final bytes before
  emission and keeps it under 400 lines (DECISION F105 D5) — the cap that is
  actually enforceable — with 240 the preferred target, not a ceiling nobody
  counted. R-0389 registers a 293-line block emitted against the old unmeasured
  240 figure; the cap exists so the block-save commit stays inside the
  500-insertion limit (R-0381).
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
→ R11 record the R10 FAIL, register R-0387 to R-0390 and DECISION F077 D10,
then HALT at the ordered repair: the loop DOES record after a trip, so D10's
number collides on the safe-point path ✅ (the halt was the block's own stop
clause) → R12 record the R11 PASS, register R-0391, resolve R-0388 as a
misdiagnosis and R-0390, decide DECISION F077 D11 and repair the one red test —
no production file touched (its own verdict lands in R13) → R13 record the R12
PASS, register R-0392 and INVENTORY T003 read-only — the mission-verb wiring,
the side-effect-free evaluator, the dedup's real home, the report surface, the
guards and the paused-mission pass → R14 record the R13 PASS, decide DECISION
F077 D12 and build the first half of T003 against the inventory: the read-only
`watchdog.evaluate_mission`, the manual `mission watchdog` CLI and the
`mission resume` verb, report surface deferred → R15 record the R14 verdict,
register R-0393 and build that report surface — `latest_trips_from_ledger` plus
the trip lead in `_cmd_mission_show` under D12, which completes T003 → R16 the
integration gate: 16898 passed on the branch, zero branch-only failures, all
eight base-only ids attributed to the environment → R17 records that gate and
writes the ist-doc → closure per docs/roadmap/STATUS_closure_protocol.md.
