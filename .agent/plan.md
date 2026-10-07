# Plan — F295 Machine client contract v1

## Goal
Remedy can be driven end to end by a program through the command line's JSON envelope alone: an
order file, one digest, decisions answered with `--json`, an approved apply and the proof
(docs/roadmap/features/T12_F295.md). DECISION F295 D1 fixes the slices and their order.

## Current Step
Round 31, at the Open PR Gate of pull request 311: repair R-1159 in
`tests/ui_server/test_pause_door_live.py` per DECISION F295 D22 (3) and D24 (task 2's build call
held until the pause request exists; a DETAIL line on every assertion). Book round 30's PASS and
register R-1160, the after-task safe point that blocks a pause as a budget stop.

## Next Steps
1. The push of round 31 starts the one fresh hosted run of D22 (4): green → book R-1159 resolved,
   the Open PR Gate merges, Rule A5 claims F287; red → nothing is merged, an operator question is
   written and the session stops.
2. In SLOW MODE, F287 gets the hardening stage of operator amendment amend0930b-slow-cap before
   its closure sequence.

## Risks
- R-1160 (Medium) is open, owned by F297: a job pause arriving while a task is applied blocks the
  job instead of parking it (DECISION F295 D24).
- R-1159 (Low) stays open until a green hosted run.
- R-1138, R-1139, R-1143, R-1149, R-1156, R-1157 and R-1158 (Low) stay open, owned by F297.
