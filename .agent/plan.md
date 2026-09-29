# Plan — F041 Artifact preview

Branch: feature/f041-artifact-preview, cut from `main` at `45c584e6`,
the merge commit of pull request 294 (F286 Findings paydown v5).

## Goal

Make a job's results tangible in the cockpit: its README as sanitized
markdown, its screenshots in a lightbox, and an app card that shows a live
link only after a probe passes (`docs/roadmap/features/T5_F041.md`,
DECISION F041 D1).

## Current Step

ROUND 1 COMPLETE. Amendment F041 R1 A1 withdrew C3's stop clause and split
it into C3a (S1-S4, `artifact_markdown.py`) and C3b (S5-S6 + allowlist.diff,
`artifact_preview.py` and the `ui_server.py` route). All of C1a-C1c, C2, C7,
A0, C3a, C3b, C4, C5, C6, C8 are committed and pushed. The reviewer's whole
corpus and traversal fixtures pass unedited (106+20+5 = 131), ruff is clean,
integrity check reads all six pass, and all 9 named mutations are caught and
restored cleanly in a real worktree at C6.

## Next Steps

1. ROUND 2: the file route for screenshot bytes and the full README, with
   its headers, and the start of T002.
2. T002: the preview commands, the supervisor intent, the probe-gated link
   and its failure fixtures.
3. T003: the panel, the lightbox, the idle stop and the end-to-end run.
4. The closure sequence.

## Risks

Open findings: 0.
