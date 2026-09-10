# Mission Run Loop + Morning Report v0

> **Status: SEMANTICS SUPERSEDED** — The overnight / time-of-day mechanics described here
> are explicitly deprecated by the roadmap (docs/roadmap/ROADMAP.md, Teil B).
> The underlying execution and approval concepts remain valid.

## What is a Mission Run?

A Mission Run is a bounded, step-at-a-time orchestration loop. It evaluates
what Remedy should do next, records the decision, and stops when done,
blocked, or out of budget.

A Mission Run is not a fixed-duration timer. It stops as soon as the mission
is satisfied, or when it cannot safely continue.

## Quick start (recommended)

```bash
# 1. Run a bounded mission loop, keyed on a MISSION id
remedy mission run <mission_id> --json

# 2. Read the morning report, keyed on a JOB id
remedy mission report <job_id> --json
```

These are the operator-facing commands, and since F275 they are the only
ones: the internal `dogfood` group they used to wrap is deleted.

## What makes a run stop?

A run stops on any of these conditions:

- Mission satisfied (contract fulfilled with required evidence)
- Blocked (no safe action available)
- Waiting for approval (operator must approve managed execution)
- Waiting for operator (builder session needs human action)
- Budget exhausted (token budget reached)
- Operator stopped (manual stop command)
- Iteration cap reached (`--iterations`)
- No safe next action
- Internal error

Remedy deliberately ships no per-step or wall-clock cap on `remedy mission
run`. The `--max-steps` and `--max-seconds` flags belonged to the deleted
dogfood loop, were accepted and ignored by the surviving handler, and F275
removed them rather than wiring them in — see R-0871 and DECISION F275 D14.

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

## How Self-Repair Proposals fit

They do not, any more. The `self-repair` group and the proposal queue behind
it were deleted by F275; the approval gate F017 owns inherited the idea of a
policy-authorised approval, and no surviving command creates, lists or
approves a self-repair proposal. The finding R-0845 records what was lost and
DECISION F260 D3 records which feature took which idea.

## What is still manual

For full overnight autonomy, these steps still require operator action:

- Starting the loop (`remedy mission run`)
- Reviewing builder output
- Applying approved self-repair proposals
- Merging PRs

The loop and report make the state visible. They do not act autonomously
beyond evaluating state and recording checkpoints.

## Terminology note

The CLI group `dogfood` was internal developer naming for the prototype this
page was written against. Operator-facing documentation uses:

- **Mission Run** — the bounded loop
- **Mission Report** — the morning report

Remedy deliberately ships no low-level equivalents of these two commands.
The whole `dogfood` group — create, run-loop, morning-report, step, replay
and show — was deleted by F275 together with the module behind it, and
nothing stands in for it: there is no alias, no shim and no compatibility
reader, per AGENTS.md Scope Control. The operator-facing pair above is the
only surface, and git history is where the prototype lives now.
