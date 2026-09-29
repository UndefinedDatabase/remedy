# Plan — F041 Artifact preview

Branch: feature/f041-artifact-preview, cut from `main` at `45c584e6`,
the merge commit of pull request 294 (F286 Findings paydown v5).

## Goal

Make a job's results tangible in the cockpit: its README as sanitized
markdown, its screenshots in a lightbox, and an app card that shows a live
link only after a probe passes (`docs/roadmap/features/T5_F041.md`,
DECISION F041 D1).

## Current Step

ROUND 4: book round 3 and record DECISION F041 D4, then land the door's
preview commands, the UI server's preview worker with its revalidation and
idle stop, the `preview` view that shows a link only while live, and the
`preview.idle_ttl_seconds` key.

## Next Steps

1. T003: the preview panel with the README, the screenshot grid and
   lightbox, and the app card, per the design reference.
2. The end-to-end run on a fixture app, then the closure sequence.

## Risks

Open findings: 0.
