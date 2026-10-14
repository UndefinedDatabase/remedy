# Context — amend1014-do-golden-path-now

## Active Branch
feature/do-golden-path, from `main` at `e688b30f3`. F078 is parked on feature/f078-autonomy-levels.

## Scope
`remedy do` only: lane classifier, plan normalization, progress, cockpit order, `--run-unattended`,
scope guard, docs. No planner rewrite, no data-model change, no UI redesign.

## Do not touch
`no_file_changed`, apply approval, repository isolation, non-human content policy; F078's files.

## Constraints
- Structure ratchet: `plan_order_job`, `_cmd_do_order`, `_cmd_do` and `do_cmd.py` may not grow
  (this branch lowered three rows); `do_sequence.py` stays under 1000 lines.
- One test run at a time (`scripts/remedy_pytest.sh`); the full suite once at closure.

## Steps
The item-status table for the work lives in the handback, `.agent/handoff.md`; the commits C1 to C8
of this branch are its steps (D2, D6 prompt, D3, D1 with D6, D4 with D5, tests, docs, repair).
