# Plan — F260 One world: mission → job → run

Branch: feature/f260-one-world, cut from `main` at b5cd6c20, `origin/main` merged
in at round 16. Rounds 1 to 17 are reviewed; round 1 FAILED and was repaired, and
2 to 17 PASSED.

## Goal

Session 7 reaches the amend0905-throughput soft limit of 7 sessions, so this
session performs SPLIT-AND-CLOSE on its own authority. DECISION F260 D8, recorded
in round 17, closes F260 at the scope it built — T001 whole, and the RUN side of
T002 — and moves the remainder to a follow-up feature registered directly after
F260 per operator order amend0906-split-placement.

## Current Step

Round 18 REGISTERS that follow-up as F272: its detail file, its STATUS line
between F260's and F261's, the README counters, the `TOTAL_FEATURES` pin and the
six downstream "Depends on" lines, all in ONE commit, because the docs suite pins
those values against each other.

## Next Steps

1. The integration gate: the full suite at the branch head and at the merge base,
   per docs/agents/integration_gate.md.
2. Closure part 1: the self-use item, the evidence job and the review zip.
3. Closure part 2: the verdict bookings and the ledger rotation.
4. Closure part 3: the STATUS accepted flip, the README sync, the handback and the
   pull request, which is left UNMERGED as the operator's review window.

## Risks

- README.md and docs/roadmap/STATUS.md may never disagree in any committed state.
  This round moves both plus the pin in one commit; the closure flip moves both
  again in one commit; no other commit of this session touches either.
- The self-use queue is EXHAUSTED — all ten entries carry a `consumed_by` — so
  closure precondition 6 runs `generate_and_append_if_empty` FIRST and records
  `self-use NONE (queue exhausted)` only after that also answers `None`.
