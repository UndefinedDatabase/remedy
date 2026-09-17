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

ROUND 13. C1 books round 12's PASS (with a commit-message-slip note) and
re-points `.agent/plan.md`. C2 clears the 10 remaining Job-bucket ArgDefs
(`teacher.ask`'s `--job-id`, `job.stop`'s `--reason`, `brain.continue`'s
`--prompt`, `mission.continue`'s `next_step`, `stats.failures`'s and
`stats.report`'s `--job`, `stats.backfill-ledger`'s and
`stats.verify-ledger`'s `evidence_dir`, `self.inspect`'s and
`self.report`'s `--job-id`), each appending ", under its mission" or
"(under its mission)". `stats.bench`'s Order collision is DELIBERATELY left
unfixed — see the Goal section of this round's own block
(`.agent/authored/f281-r13.md`) for why: fixing it now, with
`_synonym_offenders()` still at 2, would empty `_meaning_violations()`
while `VOCABULARY_MODE` stays `"planned"`, and that mode's own test asserts
`violations != []`, so the suite would redden.

After this round: `_meaning_violations()` reads 1 — ONLY `stats.bench`'s
Order collision remains in the entire catalog. `_synonym_offenders()`
remains at 2 (`dev.agent-loop`'s command_id and `do.run --fixture-builder`'s
description — DECISION F281 D2's two-item floor, tracked since round 2).

## Next Steps

1. Re-run `_meaning_violations()` and `_synonym_offenders()` at the start
   of round 14 to confirm 1 and 2 respectively (re-measure rather than
   trust). Round 14 (or whichever round resolves DECISION F281 D2's two
   synonym sites) should land THREE things together, in one round, so the
   suite never sits in a state where fixing one breaks the other: (a) the
   `stats.bench` Order reword ("the order and both numbers" → "the sequence
   and both numbers", already drafted and dry-run-verified in round 13's
   own authoring — see `.agent/authored/f281-r13.md`'s Goal section for the
   exact FROM/TO), (b) the two synonym-offender fixes DECISION F281 D2
   names, and (c) the `VOCABULARY_MODE` flip from `"planned"` to
   `"enforced"` plus BOTH mode-dependent tests' assertions re-verified
   against the real, post-flip catalog before committing.
2. Session 2 of F281 is now 5 delegated rounds in (rounds 9-13), within the
   6-to-8 target (amend0905-throughput). Consider ending this session with
   a handoff after round 13, since round 14 is qualitatively different work
   (the mode flip, needs its own careful reading of DECISION F281 D2 and
   the two synonym sites) — a natural session boundary, not a stall.
3. Four lessons carried from rounds 9-12 (see `.agent/prose_slips.md`): a
   G5 sweep counts the LITERAL text actually written, never the violation
   count credited to a shared-constant edit; a worker never reports a gate
   as PASS from stale memory — G6 is re-run and re-read literally as the
   LAST action before the handback; a C1 commit's subject line is composed
   fresh, never copied from a previous round's template; and a
   mode-dependent test's assertion direction must be read in FULL before
   predicting whether a round's edit turns it red or green (round 13's own
   reviewer caught this before authoring, not after a red gate).

## Risks

- The final Job/Order/synonym convergence (round 14, per Next Steps 1) is a
  three-part atomic change: reword `stats.bench`, fix the 2 synonym sites,
  and flip `VOCABULARY_MODE` — all three land together or the suite reddens
  in one direction or the other. Read DECISION F281 D2 fresh before drafting
  that round; do not assume its two-item floor's exact fix is still what it
  was when D2 was written in round 2.
