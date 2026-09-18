# Plan — F268 remedy do: the one-command start

Branch: feature/f268-remedy-do, cut from `main` at `8e075bbe` (the merge
commit of pull request 255, F266's closure).

## Goal

`remedy do "<order>"` is one thin sequence walked from data — init, study,
plan, shape, run, ui, apply — that registers an unregistered repo, studies
it once, plans a mission and its jobs, runs them, and stops before apply
unless asked otherwise (`docs/roadmap/features/T2_F268.md`).

## Current Step

Round 10: book round 9's verdict and resolve R-0933; delete `run_do`,
`export_do_run_json`, `summarize_do_run` and `dry_run_autorun`, left
without a caller by round 9, with their tests; the do guide describes
the sequence.

## Next Steps

1. Review round 10 and book its verdict in the next round's first commit.
2. The closure sequence (docs/roadmap/STATUS_closure_protocol.md).
