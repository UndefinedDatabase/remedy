# Context

## Active Branch
feature/steps-2076-2125-managed-execution-approval-dogfood-observability-hardening-v1-1
(forked from clean main at 1970b7c after PR #76 merged Managed External Builder Execution v1).

## Scope
Steps 2126-2145: Review closure for R-0111/R-0112/R-0113/R-0114/R-0115.
All code fixes + 23 new tests + existing test updates. Awaiting reviewer re-verdict.

## Findings closure summary
| Finding | Severity | Fix summary |
|---------|----------|-------------|
| R-0111 | High | Runner blocks ghost sessions; _validate_session_binding returns session_not_found |
| R-0112 | Medium | isinstance check on adapter spec; no .to_dict() crash on dict |
| R-0113 | Medium | approve_managed_execution auto-binds package_id/adapter_id/adapter_kind from real session |
| R-0114 | Medium | execution.run may_execute_commands=False; controlled_builder_execution action_class only |
| R-0115 | Medium | OUTPUT_REF_CREATED event; integrity checks completed_missing_output_ref_event; debug bundle output_ref_event_present |

## Carried residual risks
- Real rollback RESTORE still NOT implemented (metadata-only).
- Real adapters NOT configured — all disabled by default, no secrets committed.
- Pre-existing deselected `test_project_brain.py::...::test_full_chain_order`.
- UI `npm run lint` pre-existing TS parser blocker.

## Status
Code + tests complete. Full suite 6497 passed. Awaiting commit + reviewer verdict.
