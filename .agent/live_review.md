# Live Review — Steps 6621-6660 — F007 external acceptance closure

## Verdict (reviewer-owned)
**PASS_WITH_RISKS** — ACCEPTED (F007, external review, 2026-07-13; 0 open findings)

The verdict stays `PASS_WITH_RISKS`, not `PASS`: final human review is still required
before this branch is committed. `review_ready` is therefore `false` in the review
manifest, and that is the honest state — it is not something to be tuned away.

## Builder Handoff

This closure was performed by the **operator by hand**. No Builder ran, no Reviewer ran,
no provider was called (0 provider calls), and neither `job-flow` nor `job-run` was used.

- **Frozen:** the accepted F007 runtime implementation and its tests were not touched —
  `apps/cli/commands/runtime_cmd.py`, `packages/runtimes/dev_server.py`,
  `packages/runtimes/runtime_supervisor.py`, `tests/cli/test_runtime_cmd.py`,
  `tests/runtimes/runtime_cleanup.py`,
  `tests/runtimes/test_runtime_cli_process_boundary.py` and
  `tests/runtimes/test_supervisor_portability.py` are byte-identical to the accepted
  package (7/7 sha256 verified before and after every run).
- **Changed:** acceptance documentation and operator state only, plus one focused
  regression test for the review-manifest parser contract.
- **Not started:** F010 (next feature), F008, F009, F146.
- **Branch:** uncommitted, unpushed, unmerged — awaiting the human commit decision.

## Accepted package

`remedy-review-20260713-115439-READY_FOR_REVIEW.zip`
(sha256 `4df642850249b8e1d2763400311aced43a712fd0523e79e4c6c169d5c0b263a9`),
Evidence job `2e820a4dbf9842cf`, history jobs `eb2b76fd1aba4668`, `809b9b5743694abf`,
7/7 content proofs matched the packaged files.

Independent external verification:
- ZIP sha256 matched exactly; bundle integrity, subject/Evidence alignment, fresh
  Evidence, change provenance, artifact contract and runtime integration all PASS.
- `tests/runtimes/test_supervisor_portability.py` — 99 passed, normal final summary.
- `tests/runtimes/test_runtime_cli_process_boundary.py` — 15 passed, normal final summary.
- Both files in ONE pytest invocation — **114 passed in 525.44s**, normal final summary.
- **No `/tmp/pytest-*` runtime supervisor or application survived any complete run.**
- A deliberately failing pytest probe confirmed the registered subprocess cleanup still
  runs after an assertion failure and leaves no child alive.
- `compileall` and `bash -n scripts/make_review_zip.sh` passed.
- Disclosed environment limitation (not an F007 blocker): the extracted review ZIP excludes
  `apps/ui/node_modules`, so the external host ran 2 apps/ui tests and skipped 5 with an
  explicit missing-Vite-dependency blocker. All 7 pass on the operator environment, where
  the dependencies are already installed; production code is byte-identical.

## Closure state

- F007 is `[x]` in `docs/roadmap/STATUS.md` with the accepted ZIP, Evidence job
  `2e820a4dbf9842cf`, the verdict and the acceptance date; `T0_F007.md` and `README.md`
  record the same truth; the docs-consistency test pins it.
- The long 114-test subprocess proof was not rerun: none of its files changed, and the
  external result is referenced instead.
- **Zero open findings.** Zero provider calls.
