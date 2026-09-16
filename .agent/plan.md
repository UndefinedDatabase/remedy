# Plan — F280 CLI vocabulary v2, part two

Branch: feature/f280-cli-vocabulary-v2-part-two, cut from `main` at
`9f1b6d250e68fb5ee3a2dd39d0a8ffef3eef0792`, the merge commit of pull request 251.

## Goal

Finish what F261 could not reach: the catalog `apps/cli/command_catalog.py` equals DECISION
amend0905-vocab D4 apart from the words D4 gives F268, F269 and F273, and the help surface of
T002 holds, per `docs/roadmap/features/T2_F280.md`.

## Current Step

ROUND 8 books round 7's independently-reviewed PASS (Gate: F280 R7), fixes R-0939 (the missing
trailing newline round 7's C1 left in four `.agent/` files), and renames the `job run` flag
`--max-tasks` to `--tasks` (DECISION amend0905-vocab D4's `job run <id> [--tasks n]`), keeping the
internal `max_tasks` field name unchanged since D4 governs only the CLI surface.

## Next Steps

1. `worker doctor`, the other D4 word no feature owns yet (`worker list | show | resources |
   unload | status | doctor`): a read-only per-provider health check beside `doctor core`,
   reusing `list_worker_specs()` and the ollama/GPU probes `worker resources` already has.
2. `propose`, once operator question Q4 is answered.
3. The rest of the `flight_plan` rename DECISION F280 D5 deferred: the module
   `flight_plan.py` to `job_plan.py` (with `FlightPlanResult` and its lowercase function names),
   then the persisted job key, schema tag and decision-type literals, then the surviving
   English prose.
4. `job attach-repo` and `job permit`, only once a DECISION gives the repository attach and the
   capability grants another writer, as DECISION F280 D4 requires.
5. T002, which also re-derives the root help's quick start with the README quickstart (R-0895)
   and closes the flag scanner's blind spot (R-0934).

## Risks

- 128 findings are open by distinct id after this round's record (R-0939 is registered and
  resolved in the same commit, so the count is unchanged from round 7's); three are High,
  R-0803, R-0804 and R-0807, none of them this feature's.
- R-0899 (open, owned F273): section 3 of `scripts/remedy_smoke.sh` reads a `state` key `job show`
  does not print, so its planned-state check fails wherever the script is actually run.
- R-0937 (open, owned F273): five comment/message lines in `tests/test_remedy_smoke_script.py`
  still name the retired `--task-type`/`--task-description` flags. R-0938 (open, owned F280):
  round 6's own handback misreports one commit's insertion/deletion counts; nothing to fix.
- `job attach-repo` and `job permit` are the only command-line writers of a job's repository
  and of its test and revert grants, so the Acceptance line naming them cannot hold until a
  later DECISION supplies a writer.
- R-0935: the run contract never inherits a job's F018 token and wall-clock budgets, so what
  `job budget <id> set` writes into the contract is not overwritten by them either. Operator
  question Q4 is open: `propose`'s deletion (DECISION amend0905-vocab D4) is blocked on an answer.
