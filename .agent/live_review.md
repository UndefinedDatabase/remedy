# Live Review — Steps 6081-6140 — F007 — Runtime harness

Reviewer: external final reviewer (independent; owns the verdict).

## Verdict

**MERGED AS AN HONEST CHECKPOINT** — the persistent-supervisor round has NOT been
externally accepted. The last external review
(`remedy-review-20260712-134354-READY_FOR_REVIEW.zip`, job `959213bbdabe432f`,
13 content proofs, 339 evidence tests) returned FINDINGS, the binding one being that
`runtime serve` was not persistent across the CLI process boundary. That is now fixed
and proved with real separate-process tests, but the fix itself has not been through
an external round, so F007 stays `[~]`.

## Branch / Base

- Branch: `feature/f007-runtime-harness`
- Base: `d969688` (main after the F006 merge)

## Scope

`remedy runtime serve|probe|stop`; RuntimeSpec bound to `.remedy/config.toml
[runtime]` with vite/next/uvicorn detection; free-port fallback with the effective
port reported; HTTP readiness with a bounded log tail; psutil process-tree shutdown
with no zombies; durable runtime state whose identity is PID + creation time +
command fingerprint, so a recycled PID can never be killed.

## Task scopes (manual completion, non-overlapping)

- T001 process manager + process-tree/dummy-server tests.
- T002 config, detection, CLI group, catalog and handler tests.
- T003 real apps/ui Vite probe + roadmap/state.

## Verification

- F007 — 167 passed (dev_server 28, runtime_config 19, runtime CLI 16, lifecycle
  safety 51, state machine 32, CLI process boundary 14, real apps/ui 7), each file
  run separately. No failing tests.
- Affected: command catalog 23, CLI UX 57, config CLI 14, config 55, stream
  evidence 38.
- compileall, `bash -n scripts/make_review_zip.sh`, `git diff --check` clean.
- Zero provider calls; local HTTP servers, real subprocess trees and the already
  installed apps/ui dependencies only.

## Status

Implementation merged into main. F007 remains `[~]` pending external acceptance of
the supervisor architecture. F008 and F146 untouched.
