# Handoff — exec-1018b: verified repair, reliable evidence, adaptive execution (2026-10-18)

Session 1 of exec-1018b. Branch `feature/verified-repair` from PR 362's head `cfd906254` (PR 362 is on
PR 361's `652029edc`, on PR 360's `9b172a16c`); worktree `.remedy-wt/verified-repair`. **Merge
order: PR 360, PR 361, PR 362, then this PR.** Not merged, not deployed; `.agent/STOP`, the
supervisor (`luna-remedy-serve.service`, `remedy serve start` on main) and the live checkout (main
`6933bb0e0`) untouched; its `.data` was never read (the operator's settings deny it). Outside the
roadmap queue: F078 stays next. Decisions exec-1018b D1–D10; findings R-1354–R-1358.

## Findings and items
| Item | Status | Reason |
|---|---|---|
| R-1351 red tests after review: no repair from that evidence | done | D1; real run 3 (D9) |
| R-1354 repair round after a reviewer pass carried no test evidence | done | D1 |
| R-1355 shell exit 126/127 read as a failed test | done | D2 |
| P0 2 review reports export | done | D3: path proven over HTTP on this branch and on main; no captured runs |
| R-1356 walk order outlived its walk (`_WALK_ORDER_DIR`) | done | D4 |
| R-1357 job cancelled during its final gate completed and was applied | done | D5 |
| R-1358 wording decides whether a guarded file is changed | done | D6; matrix 12/21 → 21/21 |
| P1 5 project rules per turn | done | D7: lossless dedupe |
| P1 6 experience reuse | done | D8: measured, nothing shipped |
| P1 7 test-suite efficiency | done | D10 |
| Real local-model runs (3) | done | D9 |
| Public API | done | no route, key or word added; route text of job abandon updated; stays 1.20 |

## Verification
Focused owner selections green per step; one investigative full run on `d54ff1e96` (D10). The one
full local gate on the final commit is recorded in the PR body (commit, tree, command, interpreter,
result).

## Universe API handoff (no new fields; behaviour within the 1.20 contract)
- A required test that fails in a job's last task now gets one repair round: a running job's story
  shows round 2 (`task_round_repaired`); `verification` stays `{status, required}`; a job held at
  its task by red tests reads `tests_failed` as before. `verification.runs` (CLI and order JSON)
  may hold a `source: "task"` run when the gate never ran.
- `POST /api/v1/jobs/{job}/abandon` on a running job (`cancel_pending: true`) now always ends the job
  `cancelled`, also when the cancel lands while its final checks run; such a job is never applied.
- Story reason `tests_failed` / `sandbox_unavailable` / verification `not_run` unchanged; a test
  script whose tool is missing (exit 127) is `not_run`, never `failed`.
- Review reports: `capture_review: true` on `POST /api/v1/orders` is the only switch; reports exist
  only for orders that set it.

## Next
Operator: review and merge PR 360, 361, 362, then this PR; restart `remedy serve` to load the code.
Open: context files misread as required still block correct work on unknown wordings (D6); capture
by default is the operator's decision (D3).
