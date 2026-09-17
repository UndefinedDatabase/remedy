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

ROUND 8. C1 books round 7's PASS and re-points `.agent/plan.md`. C2 clears 33
of the 65 Project-bucket violations via FOUR shared-literal edits: the
`_PROJECT_SCOPE_OPT` constant (21 call sites — `job.list`, `teacher.ask`, all
11 `mission.*` commands, and all 7 `stats.*` commands that take a `--project`
option), the "Project slug or UUID" literal (3 sites: `project.current`,
`project.attach`, `project.adopt`), the "Project UUID scope" literal (3
sites: `memory.store`, `memory.recall`, `memory.list`), and the "Project ID
scope" literal (6 sites: the six `memory.card-*` commands).

After this round: Order remains 1 (`stats.bench`, unchanged), Mission, Task,
Evidence, Decision and Run all read 0. Project drops from 65 to 32 — the
remaining text is unique per command: `do.run`'s own `--project` ArgDef,
`init.run`'s `--project-name`, most of the `project.*` group's own
descriptions and `project_id` ArgDefs, `runtime.*`'s `--repo` ArgDefs,
`brain.*`'s descriptions, `status.run`'s description, `job.list`'s own
description, `stats.backfill-ledger`'s own description, and the `brain`,
`memory`, `runtime`, `status` and `test` group descriptions. Job stays at 118
— untouched this round, still the largest remaining bucket.

## Next Steps

1. Re-run `_meaning_violations()` grouped by word at the start of round 9;
   expected: Project (~32) and Job (~118) are the only two buckets left
   (plus Order's 1 unfixed `stats.bench` collision), at approximately 150-151
   total (re-measure rather than trust). Job is now by far the largest;
   continue looking for shared constants there first (the many `job_id`
   ArgDefs are the obvious candidate) before writing per-command edits.
2. This session (session 1 of F281) has now run 8 delegated rounds, at the
   TOP of the operator's 6-to-8 target (amend0905-throughput). The session's
   own honest assessment governs whether it continues (context comfortably
   sufficing) or ends with a handoff; either is legitimate.
3. Help wrap, `doctor core` dead-commands (D11d), the D11a catalog
   group-reach test, the visible-order data-pinned test, the F259 enforced
   flip (bounded by DECISION F281 D2's two-item floor, possibly `stats.bench`
   as a third), and the README quickstart's R-0895 line remain entirely
   undone — none of T001's non-description work has started yet.

## Risks

- Same as rounds 2-7: every catalog description edit is verified by
  re-running the real `_meaning_violations()`/`_synonym_offenders()`
  functions against the modified catalog before authoring, diffed fixed vs.
  introduced.
- The Job bucket (~118) likely contains many shared constants (the repeated
  `job_id`/`Job ID` ArgDefs across dozens of commands) and many genuinely
  distinct descriptions; it will need several rounds and careful checking
  for the "fragment is itself a binding word" and "same word, different
  sense" traps this feature has already found twice.
