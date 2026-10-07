# Plan — F287 Provider session continuity across relaunch

## Goal
A relaunch of a task that a pause or a stop interrupted resumes, on the `claude-cli` provider, the
builder and reviewer sessions the task last used, so finished work is not paid for twice; every
other production provider records that it did not resume (docs/roadmap/features/T3_F287.md).
DECISION F287 D1 fixes the slices and their order; T001 to T003 have landed.

## Current Step
Session 3, round 17: the closing round. Book round 16's PASS, rotate the ledger, accept F287 in
STATUS with its README sync and the self-use entry SU-046's `consumed_by`, push, and open the
pull request. F287 owns no open finding; the nine open findings are owned by F297.

## Next Steps
1. The next session: Phase 1 rule 1 (`.agent/STOP`), then the Open PR Gate merges F287's pull
   request; round 17's verdict is booked in the next feature's first commit.
2. Then Rule A5: the next unchecked feature in `docs/roadmap/STATUS.md`, F116.

## Risks
- Repair rounds on `claude-cli` now send shortened prompts to a continued session (F106, F109,
  DECISION F287 D6); the closure's self-use run needed no repair round, so that is not yet
  observed in real use.
- R-1160 (Medium) and R-1138, R-1139, R-1143, R-1149, R-1156, R-1157, R-1158, R-1162 (Low) stay
  open, owned by F297.
