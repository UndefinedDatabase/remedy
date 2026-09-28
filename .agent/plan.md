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

ROUND 5: book round 4, register and repair R-1100 — three docstrings that
promise a configuration change without a restart — and land the in-app
story panel with its golden walkthrough and headless render (DECISION F039
D6), which closes T002.

## Next Steps

1. T003: the export command and its build, the font licensing finding, the
   size budget, the clean-browser test with zero network requests, and the
   docs.
2. The closure sequence.

## Risks

- The export bundles no font before the licensing finding is written.
