# Plan — F277 Machine contracts: event vocabulary, JSON envelope, exit codes

Branch: feature/f277-machine-contracts, cut from `main` at `f2494c02`, the
merge commit of pull request 262 (F276's closure). No pull request is open.

## Goal

Three machine-facing contracts become declarations a test can read: the event
vocabulary written into the run ledger, the JSON envelope every `--json`
command emits, and the meaning of each exit code
(`docs/roadmap/features/T2_F277.md`).

## Current Step

T001 and T002 are finished. Round 7 (booked) migrated the `event` and `file`
groups onto the shared `fail()` helper and closed clean (PASS).

Round 8 is BLOCKED before any commit. The R8 block ordered five state-payload
appends/rewrite (C1a/C1b: ledger.md, decisions.md, plan.md, slips.md) and five
`git apply` diffs (C2-C6: job context, worker, change, blocker, contract). Nine
payloads were verified against the block's PAYLOADS table before use; eight
matched byte-for-byte and `decisions.md` did not (54 lines both, but 4185
bytes/sha256 `2b34e363...` measured vs 4192 bytes/sha256 `41456077...`
expected). Per the block's own rule ("do not guess which half of a
disagreement is wrong"), no commit consuming any payload was made.

## Next Steps

1. Operator/reviewer regenerates or corrects the `decisions.md` payload (or
   the block's table entry) for round 8; re-verify all nine payloads before
   any commit is attempted.
2. Once transport is clean, resume the R8 bundle: C1a, C1b, then C2-C6
   (job context, worker, change, blocker, contract groups onto `fail()`).
3. T003 catalog-half closure: the 33 read-only-without-`supports_json`
   commands (including `init run`, `dev status`), plus the catalog test.
4. T004: exit-code taxonomy under `docs/guides/`, asserted from the catalog,
   plus `tests/cli/test_json_contract.py`'s sweep.
5. Closure: §3 checklist consolidation (R-1014's fix merged into item 12),
   full-suite integration gate, evidence job, review zip, STATUS flip.

## Risks

T003 is the largest slice of this feature; each migrated group's round
carries a test proving the text branch is byte-identical to the prior print.
Round 8's blocker is a transport-integrity issue on one payload file, not a
code or design risk — re-verify before trusting any file under
`.remedy-wt/f277-r8-payloads/` a second time.
