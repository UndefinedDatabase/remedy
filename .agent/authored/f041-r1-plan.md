# Plan — F041 Artifact preview

Branch: feature/f041-artifact-preview, cut from `main` at `45c584e6`,
the merge commit of pull request 294 (F286 Findings paydown v5).

## Goal

Make a job's results tangible in the cockpit: its README as sanitized
markdown, its screenshots in a lightbox, and an app card that shows a live
link only after a probe passes (`docs/roadmap/features/T5_F041.md`,
DECISION F041 D1).

## Current Step

ROUND 1: claim F041, re-head the live review record, book F286's round 4,
record DECISION F041 D1, and land the sanitized markdown pipeline against
the reviewer's attack corpus, the artifact roots with their traversal
fixtures, and the `/api/jobs/<id>/artifacts` route.

## Next Steps

1. The file route for screenshot bytes and the full README, with its
   headers, and the start of T002.
2. T002: the preview commands, the supervisor intent, the probe-gated link
   and its failure fixtures.
3. T003: the panel, the lightbox, the idle stop and the end-to-end run.
4. The closure sequence.

## Risks

Open findings: 0.
