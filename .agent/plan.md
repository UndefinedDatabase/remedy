# Plan — F277 Machine contracts: event vocabulary, JSON envelope, exit codes

Branch: feature/f277-machine-contracts, cut from `main` at `f2494c02`, the
merge commit of pull request 262 (F276's closure). No pull request is open.

## Goal

Three machine-facing contracts become declarations a test can read: the event
vocabulary written into the run ledger, the JSON envelope every `--json`
command emits, and the meaning of each exit code
(`docs/roadmap/features/T2_F277.md`).

## Current Step

Round 3 books round 2's PASS and gives `command_discovery_completed` its
writer, per DECISION F277 D4. `remedy test discover <job>` now records itself
in the run ledger with the two metadata keys `memory_learn` already indexes,
so autonomy level 3 becomes reachable for the first time and the name moves
out of the quarantine into `EVENT_NAMES`. The quarantine goes from four names
to three.

## Next Steps

1. `snapshot_created`, the `autonomy_loop` level-5 gate, routed through
   `build_snapshot_truth` rather than renamed; plus the rest of
   `patch_intent_reverted`, whose surviving readers index by a key its writer
   does not carry.
2. `stop_reason_recorded`, whose readers in `project_summary.py`,
   `ui_view_model.py` and `ui_server.py` are leftovers of DECISION F031 D2
   and D9 and whose removal is a UI behaviour change.
3. T002: `apps/cli/json_envelope.py` with `emit_ok` and `emit_error` over one
   shape, and an error boundary around dispatch in `apps/cli/grouped.py`.
4. T003: the shared `fail()` helper replacing the `print(...); sys.exit(1)`
   pairs, and the read-only-without-`supports_json` set emptied.
5. T004: the exit-code taxonomy under `docs/guides/`, asserted from the
   catalog, plus the `tests/cli/test_json_contract.py` sweep.
6. Closure: integration gate, evidence job, review zip, STATUS flip.

## Risks

`_discover_sinks` derives a sink's positional index from the DEFINITION's
argument list, so a bound METHOD sink would be read one position off at its
call sites. This round's writer is a keyword argument to `append_run_event`,
a seed sink, so the collector sees it; a later writer added as a method would
be invisible and the strict-mode flag is the only backstop.
