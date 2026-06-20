# First Perfect Job Demo v0

## What this demo proves

A user gives Remedy a goal. Remedy creates a bounded job, produces safe
evidence, stops before any dangerous action, and explains exactly what
happened and what the next safe action is.

Specifically:

1. `do run` creates a job with tasks and artifacts
2. `job status` shows artifact count, approval state, and next safe action
3. `job report` shows task details, patch intents, and `code_applied: false`
4. No code is applied, no PR created, no provider executed, no repo mutated

## Demo command sequence

```bash
# 1. Create a temporary repo
DEMO_REPO=$(mktemp -d)
cd "$DEMO_REPO" && git init && echo "x = 1" > main.py && git add . && git commit -m "init"

# 2. Run a job with fixture builder (deterministic, no real provider)
remedy do run "Fix the bug in main.py" \
  --repo "$DEMO_REPO" \
  --json \
  --fixture-builder true \
  --autonomy-level 2

# 3. Extract the job ID from output
JOB_ID=$(remedy do run "Fix the bug in main.py" \
  --repo "$DEMO_REPO" --json --fixture-builder true --autonomy-level 2 \
  | python3 -c "import sys,json; print(json.load(sys.stdin).get('job_id',''))")

# 4. Check job status
remedy job status "$JOB_ID" --json

# 5. Read job report
remedy job report "$JOB_ID" --json

# Cleanup
rm -rf "$DEMO_REPO"
```

## Expected output fields

### `job status --json`

| Field | Expected value | Meaning |
|-------|---------------|---------|
| `state` | `paused` or `pending` | Job stopped before dangerous action |
| `artifact_count` | >= 1 | Builder produced at least one artifact |
| `approval_required` | `true` (if patch intent exists) | Operator must approve before apply |
| `patch_intent_ids` | non-empty list (if patch) | Identifies what needs approval |
| `latest_stop_reason` | `approval_required` or `autonomy_too_low` | Why the job stopped |
| `next_safe_action` | approval or run-loop command | What the operator should do next |
| `code_applied` | (not in status) | Status does not claim apply |

### `job report --json`

| Field | Expected value | Meaning |
|-------|---------------|---------|
| `code_applied` | `false` | v1 never applies code without approval |
| `tasks` | list with task details | Shows what was planned |
| `artifact_count` | >= 1 | Evidence was produced |
| `approval_required` | `true` (if patch) | Same as status |

## What this demo does NOT prove

- Real provider execution (uses fixture builder)
- Code application (v1 never applies)
- PR creation (v1 never creates PRs)
- Test execution after repair (requires approval)
- Multi-cycle autonomous loop (bounded by contract)

## Safety invariants demonstrated

1. **No code mutation**: `code_applied` is always `false`
2. **No provider call**: fixture builder is deterministic, no API key needed
3. **No repo mutation**: working directory unchanged after `do run`
4. **Explicit stop**: job stops at approval boundary with clear reason
5. **Structured truth**: all state is JSON, testable, no `.agent/` dependency
