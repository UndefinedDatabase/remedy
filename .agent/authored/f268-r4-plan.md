# Plan — F268 remedy do: the one-command start

Branch: feature/f268-remedy-do, cut from `main` at `8e075bbe` (the merge
commit of pull request 255, F266's closure).

## Goal

`remedy do "<order>"` is one thin sequence walked from data — init, study,
plan, shape, run, ui, apply — that registers an unregistered repo, studies
it once, plans a mission and its jobs, runs them, and stops before apply
unless asked otherwise (`docs/roadmap/features/T2_F268.md`).

## Current Step

Round 4: book round 3's verdict, resolve R-0964 and R-0966, register
R-0967; repair R-0967 and the rest of R-0811's placeholder tips; land
T004 — the detached cockpit, `--apply`, and the F269/F270 flags refusing
as not yet available (DECISION F268 D9).

## Next Steps

1. Review round 4 and book its verdict in the next round's first commit.
2. R-0807: `do` prints measured token totals per role and cost, and the
   builder's context size reaches the run's evidence.
3. R-0892: a `do` run's evidence package passes the required-artifact
   check of `scripts/build_review_manifest.py`.
4. T005: the five-line quick start in `remedy --help`, and R-0933's
   non-bare `do run` remainder.
5. The closure sequence.
