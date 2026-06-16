# Plan — Steps 2076-2125: Managed Execution Approval + Dogfood Observability Hardening v1.1

## Goal
Harden managed execution approval model: expiry, caps, session/package/adapter/template binding,
approval validation function, extended events/debug bundle, CLI hardening, observability surfaces,
integrity checks, structured logging bridge. Turns safe prototype into operator-grade dogfood.

## Core principle
Workers execute. Remedy governs. Approval scoped+expiring+bounded+auditable. One approval cannot
authorize unlimited runs. Template kind must match adapter kind. Builder output untrusted.

## Current Step
2097-2110 — builder work complete; targeted 93 + full suite 6461 green; awaiting reviewer verdict.

## Steps
- [x] 2076: mainline closure (PR #76 → main 1970b7c; fresh branch) + reconcile
- [x] 2077: architecture note (v1.1 hardening doc)
- [x] 2078-2080: harden ExecutionApproval (9 new fields + ApprovalScope + from_dict)
- [x] 2081-2083: validate_execution_approval() (11 codes) + binding validation in runner
- [x] 2084-2086: 7 new event kinds + debug bundle hardening + repair item suggestion
- [x] 2087-2088: CLI hardening (approval-show, approval-validate, approval-list) + catalog + contract
- [x] 2089-2091: review bundle / progress / cockpit / feature planner hardening
- [x] 2092-2094: extended integrity checks (audit_approval_safety + 9 new detection codes)
- [x] 2095-2096: structured logging bridge (Python logging in _append_event)
- [x] 2097-2110: tests — targeted 93 passed (83 unit + 10 CLI); full suite 6461 passed
- [ ] 2111: final handoff
- [ ] 2112-2125: reserved for reviewer findings (R-0106+)

## Hard rules
- No shell=True; no provider SDK; no auto-apply/approve/PR/git; no MemPalace/embeddings.
- Builder output ALWAYS untrusted. execution_satisfies_mission stays False.
- Tests via scripts/remedy_pytest.sh; full once. Auto-merge on reviewer PASS.

## Next block
TBD (only after this block PASS).
