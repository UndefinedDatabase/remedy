# Handoff — F253 round 23: book round 22, repair R-1208: a client reads a run's end, the gate tests wait for it

## Session

SESSION 5 of feature F253 · round 23 · rounds so far 23

Context self-assessment: the reviewer's context is workable after five rounds; the session continues
with the hardening stage's acceptance audit.

Fortschritt: ~93 % (S1 to S7 · hardening and closure open) — Schätzung

## Range

Review of `4cbcd332b599098e821cc83bd75567e7017ea27b`..`96995dabf3799c27f05b63cdfcd4cd0c33944c8b`
(the last commit before this handback, C3x).

## Commits

### 00b34fff5 F253 R23 C1: book round 22, resolve R-1205 and R-1206, register R-1208, DECISION F253 D20, the plan and the block

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f253-r23.md` | 187/0 | new file, byte copy of `block.md` (187 lines, sha256 `d1fc4fec23d0608026fce1357f6b73559de0b71e88015374caa8620a453d7898`) |
| `.agent/decisions.md` | 10/0 | `append-decisions.txt`'s bytes appended: DECISION F253 D20 |
| `.agent/live_review.md` | 8/0 | `append-live_review.txt`'s bytes appended: round 22's gate entry, VERDICT PASS, R-1205 and R-1206 resolved, R-1208 |
| `.agent/plan.md` | 15/14 | `dry-plan.md`, byte for byte |

### 9ace1b8b1 F253 R23 C2: remedy client run reads the run the supervisor started for a job (DECISION F253 D20)

| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/serve_runs.py` | 47/0 | `run_state`, `run_answer`, `run_not_found_message` and `run_record_payload`, each beside its order twin, docstrings naming DECISION F253 D20; `run_state` keeps `paths` for symmetry and does not read it |
| `apps/cli/command_catalog.py` | 18/0 | the read-only entry `client.run`: one positional `job`, `--json`, exit codes 0 to 3 |
| `apps/cli/commands/client_cmd.py` | 38/0 | `_cmd_client_run`: `lookup_job_id`, refuses `run_not_found` with exit 3 when it raises `JobIdError` or no record is read, prints `Run of job <id>: <state>` without `--json`; module docstring paragraph |
| `apps/cli/client_interface.py` | 12/2 | the operation, its refusal token, its answer keys and its empty answer tree; `CLIENT_INTERFACE_VERSION` `1.5` with its comment |
| `docs/system/machine-client-contract-v1.md` | 16/1 | generated section regenerated with the writer (version `1.5`, the `remedy client run` entry) |
| `docs/guides/exit-codes.md` | 1/0 | the row `remedy client run` 3 |
| `tests/cli/test_client_interface.py` | 14/1 | version `1.5`; the static answer-key reader's site for `_cmd_client_run:**payload`; the real-run test calls `client.run` once for its refusal |
| `tests/cli/test_client_run_cmd.py` | 124/0 | new: an ended stand-in run through `RunLauncher` read by `remedy client run` as a child process (keys, values, answer), a job prefix, a saved job with no record, an unknown full id and two values that are no id, the summary without `--json` |
| `tests/orchestration/test_serve_runs.py` | 56/0 | `run_state` running, ended and lost; `run_answer` for a last line that is no envelope and one that is; `run_record_payload` keys while running and once ended; the message |

### 07e24aca8 F253 R23 C3: a client polls a run over HTTP, and the gate tests wait for its end (R-1208)

| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/public_api.py` | 57/9 | route `GET /api/v1/jobs/{job}/run`, twin `client.run`, refusal `run_not_found` 404, placed before the POST run route; `_run_answer` in `_TWIN_ANSWERS`; `_start_run_answer` answers 202 with `run_record_payload`; `PUBLIC_API_VERSION` `1.10`; module and function docstrings name DECISION F253 D20; the POST row's description now sends a client to the poll |
| `docs/system/public-http-api-v1.md` | 12/5 | hand-written "Runs": the 202 answer also holds `state` and `answer`, the poll, why a client waits for it, 404 `run_not_found`; generated section regenerated (version `1.10`, the new row, the POST row) |
| `tests/ui_server/test_public_api.py` | 74/5 | `PINNED_ROUTES` gains the route; both version assertions read `1.10`; the POST run pin test selects the POST route by method; the 202 test holds `state` and `answer`; four new tests: the pin, the poll equals `remedy client run <job> --json` for an ended stand-in run (and a prefix), 404 `run_not_found` for a job with no record, 404 for a value that is no id |
| `tests/orchestration/test_public_api_gate_paths.py` | 70/42 | `Supervisor.ended_run` polls the run route until `state` is not `running` and asserts `ended` and exit code 0; called after each `start_run` (F295's path, the order of two jobs); every assertion on an HTTP answer carries that answer; docstring names R-1208 |

### 96995dabf F253 R23 C3x: client.run's descriptions carry the vocabulary page's meaning fragments

| Path | +/- | Reason |
|---|---|---|
| `apps/cli/command_catalog.py` | 5/2 | the command's and the argument's descriptions reworded to carry the fragment "task" (Job and Run) |
| `docs/system/machine-client-contract-v1.md` | 2/2 | generated section regenerated |

### This commit (self-reference)

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | this commit | this file; a handback cannot table the commit that writes it |
| `.agent/operator_questions.md` | this commit | byte copy of `dry-operator_questions.md`: Q13 |

## External actions

- `git push origin feature/f253-public-http-api`, once, after this commit: reported in the
  worker's reply, not here (this file is written before the push).
- No pull request opened, no full suite, no mutation, no worktree, no merge, no new branch, no
  force-push, no pull, no `REMEDY_TEST_MAX_WORKERS`, no `-n`. No command of mine read, listed or
  wrote the repository's own `.data`. No test started a real provider: every order was `no_llm`
  with both providers `fake`, every run named both providers `fake`, and every stand-in run was a
  test's own.

## Verification

0. Preconditions, before any write: `block.md` read sha256
   `d1fc4fec23d0608026fce1357f6b73559de0b71e88015374caa8620a453d7898`; `append-live_review.txt`,
   `append-decisions.txt`, `dry-plan.md` and `dry-operator_questions.md` each matched their
   `digests.txt` entry (Python `hashlib`); `git rev-parse HEAD` and
   `origin/feature/f253-public-http-api` both read `4cbcd332b599098e821cc83bd75567e7017ea27b`;
   `git status --porcelain` empty; `.agent/STOP` absent. `git branch --show-current` read
   `feature/f253-public-http-api` before each commit.
1. **Gate 1**: `git status --porcelain` empty after C3x; C1's byte proofs, one script, read from the
   committed blobs of `00b34fff5`: the authored copy equals `block.md`, `.agent/plan.md` equals
   `dry-plan.md`, `.agent/live_review.md` and `.agent/decisions.md` each equal their blob at the
   base followed by their slice — all True.
2. **Gate 2**, the block's selection from the primary checkout (18 test targets, as ordered):
   the first run read exit 1, `1 failed, 1191 passed in 139.43s (0:02:19)`; the one failure was
   `tests/docs/test_vocabulary.py::test_every_binding_word_in_a_description_carries_the_pages_meaning`,
   whose assertion read `descriptions use a binding word against the page: [('arg:client.run:job:description', 'Job'), ('arg:client.run:job:description', 'Run'), ('command:client.run:description', 'Job'), ('command:client.run:description', 'Run')]`.
   The cause was C2's own descriptions; fixed in C3x. The second run, after C3x: exit 0, tail
   `1192 passed in 146.66s (0:02:26)`, no FAILED, ERROR or SKIPPED line. Two runs in all.
3. **Gate 3**: `python3 -m ruff check` on the ten Python files C2 and C3 touched — exit 0,
   `All checks passed!`.
4. **Gate 4**: `python3 -m apps.cli.main integrity check --json` — exit 0, `"check_count": 6`, all
   six `pass`, `"fail_count": 0`.
5. **Gate 5**: the open-finding reader — exit 0, `['R-1138', 'R-1139', 'R-1143', 'R-1149',
   'R-1156', 'R-1157', 'R-1158', 'R-1160', 'R-1162', 'R-1172', 'R-1176', 'R-1196', 'R-1207',
   'R-1208']`, as ordered.
6. Gate 6 (after the push): reported in the worker's reply, not here.

## Authored-text proofs

- `block.md` to `.agent/authored/f253-r23.md`: 187 lines, byte-equal, sha256
  `d1fc4fec23d0608026fce1357f6b73559de0b71e88015374caa8620a453d7898`.
- `append-live_review.txt` and `append-decisions.txt` each appended to their base blob at
  `4cbcd332b`: "post equals pre plus slice" True for both.
- `dry-plan.md` to `.agent/plan.md`: byte-equal.
- `dry-operator_questions.md` to `.agent/operator_questions.md`: copied byte for byte in this
  commit.

## Deviations & assumptions

- An extra commit, `96995dabf` (C3x): gate 2's first run was red in
  `tests/docs/test_vocabulary.py` because C2's description of `client.run` and of its `job`
  argument used the binding words Job and Run without a fragment of the vocabulary page's meaning
  table. I reworded both (they now contain "task") and regenerated the machine client page.
  Gate 2 therefore ran twice.
- Files outside the paths the block names per commit, as the precedent's guards forced: none of
  C2's files lies outside the named paths (`docs/system/machine-client-contract-v1.md` is the
  generated page the block orders regenerated); `docs/system/machine-client-contract-v1.md` was
  also changed by C3x for the reworded description.
- Choices left to me: the wording of every description, docstring and page sentence; the summary
  line `Run of job <id>: <state>`; an ambiguous job prefix is refused `run_not_found` like any
  value `lookup_job_id` refuses (the block lists `JobIdError` as the one case); the stand-in run in
  `test_client_run_cmd.py` prints an envelope naming the job id, and the test saves its job on the
  scratch data root with `monkeypatch.setenv("REMEDY_DATA_DIR", ...)` and `save_job_plan`;
  `test_public_api.py`'s poll test imports `_start_ended_run` from `tests/cli/test_client_run_cmd.py`
  as the order poll test imports `_start_ended_order`; the 202 test of the POST run route now
  expects `state` `lost` and `answer` null because its stand-in record names a process of no run
  of that job and a log that does not exist; the existing pin test of the POST run route selects
  its route by method, since two routes now share the path; `test_vocabulary.py` was not touched.
  `ended_run` is called after each of the two `start_run` calls in the file (F295's path and the
  order of two jobs), the only places a test starts a run; the other three tests start none.
  Every assertion in the file that reads an HTTP answer now carries it (some by binding the
  digest first); assertions on git state and files carry what they already carried.
- Diff reading: the block-copy hunk of C1 (lines 1 to 193 of its diff file, headers included) was
  not read, as the block allows for a byte-proven copy; every other diff was read whole before its
  commit.
- Single test files run while writing: `test_client_run_cmd.py` with the new `test_serve_runs.py`
  tests (14 passed), `test_client_interface.py`, `test_exit_codes.py`, `test_command_catalog.py` and
  `test_machine_client_contract.py` (460 passed), `test_public_api.py` (180 passed),
  `test_public_api_gate_paths.py` (5 passed), then `test_vocabulary.py` with
  `test_machine_client_contract.py` after C3x (14 passed); ruff before each commit.
- The `remedy` command installed on this machine was never run; every Remedy call was
  `python3 -m apps.cli.main` from the checkout, or a child given `PYTHONPATH` naming it.

## Round verdicts

Round 22's PASS, with R-1205 and R-1206 resolved and R-1208 registered, is booked by C1 above.
Round 23's verdict is the reviewer's.

## For the operator, in plain sentences

Round twenty-two's work passed review, and the review found one more thing: a program could not
tell when a run it had started was really over, because Remedy's overview calls a job finished a
moment before its run has ended, and one of the new tests failed once, probably because of that; a
program can now ask about a run directly and wait for its true end, and the tests do so. The second
question below tells you that the `remedy` command installed on this computer runs old code, and
how to fix that.

## Next

1. Phase 1 rule 1 (`.agent/STOP`): if it appears, finish the commit in hand, write the handback and
   stop.
2. Then the Open PR Gate (rule 2): no pull request for this branch, none to merge.
3. Then book round 23's verdict and resolve R-1208 in the next round's first commit.
4. Then the amend0930b-slow-cap hardening stage: the acceptance audit.

Operator questions open: 2.
Open findings: 14 (R-1208, Low, owned by F253; R-1160, Medium, and R-1138, R-1139, R-1143, R-1149,
R-1156, R-1157, R-1158, R-1162, R-1172, R-1176, R-1196 and R-1207, Low, owned by F297).

## Item status

| Item | Status | Reason |
|---|---|---|
| C1: book round 22, resolve R-1205 and R-1206, register R-1208, DECISION F253 D20, the plan and the block | done | `00b34fff5` |
| C2: `remedy client run` reads the run the supervisor started for a job | done | `9ace1b8b1` |
| C3: a client polls a run over HTTP, and the gate tests wait for its end (R-1208) | done | `07e24aca8` |
| C3x: `client.run`'s descriptions carry the vocabulary page's meaning fragments | done | `96995dabf`, forced by gate 2's first run |
| Gates 1 to 5 | done | all green (gate 2 on its second run) |
| C4: this handback and operator question Q13 | done | this commit |
| Push, Gate 6 | pending | reported in the worker's reply |
