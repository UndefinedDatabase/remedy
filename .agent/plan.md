# Plan — Steps 2146-2205: Open-Ended Dogfood Run Orchestrator + Replay Analyzer v0

## Goal
Make Remedy dogfoodable with open-ended, step-at-a-time run orchestration. No fixed
time profiles. Runs stop when done/blocked/budget/operator-stop.

## Core principle
Workers execute. Remedy governs. No provider execution. No auto-apply. No unbounded loops.
Done != Resolved. Reviewer verdict beats builder self-report.

## Current Step
2146-2205 — all 15 phases implemented; 48 targeted + 18 catalog + 6551 full suite (2 pre-existing).

## Steps
- [x] Phase 1: Architecture doc
- [x] Phase 2: Core run model (DogfoodRunStatus, DogfoodRunPolicy, DogfoodRunRecord, DogfoodRunCheckpoint)
- [x] Phase 3: Run storage (create/save/load/list/checkpoints/brainstorm)
- [x] Phase 4: Run evaluator (evaluate_dogfood_run)
- [x] Phase 5: Run stepping (step_dogfood_run, stop_dogfood_run)
- [x] Phase 6: Replay analyzer (analyze_dogfood_run_replay)
- [x] Phase 7: Brainstorm lane metadata
- [x] Phase 8: CLI surface (10 commands under remedy dogfood)
- [x] Phase 9: Command catalog + run contract entries
- [x] Phase 10: Progress ledger + review bundle integration
- [x] Phase 11: Integrity checks (8 invariants)
- [x] Phase 12: User guide doc
- [x] Phase 13: Targeted tests (48 passed)
- [x] Phase 14: Full suite (6551 passed, 2 pre-existing failures)
- [ ] Phase 15: Commit + push + reviewer verdict

## Hard rules
- No shell=True; no provider SDK; no auto-apply/approve/PR/git; no MemPalace/embeddings.
- Builder output ALWAYS untrusted. execution_satisfies_mission stays False.
- Do not claim merge-ready until reviewer PASS.

## Carried residual risks
- Pre-existing deselected test_project_brain.py::TestFileProvenanceChain::test_full_chain_order.
- Pre-existing test_resource_safety reads stale .agent/context.md.

## Next block
Ruff/Mypy/Coverage Baseline v0 (only after reviewer PASS).
