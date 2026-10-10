# Plan — F302 The claude-cli worker's tokens per call: measure, attribute, cut

## Goal
The tokens one `claude-cli` call spends before it does any work are measured, attributed to their
sources and cut by the configuration Remedy starts the worker with; `remedy stats` shows tokens by
kind per call and per landed change (docs/roadmap/features/T3_F302.md; DECISIONs F302 D1 and D2).

## Current Step
Round 3 on `feature/f302-claude-cli-tokens`: book round 2, record DECISION F302 D2, move the two
`claude_planner` keys to `packages/orchestration/config_keys_claude.py` unchanged, then T003's cut:
`--safe-mode` and the role's tools on every worker command line, with the keys
`claude_cli.customizations` and `claude_cli.all_tools`, and the page
`docs/system/claude-cli-worker-launch-v1.md`.

## Next Steps
1. T003's record: `ExecutionConfig` and its two serializers leave `pingpong_job.py` unchanged;
   then a job's execution configuration names the two keys' values, and the client interface rises.
2. T003's measurement: the fixed question again under the defaults, and one small real task as a
   job with claude-cli builder and reviewer before and after the cut, each passing review; at most
   twelve calls; the figures by kind in the Built State.
3. T004: `remedy stats` gains tokens by kind per call and per landed change, per role and provider.
4. Closure: the one full suite, the self-use item, the evidence and the package, the STATUS line.

## Risks
- A cut that makes a job fail review is turned back on (DECISION F302 D2 (4)).
- R-1138, R-1139, R-1143, R-1149, R-1156, R-1157, R-1158, R-1162, R-1172, R-1176, R-1196, R-1219,
  R-1220, R-1225 and R-1230 (Low) are open and owned by F297; F302 owns none.
