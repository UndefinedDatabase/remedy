# Plan — F268 remedy do: the one-command start

Branch: feature/f268-remedy-do, cut from `main` at `8e075bbe` (the merge
commit of pull request 255, F266's closure).

## Goal

`remedy do "<order>"` is one thin sequence walked from data — init, study,
plan, shape, run, ui, apply — that registers an unregistered repo, studies
it once, plans a mission and its jobs, runs them, and stops before apply
unless asked otherwise (`docs/roadmap/features/T2_F268.md`).

## Current Step

Round 5: book round 4's verdict, resolve R-0967 and R-0811, register
R-0968, R-0969 and R-0970 (owned by F273); repair R-0968 as DECISION
F268 D12 amends D10 — a multi-job walk runs job 1 and names the jobs
that wait for its committed output — and R-0969; land R-0807's F268 half
(DECISION F268 D11).

## Next Steps

1. Review round 5 and book its verdict in the next round's first commit.
2. R-0892: a `do` run's evidence package passes the required-artifact
   check of `scripts/build_review_manifest.py`.
3. T005: the five-line quick start in `remedy --help`, and R-0933's
   non-bare `do run` remainder.
4. The closure sequence.
