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

ROUND 3: book round 2 with R-1098's resolution, register and repair
R-1099 — the narration goldens' untested count of events — and land
T002's autoplay pacing with its chapter pauses (DECISION F039 D4).

## Next Steps

1. T002 closed: the in-app story mode on the demo recording, the pacing's
   configuration keys, its golden walkthrough and its assumption-log entry.
2. T003: the export command and its build, the font licensing finding, the
   size budget, the clean-browser test with zero network requests, and the
   docs.
3. The closure sequence.

## Risks

- The design reference draws no story mode and no narration card; the
  in-app round records its treatment in the assumption log.
- The export bundles no font before the licensing finding is written.
