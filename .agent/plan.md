# Plan

## Goal
Step 30.3: Apply Proof E2E Closure

## Status
COMPLETE — ready to commit

## Completed
- [x] test_patch_apply.py: test_marker_injection_in_create_file_is_neutralized — exercises _build_create_content
- [x] scripts/remedy_smoke.sh: RUNS_ROOT resolution (REMEDY_DATA_DIR or packages import fallback)
- [x] scripts/remedy_smoke.sh: step 7e — exact patch_intent_applied run-log schema check (blocked/applied/noop outcomes + exact metadata keys)
- [x] scripts/remedy_smoke.sh: step 11 — assert patch_apply brain node present when FIRST_INTENT_ID set
- [x] tests/test_remedy_smoke_script.py: 5 new text assertions (brain patch_apply, run-log schema, outcomes, RUNS_ROOT)
- [x] docs/architecture.md: Step 30.3 E2E apply proof smoke note + marker injection defense note
- [x] Full suite: 1669 passed (1664 → 1669)

## Next
Commit, push, PR.
