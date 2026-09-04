# Plan — F114 Cost preview per command

Branch: feature/f114-cost-preview-per-command, cut from `main` after
pull request 234 was merged at the Open PR Gate.

## Goal

Expensive actions stop starting silently: commands that will spend real
money show an upfront estimate band with its basis and require
confirmation above a configured threshold in attended mode; unattended
runs rely on budgets, not prompts (docs/roadmap/features/T3_F114.md).

## Current Step

Round 11 runs the INTEGRATION GATE (docs/agents/integration_gate.md,
steps 1-5) before closure: branch run vs. a base run at the merge-base
`a1b5d4bb455550f082da7d6c4c80fd968d6e1a88` (PR 234's merge into main),
UI parity restored in a disposable worktree on a throwaway branch,
every branch-only failure attributed, evidence saved under
`.agent/gate_f114_r11/`. The worker measures; only the reviewer issues
the gate verdict at the next round.

## Next Steps

- If the gate is clean (no unattributed branch-only failure): author
  the closure sequence per STATUS_closure_protocol.md - evidence job,
  fresh review zip, the STATUS line, the PR. T003's core scope (mark,
  golden tests, docs) is complete; marking further commands
  `is_expensive` and real cost bands for `job.run` are named as
  explicit future work in the guide and the feature file, not blockers.
- If a branch-only failure is a genuine BLOCKER coupled to F114 code:
  that repair is its own reviewer-gated round before closure proceeds.
- Session note: round 11, session 3 - 2nd delegated round this session,
  at the 4-5 default.

## Risks

- The integration gate is the round most likely to surface xdist-flake
  noise (F135/F052 class) unrelated to F114; every branch-only id gets
  a serial re-run and a stated attribution, never an assumed one.
- UI parity (apps/ui/node_modules, apps/ui/dist) must be restored
  correctly in the base worktree or false base-only failures mask real
  ones (R-0736 mtime lesson) - the block states the exact copytree and
  re-stamp procedure rather than leaving it to be improvised.