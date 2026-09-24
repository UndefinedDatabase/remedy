# Context — F264 Steering channel (remedy chat)

## Active Branch
feature/f264-steering-channel, cut from `main` at `ef4cb503`
(the merge commit of pull request 270, F282 Findings paydown v2).

## Scope
F264 (Tier 5), registered 2026-08-31 by operator order
amend0831-vocab-registrations. It builds the steering channel: a free-form
message to a running job, persisted and certified (T001), folded into the
next prompt at the run's next safe point (T002), and acknowledged with what
was understood and from which round (T003), in `remedy chat` and in the
cockpit, as `docs/roadmap/features/T5_F264.md` specifies. F269 already built
the mission side: `mission_contract.amend_mission_contract`, the round of
effect and the ledger acknowledgement; F264 owns the route a message
arrives by (DECISION F269 D8).

## Do not touch
F009's write-channel contract — its route, payload shape, authentication,
nonce and rate limit; a new exposed catalog id is the extension point F009
D4 built, not a widening. The approval gate. The model call itself: nothing
here reaches into a call in flight. Co-editing a job's worktree is a non-goal
(DECISION amend0921-operator-feedback D5).

## Active assumptions
- A steering message is job-keyed: `remedy do` can make a job with no
  mission, and the channel must serve it (DECISION F264 D1).
- A sealed record never changes; the round a message is consumed in is
  recorded by T002 as a fact of its own.

## Constraints
- `python3 -m ruff check <path>` is the spelling every gate orders.
- A round touching `docs/roadmap/**` also gates `tests/docs/` and
  `tests/orchestration/test_roadmap_index.py`.
- A new module under `apps/` or `packages/` joins
  `tests/orchestration/import_reachability_allowlist.txt` in the same round.
- Destructive verification runs only inside a disposable git worktree under
  `.remedy-wt/`, never in the primary checkout, which satisfies
  `git status --porcelain` empty at every verdict.
- Per operator amendment amend0917-throughput (2026-09-17): the full pytest
  suite runs exactly once per feature, in the closure sequence's
  integration-gate round; a round runs targeted pytest files, the golden
  path, `tests/docs/` when `docs/roadmap/**` changed, and ruff.

The cockpit half (T001's route and T003's rendering) is UI work and binds
`docs/ui/design_reference`; round 1 touches no UI component.

## Steps
The item-status table for each round lives in that round's handback,
`.agent/handoff.md`.
