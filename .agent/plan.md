# Plan — F295 Machine client contract v1

## Goal
Remedy can be driven end to end by a program through the command line's JSON envelope alone: an
order file, one digest, decisions answered with `--json`, an approved apply and the proof
(docs/roadmap/features/T12_F295.md). DECISION F295 D1 fixes the slices and their order.

## Current Step
Round 29, at the Open PR Gate of pull request 311: the first hosted CI run failed one node on
Python 3.12. Book round 28's PASS, register that node as R-1159 (Low, owned by F297) and land
DECISION F295 D21, then push; the push's fresh hosted run is the one re-run.

## Next Steps
1. Green fresh run: the Open PR Gate merges pull request 311, then Rule A5 claims F287.
2. Red fresh run: nothing is merged; an operator question is written and the session stops.

## Risks
- R-1138, R-1139, R-1143, R-1149, R-1156, R-1157, R-1158 and R-1159 (Low) stay open, owned by F297.
- Another actor switched the primary checkout during round 24 (operator question Q6).
