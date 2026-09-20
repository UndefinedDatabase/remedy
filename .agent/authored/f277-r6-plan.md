# Plan — F277 Machine contracts: event vocabulary, JSON envelope, exit codes

Branch: feature/f277-machine-contracts, cut from `main` at `f2494c02`, the
merge commit of pull request 262 (F276's closure). No pull request is open.

## Goal

Three machine-facing contracts become declarations a test can read: the event
vocabulary written into the run ledger, the JSON envelope every `--json`
command emits, and the meaning of each exit code
(`docs/roadmap/features/T2_F277.md`).

## Current Step

T001 is finished. Round 6 books round 5's PASS, registers `R-1014` — the
round 5 gate whose blob-id table was rotated by one row and which no round
could have satisfied — and lands T002: `apps/cli/json_envelope.py` with one
envelope shape, and an error boundary around dispatch in `apps/cli/grouped.py`
so that no uncaught handler exception reaches the operator as a traceback,
under `--json` or otherwise. DECISION F277 D6 records why the boundary catches
`Exception` rather than the project exception base T002 named, which does not
exist, and amends the feature file to match.

## Next Steps

1. T003: the shared `fail(code, message, *, json_output)` replacing the
   `print(...); sys.exit(1)` pairs, one command group per commit and only for
   groups that survive F261; the three commands that accept `--json` and
   ignore it; and the read-only-without-`supports_json` set emptied, asserted
   by a catalog test.
2. T004: the exit-code taxonomy under `docs/guides/`, asserted from the
   catalog rather than from prose, plus `tests/cli/test_json_contract.py`
   sweeping every `supports_json` command on success AND on an invalid
   argument, with catalog-to-dispatch parity in the same file.
3. Closure: the §3 checklist consolidation pass, which is where `R-1014`'s fix
   clause lands — merged into item 12, never appended, because the list may
   not grow; then the integration gate (the full suite, once), the evidence
   job, the review zip and the STATUS flip.

## Risks

`R-1014` is open and owned by F277, and its repair is the consolidation pass
in step 3. A closure that runs that pass without applying the clause leaves
the finding to be re-assigned, which is the one outcome the fix clause exists
to prevent.
