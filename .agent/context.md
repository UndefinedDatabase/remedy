# Context

## Active Branch
feature/steps-247-252-data-honest-contract

## Scope
Steps 367-374: Resume execution quality, test_runner integration, dry-run truth.

## Completed
- Ad-hoc subprocess resume replaced with execute_resume_from_apply() using run_tests_local
- Capability-aware dry-run: validates permission, repo path, test candidate before can_resume=True
- Resume events: resume_started, resume_test_started, resume_test_completed, resume_completed
- Test metadata: test_run_id, output_truncated, persisted_output_bytes, command_source_type
- Checkpoint data contract: required_data, missing_data, resume_mode_supported, inspectable, dry_run_available
- CLI calls orchestration helper, renders safe export_resume_result_json
- Resume docs (docs/resume.md): what replay/checkpoints are, supported/blocked modes, commands
- 27 replay/checkpoint tests, 35 Vitest, TypeScript clean, build OK

## Constraints
- UI remains read-only
- Resume only from source_apply_proven (from_apply → tests) in v1
- No from_approval resume until patch persistence
- No from_test_failure repair resume until implementation
- source_apply requires permission + approved intent

## Remaining Risks
- from_approval blocked until structured patch payload persistence
- Repair resume blocked until implementation
- Background worker not implemented

## Recommended Next Block
Steps 375-382 — Builder Prompt Quality And Real-Ollama Hardening
