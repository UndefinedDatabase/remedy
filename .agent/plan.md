# Plan — F255 Teacher role

Branch: feature/f255-teacher-role, cut from `main` at b35d350b, the merge commit
of pull request #207. No pull request is open for this branch; on this project
the PR is created by the closure round.
`.agent/live_review.md` is the source of truth for the open set, for the next
free finding id and for the round map; this file repeats none of them.

## Goal
A fourth configured role, `teacher`, that narrates a running mission and answers
operator questions about the operator's own code, and never influences the run.
DONE when passive narration keyed to ledger events (Stage 1, deterministic
templates, zero tokens) and on-demand Q&A (Stage 2, through the teacher role's
own model) both work, the three grounding sources are never mixed silently,
teacher spend is its own budget pool in the F103 ledger, and the read-only
invariants hold under test.

## Current Step
R2: register R-0601 and R-0602, record the R1 verdict, and MEASURE the five
seams F255 depends on into `.agent/f255_inventory.md`. Nothing is designed and
nothing is built this round.

## Next Steps
1. R3 RULES THE SHAPE AS A DECISION and amends
   `docs/roadmap/features/T5_F255.md` with the Design, Task slicing, Acceptance
   and Do-not-touch sections its registration stub has never carried. R3 also
   rules R-0602, the dead token cap, per §4 item 7.
2. R3 MUST RULE ON EACH SPEC-VS-REALITY GAP R2 MEASURES, rather than building
   around it. A dependency the registration names but the code lacks is a
   planning decision, not a detail for a build round to improvise.
3. R4 ONWARD BUILDS THE T-SLICES that DECISION names, Stage 1 before Stage 2.

## Risks
- THE REGISTRATION MAY NAME GROUND THAT DOES NOT EXIST. F255 depends on a
  "stable ledger event vocabulary" and on the isolation rules of a `watch`
  command; R2 measures whether either is real before R3 designs on top of it.
- READ-ONLY IS AN INVARIANT, NOT AN INTENTION. If `ActionClass` read_only turns
  out to be declarative only, the teacher's hard invariant needs an enforcement
  seam that must be designed rather than assumed.
- THE THREE GROUNDING SOURCES ARE THE WHOLE FEATURE. A teacher that silently
  mixes ledger fact, workspace code and model knowledge is worse than no
  teacher, so their separation is a test obligation and not a prompt wish.
