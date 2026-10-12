# Plan — F058 Model failover chain

## Goal
Each role may carry a failover chain in `remedy.toml`; when its provider is unavailable after the
transport retries, the call walks the chain, every link held to the hard rules, and every
failed-over call discloses the intended and the used model in its evidence and in the run report
(docs/roadmap/features/T3_F058.md; DECISIONs F058 D1 to D5).

## Current Step
Round 9 on `feature/f058-model-failover-chain`, session 4, the closure again from its suite after
the merge of `main`: book round 8 (PASS, R-1264 and R-1265 resolved), the feature's one full suite
on the merged tree replacing `.agent/authored/f058-closure-suite.txt` at the same path
(amend0921-operator-feedback rule 1) with its CPU cost, then the staging reclaim, the evidence job
on the accepted head and the review package (`docs/roadmap/STATUS_closure_protocol.md` algorithm
steps 1 and 2).

## Next Steps
1. The closing round: the Built State's closure paragraph, the ledger rotation, the self-use entry
   SU-059's `consumed_by`, the STATUS flip with the README sync, and the pull request, left
   unmerged until the next feature's Open PR Gate.

## Risks
- A red suite stops the round; its repair is the next round's.
- R-1235, R-1246, R-1251 and R-1252 are owned by F306.
