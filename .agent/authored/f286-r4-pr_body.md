## What

F286 — Findings paydown v5. The one review finding open at the claim is repaired with evidence,
and none was added:

- R-1104: the staleness catalog's config-key check, `_run_c07` in
  `packages/orchestration/doc_staleness.py`, leaves out a backticked span whose last segment is a
  file extension, so the story guide's `story.html` is no longer reported as an unregistered config
  key, while an unregistered key such as `story.speed` still is. A test over the live truth holds
  that no registered config key ends in one of those extensions.

## Why

The false report made every closure's self-use generator offer the same item again, and the one
self-use run that took it answered by removing the file name's code formatting, which made the
guide worse. The check was wrong, not the guide.

## Key decisions (in `.agent/decisions.md`)

- F286 D1 — the slice list is one slice, landed in the claiming round; R-1104 is not made the
  closure's self-use item.

## How to review

`packages/orchestration/doc_staleness.py` (`_FILE_EXTENSIONS`, `_run_c07` and the
`doc_config_keys` entry of `CHECKS`) and `tests/orchestration/test_doc_staleness.py`. The Built
State of `docs/roadmap/features/T2_F286.md` lists the slice; the round's mutation tool is
`.agent/authored/f286-r1-mutations.py`.

## Verification

- The one full suite, on the tree that ships: `20613 passed, 20 skipped` at exit 0, no bad node
  (`.agent/authored/f286-closure-suite.txt`).
- Evidence job `f286r3e1001` against the fork point `6ba1f4be`: 557 selected tests passed at exit 0.
- Review package `remedy-review-20260929-044850-READY_FOR_REVIEW.zip`, SHA-256
  `13311e03d7335e6ad49adc91a0d961e3bc832026dce35fa57fb173c5eddd3d9a`, READY_FOR_REVIEW.
- The closure's self-use reading: the generator and the queue both answered none, so no self-use
  item is consumed (queue exhausted).

## Findings and notes

Latest verdict PASS; accepted PASS. Open findings after this feature: none. The closure registers
F290 — Findings paydown v6 under operator amendment amend0911-feedback rule B.

## Runtime actuals

Four rounds in one session, from the branch's first commit at 04:16 on 2026-09-29 to the accepted
head `b7c09100` at 04:45 the same day (UTC+2); reviewer and workers ran as Claude Opus 5.5; tokens
not measured. Remedy itself made no provider call.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
