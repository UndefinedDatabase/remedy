# Context — F035 Ownership ledger

## Active Branch
feature/f035-ownership-ledger, cut from `main` at `a0b287a5`
(the merge commit of pull request 289, F030 Steering messages).

## Scope
F035 (Tier 5): one ownership ledger per job — every human-attributable
action with its actor, time, verbatim text and consequence, built as a
pure pass over the records earlier features already write, rendered as
plain sentences in the report, the digest, the browser and the command
line, as `docs/roadmap/features/T5_F035.md` and DECISION F035 D1 specify.

## Do not touch
Audit formats (consumed, not changed), decision semantics, and future
authentication or identity.

## Active assumptions
- The ledger reads every record and writes none of them; its file is
  regenerable and never a second truth (DECISION F035 D1).
- An actor is never named beyond what its record holds: a door, and a
  token number for a browser fingerprint.

## Constraints
- Every pytest run in a round is targeted and serial; the resource and
  pytest budgets of `tests/regression/test_resource_safety.py` apply.
- A round touching `docs/roadmap/**` also gates `tests/docs/`.
- Destructive verification runs only inside a disposable git worktree under
  `.remedy-wt/`, never in the primary checkout.
- Per operator amendment amend0917-throughput (2026-09-17): the full pytest
  suite runs exactly once per feature, in the closure sequence's
  integration-gate round.

## Steps
The item-status table for each round lives in that round's handback,
`.agent/handoff.md`.
