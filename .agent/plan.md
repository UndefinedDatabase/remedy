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

Round 27, session 9 — closure algorithm steps 1-2 of
docs/roadmap/STATUS_closure_protocol.md: book round 26 (all six closure
preconditions now hold), then build the evidence bundle (job
`f262-closure`, seven scoped verification runs, EVIDENCESCRIPT template
from `.agent/authored/f009-r33.md`) and the fresh review zip with its
red control, from the clean tree at C1. No `[x]` flip, no README sync,
no `consumed_by` edit, no pull request this round.

## Next Steps

- The closure commit, in ONE commit: STATUS `[x]` line (reviewer-authored,
  carrying the package name, SHA-256, archived path and accepted HEAD =
  this round's C1), README numerals (accepted count, Tier 2 Done cell)
  plus the F262 capability paragraph, `consumed_by=F262` on SU-009.
- Open the pull request; merge under the operator's 2026-09-05
  authorization once hosted CI reads green (checks read as their own
  command first).

## Risks

- The evidence directory and the zip are gitignored and NEVER
  committed; only `.agent/**` changes land in git this round.
- `remedy-review-*.zip` files write under
  `/home/decodeux/Repos/remedy-history/zips`; nothing there is deleted.