# Plan

## Goal
Step 6.5: Workspace Materialization Hardening.

## Status
COMPLETE. All changes on feature/step6-workspace-runtime (PR #7).

## What Was Done
1. task_runner.py: _extract_proposed_changes() — section-aware extraction (Proposed Changes only)
2. task_runner.py: _sanitize_path_component() — neutralizes traversal, replaces unsafe chars, truncates
3. task_runner.py: materialize_task_output() — collision-safe naming, sanitized paths, uses helpers
4. Tests: 25 new tests in test_workspace.py; 1 updated (filename pattern)
5. Docs: README + architecture.md updated (naming rules, ordering, content extraction)

## Key Decisions
- _extract_proposed_changes: state machine over known section headers — simple, no parser framework
- Filename: {index:03d}_{safe_type}_{short_id}.txt — deterministic, collision-safe, readable
- _sanitize_path_component: re.sub non-[a-zA-Z0-9_-] → _, truncate 48, strip _, fallback "unknown"
- Ordering documented: annotate → materialize → save_job (materialize before persist)

## Branch
feature/step6-workspace-runtime (PR #7) — in-scope per PR Continuity Rule
