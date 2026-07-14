# Live Review — Steps 7161-7260 — F010 closure — automatic failure post-mortems

## Verdict (reviewer-owned)
**PASS_WITH_RISKS** — ACCEPTED (F010, external review, 2026-07-14; 0 open findings)

## Builder Handoff

F010 is externally accepted. The reviewed package was
`remedy-review-20260714-135557-READY_FOR_REVIEW.zip`
(sha256 `02b36b4de139c966f6173a2090a023f35721414fe4eb053e00f1297df95ed53e`,
Evidence job `01363c70e13046e2`, linked prior `953ec09d1b4b4403`). The SHA matched, 23/23
content proofs matched, no Source/Test file was missing or uncovered, and the seven
`O_NOFOLLOW` failures from the previous Linux 4.4 round are gone.

External results: F010 core **194 passed**, writer suite **109 passed**, focused F007
redaction **26 passed**. One supporting invocation reported `518 passed, 1 failed`; the
single failure was the unchanged F007 test
`tests/runtimes/test_dev_server.py::TestReadiness::test_readiness_timeout_stops_the_tree_and_leaves_no_state`,
which assumed a new Python process reaches its first `print()` within 1.5s. That is a test
assumption, not a runtime defect: the runtime timed out and stopped the tree correctly.

This run applied one narrow correction: the test now polls `runtime.log` for the
`"booting but never listening"` marker under a finite 30s setup deadline (failing loudly if
it never appears), asserts the process is still alive, and only then calls `wait_ready()`.
The short readiness timeout, the `ready` error class, the bounded log tail, the process-tree
stop and the no-leftover-state assertions are all unchanged. No F007 production code was
touched.

## Disclosed risks (both accepted)

1. **Same-UID directory relocation is outside the v1 threat model.** The writer refuses path
   traversal, pre-existing symlinks, different-inode substitution, an ineffective
   `O_NOFOLLOW` and the ordinary check/open race. It does not resist a process running as
   the same OS user that renames an already-opened private evidence directory — that
   adversary can modify Remedy's evidence directly anyway. Defending against it needs
   `openat2`/mount constraints or a separate service account. Documented in
   `docs/roadmap/features/T0_F010.md`.
2. **The slow-host F007 test was hardened test-side only.** The readiness proof is now
   deterministic on a host where interpreter startup exceeds 1.5s; `packages/runtimes/dev_server.py`
   is unchanged.

## Open findings

0.

## Status

F010 `[x]` — accepted 2026-07-14. F011 not started.
