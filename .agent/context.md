# Context — F044 Command palette, keyboard, performance budget

## Active Branch
feature/f044-command-palette, cut from `main` at `33f66862`
(the merge commit of pull request 300, F043 Explanation layer).

## Scope
F044 (Tier 5): the command palette fused with the command bar, a fuzzy
node jump, the question-versus-command routing rule, one keymap module
with its cheat overlay, and the bundle, first paint and frame-rate
budgets in CI, as `docs/roadmap/features/T5_F044.md` and DECISION F044
D1 specify.

## Do not touch
The chat's internals (routed to, not built), the zoom transitions, and
the CI entrypoint's architecture.

## Active assumptions
- The write door's exposed set is the one source of the palette's
  commands, held there by a contract test (DECISION F044 D1 (1)).
- The bar's routing rule is the chat's own parse, held there by shared
  goldens (DECISION F044 D1 (3)).
- The palette's seven form entries stay disabled until F292 builds the
  plan view and the hunk controls they open (DECISION F044 D5).
- One keymap module decides every shortcut; a press from a field is text
  (DECISION F044 D5).

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
