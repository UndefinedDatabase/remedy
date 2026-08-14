# Context — F057 Rate-limit-aware scheduler

## Active Branch
feature/f057-rate-limit-scheduler, cut from main at 21c8148e after the
paydown0814 PR #198 merged at the Open PR Gate. F057 is claimed `[~]` in
docs/roadmap/STATUS.md for the life of this branch.

## Scope
In: `packages/orchestration/rate_governor.py` and
`tests/orchestration/test_rate_governor.py`, both new, plus the `.agent/**`
round state and the one claimed STATUS line. R1 builds T001 only — signal
normalization — so nothing imports the new module yet.

Out: the per-call retry policy in `packages/orchestration/provider_timeouts.py`,
parallelism itself, and the provider adapters' internals. All three are the
feature file's Do-not-touch list. `packages/orchestration/pingpong_loop.py`
holds the seam and stays untouched until T003.

## Constraints
- The main session writes nothing in the work tree; a delegated worker subagent
  makes every commit (docs/agents/self_drive_protocol.md).
- Merges only at the Open PR Gate and never a PR this session created; never
  force-push; never work on main.
- Verification is pytest, scoped per round, plus the canary
  tests/cli/test_golden_path.py. A round that touches docs/roadmap/** also
  gates tests/docs/. Destructive and red-proof checks run only inside a
  disposable git worktree under .remedy-wt/, so resource safety stays intact
  and no background pytest process is ever left running.
- Unit tests use an injected clock. A real sleep in a unit test is a finding
  the feature file names in its Orchestrator brief.
- A round pushes after EVERY commit, not once at its last step (R-0289).

## Steps
R1 claim and T001 signal normalization → R2 T002 governor and acquire
semantics → R3 T003 seam, wait evidence and the fixture end-to-end →
integration gate → closure.
