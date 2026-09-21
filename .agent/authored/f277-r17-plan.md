# Plan — F277 Machine contracts: event vocabulary, JSON envelope, exit codes

Branch: feature/f277-machine-contracts, cut from `main` at `f2494c02`, the
merge commit of pull request 262 (F276's closure). No pull request is open.

## Goal

Three machine-facing contracts become declarations a test can read: the event
vocabulary written into the run ledger, the JSON envelope every `--json`
command emits, and the meaning of each exit code
(`docs/roadmap/features/T2_F277.md`). F277 closes on the first two complete
and the third half applied; DECISION F277 D10 moved the rest to F283.

## Current Step

Round 16's package is BLOCKED_EVIDENCE on one validator error: the
verification record's `test_files` was dictated in selection order and the
validator requires it sorted. Round 17 registers the product half as
`R-1017`, lands the pitfall as (f) in the closure protocol so the next
closure reads it, and rebuilds — with `validate_verification_tests` called on
the produced document as a pre-check, which surfaces a rejection without
paying for a package build.

## Next Steps

1. If the package still is not READY_FOR_REVIEW, read its raw error and
   repair the cause; nothing may be closed over a package that is not ready.
2. The §3 consolidation pass, where `R-1014`'s fix clause lands merged into
   an existing item and never appended; the list comes out no longer than it
   went in, and its merged number is retired rather than reused.
3. The ledger rotation by `scripts/rotate_live_review.py`, as its own commit,
   then the owner re-assignment of every open finding F277 did not resolve to
   the next findings-paydown feature.
4. The STATUS `[x]` flip with the README capability sync and the `SU-025`
   `consumed_by` edit in the SAME commit, last on the branch under Rule A4,
   then the pull request, which is NOT merged this session.

## Risks

The closure has now spent two rounds on the evidence package, which is the
historical shape: F281 needed four. Every remaining number comes from a
script or a transcript rather than from the reviewer's arithmetic, and the
pre-check added this round is what makes a third packaging round cheap to
avoid rather than cheap to discover.
