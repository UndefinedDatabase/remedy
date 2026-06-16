# Plan — Steps 2126-2145: Managed Execution Approval Binding Closure

## Goal
Close 5 reviewer findings (R-0111 through R-0115) from Steps 2076-2125 block.
Session-required runner, dict-safe adapter spec, auto-binding, controlled execution class,
output-ref-created event.

## Core principle
Workers execute. Remedy governs. Approval scoped+expiring+bounded+auditable.
Done ≠ Resolved. Reviewer verdict beats builder self-report.

## Current Step
2126-2145 — all 5 fixes implemented; targeted 119 + CLI 10 + catalog 18 green; full suite 6497.

## Steps
- [x] 2126: R-0111 — runner blocks ghost sessions; _validate_session_binding returns session_not_found
- [x] 2127: R-0112 — spec dict handling (isinstance check, no .to_dict() crash)
- [x] 2128: R-0113 — approve_managed_execution auto-binds package_id/adapter_id/adapter_kind from session
- [x] 2129: R-0114 — execution.run may_execute_commands=False; controlled_builder_execution only
- [x] 2130: R-0115 — OUTPUT_REF_CREATED event kind; emit after _save_raw_output; integrity check
- [x] 2131-2140: fix all existing tests (add _create_test_session helper); add 23 closure tests
- [x] 2141: targeted 119 + CLI 10 + catalog 18 passed; full suite 6497 passed (0 failed)
- [ ] 2142: commit + push
- [ ] 2143-2145: reserved for reviewer findings (R-0116+)

## Hard rules
- No shell=True; no provider SDK; no auto-apply/approve/PR/git; no MemPalace/embeddings.
- Builder output ALWAYS untrusted. execution_satisfies_mission stays False.
- Do not claim merge-ready until reviewer PASS.

## Next block
Dogfood Run Profile + Replay Analyzer v0 (only after reviewer PASS).
