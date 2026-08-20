# Plan — F255 Teacher role

Branch: feature/f255-teacher-role, cut from `main` at b35d350b, the merge commit
of pull request #207. No pull request is open for this branch; on this project
the PR is created by the closure round.
`.agent/live_review.md` is the source of truth for the open set, for the next
free finding id and for the round map; this file repeats none of them.

## Goal
A fourth configured role, `teacher`, that narrates a running mission and answers
operator questions about the operator's own code, and never influences the run.
DONE when passive narration keyed to an enumerated set of ledger events (Stage 1,
deterministic templates, zero tokens) and on-demand Q&A (Stage 2, through the
teacher role's own model) both work, the three grounding sources are never mixed
silently, teacher spend is reported as its own role in the F103 ledger, and the
read-only invariant is proven behaviourally.

## Current Step
R10: record the R9 verdict and finish T002 and T003 — `remedy teach narrate`
over a real run log, its catalog entry declaring `action_class="read_only"`, and
the behavioural proof that the command changes no byte under the data root.

## Next Steps
1. R11 BUILDS T004, Stage 2 Q&A: `remedy teach ask`, the small context, the
   three grounding sources labelled per answer, the level dial, and spend
   recorded under the role name `teacher`. It is the round that gives
   `teacher.model` its first reader.
2. The INTEGRATION GATE round follows T004 — the full suite, per
   docs/agents/integration_gate.md — because T002 and T003 touch the CLI
   catalog, which the parser and the help renderer both read.
3. The CLOSURE round follows, per docs/roadmap/STATUS_closure_protocol.md:
   evidence job, fresh review zip, the STATUS line, and the pull request.

## Risks
- STAGE 2 IS THE ROUND THAT CAN BREAK THE COST STORY. Stage 1 spends nothing
  because it calls no model; T004 introduces the first teacher model call, and
  its spend must land under the role name `teacher` in the F103 ledger or
  DECISION F255 D3 is unmet.
- THE READ-ONLY PROOF COVERS THE NARRATE PATH ONLY. `remedy teach ask` is a new
  path and needs its own proof; a proof of one command is not a proof of a role.
- THE CATALOG IS SHARED GROUND. `teach` is a new command group the parser and
  the help renderer both build from, so a later round changing its shape re-runs
  their suites, not only the teacher's own.
