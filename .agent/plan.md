# Plan — F295 Machine client contract v1

## Goal
Remedy can be driven end to end by a program through the command line's JSON envelope alone: an
order file, one digest, decisions answered with `--json`, an approved apply and the proof
(docs/roadmap/features/T12_F295.md). DECISION F295 D1 fixes the slices and their order.

## Current Step
Session 7, round 28: the closing round. Book round 27's PASS, rotate the ledger, accept F295 in
STATUS with its README sync and the self-use entry SU-045's `consumed_by`, push, and open the
pull request. F295 owns no open finding; the seven open findings are owned by F297.

## Next Steps
1. The next session: Phase 1 rule 1 (`.agent/STOP`), then the Open PR Gate merges F295's pull
   request; round 28's verdict is booked in the next feature's first commit.
2. Then Rule A5: the next unchecked feature in `docs/roadmap/STATUS.md`, F287.

## Risks
- R-1138, R-1139, R-1143, R-1149, R-1156, R-1157 and R-1158 (Low) stay open, owned by F297.
- Another actor switched the primary checkout during round 24 (operator question Q6).
