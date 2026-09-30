# Plan — F044 Command palette, keyboard, performance budget

Branch: feature/f044-command-palette, cut from `main` at `33f66862`,
the merge commit of pull request 300 (F043 Explanation layer).

## Goal

One bar reaches everything: the command bar grows a palette over the
write door's commands, a fuzzy jump to any task, the projects and the
help, with a routing rule that sends questions to the chat; one keymap
drives the cockpit from the keyboard; and CI enforces the bundle, first
paint and frame-rate budgets (`docs/roadmap/features/T5_F044.md`,
DECISIONS F044 D1 to D11).

## Current Step

ROUND 10: book round 9, record DECISION F044 D11, and sync
`docs/system/ci-self-check-v1.md`'s stage and budget tables to the
`budgets` stage's real, current seven-path selection — a fresh
three-sample measurement (`.agent/f083_inventory.md` `## Q14`) confirms
the stage's `timeout_sec=300` is still correct, so
`packages/orchestration/ci_stages.py` is unchanged.

## Next Steps

1. The closure sequence (docs/roadmap/STATUS_closure_protocol.md): the
   checklist's consolidation, the feature file's Built State, the
   self-use item, the integration gate's one full suite run, the
   evidence bundle and review package, the ledger rotation, and the
   STATUS flip with the pull request.

## Risks

Open findings: 0.
Operator questions open: 0.
