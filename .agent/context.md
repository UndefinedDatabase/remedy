# Context

## Active Branch
`feature/step13-task-registry`

## PR
(none yet)

## Scope
Step 13: Task Type Registry v1.
- New: packages/orchestration/task_registry.py (TaskTypeSpec, get_task_type_spec, is_known_task_type, iter_task_type_specs)
- Refactored: repo_applicator._resolve_repo_path → delegates to registry
- Refactored: patch_intent._derive_target_path → delegates to registry
- Removed: _REPO_PATH_RULES (repo_applicator), _INTENT_RULES (patch_intent)
- Removed: _sanitize_path_component from repo_applicator (no longer needed)
- Updated: TestKeywordSync → registry-backed routing parity tests
- New: tests/test_task_registry.py (59 tests)
- Updated: docs/architecture.md (new Task Type Registry section)
No behavior changes; 455 tests pass.

## Key decisions
- task_type is NOT an enum; LLM-generated types remain valid
- Unknown fallback: repo_route=None, capabilities={"unknown_task_type"} — conservative
- repo_route in returned TaskTypeSpec is always fully resolved (no {safe_type})
- keyword-backed matching internally (v1) — same semantics as removed tables
