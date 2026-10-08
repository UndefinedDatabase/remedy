# Handoff — F253 round 20: book round 19, S6b-2: a client token's job writes stay inside its policy

## Session

SESSION 5 of feature F253 · round 20 · rounds so far 20

Context self-assessment: the reviewer's context is workable after two rounds; the session continues
with S7.

Fortschritt: ~88 % (S1 to S6 · S7 open, then hardening and closure) — Schätzung

## Range

Review of `be49a81a155e93c10880c4e7debc6e5421902de4`..`82706dbaf63713a1c6ab5bf699422233a84c65c0`
(the last commit before this handback, C3).

## Commits

### eebc09727 F253 R20 C1: book round 19, DECISION F253 D17, the plan and the block

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f253-r20.md` | 186/0 | new file, byte copy of `block.md` (sha256 `8ccc048e8be41871498e69385e2e5c235d51c491fbd78f78bf5d258212651870`) |
| `.agent/decisions.md` | 10/0 | `append-decisions.txt`'s bytes appended: DECISION F253 D17 |
| `.agent/live_review.md` | 2/0 | `append-live_review.txt`'s bytes appended: round 19's gate entry, VERDICT PASS |
| `.agent/plan.md` | 11/12 | `dry-plan.md`, byte for byte |

### 61f376749 F253 R20 C2: the budget decision's predicate lives in decision_queue

| Path | +/- | Reason |
|---|---|---|
| `apps/cli/commands/decision.py` | 3/1 | `_is_budget_decision_id` now calls `is_budget_decision_id` |
| `packages/orchestration/decision_queue.py` | 7/0 | new public `is_budget_decision_id`, below `budget_decision_id` |
| `tests/orchestration/test_decision_queue.py` | 17/0 | new: the predicate is true for the two ids `budget_decision_id` builds and false for four others |

### 82706dbaf F253 R20 C3: a client token's decisions, declines and applies stay inside its projects and ceilings

| Path | +/- | Reason |
|---|---|---|
| `docs/system/public-http-api-v1.md` | 6/3 | hand-written part: "Until the next slice" sentence removed; the policy paragraph names the project rule and the budget ceilings |
| `packages/orchestration/api_clients.py` | 38/2 | `client_lists_project`, `client_budget_answer_refusal`, `client_order_refusal` uses the first; docstring names D17 |
| `packages/orchestration/public_api.py` | 54/1 | `_client_job_refusal` and its use in `answer_public_api_post`, before the may-apply check |
| `tests/orchestration/test_api_clients.py` | 33/0 | `client_lists_project` and `client_budget_answer_refusal` |
| `tests/ui_server/test_public_api.py` | 153/3 | may-apply test changed to a job of a listed project; job tests for decision, decline and apply; budget tests; socket-handler decline test; page test |

### This commit (self-reference)

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | this commit | this file; a handback cannot table the commit that writes it |

## External actions

- `git push origin feature/f253-public-http-api`, once, after this commit: reported in the
  worker's reply, not here (this file is written before the push).
- No pull request opened, no full suite, no mutation, no worktree, no merge, no new branch, no
  force-push, no pull, no `REMEDY_TEST_MAX_WORKERS`, no `-n`. No command of mine read, listed or
  wrote the repository's own `.data`.

## Verification

0. Preconditions, before any write: `block.md` read sha256
   `8ccc048e8be41871498e69385e2e5c235d51c491fbd78f78bf5d258212651870`; `append-live_review.txt`,
   `append-decisions.txt` and `dry-plan.md` each matched their `digests.txt` entry (Python
   `hashlib`); `git rev-parse HEAD` and `origin/feature/f253-public-http-api` both read
   `be49a81a155e93c10880c4e7debc6e5421902de4`; `git status --porcelain` empty; `.agent/STOP` absent.
   `git branch --show-current` read `feature/f253-public-http-api` before each commit.
1. **Gate 1**: `git status --porcelain` empty after C3; C1's byte proofs, one script, read from the
   committed blobs of `eebc09727`: the authored copy equals `block.md`, `.agent/plan.md` equals
   `dry-plan.md`, `.agent/live_review.md` and `.agent/decisions.md` each equal their blob at the
   base followed by their slice — all True.
2. **Gate 2**, once, from the primary checkout:
   `python3 -m pytest -q -rfEs tests/orchestration/test_api_clients.py tests/ui_server/test_public_api.py tests/orchestration/test_serve_daemon.py tests/orchestration/test_budget_decision.py tests/cli/test_decision_cmd.py tests/cli/test_decision_answers.py tests/orchestration/test_decision_queue.py tests/orchestration/test_import_reachability.py tests/test_ble001_ratchet.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/docs/ tests/cli/test_golden_path.py`
   — exit 0, tail `752 passed in 113.07s (0:01:53)`, no FAILED, ERROR or SKIPPED line.
3. **Gate 3**: `python3 -m ruff check` on the seven named files — exit 0, `All checks passed!`.
4. **Gate 4**: `python3 -m apps.cli.main integrity check --json` — exit 0, `"check_count": 6`,
   all six `pass`, `"fail_count": 0`.
5. **Gate 5**: the open-finding reader — exit 0, `['R-1138', 'R-1139', 'R-1143', 'R-1149',
   'R-1156', 'R-1157', 'R-1158', 'R-1160', 'R-1162', 'R-1172', 'R-1176', 'R-1196']`, as ordered.
6. Gate 6 (after the push): reported in the worker's reply, not here.

## Authored-text proofs

- `block.md` to `.agent/authored/f253-r20.md`: 186 lines, byte-equal, sha256
  `8ccc048e8be41871498e69385e2e5c235d51c491fbd78f78bf5d258212651870`.
- `append-live_review.txt` and `append-decisions.txt` each appended to their base blob at
  `be49a81a1`: "post equals pre plus slice" True for both.
- `dry-plan.md` to `.agent/plan.md`: byte-equal.

## Deviations & assumptions

- Choices left to me: the wording of the two refusal sentences (the job sentence names the client
  and the job as sent, the budget sentence names the client, the limit, the ceiling and the value
  given; both end "; nothing was run"); `_client_job_refusal` returns None when `load_job_plan`
  answers no record as well as when `lookup_job_id` raises `JobIdError`; for a job with an empty
  `project_id` no `select_project` call is made and the job has no keys; `decision.py` imports
  `is_budget_decision_id` inside the function body, as that file imports `decision_queue` elsewhere;
  the budget check is written inline in `answer_public_api_post` beside the call of the job helper;
  test names and the table `_JOB_WRITES` of the new tests.
- `write_public_api_page()` changed nothing: the generated section was already current, so C3
  holds only the hand-written part of the page.
- Diff reading: the block-copy hunk of C1 (the first 189 lines of its diff file) was not read, as
  the block allows for a byte-proven copy; every other diff was read whole before its commit.
- No C3x commit, no split (C1 209, C2 27, C3 284 insertions). Gate 2 ran once. Before C3 I ran
  `test_api_clients.py` (51 passed) and `test_public_api.py` (146 passed) once each, and ruff once.

## Round verdicts

Round 19's PASS is booked by C1 above. Round 20's verdict is the reviewer's.

## For the operator, in plain sentences

Round nineteen's work passed review. A program's own key may now act on a job only when the job
belongs to one of the projects the operator wrote for that key, and when a job stops at its
spending limit, the key may raise that limit only up to the largest number of model tokens and
provider calls the operator allowed it.

## Next

1. Phase 1 rule 1 (`.agent/STOP`): if it appears, finish the commit in hand, write the handback and
   stop.
2. Then the Open PR Gate (rule 2): no pull request for this branch, none to merge.
3. Then book round 20's verdict in the next round's first commit.
4. Then S7: F295's and F298's gate tests driven through HTTP alone.

Operator questions open: 0.
Open findings: 12 (R-1160, Medium, and R-1138, R-1139, R-1143, R-1149, R-1156, R-1157, R-1158,
R-1162, R-1172, R-1176 and R-1196, Low, owned by F297).

## Item status

| Item | Status | Reason |
|---|---|---|
| C1: book round 19, DECISION F253 D17, the plan and the block | done | `eebc09727` |
| C2: the budget decision's predicate lives in decision_queue | done | `61f376749` |
| C3: a client token's decisions, declines and applies stay inside its projects and ceilings | done | `82706dbaf` |
| Gates 1 to 5 | done | all green |
| C4: this handback | done | this commit |
| Push, Gate 6 | pending | reported in the worker's reply |
