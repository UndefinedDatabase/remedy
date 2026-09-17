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

ROUND 10. C1 books round 9's PASS (with a G5-arithmetic correction and two
prose-slip lines) and re-points `.agent/plan.md`. C2 clears 14 of the
Project bucket's 32 remaining violations: the `_PROJECT_ID` constant (6
call sites — `project.show`, `project.attach-repo`, `project.attach-job`,
`project.brain`, `project.context`, `project.summary`), the duplicated
`--repo` literal `"Path to the project (defaults to the current
directory)"` (3 sites: `runtime.serve`, `runtime.probe`, `runtime.stop`),
and all 5 remaining group descriptions (`status`, `memory`, `runtime`,
`test`, `brain`).

After this round: Order remains 1 (`stats.bench`, unchanged), Job remains 41
(untouched this round). Project drops from 32 to 18 — the remaining text is
`do.run`'s own `--project` ArgDef ("Project ID to use or create"),
`init.run`'s `--project-name`, `project.create`'s `name` and
`--description` ArgDefs, and 14 command descriptions across the `project.*`,
`brain.*`, `job.list`, `runtime.serve`, `stats.backfill-ledger` and
`status.run` commands — all genuinely distinct per-command prose, no further
shared literals found in this bucket.

## Next Steps

1. Re-run `_meaning_violations()` grouped by word at the start of round 11;
   expected: Job (~41) and Project (~18) are the only two buckets left
   (plus Order's 1 unfixed `stats.bench` collision), at approximately 60
   total (re-measure rather than trust). Both remaining buckets are now
   located, per-command prose; continue with careful individual edits,
   batching by group/command family where the prose can share a pattern
   without forcing an inaccurate one.
2. Session 2 of F281 is now 2 delegated rounds in (rounds 9-10), still below
   the 6-to-8 target (amend0905-throughput); continue.
3. Help wrap, `doctor core` dead-commands (D11d), the D11a catalog
   group-reach test, the visible-order data-pinned test, the F259 enforced
   flip (bounded by DECISION F281 D2's two-item floor, possibly `stats.bench`
   as a third), and the README quickstart's R-0895 line remain entirely
   undone — none of T001's non-description work has started yet.
4. Gate-authoring lesson from round 9 (see `.agent/prose_slips.md`, two
   2026-09-17 lines): every future G5 sweep in this feature states, per
   edit, the exact count of the LITERAL TEXT actually written to disk —
   never the count of violations the edit is credited with fixing — and a
   worker that corrects an unmeetable or wrong gate clause records the
   correction explicitly under "Deviations & assumptions," never leaving it
   to read "None."

## Risks

- Same as rounds 2-9: every catalog description edit is verified by
  re-running the real `_meaning_violations()`/`_synonym_offenders()`
  functions against the modified catalog before authoring, diffed fixed vs.
  introduced.
- The remaining Job (~41) and Project (~18) buckets are entirely located,
  per-command prose; expect several more rounds of smaller, careful edits,
  with continued vigilance for the "fragment is itself a binding word" and
  "same word, different sense" traps this feature has already found twice,
  plus the new G5-arithmetic lesson above.
