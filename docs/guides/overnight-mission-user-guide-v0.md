# Overnight missions — user guide (v0)

> **Status: SEMANTICS SUPERSEDED** — The overnight / time-of-day mechanics described here
> are explicitly deprecated by the roadmap (docs/roadmap/ROADMAP.md, Teil B).
> The underlying execution and approval concepts remain valid.

This guide explains, in plain language, how Remedy tracks a mission you give it and decides whether
it is **done** — without running any model, worker, or test on its own yet.

## What a mission contract is

When you give Remedy a goal, it creates a **mission contract**: a written record of what you asked
for, what counts as done (your acceptance criteria), what's allowed and forbidden, and which quality
gates must pass. Remedy then tracks that contract until it is fulfilled or safely blocked.

```
remedy overnight contract-create <job_id> --user-goal "Fix the failing checkout test" \
       --acceptance "checkout test passes, no new failures" --json
remedy overnight evaluate <contract_id> --json
remedy overnight next-action <contract_id> --json
```

## What counts as done

A mission is **done** only when, from real evidence:

- you have defined acceptance criteria,
- the reviewer verdict is PASS with no open Blocker/High findings,
- no tasks are still open,
- no tests are failing,
- the required gates (tests/proof) pass,
- there's no open repair.

If you haven't given acceptance criteria yet, Remedy says so and asks you to define them — it will
**not** pretend the mission is complete.

## Why open review findings block completion

Remedy trusts the **independent reviewer**, not its own claims. If the reviewer has open Blocker or
High findings — or hasn't set PASS — the mission cannot be "done". A builder writing "fixed it" is
not the same as the reviewer marking it resolved.

## Why missing tests/proofs/snapshots block real overnight mode

Real overnight work needs real test results and rollback proof. Those don't exist yet, so if your
contract requires them, Remedy reports them as **missing gates** and keeps the mission open. It never
fakes a green test or a verified proof.

## Required next actions vs optional future ideas

Remedy separates two lists:

- **Required next actions** — what's needed to satisfy *this* mission (e.g. resolve a review finding,
  continue a repair, define acceptance criteria).
- **Optional future ideas** — nice product ideas for later, shown only once the current contract is
  satisfied so they never distract from finishing the job.

## What is not automated yet

- Remedy does **not** run Claude, Pi, OpenCode, Ollama, or any provider/model.
- Remedy does **not** run tests, apply patches, approve changes, or open PRs on its own here.
- There is **no** full overnight autonomy yet — this is the contract/readiness spine that future
  worker adapters will plug into.

## Where Claude/Pi/OpenCode/Ollama/MemPalace fit later

- Future **worker adapters** (Claude/Pi/OpenCode/Ollama/cloud) will do the actual building; the
  contract already defines what "done" means for them.
- **MemPalace** is an external memory tool that may later store mission learnings across runs. Nothing
  is stored as long-term memory in this version.
