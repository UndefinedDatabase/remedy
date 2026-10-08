# Handoff — F253 round 9: book round 8, register R-1192, R-1193 and R-1194, and repair them

## Session

SESSION 2 of feature F253 · round 9 · rounds so far 9

Context self-assessment: the reviewer's context is workable after three rounds; the session continues with S4b.

Fortschritt: ~58 % (S1 to S3, S4a, S6a · S4b, S4c, S5, S6b, S7 open) — Schätzung

## Range

Review of `891372dca27d184568c928caeb6d93c04e649fd2`..HEAD (HEAD is C4 below, which carries this
handback and is the last commit on the branch).

## Commits

### 8a2e047e9 F253 R9 C1: book round 8, register R-1192, R-1193 and R-1194, the plan and the block

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f253-r9.md` | 127/0 | new file, byte copy of `block.md` |
| `.agent/live_review.md` | 8/0 | `append-live_review.txt`'s bytes appended: round 8's gate entry and R-1192, R-1193, R-1194 |
| `.agent/plan.md` | 6/5 | `dry-plan.md`, byte for byte |

### c8975aec8 F253 R9 C2: a route's path values are percent-decoded and a write locks on the full job id (R-1192, R-1193)

| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/public_api.py` | 19/6 | `_match_route_path` binds each `{name}` segment through `unquote`; `_job_lock_key`; `answer_public_api_post` passes the lock key to the runner |
| `docs/system/public-http-api-v1.md` | 2/1 | the page says a path value may be percent-encoded |
| `tests/ui_server/test_public_api.py` | 32/0 | three tests: a decoded decision id, a path value that decodes to a dash, a prefix and its full id lock on one key |

### c4e1051ad F253 R9 C3: tests hold a write's query refusal, its body ceiling and the runner's timeout (R-1194)

| Path | +/- | Reason |
|---|---|---|
| `tests/orchestration/test_serve_daemon.py` | 27/0 | a write with a query string and a write declaring a body one byte above the ceiling each answer 400 through a real supervisor and leave the decision open |
| `tests/orchestration/test_serve_runs.py` | 3/0 | the timeout test also holds that the call returns within 30 seconds |

### This commit (self-reference)

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | this commit | this file; a handback cannot table the commit that writes it |

## External actions

- Preconditions, before any write: `git rev-parse HEAD` read `891372dca27d184568c928caeb6d93c04e649fd2`,
  equal to `git rev-parse origin/feature/f253-public-http-api`; `git status --porcelain` was empty;
  `.agent/STOP` was absent; `block.md` read sha256
  `d7889c1e62961f96d3e7a4ec0a1d9a33dba459729bbd479bbe7050ee255b5996` with 127 lines, and all eight
  files listed in `digests.txt` matched (Python `hashlib`, 8 of 8 True); `git branch --show-current`
  read `feature/f253-public-http-api` before every commit.
- `git push origin feature/f253-public-http-api`, once, after this commit: reported in the worker's
  reply, not here (this file is written before the push).
- No full suite, no mutation, no worktree, no merge, no new branch, no force-push, no pull, no
  `REMEDY_TEST_MAX_WORKERS`, no `-n`. No command read, listed or wrote the repository's `.data`.

## Verification

0. Digests: 8 of 8 True (External actions).
1. Every commit: its staged diff was written to a file in the worker folder and read whole before the
   commit (C1 175 lines, C2 125, C3 50).
2. **Gate 1**: `git status --porcelain` empty (exit 0); `.agent/live_review.md` equals its blob at
   `891372dca` followed by `append-live_review.txt`, True; `.agent/authored/f253-r9.md` 127 lines,
   sha256 `d7889c1e62961f96d3e7a4ec0a1d9a33dba459729bbd479bbe7050ee255b5996`; the seven copied files
   (the block, the plan, and the five of C2 and C3) each byte-equal to its prepared file, all True.
