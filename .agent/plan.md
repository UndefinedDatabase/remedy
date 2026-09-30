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

ROUND 11, the closure sequence's first round: book round 10, record
DECISION F044 D12 (discharging T003's Design-only "trend visible" line
as out of scope; Acceptance's own "numbers" clause is already met), the
feature file's Built State for T001 through T003, the checklist
consolidation pass (nothing to add — no F044 round left a
`.agent/prose_slips.md` entry), and the closure's self-use item: run to
its approval gate, its findings registered if any.

## Next Steps

1. Land the self-use item's own diff, with reviewer-authored tests, and
   its own Built State paragraph (mirroring F043's R6→R7 split).
2. The integration gate: the feature's one full suite run
   (`python3 -m pytest -n auto -q`, worker, primary checkout),
   committed as `.agent/authored/f044-closure-suite.txt`.
3. The evidence bundle and the review zip package.
4. Runtime actuals, the STATUS line, the ledger rotation, the README
   sync, the closure commit and the pull request.

## Risks

Open findings: 0 (pending the self-use item's own defects, if any,
registered this round).
Operator questions open: 0.
