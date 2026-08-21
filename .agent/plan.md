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
R11: record the R10 verdict and build the DETERMINISTIC half of T004 Stage 2 —
the grounding-source labelling, the level dial and the small-context assembly,
as a pure module that reaches no model and opens no file.

## Next Steps
1. R12 FINISHES T004: `remedy teach ask` on the CLI, the teacher model call
   through the role's own config, the honest refusal when no model is
   configured, and spend recorded under the role name `teacher` so
   `query_cost(by="role")` separates it from mission spend.
2. The INTEGRATION GATE round follows T004 — the full suite, per
   docs/agents/integration_gate.md — because T002 and T003 touch the CLI
   catalog, which the parser and the help renderer both read.
3. The CLOSURE round follows, per docs/roadmap/STATUS_closure_protocol.md:
   evidence job, fresh review zip, the STATUS line, and the pull request.

## Risks
- R12 IS WHERE THE COST STORY IS PROVEN OR LOST. Stage 1 and this round spend
  nothing because neither calls a model; R12 makes the first teacher model call,
  and its spend must land under the role name `teacher` or DECISION F255 D3 is
  unmet.
- THE LEDGER'S ONE ROW IS A TASK RUN. `token_ledger.record_call` is documented
  as one row per finalized task run, keyed `<job_id>:<task_id>`, and a teacher
  question is neither. R12 must settle that shape before it writes a row.
- THE READ-ONLY PROOF COVERS NARRATE ONLY; `teach ask` needs its own.
