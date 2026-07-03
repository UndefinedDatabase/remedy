# Managed External Builder Execution v1 + Dogfood Observability

## Overview

The first managed execution seam for external builder adapters. Remedy can now launch a
builder session via a bounded subprocess — but only through a pre-approved command template,
with a sanitized environment, hard timeout, output byte cap, and mandatory sandbox intake.

**Workers execute. Remedy governs.**

## Architecture

```
                 ┌──────────────────────────────────────┐
                 │        Main Builder Adapter v0        │
                 │  (registry, request packages, sessions)│
                 └──────────────┬───────────────────────┘
                                │ session_id + adapter_id
                                ▼
                 ┌──────────────────────────────────────┐
                 │   Managed Builder Execution v1        │
                 │                                       │
                 │  ┌─────────────────────────────────┐  │
                 │  │ Command Template Registry       │  │
                 │  │ (bounded, no shell, no secrets)  │  │
                 │  └──────────┬──────────────────────┘  │
                 │             │ resolve template         │
                 │  ┌──────────▼──────────────────────┐  │
                 │  │ Operator Approval Gate           │  │
                 │  │ (approval_required by default)   │  │
                 │  └──────────┬──────────────────────┘  │
                 │             │ approved                 │
                 │  ┌──────────▼──────────────────────┐  │
                 │  │ Managed Runner                   │  │
                 │  │ subprocess.run(argv, shell=False) │  │
                 │  │ sanitized env, timeout, cap      │  │
                 │  └──────────┬──────────────────────┘  │
                 │             │ output_ref (redacted)    │
                 │  ┌──────────▼──────────────────────┐  │
                 │  │ Event Ledger + Debug Bundle      │  │
                 │  │ (replay, timing, safe summaries)  │  │
                 │  └──────────┬──────────────────────┘  │
                 └─────────────┼────────────────────────┘
                               ▼
                 ┌──────────────────────────────────────┐
                 │   External Builder Sandbox v0         │
                 │   (quarantine → Trust Gate → verify)  │
                 └──────────────────────────────────────┘
```

## Command Templates

A command template defines the exact argv pattern for launching a builder:

- **template_id**: unique identifier (e.g., `claude-code-repair-v0`)
- **adapter_kind**: which adapter this template serves
- **argv_template**: list of argv tokens with `{placeholders}` for safe substitution
- **allowed_placeholders**: which `{...}` keys may appear (bounded set)
- **sanitized_env_keys**: allowlist of env vars passed to subprocess (e.g., `PATH`, `HOME`)
- **timeout_seconds**: hard cap (default 300s, max 600s)
- **max_output_bytes**: output cap (default 256KB)
- **requires_approval**: whether operator must approve before launch (default True)
- **enabled**: whether this template is active (default False)

Templates are validated at save time:
- No shell metacharacters in argv tokens
- No forbidden/destructive programs
- No secrets in argv or env
- No absolute paths that leak private dirs
- Placeholder count bounded

## Operator Approval Gate

Before any managed execution:
1. Template must exist and be enabled
2. Adapter must be enabled
3. Session must be in WAITING_FOR_OPERATOR or PACKAGE_READY
4. If `requires_approval=True`, operator must explicitly approve

Approval creates a durable record with timestamp, template_id, and session_id.
No auto-approval. No bypass.

## Managed Runner

The single managed execution function:
- Takes a resolved command template + placeholder values
- Builds argv list from template (no shell=True, ever)
- Filters env to allowlisted keys only
- Runs `subprocess.run(argv, shell=False, timeout=..., capture_output=True, env=sanitized_env)`
- Caps stdout/stderr to max_output_bytes
- Records exit code, duration, output_ref (never raw output in public surfaces)
- On timeout: records TIMEOUT status, kills process
- On error: records ERROR status with safe summary
- Output goes to private file (0o600), public surfaces get redacted ref only

**Hard invariants:**
- `shell=False` always
- No secrets/tokens in env (allowlisted keys only)
- No network passthrough (no proxy/API key env vars)
- Process killed on timeout
- Output never appears raw in public surfaces

## Event Ledger

Each managed execution creates events:
- `execution_requested`: template resolved, approval checked
- `execution_approved`: operator approval recorded
- `execution_started`: subprocess launched
- `execution_completed`: exit code, duration, output_ref
- `execution_failed`: error reason, safe summary
- `execution_timeout`: timeout reached
- `intake_started`: sandbox intake initiated
- `intake_completed`: sandbox submission recorded

Events are append-only, timestamped, and carry safe summaries (no raw content).

## Dogfood Debug Bundle

A structured debug bundle for each managed execution:
- Command template used (with placeholder values redacted of secrets)
- Timing (start, end, duration_ms)
- Exit code
- Output summary (first/last N chars, scrubbed)
- Session status transitions
- Event timeline
- Intake result (if sandbox intake completed)

Bundle is private (0o600) — for operator debugging, not public export.

## Integration Points

- **Session lifecycle**: execution updates session status (RUNNING → CANDIDATE_RECEIVED or BLOCKED)
- **Sandbox intake**: successful output goes through existing `intake_provider_repair` path
- **Repair Loop**: session status consumed by repair evaluation
- **Mission Contract**: active/blocked sessions affect mission evidence
- **Progress Ledger**: execution events surface as progress items
- **Review Bundle**: execution summary in bundle (safe counts/status only)
- **Cockpit**: execution status shown (read-only, live=bool(running))
- **Integrity**: checks for shell=True, unconstrained subprocess, secrets in env, etc.

## Safety Model

| Concern | Mitigation |
|---------|-----------|
| Shell injection | shell=False always; argv list only |
| Env secrets leak | Allowlisted env keys only |
| Unbounded runtime | Hard timeout (max 600s) |
| Output flood | Byte cap (default 256KB) |
| Arbitrary commands | Template registry; forbidden tokens check |
| Auto-apply | Never; output goes through sandbox intake |
| Raw output leak | Private file; public surfaces get scrubbed ref |
| Uncontrolled execution | Operator approval required by default |
| Managed runner always on | Disabled by default; explicit enable required |

## CLI Commands (8)

| Command | Action class | Description |
|---------|-------------|-------------|
| `execution.template-list` | read_only | List command templates |
| `execution.template-show` | read_only | Show template details |
| `execution.template-create` | write_metadata | Create/update command template |
| `execution.approve` | approval_gate | Approve a managed execution |
| `execution.run` | test_execution | Run managed builder execution |
| `execution.show` | read_only | Show execution result |
| `execution.list` | read_only | List executions for a session/job |
| `execution.debug-bundle` | read_only | Show dogfood debug bundle |

## What This Does NOT Do

- No arbitrary shell execution (shell=True forbidden)
- No unconstrained subprocess (template-bounded only)
- No provider SDK calls (adapter-agnostic)
- No auto-apply/approve/PR/git
- No secrets in subprocess env
- No raw output in public surfaces
- No MemPalace/memory/embeddings
- No UI changes
