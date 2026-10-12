# Plan — F058 Model failover chain

## Goal
Each role may carry a failover chain in `remedy.toml`; when its provider is unavailable after the
transport retries, the call walks the chain, every link held to the hard rules, and every
failed-over call discloses the intended and the used model in its evidence and in the run report
(docs/roadmap/features/T3_F058.md; DECISIONs F058 D1 to D3).

## Current Step
Round 3 on `feature/f058-model-failover-chain`, session 2: C1-C6 plus one gate-3 fix commit
landed — booked round 2's verdict (PASS, R-1259 and R-1260 registered, R-1257 and R-1258
resolved), repaired both, moved the per-call record helpers out of
`packages/orchestration/pingpong_loop.py` into `packages/orchestration/pingpong_call_record.py`
and the `run` handlers out of `apps/cli/commands/do_cmd.py` into
`apps/cli/commands/run_report_cmd.py` (both structural), and landed the rest of T002: a
failed-over call's disclosure in the run's record, the `remedy run show` report line, and the
fixtures through a real run for a primary that is down and a chain that runs out. All six gates
passed after the fix commit.

## Next Steps
1. The next round's first commit books round 3's verdict.
2. T003: the trigger discipline as negative tests through a run, the sticky cooldown on an
   injected clock, and the session guard.
3. The documentation page for model failover, registered in `docs/README.md`.
4. The closure sequence.

## Risks
- `run_pingpong`, `export_pingpong_json` and `_call_with_retry` are rows of
  `docs/system/structure-ledger-v1.md` that may not grow; T003's cooldown and guard sit in the
  walk and the factory, not in them.
- R-1235, R-1246, R-1251 and R-1252 are owned by F306.
