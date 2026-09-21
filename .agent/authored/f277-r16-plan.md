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

The integration gate is green at `17813 passed, 20 skipped` and the shrinking
rule was satisfied in one of its three rounds. Round 16 is the evidence
round: the feature-scoped bundle through `create_manual_completion_bundle`
and a FRESH review zip. The base is the branch's FORK POINT
`f2494c0216b33d5f261195789ec9f7a300de5fca`, where the two `rev-list` counts
agree at 87; the evidence dir stays gitignored and is never committed.

## Next Steps

1. If the zip does not build READY, the next round reads its raw error and
   repairs the cause. A failing zip is a closure BLOCKER, and the
   BLOCKED_EVIDENCE attempts of F281 took four rounds — the known causes are
   node-id hygiene, directory entries in `test_files`, and a base that is not
   the fork point.
2. The §3 consolidation pass, where `R-1014`'s fix clause lands merged into
   an existing item and never appended; the list comes out no longer than it
   went in.
3. The ledger rotation by `scripts/rotate_live_review.py`, as its own commit,
   then the owner re-assignment of every open finding F277 did not resolve to
   the next findings-paydown feature.
4. The STATUS `[x]` flip with the README capability sync and the `SU-025`
   `consumed_by` edit in the SAME commit, last on the branch under Rule A4,
   then the pull request, which is NOT merged this session.

## Risks

Four numerals the reviewer wrote by hand across three rounds were wrong and
the worker caught every one; the tree numbers now come from a script, and the
evidence bundle's own numbers are derived inside the driver rather than
transcribed into the block, because that is where this class has cost most.
