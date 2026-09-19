
## DECISION F273 D14 (2026-09-19, reviewer, round 14) — the last placeholder tips name real ids, and the dead brain, rollback, recommendation, evidence-export, task-file and fulfillment code goes with its tests
CONTEXT: R-0989, R-0903, R-0908, R-0911, R-0932 and R-0936 each needed a choice between routes
their texts allow, taken in the round that lands the patch (amend0917-throughput rule 3). Measured by
research helpers and re-measured by the reviewer's dry run at `3a93d638`: `_status_section` and the
cockpit print `<job_id>`, `<patch_intent_id>` and `<goal>` where the value is known or nameable;
`orchestrator_brain.list_decisions`, the rollback-proof reader and audit, the reviewer's
recommendation store and `pingpong_evidence.export_evidence` have test callers only, and nothing
writes what the first three read; `load_task_file`, `load_task_stdin`, `summarize_pingpong` and the
`scope_contract` parameters survive only for tests; and `run_job_fulfill` has no production caller,
so the fulfillment spine, three staging functions and the fulfillment sections of `job show --full`
read records nothing writes.
CHOSEN: (1) R-0989. The status tip names the first pending intent, since a next action is one
command, falling back to `patch list`; the cockpit's tips and attention items name the real job id
and intent ids, and its goal tip names the order in words. (2) R-0903. `orchestrator_brain.py` is
deleted with its dashboard section and tests, and the rollback reader and audit with theirs; the
snapshot section reports no rollback count. `validate_next_safe_action_command` leaves production
for `tests/orchestration/catalog_commands.py`, because seven test files use it to hold other
modules' printed commands to the catalog, which is a test's job and not a product's. (3) R-0908.
The two cockpit readers and the recommendation store are deleted with their tests; `run_reviewer`
stays, because `dev status` probes it; and `docs/system/orchestrator-loop.md` says that no step
replaced `review accept`, because the reviewer's verdict now acts inside `job run`. The finding's
four `token_economy` exports are left for its own text to settle, since neither its fix nor its
Acceptance line orders anything for them. (4) R-0911. `export_evidence` is deleted; every
file-content assertion of its eight test classes is kept against `build_evidence_bundle` and
`write_evidence_bundle`, the calls `job_evidence` makes, and only the assertions about the deleted
function's return value go. (5) R-0932. The two loaders, `summarize_pingpong` and the
`scope_contract` parameters are deleted with the tests that pinned only them; the two prompt goldens
are re-cut by computation from their base render minus the dropped segment, with a declared-change
note in each, because no generator exists. (6) R-0936. `job_fulfillment.py`, the three staging
functions and the fulfillment sections of `job show --full` are deleted with their tests, and
seven cockpit labels for events only that module emitted leave `humanizeCatalog.ts`. (7) R-0990,
found in this round, is registered and is the next round's.
ALTERNATIVES: naming every pending intent in one tip, rejected because a next action is one
command; keeping the validator in production for tests, rejected as production code nothing runs;
hand-editing the goldens, rejected as unprovable; keeping the fulfillment spine for a future heir,
rejected because git is the archive (AGENTS.md, Replacing is deleting).
REVERSE: restore every file the three diffs touch from `3a93d638`, and delete this paragraph.
