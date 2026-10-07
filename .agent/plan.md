# Plan — F295 Machine client contract v1

## Goal
Remedy can be driven end to end by a program through the command line's JSON envelope alone: an
order file, one digest, decisions answered with `--json`, an approved apply and the proof
(docs/roadmap/features/T12_F295.md). DECISION F295 D1 fixes the slices and their order.

## Current Step
Round 30, at the Open PR Gate of pull request 311: the one re-run failed the same node again
(R-1159). Book round 29's PASS, record the recurrence, land DECISION F295 D22 and operator
question Q7, push, and stop. Nothing is merged.

## Next Steps
1. The next session (unless the operator answers Q7 otherwise): one reviewed round on this branch
   repairs R-1159 in `tests/ui_server/test_pause_door_live.py` per DECISION F295 D22 (3).
2. Its push starts one fresh hosted run: green → the Open PR Gate merges, Rule A5 claims F287;
   red → nothing is merged, an operator question is written and the session stops.

## Risks
- R-1159 (Low) is owned by F295; its first instance, `FINAL:blocked`, is unexplained.
- R-1138, R-1139, R-1143, R-1149, R-1156, R-1157 and R-1158 (Low) stay open, owned by F297.
- Another actor switched the primary checkout during round 24 (operator question Q6).
