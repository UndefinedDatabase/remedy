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

ROUND 7. C1 books round 6's PASS and re-points `.agent/plan.md`. C2 clears the
full "Run" bucket (30 of 30): the group descriptions for `ci`, `teacher` and
`test`; the command descriptions and ArgDef help text of `ci.run`,
`integrity.check`, `teacher.ask`, `teacher.narrate`, `test.status`,
`test.result`, `test.list`, `test.run` (`--apply-id`, `--intent-id`),
`mission.run` (description, `--iterations`, `--no-llm`), `mission.readiness`,
`run.show` (description and `run_id`), `job.resume` (`--cycles`), `job.run`
(`--test-command`), `job.apply` (description and `--approve`), `job.evidence`
(`--verification-command`), `do.run` (`--ui`), and `stats.bench` (description
and `--series`). Two of the thirty edits (`test.list`, `test.status`) also
land a bonus, truthful fix on the separate `Job`-word bucket, as a documented
side effect — not a new violation.

After this round: Order remains 1 (`stats.bench`, still the word-sense
collision round 4 named — untouched by this round), Mission, Task, Evidence,
Decision and Run all read 0. Only Project (65) and Job (118, down from 120)
remain — the two largest buckets.

## Next Steps

1. Re-run `_meaning_violations()` grouped by word at the start of round 8;
   expected: Project and Job are the only two buckets left, at approximately
   183-184 total (re-measure rather than trust). Job (~118) is by far the
   largest; Project (~65) is next. Given their size, a future round should
   look for shared constants (as the many `job_id`/`--project` ArgDefs)
   before writing many per-command edits — grep for the most-repeated exact
   help strings among the violations first.
2. This session (session 1 of F281) has now run 7 delegated rounds, inside
   the operator's 6-to-8 target (amend0905-throughput: 6-8 default, 4 the
   floor). The session's own honest assessment governs whether it continues
   or ends with a handoff; either is a legitimate outcome per the protocol.
3. Help wrap, `doctor core` dead-commands (D11d), the D11a catalog
   group-reach test, the visible-order data-pinned test, the F259 enforced
   flip (bounded by DECISION F281 D2's two-item floor, possibly `stats.bench`
   as a third), and the README quickstart's R-0895 line remain entirely
   undone — none of T001's non-description work has started yet.

## Risks

- Same as rounds 2-6: every catalog description edit is verified by
  re-running the real `_meaning_violations()`/`_synonym_offenders()`
  functions against the modified catalog before authoring, diffed fixed vs.
  introduced.
- The Job bucket (~118) likely contains many shared constants and many
  genuinely distinct descriptions; it will need several rounds and careful
  checking for the "fragment is itself a binding word" and "same word,
  different sense" traps this feature has already found twice.
