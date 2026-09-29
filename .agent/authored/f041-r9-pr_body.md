## What

F041 — Artifact preview. A job's results become tangible in the cockpit:

- T001: the job's README is rendered on the server by the standard library alone and rebuilt from
  an allowlist, so raw HTML, script, event handlers, `javascript:` links and scheme-bearing images
  never reach the page; the reviewer's attack corpus in `tests/orchestration/test_artifact_markdown.py`
  pins every vector's whole output and only grows. `/api/jobs/<id>/artifacts` answers it with the
  screenshots under the evidence directory's `captures/`, and the file route serves exactly
  `README.md` as plain text and one captured image, with `nosniff`, a sandboxing content security
  policy and `no-store`; R-1105 made the static asset route's containment a path test.
- T002: a preview is the job's own project run by the runtime harness's `serve`, `probe` and `stop`
  verbs; its record shows a link only after a probe passed, and the probe's own link, so the
  harness's free-port fallback shows the port that answered. The write door's `job.preview-start`
  and `job.preview-stop` hand the request to the UI server's preview worker, which re-probes a live
  preview every fifteen seconds, stops one nobody has viewed for `preview.idle_ttl_seconds`
  (default 900) and stops them all when the server closes. `remedy job preview-start` and
  `remedy job preview-stop` drive it from the command line.
- T003: a Results button opens a panel with the app card, the README (the one
  `dangerouslySetInnerHTML` of `apps/ui/src`, pinned by a contract test) and a screenshot grid that
  opens a lightbox; the guided tour gains a "See it running" stop for a job whose project can run;
  and an end-to-end test drives a real UI server and a real small app from the door's start to the
  worker's idle stop, with no process left. R-1106 made the README's image rewrite a single pass.

## Why

T5_F041.md asks that results become tangible without leaving the cockpit, with no dead links, no
XSS and no fake liveness: the link renders only after a probe passes, and stopping a preview is as
easy as starting it.

## Key decisions (in `.agent/decisions.md`)

- F041 D1 — the README is rendered and sanitized on the server by the standard library alone; the
  reviewer ships the attack corpus as the tests.
- F041 D2 — the file route serves exactly two kinds of name, with headers that keep a served file
  from ever running as a page.
- F041 D3 — a preview runs the harness's own verbs through their JSON envelopes; one record per job
  whose link is written only after a probe passed.
- F041 D4 — the door records the request and the UI server's preview worker acts on it, re-probes
  and stops idle previews.
- F041 D5 — the Results panel, its pure rules, its send and its two read doors.
- F041 D6 — the tour's `preview` anchor and the end-to-end proof.

## How to review

Server: `packages/orchestration/artifact_markdown.py`, `artifact_preview.py`, `preview_control.py`,
`preview_runner.py`, `preview_worker.py`, the `artifacts`, `artifacts/file` and `preview` routes and
the preview clause of the door in `ui_server.py`, and the `preview` anchor in `result_tour.py`.
Cockpit: `apps/ui/src/api/artifactPreview.ts`, `previewSend.ts` and
`apps/ui/src/components/artifacts/`. The Built State of `docs/roadmap/features/T5_F041.md` walks
all three slices; each round's mutation tool is under `.agent/authored/f041-r*-mutations.py`.

## Verification

- The one full suite, on the tree that ships: `20859 passed, 20 skipped` at exit 0, no bad node
  (`.agent/authored/f041-closure-suite.txt`).
- Evidence job `f041r8e1001` against the fork point `45c584e6`: 782 selected tests passed at exit 0.
- Review package `remedy-review-20260929-110032-READY_FOR_REVIEW.zip`, SHA-256
  `069f6b42c571f38b94f1cd4359faf276b2aeec67afcd0155bef1ead648c5a103`, READY_FOR_REVIEW.
- A headless Chrome render of the Results panel read eight checks of eight
  (`.agent/authored/f041-r5-render.txt`).
- The closure's self-use reading: the generator and the queue both answered none, so no self-use
  item is consumed (queue exhausted).

## Findings and notes

Latest verdict PASS; accepted PASS. Two findings were raised and resolved inside the feature,
R-1105 and R-1106. Open findings after this feature: none.

## Runtime actuals

Nine rounds in two sessions, from the branch's first commit at 06:00 on 2026-09-29 to the accepted
head `72bee58a` at 10:57 the same day (UTC+2); reviewer and workers ran as Claude Opus 5.5; tokens
not measured. Remedy itself made no provider call.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
