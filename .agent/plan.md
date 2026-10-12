# Plan — F058 Model failover chain

## Goal
Each role may carry a failover chain in `remedy.toml`; when its provider is unavailable after the
transport retries, the call walks the chain, every link held to the hard rules, and every
failed-over call discloses the intended and the used model in its evidence and in the run report
(docs/roadmap/features/T3_F058.md; DECISIONs F058 D1 and D2).

## Current Step
Round 2 on `feature/f058-model-failover-chain`, session 2: book round 1's verdict (FAIL, R-1257
and R-1258 owned by F058), repair both, move the construction of a role's provider out of
`packages/orchestration/pingpong_loop.py` into `packages/orchestration/role_provider_factory.py`
(structural), and land the first part of T002: the failover walk in
`packages/orchestration/model_failover.py`, wired where a run builds its providers, with tests.

## Next Steps
1. The rest of T002: each failed-over call's disclosure in the run's provider evidence, the run
   report's line, and the fixtures for a primary that is down and a chain that is exhausted.
2. T003: the trigger discipline as negative tests through a run, the sticky cooldown on an
   injected clock, and the session guard.
3. The closure sequence.

## Risks
- `packages/orchestration/pingpong_loop.py`, `run_pingpong` and `_build_provider_evidence` are
  rows of `docs/system/structure-ledger-v1.md` that may not grow; the disclosure needs a door out
  of them first.
- R-1235, R-1246, R-1251 and R-1252 are owned by F306.
