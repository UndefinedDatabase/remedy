# Context — F057 Rate-limit-aware scheduler

## Active Branch
feature/f057-rate-limit-scheduler, cut from main at 21c8148e. F057 is claimed
`[~]` in docs/roadmap/STATUS.md and stays claimed until closure. No PR exists
for this branch yet; one is created at closure, not before.

## Scope
In: `packages/orchestration/rate_governor.py` and
`tests/orchestration/test_rate_governor.py`, plus `.agent/**` round state and
the one claimed STATUS line. T001 is complete and reviewed; T002 (the governor)
and T003 (the seam) remain.

Out: the per-call retry policy in `packages/orchestration/provider_timeouts.py`,
parallelism itself, and the provider adapters' internals — the feature file's
Do-not-touch list, verified byte-identical at every round so far.
`packages/orchestration/pingpong_loop.py` holds the T003 seam and stays
untouched until then.

## Constraints
- The main session writes nothing in the work tree; a delegated worker subagent
  makes every commit (docs/agents/self_drive_protocol.md).
- Merges only at the Open PR Gate; never force-push; never work on main.
- Verification is pytest, scoped per round, plus the canary
  tests/cli/test_golden_path.py. A round touching docs/roadmap/** also gates
  tests/docs/. Destructive and red-proof checks run only inside a disposable
  git worktree under .remedy-wt/, so resource safety stays intact and no
  background pytest process is ever left running.
- Repository-wide `ruff check` is RED at base 21c8148e with 26 pre-existing
  errors (20 I001, 4 F401, 1 F821, 1 UP035). It is NOT a round gate; ruff is
  gated scoped to the files this feature owns. Repairing it is a paydown
  branch's job, not this one's (R-0364).
- Unit tests use an injected clock. A real sleep in a unit test is a finding.
- A round pushes after EVERY commit, not once at its last step.

## Steps
R1 claim and T001 ✅ → R2 findings and two fixes ✅ → R3 verdict and session
close ✅ → next session: T002 governor → T003 seam → integration gate → closure.
