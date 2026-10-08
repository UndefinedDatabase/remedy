# Handoff — F253 round 21: book round 20, repair R-1204, S7a: a client starts a job's run over HTTP

## Session

SESSION 5 of feature F253 · round 21 · rounds so far 21

Context self-assessment: the reviewer's context is workable after three rounds; the session continues
with S7b.

Fortschritt: ~90 % (S1 to S6, S7a · S7b, hardening and closure open) — Schätzung

## Range

Review of `a4236dff866d7aebffbd62ce69363d38d459d4b4`..`eeb095a363e0890ec871957bf555eec805c21f40`
(the last commit before this handback, C4).

## Commits

### c543f6c12 F253 R21 C1: book round 20, register R-1204, DECISION F253 D18, the plan and the block

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f253-r21.md` | 206/0 | new file, byte copy of `block.md` (206 lines, sha256 `5fed5baec94d33b7f99fe5bbd69c52f0c7d0838404d4e20787f8fe6fe04218ac`) |
| `.agent/decisions.md` | 10/0 | `append-decisions.txt`'s bytes appended: DECISION F253 D18 |
| `.agent/live_review.md` | 4/0 | `append-live_review.txt`'s bytes appended: round 20's gate entry, VERDICT PASS, and R-1204 |
| `.agent/plan.md` | 12/12 | `dry-plan.md`, byte for byte |

### 0730cedb8 F253 R21 C2: a write on a job whose record cannot be read answers instead of raising (R-1204)

| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/public_api.py` | 10/8 | `_job_apply_argv` and `_client_job_refusal` read the job with `load_job_plan_safe`; each docstring names R-1204 |
| `tests/ui_server/test_public_api.py` | 39/0 | new: an apply with no client is passed on as sent with no `--repo`; apply, decline and decision with a client listing every project key answer 403 and run nothing |

### 32ec5ead8 F253 R21 C3: the supervisor's RunLauncher passes options to a run

| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/serve_runs.py` | 7/6 | `RunLauncher.start` takes `options`, placed after `argv_for(job_id)` and before `--json`; docstring names D18 (3) |
| `tests/orchestration/test_serve_runs.py` | 23/0 | new: a stand-in child writes its arguments as JSON; with options and `--json` and with neither |

### eeb095a36 F253 R21 C4: POST api v1 jobs run starts a job's run through the supervisor

| Path | +/- | Reason |
|---|---|---|
| `docs/system/public-http-api-v1.md` | 25/1 | new hand-written section `## Runs`; generated section regenerated (version `1.9`, the new row) |
| `packages/orchestration/public_api.py` | 96/1 | `starts_run` field, the route, `PUBLIC_API_VERSION = "1.9"`, `_start_run_answer`, `start_run` keyword of `answer_public_api_post` |
| `packages/orchestration/serve_daemon.py` | 10/5 | `public_api_handler_class` takes `launcher`; `run_supervisor` hands its `RunLauncher` to it |
| `packages/orchestration/ui_server.py` | 11/1 | class attribute `run_launcher`; `_send_public_api_post` passes `start_run=` |
| `tests/orchestration/test_serve_daemon.py` | 83/0 | new: a real supervisor with a port starts a run over the port and one over the socket, a second post answers 409, both ends are recorded |
| `tests/ui_server/test_public_api.py` | 174/4 | pinned route and test, version `1.9`, the well-formed test adapted, run-route tests, page test |

### This commit (self-reference)

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | this commit | this file; a handback cannot table the commit that writes it |

## External actions

- `git push origin feature/f253-public-http-api`, once, after this commit: reported in the
  worker's reply, not here (this file is written before the push).
- No pull request opened, no full suite, no mutation, no worktree, no merge, no new branch, no
  force-push, no pull, no `REMEDY_TEST_MAX_WORKERS`, no `-n`. No command of mine read, listed or
  wrote the repository's own `.data`. No test started a real provider or a real `remedy job run`.

## Verification

0. Preconditions, before any write: `block.md` read sha256
   `5fed5baec94d33b7f99fe5bbd69c52f0c7d0838404d4e20787f8fe6fe04218ac`; `append-live_review.txt`,
   `append-decisions.txt` and `dry-plan.md` each matched their `digests.txt` entry (Python
   `hashlib`); `git rev-parse HEAD` and `origin/feature/f253-public-http-api` both read
   `a4236dff866d7aebffbd62ce69363d38d459d4b4`; `git status --porcelain` empty; `.agent/STOP` absent.
   `git branch --show-current` read `feature/f253-public-http-api` before each commit.
1. **Gate 1**: `git status --porcelain` empty after C4; C1's byte proofs, one script, read from the
   committed blobs of `c543f6c12`: the authored copy equals `block.md`, `.agent/plan.md` equals
   `dry-plan.md`, `.agent/live_review.md` and `.agent/decisions.md` each equal their blob at the
   base followed by their slice — all True.
