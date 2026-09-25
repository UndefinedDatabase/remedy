# Context — F025 Pause/resume (global & per node)

## Active Branch
feature/f025-pause-resume, cut from `main` at `49624d5c`
(the merge commit of pull request 279, F024 Phase timeline with scrubber).

## Scope
F025 (Tier 5): pause and resume at two scopes — the control kinds, the
paused states and the safe-point and ready-set integration (T001), the
write-channel commands with their audit, the CLI verbs and live fake-job
tests (T002), and the UI states, banner, NowCard line and the end-to-end
(T003), as `docs/roadmap/features/T5_F025.md` specifies, with
`docs/ui/design_reference/` authoritative on the visuals.

## Do not touch
The kill switch's terminals, the checkpoint format, and session mechanics.

## Active assumptions
- A pause is a control fact beside the stop, read at the stop's safe
  points; a parked job is `paused` with a pause record and its process
  exits; the relaunch is the resume (DECISION F025 D1).

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
