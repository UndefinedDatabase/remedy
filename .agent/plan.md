# Plan — F310 Budgets that fit the provider, and one stop, one question

## Goal
A job's default limits come from the profile of its provider class, its wall clock measures work
and not waiting, and a budget stop asks the operator exactly one question
(`docs/roadmap/features/T12_F310.md`). Owns findings R-1370, R-1371 and R-1372.

## Current Step
Round 3 (session 1): book round 2's verdict and R-1372, DECISION F310 D5, repair R-1372 with a
test, the budget branch of `_cmd_decision_resolve` as a function of its own (structure step), and
T003 part one — the budget decision names the blockers, `extend` without an answer doubles what
the stop exhausted, answers are checked against the limits the run read, and over the public API
the run resumes by itself.

## Next Steps
1. Round 4, T003 part two under DECISION F310 D6: the remainder decision is raised only for a job
   that stands final; `do_budget_stop_remainder` and `answer_contract_remainder_on_extend` are
   deleted, with the dated continuations of F269 D9 and F295 D11, D12 and D19; then T004, the lab
   stop of 2026-10-20 rebuilt as a fixture.
2. Resolution lines for R-1370, R-1371 and R-1372 at the gate that proves them.
3. Closure sequence per `docs/roadmap/STATUS_closure_protocol.md`.

## Risks
- Four listed functions and one listed file are touched: every edit shrinks them or stays
  line-neutral, and every shrink lowers its row in the same commit.
- An order's own caps still bind its jobs (DECISION F310 D3, operator question Q19).
- Until round 4 a budget stop still raises the remainder decision beside the budget decision.
