# Plan — F058 Model failover chain

## Goal
Each role may carry a failover chain in `remedy.toml`; when its provider is unavailable after the
transport retries, the call walks the chain, every link held to the hard rules, and every
failed-over call discloses the intended and the used model in its evidence and in the run report
(docs/roadmap/features/T3_F058.md; DECISION F058 D1).

## Current Step
Round 1 on `feature/f058-model-failover-chain`, session 1: claim F058, book F206's round 6, the
structural step that moves the model routing keys out of `packages/orchestration/config.py`, and
T001, the chains' key, parse and hard-rule validation in `packages/orchestration/model_failover.py`.

## Next Steps
1. T002: the failover walk where a run builds its providers, its disclosure in each call's
   evidence and the run report's line, with the down-primary and exhausted-chain fixtures.
2. T003: the trigger discipline, the sticky cooldown on an injected clock, and the session guard.
3. The closure sequence.

## Risks
- `packages/orchestration/pingpong_loop.py` and its `run_pingpong` are rows of
  `docs/system/structure-ledger-v1.md` that may not grow; T002 needs a door out of them first.
- R-1235, R-1246, R-1251 and R-1252 are owned by F306.
