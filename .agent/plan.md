# Plan — F280 CLI vocabulary v2, part two

Branch: feature/f280-cli-vocabulary-v2-part-two, cut from `main` at
`9f1b6d250e68fb5ee3a2dd39d0a8ffef3eef0792`, the merge commit of pull request 251.

## Goal

Finish what F261 could not reach: the catalog `apps/cli/command_catalog.py` equals DECISION
amend0905-vocab D4 apart from the words D4 gives F268, F269 and F273, and the help surface of
T002 holds, per `docs/roadmap/features/T2_F280.md`.

## Current Step

ROUND 3 books round 2's PASS with the resolutions of R-0767 and R-0894, registers R-0935 and
R-0936, and records DECISIONs F280 D3 and D4. Its first table builds `job budget <id> set` over
the run contract's budget fields and the token budget profile (R-0906, R-0909); its second deletes
`job fulfill`. D4 defers `job attach-repo` and `job permit`. The worker runs the suite once.

## Next Steps

1. The fixtures and smoke sections moved off `job create`, then `job create` with its hints; the
   next record books round 3's verdict with the resolutions of R-0906 and R-0909.
2. `propose`, with the DECISION on the two surviving gates DECISION F261 D22 names.
3. The `flight_plan` rename; `worker doctor` and `job run --tasks`.
4. `job attach-repo` and `job permit`, only once a DECISION gives the repository attach and the
   capability grants another writer, as DECISION F280 D4 requires.
5. T002, which also re-derives the root help's quick start with the README quickstart (R-0895)
   and closes the flag scanner's blind spot (R-0934).

## Risks

- 128 findings are open by distinct id after this round's record; three are High, R-0803,
  R-0804 and R-0807, none of them this feature's.
- `job attach-repo` and `job permit` are the only command-line writers of a job's repository
  and of its test and revert grants, so the Acceptance line naming them cannot hold until a
  later DECISION supplies a writer.
- R-0935: the run contract never inherits a job's F018 token and wall-clock budgets, so what
  `job budget <id> set` writes into the contract is not overwritten by them either.
