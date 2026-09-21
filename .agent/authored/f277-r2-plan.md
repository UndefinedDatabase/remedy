# Plan — F277 Machine contracts: event vocabulary, JSON envelope, exit codes

Branch: feature/f277-machine-contracts, cut from `main` at `f2494c02`, the
merge commit of pull request 262 (F276's closure). No pull request is open.

## Goal

Three machine-facing contracts become declarations a test can read: the event
vocabulary written into the run ledger, the JSON envelope every `--json`
command emits, and the meaning of each exit code
(`docs/roadmap/features/T2_F277.md`).

## Current Step

Round 2 books round 1's PASS, registers and resolves `R-1012`, and disposes of
three of the six quarantined event names per DECISION F277 D4:
`worker_adapters_listed` is deleted with its zero-caller reader,
`approval_decision`'s reader is repointed at `patch_intent_approved` and
`patch_intent_rejected` so an approved intent stops being reported as a
blocker, and `patch_intent_reverted` loses the dead `revert_snapshot` signal
while `project_brain`'s `revert_capable` starts reading the authoritative
`verified_snapshot`. The quarantine shrinks from six names to four.

## Next Steps

1. `command_discovery_completed` gets a writer in the discovery path, with the
   metadata keys `memory_learn` already reads (`source_types`,
   `candidate_count`); this is what makes autonomy level 3 reachable at all.
2. `snapshot_created`, the `autonomy_loop` level-5 gate, routed through
   `build_snapshot_truth`; plus the rest of `patch_intent_reverted`, whose
   remaining readers index by a key its writer does not carry.
3. `stop_reason_recorded`, whose three readers are leftovers of DECISION F031
   D2 and D9 and whose removal is a UI behaviour change.
4. T002: `apps/cli/json_envelope.py` with `emit_ok` and `emit_error` over one
   shape, and an error boundary around dispatch in `apps/cli/grouped.py`.
5. T003: the shared `fail()` helper replacing the `print(...); sys.exit(1)`
   pairs, and the read-only-without-`supports_json` set emptied.
6. T004: the exit-code taxonomy under `docs/guides/`, asserted from the
   catalog, plus the `tests/cli/test_json_contract.py` sweep.
7. Closure: integration gate, evidence job, review zip, STATUS flip.

## Risks

`_discover_sinks` derives a sink's positional index from the DEFINITION's
argument list, so a bound METHOD sink would be read one position off at its
call sites. Measured at `9114721f` the discovery adds seven sinks and none is
a method — but step 1 mints a writer, and a method would be invisible to it.
