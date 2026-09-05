# Plan — F262 List commands v2 (dates, sort, filter)

Branch: feature/f262-list-commands-v2, cut from `main` after pull
request 235 was merged at the Open PR Gate.

## Goal

Every list command shows a CREATED and an UPDATED date and carries the
same `--sort <field> [--desc] --since <when> --until <when> --limit <n>`
flags, with newest-first as the DEFAULT everywhere, without a flag
(docs/roadmap/features/T2_F262.md, scoped by DECISION F262 D4; the nine
remaining wirings are F267's per DECISION F262 D5).

## Current Step

Round 29, session 9 — the repair of round 28's red docs gate and the
pull request. Books RECORD28 (FAIL on G6, all else held), registers
FINDING R-0797 (the reviewer's README slice named F267 inside an
"Accepted" block), applies one README pair that names no feature id,
re-runs `tests/docs/` to 295, then `gh pr create`. The STATUS `[x]`
line, README numerals and `consumed_by=F262` landed at `423bc28d` and
are untouched.

## Next Steps

None on this branch — F262 closes with this round's pull request. The
reviewer reads the PR checks, merges under the operator's 2026-09-05
authorization, and verifies `main`. R-0797 stays `Landed:` until the
next feature's first round books its `Done:`.

## Risks

- A README repair after the STATUS flip is the F112 R30 shape; it is
  declared, not hidden, and the flip commit itself is not rewritten.