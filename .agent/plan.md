# Plan

## Goal
Step 13: Task Type Registry v1

## Status
IN PROGRESS

## Steps
1. [x] Merge PR #12, checkout main, create feature/step13-task-registry
2. [ ] Create packages/orchestration/task_registry.py
       - TaskTypeSpec dataclass (frozen)
       - _ROUTE_RULES: ordered keyword→(description, repo_route_template) list
       - get_task_type_spec(task_type) → TaskTypeSpec (resolved; unknown fallback)
       - is_known_task_type(task_type) → bool
       - iter_task_type_specs() → tuple[TaskTypeSpec, ...]
3. [ ] Refactor repo_applicator.py: _resolve_repo_path delegates to get_task_type_spec;
       remove _REPO_PATH_RULES + local _sanitize_path_component
4. [ ] Refactor patch_intent.py: _derive_target_path delegates to get_task_type_spec;
       remove _INTENT_RULES; keep local _sanitize_path_component for materialization
5. [ ] Add tests/test_task_registry.py (known specs, unknown fallback, registry parity)
6. [ ] Update test_patch_intent.py: replace TestKeywordSync table-sync tests with
       registry-backed routing parity tests; remove _INTENT_RULES / _REPO_PATH_RULES imports
7. [ ] Update docs/architecture.md: Task Type Registry v1 section
8. [ ] .agent/decisions.md, context.md
9. [ ] Run all tests, self-review, commit, push, open PR

## Branch
feature/step13-task-registry

## PR
(none yet)
