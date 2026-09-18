# Plan — F268 remedy do: the one-command start

Branch: feature/f268-remedy-do, cut from `main` at `8e075bbe` (the merge
commit of pull request 255, F266's closure).

## Goal

`remedy do "<order>"` is one thin sequence walked from data — init, study,
plan, shape, run, ui, apply — that registers an unregistered repo, studies
it once, plans a mission and its jobs, runs them, and stops before apply
unless asked otherwise (`docs/roadmap/features/T2_F268.md`).

## Current Step

Round 3: book round 2's verdict, resolve R-0963, R-0965, R-0808 and
R-0897, register R-0966; repair R-0964's residue, R-0966 and R-0811's `job show`
half; land T003 — `--step-by-step` and `--plan-only` (DECISION F268 D8) —
and list every job's tasks in `do`'s output.

## Next Steps

1. Review round 3 and book its verdict in the next round's first commit.
2. T004: cockpit auto-open unless `--no-ui`, `--apply`, `--contract` and
   the F270 pass-through flags as "not yet available".
3. R-0807: `do` prints measured token totals per role and cost, and the
   builder's context size reaches the run's evidence.
4. T005: the five-line quick start in `remedy --help`.
5. The owned findings still open — R-0892 and R-0933 — each inside the
   slice that reaches it; then the closure sequence.
