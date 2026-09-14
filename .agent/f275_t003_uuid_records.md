# F275 T003 — every record the flip FEEDS that still declares a UUID-typed field

> Generated, never typed, by the instrument committed at
> `.agent/authored/f275-r56-records.py.md`. Measurement base: `62d4bbe7`.
> This file SIZES a class; it performs none of it, and no line under `packages/`,
> `apps/`, `tests/`, `docs/` or `scripts/` moved in the round that wrote it.

## 1. Why the earlier sweep could not see these

DECISION F275 D26's premise P2 reads, in its own instrument, `issubclass(obj,
BaseModel)`. That is False for every dataclass, so a dataclass declaring a UUID-typed
id was invisible to it, and D27 and D28 migrated the pydantic models it did find. The
sweep below widens in two directions at once — from pydantic to every class kind, and
from `packages.` to `apps.` as well — and reports which direction found anything.

## 2. The reading, complete and untrimmed

```
modules walked: 328 | modules that RAISED on import and were skipped: 0
classes under `packages.` or `apps.` declaring a UUID-typed field: 13
by declaration kind: {'dataclass': 8, 'pydantic': 5}
by top-level package: {'packages': 13}

  pydantic         packages.core.models.Artifact
      id: <class 'uuid.UUID'>
      -> THE CLASSIC RECORD ITSELF
  pydantic         packages.core.models.Job
      id: <class 'uuid.UUID'>
      -> THE CLASSIC RECORD ITSELF
  pydantic         packages.core.models.Task
      id: <class 'uuid.UUID'>
      output_artifact_ids: list[uuid.UUID]
      -> THE CLASSIC RECORD ITSELF
  dataclass        packages.memory.models.MemoryEntry
      id: UUID
      -> NOT ENUMERATED — fed by the flip at 0 constructions
  dataclass        packages.orchestration.agent_loop.AgentLoopState
      job_id: UUID
      -> NOT ENUMERATED — fed by the flip at 5 constructions
  dataclass        packages.orchestration.dag_schedule.TaskNode
      task_id: UUID
      depends_on: tuple[UUID, ...]
      -> NOT ENUMERATED — fed by the flip at 2 constructions
  dataclass        packages.orchestration.long_run_executor.TaskAttempt
      task_id: UUID | None
      -> NOT ENUMERATED — fed by the flip at 12 constructions
  pydantic         packages.orchestration.patch_intent.PatchIntentSet
      artifact_id: <class 'uuid.UUID'>
      -> MIGRATED by DECISION F275 D27 or D28
  dataclass        packages.orchestration.project_brain.ProjectBrainGraph
      job_id: UUID
      -> NOT ENUMERATED — fed by the flip at 1 constructions
  pydantic         packages.orchestration.project_registry.RemyProject
      id: <class 'uuid.UUID'>
      -> NOT ENUMERATED — fed by the flip at 0 constructions
  dataclass        packages.orchestration.task_runner.RunTaskResult
      task_id: UUID | None
      -> NOT ENUMERATED — fed by the flip at 11 constructions
  dataclass        packages.orchestration.verifier.VerificationResult
      task_id: UUID
      -> NOT ENUMERATED — fed by the flip at 18 constructions
  dataclass        packages.orchestration.workspace.Workspace
      job_id: UUID
      -> NOT ENUMERATED — fed by the flip at 1 constructions

the constructions of each NOT ENUMERATED record, and what its id field is given:
  AgentLoopState.job_id  5 constructions in 1 files, of which 5 pass a value the flip retypes
         5  Attribute  <- the flip retypes this
  MemoryEntry.id  15 constructions in 4 files, of which 0 pass a value the flip retypes
        15  (the field is not passed)
  ProjectBrainGraph.job_id  1 constructions in 1 files, of which 1 pass a value the flip retypes
         1  Attribute  <- the flip retypes this
  RemyProject.id  36 constructions in 18 files, of which 0 pass a value the flip retypes
        33  (the field is not passed)
         3  UUID()
  RunTaskResult.task_id  13 constructions in 4 files, of which 11 pass a value the flip retypes
        10  Attribute  <- the flip retypes this
         2  Constant
         1  Name  <- the flip retypes this
  TaskAttempt.task_id  23 constructions in 6 files, of which 12 pass a value the flip retypes
        12  Attribute  <- the flip retypes this
        11  (the field is not passed)
  TaskNode.task_id  2 constructions in 1 files, of which 2 pass a value the flip retypes
         2  Attribute  <- the flip retypes this
  VerificationResult.task_id  18 constructions in 4 files, of which 18 pass a value the flip retypes
        10  Name  <- the flip retypes this
         8  Attribute  <- the flip retypes this
  Workspace.job_id  1 constructions in 1 files, of which 1 pass a value the flip retypes
         1  Name  <- the flip retypes this
```

## 3. What this does NOT settle

WHICH RECORDS MUST MIGRATE IS A RULING AND NOT A COUNT. A record fed by the flip at
zero constructions is not thereby safe: this sweep resolves a CONSTRUCTION, and a field
assigned after construction is not a construction. That reading was not taken.

NO CLAIM IS MADE THAT THIS SWEEP IS COMPLETE, and section 2 reports the two ways it can
be short. A module that RAISES on import is skipped, and the count of those is printed
rather than left to be assumed — the D26 instrument skipped the same way and reported
no number at all. And a `TypedDict`, a `NamedTuple` built by the functional form, and
any id held in a plain `dict` carry no class annotation, so they are invisible to every
sweep of this shape, including this one.
