# Plan — F280 CLI vocabulary v2, part two

Branch: feature/f280-cli-vocabulary-v2-part-two, cut from `main` at
`9f1b6d250e68fb5ee3a2dd39d0a8ffef3eef0792`, the merge commit of pull request 251.

## Goal

Finish what F261 could not reach: the catalog `apps/cli/command_catalog.py` equals DECISION
amend0905-vocab D4 apart from the words D4 gives F268, F269 and F273, and the help surface of
T002 holds, per `docs/roadmap/features/T2_F280.md`.

## Current Step

ROUND 4 books round 3's PASS with the resolutions of R-0906 and R-0909, then moves the four test
fixtures and the smoke script's job-creation step off the `job create` CLI word by one table: each
now calls `_cmd_create_job` directly, in-process inside its own subprocess, rather than through
`apps.cli.main`'s dispatch, so deleting `job create` in a later round breaks none of them. No
catalog entry, no dispatch table row and no surviving command's behaviour changes; only test and
tooling wiring moves, so this round needs no DECISION.

## Next Steps

1. `job create` is the next word to delete, with its hints, now that only its own tests and the
   catalog dispatch table still name it.
2. `propose`, with the DECISION on the two surviving gates DECISION F261 D22 names.
3. The `flight_plan` rename; `worker doctor` and `job run --tasks`.
4. `job attach-repo` and `job permit`, only once a DECISION gives the repository attach and the
   capability grants another writer, as DECISION F280 D4 requires.
5. T002, which also re-derives the root help's quick start with the README quickstart (R-0895)
   and closes the flag scanner's blind spot (R-0934).

## Risks

- 126 findings are open by distinct id after this round's record; three are High, R-0803,
  R-0804 and R-0807, none of them this feature's.
- R-0899 (open, owned F273): section 3 of `scripts/remedy_smoke.sh` reads a `state` key `job show`
  does not print, so its planned-state check fails wherever the script is actually run. This
  round's table changes the same section's job-creation line only, for the `job create` word; it
  does not touch the broken key and does not repair R-0899.
- `job attach-repo` and `job permit` are the only command-line writers of a job's repository
  and of its test and revert grants, so the Acceptance line naming them cannot hold until a
  later DECISION supplies a writer.
- R-0935: the run contract never inherits a job's F018 token and wall-clock budgets, so what
  `job budget <id> set` writes into the contract is not overwritten by them either.
