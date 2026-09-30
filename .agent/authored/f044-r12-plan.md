# Plan — F044 Command palette, keyboard, performance budget

Branch: feature/f044-command-palette, cut from `main` at `33f66862`,
the merge commit of pull request 300 (F043 Explanation layer).

## Goal

One bar reaches everything: the command bar grows a palette over the
write door's commands, a fuzzy jump to any task, the projects and the
help, with a routing rule that sends questions to the chat; one keymap
drives the cockpit from the keyboard; and CI enforces the bundle, first
paint and frame-rate budgets (`docs/roadmap/features/T5_F044.md`,
DECISIONS F044 D1 to D12).

## Current Step

ROUND 12, the closure sequence's second round: book round 11, register
`R-1117` (the self-use item's own reviewer approving a task that
changed nothing — the safety net that caught it, `describe_self_use_
run_defects`, working as designed), owned by F290, and add the
self-use item's own paragraph to the feature file's Built State.
Nothing from the self-use item's job branch is applied — its diff was
empty.

## Next Steps

1. The integration gate: the feature's one full suite run
   (`python3 -m pytest -n auto -q`, worker, primary checkout),
   committed as `.agent/authored/f044-closure-suite.txt`.
2. The evidence bundle and the review zip package.
3. Runtime actuals, the STATUS line, the ledger rotation, the README
   sync, the closure commit (which sets `scripts/self_use_queue.json`'s
   `SU-039.consumed_by` to `F044`) and the pull request.

## Risks

Open findings: 1 (`R-1117`, Medium, owned by F290).
Operator questions open: 0.
