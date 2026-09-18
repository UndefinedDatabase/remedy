# Plan — F268 remedy do: the one-command start

Branch: feature/f268-remedy-do, cut from `main` at `8e075bbe` (the merge
commit of pull request 255, F266's closure).

## Goal

`remedy do "<order>"` is one thin sequence walked from data — init, study,
plan, shape, run, ui, apply — that registers an unregistered repo, studies
it once, plans a mission and its jobs, runs them, and stops before apply
unless asked otherwise (`docs/roadmap/features/T2_F268.md`).

## Current Step

Round 7: book round 6's verdict; DECISION F268 D15 (amends D14); land
T005, the five-line quick start in `remedy --help` and the README, with
the test that runs it; R-0892's `SKILL.md` half.

## Next Steps

1. Review round 7 and book its verdict in the next round's first commit.
2. The `do` flag list of T2_F268.md's Design: bare `do` honours
   `--project`, the budget flags and the role flags; the flags outside the
   list and the non-bare `do run` autorun path leave (a deletion round),
   which closes R-0933.
3. The closure sequence (docs/roadmap/STATUS_closure_protocol.md).
