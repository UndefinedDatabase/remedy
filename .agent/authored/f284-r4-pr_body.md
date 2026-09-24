## F284 — Findings paydown v3

The third rolling findings paydown (operator amendment amend0911-feedback rule B). It owned four
open review findings; three are repaired with evidence and one is carried to the next paydown.

### What changed and why

- **R-1046 — the teacher's configured model now reaches `remedy teacher ask`.** The setting
  `teacher.model` (or `REMEDY_TEACHER_MODEL`) was documented but nothing on the question path read
  it. One helper, `teacher_role_overrides` in `packages/orchestration/teacher_model.py`, now reads
  it for both `ask_teacher` and the lessons written after each task; the older lessons-only helper
  is deleted, and the setting's description and `docs/guides/environment.md` say who reads it.
- **R-0499 — a flaky structural sweep, named and repaired.** `test_vitest_passes` skipped only when
  the `apps/ui/node_modules` directory was missing, while its neighbour `test_typescript_compiles`
  skips when the installed `tsc` is missing. A directory that exists but is not yet populated made
  the first fail and the second skip, which is the recorded red signature. The vitest node now
  gates on `apps/ui/node_modules/.bin/vitest`.
- **R-0950 — the zombie-process smoke test no longer reads a foreign port as its own.** Five
  teardown checks in `tests/orchestration/test_product_smoke.py` asserted that nothing listened on
  the app's port, but a fallback port comes from the machine's shared pool and may be reused by an
  unrelated process. One helper now judges teardown by the harness's own scoped sweep, requires this
  worker's own port closed, and fails an open fallback port only when the process holding it runs
  inside the test's project.
- **R-1008 is carried** to F285 — Findings paydown v4, registered by this closure after F026: only
  a closure self-use run can resolve it, and this closure's self-use track found no eligible item.

### Key decisions

DECISION F284 D1 (slice list; one helper for `teacher.model`; R-0499's node named by a controlled
reproduction), D2 (teardown judged by the harness sweep and a port by its holder, at all five
sites; a private port band rejected), D3 (R-1008 carried, F285 registered, PASS_WITH_RISKS).

### How to review

Each repair has mutation red-proofs recorded in `.agent/live_review.md` (`Gate: F284 R1` and
`Gate: F284 R2`); the probe plugin for R-0950 is `.agent/authored/f284-r2-r0950_probe.py`.
Targeted: `python3 -m pytest -q tests/orchestration/test_teacher_model.py
tests/orchestration/test_lessons.py tests/orchestration/test_test_runner.py
tests/orchestration/test_product_smoke.py`.

### Verification

- Full suite, run once at the integration gate: `19094 passed, 20 skipped`, exit 0, no bad node
  (`.agent/authored/f284-closure-suite.txt`).
- Evidence job `f284r3e1001`; package `remedy-review-20260924-224939-READY_FOR_REVIEW.zip`,
  SHA-256 `bd37ef4ace2f086aef2813a61fdb8d58eed56ff10cffa6b9ffead7da64eb91cc`, in
  `/home/decodeux/Repos/remedy-history/zips`; accepted HEAD
  `0bf2591365ad8c58533b62313acaac0cb90d9345`.
- Latest verdict: rounds 1 to 3 PASS; the closing round's verdict is posted on this pull request.
- Open findings after this feature: 1 (R-1008, owned by F285).

### Runtime actuals

Four delegated rounds in one session; wall clock about two hours; reviewer and workers ran on
Claude Opus 5.5; tokens and cost not-measured.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
