# Plan — F047 Checkpoint & resume (kill-proof)

## Goal
A hard-killed run loses nothing but the in-flight task: after every cycle
a checkpoint captures where the run stands, and
`remedy job resume <id>` continues from the newest valid one.
Corrupted checkpoint falls back to the previous valid one; a
never-checkpointed job degrades honestly to plain re-run of pending
tasks.

## Checklist
- [ ] Setup: Open PR Gate (#152 merged), branch, STATUS claim, state files
- [ ] T001 checkpoint writer/loader + hashing + retention + unit tests
- [ ] T002 resume CLI + head verification + gate/stop interplay + tests
- [ ] T003 kill -9 / resume subprocess test (exactly-once proof)
- [ ] Integration gate
- [ ] Closure

## Current Step
Setup + T001 + T002 (this round). T003 is a separate round.

## Next Steps
T003 kill test, then integration gate, then closure.

## Risks
- Checkpoint write failure must not kill the run: log loudly,
  continue, retry next cycle (A9 default from the feature file).
- Resume must consume plan-approval gate and pending stop requests —
  never bypass (feature file "How it fits").
