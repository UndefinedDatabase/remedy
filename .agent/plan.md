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

ROUND 6. C1 books round 5's PASS and re-points `.agent/plan.md`. C2 clears the
full "Mission" bucket (16 of 16): 8 identical `mission_id` ArgDefs (abandon,
achieve, continue, pause, plan, resume, show, watchdog — one global
find-and-replace of the shared literal string), `mission.handoff`'s own
distinct `mission_id` ArgDef, `mission.run`'s `run_id` ArgDef,
`mission.start`'s `goal` ArgDef, and 5 command descriptions (`mission.handoff`,
`mission.pause`, `mission.resume`, `mission.run`, `mission.watchdog`).

After this round: Order reads 1 (`stats.bench`, unfixed per round 4's note),
Mission and Task and Evidence and Decision all read 0. Only Run, Project and
Job remain — the three largest buckets, ~29, 65 and 120 respectively before
this round's own measurement (which touches none of them directly, though
`mission.run` and `mission.watchdog`'s Run-fragment satisfaction was already
in place from round 3, so no cascade is expected here — confirm at round 7's
start).

## Next Steps

1. Re-run `_meaning_violations()` grouped by word at the start of round 7;
   expected: Run, Project, Job are the only three buckets left, at
   approximately 216 total (232 minus this round's 16 — re-measure rather
   than trust). Job (~120) is by far the largest; Project (~65) and Run
   (~29-30) are next. Given their size, a future round should look for
   shared constants (as `_LIST_DESC_ARG`/`_TASK_OPT`/the `mission_id` literal
   already proved out) before writing many per-command edits — grep for the
   most-repeated exact help strings among the violations first.
2. This session (session 1 of F281) has now run 6 delegated rounds, inside
   the operator's 6-to-8 target. The session's own honest assessment governs
   whether it continues or ends with a handoff; either is a legitimate
   outcome per the protocol, not a fixed count.
3. Help wrap, `doctor core` dead-commands (D11d), the D11a catalog
   group-reach test, the visible-order data-pinned test, the F259 enforced
   flip (bounded by DECISION F281 D2's two-item floor, possibly `stats.bench`
   as a third), and the README quickstart's R-0895 line remain entirely
   undone — none of T001's non-description work has started yet.

## Risks

- Same as rounds 2-5: every catalog description edit is verified by
  re-running the real `_meaning_violations()`/`_synonym_offenders()`
  functions against the modified catalog before authoring, diffed fixed vs.
  introduced.
- The Job bucket (~120, by far the largest) likely contains many shared
  constants and many genuinely distinct descriptions; it will need several
  rounds and careful checking for the "fragment is itself a binding word"
  and "same word, different sense" traps this feature has already found
  twice.
