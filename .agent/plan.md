# Plan

## Goal
Step 5.6: CLI Hotfix and Final Pre-Step-6 Hardening.

## Status
IN PROGRESS — Commit 1/3

## Commits Planned
1. [ ] Fix CLI: move OllamaBuilder() inside try/except in run-next-task-local
2. [ ] Fix annotate_planning_result: raise RuntimeError if changed=True but no artifact
3. [ ] Fix BuilderOutput: require proposed_changes to have at least 1 item; tests

## Key Decisions
- OllamaBuilder() construction raises ValueError on bad env vars; must be inside try block
- annotate_planning_result no-op on changed=False is correct; raise on changed=True missing artifact
- proposed_changes min_length=1: empty list is not a valid builder response
- Step 5.6 continues on feature/step5-task-execution (PR #6) — same feature boundary

## Branch
feature/step5-task-execution (PR #6) — in-scope per PR Continuity Rule
