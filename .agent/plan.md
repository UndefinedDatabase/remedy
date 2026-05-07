# Plan

## Goal
Step 30.1: Patch Apply Proof Hardening

## Status
COMPLETE — ready to commit

## Completed
- [x] patch_apply.py: remove dead .md check after _validate_target_path (clarified comment)
- [x] test_patch_apply.py: test_run_log_exact_metadata_keys → exact set equality (no extra keys)
- [x] test_patch_apply.py: test_symlink_escape_blocked — real symlink pointing outside repo
- [x] test_patch_apply.py: test_brain_node_detail_no_patch_content — extended to cover all sentinels
- [x] docs/architecture.md: Proof-chain model note (Step 30.1)
- [x] Full suite: 1658 passed

## Next
Commit, push, PR.
