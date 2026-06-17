# Mission Run Loop + Morning Report v0

## What is a Mission Run?

A mission run is a bounded, step-at-a-time orchestration loop. It evaluates
what Remedy should do next, records the decision, and stops when done,
blocked, or out of budget.

A mission run is not a fixed-duration timer. It stops as soon as the mission
is satisfied, or when it cannot safely continue.

## Terminology

The CLI group is `dogfood` (internal developer naming). Operator-facing
documentation prefers:

- **Mission Run** — the bounded loop
- **Self-Test Run** — when Remedy tests itself
- **Run Replay** — checkpoint log analysis
- **Evidence Bundle** — review bundle with proof chain
- **Self-Repair Proposal** — suggested fix from analysis

The CLI commands remain unchanged for backwards compatibility.

## What makes a run stop?

A run stops on any of these conditions:

- Mission satisfied (contract fulfilled with required evidence)
- Blocked (no safe action available)
- Waiting for approval (operator must approve managed execution)
- Waiting for operator (builder session needs human action)
- Budget exhausted (step, token, or wall-clock limit reached)
- Operator stopped (manual stop command)
- Max loop steps reached (loop-level cap)
- Max loop seconds reached (wall clock for this invocation)
- No safe next action
- Internal error

No unbounded loop is allowed.

## Quick start

```bash
# 1. Create a run
remedy dogfood create <job_id> --json

# 2. Run the bounded loop (10 steps, 5 minutes max)
remedy dogfood run-loop <run_id> --job-id <job_id> --max-steps 10 --max-seconds 300 --json

# 3. Check the morning report
remedy dogfood morning-report <run_id> --job-id <job_id> --json

# 4. Single step (fine-grained control)
remedy dogfood step <run_id> <job_id> --json

# 5. Replay analysis
remedy dogfood replay <run_id> <job_id> --json
```

## How to inspect at any time

After 10 minutes, 1 hour, or overnight:

```bash
# Quick status
remedy dogfood show <run_id> <job_id> --json

# Full morning report
remedy dogfood morning-report <run_id> --job-id <job_id> --json
```

The morning report answers:

- Is it done?
- Is it stuck?
- What is it waiting for?
- Did Claude/another builder run?
- Is there output?
- Did output pass intake/review/test gates?
- Is there a proposed self-repair prompt?
- What should I do next?

## How Claude Code fits

Claude Code can be launched through the existing managed execution rails:

1. Operator enables adapter + template (`remedy execution claude-doctor --json`)
2. Operator approves execution for a session
3. Loop or operator runs managed execution
4. Output enters sandbox intake (untrusted)
5. Morning report shows execution status

See `docs/controlled-claude-code-operator-path-v0.md` for the full walkthrough.

## How Self-Repair Proposals fit

The morning report shows:

- Whether proposals exist
- Latest proposal status
- How many await approval
- Command to inspect proposals

Self-repair proposals are never auto-created by the loop. They come from
prior analysis (replay, review, test failures).

## What is still manual

For full overnight autonomy, these steps still require operator action:

- Starting the loop (`remedy dogfood run-loop`)
- Approving managed execution (`remedy execution approve`)
- Reviewing builder output
- Applying approved self-repair proposals
- Merging PRs

The loop and report make the state visible. They do not act autonomously
beyond evaluating state and recording checkpoints.
