# Live Review — Steps 2126-2145: Managed Execution Approval Binding Closure

Reviewer: parallel reviewer (independent; owns verdict — builder self-report does not set verdict;
a builder `Done:` marker is NOT reviewer `Resolved`).
Scope (ALLOWED): approval binding closure (session existence gate, adapter spec safety, auto-bind
from session, execution classification, output-ref event); docs/tests.
Must NOT: real provider execution; provider SDK; direct repo mutation; auto-apply; auto-approval;
auto-PR/git; hidden browser; arbitrary shell; shell=True; raw transcript/candidate/prompt/log leaks;
secret/env token storage; hardcoded provider monopoly; MemPalace; embeddings/vector DB; UI redesign;
MCP; repo-wide logging refactor.
BINDING CLOSURE BLOCK — hardens approval binding from "advisory" to "enforced".
Hard invariants: ghost sessions blocked; adapter spec dict/dataclass safe; empty binding fields
auto-populate from real session; execution.run is not generic command execution; output-ref event
exists for replay provenance; Done ≠ Resolved; reviewer verdict beats self-report.
Timestamp: 2026-06-16

## Verdict (reviewer-owned)
PENDING — builder commit with all 5 fixes + 23 new tests incoming.
Targeted 119 + CLI 10 + catalog 18 passed. Full suite 6497 passed. Awaiting reviewer re-verdict.

## Prior block
Steps 2076-2125: PASS @ 1de56cf (R-0106..R-0110 all Resolved). 189 targeted tests passed.

## Uncommitted WIP summary (pre-scan only, no findings)
| File | What changed |
|------|-------------|
| packages/orchestration/managed_builder_execution.py | +44L: R-0111 session existence gate in run_managed_builder; R-0112 isinstance(spec,dict) guard in _validate_session_binding; R-0113 auto-bind package_id/adapter_id/adapter_kind from real session in approve_managed_execution; _validate_session_binding now returns session_not_found when session is None |
| apps/cli/command_catalog.py | +2L: R-0114 may_execute_commands=False on execution.run |
| .agent/live_review.md | builder overwrote (reviewer will re-own) |

## Findings — Steps 2126-2145

### R-0111 — Managed execution requires real BuilderSession (High, Done)
run_managed_builder blocks ghost sessions at step 1b (before approval check). Status BLOCKED,
reason "session_not_found". _validate_session_binding returns session_not_found code.
3 targeted tests: runner blocks ghost, runner passes real, validate returns session_not_found.
**Done: R-0111** — awaiting reviewer verdict.

### R-0112 — AdapterSpec dict/dataclass safety (Medium, Done)
isinstance(spec, dict) guard in _validate_session_binding. No .to_dict() crash on dict.
3 targeted tests: real session+adapter no crash, kind mismatch detected, disabled adapter detected.
**Done: R-0112** — awaiting reviewer verdict.

### R-0113 — Empty approval binding auto-bind from real session (Medium, Done)
approve_managed_execution auto-binds package_id/adapter_id/adapter_kind from real
BuilderSessionRecord + AdapterSpec when caller omits them. Explicit values not overridden.
3 targeted tests: auto-binds package_id, auto-binds adapter_id, explicit not overridden.
**Done: R-0113** — awaiting reviewer verdict.

### R-0114 — execution.run is not generic command execution (Medium, Done)
execution.run may_execute_commands=False in catalog. action_class=controlled_builder_execution.
2 targeted tests: may_execute_commands is False, no generic execution permission.
**Done: R-0114** — awaiting reviewer verdict.

### R-0115 — Output-ref event exists for replay (Medium, Done)
OUTPUT_REF_CREATED event kind added. Emitted after _save_raw_output in runner.
Integrity flags completed_missing_output_ref_event. Debug bundle includes output_ref_event_present.
6 targeted tests: run emits event, missing event flagged, full events clean, bundle field,
event in _ALL_EVENT_KINDS, no raw output in event.
**Done: R-0115** — awaiting reviewer verdict.

Next id: R-0116.

## Reviewer audit log
- Block opened for Steps 2126-2145 (Binding Closure). Prior block 2076-2125 PASS @ 1de56cf.
- Uncommitted WIP detected: +44L managed_builder_execution.py, +2L command_catalog.py.
- Pre-scan: no danger imports, no new modules, all imports already in committed code.
- Awaiting builder commit for full line-level review.
