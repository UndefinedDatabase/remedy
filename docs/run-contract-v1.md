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

- No user-configurable contracts (hardcoded defaults only)
- No runtime contract mutation
- No token/cost budget enforcement (fields exist, not yet wired)
- No real test execution budget (max_test_runs=0)
- No overnight mode
- No automatic apply

## CLI

```
remedy contract inspect <job_id> --json
remedy contract check <job_id> <action> [--path <path>] [--risk <risk>] --json
```

Both commands are read-only. No repo mutation. No external command execution.

## Integration

- **do_run**: Creates DoRunContract, checks contract before plan/context/build/patch_intent phases
- **repair_loop**: Creates internal repair contract, checks before create_fix_task and create_patch_intent
- **progress_ledger**: Contract blockers appear as `run_contract_blocker` items
- **feature_planner**: Blocked contract items trigger high-priority suggestions via existing rules
- **review_bundle**: `run_contract_summary.json` included in bundles
