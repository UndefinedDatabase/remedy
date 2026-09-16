# Run Contract v1

## Overview

A Run Contract is an immutable execution boundary for a Remedy job run. It defines what actions are allowed, what paths are safe, and what budgets apply. It is enforced before each phase in `do_run` and `repair_loop`.

## What the contract controls

- **Allowed/denied actions**: Which phase actions can execute (plan, build, create_patch_intent, etc.)
- **Path policy**: Which file paths are writable/readable and which are blocked
- **Loop budget**: Maximum number of loops before the run stops
- **Test budget**: Maximum test runs allowed
- **Runtime budget**: Maximum wall-clock seconds
- **Apply gate**: `stop_before_apply=True` blocks all apply/source_apply actions by default
- **Risk policy**: `stop_on_unknown_risk`, `stop_on_medium_risk` block actions with insufficient risk assessment
- **Cloud policy**: `no_cloud=True` blocks all cloud provider and network fetch actions

## Default behavior

By default, a v1 contract:

- Allows: plan, context, build_artifact, create_patch_intent, discover_commands, write_metadata
- Denies: apply, source_apply, arbitrary_shell, cloud_provider, network_fetch, install_packages
- Blocks all apply actions (`stop_before_apply=True`)
- Blocks unknown-risk actions (`stop_on_unknown_risk=True`)
- Enforces local-only execution (`no_cloud=True`)
- Denies writes to `.env`, `.env.secret`, `.git/`, `credentials.json`, etc.
- Max 10 loops, 0 test runs (test execution not yet enabled)

## Path rules

- Absolute paths are always blocked
- Path traversal (`..`) is always blocked
- Denied paths take precedence over allowed paths
- If `allowed_paths` is empty, no path restriction applies (action-level checks still apply)

## What v1 does not do

- No overnight mode
- No automatic apply

## Persistence

One contract is persisted per job in `job.metadata["run_contract"]`. `ensure_contract(job)` loads it or creates+saves a default. `contract_id` and `created_at` are stable across calls. Usage is tracked separately in `job.metadata["run_usage"]`.

## Contract mutation

No command sets a contract field: F261 round 17 deleted the `contract` group, whose `set`
subcommand was the only writer of `max_loops`, `max_test_runs`, `max_runtime_seconds`,
`stop_before_apply`, `stop_on_unknown_risk`, `stop_on_medium_risk`, `no_cloud` and `notes`.
The contracts written now are the default of `build_default_run_contract`, the caller
override `do_run` persists for the job it creates, and the fixture contract of
`job_fulfillment`.

## CLI

None. The group's three subcommands were deleted by F261 round 17 under DECISION
amend0905-vocab D4, which frees the word `contract` for the acceptance criteria of a
mission. A job's execution boundary is read as its permissions and fences with
`remedy job show <job_id> --full --json`.

## Integration

- **do_run**: Loads persisted contract via `ensure_contract(job)`, checks before each phase, records usage
- **repair_loop**: Loads same persisted contract via `ensure_contract(job)`, checks before create_fix_task and create_patch_intent, records usage
