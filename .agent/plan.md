# Plan — F280 CLI vocabulary v2, part two

Branch: feature/f280-cli-vocabulary-v2-part-two, cut from `main` at
`9f1b6d250e68fb5ee3a2dd39d0a8ffef3eef0792`, the merge commit of pull request 251.

## Goal

Finish what F261 could not reach: the catalog `apps/cli/command_catalog.py` equals DECISION
amend0905-vocab D4 apart from the words D4 gives F268, F269 and F273, and the help surface of
T002 holds, per `docs/roadmap/features/T2_F280.md`.

## Current Step

ROUND 2 books round 1's PASS, registers R-0932 to R-0934 and records DECISION F280 D2. Its three
table commits delete the ping-pong path of `do run` with the flags only it reads, delete the
scope plan module with `run_pingpong`'s scope branches, and turn argparse prefix matching off, so
no deleted flag survives as an abbreviation of a kept one. The worker runs the suite once.

## Next Steps

1. `job budget <id> set` over the run-contract budget fields and the token budget profile
   (R-0906, R-0909), then `job fulfill`; the next record books round 2's verdict with the
   resolutions of R-0767 and R-0894.
2. The fixtures and smoke sections moved off `job create`, then `job create`, `job attach-repo`
   and `job permit`.
3. `propose`, with the DECISION on the two surviving gates DECISION F261 D22 names.
4. The `flight_plan` rename; `worker doctor` and `job run --tasks`.
5. T002, which also re-derives the root help's quick start with the README quickstart (R-0895)
   and closes the flag scanner's blind spot (R-0934).

## Risks

- 128 findings are open by distinct id after this round's record; three are High, R-0803,
  R-0804 and R-0807, none of them this feature's.
- The quick start this round writes needs `remedy init` first and stops at the default autonomy
  level before any build, as DECISION F280 D2 records.
- Prefix matching is off for every command, so an operator's abbreviated flag now exits 2; the
  reviewer's scan found no abbreviated Remedy flag in the repository.
