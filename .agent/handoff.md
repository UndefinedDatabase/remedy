# Handoff — exec-1018: adaptive execution, complete safety, real-world reliability (2026-10-18)

Session 1 of exec-1018. Branch `feature/adaptive-reliability` from PR 361's head `652029edc` (PR 361
is on PR 360's `9b172a16c`); worktree `.remedy-wt/adaptive-reliability`. **Merge order: PR 360, then
PR 361, then this PR.** Not merged, not deployed; `.agent/STOP`, the supervisor (`remedy serve`,
running on main) and the live checkout (main `6933bb0e0`, editable install) untouched. Outside the
roadmap queue: F078 stays next. Decisions exec-1018 D1–D10; findings R-1345–R-1353.

## Findings and items
| Item | Status | Reason |
|---|---|---|
| R-1343 loop half / R-1345 refused test command, post-mortem class | done | D1 |
| R-1346 planner call in flight not cancellable, fallback plan after cancel | done | D2; real Ollama: 0.246 s |
| R-1347 rules only short and root, never the reviewer | done | D3 |
| R-1348 context/forbidden named files required | done | D4 |
| R-1349 plan-only / verify-only orders change files | done | D4 |
| R-1350 independent parts one task | done | D4 |
| R-1351 red tests after review: no repair from that evidence | skipped | registered; needs an A/B, `run_job` at its row |
| R-1352 tiny full-lane order pays narration | done | D7 |
| R-1353 no lesson or study card reaches a walk's model call | skipped | measured (D8); product decision |
| P1 7 efficiency | deviated | measured in calibration; R-1343 and R-1352 repaired, tool set unchanged |
| P1 8 Go/Rust verification | done | D5 |
| P1 9 historical lessons | done | experiment D8: nothing reaches a prompt, nothing built |
| P1 10 test audit | done | D9 |
| Local calibration (4 cases) | done | D6 |
| API/interface 1.20 | done | D10 |

## Calibration (real model, local Ollama `muse-glimmer:latest`, disposable repositories)
c1 lab README 25.8 s / 18,953 tok / builder 4 turns, passed; c2 lab add 37.0 s / 28,419 / 6 turns,
BLOCKED by real `npm test` (R-1351); c3 two-file rename 22.3 s / 17,211 / 4 turns, correct diff,
passed; c4 high-risk plan-only cancelled in its mission-plan call: ended 0.246 s after the request.
Evidence and the harness: session scratchpad `calib/` (not committed).

## Verification
Focused owner and neighbour selections green per step (see the PR body for the list); repo-wide
guards 3,816 green; campaign nodes 68/68 green alone with an empty HOME. The one full local gate
on the final commit is in the PR body (command, tree, interpreter, result).

## Next
Operator: review and merge PR 360, then PR 361, then this PR; restart `remedy serve` to load the
code. Then: R-1351 A/B (one repair round from a red DoD) and R-1353 (lessons) as one paydown.