2. **Gate 2**, once, from the primary checkout:
   `python3 -m pytest -q -rfEs tests/ui_server/test_public_api.py tests/orchestration/test_serve_runs.py tests/orchestration/test_serve_daemon.py tests/orchestration/test_api_clients.py tests/ui_server/test_command_channel.py tests/orchestration/test_import_reachability.py tests/test_ble001_ratchet.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/docs/ tests/cli/test_golden_path.py`
   — exit 0, tail `865 passed in 121.65s (0:02:01)`, no FAILED, ERROR or SKIPPED line.
3. **Gate 3**: `python3 -m ruff check` on the seven named files — exit 0, `All checks passed!`.
4. **Gate 4**: `python3 -m apps.cli.main integrity check --json` — exit 0, `"check_count": 6`,
   all six `pass`, `"fail_count": 0`.
5. **Gate 5**: the open-finding reader — exit 0, `['R-1138', 'R-1139', 'R-1143', 'R-1149',
   'R-1156', 'R-1157', 'R-1158', 'R-1160', 'R-1162', 'R-1172', 'R-1176', 'R-1196', 'R-1204']`, as
   ordered.
6. Gate 6 (after the push): reported in the worker's reply, not here.

## Authored-text proofs

- `block.md` to `.agent/authored/f253-r21.md`: 206 lines, byte-equal, sha256
  `5fed5baec94d33b7f99fe5bbd69c52f0c7d0838404d4e20787f8fe6fe04218ac`.
- `append-live_review.txt` and `append-decisions.txt` each appended to their base blob at
  `a4236dff8`: "post equals pre plus slice" True for both.
- `dry-plan.md` to `.agent/plan.md`: byte-equal.

## Deviations & assumptions

- Choices left to me: `_start_run_answer` and `_RUN_PROVIDER_KEYS` are new private names in
  `public_api.py` holding the run branch; its refusal sentences (`invalid_job_id` and
  `ambiguous_job_id` use the words of `_change_proof_answer`, `job_not_found` for an unreadable
  record ends "; nothing was run", `api_command_failed` says "the run for '<path>' could not be
  started; nothing runs"); the route's description and the page's `## Runs` wording; in
  `_client_job_refusal` a record that cannot be read is told apart from a missing one by the
  `degraded` flag, a missing one still passing on; `_job_apply_argv` ignores the flag; the
  `start_run` function in `_send_public_api_post` is a conditional lambda; the daemon test uses its
  own fixture `running_with_run_route`; the C3 test's second case runs with `json_output=False`
  and no options; extra tests beyond the block: a cockpit-server 405 for the run route, a body
  with a wrong kind, an ambiguous prefix, a client's listed project answering 202.
- Diff reading: the block-copy hunk of C1 (the first 204 lines of its diff file, headers included) was not read, as
  the block allows for a byte-proven copy; every other diff was read whole before its commit.
- Observed, not changed (outside the block): a provider value holding a NUL character makes
  `subprocess.Popen` in `RunLauncher.start` raise `ValueError`, which neither `_start_run_answer`
  nor `_send_public_api_post` catches; the order route has the same shape for its string keys.
- No C4x commit, no split (C1 232, C2 49, C3 30, C4 399 insertions). Gate 2 ran once. While
  writing I ran `test_public_api.py` twice (4 selected, then 171 passed), `test_serve_runs.py` once
  (56 passed), a selection of four tests of `test_serve_daemon.py` once (4 passed), and ruff on the
  touched files before each commit.

## Round verdicts

Round 20's PASS, with R-1204 registered, is booked by C1 above. Round 21's verdict is the
reviewer's.

## For the operator, in plain sentences

Round twenty's work passed review, and the review found one thing to fix, which this round fixed:
a request about a job whose record on disk is damaged now gets an answer instead of none. And a
program can now start the run of a job it ordered, naming which model builds and which reviews,
and then watch it in the same overview it already reads.

## Next

1. Phase 1 rule 1 (`.agent/STOP`): if it appears, finish the commit in hand, write the handback and
   stop.
2. Then the Open PR Gate (rule 2): no pull request for this branch, none to merge.
3. Then book round 21's verdict and resolve R-1204 in the next round's first commit.
4. Then S7b: F295's gate path and F304's five paths driven through a real supervisor's port alone.

Operator questions open: 0.
Open findings: 13 (R-1204, Low, owned by F253; R-1160, Medium, and R-1138, R-1139, R-1143, R-1149,
R-1156, R-1157, R-1158, R-1162, R-1172, R-1176 and R-1196, Low, owned by F297).

## Item status

| Item | Status | Reason |
|---|---|---|
| C1: book round 20, register R-1204, DECISION F253 D18, the plan and the block | done | `c543f6c12` |
| C2: a write on a job whose record cannot be read answers instead of raising (R-1204) | done | `0730cedb8` |
| C3: the supervisor's RunLauncher passes options to a run | done | `32ec5ead8` |
| C4: POST api v1 jobs run starts a job's run through the supervisor | done | `eeb095a36` |
| Gates 1 to 5 | done | all green |
| C5: this handback | done | this commit |
| Push, Gate 6 | pending | reported in the worker's reply |
