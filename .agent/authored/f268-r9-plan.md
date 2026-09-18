# Plan — F268 remedy do: the one-command start

Branch: feature/f268-remedy-do, cut from `main` at `8e075bbe` (the merge
commit of pull request 255, F266's closure).

## Goal

`remedy do "<order>"` is one thin sequence walked from data — init, study,
plan, shape, run, ui, apply — that registers an unregistered repo, studies
it once, plans a mission and its jobs, runs them, and stops before apply
unless asked otherwise (`docs/roadmap/features/T2_F268.md`).

## Current Step

Round 9: book round 8's verdict; DECISION F268 D17. Land D16 (1) to (3):
every `remedy do` walks the sequence, the autorun branch and the four
flags outside the Design's list leave, smoke section `12ao` becomes a
`do` sequence run (R-0933).

## Next Steps

1. Review round 9 and book its verdict in the next round's first commit.
2. A deletion round: `run_do`, `export_do_run_json`, `summarize_do_run`
   and `dry_run_autorun`, left without a caller by round 9, leave with
   their tests.
3. The closure sequence (docs/roadmap/STATUS_closure_protocol.md).
