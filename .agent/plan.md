# Plan — amend0825-dogfood-findings

Branch: feature/amend0825-dogfood-findings, cut from `main` at `6325ac2f`, the
merge commit of pull request #213. Operator collection order amend0825, no
self-drive loop; the operator prompt carries the authorization for the alias
repoint and for merging this branch's own pull request.

## Goal
Six findings from the first operator dogfooding run (project ~/demo-remedy,
jobs edbbc42bba4c4b00 and e984ec1943bb422f) triaged by ONE rule: repaired in
code only when the repair is surgical AND a regression test proves it,
otherwise recorded as a dated "Operator finding (2026-08-25, dogfooding)"
paragraph in the owning file under docs/roadmap/features/.

## Current Step
All six items are decided and committed. The first hosted CI run was RED with
seven failures, all of this round's own making, and repairing them is this
round's work (AGENTS.md amend0820 gate autonomy). Remaining: land the repair,
re-watch the hosted run to green, merge, and confirm zero open pull requests.

The seven failures, their causes and their repairs are tabled in
`.agent/handoff.md`; they are not restated here.

| Item | Status | Reason |
|------|--------|--------|
| 1 — do run budget crash | done | repaired; tests/cli/test_do_cmd_pingpong_budget.py |
| 2 — teacher blind to job runs | done | resolver repaired; narration residue recorded in T5_F255.md |
| 3 — empty token ledger | deviated | design gap, not wiring — recorded in T2_F103.md |
| 4 — promotion dead end | done | recorded in T0_F017.md, three facets, guard untouched |
| 5 — doctor lanes from a foreign cwd | done | repaired; tests/cli/test_worker_facade_cmd.py |
| 6 — dead built-in model ids | done | aliases repointed; do run header names the model |

## Next Steps
1. `gh pr create`, then `gh run watch` until the hosted run is green.
2. Merge the pull request and delete the branch; end at zero open PRs.
3. The next session's first reviewed round decides what to do with the three
   recorded findings; none of them is claimed here.

## Risks
- `.agent/STOP` is on disk, untracked, from the stopped F031 R10 round. It
  governs the self-drive loop, not this order, and is never deleted here.
- Finding 3 leaves job-path cost invisible until one of the three shapes the
  F103 entry weighs is chosen. Nothing in this branch narrows that choice.
- Finding 4 leaves a blocked promotion with no next step in the output. The
  guardrail is correct and was deliberately not touched.
- `remedy plan next` reports F031, not F022: F022 closed on 2026-08-23.
