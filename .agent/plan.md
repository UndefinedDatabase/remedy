# Plan — F044 Command palette, keyboard, performance budget

Branch: feature/f044-command-palette, cut from `main` at `33f66862`,
the merge commit of pull request 300 (F043 Explanation layer).

## Goal

One bar reaches everything: the command bar grows a palette over the
write door's commands, a fuzzy jump to any task, the projects and the
help, with a routing rule that sends questions to the chat; one keymap
drives the cockpit from the keyboard; and CI enforces the bundle, first
paint and frame-rate budgets (`docs/roadmap/features/T5_F044.md`,
DECISIONS F044 D1 and D2).

## Current Step

ROUND 2: book round 1, record DECISION F044 D2, and build the bar's
dropdown sheet: the Recent, Jump, Projects and Help rows, the combobox,
the deletion of the shell's `handleJump`, and the tour's sixth stop on
the bar, proved in a real browser by a render harness.

## Next Steps

1. The commands: the Commands section, their execution and argument
   flows, the disabled states with their reasons, the route to the
   chat, and the reference's placeholder.
2. The form entries' structured flows: the plan edits and the hunks.
3. The keymap module and its cheat overlay.
4. The three budgets in CI with their recorded numbers.
5. The closure sequence.

## Risks

Open findings: 0.
