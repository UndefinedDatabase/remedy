# Plan — F272 One world completion

Branch: feature/f272-one-world-completion. Rounds 1, 3, 4, 5 and 6 PASSED; round
2 FAILED on a premise DECISION F272 D2 has corrected. T001 is COMPLETE: the run
re-key, the repository-wide spelling sweep and the name collapse have all landed.

## Goal

Finish what F260 began: a Job that carries MANY runs, every consumer on the
unified model, and the classic runner, its resolver and the prototype cluster
deleted. Task slicing per `docs/roadmap/features/T2_F272.md` — T001 the plural
run list and the run re-key, T002 the rest of the unified record, T003 the
eleven consumers, T004 the classic runner, T005 the reachability test and the
cluster deletion, which is never split.

## Current Step

T002 begins. This round gives `JobPlan` the eight administrative fields of
DECISION F260 D1 that have no counterpart on it today — `mission`,
`user_prompt`, `project_id`, `intake`, `flight_plan`, `artifacts`, `budget` and
`fences` — wired through both `_export_job` and `_import_job`, which are
explicit field-by-field functions, so the fields survive a persist/resume cycle
rather than existing only in memory. A new test file pins each field, the whole
round trip through JSON, and the defaulted read that keeps older records
loadable.

## Next Steps

1. The three administrative fields that COLLIDE with an existing spelling:
   `id` is already the 16-hex `job_id`, `name` is `job_title`, and `state` must
   absorb `status` as one `RunState` field with the bare string dropped. The
   last of those is a type change with wide reach and needs its own ruling.
2. The Mission extension — the order, the contract, the mission plan and the
   ordered job references.
3. T003, the eleven consumers named under Design in `T2_F260.md`, one per commit
   where the diff allows, each with a test that proves it works on a job created
   through the ping-pong path.
4. T004, the classic runner and the resolver collapse; then T005, the
   reachability test and the cluster deletion, which is never split.

## Risks

- A field added to the dataclass and to neither writer is a Python-only
  attribute that vanishes on the first persist/resume cycle. That is why the
  round trip through `json.dumps` is the gate rather than a field-presence read.
- Older job records on disk carry none of the new keys and must still load, so
  every import reads through a default.
