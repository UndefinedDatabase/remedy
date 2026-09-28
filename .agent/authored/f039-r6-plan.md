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

ROUND 6, the repair of round 5: book its FAIL with R-1100's resolution,
register and repair R-1101 — the story panel's autoplay stalling while its
host re-renders — and prove the repair in the headless render.

## Next Steps

1. T003: the export command and its build, the font question settled by
   the asset authority, the size budget, the clean-browser test with zero
   network requests, and the docs.
2. The closure sequence.

## Risks

- The export bundles no font: `assets_spec.md` forbids base64 fonts in CSS.
