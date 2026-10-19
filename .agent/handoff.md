# Handoff — rel-1019: release readiness of PRs 360-365 (2026-10-19)

Session 1 of rel-1019 (operator order "Release Readiness, Operational Reliability and Real Execution
Quality"). Branch `feature/release-readiness` from PR 365's head `7181a2311`, worktree
`.remedy-wt/release-readiness`. Not merged, not deployed. `.agent/STOP`, the supervisor
(`luna-remedy-serve.service`, main `6933bb0e0`, API 1.17), the main checkout and its `.data`, and
every live job untouched. Decisions rel-1019 D1–D5; findings R-1365–R-1367 (all repaired here).

## 1. Git and PR state (read from git and GitHub at the start of the session)
| PR | Branch | Head | API | State |
|---|---|---|---|---|
| 360 | feature/execution-excellence | `9b172a16c` | 1.18 | open, mergeable, no checks |
| 361 | feature/order-cancel | `652029edc` | 1.19 | open, mergeable |
| 362 | feature/adaptive-reliability | `cfd906254` | 1.20 | open, mergeable |
| 363 | feature/verified-repair | `6f26f3c2e` | 1.20 | open, mergeable |
| 364 | feature/close-from-chat | `eb439f9fb` | 1.21 | open, mergeable |
| 365 | feature/release-candidate-verify | `7181a2311` | 1.21 | open, mergeable |
| this | feature/release-readiness | see PR | 1.21 | new |
Each head is an ancestor of the next (`git merge-base --is-ancestor`). All target `main`. Hosted CI
is manual (amend1011), so no PR carries a check. Implemented, tested and pushed: all seven. Merged,
installed, active in the supervisor: none (the service runs main 1.17, started 2026-10-17 17:53).

## 2. The lost handback (rel-1019 D1)
The newest engineering handback is `.agent/handoff.md` on PR 365's branch (commit `0ec6848cc`). The
ZIP of 2026-10-19 09:18 (`remedy-review-20261019-091839-NO_EVIDENCE.zip`) was packaged from the main
checkout at `6933bb0e0` (its manifest: branch `main`, dirty only `?? .agent/STOP`), so it carries
main's last handoff (scale-correctness) and main's stager (no `reports_dir`). Nothing was lost; the
stack is just not on main. A ZIP shows the handoff of the branch it is built from (shown again
below: the ZIP built on this branch carried PR 365's handoff until this file replaced it).

## 3. Findings and repairs
| Item | Status | Reason |
|---|---|---|
| R-1365 Medium: a `cancel_pending` job whose run or walk died before its safe point stayed `running`, its order `cancelling` on every poll | done | D2, `serve_runs.settle_orphaned_job_cancels` at process end and supervisor start |
| R-1366 Medium: a rejected plan's story offered `run`, which every run refuses (`plan_rejected`); order view said `needs_plan_approval` | done | D3, story `stopped`/`declined`, next `none`, end `abandon`; order phase `declined` |
| R-1367 Low: a change Remedy's file check refused read `unknown`, while the 1.21 matrix promised `review_not_passed` | done | D4, code made to match the documented contract |
| Tool missing (exit 127) reads reason `unknown` beside `verification: not_run` | skipped | a precise word is a new closed word (API 1.22), operator's call |
| `order_cancel._runner_alive` duplicates `serve_runs.job_runner_alive` | skipped | same rule with the order in hand; merging them is a refactor, not a release fix |
| Pre-existing R-1172 pollution (`test_do_evidence_package.py` then `test_do_order_budget.py` in one process) | skipped | owned by F297; full gate unaffected |

## 4. Lifecycle acceptance (`tests/ui_server/test_public_api_lifecycle.py`, now 17 rows, real `CommandRunner`)
PR 365's 15 rows stand (never started, waiting for predecessor, orphaned, loop cap, stopped, budget
stop through both doors, answered then stopped, awaiting apply, ended, running alive/gone, two
clients, decline under polling, foreign token, order cancelled while planning across a restart).
Added: plan awaiting approval (`waiting task_plan_approval`, next `answer`, end `abandon`; approve →
`queued`/`run`), plan rejected (R-1366). Restart during cancellation (R-1365):
`test_order_cancel.py` (a real walk dies after `cancel_pending`: order `lost`/`cancelled`, job
`cancelled` with the first reason), `test_serve_runs.py` (a run dies; a terminal-held job keeps
waiting; an order's reaper settles its jobs), `test_serve_daemon.py` (a starting supervisor ends it).

Live jobs (D5 (2)), read with this branch's `remedy client story --json` under a read-only
Bubblewrap mount, nothing changed: 11 open, every one `end: abandon` (4 stopped + `resume`, 1 queued
+ `run`, 4 failed `tests_failed`, 2 failed `budget_exhausted` without a budget question). None runs,
so each abandon ends it at once. Closing them is the operator's action (section 13).

## 5. Repair and verification (real `node --test`, `tests/cli/test_do_verified_repair.py`)
| Scenario | Builds | Story | Verification |
|---|---|---|---|
| broken import → red → diagnostic in repair prompt → green | 2 | done, next apply | passed |
| repair cannot fix (same failure) | 2 | failed `tests_failed` | failed |
| sandbox refused (126) / tool missing (127), simulated at the spawn | 1 | failed `sandbox_unavailable` / `unknown` | not_run |
| budget cannot pay a round | 1 | failed `tests_failed` | failed |
| cancelled before repair | 1 | cancelled | — |
| repair touches an unnamed file of a fenced order | 2 | failed `review_not_passed` (R-1367) | passed, never applied |
| repair rewrites the test script | 2 | failed `review_not_passed` | not_run |
Manual apply kept in every case; nothing reached the repository.

## 6. Workloads, small to large (D5 (3), deterministic fake providers)
| Case | Lane | Jobs/tasks | Planner | Builder/Reviewer (fake) | Verification |
|---|---|---|---|---|---|
| tiny README / same in 10,000 files | bounded | 1/1 | 0 | 2/2 | not_required |
| lab bugfix + test | bounded | 1/1 | 0 | 2/2 | passed (fence blocks the fake's extra file) |
| bug + regression test | bounded | 1/1 | 0 | 2/2 | failed (fake does not fix) |
| multi-file rename | bounded | 1/1 | 0 | 2/2 | passed |
| three independent parts | bounded | 1/3 | 0 | 6/6 | passed |
| medium planned feature | full | 1/1 | 7 (4 study) | 2/2 | passed |
| large one-file auth migration | full | 1/1 | 7 | 2/2 | not_run |
| polyglot package tests | bounded | 1/1 | 0 | 2/2 | passed |
| high-risk plan-only | full | 1/1 | 3 | 0/0 | pending |
| ambiguous bare README | hold | 0 | 0 | 0/0 | — |
Multi-repository: `tests/cli/test_do_several_projects.py` (green). The fake reviewer fails round 1
by design, so 2/2 is the fake's; real runs are 1/1. Study runs once per repository head.

## 7. Real model usage (D5 (1), one sample per side)
| Run | Wall | Calls | Tokens | Builder turns / input | Builder tools |
|---|---|---|---|---|---|
| PR 363 code (exec-1018b D9) | 37.0 s | 2 | 31,709 | 7 / 26,971 | read, ls, edit, write, bash, bash |
| this branch | 38.5 s | 2 | 25,294 | 5 / 20,275 | edit, write, bash, bash |
Local `muse-glimmer:latest` through Pi only; no paid call; `claude-cli` over HTTP stays refused.

## 8. Review reports and ZIP
Empty index on the live ZIP = no captured order (capture is opt-in), same root on both sides (D1).
Proven on real data: the real run above left one report; `make_review_zip.sh` with no argument
(`REMEDY_DATA_DIR` = that run's data root, `REMEDY_REVIEW_DIR` = `.remedy-wt/rel1019-evidence/zips`)
→ `remedy-review-20261019-101509-NO_EVIDENCE.zip`, exit 0, `review_reports/index.json` count 1,
`reports_dir` named, no home path and no secret-like string in the report. Latest ten, failed
runs, redaction: `test_stage_review_reports.py`, `test_review_reports.py` (green). Operator check,
read-only: `ls ~/Repos/remedy/.data/review_reports | wc -l` (0 confirms D1).

## 9. Tests
Focused owners per repair green (counts in the PR). Measured: owner suites of the stack 147 in
22 s; root and guard files 3,655 in 28 s. Slowest modules of the last full run (2026-10-18, 339 s
wall, 6 workers): review ZIP hygiene 47 s CPU (real packagings), supervisor portability 45 s, scale
matrix 43 s. No test deleted or merged: no equivalence was proven. Full gate: once, on the final
commit; result in the PR body.

## 10. API for Universe (1.21, unchanged version)
Discovery: `GET /api/v1/interface` (`version` 1.21, closed word lists). Job card: `GET
/api/v1/jobs/{job}/story` → `state`, `state_detail`, `next` {action, route}, `end` {action, route}
or null. Offer `next` when not `none`; offer "Beenden" whenever `end` is not null, POST its route with
`{"reason": "<non-blank>"}`; after `abandon` read `cancel_pending` (true: poll; since R-1365 it ends
even if the process dies). Answer a question by POSTing `next.route` (`task_plan_approval`: reason
`approve`/`reject`; `token_budget`: `extend` with `answer` `["max_provider_calls=<n>"]` or
`abandon`). Orders: `POST /api/v1/orders` (`capture_review` for the report), `GET
/api/v1/orders/{order}` (`phase`, `jobs[].phase`, `jobs[].story`), `POST
/api/v1/orders/{order}/cancel` (`decline_results`). Value changes inside 1.21 are listed in
`docs/system/api-release-matrix-v1.json` (this branch: R-1365, R-1366, R-1367).

## 11. Merge order
360 → 361 → 362 → 363 → 364 → 365 → this PR, each a merge commit, no squash.

## 12. Deploy and rollback (operator)
Merge in order; in `~/Repos/remedy` `git pull --ff-only`; `sudo systemctl restart
luna-remedy-serve.service`; `GET /api/v1/interface` reads 1.21; `remedy doctor health --json` passes.
Rollback: `git checkout 6933bb0e0` there and restart; no data migration in 360-365 or here.

## 13. Operator approvals needed
Merging and deploying; abandoning the 11 open live jobs (each `POST /api/v1/jobs/{job}/abandon` or
`remedy job abandon <job> --reason ...`); turning capture on by default (product choice); a 1.22
word for a missing test tool.

## Next
Operator: review this PR beside 360-365 and merge in the order above; deploy per section 12.
