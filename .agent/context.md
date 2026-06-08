# Context

## Active Branch
feature/steps-850-864-tooling-provenance

## Scope
Steps 825-849 (Proof Chain Truth Closure + Timing Closure) are verified complete on this branch.
Steps 850-864 (file provenance hotfix + agent tooling) are committed and reviewed.

## Prior Step Status
Steps 810-824: PASS — Proof Chain v1 shipped.
Steps 825-839: PASS — False verified fix, structured NextSafeAction, redaction hardening, linked test evidence.
Steps 840-849: PASS — After-apply timing enforcement, change_set safe association, missing link reasons.
Steps 850-864: PASS WITH RISKS — File provenance linked-test filtering, Pi/Claude/MCP tooling config.

## Proof Chain Truth Status
- `verified` requires: approved + applied + apply_event + proof + (linked passed test OR explicit not_required).
- Test absence is never verified.
- Generic sole-change tests require after-apply timestamp ordering.
- Multi-change generic tests never verify individual changes.
- change_set uses `_link_test_to_change()` — no global latest test association.
- file_provenance catches (KeyError, ValueError, TypeError), not broad Exception.
- NextSafeAction is structured with catalog validation.

## Resource Safety
Use `scripts/remedy_pytest.sh`; no direct pytest, no background pytest, no `shell=True`.
No secrets, `.env`, `.data`, raw artifacts/stdout/diffs/source content in summaries.
Reviewer findings beat worker self-report.

## Constraints
Read-only proof chain output only. No raw diffs, content, secrets, stdout/stderr, command output, tracebacks, or approval reasons.
