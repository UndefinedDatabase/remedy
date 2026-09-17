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

ROUND 5. C1 books round 4's PASS and re-points `.agent/plan.md`. C2 clears the
full "Evidence" bucket (12 of 12: `group:stats:description`,
`group:self:description`, `arg:job.stop:--reason:description`,
`command:mission.report:description`, `command:mission.abandon:description`,
`arg:job.run:--no-stream-evidence:description`,
`arg:stats.failures:--job:description`,
`arg:stats.backfill-ledger:evidence_dir:description`,
`command:stats.verify-ledger:description`,
`arg:stats.verify-ledger:evidence_dir:description`,
`command:self.inspect:description`, `command:self.report:description`) plus
one side-effect fix (`mission.report`'s Job violation, since its rewrite
already needed the word "mission" nearby, which is one of Job's own three
fragments) — 13 total, zero introduced.

After this round the ONLY remaining Order violation is `stats.bench`'s
(unfixed, per round 4's note — mathematical "order", not the vocabulary
concept), and Task and Evidence both read zero.

## Next Steps

1. Re-run `_meaning_violations()` grouped by word at the start of round 6;
   expected counts after this round: Mission 16 (unchanged — none of this
   round's fixes touched a standalone Mission violation), Order 1
   (`stats.bench`, unfixed), Run ~29-30, Project 65, Job ~120 — 232 total
   (measured directly this round; re-measure rather than trust). Take the
   next-smallest bucket (Mission, 16, unless a fresh measurement disagrees).
2. Continue watching for the "fragment is itself a binding word" trap
   (Mission's own fragments are order/job/contract — all three ARE binding
   words) and the "same word, different sense" trap (`stats.bench`'s
   mathematical order): every rewrite is checked against the FULL before/after
   diff of the real `_meaning_violations()`/`_synonym_offenders()` functions,
   never assumed safe from reading the text alone.
3. Help wrap, `doctor core` dead-commands (D11d), the D11a catalog
   group-reach test, the visible-order data-pinned test, the F259 enforced
   flip (bounded by DECISION F281 D2's two-item floor, possibly `stats.bench`
   as a third), and the README quickstart's R-0895 line remain entirely
   undone. This session (session 1 of F281) has now run 5 delegated rounds,
   at the operator's 4-to-5 default and approaching the 6-to-8 target; the
   next round may be this session's last if a natural stopping point is
   reached, per a session's own honest self-assessment rather than a fixed
   count.

## Risks

- Same as rounds 2-4: every catalog description edit is verified by
  re-running the real `_meaning_violations()`/`_synonym_offenders()`
  functions against the modified catalog before authoring, diffed fixed vs.
  introduced.
