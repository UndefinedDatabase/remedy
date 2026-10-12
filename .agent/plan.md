# Plan — F058 Model failover chain

## Goal
Each role may carry a failover chain in `remedy.toml`; when its provider is unavailable after the
transport retries, the call walks the chain, every link held to the hard rules, and every
failed-over call discloses the intended and the used model in its evidence and in the run report
(docs/roadmap/features/T3_F058.md; DECISIONs F058 D1 to D5).

## Current Step
Round 8 on `feature/f058-model-failover-chain`, session 4: book round 7 (stopped after its evidence
job), merge `main` after pull request 331 into the branch in one merge commit, and repair the two
guards that merge turns red, R-1264 (the structure ratchet, a structural step) and R-1265 (the
`--host` help's retired word), per DECISION F058 D5.

## Next Steps
1. The closure again from its suite: the feature's one full suite on the merged tree, replacing
   `.agent/authored/f058-closure-suite.txt` at the same path (amend0921-operator-feedback rule 1),
   its CPU cost, then the staging reclaim, the evidence job and the review package on the new head.
2. The closing round: the Built State's closure paragraph, the ledger rotation, the self-use entry
   SU-059's `consumed_by`, the STATUS flip with the README sync, and the pull request, left
   unmerged until the next feature's Open PR Gate.

## Risks
- The evidence selection must hold no parameter id the packaging scan reads as unsafe.
- R-1235, R-1246, R-1251 and R-1252 are owned by F306.
