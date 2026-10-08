# Handoff — F253 round 22: book round 21, repair R-1205 and R-1206, S7b: the gate paths over HTTP alone

## Session

SESSION 5 of feature F253 · round 22 · rounds so far 22

Context self-assessment: the reviewer's context is workable after four rounds; the session continues
with the hardening stage.

Fortschritt: ~92 % (S1 to S7 · hardening and closure open) — Schätzung

## Range

Review of `ec3565f8491693b209f5ae73f9adb4a1e31fa724`..`86cd5b284d32ab0cc0db6e638f4385a39a1059e7`
(the last commit before this handback, C3).

## Commits

### 978b062b9 F253 R22 C1: book round 21, resolve R-1204, register R-1205 to R-1207, DECISION F253 D19, the plan and the block

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f253-r22.md` | 187/0 | new file, byte copy of `block.md` (187 lines, sha256 `f564335fe42219076b6821638c7b5f574301de672b51eda1a2096af60d2c1617`) |
| `.agent/decisions.md` | 10/0 | `append-decisions.txt`'s bytes appended: DECISION F253 D19 |
| `.agent/live_review.md` | 10/0 | `append-live_review.txt`'s bytes appended: round 21's gate entry, VERDICT PASS, R-1204 resolved, R-1205, R-1206 and R-1207 |
| `.agent/plan.md` | 17/15 | `dry-plan.md`, byte for byte |

### b4e284b49 F253 R22 C2: a body string holding a NUL is refused, and the run route's table cell names its record (R-1205, R-1206)

| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/public_api.py` | 21/5 | `_body_refusal` answers "'<key>' must not hold a NUL character" for a `string` value, or an item of a `strings` value, holding a NUL (docstring names R-1205); `render_public_api_markdown` writes a `starts_run` route's "Answers as" cell as the run's record with `RunLauncher` (comment names R-1206) |
| `tests/ui_server/test_public_api.py` | 51/0 | new: decision (reason, and an answer item), decline, order (deadline) and run (builder provider) posts holding a NUL each answer 400 `api_body_invalid` naming the key with nothing run or started; the rendering's run row holds the new cell and not `remedy job run --json` |
| `docs/system/public-http-api-v1.md` | 1/1 | generated section regenerated (the run row's cell); version stays `1.9` |

### 86cd5b284 F253 R22 C3: F295's gate path and four of F304's paths driven through a real supervisor over HTTP alone

| Path | +/- | Reason |
|---|---|---|
| `tests/orchestration/test_public_api_gate_paths.py` | 377/0 | new: a fixture starts `remedy serve start --json` as a child on a scratch data root with `REMEDY_SERVE_API_PORT=0`; five tests drive F295's gate path and F304's apply-with-history-and-push, order of two jobs, order naming its project and decline over the port alone |
| `docs/system/public-http-api-v1.md` | 23/0 | hand-written: new `## A client's test` before `## Staying current`; in `## Orders` one sentence that a resent order is started again |

### This commit (self-reference)

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | this commit | this file; a handback cannot table the commit that writes it |
| `.agent/operator_questions.md` | this commit | byte copy of `dry-operator_questions.md`: Q12 |

## External actions

- `git push origin feature/f253-public-http-api`, once, after this commit: reported in the
  worker's reply, not here (this file is written before the push).
- No pull request opened, no full suite, no mutation, no worktree, no merge, no new branch, no
  force-push, no pull, no `REMEDY_TEST_MAX_WORKERS`, no `-n`. No command of mine read, listed or
  wrote the repository's own `.data`. No test started a real provider: every order was `no_llm`
  with both providers `fake`, every run named both providers `fake`, and `ps` after the new file's
  run showed no `remedy serve` process left.

## Verification

0. Preconditions, before any write: `block.md` read sha256
   `f564335fe42219076b6821638c7b5f574301de672b51eda1a2096af60d2c1617`; `append-live_review.txt`,
   `append-decisions.txt`, `dry-plan.md` and `dry-operator_questions.md` each matched their
   `digests.txt` entry (Python `hashlib`); `git rev-parse HEAD` and
   `origin/feature/f253-public-http-api` both read `ec3565f8491693b209f5ae73f9adb4a1e31fa724`;
   `git status --porcelain` empty; `.agent/STOP` absent. `git branch --show-current` read
   `feature/f253-public-http-api` before each commit.
1. **Gate 1**: `git status --porcelain` empty after C3; C1's byte proofs, one script, read from the
   committed blobs of `978b062b9`: the authored copy equals `block.md`, `.agent/plan.md` equals
   `dry-plan.md`, `.agent/live_review.md` and `.agent/decisions.md` each equal their blob at the
   base followed by their slice — all True.
2. **Gate 2**, once, from the primary checkout:
   `python3 -m pytest -q -rfEs tests/orchestration/test_public_api_gate_paths.py tests/ui_server/test_public_api.py tests/cli/test_client_interface.py tests/test_ble001_ratchet.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/docs/ tests/cli/test_golden_path.py`
   — exit 0, tail `682 passed in 105.72s (0:01:45)`, no FAILED, ERROR or SKIPPED line.
3. **Gate 3**: `python3 -m ruff check packages/orchestration/public_api.py tests/ui_server/test_public_api.py tests/orchestration/test_public_api_gate_paths.py`
   — exit 0, `All checks passed!`.
4. **Gate 4**: `python3 -m apps.cli.main integrity check --json` — exit 0, `"check_count": 6`, all
   six `pass`, `"fail_count": 0`.
5. **Gate 5**: the open-finding reader — exit 0, `['R-1138', 'R-1139', 'R-1143', 'R-1149',
   'R-1156', 'R-1157', 'R-1158', 'R-1160', 'R-1162', 'R-1172', 'R-1176', 'R-1196', 'R-1205',
   'R-1206', 'R-1207']`, as ordered.
6. Gate 6 (after the push): reported in the worker's reply, not here.

## Authored-text proofs

- `block.md` to `.agent/authored/f253-r22.md`: 187 lines, byte-equal, sha256
  `f564335fe42219076b6821638c7b5f574301de672b51eda1a2096af60d2c1617`.
- `append-live_review.txt` and `append-decisions.txt` each appended to their base blob at
  `ec3565f84`: "post equals pre plus slice" True for both.
- `dry-plan.md` to `.agent/plan.md`: byte-equal.
- `dry-operator_questions.md` to `.agent/operator_questions.md`: copied byte for byte in this
  commit.

## Deviations & assumptions

- Added to the child environment beyond the block's list: `PYTHONPATH`, set to this checkout's
  root (with any existing value after it). Observed: `python3 -m apps.cli.main` started from a
  folder outside the checkout imported `apps.cli.main` from a stale tree under
  `.remedy-wt/job-f146c82a6d8e42ca`, not from this checkout; the supervisor's
  own children put their code root first, but the supervisor, `project register` and `serve stop`
  do not. Not changed (outside the block); the test pins the checkout through `PYTHONPATH`, built
  when a test needs it.
- Choices left to me: the test file imports `_GIT_IDENTITY`, `PAST_DEADLINE`, `LATER_DEADLINE`,
  `_digest_job`, `_scratch_repo` from the F295 gate test and `_bare_upstream`, `_git` from the F304
  one, and makes its own `_repository` (F304's `_client` shape); a `Supervisor` dataclass holds the
  HTTP helpers; the child's standard error goes to a file in its working folder; the supervisor's
  working folder is `supervisor-folder` and the registration folder `elsewhere`, both under the
  test's temporary folder; the data root is `tmp_path_factory.mktemp("gp")`; the page text and the
  test names are mine. Two assertions of the model tests are absent because no HTTP answer carries
  their key: the mission's `order_source_path` (F295 step 2) and the job's ownership entries
  (F304's decline). `_body_refusal` checks every `string` key, so a NUL in the order's own text is
  refused too, naming `order`. Extra tests beyond the block's list: the decision test also sends a
  NUL in an `answer` item.
- Diff reading: the block-copy hunk of C1 (lines 1 to 193 of its diff file, headers included) was
  not read, as the block allows for a byte-proven copy; every other diff was read whole before its
  commit.
- One Bash call of mine began with `cd` (a grep); the permission layer refused it before it ran and
  I repeated it without the `cd`. Nothing else broke the no-`cd` rule.
- No C3x commit, no split (C1 224, C2 73, C3 400 insertions). Gate 2 ran once. While writing I ran
  `test_public_api.py` twice (176 passed each time), the new test file once (5 passed, with `-x`),
  and ruff on the touched files before each commit.

## Round verdicts

Round 21's PASS, with R-1204 resolved and R-1205 to R-1207 registered, is booked by C1 above.
Round 22's verdict is the reviewer's.

## For the operator, in plain sentences

Round twenty-one's work passed review, and the review found three more things: a request whose text
holds an invisible zero character got no answer, which this round fixed; a table on the web
interface's page described one answer wrongly, which this round fixed; and an order a program sends
twice runs twice, which waits for a later feature, and the one question below asks you about it. This
round also proved the whole path a program takes — order, read, answer, run, approve, prove and
decline — through the web interface alone, against a real Remedy started the way a program's own
test would start it.

## Next

1. Phase 1 rule 1 (`.agent/STOP`): if it appears, finish the commit in hand, write the handback and
   stop.
2. Then the Open PR Gate (rule 2): no pull request for this branch, none to merge.
3. Then book round 22's verdict and resolve R-1205 and R-1206 in the next round's first commit.
4. Then the amend0930b-slow-cap hardening stage: the acceptance audit.

Operator questions open: 1.
Open findings: 15 (R-1205 and R-1206, Low, owned by F253; R-1160, Medium, and R-1138, R-1139,
R-1143, R-1149, R-1156, R-1157, R-1158, R-1162, R-1172, R-1176, R-1196 and R-1207, Low, owned by
F297).

## Item status

| Item | Status | Reason |
|---|---|---|
| C1: book round 21, resolve R-1204, register R-1205 to R-1207, DECISION F253 D19, the plan and the block | done | `978b062b9` |
| C2: a body string holding a NUL is refused, and the run route's table cell names its record (R-1205, R-1206) | done | `b4e284b49` |
| C3: F295's gate path and four of F304's paths driven through a real supervisor over HTTP alone | done | `86cd5b284` |
| Gates 1 to 5 | done | all green |
| C4: this handback and operator question Q12 | done | this commit |
| Push, Gate 6 | pending | reported in the worker's reply |
