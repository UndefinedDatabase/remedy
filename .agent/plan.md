# Plan — F255 Teacher role

Branch: feature/f255-teacher-role, cut from `main` at the merge commit of pull
request #207, which this round merged at the Open PR Gate.
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
R1: merge #207, claim F255, reset `.agent/live_review.md` carrying the F086 open
set forward, register R-0600 and record the F086 R35 verdict. No source file and
no test changes this round.

## Next Steps
1. R2 MEASURES THE GROUND BEFORE ANYTHING IS DESIGNED, because the feature file
   is a registration stub: how `role_config` resolves a role, which ledger
   events carry a stable vocabulary, how F103 separates a budget pool, what
   `ActionClass` read_only enforces, and how the watch path isolates a reader.
2. R3 RECORDS R2 AND RULES THE SHAPE AS A DECISION, amending
   `docs/roadmap/features/T5_F255.md` with the Design, Task slicing, Acceptance
   and Do-not-touch sections it has never carried.
3. R4 ONWARD BUILDS THE T-SLICES that DECISION names, Stage 1 before Stage 2.

## Risks
- THE FEATURE FILE IS A STUB. It carries Goal & Done, Scope and Non-goals only,
  so the Task slicing and Acceptance every build round reads are absent, and
  designing from the stub alone would be guessing rather than planning.
- THE THREE GROUNDING SOURCES ARE THE WHOLE FEATURE. A teacher that silently
  mixes ledger fact, workspace code and model knowledge is worse than no
  teacher, so their separation is a test obligation and not a prompt wish.
- READ-ONLY IS AN INVARIANT, NOT AN INTENTION. `ActionClass` read_only and the
  watch isolation must be shown to hold for the teacher path itself.
