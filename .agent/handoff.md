# Handoff — F254 R1 (Open PR Gate, branch, claim, state reset)
Feature T2_F254 Model alias table & dead-model doctor check · Round R1 · SPLIT ·
branch `feature/f254-model-alias-table`, cut from main at `fc023265`.
Length: 76 lines. Reason for exceeding 60: three mandatory tables (8-row
changed-files, 5-row verification, 4-item status) plus the gate transcript this
round was ordered to record verbatim. No section is dropped.

## Open PR Gate (A)
Pre-check `git status --porcelain` empty, exit 0. `gh pr list` returned EXACTLY the
predicted single entry `{"baseRefName":"main","headRefName":"feature/selfdrive-skill","isDraft":false,"number":185}`, exit 0.
`gh pr merge 185 --merge --delete-branch` exit 0 — fast-forwarded local main
`df39c3fa..fc023265` and deleted the head branch; `gh pr view 185` confirms state
MERGED, mergedAt 2026-08-07T14:26:32Z, mergeCommit `fc023265`. `git checkout main`
("Already on 'main'") and `git pull --ff-only` ("Already up to date.") both exit 0.
`git log --oneline -n 3`: `fc023265` merge PR #185 · `fc099951` · `ecee9194`.
This was the only merge; no other PR existed.

## Commits (range fc023265..HEAD, two)
- `ef71d83e` feat(f254): claim the feature and reset agent state — four receipts +
  STATUS.md + live_review.md + plan.md + context.md. Pushed, exit 0.
- commit 2 `chore(f254): rewrite handoff for the R1 handback` — SHA self-referential
  (this file is its only content), the branch tip at handback; declared, not guessed.

## Changed files — GENERATED from `git diff --numstat fc023265..ef71d83e` (R-0210 fix, not retyped)
| Path | + | - |
|---|---|---|
| .agent/authored/f254-r1-1.md | +15 | -0 |
| .agent/authored/f254-r1-2.md | +42 | -0 |
| .agent/authored/f254-r1-3.md | +44 | -0 |
| .agent/authored/f254-r1-4.md | +37 | -0 |
| .agent/context.md | +28 | -29 |
| .agent/live_review.md | +32 | -220 |
| .agent/plan.md | +35 | -37 |
| docs/roadmap/STATUS.md | +1 | -1 |
| .agent/handoff.md | self-referential | written by commit 2; declared, not omitted |

## Verification (all run for real; docs gate mandatory — docs/roadmap/ changed)
| Command | Result | exit |
|---|---|---|
| `pytest tests/docs/ -q` | 294 passed in 0.44s | 0 |
| `pytest tests/ui_server/test_dashboard_contract.py -q` | 70 passed in 4.32s | 0 |
| `pytest tests/orchestration/test_test_runner.py -q` | 51 passed in 4.35s | 0 |
| `pytest tests/regression/test_resource_safety.py -q` | 21 passed in 10.72s | 0 |
| `pytest tests/cli/test_golden_path.py -q` | 42 passed in 20.44s | 0 |
Equal to the predicted 294 · 70 · 51 · 21 · 42. No full-suite claim is made.
`git status --porcelain` empty after commit 1 + push and after commit 2 + push.
No force-push, no history rewrite, no `git worktree`, no PR created.

## Transport proofs (C — copied with `cp`, never retyped)
`cmp <scratchpad>/f254-r1-N.md .agent/authored/f254-r1-N.md` → no output, exit 0 for N = 1,2,3,4.
sha256: r1-1 `2870e398e1e0ed62c3bb96055fa82cc2c6b1663ccb2e3c89cf73f3808b5d3bad` · r1-2 `e37a8d86082330f75bdd8b1bbee3aba6dc591486d91da04cee7fd6ca8554c055`
r1-3 `40ee9f357a925bf098600ddb7ad0edcf245f577018aa0b858ca905e435f2966b` · r1-4 `d4cffe583d74368fdd514f3688b647e07813cad1ae1bd80c856548c30c75592c`
Full-file applications: `cmp` r1-2↔live_review.md, r1-3↔plan.md, r1-4↔context.md — all exit 0.

## STATUS.md counts (C1, REWRITE shape)
FROM was exactly 1x before the edit (line 66). After: FROM **0x** (grep exit 1) and
TO **1x** (grep exit 0). `grep -c '^- \[~\]' docs/roadmap/STATUS.md` → **1**, exit 0.

## Findings, deviations, assumptions
0 open findings; next free ID R-0211; none raised this round. No deviations — every
prediction in the step block was checked against real output and matched. For the
record, not a deviation: Rule A5's first unchecked line is F103; claiming F254 ahead
of it is the planner's deliberate choice, stated in the authored context.md.

## Item status
| Item | Status | Reason |
|---|---|---|
| A Open PR Gate | done | PR #185 MERGED; main at fc023265 |
| B branch | done | feature/f254-model-alias-table |
| C receipts + application | done | 4 cmp + 3 full-file cmp, all exit 0 |
| D commit, push, handoff | done | ef71d83e pushed; this file is commit 2 |

## Next
Reviewer re-reads `git diff fc023265..HEAD` and re-runs the five gates. On PASS,
LAST_REVIEWED_SHA advances to the tip and R2 opens with the ground inspection the
feature file demands, then the alias module. No PR exists for this branch yet.
