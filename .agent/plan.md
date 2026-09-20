# Plan — F277 Machine contracts: event vocabulary, JSON envelope, exit codes

Branch: feature/f277-machine-contracts, cut from `main` at `f2494c02`, the
merge commit of pull request 262 (F276's closure). No pull request is open.

## Goal

Three machine-facing contracts become declarations a test can read: the event
vocabulary written into the run ledger, the JSON envelope every `--json`
command emits, and the meaning of each exit code
(`docs/roadmap/features/T2_F277.md`).

## Current Step

Round 1 claims F277, re-heads `.agent/live_review.md`, books F276 round 15's
verdict, and builds T001: `packages/orchestration/event_names.py` declaring the
83 event names this repository writes, the six it only reads quarantined beside
them, the AST test that measures both from the source, and an opt-in strict
check in `RunLogWriter.log`. DECISIONs F277 D1 and D2 carry the collector
design and the quarantine, and D2 amends T001's Acceptance line.

## Next Steps

1. Dispose of the six quarantined names — one commit each, a writer or the
   reader deleted with what it feeds — until `READ_ONLY_EVENT_NAMES` is empty
   and `read ⊆ written ⊆ declared` holds. This is what round 1 defers.
2. T002: `apps/cli/json_envelope.py` with `emit_ok` and `emit_error` over one
   shape, and an error boundary around dispatch in `apps/cli/grouped.py` so no
   traceback reaches the operator.
3. T003: the shared `fail()` helper replacing the `print(...); sys.exit(1)`
   pairs, one command group per commit, and the read-only-without-`supports_json`
   set emptied.
4. T004: the exit-code taxonomy documented under `docs/guides/` and asserted
   from the catalog, plus `tests/cli/test_json_contract.py` sweeping every
   `supports_json` command on success AND on an invalid argument.
5. Closure: the integration gate runs the full suite once, then the evidence
   job, the review zip and the STATUS flip.

## Risks

The collector reads the code statically, so a name assembled across a module
boundary is invisible to it by construction. The strict-mode flag is the
runtime backstop, and it is off by default; nothing yet runs the suite with it
on. Whether it should be turned on inside the test suite is round 2's question.
