# Plan

## Goal
Step 22.1: Agent Loop stale blocker fix + run-log/redaction hardening.

## Prior step
Step 22 introduced the Agent Loop Contract (models, derive, summarize, CLI).

## Status
COMPLETE — 1051 tests pass.

## Steps
1. [x] Fix stale blocker: derive_agent_loop_state reflects current state, not history
   - _find_current_blocker: check 1 = explicit deny override; check 2 = unresolved event
   - Historical perm_denied ignored when task completed or no pending tasks remain
2. [x] Specific blocked_reason: "permission_denied:workspace_write" format
3. [x] Next action uses concrete capability name in set-permission hint
4. [x] blockers display: "permission_denied (workspace_write)"
5. [x] Fix: default-deny capabilities (repo_generated_write) do NOT trigger check 1
6. [x] agent_loop_inspected metadata schema hardening (exact keyset test)
7. [x] Redaction hardening (5 sentinel tests)
8. [x] Update test file: stale comment, updated/new tests
9. [x] Update docs/architecture.md — stale-event policy, blocked_reason format, schema
10. [x] Update .agent files
11. [x] Run full suite (1051 pass)
12. [ ] Commit Step 22.1 changes
13. [ ] Push to feature/step21-project-constitution-v1

## Branch
feature/step21-project-constitution-v1
