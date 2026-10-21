# Context — F060 Long-run certificate

## Active Branch
`feature/f060-long-run-certificate`, from `main` at `646c4b1d7` (the merge commit of pull request
374, which carried F141).

## Scope
F060 (Tier 3), as `docs/roadmap/features/T3_F060.md` and DECISION F060 D1 state: the certificate
profile with its manifest, claims and byte budget, the sources of a finished job, the verifier with
its tamper fixtures, and the two commands `remedy job certificate` and `remedy verify`.

## Do not touch
Cryptographic signing (the manifest's `signature` field stays reserved and empty), publishing or
hosting of certificates, and the review package's meaning for its existing users:
`packages/orchestration/review_zip.py` is reused, never changed.

## Active assumptions
- The packer and the reopen check are `build_review_zip_from_snapshot` and `verify_review_zip`.
- Every behaviour lands with a test that is red without it, proved by the reviewer's mutation.

## Constraints
- One full pytest suite per feature, in the closure's integration-gate round; every round runs
  its own selection once (operator amendments amend0917-throughput and amend0930-test-load).
- The structure ratchet: no listed function or file grows; new logic goes into new modules.
- No file under `.agent/` gains this machine's absolute paths; the commit hook refuses them.

## Steps
The item-status table for each round lives in that round's handback, `.agent/handoff.md`.
