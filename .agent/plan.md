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
R4: record the R3 verdict and amend `docs/roadmap/features/T5_F255.md` by
APPEND — the Design, Task slicing, Acceptance, Edge cases, Orchestrator brief
and Do-not-touch sections, plus the three supersessions the R3 rulings require.
Nothing is built this round and no registered word is rewritten.

## Next Steps
1. R5 APPLIES DECISION F255 D6 to `docs/agents/handback_template.md`, removing
   the withdrawn 800-token cap and stating that the LINE cap is the operative
   bound. It is a docs round and gates tests/docs/ accordingly.
2. R6 BUILDS T001 — the role vocabularies — including the renamed seven-to-eight
   pin in the SAME commit as the tuple it guards.
3. R7 ONWARD BUILDS T002 AND T003 TOGETHER, Stage 1 narration with its
   behavioural read-only proof, then T004 last.

## Risks
- THE AMENDMENT IS NOW THE SPEC. If a T-slice drifts from it, the drift is a
  finding rather than a preference, which is the point of writing it down.
- STAGE 1 MUST STAY ZERO-TOKEN TO BE WORTH HAVING. If narration quietly starts
  calling a model, the feature loses both its cost story and its offline story.
- READ-ONLY IS PROVEN BY ONE TEST SHAPE. If that test is weak, the feature's
  hardest invariant is decorative — DECISION F255 D4 is only as good as the
  test T003 writes.
