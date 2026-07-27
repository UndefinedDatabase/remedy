# Plan — F047 Checkpoint & resume (kill-proof) — CLOSED

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
- [x] Integration gate (PASS, zero F047-attributable regressions)
- [x] Closure (Built State, evidence job, READY zip, STATUS line)

## Current Step
CLOSED. Evidence job 29fbc2fe-60d6-4bb2-a7bb-05dc59dd40d7 · package
remedy-review-20260727-101857-READY_FOR_REVIEW.zip · accepted HEAD
8e870062feb3487f890232d659ef569cf3aa326e. PR #153 is ready for review and
NOT merged — the Open PR Gate merges it at the next feature's start.

## Next Steps
Worker idle. Next feature is selected by Rule A5 in a fresh session; the
Open PR Gate merges PR #153 first.

## Risks
- Carried risks are recorded in the Built State section of
  docs/roadmap/features/T1_F047.md (5 items: unknown live worktree head
  proceeds; checkpoint write failure surfaces only via job metadata plus a
  warning log; pre-existing full-suite xdist nondeterminism F135/F052;
  docs/resume.md absent as a BACKLOG gap item; integrity-check
  live_review_verdict matcher warn).
