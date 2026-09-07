# Plan — F272 One world completion

Branch: feature/f272-one-world-completion. Rounds 1 to 25 PASSED except round 2 (premise
corrected by DECISION F272 D2) and round 21 (R-0824, repaired by round 22). T001, T002
and T003 are COMPLETE. T004 is part-done and its remainder is being split off.

## Goal

Finish what F260 began: a Job that carries MANY runs, every consumer on the unified model,
and the classic runner, its resolver and the prototype cluster deleted. Task slicing per
`docs/roadmap/features/T2_F272.md`. Session 12 reaches the soft limit of 12 sessions, so
this session's goal is the SPLIT-AND-CLOSE default, not more building.

## Current Step

Round 26, the split half: register the remaining scope as F274 directly after F272 per
amend0906-split-placement, in ONE atomic ledger commit, and record the move as DECISION
F272 D16 in `.agent/decisions.md`.

## Next Steps

1. F272's own Built State section, naming which slices moved to F274. Closure
   precondition 4 needs it and this file has no such section yet.
2. The integration-gate round — the full suite on the branch and at the fork point, per
   `docs/agents/integration_gate.md`. Closure precondition 2 needs it and F272 has never
   run one.
3. The self-use round closure precondition 6 requires: generate an item, since the queue
   holds no pending one, plan it, run it, register every defect string it returns.
4. The closure sequence: evidence job, fresh review zip, ledger rotation, the STATUS `[x]`
   flip with the README sync in the same commit, then the PR.
5. F274 owns the atomic record flip and the cluster deletion. None of that work starts on
   this branch.

## Risks

- Four open findings are High — R-0803, R-0804, R-0806 and R-0807. All four are booked to
  F273's T001 by the 2026-09-06 triage, so the close is PASS_WITH_RISKS and names them
  rather than pretending the set is empty.
- A failing review-zip build is a closure BLOCKER; the round that hits one stops rather
  than closing.
