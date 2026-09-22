# Plan — F283 Machine contracts, part two: the refusal sweep, the JSON gap and the exit-code taxonomy

Branch: feature/f283-machine-contracts-part-two, cut from `main` at
`d0d40e89`, the merge commit of pull request 263 (F277's closure).

## Goal

Every CLI refusal answers a machine in the envelope, the
read-only-without-`supports_json` set becomes empty, and every exit code in use
is documented and asserted from the catalog
(`docs/roadmap/features/T2_F283.md`).

## Current Step

ROUND 9. It books round 8's PASS and the `Done:` lines of R-1019 and R-1025,
and records DECISION F283 D4. Then, one commit each: the `project` group's
refusal pairs move onto `fail()`, its uppercase `ERROR: ` sites included
under D4; and the three `do` refusals round 8 correctly declined — the
contract-template lookup in `_cmd_do`, the run lookup in `_cmd_run_show` and
the list-option refusal in `_cmd_run_list` — move with the tests that pinned
their old `--json` shape.

## Next Steps

1. `_cmd_do_order`'s failure line, which follows a result document already
   printed under `--json`: the result document itself takes the envelope.
2. The remaining groups largest first — `grouped`, `test_cmds`, then the
   tail; `runtime_cmd.py` is its own round.
3. T001's catalog half, then T002's taxonomy and sweep.

## Risks

Twenty-two findings are open and none is this feature's own. The refusal
pairs left are several sessions of work, so the soft limit of 7 sessions and
25 rounds is the number to watch.
