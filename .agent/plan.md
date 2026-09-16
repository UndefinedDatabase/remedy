# Plan — F280 CLI vocabulary v2, part two

Branch: feature/f280-cli-vocabulary-v2-part-two, cut from `main` at
`9f1b6d250e68fb5ee3a2dd39d0a8ffef3eef0792`, the merge commit of pull request 251.

## Goal

Finish what F261 could not reach: the catalog `apps/cli/command_catalog.py` equals DECISION
amend0905-vocab D4 apart from the words D4 gives F268, F269 and F273, and the help surface of
T002 holds, per `docs/roadmap/features/T2_F280.md`.

## Current Step

ROUND 6 books rounds 4 and 5's combined PASS and registers R-0937, then deletes `job create`: its
catalog entry, its dispatch row, the two dangling `related=` references to it, its own
catalog-count and help tests, the four production "create a new job" hint strings that named it,
and the docs pages that advertised it as a live command. `_cmd_create_job` itself is kept, now
reached only by tests and by the smoke script, matching the pattern R-0932 and R-0936 already
recorded for other handlers this feature left behind.

## Next Steps

1. `propose`, with the DECISION on the two surviving gates DECISION F261 D22 names.
2. The `flight_plan` rename; `worker doctor` and `job run --tasks`.
3. `job attach-repo` and `job permit`, only once a DECISION gives the repository attach and the
   capability grants another writer, as DECISION F280 D4 requires.
4. T002, which also re-derives the root help's quick start with the README quickstart (R-0895)
   and closes the flag scanner's blind spot (R-0934).

## Risks

- 127 findings are open by distinct id after this round's record; three are High, R-0803,
  R-0804 and R-0807, none of them this feature's.
- R-0899 (open, owned F273): section 3 of `scripts/remedy_smoke.sh` reads a `state` key `job show`
  does not print, so its planned-state check fails wherever the script is actually run.
- R-0937 (open, owned F273): five comment/message lines in `tests/test_remedy_smoke_script.py`
  still name the retired `--task-type`/`--task-description` flags.
- `job attach-repo` and `job permit` are the only command-line writers of a job's repository
  and of its test and revert grants, so the Acceptance line naming them cannot hold until a
  later DECISION supplies a writer.
- R-0935: the run contract never inherits a job's F018 token and wall-clock budgets, so what
  `job budget <id> set` writes into the contract is not overwritten by them either.
