# Plan — F058 Model failover chain

## Goal
Each role may carry a failover chain in `remedy.toml`; when its provider is unavailable after the
transport retries, the call walks the chain, every link held to the hard rules, and every
failed-over call discloses the intended and the used model in its evidence and in the run report
(docs/roadmap/features/T3_F058.md; DECISIONs F058 D1 to D4).

## Current Step
Round 6 on `feature/f058-model-failover-chain`, session 3, the closure's first round: book round
5's verdict (PASS, R-1263 registered, R-1262 resolved), repair R-1263, the checklist's
consolidation pass for F058, the closure's self-use item run to its approval gate and never
applied, and the feature's one full suite with its CPU cost
(`.agent/authored/f058-closure-suite.txt`).

## Next Steps
1. The evidence bundle and the review package, per `docs/roadmap/STATUS_closure_protocol.md`
   steps 1 and 2 (or a repair round naming every bad node id, if the suite is red).
2. The closing round: the Built State's closure paragraph, the ledger rotation, the STATUS line,
   the self-use queue's `consumed_by` and the pull request.

## Risks
- The self-use run makes real provider calls within the `self_use` role's budget.
- R-1235, R-1246, R-1251 and R-1252 are owned by F306.
