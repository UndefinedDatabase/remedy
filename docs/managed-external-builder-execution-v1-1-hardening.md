# Managed External Builder Execution v1.1 — Approval Hardening

## What changed (v1 → v1.1)

v1 introduced managed execution with a simple approval model: session_id + template_id, no expiry,
no caps, no binding to adapter or package. v1.1 hardens this into an operator-grade approval model
with scoped, expiring, bounded, auditable approvals.

## Approval model hardening

### New fields on ExecutionApproval

| Field | Type | Purpose |
|-------|------|---------|
| package_id | str | Bind approval to a specific request package |
| adapter_id | str | Bind approval to a specific adapter registration |
| adapter_kind | str | Must match template.adapter_kind |
| expires_at | str | ISO timestamp; approval rejected after this time |
| max_runs | int | Max number of executions this approval authorizes (0 = unlimited) |
| used_count | int | How many times this approval has been consumed |
| max_runtime_seconds | int | Per-run runtime cap (clamped to MAX_TIMEOUT_SECONDS) |
| max_output_bytes | int | Per-run output cap (clamped to MAX_OUTPUT_BYTES) |
| approval_scope | str | One of: single_run, session_lifetime, time_bounded |

### Approval validation (11 codes)

`validate_execution_approval()` returns a list of validation codes:

| Code | Meaning |
|------|---------|
| approval_not_found | No approval exists for this session |
| approval_expired | Current time > expires_at |
| approval_exhausted | used_count >= max_runs (when max_runs > 0) |
| template_mismatch | approval.template_id != requested template_id |
| adapter_kind_mismatch | approval.adapter_kind != template.adapter_kind |
| session_mismatch | approval.session_id != requested session_id |
| package_mismatch | approval.package_id set but != requested package_id |
| adapter_mismatch | approval.adapter_id set but != requested adapter_id |
| runtime_exceeds_cap | template timeout > approval.max_runtime_seconds |
| output_exceeds_cap | template max_output > approval.max_output_bytes |
| scope_violation | single_run approval already used |

### Approval lifecycle

1. Operator calls `remedy execution approve` with binding fields
2. `validate_execution_approval()` checks all 11 codes before run
3. On successful run, `used_count` increments
4. Expired/exhausted approvals block further runs
5. Debug bundle shows full approval validation summary

## New event kinds (v1.1)

| Kind | When |
|------|------|
| approval_expired | Run rejected due to expired approval |
| approval_exhausted | Run rejected due to max_runs exceeded |
| approval_validated | Approval passed all 11 checks |
| binding_mismatch | Adapter/package/session binding failed |
| approval_consumed | used_count incremented after successful run |
| runtime_cap_applied | Approval runtime cap applied (lower than template) |
| output_cap_applied | Approval output cap applied (lower than template) |

## Safety invariants (unchanged from v1)

- shell=False ALWAYS
- Sanitized env (allowlisted keys only)
- Hard timeout (max 600s)
- Output byte cap (256KB)
- Builder output ALWAYS untrusted
- execution_satisfies_mission stays hardcoded False
- No auto-apply / auto-approve / auto-PR / auto-git

## Debug bundle hardening

The debug bundle now includes:
- Full approval validation summary (all 11 codes checked, pass/fail per code)
- Approval binding details (which fields matched, which didn't)
- Cap enforcement details (runtime/output caps from approval vs template)
- Repair item suggestion when blocked by approval issues

## Integrity extension

11+ new detection codes for approval-related violations:
- Expired approvals still referenced by active executions
- Exhausted approvals with used_count > max_runs
- Adapter kind mismatches between approvals and templates
- Missing binding fields on approvals for bound templates
- Approval scope violations
