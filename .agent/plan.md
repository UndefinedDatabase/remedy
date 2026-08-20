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
R8: register R-0605 against the R7 block, record the R7 verdict, and finish T001
by declaring the `teacher.model` config key with its pin in the same commit.
T001 is complete when this round lands.

## Next Steps
1. R9 BUILDS T002 AND T003 TOGETHER — Stage 1 narration over an enumerated
   event set, and the behavioural read-only proof — because a read-only feature
   whose read-only-ness is unproven is this feature's likeliest failure.
2. T004, Stage 2 Q&A, comes last and only once the grounding-source labelling
   of T002 is real. It is also the round that gives `teacher.model` its first
   reader.
3. The integration gate and the closure round follow T004, per
   docs/roadmap/STATUS_closure_protocol.md.

## Risks
- THE NEW CONFIG KEY HAS NO READER UNTIL T004. That is deliberate and stated in
  the key's own description, so a later reader finds a decision rather than a
  forgotten wiring — but if T004 slips, the key ships unread and the feature
  file's T001 claim outruns the code.
- STAGE 1 MUST STAY ZERO-TOKEN TO BE WORTH HAVING. If narration quietly starts
  calling a model, the feature loses both its cost story and its offline story.
- FIVE ROLE LISTS EXIST AND T001 TOUCHED TWO. DECISION F255 D1 rules that the
  CLI-override and token-cost lists are deliberately NOT extended.
