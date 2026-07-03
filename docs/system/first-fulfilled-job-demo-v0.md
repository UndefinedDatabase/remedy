# First Fulfilled Job Demo v0

## What this demo proves

A job is created, tasks are planned, a fixture worker produces artifacts,
a review catches one finding, a repair task fixes it, approval is granted,
the patch is applied in an isolated staging workspace, tests pass in staging,
proof is built, staged changes are promoted to the target repo, the job
reaches completed_verified, and next suggestions are generated.

All of this happens through existing safe gates:
- Repo writes through `patch_apply.apply_patch_intent`
- Tests through `test_execution_service.execute_test_run`
- Proof through `proof_chain.build_proof_chain`

No real provider. No network. No git operations. No hidden execution.

## Demo command sequence

```bash
# 1. Create a job with a repo attached
JOB_ID=$(remedy job create "Improve the project docs")
remedy job attach-repo "$JOB_ID" /path/to/demo/repo  # see Repo Requirements below

# 2. Run fulfillment in fixture-demo mode
remedy job fulfill "$JOB_ID" --fixture-demo --json

# 3. Check final status
remedy job status "$JOB_ID" --json

# 4. Read the full report
remedy job report "$JOB_ID" --json

# 5. List proposed next tasks
remedy propose list "$JOB_ID" --json

# 6. User decides on suggestions
remedy propose approve "$JOB_ID" <task_id> --json
remedy propose reject "$JOB_ID" <task_id> --json
remedy propose defer "$JOB_ID" <task_id> --json
```

## Expected output fields

### `job fulfill --fixture-demo --json`

| Field | Expected | Meaning |
|-------|----------|---------|
| `status` | `completed_verified` | All gates passed |
| `task_count` | >= 2 | At least two tasks planned |
| `review_round_count` | >= 2 | First review found issue, second passed |
| `repair_task_ids` | non-empty | One repair task created from finding |
| `apply_ids` | non-empty | Patch applied through safe gate |
| `test_passed` | `true` | Tests passed |
| `proof_status` | `verified` or `accepted` | Proof confirmed |
| `final_review_status` | `pass` | All contract gates passed |
| `staging_used` | `true` | Apply/test ran in isolated staging |
| `staging_promoted` | `true` | Staged changes promoted to target |
| `next_suggestion_ids` | 3 items | Proposed next steps |

### `job status --json` (after fulfill)

| Field | Expected | Meaning |
|-------|----------|---------|
| `state` | `completed` | Job is done |
| `approval_required` | `false` | No pending approvals |
| `code_applied` | `true` | Changes were applied |
| `fulfillment_status` | `completed_verified` | Fulfillment completed |
| `staging_used` | `true` | Staging workspace was used |
| `staging_promoted` | `true` | Changes promoted to target |

### `job report --json` (after fulfill)

| Field | Expected | Meaning |
|-------|----------|---------|
| `code_applied` | `true` | Changes were applied |
| `tasks` | all completed | Every task finished |

## Repo requirements

The target repo must contain a discoverable test command (e.g. `pytest`, a
`Makefile` test target, or a `scripts/` test runner). The test execution
service discovers and runs tests automatically.

- **No-test repos** block honestly with `stop_reason=no_test_command`.
- **Failing-test repos** block honestly with `stop_reason=test_not_passed:failed`.
- **Target repo is unchanged** until promotion succeeds. Blocked jobs leave
  target untouched.
- **Proof** may be `accepted` with reason in fixture mode because fixture
  workers do not emit all proof chain events.

Use `create_demo_repo()` from `packages.orchestration.job_fulfillment` to
generate a valid demo repo for testing.

## Blocked fulfillment behavior

When fulfillment is blocked:

| Field | Value | Meaning |
|-------|-------|---------|
| `status` | `blocked` | Fulfillment stopped |
| `code_applied` | `false` | Target was not modified |
| `staging_promoted` | `false` | Staged changes not promoted |
| `changed_target_files` | `[]` | No target files changed |
| `stop_reason` | descriptive | Why it blocked |
| `next_safe_action` | command | What to do next |

Staged files are listed in `staged_files` but are NOT target changes.

## What this demo does NOT prove

- Real provider execution (uses fixture builder/reviewer)
- Real test execution (tests run through Test Execution Service but in demo repo only)
- Git operations (no commits, branches, or PRs)
- Multi-repo support
- Budget-aware stopping

## Safety invariants demonstrated

1. **Isolated staging**: apply/test/proof run in staging workspace, not target repo
2. **No metadata mutation**: `target_repo` in saved job never points to staging
3. **Explicit override**: staging apply uses `target_repo_override`, not metadata mutation
4. **Scoped cleanup**: staging parent always removed via try/finally, not atexit
5. **Bounded write**: only `.md` files written through patch apply gate
6. **MD-only promotion**: non-markdown files blocked during promotion with blockers recorded
7. **Prefix-based append**: modify promotion requires staged content to start with exact target content
8. **Env file exclusion**: `.env`, `.env.*`, `.env-*` files excluded from staging copy
9. **Symlink escape detection**: symlinks resolving outside repo root excluded from staging
10. **No provider call**: fixture mode, no API key needed
11. **No git operations**: no commits, no branches, no PRs
12. **Review required**: job cannot complete without review pass
13. **Repair loop**: finding creates repair task, second review confirms fix
14. **Approval gate**: patch intent must be approved before apply
15. **Test gate**: tests must pass (or be accepted) before completion
16. **Proof gate**: proof chain built after apply/test
17. **Contract enforcement**: `completed_verified` only when all gates pass
18. **Honest failure**: test failure stops fulfillment with clear next action
