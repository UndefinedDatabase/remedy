# Handoff — exec-1018c: release candidate of PRs 360-364 (2026-10-18)

Session 1 of exec-1018c. Branch `feature/release-candidate-verify` from PR 364's head `eb439f9fb`,
worktree `.remedy-wt/rc-verify`. Not merged, not deployed. `.agent/STOP`, the supervisor
(`luna-remedy-serve.service`), the live checkout (main `6933bb0e0`) and its `.data` untouched; the
live data root was never read (the operator's settings deny it). Decisions exec-1018c D1–D6;
findings R-1361–R-1364. This is no claim that Remedy is perfect: what is below is what was shown.

## 1. Git and PR dependency state (verified directly)
| PR | Branch | Head | Base | API |
|---|---|---|---|---|
| 360 | feature/execution-excellence | `9b172a16c` | main `6933bb0e0` | 1.18 |
| 361 | feature/order-cancel | `652029edc` | 360 | 1.19 |
| 362 | feature/adaptive-reliability | `cfd906254` | 361 | 1.20 |
| 363 | feature/verified-repair | `6f26f3c2e` | 362 | 1.20 |
| 364 | feature/close-from-chat | `eb439f9fb` | 363 | 1.21 |
| this | feature/release-candidate-verify | see PR | 364 | 1.21 |
Every PR targets `main`; each head is an ancestor of the next (checked with `git merge-base
--is-ancestor`). The installed service runs main (1.17); none of 360-364 is deployed.

## 2. Independent findings and fixes
| Item | Status | Reason |
|---|---|---|
| R-1361 High: abandon of an order's job a dead walk left `running` answered `cancel_pending` forever | done | D1, `serve_runs.job_runner_alive` |
| R-1362 High: R-1359 recurred through the run log (answered budget stop, later person's stop) | done | D2, queue reads `open_budget_decision_id`; 1,032/1,600 → 0 |
| R-1363 Medium: a fenced order's round (a repair's too) could change an unnamed file and complete | done | D3, `unrequested_file_changed` |
| R-1364 Low: the review ZIP's "none" never said which data root it read | done | D4 |
| Stale HTTP doc: story `queued`, `run`, `resume` (1.19) missing | done | D5 |
| P1 7 builder targeting from the whole prompt | done | D6, deterministic replay; real turns unmeasured |
| Pre-existing: `test_do_evidence_package.py` → `test_do_order_budget.py` red in one process | skipped | R-1172's leaked tripwire class (F297); reproduced identically on `eb439f9fb` |

## 3. Lifecycle matrix and budget answers (`tests/ui_server/test_public_api_lifecycle.py`)
Through `answer_public_api_get/post` and the supervisor's own `CommandRunner` (the real `remedy`
child); a fresh runner re-reads the disk after each action (a restart). Client token scoped to the
job's project for every row; a foreign project's token gets 403 and runs nothing.
| State | Story before | Action (body `{"reason": …}`) | Answer | After (story / digest active) | A process may still run |
|---|---|---|---|---|---|
| order planning | order `planning` | `POST /orders/{o}/cancel` | `cancelling`, then `cancelled` after the walk | `cancelled`, no jobs; 2nd cancel `already_cancelled` | the walk until its next step |
| never started | `queued`, next `run`, end `abandon` | end | `cancelled` | `stopped/cancelled`, end null / no | no |
| waits for job | `queued {after_job}`, next `none`, end `abandon` | end | `cancelled` | ended / no; predecessor untouched | no |
| predecessor cancelled | `queued`, next `none`, end `abandon` | end | `cancelled` | ended / no | no |
| blocked by loop cap | `failed budget_exhausted`, no budget question | end | `cancelled` | ended / no | no |
| stopped (resumable) | `stopped`, next `resume`, end `abandon` | end | `cancelled` | ended / no | no |
| budget stop | `waiting token_budget`, next `answer`, end `abandon` | answer `abandon` or end | `cancelled` | ended / no, question closed | no |
| budget stop answered, then stopped by the person | `stopped`, next `resume`, end `abandon`, no question | end | `cancelled` | ended / no | no |
| awaiting apply | `done`, next `apply`, end `decline` | end (blank reason → 400 `missing_argument`) | declined | `stopped/declined`, changes still listed / no; abandon 409 | no |
| running, runner alive | end `abandon` | end | `cancel_pending: true`, still `running` | active until its safe point | yes |
| running, runner gone | end `abandon` | end | `cancelled` at once (first reason kept) | ended / no | no |
| failed / cancelled / declined | end null | abandon | 409 `job_not_cancellable` / `already_cancelled` / `already_declined` | unchanged | no |
| two clients | end `abandon` | two runners at once | both 200, one request | `cancelled` once | no |
| decline under polling | `done` | end | declined | every poll reads `done/decline` or `stopped/null` | no |

## 4. Verified repair (PR 363), independently checked
Real `node --test` in `tests/cli/test_do_verified_repair.py`: red → diagnostic in the repair
prompt → green (completed, apply manual); unchanged failure → one repair, `test_failure_unchanged`,
blocked; budget for one round missing → no repair; cancel during review → no repair, `cancelled`;
exit 126 (sandbox) / 127 (tool) → `not_run`, never repaired. Added here: a repair that rewrites the
test script → `test_command_changed`, `not_run`, blocked; a repair that touches an unnamed file of a
fenced order → blocked (R-1363). Edge accepted: only the previous round is compared, so failures
alternating A/B run to the repair cap (bounded).

