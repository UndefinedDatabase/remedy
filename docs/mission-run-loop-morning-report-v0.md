# Mission Run Loop + Morning Report v0

## What is a Mission Run?

A Mission Run is a bounded, step-at-a-time orchestration loop. It evaluates
what Remedy should do next, records the decision, and stops when done,
blocked, or out of budget.

A Mission Run is not a fixed-duration timer. It stops as soon as the mission
is satisfied, or when it cannot safely continue.

## Quick start (recommended)

```bash
# 1. Run a bounded mission loop
remedy mission run <run_id> --job-id <job_id> --json

# 2. Read the morning report
remedy mission report <run_id> --job-id <job_id> --json
```

These are the operator-facing commands. They call the same logic as the
internal `dogfood` commands below.

## What makes a run stop?

A run stops on any of these conditions:

- Mission satisfied (contract fulfilled with required evidence)
- Blocked (no safe action available)
- Waiting for approval (operator must approve managed execution)
- Waiting for operator (builder session needs human action)
- Budget exhausted (step, token, or wall-clock limit reached)
- Operator stopped (manual stop command)
- Max loop steps reached (loop-level cap, default 10)
- Max loop seconds reached (wall clock, default 300)
- No safe next action
- Internal error

No unbounded loop is allowed.

## What the Morning Report tells you

The morning report answers:

- Is it done?
- Is it stuck?
- What is it waiting for?
- Did a builder (like Claude Code) run?
- Is there output?
- Did output pass intake/review/test gates?
- Is there a proposed self-repair prompt?
- What should I do next?

## How Claude Code fits

Claude Code can be launched through managed execution rails:

1. Operator adds worker: `remedy worker add claude --json`
2. Operator approves execution for a session
3. Loop or operator runs managed execution
4. Output enters sandbox intake (untrusted)
5. Morning report shows execution status

See `docs/controlled-claude-code-operator-path-v0.md` for the full walkthrough.

## How Self-Repair Proposals fit

The morning report shows:

- Whether proposals exist
- Latest proposal status
- How many await operator review
- Command to inspect proposals

Self-repair proposals are never auto-created by the loop. They come from
prior analysis (replay, review, test failures).

## What is still manual

For full overnight autonomy, these steps still require operator action:

- Starting the loop (`remedy mission run`)
- Approving managed execution (`remedy execution approve`)
- Reviewing builder output
- Applying approved self-repair proposals
- Merging PRs

The loop and report make the state visible. They do not act autonomously
beyond evaluating state and recording checkpoints.

## Terminology note

The CLI group `dogfood` is internal developer naming. Operator-facing
documentation uses:

- **Mission Run** — the bounded loop
- **Mission Report** — the morning report
- **Self-Repair Proposal** — suggested fix from analysis

The internal `dogfood` commands remain available for debugging and
backwards compatibility.

## Internal commands (advanced)

```bash
# Create a run
remedy dogfood create <job_id> --json

# Run the bounded loop (low-level)
remedy dogfood run-loop <run_id> --job-id <job_id> --max-steps 10 --max-seconds 300 --json

# Morning report (low-level)
remedy dogfood morning-report <run_id> --job-id <job_id> --json

# Single step (fine-grained control)
remedy dogfood step <run_id> <job_id> --json

# Replay analysis
remedy dogfood replay <run_id> <job_id> --json

# Quick status
remedy dogfood show <run_id> <job_id> --json
```
