# Plan — F268 remedy do: the one-command start

Branch: feature/f268-remedy-do, cut from `main` at `8e075bbe` (the merge
commit of pull request 255, F266's closure).

## Goal

`remedy do "<order>"` is one thin sequence walked from data — init, study,
plan, shape, run, ui, apply — that registers an unregistered repo, studies
it once, plans a mission and its jobs, runs them, and stops before apply
unless asked otherwise (`docs/roadmap/features/T2_F268.md`).

## Current Step

Round 2: book round 1's verdict and findings R-0963, R-0964 and R-0965;
repair all three; land T002 — the shape read from the mission plan,
`--force-job`, `--force-mission`, and tasks bounded by deliverables with
one validator (DECISIONs F268 D5 to D7).

## Next Steps

1. Review round 2 and book its verdict in the next round's first commit.
2. T003: `--step-by-step` halts at the safe points and `--plan-only`.
3. T004: cockpit auto-open unless `--no-ui`, `--apply`, `--contract` and
   the F270 pass-through flags as "not yet available".
4. T005: the five-line quick start in `remedy --help`.
5. The owned findings still open — R-0807, R-0808, R-0811, R-0892,
   R-0897, R-0933 — each inside the slice that reaches it; then the
   closure sequence.
