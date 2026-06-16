# Plan — Steps 2113-2125: Managed Execution Approval Hardening Closure

## Goal
Close 5 reviewer findings (R-0106 through R-0110) from Steps 2076-2125 block.
Fix code + tests, prove green, request reviewer re-verdict.

## Core principle
Workers execute. Remedy governs. Approval scoped+expiring+bounded+auditable.
Done ≠ Resolved. Reviewer verdict beats builder self-report.

## Current Step
2113-2125 — all 5 fixes implemented; targeted 102 + CLI 10 green; full suite running.

## Steps
- [x] 2113: R-0106 — default 30min expiry; empty expires_at = expired; integrity flag
- [x] 2114: R-0107 — _validate_session_binding loads real session (graceful if absent)
- [x] 2115: R-0108 — used_count increments before subprocess (failed runs consume)
- [x] 2116: R-0109 — action_class → controlled_builder_execution
- [x] 2117: R-0110 — event sequence + output_ref integrity; binding_summary in debug bundle
- [x] 2118-2120: fix existing tests (test_clean_approval_passes, test_known_status_clean, test_exhausted_approval)
- [x] 2121-2123: closure tests (R-0106: 4, R-0107: 3, R-0108: 3, R-0109: 2, R-0110: 7)
- [x] 2124: targeted 102 + CLI 10 passed
- [ ] 2125: full suite + commit + handoff

## Hard rules
- No shell=True; no provider SDK; no auto-apply/approve/PR/git; no MemPalace/embeddings.
- Builder output ALWAYS untrusted. execution_satisfies_mission stays False.
- Tests via scripts/remedy_pytest.sh; full once. Do not claim merge-ready until reviewer PASS.

## Next block
TBD (only after reviewer PASS).
