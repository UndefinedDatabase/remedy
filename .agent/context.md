# Context

## Active Branch
feature/steps-2076-2125-managed-execution-approval-dogfood-observability-hardening-v1-1
(forked from clean main at 1970b7c after PR #76 merged Managed External Builder Execution v1).

## Scope
Steps 2113-2125: Review closure for R-0106/R-0107/R-0108/R-0109/R-0110.
All code fixes + 19 new/updated tests. Awaiting reviewer re-verdict.

## Findings closure summary
| Finding | Severity | Fix summary |
|---------|----------|-------------|
| R-0106 | Medium | DEFAULT_APPROVAL_EXPIRY_SECONDS=1800; empty expires_at → expired; integrity flag |
| R-0107 | High | _validate_session_binding loads real BuilderSessionRecord; graceful if absent |
| R-0108 | Medium | _increment_approval_used_count before subprocess.run; argv failure doesn't consume |
| R-0109 | Medium | action_class changed to controlled_builder_execution |
| R-0110 | Low | completed_missing_output_ref/started/completed event checks; binding_summary in bundle |

## Carried residual risks
- Real rollback RESTORE still NOT implemented (metadata-only).
- Real adapters NOT configured — all disabled by default, no secrets committed.
- Pre-existing deselected `test_project_brain.py::...::test_full_chain_order`.
- UI `npm run lint` pre-existing TS parser blocker.

## Resource safety (standing)
- No background pytest. Use `scripts/remedy_pytest.sh`; full suite once at block end.

## Status
Code + tests complete. Targeted 102 + CLI 10 passed. Awaiting full suite + commit.
