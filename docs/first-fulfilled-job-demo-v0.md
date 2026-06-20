# First Fulfilled Job Demo v0

## What this demo proves

A job is created, tasks are planned, a fixture worker produces artifacts,
a review catches one finding, a repair task fixes it, approval is granted,
the patch is applied to the repo, tests pass, proof is built, the job
reaches completed_verified, and next suggestions are generated.

All of this happens through existing safe gates:
- Repo writes through `patch_apply.apply_patch_intent`
- Tests through `test_execution_service.execute_test_run`
- Proof through `proof_chain.build_proof_chain`

No real provider. No network. No git operations. No hidden execution.

## Demo command sequence

```bash
# 1. Create a job with a repo attached
remedy job create "Improve the project docs" --json
JOB_ID=<job_id from output>
remedy job attach-repo "$JOB_ID" /path/to/demo/repo

# 2. Run fulfillment in fixture-demo mode
remedy job fulfill "$JOB_ID" --fixture-demo --json

# 3. Check final status
remedy job status "$JOB_ID" --json

# 4. Read the full report
remedy job report "$JOB_ID" --json

# 5. List proposed next tasks
remedy propose list --job-id "$JOB_ID" --json

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
| `next_suggestion_ids` | 3 items | Proposed next steps |

### `job status --json` (after fulfill)

| Field | Expected | Meaning |
|-------|----------|---------|
| `state` | `completed` | Job is done |
| `approval_required` | `false` | No pending approvals |
| `code_applied` | `true` | Changes were applied |

### `job report --json` (after fulfill)

| Field | Expected | Meaning |
|-------|----------|---------|
| `code_applied` | `true` | Changes were applied |
| `tasks` | all completed | Every task finished |

## What this demo does NOT prove

- Real provider execution (uses fixture builder/reviewer)
- Real test execution (may use fixture fallback)
- Git operations (no commits, branches, or PRs)
- Multi-repo support
- Rollback on failure
- Budget-aware stopping

## Safety invariants demonstrated

1. **Bounded write**: only `.md` files written through patch apply gate
2. **No provider call**: fixture mode, no API key needed
3. **No git operations**: no commits, no branches, no PRs
4. **Review required**: job cannot complete without review pass
5. **Repair loop**: finding creates repair task, second review confirms fix
6. **Approval gate**: patch intent must be approved before apply
7. **Test gate**: tests must pass (or be accepted) before completion
8. **Proof gate**: proof chain built after apply/test
9. **Contract enforcement**: `completed_verified` only when all gates pass
10. **Honest failure**: test failure stops fulfillment with clear next action
