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
Integration gate: full suite on the branch vs. base 89c4ef0, parity
comparison, canary. Round-2 verdict PASS is persisted
(LAST_REVIEWED_SHA = 72fc653). No closure artifacts in this round.

## Next Steps
Closure (its own reviewer-gated round): evidence job, review package,
Built State in T1_F047.md, STATUS line. Docs: `remedy job resume` gained
two behaviors (F047 mode, --dry-run preview) — docs/resume.md does not
exist and its two tests are pre-existing red on main.

## Risks
- Checkpoint write failure must not kill the run: log loudly,
  continue, retry next cycle (A9 default from the feature file).
- Resume must consume plan-approval gate and pending stop requests —
  never bypass (feature file "How it fits").