## 5. Execution scale by task type
`tests/orchestration/scale_matrix.py` holds 40 cases with exact lanes and call counts (tiny edit,
one-file bug, bug + test, multi-file, three independent parts, medium HTTP, large repo tiny edit,
high-risk auth plan, polyglot with tests, plan-only, verify-only, ambiguous, sandbox refusal);
multi-repository ordering is `tests/cli/test_do_several_projects.py`, cancellation at each stage
`tests/orchestration/test_order_cancel.py`. All green on this branch; none added (all shapes covered).

## 6. Real model measurements versus fake-provider results
Real (exec-1018b D9, local `muse-glimmer` via Pi, not repeated here): builder 6-7 turns, ~27k input
tokens per call, ~3.9k per turn; reviewer ~3k. Simulated here (D6): the context the builder is
handed, replayed over those recorded prompts: lab add and rules runs now get the deliverable and the
new test's style file instead of README/package.json/format.js/AGENTS.md (−26 %, −21 % chars).
Effect on real turns: NOT measured (another session's `pi` held the shared Ollama). Fake-provider
call counts are pinned by the scale matrix and say nothing about tokens.

## 7. Reporting and ZIP
`tests/orchestration/test_serve_daemon.py::test_http_orders_with_capture_review_leave_reports…`:
a real supervisor, three HTTP orders with `capture_review: true` (completed, budget-stopped,
cancelled) → three reports, the stager and the no-argument ZIP carry all three, no secret and no
home path in any byte. Installed configuration: the service (`~/.local/bin/remedy`, no
`REMEDY_DATA_DIR`, no `data_dir`) writes to `~/Repos/remedy/.data`; build the ZIP from that checkout
(or set `REMEDY_DATA_DIR`). The index now names `reports_dir`, so a ZIP built elsewhere says where it
looked. Empty case: "no review report exists in <dir>". No report was fabricated.

## 8. CLI/API contract changes
This branch: none (stays 1.21). Behaviour inside 1.21: R-1361 (abandon answers `cancelled`, not a
pending cancel nobody reads), R-1362 (no unanswerable budget question), R-1363 (a fenced order's
stray change blocks; story reads `failed`/`review_not_passed`). The stack: `docs/system/api-release-
matrix-v1.json` — additive only from 1.17 (3 routes, 3 commands, keys and words; nothing removed),
with each version's value changes (1.19: `planning` → `queued`; reason `cancelled` → `stopped` for a
resumable stop; `next` `none` → `run`/`resume`).

## 9. Tests
Focused owners per step (all green; listed in the PR). Full local gate: once, on this branch's final
commit; commit, tree, command, interpreter, result and wall time are in the PR body.

## 10. Remaining risks
- A job held `running` by a crashed TERMINAL run (no supervisor record) still answers
  `cancel_pending`; ending it there could race a live process. Supervisor-started work is covered.
- R-1363's refusal reads `review_not_passed` in the story (as protected-file refusals do); a precise
  reason word is an API change (1.22), the operator's call.
- Derived stop reasons (`sr:derived_no_repo`, `sr:derived_test_fail`) are counted by the digest for
  ended jobs; only jobs without a target repository or legacy test events reach them, never an
  order's job of 360-364.
- R-1172 test pollution can turn a hand-picked serial selection red; the full gate is unaffected.
- Real-model effect of D6 unmeasured; Pi turn waste beyond it is model compliance.

## 11. Merge order
360 → 361 → 362 → 363 → 364 → this PR. Each with a merge commit, no squash (the later branches carry
the earlier commits).

## 12. Deployment and rollback (operator)
Deploy: merge in order; in `~/Repos/remedy` (the service's checkout) `git pull --ff-only`;
`sudo systemctl restart luna-remedy-serve.service`; check `GET /api/v1/interface` reads `1.21` and
`remedy doctor health --json` passes. Rollback: `git checkout 6933bb0e0` in that checkout (main
before the stack; no data migration exists in 360-364, records written by 1.21 stay readable as
plain job JSON) and restart the service; `.agent/STOP` stays as the operator left it.

## 13. What Universe Chat consumes after release
Per job card: `GET /api/v1/jobs/{job}/story`; show `state`/`state_detail` words from
`GET /api/v1/interface` `story`; offer `next` (`apply`, `answer`, `run`, `resume`) and, whenever
`end` is not null, a "Beenden" button that POSTs `end.route.path` with `{"reason": "<text>"}`
(non-blank: `decline` refuses a blank one with 400 `missing_argument`). After `abandon`, read
`cancel_pending`: true means still running until its safe point; poll the story. Offer a budget
question only when the story's `state` is `waiting` with `question: token_budget`, answering
`POST next.route.path` with `{"reason": "extend", "answer": ["max_provider_calls=<n>"]}` or
`{"reason": "abandon"}`. Per order: `POST /api/v1/orders` (with `capture_review: true` for the
checkbox), poll `GET /api/v1/orders/{order}` (`phase`, `jobs[].story`), cancel with `POST
/api/v1/orders/{order}/cancel` (`decline_results: true` to also decline waiting results). Remote
providers: builder `pi|claude|fake`, reviewer `pi|ollama|claude|fake`; `claude-cli` is refused with
400 `api_provider_not_offered`.

## Next
Operator: review this PR beside 360-364 and merge in the order above; deploy as in 12.
