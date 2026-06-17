# Controlled Claude Code Operator Path v0

## Simple path (recommended)

Most operators should use these commands:

```bash
# 1. Check readiness
remedy worker doctor claude --json

# 2. Set up the worker
remedy worker add claude --json

# 3. Run a bounded mission loop
remedy mission run <run_id> --job-id <job_id> --json

# 4. Approve execution when prompted
remedy execution approve <session_id> --template claude-code-repair-v0 --json

# 5. Read the morning report
remedy mission report <run_id> --job-id <job_id> --json
```

See `docs/simple-operator-quickstart-v0.md` for full details.

## What is this?

A CLI path for operators to run Claude Code through Remedy's bounded
subprocess execution rails. Every step is explicit, every action
requires operator approval, and all output is treated as untrusted.

This is NOT automatic code repair, NOT auto-apply, and NOT provider SDK
integration. The operator launches, approves, and reviews every step.

## Safety guarantees

- `shell=False` always — no shell injection possible
- Forbidden programs blocked (rm, sudo, curl, etc.)
- Shell metacharacters blocked in argv tokens
- Output treated as untrusted — enters sandbox intake
- Approval is scoped and expiring
- Raw output never surfaces in public APIs
- Secret patterns redacted from all summaries

## Advanced / internal rails

The commands below are for debugging, advanced template management,
and direct session control. Most operators do not need these.

### Pre-flight check

```bash
remedy execution claude-doctor --json
```

Checks: binary on PATH, adapter exists and enabled, template exists and
enabled. Any blockers are listed with fix commands.

### Operator runbook

```bash
remedy execution operator-runbook <session_id> --template claude-code-repair-v0 --json
```

Returns ordered steps with exact CLI commands and any blockers.

### Direct adapter management

```bash
# Enable adapter with specific mode
remedy builder adapter-enable claude-code-v0 --mode operator_launched --json

# Show adapter state
remedy builder adapter-show claude-code-v0 --json

# List all adapters
remedy builder adapter-list --json
```

### Direct template management

```bash
# Enable a template (safety-validated)
remedy execution template-enable claude-code-repair-v0 --json

# Disable a template
remedy execution template-disable claude-code-repair-v0 --json

# Set timeout to 5 minutes
remedy execution template-update claude-code-repair-v0 --timeout-seconds 300 --json

# Set output cap to 128KB
remedy execution template-update claude-code-repair-v0 --max-output-bytes 131072 --json

# Show template details
remedy execution template-show claude-code-repair-v0 --json

# List all templates
remedy execution template-list --json
```

### Direct session and execution control

```bash
# Create package from analysis context
remedy builder package-create <job_id> --json

# Create session bound to adapter
remedy builder session-create <package_id> --adapter-id claude-code-v0 --json

# Approve the execution
remedy execution approve <session_id> --template claude-code-repair-v0 --json

# Run the execution
remedy execution run <session_id> --template claude-code-repair-v0 --json

# Show execution result (safe summary only)
remedy execution show <execution_id> --json

# Full debug bundle (operator only)
remedy execution debug-bundle <execution_id> --json

# Record output reference back to session
remedy builder session-record-output <session_id> --artifact-ref <ref> --json

# Run sandbox intake (trust gate, quality checks)
remedy builder session-intake <session_id> --json
```

Placeholder values (`{goal_summary}`, `{session_id}`, `{job_id}`, etc.)
are auto-sourced from the session and its linked package. No manual
copy-paste required.

The subprocess runs with `shell=False`, sanitized env, hard timeout, and
output byte cap. Raw output is stored privately (0o600 permissions).

### Disable after use

```bash
# Simple path
remedy worker disable claude --json

# Low-level equivalent
remedy execution template-disable claude-code-repair-v0 --json
remedy builder adapter-disable claude-code-v0 --json
```
