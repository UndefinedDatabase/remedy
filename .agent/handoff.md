# Handoff — F253 round 8: book round 7 and R-1191's resolution, DECISION F253 D9, and S4a: answering a decision over HTTP

## Session

SESSION 2 of feature F253 · round 8 · rounds so far 8

Context self-assessment: the reviewer's context is workable after two rounds; the session continues with S4b.

Fortschritt: ~56 % (S1 to S3, S4a, S6a · S4b, S4c, S5, S6b, S7 open) — Schätzung

## Range

Review of `64caf46a2f23ea1bb1b50213dae604e79eb3356b`..HEAD (HEAD is C5 below, which carries this
handback and is the last commit on the branch).

## Commits

### 1ad10410e F253 R8 C1: book round 7 and R-1191's resolution, DECISION F253 D9, the plan and the block

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f253-r8.md` | 250/0 | new file, byte copy of `block.md` |
| `.agent/decisions.md` | 10/0 | `append-decisions.txt`'s bytes appended: DECISION F253 D9 |
| `.agent/live_review.md` | 4/0 | `append-live_review.txt`'s bytes appended: round 7's gate entry and R-1191's resolution |
| `.agent/plan.md` | 18/19 | `dry-plan.md`, byte for byte |
| `.agent/prose_slips.md` | 1/0 | `append-prose_slips.txt`'s bytes appended |

### a8a91ff8a F253 R8 C2: CommandRunner runs a command as a child of the supervisor and returns its envelope (DECISION F253 D9)

| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/serve_runs.py` | 60/4 | `child_environment`, `PUBLIC_API_COMMAND_TIMEOUT_SECONDS`, `CommandRunner`; `RunLauncher.start` calls `child_environment` |
| `tests/orchestration/test_serve_runs.py` | 97/0 | the runner's tests with a `-c` stand-in command, and one test that `start` passes the child environment |

### 300105d0f F253 R8 C3: POST /api/v1/jobs/{job}/decisions/{decision} answers remedy decision resolve through the supervisor (S4a, DECISION F253 D9)

| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/public_api.py` | 139/5 | `body` and `refusal_default` on `PublicApiRoute`, the POST route, version 1.4, `answer_public_api_post`, the argv builder table, the generated table's columns |
| `packages/orchestration/ui_server.py` | 45/1 | `command_runner` class attribute, the POST branch of `do_POST`, `_send_public_api_post` |
| `packages/orchestration/serve_daemon.py` | 12/8 | `runner` for both handler classes; `run_supervisor` builds one `CommandRunner` |
| `docs/system/public-http-api-v1.md` | 3/2 | generated section regenerated with `write_public_api_page()` |
| `tests/ui_server/test_public_api.py` | 142/1 | route pinned; the argv, body, path, 500, refusal and 404/405 tests; the cockpit's 405 with its ledger line; the well-formed test accepts POST |
| `tests/orchestration/test_serve_daemon.py` | 110/2 | a real supervisor: the POST on the port equals the command's envelope, 409, 404, 401, the ledger; the same POST on the socket; `_api_request` takes a body |

### ee7670565 F253 R8 C4: the page says how a write is answered

| Path | +/- | Reason |
|---|---|---|
| `docs/system/public-http-api-v1.md` | 20/3 | the last sentence of "The envelope and its refusals" replaced; section "Writes" added |
| `tests/ui_server/test_public_api.py` | 8/0 | a test that the three new tokens and the section are on the page |

### This commit (self-reference)

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | this commit | this file; a handback cannot table the commit that writes it |

## External actions

- Preconditions, before any write: `git rev-parse HEAD` read `64caf46a2f23ea1bb1b50213dae604e79eb3356b`,
  equal to `git rev-parse origin/feature/f253-public-http-api`; `git status --porcelain` was empty;
  `.agent/STOP` was absent; `block.md` read sha256
  `c392e539a86db83c65a886460bd8d95fa8938bb61b18a683c8baea7b94c372e0` with 250 lines, and all five
  files listed in `digests.txt` matched (Python `hashlib`, 5 of 5 True); `git branch --show-current`
  read `feature/f253-public-http-api` before every commit.
- `git push origin feature/f253-public-http-api`, once, after this commit: reported in the worker's
  reply, not here (this file is written before the push).
- No full suite, no mutation, no worktree, no merge, no new branch, no force-push, no pull, no
  `REMEDY_TEST_MAX_WORKERS`, no `-n`. No command read, listed or wrote the repository's `.data`.

## Verification

0. Digests: 5 of 5 True (External actions).
1. C1: `.agent/authored/f253-r8.md` read 250 lines, sha256
   `c392e539a86db83c65a886460bd8d95fa8938bb61b18a683c8baea7b94c372e0`, byte-equal to `block.md`;
   `.agent/live_review.md`, `.agent/prose_slips.md` and `.agent/decisions.md` each "post equals pre
   plus slice" True (`.agent/decisions.md` never read whole); `.agent/plan.md` byte-equal to
   `dry-plan.md`.
2. Every commit: its staged diff was written to a file in the worker folder and read whole before the
   commit (C1 351 lines, C2 220, C3 694, C4 55).
3. **Gate 1**: `git status --porcelain` empty (exit 0); the five C1 proofs re-run against the committed
   tree (base blobs via `git show 64caf46a2...:`) all True.
4. **Gate 2**, from the primary checkout, once:

       python3 -m pytest -q -rfEs tests/orchestration/test_serve_runs.py tests/orchestration/test_serve_daemon.py tests/orchestration/test_serve_paths.py tests/orchestration/test_serve_stop_file.py tests/cli/test_serve_cmd.py tests/ui_server/test_public_api.py tests/ui_server/test_command_channel.py tests/test_subprocess_timeouts.py tests/test_ble001_ratchet.py tests/orchestration/test_import_reachability.py tests/test_no_orphan_modules.py tests/docs/ tests/cli/test_golden_path.py

   exit 0, `650 passed in 124.73s (0:02:04)`; no FAILED, ERROR or SKIPPED line;
   `tests/orchestration/import_reachability_allowlist.txt` did not need to change.
5. **Gate 3**: `python3 -m ruff check` on the seven Python files C2 and C3 touched — exit 0,
   `All checks passed!`.
6. **Gate 4** (`python3 -m apps.cli.main integrity check --json`): exit 0, `"check_count": 6`, all six
   `pass`, `"fail_count": 0`, `"ok": true`.
7. **Gate 5**: exit 0, `['R-1138', 'R-1139', 'R-1143', 'R-1149', 'R-1156', 'R-1157', 'R-1158',
   'R-1160', 'R-1162', 'R-1172', 'R-1176']`.
8. Gate 6 (after the push): reported in the worker's reply, not here.

## Authored-text proofs

- `block.md` to `.agent/authored/f253-r8.md`: 250 lines, byte-equal, sha256
  `c392e539a86db83c65a886460bd8d95fa8938bb61b18a683c8baea7b94c372e0`.
- `append-live_review.txt`, `append-prose_slips.txt` and `append-decisions.txt` appended to their base
  blobs at `64caf46a2`: each "post equals pre plus slice" True, proved before C1 and again as gate 1.
- `dry-plan.md` to `.agent/plan.md`: byte-equal, proved before C1 and again as gate 1.

## Deviations & assumptions

1. One shell call, a `grep` of `client_interface.py` made while reading, began with `cd` to the primary
   checkout (`cd ... 2>/dev/null; grep ...`), against the block's "never `cd`". It changed no reading
   and no later call used it.
2. `answer_public_api_post` answers a refusal not listed in `refusals` with
   `route.refusal_default or 500`, where the block gave `route.refusal_default`: a route with no
   default would otherwise hand `None` to the sender. The one route has default 409, so no answer
   differs.
3. In `_send_public_api_post` a `Content-Length` below zero is treated as "not a whole number" and
   answers 400 `api_body_invalid` without reading, as the block's "or not a whole number" does for
   text.
4. For "`RunLauncher.start` still passes the same environment" C2 adds one new test
   (`test_a_run_starts_with_the_child_environment`), which compares `child_environment` and a started
   run's own output; no existing test was edited.
5. C3 held 451 insertions, under the cap, so it is one commit and not split into parts.
6. One call that was not part of the block: a `python3 - <<EOF` call printing `1`, a test of whether
   the sandbox takes a heredoc after an earlier heredoc was refused. It touched nothing.
7. One run of `tests/orchestration/test_serve_daemon.py` printed the line `Exception occurred during
   processing of request from` on standard error (no further text survived my 2000-character tail); it
   passed (31 passed) and the same file passed twice more with no such line, and gate 2 printed none.
   I did not find its cause; it may come from a client that closes a connection to the socket or port
   server as the test ends.

## Round verdicts

Round 7's PASS and R-1191's resolution are booked by this round's C1. Round 8's verdict is the
reviewer's, written into the next round's first commit.

## For the operator, in plain sentences

Round seven's work passed review. A program can now answer one of Remedy's questions over the web
interface of the background service, and the answer is exactly what the command line would have given,
because the service runs that very command for it. The cockpit in the browser does not take answers
this way yet. The next rounds add declining a result and approving one with its commit and push.

## Next

1. Phase 1 rule 1 (`.agent/STOP`): if it appears, finish the commit in hand, write the handback and
   stop.
2. Then the Open PR Gate (rule 2): there is no pull request for this branch yet, so it finds none to
   merge.
3. Then book round 8's verdict in the next round's first commit.
4. Then S4b: decline a result through `remedy job decline`.

Operator questions open: 1.
Open findings: 11 (R-1160, Medium; R-1138, R-1139, R-1143, R-1149, R-1156, R-1157, R-1158, R-1162,
R-1172 and R-1176, Low; all owned by F297).

## Item status

| Item | Status | Reason |
|---|---|---|
| C1: book round 7 and R-1191's resolution, DECISION F253 D9, the plan and the block | done | `1ad10410e` |
| C2: CommandRunner (DECISION F253 D9) | done | `a8a91ff8a` |
| C3: POST /api/v1/jobs/{job}/decisions/{decision} (S4a) | done | `300105d0f` |
| C4: the page says how a write is answered | done | `ee7670565` |
| Gates 1 to 5 | done | all green, run once each, after C4 and before this file |
| C5: this handback | done | this commit |
| Push, Gate 6 | pending | reported in the worker's reply |
