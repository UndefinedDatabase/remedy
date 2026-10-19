# Context — adaptive reliability campaign (operator order 2026-10-18)

## Active Branch
feature/adaptive-reliability from PR 361's head `652029edc` (feature/order-cancel, itself on PR
360's `9b172a16c`) in `.remedy-wt/adaptive-reliability`. Merge order: 360, 361, this. The main
checkout stays on main (editable install, supervisor), never switched or pulled here.

## Evidence
- Scale matrix (tests/orchestration/scale_matrix.py) with fake providers, run from the worktree;
  baseline on 652029edc kept in the session scratchpad.
- Reproductions through `run_pingpong` and the real `remedy do` walk in disposable repositories.

## Scope
P0: R-1343 loop half, in-flight planner cancel, project rule delivery, lane/target roles,
plan-only/verify-only wording. P1 as far as measured. API/interface contract additions.

## Steps
The order's phases; the current one is in plan.md. Outside the roadmap queue: F078 stays next.

## Do not touch
The roadmap queue, `.agent/STOP`, the supervisor and service, the live checkout, the lab
repository, provider defaults, `pi.*` caps, Universe's repositories, other sessions' processes.

## Constraints
- Real model calls only as the order's local calibration (disposable fixtures, local Ollama, caps).
- One pytest process tree at a time; focused tests per phase; one full local gate at the end.
- Commits at most 500 insertions; structure ratchet: listed files and functions do not grow.
