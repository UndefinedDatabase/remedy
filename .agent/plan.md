# Plan

## Goal
Step 23.1: Project Brain polish — visual legend, constitution dedupe, robust cycle parsing, --json export.

## Prior step
Step 23: Project Brain Graph v1 (read-only graph model/export, 60 tests).

## Status
COMPLETE — 1131 tests pass.

## Steps
1. [x] Add visual status legend section to summarize_project_brain
   - "pending nodes: grey", "running nodes: pulsing", "completed nodes: white"
   - "blocked nodes: red", "needs approval: amber"
   - "memory layer: violet", "mcp quarantine: orange"
   - Labelled "Visual status legend (Step 24+)" — no frontend exists
2. [x] Remove project_constitution_loaded from _KEY_EVENTS
   - Prevents duplicate run_event node alongside the dedicated constitution node
   - constitution node behavior unchanged (from object or event)
3. [x] Add _safe_int helper; replace int(...) in agent_loop cycle parsing
   - "2" → 2, "not-a-number" → 0, None → 0, missing → 0
   - No exception escapes build_project_brain
4. [x] Add remedy brain <job_id> --json CLI flag
   - Prints export_project_brain_json with sort_keys=True
   - project_brain_inspected logged with same exact schema either way
5. [x] Update tests (80 total in test_project_brain.py)
   - TestVisualLegend: 8 tests (one per legend entry)
   - TestSafeCycleParsing: 7 tests
   - constitution dedupe test added
   - --json CLI tests added (4 tests)
6. [x] Update docs/architecture.md
7. [x] Run full suite (1131 pass)
8. [ ] Commit Step 23.1 changes
9. [ ] Push to feature/step21-project-constitution-v1

## Branch
feature/step21-project-constitution-v1
