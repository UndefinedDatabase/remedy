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

ROUND 11. C1 books round 10's PASS (with a process-defect note) and
re-points `.agent/plan.md`. C2 clears the Project bucket's remaining 18
violations via 18 single-occurrence FROM/TO edits: 14 command descriptions
(`status.run`, `job.list`, `project.create`, `project.show`,
`project.attach-job`, `project.brain`, `project.context`,
`project.summary`, `project.current`, `project.adopt`, `brain.graph`,
`brain.constitution`, `stats.backfill-ledger`, `runtime.serve`) and 4 ArgDef
help strings (`do.run`'s `--project`, `init.run`'s `--project-name`,
`project.create`'s `--description` and `name`).

After this round: Order remains 1 (`stats.bench`, unchanged), Project reads
0 — FULLY CLEARED. Job remains 41 — untouched this round, now the ONLY
bucket besides `stats.bench`'s lone Order collision.

## Next Steps

1. Re-run `_meaning_violations()` grouped by word at the start of round 12;
   expected: Job (~41) is the only substantial bucket left (plus Order's 1
   unfixed `stats.bench` collision), at approximately 42 total (re-measure
   rather than trust). The remaining Job items are the 10 still-unique
   `--job`/`--job-id`/`evidence_dir` ArgDefs and 31 command descriptions
   named in round 9's plan entry — entirely located, per-command prose.
2. Session 2 of F281 is now 3 delegated rounds in (rounds 9-11), still below
   the 6-to-8 target (amend0905-throughput); continue.
3. Help wrap, `doctor core` dead-commands (D11d), the D11a catalog
   group-reach test, the visible-order data-pinned test, the F259 enforced
   flip (bounded by DECISION F281 D2's two-item floor, possibly `stats.bench`
   as a third), and the README quickstart's R-0895 line remain entirely
   undone — none of T001's non-description work has started yet.
4. Two lessons carried from rounds 9-10 (see `.agent/prose_slips.md`): a G5
   sweep counts the LITERAL text actually written, never the violation
   count credited to a shared-constant edit; and a worker never reports a
   gate as PASS from stale memory — G6 in particular is re-run and re-read
   literally as the LAST action before the handback is written.
5. A per-site prose edit for a binding word can introduce a NEW violation in
   a DIFFERENT word's bucket if the new text happens to contain another
   binding word (e.g. "mission") without that word's OWN meaning fragment
   (round 11's own dry-run caught exactly this on a first draft of the
   `project.show` edit, before it was ever authored into a block — the
   corrected edit avoids the word "mission" entirely). Every future
   per-site edit is re-measured with the FULL `_meaning_violations()` sweep,
   not just a check that the target violation cleared.

## Risks

- Same as rounds 2-10: every catalog description edit is verified by
  re-running the real `_meaning_violations()`/`_synonym_offenders()`
  functions against the modified catalog before authoring, diffed fixed vs.
  introduced — this now explicitly includes checking for NEWLY INTRODUCED
  violations in a bucket other than the one being edited (see Next Steps 5).
- The remaining Job bucket (~41) is entirely located, per-command prose;
  expect several more rounds of smaller, careful edits, with continued
  vigilance for the "fragment is itself a binding word" and "same word,
  different sense" traps this feature has already found multiple times.
