# Plan — F027 Task veto

Branch: feature/f027-task-veto, cut from `main` at `557cbbcc`, the merge
commit of pull request 282 (F285 Findings paydown v4).

## Goal

The human red line is one click and one reason: a vetoed task is struck,
its unreachable downstream is computed and shown, the run continues on
independent branches, and a replan proposal is filed into the decision
inbox and never executed on its own (`docs/roadmap/features/T5_F027.md`).

## Current Step

ROUND 5, BLOCKED after C4: round 4 is booked, R-1067 is registered and
repaired (landed at C3, `90e5b529`), and `job.veto-task` is in the catalog
and the CLI (C4, `d98f9922`). C5 (the door and the inbox) is written but
NOT committed: the risk below materialized. See `.agent/handoff.md` for
the exact reproduction and the question for the reviewer.

## Next Steps

1. Reviewer ruling on the door's transitive-forbidden guard (see handoff):
   either `ACCEPTED_TRANSITIVE_FORBIDDEN` gains `packages.orchestration.exec_guard`
   and `subprocess` with a DECISION, or another design reaches
   `task_veto`/`veto_proposal` without widening it.
2. Once ruled, land C5 (door + inbox), C6 (mutation tool) and C7 (handback).
3. T003: the strike, the reason on hover, the dimmed unreachable set,
   the veto affordance and the inbox card's plain-words menu on the page.
4. The diamond end-to-end through the door and the runner; the closure sequence.

## Risks

MATERIALIZED: the door reaches `packages.orchestration.exec_guard` and
`subprocess` transitively through `task_veto.py`'s own (frozen this round)
import of `stream_evidence`, whose `TYPE_CHECKING`-guarded `exec_guard`
import the guard's static reader still counts. Open findings: 1 — R-1067,
owned by F027, repaired this round (landed, not yet booked as Landed
pending the round's close).
