# Plan — F260 One world: mission → job → run

Branch: feature/f260-one-world, cut from `main` at b5cd6c20, with `origin/main`
merged in at round 16. Rounds 1 to 16 are reviewed and 2 to 16 PASSED.

## Goal

SESSION 7 REACHES THE SOFT LIMIT — 25 rounds or 7 sessions, whichever comes first,
and this is session 7. The obligation is a SCOPE REPORT and then the standing
default of operator amendment amend0905-throughput: SPLIT-AND-CLOSE, executed on
this session's own authority. F260 closes at the scope it has actually built —
T001 whole, and the RUN side of T002 — and the remainder is carried by a follow-up
feature registered directly after F260, per operator order amend0906-split-placement.

## Current Step

Round 17 RULES the split as DECISION F260 D8, books round 16's verdict and the
reviewer's three prose slips, and rewrites this feature's file so it states what
was built and what moved. The follow-up's registration is the next round's, so
that the ruling is recorded before it is applied.

## Next Steps

1. Register the follow-up feature: its detail file, its STATUS line directly after
   F260's inside the same tier heading, the README counters, the TOTAL_FEATURES
   pin and the six downstream "Depends on" lines, in ONE commit.
2. The integration gate: the full suite at the branch head and at the merge base.
3. Closure part 1: the self-use item, the evidence job and the review zip.
4. Closure part 2: the verdict bookings and the ledger rotation.
5. Closure part 3: the STATUS accepted flip, the README sync, the handback and the
   pull request, which is left UNMERGED as the operator's review window.

## Risks

- README.md and docs/roadmap/STATUS.md may never disagree in any committed state,
  so the registration counters and the closure flip each land in one commit, and
  neither file is touched by any other commit of this session.
- `tests/docs/test_docs_consistency.py` pins the feature count, the id contiguity
  and the filename tier against STATUS.md, so the registration's STATUS line, its
  detail file and the TOTAL_FEATURES pin are one commit or the suite goes red.
