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

ROUND 4: book round 3 with R-1099's resolution, and land the story's data
path: the two pacing keys and the dashboard's `story` section, a budget
tick's figures on its feed row, and the pure story view (DECISION F039 D5).

## Next Steps

1. T002 closed: the in-app story panel on the demo recording, driving the
   timeline's scrub, with its golden walkthrough and its assumption-log
   entry.
2. T003: the export command and its build, the font licensing finding, the
   size budget, the clean-browser test with zero network requests, and the
   docs.
3. The closure sequence.

## Risks

- The design reference draws no story mode and no narration card; the
  panel's round records its treatment in the assumption log.
- The export bundles no font before the licensing finding is written.
