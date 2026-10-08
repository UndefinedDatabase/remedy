# Handoff — F253 round 7: book round 6 and R-1191, DECISION F253 D8, R-1191's test, the test suite's import-time data root, and Q11

## Session

SESSION 2 of feature F253 · round 7 · rounds so far 7

Context self-assessment: the reviewer's context is fresh after one round; the session continues with S4.

Fortschritt: ~50 % (S1 to S3, S6a · S4, S5, S6b, S7 open) — Schätzung

## Range

Review of `028f3173656fe9b1154ec52199b3713ffb7541f7`..HEAD (HEAD is C4 below, which carries this
handback and is the last commit on the branch).

## Commits

### 644cc4d3e F253 R7 C1: book round 6 and R-1191, DECISION F253 D8, the plan and the block

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f253-r7.md` | 140/0 | new file, byte copy of `block.md` |
| `.agent/decisions.md` | 10/0 | `append-decisions.txt`'s bytes appended: DECISION F253 D8 |
| `.agent/live_review.md` | 4/0 | `append-live_review.txt`'s bytes appended: round 6's gate entry and R-1191's registration |
| `.agent/plan.md` | 12/9 | `dry-plan.md`, byte for byte |

### 60f881d09 F253 R7 C2: a test holds that the supervisor's API thread ends with it (R-1191)

| Path | +/- | Reason |
|---|---|---|
| `tests/orchestration/test_serve_daemon.py` | 13/0 | `dry-test_serve_daemon.py`, byte for byte: `test_ending_stops_the_thread_that_served_the_api_port` |

### 4cf369e64 F253 R7 C3: every test process gets an import-time data root, so no copy of the environment reaches the operator's (DECISION F253 D8)

| Path | +/- | Reason |
|---|---|---|
| `tests/conftest.py` | 41/16 | `dry-conftest.py`, byte for byte: `pytest_configure` sets `REMEDY_DATA_DIR` to a new temporary folder; `_isolated_data_root` takes `request` and restores that root after each test; `pytest_unconfigure` removes the folder |
| `tests/test_data_root_isolation.py` | 48/1 | `dry-test_data_root_isolation.py`, byte for byte: `ENVIRONMENT_AT_IMPORT`, `_child_data_root`, a module-scoped fixture, two tests |

### This commit (self-reference)

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | this commit | this file; a handback cannot table the commit that writes it |
| `.agent/operator_questions.md` | this commit | `dry-operator_questions.md`, byte for byte: question Q11 |

## External actions

- Preconditions, before any write: `git rev-parse HEAD` read `028f3173656fe9b1154ec52199b3713ffb7541f7`,
  equal to `git rev-parse origin/feature/f253-public-http-api`; `git status --porcelain` was empty;
  `.agent/STOP` was absent; `block.md` read sha256
  `f6844d6aaa5623d20446e943a738a158586d04a75933d41155f40347594ad849` with 140 lines, and all eight
  files listed in `digests.txt` matched (Python `hashlib`, 8 of 8 True); `git branch --show-current`
  read `feature/f253-public-http-api` before every commit.
- `git push origin feature/f253-public-http-api`, once, after this commit: reported in the worker's
  reply, not here (this file is written before the push).
- No other test run than gate 2; no full suite, no mutation, no worktree, no merge, no new branch,
  no force-push, no pull, no `REMEDY_TEST_MAX_WORKERS`, no `-n`. No command read, listed or wrote the
  repository's `.data`.

## Verification

0. Digests: 8 of 8 True (External actions).
1. C1: `.agent/authored/f253-r7.md` read 140 lines, sha256
   `f6844d6aaa5623d20446e943a738a158586d04a75933d41155f40347594ad849`, byte-equal to `block.md`;
   `.agent/live_review.md` and `.agent/decisions.md` each "post equals pre plus slice" True
   (`.agent/decisions.md` never read whole: 3129525 + 3242 = 3132767 bytes; live_review 205862 + 3551
   = 209413); `.agent/plan.md` byte-equal to `dry-plan.md`. The staged diff was written to a file and
   read as the self-review (the block's 140 lines are covered by the byte proof).
2. C2 and C3: each staged diff (24 and 181 lines) was written to a file and read whole as the
   self-review; each copy byte-equal to its prepared file.
3. **Gate 1**: `git status --porcelain` empty; the three test files byte-equal to their prepared copies,
   and the five C1 proofs (re-run against the committed tree, base blobs via `git show 644cc4d3e^:`)
   all True.
4. **Gate 2**, from the primary checkout, once:

       python3 -m pytest -q -rfEs tests/test_data_root_isolation.py tests/regression/test_data_root_guard.py tests/regression/test_f294_acceptance.py tests/regression/test_f293_acceptance.py tests/regression/test_test_load_governor.py tests/test_data_paths.py tests/orchestration/test_config.py tests/orchestration/test_manual_completion_bundle.py tests/cli/test_mission_cmd.py tests/orchestration/test_serve_daemon.py tests/cli/test_serve_cmd.py tests/test_test_categories.py tests/cli/test_golden_path.py tests/docs/

   exit 0, `725 passed, 2 skipped in 97.64s`; no FAILED or ERROR line; the two SKIPPED lines read
   "main holds F294, so its own changes are history" and "main holds F293, so its own changes are
   history".
5. **Gate 3**: `python3 -m ruff check tests/conftest.py tests/test_data_root_isolation.py tests/orchestration/test_serve_daemon.py` — exit 0, `All checks passed!`.
6. **Gate 4** (`python3 -m apps.cli.main integrity check --json`): exit 0, `"check_count": 6`, all six
   `pass`, `"fail_count": 0`, `"ok": true`.
7. **Gate 5**: exit 0, `['R-1138', 'R-1139', 'R-1143', 'R-1149', 'R-1156', 'R-1157', 'R-1158',
   'R-1160', 'R-1162', 'R-1172', 'R-1176', 'R-1191']`.
8. Gate 6 (after the push): reported in the worker's reply, not here.

## Authored-text proofs

- `block.md` to `.agent/authored/f253-r7.md`: 140 lines, byte-equal, sha256
  `f6844d6aaa5623d20446e943a738a158586d04a75933d41155f40347594ad849`.
- `append-live_review.txt` and `append-decisions.txt` appended to their base blobs at `028f31736`:
  each "post equals pre plus slice" True.
- `dry-plan.md` to `.agent/plan.md`, `dry-test_serve_daemon.py`, `dry-conftest.py` and
  `dry-test_data_root_isolation.py` to their paths: byte-equal (Verification items 1 to 3).
- `dry-operator_questions.md` to `.agent/operator_questions.md`: byte-equal, proved before this commit.

## Deviations & assumptions

One deviation: a single shell call that ran gate 3 and gate 5 began with a `cd` to the primary
checkout (`cd /home/decodeux/Repos/remedy 2>/dev/null; ...`), against the block's "never `cd`". The
gate scripts set their own working directory, so the `cd` changed no reading; no later call used it.
Otherwise none: C1 to C3 landed in the order and under the subjects the block gave, touching only the
paths it named, no commit passed 500 insertions (largest C1, 166), the gates ran once each, in order,
after C3 and before this commit. Gate 2 read 725 passed; the block named no count.

## Round verdicts

Round 6's PASS and R-1191's registration are booked by this round's C1. Round 7's verdict is the
reviewer's, written into the next round's first commit.

## For the operator, in plain sentences

Round six's work passed review. As the operator asked, the tests can no longer reach the operator's
own data folder by accident, because every test process now points its settings at a temporary folder
from the moment it starts and removes that folder when it ends. The three practice records are still
there, because the repository's settings do not let the loop read the data folder, so the loop could
not see what it would delete, and the new question in the questions file says exactly which entries to
remove. A test now holds that the background service's web listener stops completely when the service
stops.

## Next

1. Phase 1 rule 1 (`.agent/STOP`): if it appears, finish the commit in hand, write the handback and
   stop.
2. Then the Open PR Gate: there is no pull request for this branch yet, so it finds none to merge.
3. Then book round 7's verdict in the next round's first commit.
4. Then S4: answer a decision, approve an apply with its commit and push, decline a result, through
   the F009 door and the supervisor's run launcher, after a design reading of
   `_dispatch_decision_resolve` against `remedy decision resolve`.

Operator questions open: 1.
Open findings: 12 (R-1160, Medium; R-1138, R-1139, R-1143, R-1149, R-1156, R-1157, R-1158, R-1162,
R-1172 and R-1176, Low, owned by F297; R-1191, Low, owned by F253, its test landed by C2 and awaiting
the reviewer's resolution).

## Item status

| Item | Status | Reason |
|---|---|---|
| C1: book round 6 and R-1191, DECISION F253 D8, the plan and the block | done | `644cc4d3e` |
| C2: a test holds that the supervisor's API thread ends with it (R-1191) | done | `60f881d09` |
| C3: every test process gets an import-time data root (DECISION F253 D8) | done | `4cf369e64` |
| Gates 1 to 5 | done | all green, run once each, before this file was written |
| C4: this handback and operator question Q11 | done | this commit |
| Push, Gate 6 | pending | reported in the worker's reply |
