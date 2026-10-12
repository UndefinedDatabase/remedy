# Plan — F058 Model failover chain

## Goal
Each role may carry a failover chain in `remedy.toml`; when its provider is unavailable after the
transport retries, the call walks the chain, every link held to the hard rules, and every
failed-over call discloses the intended and the used model in its evidence and in the run report
(docs/roadmap/features/T3_F058.md; DECISIONs F058 D1 to D4).

## Current Step
Round 7 on `feature/f058-model-failover-chain`, session 3, the closure's evidence round: book
round 6's verdict (PASS, R-1263 resolved, the recurrence of R-1252), then the staging reclaim, the
evidence job on the accepted head and the review package, per
`docs/roadmap/STATUS_closure_protocol.md` algorithm steps 1 and 2.

## Next Steps
1. The closing round: the Built State's closure paragraph, the ledger rotation, the self-use
   entry SU-059's `consumed_by`, the STATUS flip with the README sync, and the pull request, left
   unmerged until the next feature's Open PR Gate.

## Risks
- The evidence selection must hold no parameter id the packaging scan reads as unsafe.
- R-1235, R-1246, R-1251 and R-1252 are owned by F306.
