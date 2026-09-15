# Plan — F261 CLI vocabulary v2 (rename & prune)

Branch: feature/f261-cli-vocabulary-v2, cut from `main` at
`7cdde89b5d0dc8ef1fb96980105870e956699873`, the merge commit of pull request 250.

## Goal

The catalog `apps/cli/command_catalog.py` equals DECISION amend0905-vocab D4: one name per
command, and every retired word deleted rather than aliased, per
`docs/roadmap/features/T2_F261.md`.

## Current Step

ROUND 13 opens T003. It books round 12's PASS, records DECISION F261 D12 and writes
`.agent/f261_t003_inventory.md`, then gives `GroupDef` a `hidden` field that keeps a group out
of both root helps and renames the `plan` group to the hidden `roadmap` group, one table per
commit.

## Next Steps

1. T003's deletion rounds in the order `.agent/f261_t003_inventory.md` proposes, each
   re-measured before it is authored, beginning with `orchestrator`, `rollback` and the `loop`
   command.
2. The prunes of `do`, `job`, `mission` and `worker`, the `--builder` and `--reviewer` flags
   with R-0767 and R-0894, `teach` to `teacher`, the `settings` alias and the `flight_plan`
   rename, with R-0900.
3. T004.

## Risks

- 97 findings are open by distinct id before and after this round's record; three are High,
  R-0803, R-0804 and R-0807.
- The inventory proposes sixteen rounds after this one, past F261's soft limit of 25 rounds;
  the session that reaches the limit owes the scope report and the split-and-close default.
- `job show` prints JSON that the canary, `tests/cli/test_plan_approval.py` and
  `scripts/remedy_smoke.sh` parse, so every change to it only adds keys.
