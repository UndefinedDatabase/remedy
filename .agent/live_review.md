# Live Review — Steps 7601-7700 — F011 closure — safe kill switch

## Verdict (reviewer-owned)
**PASS_WITH_RISKS** — ACCEPTED (F011, external review, 2026-07-14; 0 open findings)

## Builder Handoff

F011 is externally accepted. The reviewed package was
`remedy-review-20260714-223538-READY_FOR_REVIEW.zip`
(sha256 `47b5e2e98fcecb4e1aee25196f975fe89793a9b66620574719eb044236b3b9f2`,
Evidence job `49955e41c49f41bc`, linked prior `4044e32fa99d47a6`). The SHA matched, 20/20
content proofs matched, no Source/Test file was missing or uncovered, provider calls were 0,
and `postmortem_integrity` was `{ok: true, failures: []}`.

External results: the new core block **327 passed**; the affected orchestration block
**213 passed, 2 deselected**. The two deselected `test_event_replay.py::TestDocsExist` tests
look for a missing `docs/resume.md`; they fail identically on clean `main` and have nothing to
do with F011, so they are untouched here.

The reviewer independently reproduced that the previous parent-of-root symlink escape is now
refused for both `safe_points.request_stop()` and `failure_postmortem.write_postmortem()` —
the fix lives in the shared `packages/common/secure_fs.py`, so F010 and F011 cannot drift
apart again.

## Accepted boundaries (v1)

- The runner is not SIGKILL-recoverable: with the process gone there is no safe point left to
  observe. Stale-RUNNING recovery is a later feature.
- Checkpoint v1 is the persisted job; there are no deep checkpoints.
- No OS signal on the normal stop path, no signal handler, no thread, no daemon, no database.

## Verification (actual pytest summaries)

- F011/F010 core (six suites) → **327 passed**.
- CLI regression (`propose_cli`, `propose_cli_runtime`, `grouped_cli`, `command_catalog`,
  `cli_ux`) → **581 passed**.
- Affected orchestration + docs → **213 passed, 2 deselected** (pre-existing `docs/resume.md`).
- compileall, `bash -n scripts/make_review_zip.sh`, `git diff --check` clean.

## Status

F011 `[x]` — accepted 2026-07-14. F012 `[ ]` and **not started**.
