# Plan — F268 remedy do: the one-command start

Branch: feature/f268-remedy-do, cut from `main` at `8e075bbe` (the merge
commit of pull request 255, F266's closure).

## Goal

`remedy do "<order>"` is one thin sequence walked from data — init, study,
plan, shape, run, ui, apply — that registers an unregistered repo, studies
it once, plans a mission and its job, runs it, and stops before apply
unless asked otherwise (`docs/roadmap/features/T2_F268.md`).

## Current Step

Round 1: claim F268 and land T001 — the step list as data in
`packages/orchestration/do_sequence.py`, bare `remedy do` routed through
it, study-once recorded on the project record, one test per step
boundary on the fake provider. DECISIONs F268 D1 to D4 bind it.

## Next Steps

1. Review round 1 (T001) and book its verdict in the next round's first
   commit.
2. T002: the planner's structured shape output, `--force-job`,
   `--force-mission`, and the granularity ceilings (R-0808).
3. T003: `--step-by-step` halts at the safe points and `--plan-only`.
4. T004: cockpit auto-open unless `--no-ui`, `--apply`, and the F270
   pass-through flags as "not yet available".
5. T005: the five-line quick start in `remedy --help`.
6. The owned findings R-0807, R-0811, R-0892, R-0897 and R-0933, each
   inside the slice that reaches it; then the closure sequence.
