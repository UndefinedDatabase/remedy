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
- [x] R-0146 --dry-run is a read-only preview (fixed, tests green)
- [x] T003 kill -9 / resume subprocess test (exactly-once proof)
- [ ] Integration gate
- [ ] Closure

## Current Step
Round 2 complete: R-0146 fixed, T003 green.
test_resume_kill.py 7 passed (1.28s) · test_resume_cli.py 35 passed ·
test_checkpoints.py 37 passed · test_long_run_executor.py 49 passed ·
canary 42 passed · ruff clean. Awaiting the reviewer verdict.

## Next Steps
Integration gate, then closure. Docs: `remedy job resume` gained two new
behaviors (F047 mode, --dry-run preview) — docs update belongs to closure
(docs/resume.md does not exist; its two tests are pre-existing red on
main).

## Risks
- Checkpoint write failure must not kill the run: log loudly,
  continue, retry next cycle (A9 default from the feature file).
- Resume must consume plan-approval gate and pending stop requests —
  never bypass (feature file "How it fits").
