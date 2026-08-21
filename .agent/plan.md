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
R16 FINISHES T004. It rules the teacher's model seam, builds it as
`packages/orchestration/teacher_model.py`, and wires it to `remedy teach ask` in
the SAME round, so the seam has a caller the round it is born — the debt R13 left
and this plan has carried as a risk since.

## Next Steps
1. The INTEGRATION GATE round follows T004 — the full suite, per
   docs/agents/integration_gate.md — because T002, T003 and T004 all touch the
   CLI catalog, which the parser and the help renderer both read.
2. The CLOSURE round follows, per docs/roadmap/STATUS_closure_protocol.md:
   evidence job, fresh review zip, the STATUS line, and the pull request.

## Risks
- THE REFUSAL CONDITION IS NOT "NO MODEL CONFIGURED". `resolve_role_config`
  returns a provider-aware DEFAULT model for every role, so that state is
  unreachable and a test driving it would prove nothing. Stage 2 refuses on NO
  USABLE TRANSPORT instead (DECISION F255 D9).
- `remedy teach ask` WRITES ONE LEDGER ROW, so its read-only proof must exclude
  that file BY NAME (DECISION F255 D10) rather than by silence, or it proves the
  opposite of what it claims.
- R-0607 STAYS OPEN. Only a docs round promoting its rule into the
  docs/agents/planner_reviewer_prompt.md §3 checklist closes it; R16 obeys the
  rule without closing the finding.
