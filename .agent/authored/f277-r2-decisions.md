
DECISION F277 D4 (2026-09-20, round 2) — THE SIX QUARANTINED NAMES ARE DISPOSED OF IN FOUR
ROUNDS, AND ROUND 2 TAKES THE THREE WHOSE ANSWER IS ALREADY IN THE REPOSITORY.

CONTEXT. `READ_ONLY_EVENT_NAMES` is a quarantine, not a vocabulary: round 1 measured six names
that live code READS and nothing WRITES, and `docs/roadmap/features/T2_F277.md` rules that each
is given a writer or deleted together with its score contribution, never left absent. The six
are not one kind of problem. Measured by the reviewer at `9114721f`, `approval_decision` has ONE
event-name reader, `worker_adapters_listed` has one, `patch_intent_reverted` has four,
`command_discovery_completed` has two, and `snapshot_created` and `stop_reason_recorded` each
feed user-visible behaviour. A single round that touched all six would mix a two-line deletion
with a metadata-contract change and a UI behaviour change.

CHOSEN. Round 2 disposes of the three whose correct answer is a name this repository already
writes, or no reader at all, and states what the remaining rounds take.

  (1) `worker_adapters_listed` — DELETED with its reader. `autonomy_readiness._has_worker_adapters`
  is a private function with ZERO callers: it is absent from `_collect_signals`, from every level
  in `_assess_level` and from every test, so its "score contribution" is empty and there is
  nothing to remove beside the function itself. This is the instance the feature file names by
  hand, and the honest disposition is deletion, not a writer minted to feed a signal nobody reads.

  (2) `approval_decision` — the READER IS REPOINTED at the names the repository writes.
  `stop_reasons.derive_stop_reasons` derived `derived_not_approved` from `not any(a.get("event")
  == "approval_decision" ...)`, a comparison that has never matched, so the guard was vacuously
  true and EVERY patch intent was reported as awaiting approval, decided ones included. The
  decision is really recorded as `patch_intent_approved` or `patch_intent_rejected`, both of
  which are in `EVENT_NAMES`. A rejected intent is decided and not waiting, which is the reading
  `autonomy_readiness._has_pending_approvals` already had — this change makes the two modules
  agree rather than inventing a third rule.

  (3) `patch_intent_reverted` — ONE OF ITS FOUR READERS GOES; the name STAYS quarantined.
  `autonomy_readiness._has_revert_snapshot` fed a `revert_snapshot` signal that NO level checks,
  and `project_brain._build_readiness_node` published it as `"revert_capable"`, so that field
  has read False for every job ever built. The authoritative durable check `verified_snapshot`
  (Step 1159) sits in the same signal dict and is what level 5 already gates on, so
  `revert_capable` is repointed at it and the dead signal is deleted. The name stays in the
  quarantine because `change_set.py`, `project_brain.py` and `ui_server.py` still replay reverts
  already on disk, and `tests/orchestration/test_source_apply.py` pins that on purpose. Its
  remaining disposition is a METADATA CONTRACT and not a rename: the writer spells it
  `revert_completed` and carries `apply_id`, `snapshot_id`, `state`, `paths_restored` and
  `paths_deleted` but no `intent_id`, which is the key two of those three readers index by.

ALTERNATIVES. Dispose of all six in round 2 — rejected: it bundles a deletion, a contract change
and a UI change behind one verdict. Mint a writer for `worker_adapters_listed` so the dimension
scores present — rejected: there is no dimension, because nothing reads the function. Rename
`patch_intent_reverted` to `revert_completed` at its readers — rejected: two readers index by a
key that event does not carry, so the rename would silently drop them to zero matches, which is
the defect this feature exists to remove rather than to relocate.

WHAT THE REMAINING ROUNDS TAKE, so nothing is deferred without an owner. Round 3:
`command_discovery_completed`, whose two readers — the level-3 `command_discovery` gate and
`memory_learn`'s `context.command_discovery.*` entries — make autonomy level 3 permanently
ineligible for every job; its disposition is a writer in the discovery path, and the metadata
keys are fixed by `memory_learn`, which reads `source_types` and `candidate_count`. Round 4:
`snapshot_created`, the `autonomy_loop` level-5 gate, routed through `build_snapshot_truth`
rather than renamed, plus the remainder of `patch_intent_reverted`. Round 5:
`stop_reason_recorded`, whose readers in `project_summary.py`, `ui_view_model.py` and
`ui_server.py` are leftovers of DECISION F031 D2 and D9 and whose removal is a UI behaviour
change.

REVERSE: delete this paragraph and restore the three code sites from git history at `9114721f`.
Reversing (2) reinstates a blocker stop reason on every approved intent, and reversing (3)
reinstates a `revert_capable` field that is False by construction; both are recorded here so the
cost of the reversal is visible before it is paid.
