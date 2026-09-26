## What

F285 — Findings paydown v4. All five review findings open at the claim are repaired with evidence,
and none was added:

- R-1058: the self-use generator's job asks for the repair its finding names, with a red-to-green
  test, and tells the builder not to edit `.agent/`; `describe_self_use_run_defects` names a pass
  whose reviewed work changed no path outside `.agent/`.
- R-1057: the self-use cost cap is 6.00 USD, derived beside it from the dearest measured call and
  one build, one review and one repair round (operator question Q5 records the raised spend).
- R-1055: every round's builder and reviewer blocks in a run's `result.json` carry the provider
  session and whether it was resumed, and the relaunch of a task a park or a stop interrupted offers
  the parked run's sessions to its first calls, which resume them where the provider supports resume.
- R-1064: both `sk-` patterns of the stream-evidence redactor match only at a token start. THIS
  REPAIR WAS WRITTEN BY REMEDY ITSELF: the closure's self-use item `SU-032` ran as job
  `78ecdc636060461c` on `claude-cli` at `claude-sonnet-4-6`, completed with its review passing on the
  first round for 0.85 USD, and its diff was reviewed and landed verbatim (`e03f438c`).
- R-1008: resolved by that run — the first closure self-use run whose diff landed as a repair.

## Why

The self-use track is the check that Remedy can be used on Remedy, and until now no run of it had
ever landed anything. This feature repaired the reasons and then let the track prove itself.

## Key decisions (in `.agent/decisions.md`)

- F285 D1 — the slice list; the track is repaired before it is used; the closure's self-use run is
  aimed at R-1064; the cost cap is derived, not chosen.
- F285 D2 — the run record carries each call's session; the relaunch offers the parked sessions to
  its first calls with the prompt left at full context.

## How to review

`packages/orchestration/self_use_generator.py` (`_ledger_tier`), `self_use_findings.py`,
`self_use_runner.py` (`_MEASURED_MAX_CALL_USD`, `_COST_CAP_CALLS`, `_MAX_COST_USD`), then
`pingpong_loop.py` (`_session_fields`, `parked_session_refs`, `builder_call_resume` /
`reviewer_call_resume`) and the one call site in `pingpong_job.py`, then
`packages/orchestration/stream_evidence.py`. The Built State of `docs/roadmap/features/T2_F285.md`
lists every slice; each round's mutation tool is `.agent/authored/f285-r<n>-mutations.py`; the
self-use run's records are under `.agent/selfuse_f285/`.

## Verification

- The one full suite, on the tree that ships: `19449 passed, 20 skipped` at exit 0, no bad node
  (`.agent/authored/f285-closure-suite.txt`).
- Evidence job `f285r5e1001` against the fork point `83d3bb95`: 765 selected tests passed at exit 0,
  `tests/orchestration/test_plan_editing.py` among them for the first time.
- Review package `remedy-review-20260926-020855-READY_FOR_REVIEW.zip`, SHA-256
  `dba140f371cfe8071690be30605ba1643a77a8f5d000f66a40d8dd43c056d4d5`, READY_FOR_REVIEW.

## Findings and notes

Latest verdict PASS; accepted PASS. Open findings after this feature: none. The closure registers
F286 — Findings paydown v5 under operator amendment amend0911-feedback rule B.

## Runtime actuals

Six rounds in one session, from the branch's first commit at 23:50 on 2026-09-25 to the accepted head
`c2a4588a` on 2026-09-26; reviewer and workers ran as Claude Opus 5.5; tokens not measured. The
closure's self-use run spent 0.85 dollars in two provider calls.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
