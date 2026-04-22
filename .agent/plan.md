# Plan

## Goal
Step 5.7: Planner CLI Parity Hotfix.

## Status
IN PROGRESS — Commit 1/2

## Commits Planned
1. [ ] Fix planner CLI: move OllamaPlanner() inside try/except; add ValueError + parity error labels
2. [ ] Builder system prompt: require ≥1 proposed_changes explicitly; tests

## Key Decisions
- Same pattern as Step 5.6 fix for builder: construction must be inside try block
- Planner path adds ValueError case (matches builder path) plus parity import label
- Builder prompt: add "at least one item required" note to proposed_changes rule
- Step 5.7 continues on feature/step5-task-execution (PR #6) — same feature boundary

## Branch
feature/step5-task-execution (PR #6) — in-scope per PR Continuity Rule
