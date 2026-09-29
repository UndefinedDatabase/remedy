# Plan — F041 Artifact preview

Branch: feature/f041-artifact-preview, cut from `main` at `45c584e6`,
the merge commit of pull request 294 (F286 Findings paydown v5).

## Goal

Make a job's results tangible in the cockpit: its README as sanitized
markdown, its screenshots in a lightbox, and an app card that shows a live
link only after a probe passes (`docs/roadmap/features/T5_F041.md`,
DECISION F041 D1).

## Current Step

ROUND 3: book round 2 and R-1105's resolution, record DECISION F041 D3,
and land the preview record and its state machine, the runner of the
harness's own verbs, and `remedy job preview-start` and `preview-stop`.

## Next Steps

1. The door's preview commands, the server-side step acting on their
   requests, revalidation of a live preview and the idle stop.
2. T003: the panel, the lightbox and the end-to-end run.
3. The closure sequence.

## Risks

Open findings: 0.
