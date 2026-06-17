# Controlled Claude Code Operator Path v0

## What is this?

A step-by-step CLI path for operators to run Claude Code through Remedy's
bounded subprocess execution rails. Every step is explicit, every action
requires operator approval, and all output is treated as untrusted.

This is NOT automatic code repair, NOT auto-apply, and NOT provider SDK
integration. The operator launches, approves, and reviews every step.

## Prerequisites

- Claude Code binary on PATH (`claude --version`)
- Remedy CLI installed and configured
- A builder session with a request package

## Pre-flight check

```bash
# Check if Claude Code is ready to use with Remedy
remedy execution claude-doctor --json
```

This checks: binary on PATH, adapter exists and enabled, template exists and
enabled. Any blockers are listed with fix commands.

## Operator runbook

For a specific session, get the full step-by-step runbook:

```bash
remedy execution operator-runbook <session_id> --template claude-code-repair-v0 --json
```

Returns ordered steps with exact CLI commands and any blockers that must be
resolved first.

## Step-by-step walkthrough

### 1. Enable the Claude Code adapter

```bash
remedy builder adapter-enable claude-code-v0 --mode operator_launched --json
```

### 2. Enable the command template

```bash
remedy execution template-enable claude-code-repair-v0 --json
```

Templates ship disabled by default. Enabling runs safety validation
(no forbidden programs, no shell metacharacters, no raw markers).

### 3. Adjust template limits (optional)

```bash
# Set timeout to 5 minutes
remedy execution template-update claude-code-repair-v0 --timeout-seconds 300 --json

# Set output cap to 2MB
remedy execution template-update claude-code-repair-v0 --max-output-bytes 2097152 --json
```

### 4. Create a request package and session

```bash
# Create package from analysis context
remedy builder package-create <job_id> --json

# Create session bound to adapter
remedy builder session-create <package_id> --adapter claude-code-v0 --json
```

### 5. Approve the execution

```bash
remedy execution approve <session_id> --template claude-code-repair-v0 --json
```

Approval is scoped to this session, adapter, package, and template. It
expires and is bounded to max_runs.

### 6. Run the execution

```bash
remedy execution run <session_id> --template claude-code-repair-v0 --json
```

Placeholder values (`{goal_summary}`, `{session_id}`, `{job_id}`, etc.)
are auto-sourced from the session and its linked package. No manual
copy-paste required.

The subprocess runs with `shell=False`, sanitized env, hard timeout, and
output byte cap. Raw output is stored privately (0o600 permissions).

### 7. Review the result

```bash
# Show execution result (safe summary only)
remedy execution show <execution_id> --json

# Full debug bundle (operator only)
remedy execution debug-bundle <execution_id> --json
```

### 8. Record output and run intake

```bash
# Record output reference back to session
remedy builder session-record-output <session_id> --artifact-ref <ref> --json

# Run sandbox intake (trust gate, quality checks)
remedy builder session-intake <session_id> --json
```

## Safety guarantees

- `shell=False` always — no shell injection possible
- Forbidden programs blocked (rm, sudo, curl, etc.)
- Shell metacharacters blocked in argv tokens
- Output treated as untrusted — enters sandbox intake
- Approval is scoped and expiring
- Raw output never surfaces in public APIs
- Secret patterns redacted from all summaries

## Template management

```bash
# List all templates
remedy execution template-list --json

# Show template details
remedy execution template-show <template_id> --json

# Enable/disable
remedy execution template-enable <template_id> --json
remedy execution template-disable <template_id> --json

# Update limits
remedy execution template-update <template_id> --timeout-seconds 300 --json
```

## Disable after use

```bash
# Disable template when not in use
remedy execution template-disable claude-code-repair-v0 --json

# Disable adapter
remedy builder adapter-disable claude-code-v0 --json
```
