# Context — reliability campaign (operator order 2026-10-17, after PR 360)

## Active Branch
feature/order-cancel from PR 360's head `9b172a16c` in `.remedy-wt/order-cancel`. It depends on PR
360 (feature/execution-excellence): merge 360 first. The main checkout stays on main: `remedy serve
start` (editable install) runs its code, so nothing is switched or pulled there.

## Evidence (read through Remedy's own readers; `.data/**` not read raw)
- `remedy status --json` and `remedy client story 537d7c3612864597 --json` on the operator's data
  root, read-only, from outside the checkout.
- `select_do_lane` probed against this branch's code with `PYTHONPATH` set to the worktree.

## Scope
Order and job cancellation over CLI and HTTP, terminal state of abandoned work, story words for
waiting and stopped work, lane honesty findings of the PR 360 review.

## Steps
The order's phases; the current one is in plan.md. Outside the roadmap queue: F078 stays next.

## Do not touch
The roadmap queue, `.agent/STOP`, the supervisor and service, the lab repository, the sandbox,
provider defaults, `pi.*` caps, Universe's repositories.

## Constraints
- No real model call (no authorized Pi budget); fake providers only.
- One pytest process tree at a time; one full local gate at the end.
- Commits at most 500 insertions; structure ratchet: listed files and functions do not grow.
