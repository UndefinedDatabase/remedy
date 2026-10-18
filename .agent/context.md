# Context — release-candidate verification (operator order exec-1018c, 2026-10-18)

## Active Branch
feature/release-candidate-verify from PR 364's head `eb439f9fb` (feature/close-from-chat, on 363
`6f26f3c2e`, 362 `cfd906254`, 361 `652029edc`, 360 `9b172a16c`, all on main `6933bb0e0`) in
`.remedy-wt/rc-verify`. Five open PRs, merge withheld by the operator: AGENTS.md "PR Scope Drift
Prevention" option 2 (new branch from the tip, separate dependent PR).

## Scope
Verify, do not reimplement: fixes only for reproduced defects. No new cancellation command.

## Steps
The order's phases; the current one is in plan.md. Outside the roadmap queue: F078 stays next.

## Do not touch
`.agent/STOP`, the supervisor, the live checkout and its `.data` (operator settings deny reading
it), Universe's repositories, other worktrees, provider defaults.

## Constraints
- Disposable data roots and fake providers for evidence; real model runs only if load allows.
- Resource safety: one pytest process tree at a time (`scripts/remedy_pytest.sh` holds the lock),
  focused `-n 4` selections; the workstation is shared with Universe.
- Commits at most 500 insertions; listed ratchet files stay line-neutral.
