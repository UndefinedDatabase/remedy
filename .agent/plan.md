# Plan — Steps 5055-5072: Recovery and Verification Block

## Goal
Snapshot, classify, and commit valid E2E hardening changes from dogfood job
`0d34577b353e4109`. Fix staging noise filtering that blocked observability v2
workspace apply. Verify review ZIP includes uncommitted files.

## Current Step
Step 5059: Implement staging noise filtering in `_find_staging_changes`.

## Classification (Step 5057)
- E2E hardening changes (do_cmd, command_catalog, tests): **VALID_CONTINUE**
  - Coherent, complete, from successful dogfood with 2/2 tasks passed
  - Safe-stop messaging, improved description, 8 E2E tests
- V2 observability features (token_summary, _build_next_approve_command,
  _claude_cli_timeout_hint, final_audit): **ABSENT**
  - Exist only in blocked workspace `staging_c85f2f26f6df430a`
  - Block constraint prohibits manual rescue of blocked workspace files
  - Will require separate block to implement from scratch

## Steps
- [x] 5055: Snapshot repo state (HEAD=dc000fa, 4 modified, 1 untracked)
- [x] 5056: Search for v2 features — none in working tree
- [x] 5057: Classification — VALID_CONTINUE for E2E hardening, ABSENT for v2
- [ ] 5058: No v2 pieces to complete (absent, rescue prohibited)
- [ ] 5059: Fix staging noise in `_find_staging_changes` (pingpong_loop.py)
- [ ] 5060: Verify review ZIP handles uncommitted files
- [ ] 5061-5063: Add staging noise tests, verify existing tests
- [ ] 5064: Run targeted checks
- [ ] 5065: Smoke test
- [ ] 5066: Create review ZIP
- [ ] 5067: Commit (2 commits: E2E hardening, then staging noise fix)
- [ ] 5070: Handoff

## Risks
- Pre-existing failure: test_full_chain_order in test_project_brain.py (not ours)
