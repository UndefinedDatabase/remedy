# Plan — F058 Model failover chain

## Goal
Each role may carry a failover chain in `remedy.toml`; when its provider is unavailable after the
transport retries, the call walks the chain, every link held to the hard rules, and every
failed-over call discloses the intended and the used model in its evidence and in the run report
(docs/roadmap/features/T3_F058.md; DECISIONs F058 D1 to D4).

## Current Step
Round 4 on `feature/f058-model-failover-chain` landed: round 3's verdict booked (PASS, R-1261
registered, R-1259 and R-1260 resolved), R-1261 repaired, `parked_session_refs` moved out of
`packages/orchestration/pingpong_loop.py`, and T003: the cooldown key and the sticky window on an
injected clock, the session guard, and the three non-triggers proved through a run. Awaiting the
reviewer's verdict on round 4.

## Next Steps
1. The documentation page for model failover, registered in `docs/README.md`, with the closure's
   integration gate: the feature's one full suite.
2. The closure's evidence round and its closing round, per
   `docs/roadmap/STATUS_closure_protocol.md`.

## Risks
- `run_pingpong`, `export_pingpong_json` and `_call_with_retry` are rows of
  `docs/system/structure-ledger-v1.md` that may not grow; the cooldown and the guard live in the
  walk, the factory and `pingpong_call_record.py`.
- R-1235, R-1246, R-1251 and R-1252 are owned by F306.
