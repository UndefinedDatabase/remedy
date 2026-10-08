# Handoff — F304 session 2, round 8: R-1184's repair, `remedy job run` refuses a run that ended blocked, failed or at its budget (DECISION F304 D8)

## Session

SESSION 2 of feature F304 · round 8 · rounds so far 8

Context self-assessment: the session ends after round 8's review, at five delegated rounds (F304's
rounds 4 to 8), below the six-to-eight target, because the reviewer's context is long and three
of its own authoring slips were caught by its dry runs this session, while the next slice, T005,
is a new design over the digest, the job and contract records and the interface's key tree that
a fresh session starts better.

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

- None before round 8's handback was committed. Round 8's worker then pushed once, without a
  retry, and the reviewer read `19df4ef80` as both the local tip and
  `origin/feature/f304-machine-client-contract-v1-1-part-two`, with the tree clean. This session-close
  commit is pushed by its own worker, whose reply carries that push.
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

Round 8: VERDICT PASS, given by the reviewer of F304's second session after this handback.
Drafted for the next round's first commit, to be appended to `.agent/live_review.md` by that
round's reviewer, in this order:

`Gate: F304 R8 — the F304 round 8 entry, R-1184's repair, over `e430266a5`..`19df4ef80` (3 commits,
each single-parent; insertions by `git show --numstat`: `9b1a27a2e` 148, `3e5d24e4e` 174,
`19df4ef80` 66), followed by the session's closing commit, which touches only `.agent/handoff.md`.
VERDICT PASS, verified by dry run, bytes identical, compared at `9b1a27a2e` and `3e5d24e4e`
against the prepared files of the reviewer's dry run on `e430266a5`. `.remedy-wt/f304-r8/review8.py`,
whose readings are saved beside it as `review8-readings.txt`, read the saved block, `.agent/plan.md`
and the two appended records at `9b1a27a2e`, and the nine C2 files and the ledger's `Landed:` line
at `3e5d24e4e`, equal to the prepared files, fourteen of fourteen, and every one of them unchanged
at `19df4ef80`, which touches only `.agent/handoff.md`. The dry run's readings, saved as
`.remedy-wt/f304-r8/dry-readings.txt`: ruff clean on the eight Python files, the round's selection
`2199 passed` at exit 0, and six mutations, each red and green again after: a budget stop answering
ok, an operator's stop refused as a budget stop, a blocked run answering ok, a failed run answering
ok, the blocked refusal dropping the report, and an end the client asked for answering nothing.
The dry run's first readings were red where the reviewer's first edit was wrong and where tests
pinned the old answer: the report bound to an empty dict hid its keys from the interface's static
reading, stand-in jobs that carry no state raised, and tests that drive a run to a blocked or
budget-stopped end pinned exit 0; the handler and those tests were corrected before any file was
handed over. A live test's UI server rebuilt the stale `apps/ui/dist` by itself during the
selection and touched no tracked file. The worker's one run of the same selection on the same bytes
read `2199 passed`, with the tree clean after it. Every reflog entry after `e430266a5` is one of the
round's commits, the local tip equalled the pushed branch and the tree was clean. The worker
declared no deviation. The open set is `['R-1138', 'R-1139', 'R-1143', 'R-1149', 'R-1156',
'R-1157', 'R-1158', 'R-1160', 'R-1162', 'R-1172', 'R-1176', 'R-1184']`; R-1184 is resolved below.`

`Done: R-1184 — RESOLVED at F304 round 8 by `3e5d24e4e`, verified by the reviewer of F304's second
session. At `3e5d24e4e`, `_cmd_job_run` in `apps/cli/commands/do_cmd.py` answers a run that ends
`blocked`, `failed` or stopped by its budget with `job_blocked`, `job_failed` or
`job_stopped_by_budget`, every key of the job's report beside the token and exit 1, and a run that
completes, pauses at the operator's request or at `--tasks`, or stops at the operator's request as
before; `job.run` and `job.resume` declare the tokens; `tests/cli/test_job_run_end_states.py`
drives a real blocked run through the command line and every end state through the handler; each
of the six mutations the round's gate entry names turned its test red, green again after.`

And for `.agent/prose_slips.md`, one line:

`2026-10-08, F304 round 8 — the reviewer's first edit bound the job report to an empty dict, which
hid its keys from the interface's static reading, and read the state of stand-in jobs that carry
none; the dry run caught both and they were corrected before any file was handed over, so nothing
on disk differs.`

The outer backticks of each drafted paragraph mark where it begins and ends; the paragraph itself
is booked without them, on one line.

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
3. Then confirm that `origin`'s tip equals the tip of this branch before delegating.
4. Then, in the next round's first commit: book round 8's verdict, R-1184's `Done:` paragraph and
   the prose slip, all drafted above, as written.
5. Then T005: what an approval card needs, from records only. Its first round reads, whole,
   `build_client_digest` in `packages/orchestration/client_digest.py`, `DIGEST_KEY_TREE` in
   `apps/cli/client_interface.py` and the tests in `tests/cli/test_client_interface.py` that hold it
   to the dict literals the digest writes, the job record's task fields (`reviewer_verdict`,
   `repair_rounds_used`, `test_passed` and the test command), the apply manifests' `applied_files`,
   and `read_mission_contract` for a mission's blocking criteria; and it sizes the card against
   T007's bound, 65,536 bytes for the default digest of 1,000 settled jobs (DECISION F298 D1), so
   the changed-file list is bounded from the start.
6. Under SLOW MODE, the hardening stage of operator amendment amend0930b-slow-cap runs after T007
   and before the closure sequence; the closure's one full suite builds `apps/ui` first (DECISION
   F304 D5 (7)).

Operator questions open: 1.
Open findings: 12 (R-1160 and R-1184, Medium; R-1138, R-1139, R-1143, R-1149, R-1156, R-1157,
R-1158, R-1162, R-1172 and R-1176, Low; R-1184 owned by F304 and landed, the rest by F297).

## Item status

| Item | Status | Reason |
|---|---|---|
| C1: book round 7, DECISION F304 D8, the plan and the block | done | `9b1a27a2e` |
| C2: R-1184's repair, the nine files and the landed record | done | `3e5d24e4e` |
| Gates 1 to 4 | done | all green, before this file was written |
| C3: handback | done | `19df4ef80` |
| Push, gate 5 | done | `19df4ef80` equalled `origin/feature/f304-machine-client-contract-v1-1-part-two` after one push |
| Session close: round 8's verdict, R-1184's drafted resolution, the prose slip and the session's end | done | this commit |
