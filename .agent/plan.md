# Plan — F302 The claude-cli worker's tokens per call: measure, attribute, cut

## Goal
The tokens one `claude-cli` call spends before it does any work are measured, attributed to their
sources and cut by the configuration Remedy starts the worker with; `remedy stats` shows tokens by
kind per call and per landed change (docs/roadmap/features/T3_F302.md; DECISIONs F302 D1 to D3).

## Current Step
Round 4 on `feature/f302-claude-cli-tokens`: book round 3, register R-1235 (owned by F297) with
DECISION F302 D3, and run T003's measurement once with `.agent/authored/f302-r4-measure.py`: the
fixed question before and after the cut, and one small real task as a job before and after, at
most twelve provider calls, its readings saved as `.agent/f302_after.jsonl` and
`.agent/f302_after.md`.

## Next Steps
1. T003's Built State from the readings; a cut that made the job fail review is turned back on.
2. T004: `remedy stats` gains tokens by kind per call and per landed change, per role and provider.
3. Closure: the one full suite, the self-use item, the evidence and the package, the STATUS line.

## Risks
- R-1235 (Low) is open and owned by F297. R-1138, R-1139, R-1143, R-1149, R-1156, R-1157, R-1158,
  R-1162, R-1172, R-1176, R-1196, R-1219, R-1220, R-1225 and R-1230 (Low) are open and owned by
  F297; F302 owns none.
