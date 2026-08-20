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
R7: record the R6 verdict and build the CONVENTIONS half of T001 — `teacher`
joins `ConventionsRole`, its reviewed document lands under `docs/agents/`, the
mapping pins and rule anchors extend with it, and the docs index registers it.

## Next Steps
1. R8 ADDS THE `teacher.model` CONFIG KEY, modelled on the existing
   `orchestrator.model` spec, with its pin in the same commit. It is a round of
   its own because the R7 block reached its line cap without it.
2. R9 BUILDS T002 AND T003 TOGETHER — Stage 1 narration over an enumerated
   event set, and the behavioural read-only proof — because a read-only feature
   whose read-only-ness is unproven is this feature's likeliest failure.
3. T004, Stage 2 Q&A, comes last and only once the grounding-source labelling
   of T002 is real.

## Risks
- FIVE ROLE LISTS EXIST AND T001 TOUCHES TWO. DECISION F255 D1 rules that the
  CLI-override and token-cost lists are deliberately NOT extended, so a later
  reader finding `teacher` absent from them is seeing a decision, not an
  omission.
- THE CONVENTIONS DOCUMENT IS CAPPED. `CONVENTIONS_TOKEN_CAP` is 800 tokens
  estimated as chars/4; the document this round authors measures 1972 chars and
  493 tokens, so 307 tokens of headroom absorb later edits.
- STAGE 1 MUST STAY ZERO-TOKEN TO BE WORTH HAVING. If narration quietly starts
  calling a model, the feature loses both its cost story and its offline story.
