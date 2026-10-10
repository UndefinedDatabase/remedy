# Plan — F302 The claude-cli worker's tokens per call: measure, attribute, cut

## Goal
The tokens one `claude-cli` call spends before it does any work are measured, attributed to their
sources and cut by the configuration Remedy starts the worker with; `remedy stats` shows tokens by
kind per call and per landed change (docs/roadmap/features/T3_F302.md; DECISION F302 D1).

## Current Step
Round 2 on `feature/f302-claude-cli-tokens`: book round 1, move the catalog's `stats` group to
`apps/cli/command_catalog_stats.py` unchanged (DECISION F302 D1 (4)) with a lessons test for it,
and run T002: the attribution script `.agent/authored/f302-r2-attribution.py`, twenty provider
calls, its readings saved as `.agent/f302_attribution.jsonl` and `.agent/f302_attribution.md`.

## Next Steps
1. T003: the cut — from T002's readings, the leanest configuration that keeps a builder good
   becomes the default in `packages/orchestration/claude_cli_command.py`, each source with a key
   that turns it back on, and a run's evidence names the configuration; the same task measured
   again after it.
2. T004: `remedy stats` gains tokens by kind per call and per landed change, per role and provider.
3. Closure: the one full suite, the self-use item, the evidence and the package, the STATUS line.

## Risks
- The `claude` binary refused to run for the loop's agents in this session; T002 starts it only
  through Remedy's own provider path, as every job does.
- R-1138, R-1139, R-1143, R-1149, R-1156, R-1157, R-1158, R-1162, R-1172, R-1176, R-1196, R-1219,
  R-1220, R-1225 and R-1230 (Low) are open and owned by F297; F302 owns none.
