# Plan

## Goal
Step 24.1: Brain CLI JSON + Detail Smoke Hardening.

## Prior step
Step 24: Brain Node Detail v1 (1183 tests).

## Status
COMPLETE — 1217 tests pass.

## Steps
1. [x] Create tests/test_brain_smoke.py (34 tests)
   - TestBrainLifecycle (8): before planning, after planning, after run, after approval
   - TestBrainNodeJsonAllTypes (12): one brain-node --json test per node type
   - TestBrainJsonRegression (6): no human header in --json, empty stderr, no traceback
   - TestBrainRunLogSchema (4): exact keys for project_brain_inspected and brain_node_inspected
   - TestBrainRedactionHardening (4): all 5 sentinels absent from brain/brain-node JSON and run logs
2. [x] Update docs/architecture.md — Brain CLI JSON Contract v1 (Step 24.1) section
   - brain --json canonical machine contract for future 2D/3D graph
   - brain-node --json canonical machine contract for future click-detail panels
   - Future frontend priority: 2D graph → 3D/Animus → MemPalace → MCP
   - JSON stdout must be pure JSON; human text only in non-json mode
3. [x] Update .agent files
4. [x] Run full suite (1217 pass)
5. [ ] Commit Step 24.1 changes
6. [ ] Push to feature/step21-project-constitution-v1

## Branch
feature/step21-project-constitution-v1
