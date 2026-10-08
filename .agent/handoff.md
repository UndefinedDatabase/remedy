# Handoff — F304 session 2, round 8: R-1184's repair, `remedy job run` refuses a run that ended blocked, failed or at its budget (DECISION F304 D8)

## Session

SESSION 2 of feature F304 · round 8 · rounds so far 8

Context self-assessment: the reviewer's context is comfortable; the session continues.

Fortschritt: ~52 % (T002 to T004 done · R-1184 landed · T005 to T007 open) — Schätzung

## Range

Review of `e430266a5b6517c5bcdcd557752b1ea7531d43f5`..HEAD (HEAD is C3 below, which carries this
handback).

## Commits

### 9b1a27a2e F304 R8 C1: book round 7, DECISION F304 D8, the plan and the block

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f304-r8.md` | 125/0 (new) | byte copy of `block.md` (125 lines, sha256 `4d442ecc491788a165a315bc63b031663551c5e8ff079a14e53e9b11d91159a5`) |
| `.agent/decisions.md` | 10/0 | its bytes at `e430266a5` followed by `append-decisions.txt` (DECISION F304 D8) |
| `.agent/live_review.md` | 2/0 | its bytes at `e430266a5` followed by `append-live_review.txt` (round 7's gate entry) |
| `.agent/plan.md` | 11/9 | `dry-plan.md`, byte for byte |

### 3e5d24e4e F304 R8 C2: remedy job run refuses a run that ended blocked, failed or at its budget (R-1184, DECISION F304 D8)

| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | 2/0 | append-landed.txt's slice, byte for byte |
| `apps/cli/client_interface.py` | 6/6 | `job.run` and `job.resume` declare `job_blocked`, `job_failed`, `job_stopped_by_budget` |
| `apps/cli/commands/do_cmd.py` | 25/2 | `_cmd_job_run` refuses a `blocked`, `failed` or budget-`stopped` end with its report and exit 1 |
| `docs/system/machine-client-contract-v1.md` | 7/3 | the refusal sentence and the regenerated `job.run`/`job.resume` tables |
| `tests/cli/test_do_sequence_cli.py` | 5/4 | the budget-stop test now reads exit 1 and `job_stopped_by_budget` |
| `tests/cli/test_job_run_end_states.py` | 100/0 (new) | drives a real blocked run and every end state through the handler |
| `tests/orchestration/test_f018_authority_integration.py` | 13/8 | the signature test expects exit 1 for its nonexistent job |
| `tests/orchestration/test_job_worktree_handoff.py` | 7/3 | the resume test expects exit 1 for the one-round blocked run |
| `tests/ui_server/test_task_edit_e2e_live.py` | 3/1 | its deliberately blocked run now reads exit 1 and the blocked sentence |
| `tests/ui_server/test_task_veto_e2e_live.py` | 6/2 | its two deliberately blocked runs now read exit 1 and the blocked sentence |

## External actions

- None before this file is committed. The push of the branch and its outcome (every attempt) are
  in the worker's final reply (write-once rule; not known when this file is written).
- No `gh` command, no full suite, no mutation, no worktree, no merge, no new branch, no
  force-push, no pull.

## Verification

0. Before any write: `block.md` (125 lines), `sim-readings.txt` and `digests.txt` matched the
   prompt's sha256 digests (Python `hashlib.sha256`, 3 of 3 True), and the thirteen other prepared
   files listed in `digests.txt` matched it (13 of 13 True). `git rev-parse HEAD` and
   `origin/feature/f304-machine-client-contract-v1-1-part-two` both read
   `e430266a5b6517c5bcdcd557752b1ea7531d43f5`, `git status --porcelain` was empty, `.agent/STOP`
   was absent. `git branch --show-current` read the feature branch before each commit (checked
   inside each commit script).
1. C1 proofs: the authored copy is 125 lines, sha256
   `4d442ecc491788a165a315bc63b031663551c5e8ff079a14e53e9b11d91159a5`, byte-equal to its source.
   `.agent/live_review.md` and `.agent/decisions.md` each equal `git show e430266a5:<path>` plus
   their append file, True (the decisions proof by byte comparison of the built bytes against the
   file on disk, the file itself never read whole). `.agent/plan.md` equals `dry-plan.md`, True.
   `git diff --cached --numstat` read `125 0`, `10 0`, `2 0`, `11 9`, the cells of
   `sim-readings.txt`. The staged diff (195 lines) was written to a file and read whole.
2. C2 proofs: the nine prepared files each equal their target, True nine of nine, each verified
   byte for byte against `digests.txt`'s own sha256 before the copy and against the file on disk
   after. `git diff --cached --numstat` read `2 0`, `6 6`, `25 2`, `7 3`, `5 4`, `100 0`, `13 8`,
   `7 3`, `3 1`, `6 2`, the cells of `sim-readings.txt`. `git status --porcelain` showed exactly
   the ten C2 paths staged, nothing else. The staged diff (352 lines) was written to a file and
   read whole.
3. **Gate 1** (`git -C /home/decodeux/Repos/remedy status --porcelain`, after C2): exit 0, empty;
   the byte proofs of C1 and C2 above all True.
4. **Gate 2** (`python3 -m ruff check apps/cli/commands/do_cmd.py apps/cli/client_interface.py
   tests/cli/test_job_run_end_states.py tests/cli/test_do_sequence_cli.py
   tests/orchestration/test_f018_authority_integration.py
   tests/orchestration/test_job_worktree_handoff.py tests/ui_server/test_task_edit_e2e_live.py
   tests/ui_server/test_task_veto_e2e_live.py`): exit 0, `All checks passed!`.
5. **Gate 3** (`python3 -m pytest -q -rfEs` on the block's selection, run once, through a Python
   wrapper capturing the exit code): exit 0, last line `2199 passed in 378.21s (0:06:18)`; the
   full transcript was scanned for FAILED, ERROR and SKIPPED lines, none found; `git status
   --porcelain` empty again after.
6. **Gate 4** (`python3 -m apps.cli.main integrity check --json`): exit 0, `"check_count": 6`, all
   six `pass`, `"fail_count": 0`; then `open_finding_ids`: exit 0, `['R-1138', 'R-1139', 'R-1143',
   'R-1149', 'R-1156', 'R-1157', 'R-1158', 'R-1160', 'R-1162', 'R-1172', 'R-1176', 'R-1184']`.
7. **Gate 5** (after the push): reported in the worker's final reply.

## Authored-text proofs

- `block.md` to `.agent/authored/f304-r8.md`: 125 lines, byte-equal, sha256
  `4d442ecc491788a165a315bc63b031663551c5e8ff079a14e53e9b11d91159a5`.
- `append-live_review.txt`, `append-decisions.txt` and `append-landed.txt`: post equals pre plus
  slice in bytes, once each (Verification items 1 and 2 above).
- `dry-plan.md` to `.agent/plan.md`: byte-equal (Verification item 1 above).
- The nine C2 files (`pre-do_cmd.py`, `pre-client_interface.py`,
  `pre-machine-client-contract-v1.md`, `pre-test_job_run_end_states.py`,
  `pre-test_do_sequence_cli.py`, `pre-test_f018_authority_integration.py`,
  `pre-test_job_worktree_handoff.py`, `pre-test_task_edit_e2e_live.py`,
  `pre-test_task_veto_e2e_live.py`) to their targets: byte-equal, nine of nine (Verification item
  2 above).

## Deviations & assumptions

None.

## Round verdicts

Round 7's PASS is booked by C1.

Round 8's verdict is the reviewer's.

## For the operator, in plain sentences

The command which runs a job on now says plainly when the job got stuck, failed, or stopped
because its spending limit ran out: it answers that it did not succeed, names which of the three
happened with one fixed word, keeps every detail it gave before, and ends with exit code 1. A job
that finished, or paused or stopped because the operator asked, answers as before. This repairs
the problem the reviewer found in the round before, and nothing waits for the operator.

## Next

1. Phase 1 rule 1 (`.agent/STOP`): if it appears, finish the commit in hand, write the handback and
   stop.
2. Then Phase 1 rule 2, the Open PR Gate.
3. Then book round 8's verdict and R-1184's resolution in the next round's first commit.
4. Then T005: what an approval card needs, from records only.

Operator questions open: 1.
Open findings: 12 (R-1160 and R-1184, Medium; R-1138, R-1139, R-1143, R-1149, R-1156, R-1157,
R-1158, R-1162, R-1172 and R-1176, Low; R-1184 owned by F304 and landed, the rest by F297).

## Item status

| Item | Status | Reason |
|---|---|---|
| C1: book round 7, DECISION F304 D8, the plan and the block | done | `9b1a27a2e` |
| C2: R-1184's repair, the nine files and the landed record | done | `3e5d24e4e` |
| Gates 1 to 4 | done | all green, before this file was written |
| C3: handback | done | this commit |
| Push, gate 5 | pending at write time | outcomes in the worker's final reply |
