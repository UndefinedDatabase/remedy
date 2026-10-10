# Plan — F302 The claude-cli worker's tokens per call: measure, attribute, cut

## Goal
The tokens one `claude-cli` call spends before it does any work are measured, attributed to their
sources and cut by the configuration Remedy starts the worker with; `remedy stats` shows tokens by
kind per call and per landed change (docs/roadmap/features/T3_F302.md; DECISION F302 D1).

## Current Step
Round 1 on `feature/f302-claude-cli-tokens`: claim F302, book F301's round 11, save T001's
inventory as `.agent/f302_inventory.md`, record DECISION F302 D1, and move `build_claude_cli_args`
with its constants to `packages/orchestration/claude_cli_command.py` unchanged (structure rule 2).

## Next Steps
1. T002: the attribution — one fixed task, everything loaded and each source switched off, in a
   scratch repository and in a worktree of Remedy, at most twenty provider calls, the readings
   saved under `.agent/`.
2. T003: the cut — the leanest configuration that keeps a builder good becomes the default, each
   source with a key that turns it back on, and a run's evidence names the configuration.
3. T004: `remedy stats` gains tokens by kind per call and per landed change, per role and provider.
4. Closure: the one full suite, the self-use item, the evidence and the package, the STATUS line.

## Risks
- The `claude` binary refused to run for the loop's agents in this session; T002 starts it only
  through Remedy's own provider path, as every job does.
- R-1138, R-1139, R-1143, R-1149, R-1156, R-1157, R-1158, R-1162, R-1172, R-1176, R-1196, R-1219,
  R-1220, R-1225 and R-1230 (Low) are open and owned by F297; F302 owns none.
