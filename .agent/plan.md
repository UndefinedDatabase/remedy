# Plan — F287 Provider session continuity across relaunch

## Goal
A relaunch of a task that a pause or a stop interrupted resumes, on the `claude-cli` provider, the
builder and reviewer sessions the task last used, so finished work is not paid for twice; every
other production provider records that it did not resume (docs/roadmap/features/T3_F287.md).
DECISION F287 D1 fixes the slices and their order; T001 to T003 have landed.

## Current Step
Round 10, the end of the hardening stage (operator amendment amend0930b-slow-cap): save the
repeated audit (`.agent/f287_acceptance_reaudit1.md`, gap closed), correct the docstring and one
comment of `tests/cli/test_job_run_session_resume.py` (the rest of R-1163's repair), and write the
feature file's Built State with the stage's record (closure preconditions 4, 7 and 8).

## Next Steps
1. The closure sequence (docs/roadmap/STATUS_closure_protocol.md): book round 10 and resolve
   R-1163; the self-use item run to its approval gate; the one full suite; the checklist's
   consolidation pass; the evidence job and the review package; the ledger rotation, the STATUS
   line with its README sync, and the pull request, left unmerged.

## Risks
- Repair rounds on `claude-cli` now send shortened prompts to a continued session (F106, F109,
  DECISION F287 D6); the closure's self-use run is the first real observation.
- R-1163 (Low, F287): open until this round's docstring correction is reviewed.
- R-1162 (Low, F297): a `claude-cli` job with no model configured cannot finish a stop.
- R-1160 (Medium) and R-1138, R-1139, R-1143, R-1149, R-1156, R-1157, R-1158 (Low) stay open,
  owned by F297.
