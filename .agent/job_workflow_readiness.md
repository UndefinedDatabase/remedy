# Job Workflow Readiness Checklist

Intended single-command development flow (not yet active as default):

```bash
# 1. Plan the job
remedy do job-plan "Implement feature X" --repo .

# 2. Run the job (Builder + Reviewer ping-pong per task)
remedy do job-run <job-id> --repo .

# 3. Export evidence (optional, for audit)
remedy do job-evidence <job-id>

# 4. Preview what would be promoted
remedy do job-promote <job-id> --repo . --dry-run

# 5. Apply reviewed changes to target repo
remedy do job-promote <job-id> --repo . --approve
```

## Safety invariants before switching to this flow

- [x] Job runner runs real two-task Claude jobs
- [x] Job evidence export works
- [x] Job promote is baseline-aware
- [x] Target destination symlinks blocked
- [x] Workspace destination symlinks blocked
- [x] Staged source symlinks blocked in workspace apply
- [x] Initial staging copy does not follow symlinks
- [x] Safe diff does not leak symlink target content
- [x] Durable pre-apply promotion record
- [x] Structured final/partial record update failure
- [x] Dry-run is non-mutating
- [x] Approve requires explicit --approve
- [x] No git commit/push/reset/checkout in product code
- [x] No provider calls during promote
- [x] Review ZIP excludes debug detritus

## Not yet implemented

- [ ] Single-command orchestrator (plan + run + promote in one command)
- [ ] Automatic approval policy
- [ ] DAG scheduling
- [ ] Parallel execution
- [ ] UI
