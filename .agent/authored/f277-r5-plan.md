# Plan — F277 Machine contracts: event vocabulary, JSON envelope, exit codes

Branch: feature/f277-machine-contracts, cut from `main` at `f2494c02`, the
merge commit of pull request 262 (F276's closure). No pull request is open.

## Goal

Three machine-facing contracts become declarations a test can read: the event
vocabulary written into the run ledger, the JSON envelope every `--json`
command emits, and the meaning of each exit code
(`docs/roadmap/features/T2_F277.md`).

## Current Step

Round 5 books round 4's PASS and FINISHES T001 per DECISION F277 D5. The two
names left in the quarantine turned out not to be accidents: a dated decision
removed each one's writer and kept its readers so run logs already on disk
keep rendering (F271 D3 under R-0982, and F031 D2 and D9). The set is renamed
`RETIRED_EVENT_NAMES`, every entry must cite its ruling and name a reading
module, a new guard asserts both from the source, and the feature file's T001
design and Acceptance lines are amended to match.

## Next Steps

1. T002: `apps/cli/json_envelope.py` with `emit_ok` and `emit_error` over one
   shape (`schema_version`, `ok`, `sort_keys=True`), and an error boundary
   around dispatch in `apps/cli/grouped.py` so no traceback reaches the
   operator.
2. T003: the shared `fail(code, message, *, json_output)` replacing the
   `print(...); sys.exit(1)` pairs, one command group per commit, and the
   read-only-without-`supports_json` set emptied.
3. T004: the exit-code taxonomy under `docs/guides/`, asserted from the
   catalog rather than from prose, plus `tests/cli/test_json_contract.py`
   sweeping every `supports_json` command on success AND on an invalid
   argument.
4. Closure: integration gate (the full suite, once), evidence job, review zip,
   STATUS flip.

## Risks

T002 and T003 touch far more call sites than T001 did, and F261 settled which
command groups survive, so the migration has a fixed target. The risk is the
reverse of T001's: there the declaration had to catch up with the code, here
the code has to catch up with a declaration that does not exist yet.
