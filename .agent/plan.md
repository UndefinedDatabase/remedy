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

ROUND 12. C1 books round 11's PASS and re-points `.agent/plan.md`. C2
clears all 31 remaining Job-bucket command descriptions via 31 single-
occurrence FROM/TO edits (`job.show`, `teacher.narrate`, `job.attach-repo`,
`job.stop`, `project.attach-job`, `project.adopt`, `patch.list`,
`snapshot.create`, `brain.context`, `brain.trust`, `brain.timeline`,
`brain.cockpit`, `brain.continue`, `brain.constitution`,
`mission.readiness`, `memory.learn`, `memory.candidates`, `change.list`,
`event.list`, `event.timeline`, `event.replay`, `job.checkpoints`,
`blocker.list`, `decision.list`, `decision.explain`, `ui.start`, `ui.open`,
`job.evidence`, `job.apply`, `dev.agent-loop`, `snapshot.list-applies`),
each appending ", under its mission" or "(under its mission)" naturally
into the existing sentence.

After this round: Order remains 1 (`stats.bench`, unchanged), Project
remains 0 (fully cleared, round 11). Job drops from 41 to 10 — the
remaining text is the 10 still-unique `--job`/`--job-id`/`evidence_dir`
ArgDefs first named in round 9's plan: `teacher.ask`, `job.stop`'s own
`--reason`, `brain.continue`'s `--prompt`, `mission.continue`'s
`next_step`, `stats.failures`'s and `stats.report`'s own `--job` texts,
`stats.backfill-ledger`'s and `stats.verify-ledger`'s `evidence_dir`
ArgDefs, and `self.inspect`'s and `self.report`'s `--job-id` texts.

## Next Steps

1. Re-run `_meaning_violations()` grouped by word at the start of round 13;
   expected: Job (10) and Order (1, `stats.bench`) are the ONLY two
   remaining violations in the entire catalog, at 11 total (re-measure
   rather than trust). Round 13 can plausibly clear all 11 in one round —
   10 distinct ArgDef edits plus one `stats.bench` fix — bringing
   `_meaning_violations()` to 0 and `VOCABULARY_MODE` closer to flippable
   (still gated on `_synonym_offenders()` reaching 0 too, which needs the
   2 remaining synonym sites from `dev.agent-loop`'s command_id and
   `do.run --fixture-builder`'s description, tracked since round 2 —
   DECISION F281 D2's two-item floor).
2. Session 2 of F281 is now 4 delegated rounds in (rounds 9-12), at the
   floor of the 6-to-8 target (amend0905-throughput); continue toward 6-8
   if context allows.
3. Help wrap, `doctor core` dead-commands (D11d), the D11a catalog
   group-reach test, the visible-order data-pinned test, the F259 enforced
   flip (bounded by DECISION F281 D2's two-item floor, possibly `stats.bench`
   as a third), and the README quickstart's R-0895 line remain entirely
   undone — none of T001's non-description work has started yet. Once the
   description sweep reaches 0, these become the dominant remaining scope.

## Risks

- Same as rounds 2-11: every catalog description edit is verified by
  re-running the real `_meaning_violations()`/`_synonym_offenders()`
  functions against the modified catalog before authoring, diffed fixed vs.
  introduced, including a check for newly introduced violations in any
  OTHER bucket (round 11's lesson).
- The remaining 10 Job-bucket ArgDefs are all distinct per-site text with
  no shared literal; the `stats.bench` Order collision needs its own
  reading (round 4's plan already named it but never fixed it — its exact
  current text needs re-reading before round 13 drafts a fix).
