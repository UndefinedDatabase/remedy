# Plan — F277 Machine contracts: event vocabulary, JSON envelope, exit codes

Branch: feature/f277-machine-contracts, cut from `main` at `f2494c02`, the
merge commit of pull request 262 (F276's closure). No pull request is open.

## Goal

Three machine-facing contracts become declarations a test can read: the event
vocabulary written into the run ledger, the JSON envelope every `--json`
command emits, and the meaning of each exit code
(`docs/roadmap/features/T2_F277.md`).

## Current Step

Round 4 books round 3's PASS, registers and resolves `R-1013`, and disposes of
`snapshot_created` per DECISION F277 D4. `autonomy_loop._decide` gated level 5
on that event, which nothing writes, so level 5 answered "no snapshot for
revert" for every job that ever reached it; the gate now reads the
`verified_snapshot` signal the loop computes one statement earlier, which is
the durable `build_snapshot_truth` check `autonomy_readiness` already uses.
The branch had no test at all and now has four. The quarantine goes from three
names to two.

## Next Steps

1. `patch_intent_reverted`: its writer spells the event `revert_completed` and
   carries no `intent_id`, the key `change_set.py` and `project_brain.py`
   index by, so the disposition is a metadata contract before a repoint.
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

Every disposition so far has replaced a dead event reader with a signal the
repository already computes, so no new event name has had to be invented. The
two survivors are not like that: one needs its writer's metadata widened and
one removes user-visible UI behaviour, so both cost a decision rather than a
repoint.
