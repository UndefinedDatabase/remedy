# Plan — F039 Story/replay mode

Branch: feature/f039-story-replay-mode, cut from `main` at `4d60eb84`,
the merge commit of pull request 292 (F038 Grounded chat & intent dispatch).

## Goal

A finished run becomes a story a person can hand on: chapters from the
phases and key events of its event ledger, narration cards synced to the
scrub position with autoplay, and one self-contained HTML export that plays
anywhere without Remedy (`docs/roadmap/features/T5_F039.md`, DECISION F039
D1).

## Current Step

ROUND 7: book round 6 with R-1101's resolution, register and repair R-1102
— the cockpit replacing every minted task id — and land T003's data: the
story payload and its reader, under DECISION F039 D7.

## Next Steps

1. T003 continued: the story player as a second page of the UI build, and
   `remedy job story <id> --export <file>` with its size budget.
2. T003 closed: the clean-browser test from `file://` with zero network
   requests, and the docs.
3. The closure sequence.

## Risks

- A story larger than the configured budget is refused, never cut.
