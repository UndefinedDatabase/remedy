# Plan — F047 Checkpoint & resume (kill-proof)

## Goal
A hard-killed run loses nothing but the in-flight task: after every cycle
a checkpoint captures where the run stands, and
`remedy job resume <id>` continues from the newest valid one.
Corrupted checkpoint falls back to the previous valid one; a
never-checkpointed job degrades honestly to plain re-run of pending
tasks.

## Checklist
- [x] Setup: Open PR Gate (#152 merged), branch, STATUS claim, state files
- [x] T001 checkpoint writer/loader + hashing + retention + unit tests
- [x] T002 resume CLI + head verification + gate/stop interplay + tests
- [ ] T003 kill -9 / resume subprocess test (exactly-once proof)
- [ ] Integration gate
- [ ] Closure

## Current Step
Round complete: Setup + T001 + T002 all green.
test_checkpoints.py 35 passed · test_resume_cli.py 25 passed ·
canary tests/cli/test_golden_path.py 42 passed · ruff clean on every
touched file. Awaiting the reviewer verdict.

## Next Steps
T003 kill test (tests/orchestration/test_resume_kill.py), then the
integration gate, then closure. Docs: `remedy job resume` gained a second
mode — docs update belongs to closure (docs/resume.md does not exist;
its two tests are pre-existing red on main).

## Risks
- Checkpoint write failure must not kill the run: log loudly,
  continue, retry next cycle (A9 default from the feature file).
- Resume must consume plan-approval gate and pending stop requests —
  never bypass (feature file "How it fits").
