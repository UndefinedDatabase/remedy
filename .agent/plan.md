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

ROUND 4. C1 books round 3's PASS and re-points `.agent/plan.md`. C2 clears the
full "Order" bucket in one edit (the shared `_LIST_DESC_ARG` constant's help
text, referenced by all 12 `--desc` list-sort flags, fixes all 12 occurrences
at once — a stronger leverage point than the per-command edits every prior
round used) plus 8 of the 9 "Task" bucket violations (`brain.continue
--task-type`, `job.context --task` via the shared `_TASK_OPT` constant,
`job.run --max-rounds`, `job.run --repair-rounds`, `job.show --full`,
`job.context`'s own description, `mission.continue`'s own description,
`self.execute --job-id`, `self.execute proposed_task_id`) — 22 total
(1 shared-constant Order fix covering 12 sites, plus 9 Task-word edits,
plus one more the diff found as a side effect), zero introduced.

`command:stats.bench:description`'s Order AND Run violations are DELIBERATELY
LEFT OPEN this round: its text — "a regression warning naming the order and
both numbers" — uses "order" in the sense of a trend/regression's
mathematical order (its degree), not DECISION amend0905-vocab D1's Order
concept (what the human gave Remedy), and "runs" the same way ("the last
run" is a bench execution, correctly the Run concept, but "Never runs the
bench" is a verb use with no natural home for a fragment). Forcing either
concept's fragment into a sentence about regression math would misdescribe
the command. This is the same class of finding as DECISION F281 D2's two
floor items — a genuine word-sense collision — but is NOT yet formalized as
its own DECISION; a future round either writes one (accepting `stats.bench`
as a second permanent floor item, or finding an honest rewording this
session didn't) or clears it with a rewrite that actually works.

## Next Steps

1. Re-run `_meaning_violations()` grouped by word at the start of round 5;
   expected counts after this round: Task 0 or 1 (`stats.bench` may remain),
   Order 0 or 1 (`stats.bench`'s own Order violation, same caveat), Evidence
   12, Mission 16, Run ~29 (stats.bench's Run violation may still count),
   Project 65, Job ~120 — 245 total (measured directly by this round's own
   dry run; re-measure rather than trust this arithmetic). Take the
   next-smallest bucket.
2. When a bucket's violations share a single catalog-module CONSTANT (like
   `_LIST_DESC_ARG` or `_TASK_OPT` this round), fixing the constant once
   clears every command that references it — check for this BEFORE writing
   N per-command edits; it is faster and structurally guarantees no site is
   missed or drifts from its siblings.
3. Help wrap, `doctor core` dead-commands (D11d), the D11a catalog
   group-reach test, the visible-order data-pinned test, the F259 enforced
   flip (bounded by DECISION F281 D2's two-item floor, possibly a third if
   `stats.bench` becomes one), and the README quickstart's R-0895 line
   remain entirely undone.

## Risks

- Same as rounds 2-3: every catalog description edit is verified by
  re-running the real `_meaning_violations()`/`_synonym_offenders()`
  functions against the modified catalog before authoring, diffed fixed vs.
  introduced.
- A word can appear in the catalog in a sense DECISION amend0905-vocab D1
  does not define (`stats.bench`'s mathematical "order"; possibly others
  waiting in the Job/Project/Run buckets, which are large enough that a
  false-positive-sense collision is likely) — when a fragment cannot be
  added without misdescribing the command, the violation is LEFT OPEN and
  named, never forced.
