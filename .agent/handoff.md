# Handoff — F046 Multi-cycle loop — Round 1 (Setup + T001 + T002)

Branch: feature/f046-multi-cycle-loop · base main `c14a83a` (PR #151 merged
by the Open PR Gate at feature start)
Review range: `c14a83a..d87a3e0` · LAST_REVIEWED_SHA `c14a83a`
Open findings: 0. Next expected action: reviewer verdict in
`.agent/live_review.md`, then the integration gate. Closure is a later step.

## Item status

| Item | Status | Reason |
|------|--------|--------|
| 0 — Setup (PR gate, branch, STATUS, state files) | done | c6e2389 |
| 1 — T001 loop skeleton + terminal matrix + fixture | done | a4a6874 |
| 2 — T002 evidence + config + CLI + regression | done | 8ad17ce, d87a3e0 |

## Commits

**c6e2389** chore(f046): claim F046 — branch, STATUS, state files

| file | +/- |
|------|-----|
| .agent/context.md | +20 −29 |
| .agent/live_review.md | +6 −43 |
| .agent/plan.md | +13 −31 |
| docs/roadmap/STATUS.md | +1 −1 |

**a4a6874** feat(f046): multi-cycle loop conductor with terminal-status matrix

| file | +/- |
|------|-----|
| .agent/decisions.md | +16 −0 |
| .agent/plan.md | +4 −3 |
| packages/orchestration/long_run_executor.py | +523 −0 |
| tests/orchestration/test_long_run_executor.py | +539 −0 |

**8ad17ce** feat(f046): per-cycle evidence records and the cycles.* config keys

| file | +/- |
|------|-----|
| docs/system/remedy-toml-configuration-system-v0.md | +13 −0 |
| packages/orchestration/config.py | +30 −0 |
| packages/orchestration/long_run_executor.py | +135 −1 |
| tests/orchestration/test_long_run_executor.py | +238 −2 |

**d87a3e0** feat(f046): remedy job run with a capped --cycles flag

| file | +/- |
|------|-----|
| apps/cli/command_catalog.py | +17 −0 |
| apps/cli/commands/job.py | +109 −0 |
| tests/orchestration/test_long_run_executor.py | +82 −0 |

Commit-size note (honest): a4a6874 is 1062 lines — a new module plus the
suite that proves it. Splitting module from tests would have produced a
commit whose tests do not exist yet and one whose module is untested; T002
WAS split into two commits (208 and 416 lines) for this reason.

## Terminal status → job state mapping

| terminal status | pingpong_job status | core RunState | trigger |
|---|---|---|---|
| all_green | `completed` | COMPLETED | every task COMPLETED, verify did not fail |
| stopped_by_operator | `stopped` | PAUSED | safe point reports an operator stop |
| budget_exhausted | `stopped` | PAUSED | safe point reports a budget limit hit |
| deadline_reached | `stopped` | PAUSED | `first_exhausted_limit == deadline` (injected clock) |
| blocked | `blocked` | PAUSED | zero ready tasks and not green — terminal, no spin |
| max_cycles_reached | `running` | (untouched) | cycle budget spent, work still pending |

`RunState` has no BLOCKED member, so the authoritative status is the
pingpong string, written to `job.metadata["cycle_terminal_status"]` /
`["cycle_job_status"]` and emitted as the `cycle_loop_terminal` ledger event.
`blocked` is PAUSED, not FAILED: "no ready task, not green" also covers a job
awaiting a decision — nothing failed and the job must stay resumable.

## Verification (real output, fresh at handback)

```
$ python3 -m pytest tests/orchestration/test_long_run_executor.py -q
.................................................                        [100%]
49 passed in 0.23s
exit=0

$ ruff check packages/orchestration/long_run_executor.py \
      packages/orchestration/config.py apps/cli/commands/job.py \
      apps/cli/command_catalog.py tests/orchestration/test_long_run_executor.py
All checks passed!
exit=0

$ python3 -m pytest tests/orchestration/test_job_task_runner.py \
      tests/orchestration/test_safe_points.py -q
269 passed in 101.07s (0:01:41)
exit=0
$ git diff --stat main...HEAD -- tests/orchestration/test_job_task_runner.py \
      tests/orchestration/test_safe_points.py
(no output — both files unmodified on this branch)

$ python3 -m pytest tests/cli/test_golden_path.py -q        # canary
..........................................                               [100%]
42 passed in 18.88s
exit=0
```

Ordering red-proof: neutering the safe-point break turned 8 tests red
(both ordering tests, both operator-stop tests, budget, deadline ×2); the
edit was reverted and the suite is green from the committed source.

## Open risks / notes for the reviewer

- The T002 regression is behavioral-plus-declared-delta, not literally
  byte-identical: `run_cycles` with defaults adds exactly two metadata keys
  and one cycle evidence record. The test asserts that this IS the only
  delta. At CLI level there is no delta at all — one cycle delegates to
  `_cmd_run_next_task_local` verbatim.
- The multi-cycle CLI branch is unreachable in production while
  `CYCLE_SAFETY_CAP == 1`; it is exercised in tests with the cap raised,
  simulating post-F075.
- Cycle records default to ON, so the slice suite's data-root fixture is
  autouse. 18 stray job dirs written into `.data/jobs/` during development
  before that fixture existed were removed.
- Pre-existing full-suite nondeterminism (backlog F135/F052) — not probed
  this round; the integration gate is the next step.
