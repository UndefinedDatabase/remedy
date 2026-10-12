# Plan — F058 Model failover chain

## Goal
Each role may carry a failover chain in `remedy.toml`; when its provider is unavailable after the
transport retries, the call walks the chain, every link held to the hard rules, and every
failed-over call discloses the intended and the used model in its evidence and in the run report
(docs/roadmap/features/T3_F058.md; DECISIONs F058 D1 to D5).

## Current Step
Round 10 on `feature/f058-model-failover-chain`, session 4, the closing round: book round 9, the
Built State's closure paragraph, the ledger rotation, the STATUS flip with the README sync and the
self-use entry SU-059's `consumed_by`, then the pull request, left unmerged.

## Next Steps
1. The next session's Open PR Gate merges F058's pull request; then Rule A5 claims the next
   unchecked line of `docs/roadmap/STATUS.md`.

## Risks
- R-1235, R-1246, R-1251 and R-1252 are owned by F306.