3. **Gate 2**, from the primary checkout, once:

       python3 -m pytest -q -rfEs tests/orchestration/test_serve_runs.py tests/orchestration/test_serve_daemon.py tests/orchestration/test_serve_paths.py tests/orchestration/test_serve_stop_file.py tests/cli/test_serve_cmd.py tests/ui_server/test_public_api.py tests/ui_server/test_command_channel.py tests/test_subprocess_timeouts.py tests/test_ble001_ratchet.py tests/orchestration/test_import_reachability.py tests/test_no_orphan_modules.py tests/docs/ tests/cli/test_golden_path.py

   exit 0, `655 passed in 118.52s (0:01:58)`; no FAILED, ERROR or SKIPPED line.
4. **Gate 3**: `python3 -m ruff check` on the four Python files — exit 0, `All checks passed!`.
5. **Gate 4** (`python3 -m apps.cli.main integrity check --json`): exit 0, `"check_count": 6`, all six
   `pass`, `"fail_count": 0`, `"ok": true`.
6. **Gate 5**: exit 0, `['R-1138', 'R-1139', 'R-1143', 'R-1149', 'R-1156', 'R-1157', 'R-1158',
   'R-1160', 'R-1162', 'R-1172', 'R-1176', 'R-1192', 'R-1193', 'R-1194']`.
7. Gate 6 (after the push): reported in the worker's reply, not here.

## Authored-text proofs

- `block.md` to `.agent/authored/f253-r9.md`: 127 lines, byte-equal, sha256
  `d7889c1e62961f96d3e7a4ec0a1d9a33dba459729bbd479bbe7050ee255b5996`.
- `append-live_review.txt` appended to its base blob at `891372dca`: "post equals pre plus slice" True
  (gate 1).
- `dry-plan.md` to `.agent/plan.md`, and the five prepared files of C2 and C3 to their paths:
  byte-equal (gate 1).

## Deviations & assumptions

None.

## Round verdicts

Round 8's PASS and the registration of R-1192, R-1193 and R-1194 are booked by this round's C1.
Their resolutions and round 9's verdict are the reviewer's, written into the next round's first
commit.

## For the operator, in plain sentences

Round eight's work passed review, and the review found three small gaps, which this round closed. A
program that writes a question's name the way web browsers and most programming languages write it,
with special characters encoded, can now answer that question, where before the background service
read the name wrongly. Two answers for the same job sent at once now always wait for each other,
however the job is named. Three refusals the web interface already gave now each have a test.

## Next

1. Phase 1 rule 1 (`.agent/STOP`): if it appears, finish the commit in hand, write the handback and
   stop.
2. Then the Open PR Gate (rule 2): there is no pull request for this branch yet, so it finds none to
   merge.
3. Then book round 9's verdict and the resolutions of R-1192, R-1193 and R-1194 in the next round's
   first commit.
4. Then S4b: decline a result through `remedy job decline`.

Operator questions open: 1.
Open findings: 14 (R-1160 and R-1192, Medium; R-1138, R-1139, R-1143, R-1149, R-1156, R-1157,
R-1158, R-1162, R-1172, R-1176, R-1193 and R-1194, Low; R-1192, R-1193 and R-1194 owned by F253
and repaired by C2 and C3, awaiting the reviewer's resolution; the rest owned by F297).

## Item status

| Item | Status | Reason |
|---|---|---|
| C1: book round 8, register R-1192, R-1193 and R-1194, the plan and the block | done | `8a2e047e9` |
| C2: percent-decoded path values, the lock on the full job id (R-1192, R-1193) | done | `c8975aec8` |
| C3: tests for the query refusal, the body ceiling and the timeout (R-1194) | done | `c4e1051ad` |
| Gates 1 to 5 | done | all green, run once each, after C3 and before this file |
| C4: this handback | done | this commit |
| Push, Gate 6 | pending | reported in the worker's reply |
