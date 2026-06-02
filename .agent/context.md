# Context

## Active Branch
feature/steps-247-252-data-honest-contract

## Scope
Steps 359-366: Resume truth closure, no no-op resume claims.

## Completed
- R-12001 fixed: from_approval no longer fakes success via run_autorun(none)
- Checkpoint semantics truthful:
  - context_ready: inspectable, not resumable (resume_mode_not_implemented)
  - patch_intent_created: blocked (approval_pending)
  - approval_recorded: blocked (missing_patch_payload — no persist yet)
  - source_apply_proven: safe_to_resume=True (real test-runner resume)
  - tests_failed: blocked (resume_mode_not_implemented)
  - tests_passed: complete
  - stopped: blocked
- from_apply real resume: discovers test command, runs via subprocess, reports pass/fail
- Dry-run accurate: matches checkpoint safety, never says can_resume for unimplemented
- CLI: unimplemented modes print "blocked: resume_mode_not_implemented"
- UI: ResumeCard shows blocked state, no fake "Resume available"
- R-12001 regression tests: 2 tests prevent no-op resume claims

## Constraints
- UI remains read-only
- Resume only from source_apply_proven (from_apply → tests) in v1
- No from_approval resume until patch persistence
- No from_test_failure repair resume until implementation
- source_apply requires permission + approved intent

## Remaining Risks
- Only one resume mode implemented (from_apply → tests)
- Patch persistence needed for from_approval resume
- Repair resume needs separate implementation
- Background worker not implemented

## Recommended Next Block
Steps 367-374 — Builder Prompt Quality And Real-Ollama Hardening
Or: Steps 367-374 — Resume Expansion And Patch Persistence
