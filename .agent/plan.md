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

ROUND 3. C1 books round 2's PASS and re-points `.agent/plan.md`. C2 clears the
full "Decision" meaning-violation bucket (6 of 6: `group:decision:description`,
`command:decision.show:description`, both `decision_id` ArgDefs of
`decision.show`/`decision.resolve`, `command:patch.approve-hunks:description`,
`command:mission.watchdog:description`) plus two side-effect fixes that landed
on the same two multi-violation descriptions (`patch.approve-hunks`'s Job
violation, `mission.watchdog`'s Evidence violation) — 8 total, zero
introduced, pre-verified against the real `_meaning_violations()`/
`_synonym_offenders()` functions before authoring.
`mission.watchdog`'s OWN Mission violation is deliberately left open this
round: its only three meaning fragments (`order`, `job`, `contract`) are
THEMSELVES binding words needing their own fragment nearby, so naming any of
them bare would trade one violation for another (measured directly: an
earlier draft using "against its contract" introduced a new Contract
violation) — it stays in the Mission bucket for a round that can afford a
longer rewrite bringing a fragment's own fragment along with it.

## Next Steps

1. Re-run `_meaning_violations()` grouped by word at the start of round 4;
   expected counts after this round: Decision 0 (was 6), Evidence 12 (was
   13), Job 121 (was 122), Mission 16 (unchanged), Order 14, Run 30, Task 9,
   Project 65 — 267 total. Take the next-smallest bucket (Task, 9, unless a
   fresh measurement disagrees).
2. The "fragment is itself a binding word" trap (this round's own finding,
   above) applies whenever a rewrite reaches for Mission's, Job's or Run's own
   fragment list, since each of those three lists is built entirely or partly
   from other binding words (Mission: order/job/contract; Job: mission/
   budget/fence/task; Run: task/evidence) — always re-run the before/after
   diff against the real catalog functions, never assume a single targeted
   fix is isolated.
3. Help wrap, `doctor core` dead-commands (D11d), the D11a catalog
   group-reach test, the visible-order data-pinned test, the F259 enforced
   flip (bounded by DECISION F281 D2's two-item floor), and the README
   quickstart's R-0895 line remain entirely undone.

## Risks

- Same as round 2's: every catalog description edit is verified by
  re-running the real `_meaning_violations()`/`_synonym_offenders()`
  functions against the modified catalog before authoring, diffed fixed vs.
  introduced, never just checked for the one word first targeted.
