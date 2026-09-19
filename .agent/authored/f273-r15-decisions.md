
## DECISION F273 D15 (2026-09-19, reviewer, round 15) — the job views read intents from the approval queue, the manifest diff and the conventions module go, and four prototypes are held for rulings
CONTEXT: R-0990, R-0931 and R-0981 each needed a choice between routes their texts allow, taken in
the round that lands the patch (amend0917-throughput rule 3). Measured by research helpers and
re-measured by the reviewer's dry run at `bce5bc3b`: `_extract_job_truth` names intents by
`<uuid>-0` and reads approvals under that key; the manifest diff functions of
`packages/orchestration/run_manifest.py` have test callers only since F261 deleted the command that
ran them; and `packages/orchestration/role_conventions.py` has no importer. The same helpers
prototyped the repair-loop group (R-0923, R-0918, R-0924, R-0925, R-0926), R-0914 and the worker
queue (R-0927, R-0928), and the reviewer holds all three, below.
CHOSEN: (1) R-0990. `_extract_job_truth` takes its ids and states from
`approval_queue.list_patch_intents`, every intent of every artifact, and `approval_required` is a
pending intent with no applied record; a rejected intent is not pending, an artifact that counts
intents it does not explain has nothing `patch approve` could resolve and requires no approval, and
the timeline's `approval_required` event speaks only when no intent is listed. The status tip reads
the pending ids the truth now carries. (2) R-0931. The run-input drift check leaves with its
command: `build_current_candidate`, `diff_manifests`, `load_latest_manifest_for_cli` and
`CanonicalLoadResult` are deleted with their helpers and tests; manifests are still written,
validated and exported, and `T0_F012.md` records that the check is gone, since no `docs/system/`
page describes F012. (3) R-0981. `role_conventions.py` is deleted with its test, because
registering its segment would change prompt bytes, which F105's Do-not-touch excludes;
`T2_F105.md` records the reason, and three tests that read the conventions documents rather than
the loader move to `tests/orchestration/test_conventions_documents.py`. (4) HELD, NOT LANDED: the
R-0914 prototype deletes `create_manual_completion_bundle`, which
`docs/roadmap/STATUS_closure_protocol.md` names as the closure evidence producer, so it would break
this feature's own closure; R-0914 needs its own measurement of which attestation writer is live.
The repair-loop prototype deletes `repair_loop.py` whole, against the "module stays whole" clause
R-0923 cites from DECISION F261 D17, and drops two cockpit labels for events still emitted. The
worker-queue prototype raises `_COUPLING_CEILING` from 1 to 6 and deletes a permission guard test
whose live targets remain. Each is a ruling the next session takes with its patch.
ALTERNATIVES: keeping `<uuid>-0` ids and translating them at `patch approve`, rejected as two id
spellings for one intent; a drift view on `job show --full`, rejected because F261's Do-not-touch
forbids widening it; landing the held prototypes now, rejected for the reasons in (4).
REVERSE: restore `apps/cli/commands/job.py`, `run_manifest.py`, `role_conventions.py`, `T0_F012.md`,
`T2_F105.md` and the touched tests from `bce5bc3b`, and delete this paragraph.
