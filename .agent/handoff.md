# Handoff — F253 round 16: book round 15, repair R-1201 and R-1202

## Session

SESSION 4 of feature F253 · round 16 · rounds so far 16

Context self-assessment: the reviewer's context is workable after four rounds; the session
continues with S5c.

Fortschritt: ~79 % (S1 to S3, S4a to S4c, S5a, S5b, S6a · S5c, S6b, S7 open) — Schätzung

## Range

Review of `450711f3e51d0b79fbc3f5e45e9275a47b1c5de5`..`3d6c6a8acfb04ef66f3367a58bea822ff3319986`
(the last commit before this handback, C3).

## Commits

### c23013144 F253 R16 C1: book round 15, register R-1201 and R-1202, the plan and the block

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f253-r16.md` | 123/0 | new file, byte copy of `block.md` |
| `.agent/live_review.md` | 6/0 | `append-live_review.txt`'s bytes appended: round 15's gate entry and R-1201, R-1202 registered |
| `.agent/plan.md` | 6/7 | `dry-plan.md`, byte for byte |

### 3d6c6a8ac F253 R16 C2: an order that cannot start is answered and ledgered, and the no-project refusal gains its test (R-1201, R-1202)

| Path | +/- | Reason |
|---|---|---|
| `docs/system/public-http-api-v1.md` | 2/1 | one sentence: a child that cannot start removes the order's folder and answers 500 `api_command_failed` |
| `packages/orchestration/public_api.py` | 9/2 | docstring sentence on the `OSError` path; `answer_public_api_post` catches `OSError` from `start_order` and answers 500 `api_command_failed` |
| `packages/orchestration/serve_runs.py` | 12/4 | `import shutil`; `OrderLauncher.start` catches `OSError` from `subprocess.Popen`, removes the order's folder whole with `shutil.rmtree`, and raises again; docstring updated |
| `tests/orchestration/test_serve_runs.py` | 11/0 | R-1201: a launcher whose prefix names a program that does not exist raises `OSError` from `start`, and `orders_dir` then holds no folder |
| `tests/ui_server/test_public_api.py` | 70/2 | `_unix_request` gains an optional `body` parameter; R-1201: a starter that raises `OSError` answers 500 `api_command_failed` (direct), and through a real handler made by `socket_handler_class` holding such an `OrderLauncher`, the same POST answers 500, ledgers one line with that status and token, and leaves `orders_dir` empty; R-1202: with `REMEDY_PROJECT` naming a registered project, an order whose header names none is still refused 409 `api_order_project_unknown` with the starter uncalled |

### This commit (self-reference)

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | this commit | this file; a handback cannot table the commit that writes it |

## External actions

- `git push origin feature/f253-public-http-api`, once, after this commit: reported in the
  worker's reply, not here (this file is written before the push).
- No pull request opened, no full suite, no mutation, no worktree, no merge, no new branch, no
  force-push, no pull, no `REMEDY_TEST_MAX_WORKERS`, no `-n`. No command read, listed or wrote the
  repository's own `.data`.

## Verification

0. Preconditions, before any write: `git rev-parse HEAD` read
   `450711f3e51d0b79fbc3f5e45e9275a47b1c5de5`, equal to
   `git rev-parse origin/feature/f253-public-http-api`; `git status --porcelain` was empty;
   `.agent/STOP` was absent; `block.md` read sha256
   `345a816a44d938f74885a35f70ce8628be3f4623b79239c105d21f3d68d7c019`, matching both the literal
   the task gave and `digests.txt`'s own entry; `append-live_review.txt` and `dry-plan.md` each
   matched their own `digests.txt` entry (Python `hashlib`, 3 of 3 True); `git branch --show-current`
   read `feature/f253-public-http-api` before each commit.
1. Every commit: its staged diff was written to a file in the worker folder and read whole before
   the commit. C1's three files (`.agent/authored/f253-r16.md` byte-equal to `block.md`;
   `.agent/live_review.md` post == pre + `append-live_review.txt`'s slice; `.agent/plan.md`
   byte-equal to `dry-plan.md`) were each proven byte-equal by script and so not re-read line by
   line (the proof is stated here, per the block's own allowance), though the whole cached diff
   (135 insertions) was still read. C2's 104-insertion diff was read whole.
2. **Gate 1**: `git -C /home/decodeux/Repos/remedy status --porcelain` empty; the C1 byte proofs —
   `authored_byte_equal` True (123 lines, sha256
   `345a816a44d938f74885a35f70ce8628be3f4623b79239c105d21f3d68d7c019`);
   `live_review_post_equals_pre_plus_slice` True (pre 246160 bytes + slice 5597 bytes = post
   251757 bytes); `plan_byte_equal` True — all True.
3. **Gate 2**, from the primary checkout, once:
   `python3 -m pytest -q -rfEs tests/ui_server/test_public_api.py tests/orchestration/test_serve_runs.py tests/orchestration/test_serve_daemon.py tests/test_ble001_ratchet.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/docs/ tests/cli/test_golden_path.py`
   — exit 0, `643 passed in 104.55s`; no FAILED, ERROR or SKIPPED line.
4. **Gate 3**: `python3 -m ruff check packages/orchestration/public_api.py packages/orchestration/serve_runs.py tests/ui_server/test_public_api.py tests/orchestration/test_serve_runs.py`
   — exit 0, `All checks passed!`.
5. **Gate 4**: `python3 -m apps.cli.main integrity check --json` — exit 0, `"check_count": 6`, all
   six `pass`, `"fail_count": 0`, `"ok": true`.
6. **Gate 5**: `python3 -c "import scripts.rotate_live_review as r; print(r.open_finding_ids(open('.agent/live_review.md').read()))"`
   — exit 0, `['R-1138', 'R-1139', 'R-1143', 'R-1149', 'R-1156', 'R-1157', 'R-1158', 'R-1160',
   'R-1162', 'R-1172', 'R-1176', 'R-1196', 'R-1201', 'R-1202']`, exactly as ordered.
7. No `F253 R16 C2b` was needed: gates read green on the one and only run.
8. Gate 6 (after the push): reported in the worker's reply, not here.

## Authored-text proofs

- `block.md` to `.agent/authored/f253-r16.md`: 123 lines, byte-equal, sha256
  `345a816a44d938f74885a35f70ce8628be3f4623b79239c105d21f3d68d7c019`.
- `append-live_review.txt` appended to `.agent/live_review.md`'s base blob at `450711f3e`:
  "post equals pre plus slice" True.
- `dry-plan.md` to `.agent/plan.md`: byte-equal.

## Deviations & assumptions

- No departure from the block's ordered commit sequence: exactly C1, C2, C3, in order; no C2b was
  needed because Gate 2 read green on its one and only run.
- **R-1201's folder removal uses a plain `shutil.rmtree(order_dir)`, not `ignore_errors=True`.**
  The block says "the order's folder is removed whole and the error is raised again"; a second
  failure during removal (e.g. permission) is itself an `OSError` and still propagates, which
  reads as consistent with "and the error is raised again" rather than silently swallowing a
  second fault. Not specified either way by the block; my choice.
- **The re-raise is a bare `raise` inside `except OSError:`**, preserving the original
  exception and traceback rather than wrapping it in a new one.
- **Test names, and the `_unix_request` helper's new optional `body` parameter, are my own.**
  The block named the file and the behaviour to prove, not exact signatures. I extended
  `_unix_request` (in `tests/ui_server/test_public_api.py`) with an optional `body: bytes | None`
  parameter, backward compatible with its existing callers, because the real-handler R-1201 test
  needed to POST a JSON body over the unix socket and no existing helper did.
- **The real-handler R-1201 test wires `socket_handler_class` with a real `SR.CommandRunner(paths)`
  as `runner=`, never actually invoked.** `do_POST` only reaches `_send_public_api_post` at all
  when `self.command_runner is not None`; the order-create route itself bypasses the runner
  entirely (`route.starts_order`), so the runner object is a precondition-satisfying stand-in,
  not exercised logic. Left as a deviation note because it is a judgment call, not written in the
  block.
- **R-1202 required no production change.** `_order_text_and_options` already refuses
  unconditionally on `order_file.project is None` before `select_project` is consulted; the
  repair is the missing test alone, matching the block's instruction that only C2's named
  production files and the two test files change. I informally re-derived the finding's premise
  (not a mutation run, which the constraints forbid): with `REMEDY_PROJECT` set to a registered
  slug, `select_project(None, ".")` resolves successfully through the environment fallback
  (confirmed by a throwaway script under the worker folder, not committed), which is exactly the
  silent acceptance the new test would catch if the explicit `None` check were ever removed.
- Everything else matches the block exactly: the two production files it named, the one doc-page
  sentence, the two test files, `PUBLIC_API_VERSION` left at `1.7`, and the gates' order, commands
  and content.
- Nothing about this commit's own self-review belongs here (per the block); see the reply's
  separate self-review report.

## Round verdicts

Round 15's PASS, with R-1201 and R-1202 registered, is booked by C1 above. Round 16's verdict is
the reviewer's, to be written into round 17's first commit.

## For the operator, in plain sentences

Round fifteen's work passed review, and the review found two things to fix: when Remedy cannot
start an order, the program that sent it now gets a clear answer, the call is written down like
every other, and no half-made order is left on disk; and the rule that refuses an order naming no
project now has a test that would notice if it were lost.

## Next

1. Phase 1 rule 1 (`.agent/STOP`): if it appears, finish the commit in hand, write the handback
   and stop.
2. Then the Open PR Gate (rule 2): there is no pull request for this branch, so it finds none to
   merge.
3. Then book round 16's verdict and resolve R-1201 and R-1202 in the next round's first commit.
4. Then S5c: two orders at once through HTTP.

Operator questions open: 0.
Open findings: 14 (R-1201 and R-1202, Low, owned by F253; R-1160, Medium, and R-1138, R-1139,
R-1143, R-1149, R-1156, R-1157, R-1158, R-1162, R-1172, R-1176 and R-1196, Low, owned by F297).

## Item status

| Item | Status | Reason |
|---|---|---|
| C1: book round 15, register R-1201 and R-1202, the plan and the block | done | `c23013144` |
| C2: an order that cannot start is answered and ledgered, and the no-project refusal gains its test | done | `3d6c6a8ac` |
| Gates 1 to 5 | done | all green, run once each, after C2 and before this file |
| C2b (conditional repair commit) | skipped | not needed, Gate 2 was green on its one run |
| C3: this handback | done | this commit |
| Push, Gate 6 | pending | reported in the worker's reply |
