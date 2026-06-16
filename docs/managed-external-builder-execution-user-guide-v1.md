# Managed External Builder Execution v1 — User Guide

## What is this?

Managed Builder Execution lets Remedy launch an external builder (Claude Code, a generic CLI
tool, etc.) via a bounded subprocess. Every execution uses a pre-approved command template,
runs with `shell=False`, a sanitized environment, a hard timeout, and an output byte cap.

Builder output is **always untrusted** — it enters the External Builder Sandbox intake path
and goes through Trust Gate, Candidate Quality, review, and approval before anything is applied.

## Quick start

```bash
# 1. List available command templates
remedy execution template-list --json

# 2. Show template details
remedy execution template-show claude-code-repair-v0 --json

# 3. Approve an execution for a session
remedy execution approve <session_id> --template claude-code-repair-v0 --json

# 4. Run the managed execution
remedy execution run <session_id> --template claude-code-repair-v0 --json

# 5. Check result
remedy execution show <execution_id> --json

# 6. View debug bundle (operator only)
remedy execution debug-bundle <execution_id> --json

# 7. Check integrity
remedy execution integrity --json
```

## Safety model

| Protection | How |
|-----------|-----|
| No shell injection | `shell=False` always; argv list only |
| No env secrets | Only allowlisted env vars (PATH, HOME, etc.) |
| No unbounded runtime | Hard timeout (max 600s) |
| No output flood | Byte cap (256KB) |
| No arbitrary commands | Command template registry + validation |
| No auto-apply | Output goes through sandbox intake |
| No raw output leak | Private file; public surfaces get scrubbed ref |
| Operator gate | Approval required before any execution |
| Disabled by default | Templates and runner must be explicitly enabled |

## Command templates

Templates define the exact command shape. They are validated at save time for:
- No shell metacharacters in argv tokens
- No forbidden/destructive programs (rm, sudo, curl, etc.)
- No secrets in argv
- Timeout clamped to max 600s
- Output cap clamped to 256KB
- Placeholders limited to a bounded allowlist

Templates are disabled by default. Enable one only when you're ready to use it.

## What happens after execution?

1. Output is stored in a private file (0o600)
2. Session status updates to CANDIDATE_RECEIVED (or FAILED/TIMEOUT/BLOCKED)
3. If successful, feed output into sandbox intake:
   `remedy builder session-record-output <session_id> --artifact-ref <ref> --json`
4. Then run sandbox intake:
   `remedy builder session-intake <session_id> --json`
5. Continue through Trust Gate → Candidate Quality → review → approval

## What this does NOT do

- No arbitrary shell execution
- No provider SDK calls
- No auto-apply/approve/PR/git
- No secrets in subprocess env
- No raw output in public surfaces
