# Orchestrator Loop Contract

> How Remedy processes work through Build/Test/Review cycles.

## Core Model

The orchestrator is the chief decision-maker. It decides:

- Whether work is ready to proceed
- Whether work needs review
- Whether new tasks should be created
- Whether work can be finalized

## Not A Waterfall

Remedy is NOT a single-pass pipeline:

```
Planning → Build → Test → Review → Finalized
```

Remedy is an iterative loop:

```
Planning → [Build → Test → Review]* → Finalized
```

Build/Test/Review may repeat multiple times until quality is acceptable.

## Task Lifecycle States

| State              | Meaning                                        |
|--------------------|------------------------------------------------|
| proposed           | Suggested by review, user, or model            |
| evaluated          | Orchestrator has assessed risk/value            |
| approved_for_build | Cleared for implementation                     |
| in_progress        | Being worked on                                |
| needs_review       | Implementation done, awaiting review           |
| needs_rework       | Review found issues, must be fixed             |
| blocked            | Cannot proceed, external dependency            |
| done               | Completed and verified                         |
| rejected           | Evaluated and declined                         |
| deferred           | Valid but postponed                             |

## Proposed Task Evaluation

Not every suggested task should be implemented:

1. Review may create new proposed tasks
2. Proposed tasks must be evaluated before implementation
3. Evaluation considers: risk, value, capability requirements
4. Only approved tasks enter the work plan

A task is NOT the same as a proposed task:
- **Proposed**: suggested, needs evaluation
- **Planned**: accepted into work plan, ready for implementation
- **In Progress**: being actively worked on

## Finalized Gate

Finalized means ALL of these are true:

- Job state is completed/done/finalized
- No blocked tasks
- No pending/planned tasks
- No open approvals
- No unresolved review findings (if tracked)
- No proposed-but-not-approved tasks (if tracked)

If any data is unavailable, be conservative: do not mark finalized.

## Review-Created Tasks

When review creates new tasks:

1. Tasks start as `proposed`, not `in_progress`
2. Orchestrator evaluates each proposed task
3. Approved tasks enter the build queue
4. Timeline shows the review event but does NOT mark Finalized
5. New Build/Test/Review cycle begins

## Timeline Representation

- Phase header shows the six canonical phases (always visible)
- Rail shows progress through phases
- Event rail shows real micro-events from the event ledger
- Repeated Build/Test/Review events appear in order with cycle numbers
- Finalized only lights up when the gate passes
