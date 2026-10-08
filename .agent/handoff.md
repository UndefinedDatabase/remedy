# Handoff — F304 session 2, round 4: T003's first part, an approved apply that did not land answers ok false with one token per cause (DECISION F304 D4)

## Session

SESSION 2 of feature F304 · round 4 · rounds so far 4

Context self-assessment: the reviewer's context is comfortable; the session continues.

Fortschritt: ~26 % (T002 done · T003 half done · T004 to T007 open) — Schätzung

## Range

Review of `ecfb1929190b95c23d4cd0855e1459dcc2c81e73`..HEAD (HEAD is C3 below, which carries this handback).

## Commits

### 98645d1c7 F304 R4 C1: book round 3, resolve R-1183, DECISION F304 D4, the plan and the block

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f304-r4.md` | 129/0 (new) | byte copy of `block.md` (129 lines, sha256 `24888258df3db238f94cc81869749da80ad9448149b0db9dd2a23a32c6f6f948`) |
| `.agent/decisions.md` | 10/0 | its bytes at `ecfb19291` followed by `append-decisions.txt` (DECISION F304 D4) |
| `.agent/live_review.md` | 4/0 | its bytes at `ecfb19291` followed by `append-live_review.txt` (round 3's gate entry, R-1183's `Done:` paragraph) |
| `.agent/plan.md` | 8/7 | `dry-plan.md`, byte for byte |
| `.agent/prose_slips.md` | 3/0 | its bytes at `ecfb19291` followed by `append-prose_slips.txt` (three prose slips) |

### 2cc75eb5c F304 R4 C2: an approved apply that did not land answers ok false with one token per cause (T003, DECISION F304 D4)

| Path | +/- | Reason |
|---|---|---|
| `apps/cli/client_interface.py` | 6/1 | `job.apply` declares its fifteen `APPLY_REFUSAL_TOKENS` in `OPERATION_REFUSAL_TOKENS` |
| `apps/cli/command_catalog.py` | 3/0 | `job.apply` declares `exit_codes=(0, 1, 2, 3)` |
| `apps/cli/commands/do_cmd.py` | 26/4 | `_cmd_job_apply` refuses a flag clash with `invalid_argument` and exit 2 before the job is read, and answers a refusal with `apply_refusal`'s token, exit 3 for `job_not_found`/`job_not_ready`, else exit 1 |
| `docs/guides/exit-codes.md` | 1/0 | `remedy job apply` lists exit 3 |
| `docs/system/machine-client-contract-v1.md` | 9/3 | order-file section names the refusal and its exit codes; generated section (exit codes, refusal tokens) written again |
| `packages/orchestration/job_apply.py` | 103/6 | `apply_refusal`, `APPLY_REFUSAL_TOKENS`, `APPLY_NOT_READY_TOKENS` and the sentence-opening constants the token reader and the tests share |
| `tests/cli/test_client_interface.py` | 13/0 | the hand-verified token site for `_cmd_job_apply`'s `error`, held equal to `APPLY_REFUSAL_TOKENS` |
| `tests/cli/test_job_apply_refusals.py` | 232/0 (new) | drives each of the six named causes, a missing job, a flag clash, two previews and the text answer through the command line, and reads every token from a table of results |
| `tests/orchestration/test_job_apply.py` | 9/5 | three pinned "a blocked apply exits 0" assertions now read exit 1 with their token |
| `tests/orchestration/test_job_apply_commit.py` | 9/4 | the flag-clash test now reads exit 2 and `invalid_argument` before the job is read |
| `tests/orchestration/test_job_apply_history.py` | 3/2 | the refused-merge test now reads exit 1 and `target_dirty` |

## External actions

- None before this file is committed. The push of the branch and its outcome (every attempt) are in the worker's final reply (write-once rule; not known when this file is written).
- No `gh` command, no full suite, no mutation, no worktree, no merge, no new branch, no force-push, no pull.

## Verification

0. Before any write: `block.md` (129 lines), `sim-readings.txt` and `digests.txt` matched the prompt's sha256 digests (Python `hashlib.sha256`, 3 of 3 True), and the fifteen other prepared files listed in `digests.txt` matched it (15 of 15 True). `git rev-parse HEAD` and `origin/feature/f304-machine-client-contract-v1-1-part-two` both read `ecfb1929190b95c23d4cd0855e1459dcc2c81e73`, `git status --porcelain` was empty, `.agent/STOP` was absent. `git branch --show-current` read the feature branch before each commit (checked inside each commit script).
1. C1 proofs: the authored copy is 129 lines, sha256 `24888258df3db238f94cc81869749da80ad9448149b0db9dd2a23a32c6f6f948`, byte-equal to its source. `.agent/live_review.md`, `.agent/prose_slips.md` and `.agent/decisions.md` each equal `git show ecfb19291:<path>` plus their append file, True (the decisions proof by sha256 comparison of the built bytes against the file on disk, the file itself never read whole). `.agent/plan.md` equals `dry-plan.md`, True. `git diff --cached --numstat` read `129 0`, `10 0`, `4 0`, `8 7`, `3 0`, the cells of `sim-readings.txt`. The staged diff (208 lines) was written to a file and read whole.
2. C2 proofs: the eleven files equal their prepared files, True eleven of eleven, each sha256-verified. `git diff --cached --numstat` read `6 1`, `3 0`, `26 4`, `1 0`, `9 3`, `103 6`, `13 0`, `232 0`, `9 5`, `9 4`, `3 2`, the cells of `sim-readings.txt`. `git status --porcelain` showed exactly the eleven C2 paths staged, nothing else. The staged diff (689 lines) was written to a file and read whole.
3. **Gate 1** (`git -C /home/decodeux/Repos/remedy status --porcelain`, after C2): exit 0, empty; the byte proofs of C1 and C2 above all True.
4. **Gate 2** (`python3 -m ruff check` on the nine named files): exit 0, `All checks passed!`.
5. **Gate 3** (`python3 -m pytest -q -rfEs` on the block's selection, run once, through a Python wrapper capturing the exit code): exit 0, last line `2043 passed in 429.39s (0:07:09)`; the full transcript was scanned for FAILED, ERROR and SKIPPED lines, none found.
6. **Gate 4** (`python3 -m apps.cli.main integrity check --json`): exit 0, `"check_count": 6`, all six `pass`, `"fail_count": 0`.
7. **Gate 5** (`open_finding_ids`): exit 0, `['R-1138', 'R-1139', 'R-1143', 'R-1149', 'R-1156', 'R-1157', 'R-1158', 'R-1160', 'R-1162', 'R-1172', 'R-1176']`.
8. **Gate 6** (after the push): reported in the worker's final reply.

## Authored-text proofs

- `block.md` to `.agent/authored/f304-r4.md`: 129 lines, byte-equal, sha256 `24888258df3db238f94cc81869749da80ad9448149b0db9dd2a23a32c6f6f948`.
- `append-live_review.txt`, `append-prose_slips.txt` and `append-decisions.txt`: post equals pre plus slice in bytes, once each (Verification item 1 above).
- `dry-plan.md` to `.agent/plan.md`, and the eleven C2 files to their targets: byte-equal (Verification items 1 and 2 above).

## Deviations & assumptions

None. (Gates ran one script at a time, after C2 and before C3, as ordered; gate 1's status read was taken after C2 was committed, its byte proofs before.)

## Round verdicts

Round 3's PASS and R-1183's resolution are booked by C1.

Round 4's verdict is the reviewer's.

## For the operator, in plain sentences

Until now, when a program asked Remedy to apply a job's result and the apply was stopped — for example because the folder had unsaved changes or the push was not allowed — Remedy still answered "success" with exit code 0 and hid the reason inside the answer. From now on such an answer says plainly that it failed, names the cause with one fixed word a program can check (one word each for unsaved changes, a branch that is not checked out, a merge conflict, protected files, no place to push to, and a push the mission's own acceptance criteria forbid), keeps every detail it gave before, and ends with exit code 1, or 3 when the job does not exist or is not finished. A preview without the approval still answers as before. The description Remedy gives a program lists all these words. Nothing waits for the operator.

## Next

1. Phase 1 rule 1 (`.agent/STOP`): if it appears, finish the commit in hand, write the handback and stop.
2. Then Phase 1 rule 2, the Open PR Gate.
3. Then book round 4's verdict in the next round's first commit.
4. Then T003's second part: a command that declines a completed job's result, and a declined job or a job of an abandoned mission no longer waits for its apply.

Operator questions open: 1.
Open findings: 11 (R-1160, Medium; R-1138, R-1139, R-1143, R-1149, R-1156, R-1157, R-1158, R-1162, R-1172 and R-1176, Low, owned by F297).

## Item status

| Item | Status | Reason |
|---|---|---|
| C1: book round 3, resolve R-1183, DECISION F304 D4, the plan and the block | done | `98645d1c7` |
| C2: an approved apply that did not land answers ok false with one token per cause | done | `2cc75eb5c` |
| Gates 1 to 5 | done | all green, before this file was written |
| C3: handback | done | this commit |
| Push, gate 6 | pending at write time | outcomes in the worker's final reply |
