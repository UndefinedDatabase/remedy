# Plan

## Goal
Step 22: External Agent Loop Contract v1.

## Prior step
Step 21 + 21.1 + 21.2 delivered Project Constitution v1 with trust-report/timeline
integration and safety hygiene.

## Status
COMPLETE — 1039 tests pass.

## Steps
1. [x] Create packages/orchestration/agent_loop.py
   - AgentRole, AgentLoopStage, AgentLoopDecision enums
   - AgentAdapterSpec, AgentLoopState frozen dataclasses
   - default_agent_loop_state, derive_agent_loop_state, summarize_agent_loop_state
2. [x] Add remedy agent-loop CLI command (apps/cli/main.py)
   - Loads job + events, derives state, prints summary
   - Writes agent_loop_inspected run log event (structured fields only)
3. [x] Create tests/test_agent_loop.py (56 tests)
   - Models, derivation logic, summary output, CLI, redaction
4. [x] Update docs/architecture.md — Agent Loop Contract v1 section
5. [x] Update .agent files
6. [x] Run full suite (1039 pass)
7. [ ] Commit Step 22 changes
8. [ ] Push to feature/step21-project-constitution-v1

## Branch
feature/step21-project-constitution-v1
