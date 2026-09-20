# Plan — F277 Machine contracts: event vocabulary, JSON envelope, exit codes

Branch: feature/f277-machine-contracts, cut from `main` at `f2494c02`, the
merge commit of pull request 262 (F276's closure). No pull request is open.

## Goal

Three machine-facing contracts become declarations a test can read: the event
vocabulary written into the run ledger, the JSON envelope every `--json`
command emits, and the meaning of each exit code
(`docs/roadmap/features/T2_F277.md`).

## Current Step

Round 5 landed C1a-C1b-C2-C3 (booking DECISION F277 D5, the RETIRED_EVENT_NAMES
rename and citation guard, the T2_F277.md amendment) and STOPPED before C4.
G1, G3, G4 and G5 all read green. G2, the code-transport blob-id gate, is RED
AS LITERALLY STATED: the block's table maps its three blob ids to the three
touched paths in a scrambled order relative to what the diff's own `index`
lines specify. The three committed blobs are independently proven correct
(each equals the diff's own stated new-blob hash, and the diff's sha256 was
verified before application), so the underlying fidelity claim holds, but the
gate as worded does not pass, and a red gate stops the round per the block's
hard rules. C4-as-specified (full six-gate PASS) was not executed; this
handoff and its push are the honest record of the stop.

## Next Steps

1. Reviewer repairs G2's path-to-blob-id table (or explains why the mapping
   the worker read is wrong) and reissues round 5 or a round 6 to close T001.
2. T002: `apps/cli/json_envelope.py` with `emit_ok` and `emit_error` over one
   shape (`schema_version`, `ok`, `sort_keys=True`), and an error boundary
   around dispatch in `apps/cli/grouped.py` so no traceback reaches the
   operator.
3. T003: the shared `fail(code, message, *, json_output)` replacing the
   `print(...); sys.exit(1)` pairs, one command group per commit, and the
   read-only-without-`supports_json` set emptied.
4. T004: the exit-code taxonomy under `docs/guides/`, asserted from the
   catalog rather than from prose, plus `tests/cli/test_json_contract.py`
   sweeping every `supports_json` command on success AND on an invalid
   argument.
5. Closure: integration gate (the full suite, once), evidence job, review zip,
   STATUS flip.

## Risks

T002 and T003 touch far more call sites than T001 did, and F261 settled which
command groups survive, so the migration has a fixed target. Here the code
has to catch up with a declaration that does not exist yet.
