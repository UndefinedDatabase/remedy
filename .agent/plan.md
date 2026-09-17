# Plan — F281 CLI help surface

Branch: feature/f281-cli-help-surface, cut from `main` at
`c617dd74df26b8e677161b265a88d5926f4d78ab`, the merge commit of pull request 253
(F280's closure).

## Goal

Every catalog description, role label and help page reads as the finished
vocabulary of DECISION amend0905-vocab D4 once F280 has pruned and renamed the
command tree (`docs/roadmap/features/T2_F281.md`). DONE when T001 and the
Acceptance list hold.

## Current Step

ROUND 9. C1 books round 8's PASS and re-points `.agent/plan.md`. C2 clears 77
of the 118 Job-bucket violations via SEVEN shared-literal edits: the
`_JOB_ID` constant (61 call sites across every group that takes a bare job
UUID argument), the literal `"Job ID"` help string (3 sites: `job.run`,
`job.evidence`, `job.apply`), `job.stop`'s own `"Job ID to stop"`, `job.budget`'s
own `"Job ID to inspect"`, the `"Job UUID scope"` literal (3 sites:
`memory.store`, `memory.recall`, `memory.list`), the `"Job ID scope"` literal
(6 sites: the six `memory.card-*` commands), and the `"Only this job's
calls"` literal (2 sites: `stats.cost`, `stats.cache`).

After this round: Order remains 1 (`stats.bench`, unchanged), Project remains
32 (untouched this round), Mission, Task, Evidence, Decision and Run all
read 0. Job drops from 118 to 41 — the remaining text is the 10 still-unique
`--job`/`--job-id` ArgDefs (`teacher.ask`, `job.stop`'s own `--reason`,
`brain.continue`'s `--prompt`, `mission.continue`'s `next_step`,
`stats.failures`'s and `stats.report`'s own `--job` texts, `stats.backfill-ledger`'s
and `stats.verify-ledger`'s `evidence_dir` ArgDefs, and `self.inspect`'s and
`self.report`'s `--job-id` texts) plus the 31 command-description violations
(mostly the `brain.*`, `job.*`, `event.*`, `patch.*`, `change.*` and
`decision.*` group descriptions that name "job" without a meaning fragment).
All 66 `job_id`-named ArgDefs are fully cleared by this round (61 via the
shared constant, 3+1+1 via the four other job_id edits); the 10 remaining
arg violations are all distinct `--job`/`--job-id`/`evidence_dir` texts.

## Next Steps

1. Re-run `_meaning_violations()` grouped by word at the start of round 10;
   expected: Job (~41) and Project (~32) are the only two buckets left
   (plus Order's 1 unfixed `stats.bench` collision), at approximately 74
   total (re-measure rather than trust). The remaining Job items are mostly
   unique per-command text (command descriptions and distinct ArgDef
   strings) rather than shared literals, so this next round is likely
   located, per-command edits rather than another leverage round.
2. Session 2 of F281 begins at round 9 (round 1 of this session). Continue
   toward the 6-to-8 delegated round target (amend0905-throughput) before
   the session's own honest context assessment governs whether to continue
   or end.
3. Help wrap, `doctor core` dead-commands (D11d), the D11a catalog
   group-reach test, the visible-order data-pinned test, the F259 enforced
   flip (bounded by DECISION F281 D2's two-item floor, possibly `stats.bench`
   as a third), and the README quickstart's R-0895 line remain entirely
   undone — none of T001's non-description work has started yet.

## Risks

- Same as rounds 2-8: every catalog description edit is verified by
  re-running the real `_meaning_violations()`/`_synonym_offenders()`
  functions against the modified catalog before authoring, diffed fixed vs.
  introduced.
- The remaining Job and Project buckets (~41 and ~32) are mostly located,
  per-command prose rather than shared literals; expect several more rounds
  of smaller, careful edits, with continued vigilance for the "fragment is
  itself a binding word" and "same word, different sense" traps this
  feature has already found twice.
