# Plan — verified repair, reliable evidence, adaptive execution (operator order exec-1018b, 2026-10-18)

## Goal
A real test that fails after a passing review leads to one budgeted, evidence-fed repair instead of
a misleading completion or a pointless loop (R-1351); the review-report export is explained and
proven end to end; PRs 360, 361 and 362 are reviewed as one release. Branch
`feature/verified-repair` from PR 362's head `cfd906254`; worktree `.remedy-wt/verified-repair`.
Merge order: 360, 361, 362, this. No merge, no deploy; `.agent/STOP`, supervisor, live checkout
untouched. Outside the roadmap queue (F078 stays next).

## Current Step
1. R-1351 repaired in the loop's own test phase (`verified_repair.py`), with its acceptance walk.

## Next Steps
2. Review reports (P0 2): HTTP e2e through the supervisor; diagnosis in decisions (no `.data` read).
3. Combined review of 360-362 (P0 3), `_WALK_ORDER_DIR`; findings registered, then repaired.
4. P1: adversarial multi-file matrix (EN/DE), rule-file context tokens, lessons A/B, test-suite time.
5. At most three real local-model runs, only if every control holds; else the blocker is written.
6. Public API handoff, one full local gate on the final commit, PR, German handback.

## Risks
- `run_job`, `run_pingpong` and both files sit at their ledger rows: edits there stay line-neutral,
  new logic lives in `verified_repair.py`.
- Another session (Universe recording) uses local Ollama and the CPU: real runs check load first.
