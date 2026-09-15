# Plan — F261 CLI vocabulary v2 (rename & prune)

Branch: feature/f261-cli-vocabulary-v2, cut from `main` at
`7cdde89b5d0dc8ef1fb96980105870e956699873`, the merge commit of pull request 250.

## Goal

The catalog `apps/cli/command_catalog.py` equals DECISION amend0905-vocab D4: one name per
command, and every retired word deleted rather than aliased, per
`docs/roadmap/features/T2_F261.md`.

## Current Step

ROUND 4 books round 3's PASS, registers R-0894 and R-0895, records DECISION F261 D3, the
deletion paragraph of `do job-plan` and `do plan`, and deletes the two commands in two commits,
each applying a table the round saves under `.agent/authored/` and adding its id to the
deleted-command guard. That finishes T001 as DECISION F261 D1 re-scoped it.

## Next Steps

1. T002: `apply` replaces `promote` in code, catalog and docs, `do promote` joins `job apply`,
   and `job show --full` absorbs the read commands and `do job-report`.
2. T003, the prune to D4, which also removes `do run`'s `--scope-file` and `--approve-scope`
   with the scope-plan writer, as R-0894 records.
3. T004: descriptions, role labels, help wrapping, the catalog tests, and the README Quickstart
   re-derived from the catalog, as R-0895 records.
4. The integration gate, then the closure sequence.

## Risks

- 94 findings are open by distinct id once this round's record lands; four are High, R-0803,
  R-0804, R-0806 and R-0807, all owned by F273.
- A deleted `do` word falls through to the `do` goal entry, and for `do plan` that entry starts
  a job; DECISION F261 D3 records the measured effect beside D1's fifth ruling.
- No command writes the root artifacts a provider-run review package needs, which R-0892
  records for F268.
