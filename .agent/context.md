# Context — F200 Daemon mode (remedy serve)

## Active Branch
feature/f200-daemon-mode, cut from `main` at `959b88a85`
(the merge commit of pull request 307, F292 Plan view and hunk decisions in the cockpit).

## Scope
F200 (Tier 12): `remedy serve`, one supervisor per data root that answers the cockpit's write door
on a unix socket, takes the command line's door commands and `job run` while it runs, and runs its
jobs again after a restart, per `docs/roadmap/features/T12_F200.md` as its Amendment section
states it. DECISION F200 D1 fixes the amended design and the round order.

## Do not touch
Direct mode stays first-class: with no socket every command runs exactly as today. No second write
protocol: the socket carries the F009 envelope through the cockpit's own checks. The write door's
argument checks and refusal codes, and the STOP file (F011), stay as they are.

## Active assumptions
- The supervisor and its clients find each other only through `serve_paths` of one data root.
- A command the door does not carry runs direct in both modes (DECISION F200 D1 (3)).

## Constraints
- Every pytest run in a round is targeted; `tests/regression/test_resource_safety.py`'s budgets
  apply to every run before the closure's one full suite.
- A round touching `docs/roadmap/**` also gates `tests/docs/`.
- Per amend0930-test-load: no block, worker or reviewer sets `REMEDY_TEST_MAX_WORKERS`, passes a
  larger `-n`, or starts two test runs at once; mutation red-proofs are run by the reviewer only.
- Destructive verification runs only inside a disposable git worktree under `.remedy-wt/`.

## Steps
The item-status table for each round lives in that round's handback, `.agent/handoff.md`.
