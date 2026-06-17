# Execution Approval Policy v0

## Purpose

An operator-configured policy layer that can grant bounded execution approval
metadata for known worker/template/task combinations. Policy approval is
**disabled by default** and creates **metadata only** — it never executes
anything, applies code, creates PRs, or marks missions done.

## Architecture

```
Operator ──► CLI (remedy approval policy-enable) ──► Policy storage (JSON)
                                                         │
Mission loop (WAITING_FOR_APPROVAL) ──► _try_policy_grant()
                                           │
                                           ├─ evaluate policies (read-only)
                                           │
                                           └─ if allowed: approve_managed_execution()
                                              (creates ExecutionApproval metadata)
```

### Key invariants

1. **Disabled by default.** All default policies ship disabled.
2. **Metadata only.** Policy grant creates an ExecutionApproval record.
   It never runs a subprocess, applies a diff, creates a PR, or mutates
   the repo.
3. **Bounded.** Each policy has caps: max_timeout_seconds (≤600),
   max_output_bytes (≤256KB), max_estimated_tokens (≤500K), max_uses.
4. **Operator-scoped.** Policies are tied to specific adapter_id,
   template_id, adapter_kind, template_kind, and allowed_task_types.
5. **Auditable.** Every grant includes operator_id (prefixed "policy:"),
   reason, and timestamps.
6. **Revocable.** `remedy approval policy-disable <id>` disables instantly.
7. **Real provider requires explicit confirmation.**
   `--confirm-real-provider` flag needed for non-fixture policies.

## Default policies

| Policy ID             | Type     | Default | Notes                  |
|-----------------------|----------|---------|------------------------|
| fixture-echo-v0       | fixture  | disabled | Deterministic test only |
| claude-code-repair-v0 | real     | disabled | Requires confirmation   |
| generic-cli-v0        | real     | disabled | Requires confirmation   |

## CLI commands

All under the `approval` group:

| Command                          | Action class    | Description                |
|----------------------------------|-----------------|----------------------------|
| `approval policy-list`           | read_only       | List all policies          |
| `approval policy-show <id>`      | read_only       | Show policy details        |
| `approval policy-enable <id>`    | write_metadata  | Enable a policy            |
| `approval policy-disable <id>`   | write_metadata  | Disable a policy           |
| `approval policy-evaluate <sid>` | read_only       | Dry-run evaluate           |
| `approval policy-grant <sid>`    | write_metadata  | Evaluate and grant if ok   |

## Policy evaluation flow

1. Load template → check enabled → load session → get adapter
2. Find enabled policies matching adapter/template/kind
3. For each matching policy, check:
   - adapter_id/adapter_kind match
   - template_id/template_kind match
   - task_type in allowed_task_types
   - timeout ≤ max_timeout_seconds
   - output ≤ max_output_bytes
   - not expired
   - uses_consumed < max_uses
   - real_provider allowed if needed
   - fixture_only constraints
4. First matching policy wins. Return decision with specific denial code.

## Mission loop integration

At `WAITING_FOR_APPROVAL`, `_try_policy_grant()` parses session_id and
template_id from `next_suggested_action`, evaluates policies, and if
allowed, creates approval metadata. The run status transitions to RUNNING
and the loop continues. If denied, the loop stops with
`waiting_for_approval`.

## Morning report fields

- `policy_considered`: whether enabled policies exist
- `policy_decision_code`: evaluation result code
- `policy_granted_approval`: whether grant succeeded
- `policy_id`: matched policy ID
- `manual_approval_required`: always true by default
- `policy_reason`: human-readable reason

## Safety constraints

- Policy approval may only create bounded approval metadata
- Policy approval must never execute anything by itself
- No shell=True, no subprocess launch, no provider SDK calls
- Secret-like values (sk-, api_key=, password=) rejected at save time
- Private paths (/home/, /root/, /Users/) rejected at save time
- Caps are clamped to hardcoded maximums
