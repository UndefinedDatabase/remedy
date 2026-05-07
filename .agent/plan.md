# Plan

## Goal
Step 30.2: Patch Apply Proof Polish + Smoke Alignment

## Status
COMPLETE — ready to commit

## Completed
- [x] test_patch_apply.py: test_symlink_escape_blocked — tighten to `== "unsafe_path"` (exact)
- [x] patch_apply.py: add _escape_marker_line helper; escape proposed lines in _build_create_content and _build_modify_section
- [x] test_patch_apply.py: test_marker_injection_in_proposed_lines_is_neutralized — new test
- [x] scripts/remedy_smoke.sh: rm -rf TARGET_REPO before mkdir -p
- [x] scripts/remedy_smoke.sh: VIEW_PATH extraction uses awk sub() to avoid colon-truncation
- [x] scripts/remedy_smoke.sh: step 7 expanded to full apply lifecycle (before-approval/approve/apply/noop)
- [x] tests/test_remedy_smoke_script.py: test_view_path_uses_awk_sub — new test
- [x] tests/test_remedy_smoke_script.py: apply lifecycle text assertions (before-approval, after-approval, noop, rm-rf)
- [x] Full suite: 1664 passed

## Next
Commit, push, PR.
