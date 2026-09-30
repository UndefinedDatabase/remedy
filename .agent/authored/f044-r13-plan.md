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

ROUND 13, the closure sequence's third round: the integration gate.
Book round 12, then the feature's ONE full suite run
(`python3 -m pytest -n auto -q`, worker, primary checkout,
amend0917-throughput rule 1), committed verbatim as
`.agent/authored/f044-closure-suite.txt`.

## Next Steps

1. If the suite is green: the evidence bundle and the review zip
   package.
2. If the suite carries any bad node: a repair round (amend0917-
   throughput rule 2 — the shrinking rule, at most three repair
   rounds), unless the same node is already red on `main`'s own hosted
   CI record for the merge base.

## Risks

Open findings: 1 (`R-1117`, Medium, owned by F290).
Operator questions open: 0.
