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

Round 28, session 9 — the closure commit and the pull request. Books
round 27 (evidence job `f262-closure`, package `remedy-review-20260905-112903-READY_FOR_REVIEW.zip`, accepted HEAD
`a5896aa6`), then ONE commit flips STATUS to `[x]`, syncs the
README numerals and capability list, and sets `consumed_by=F262` on
SU-009 (docs/roadmap/STATUS_closure_protocol.md algorithm step 5); then
`gh pr create`. The merge follows under the operator's 2026-09-05
authorization once hosted CI reads green.

## Next Steps

None on this branch — F262 closes with this round's pull request. The
reviewer reads the PR checks, merges, and verifies `main`. The next
feature is claimed per Rule A5 in a fresh session.

## Risks

- README's derived numerals (accepted count, Tier 2 Done cell) move the
  moment STATUS flips; both land in the SAME commit as the flip (F112
  R30 lesson: a split closure commit went red on `tests/docs/`).