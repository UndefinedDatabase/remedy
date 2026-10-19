# Context — release readiness (operator order rel-1019, 2026-10-19)

## Active Branch
feature/release-readiness from PR 365's head `7181a2311` (feature/release-candidate-verify, on 364
`eb439f9fb`, 363 `6f26f3c2e`, 362 `cfd906254`, 361 `652029edc`, 360 `9b172a16c`, all on main
`6933bb0e0`) in `.remedy-wt/release-readiness`. Six open PRs, merge withheld by the operator:
AGENTS.md "PR Scope Drift Prevention" option 2 (new branch from the tip, separate dependent PR).

## Scope
Verify, do not reimplement: fixes only for reproduced defects. No new cancellation command, no new
orchestration architecture, no Universe UI code.

## Steps
The order's phases; the current one is in plan.md. Outside the roadmap queue: F078 stays next.

## Do not touch
`.agent/STOP`, the supervisor, the live checkout and its `.data` (operator settings deny reading
it), the seven live jobs, Universe's repositories, other worktrees, provider defaults.

## Constraints
- Disposable data roots and fake providers for evidence; no paid model calls; real local runs
  only if load allows.
- Resource safety: one pytest process tree at a time, focused `-n 6` selections at most; the
  workstation is shared with Universe.
- Commits at most 500 insertions; listed ratchet files stay line-neutral.
