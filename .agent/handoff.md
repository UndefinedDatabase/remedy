# Handoff — F304 session 4, round 15: T007's first part, the digest lists what needs something and the jobs that ended last (DECISION F304 D16)

## Session

SESSION 4 of feature F304 · round 15 · rounds so far 15

Context self-assessment: the reviewer's context is comfortable; the session continues.

Fortschritt: ~84 % (T002 to T006 done · T007's window landed · T007's template question, the
hardening stage and the closure open) — Schätzung

## Range

Review of `5eabb405924de6a9191b154829ac1396b6568885`..HEAD (HEAD is C3 below, which carries this
handback).

## Commits

### 97b4a534e F304 R15 C1: book round 14, DECISION F304 D16, the plan and the block

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f304-r15.md` | 129/0 | new file, byte copy of `block.md` |
| `.agent/decisions.md` | 10/0 | its bytes at `5eabb4059` followed by `append-decisions.txt` (DECISION F304 D16) |
| `.agent/live_review.md` | 2/0 | its bytes at `5eabb4059` followed by `append-live_review.txt` (round 14's gate entry) |
| `.agent/plan.md` | 8/9 | `dry-plan.md`, byte for byte |

### fdd780428 F304 R15 C2: the digest lists what needs something and the jobs that ended last (T007, DECISION F304 D16)

| Path | +/- | Reason |
|---|---|---|
| `apps/cli/client_interface.py` | 2/1 | `job_window` joins `DIGEST_KEY_TREE` |
| `apps/cli/command_catalog.py` | 2/0 | the `--all-ended-jobs` flag of `status` |
| `apps/cli/commands/status_cmd.py` | 8/2 | the handler passes the flag to the digest builder |
| `docs/system/machine-client-contract-v1.md` | 14/4 | step 2 says what `jobs` holds and what has ended; the generated section written again |
| `packages/orchestration/client_digest.py` | 48/5 | the ended-job window, `job_window`, `every_ended_job` |
| `tests/cli/test_client_interface.py` | 1/1 | the pinned digest call |
| `tests/cli/test_status_cmd.py` | 64/0 | 1,000 settled jobs through the command line, and the flag |
| `tests/orchestration/test_client_digest.py` | 116/0 | order, creation fallback, every kind of job that needs something, the flag, an unreadable job, the page's sentence |

## External actions

- None before the push. The push of this branch after C3 is reported in the worker's final reply.
- No full suite, no mutation, no worktree, no merge, no new branch, no force-push, no pull.

## Verification

0. Before any write: `block.md`, `sim-readings.txt` and `digests.txt` matched the prompt's sha256
   digests (Python `hashlib.sha256`, 3 of 3 True), and the eleven files listed in
   `digests.txt` matched it (11 of 11 True). `git rev-parse HEAD` and
   `origin/feature/f304-machine-client-contract-v1-1-part-two` both read
   `5eabb405924de6a9191b154829ac1396b6568885`, `git status --porcelain` was empty, `.agent/STOP`
   was absent. `git branch --show-current` read the feature branch before each commit (checked
   inside the commit script).
1. C1 proofs: the authored copy is 129 lines, sha256
   `fa859198cdcca9a48f568f436b187df889428c58c0bf17420062759840ec83c0`, byte-equal to `block.md`.
   `.agent/live_review.md` equals `git show 5eabb4059:.agent/live_review.md` plus
   `append-live_review.txt` (pre 232778 bytes, slice 2176, post 234954), post equals pre plus
   slice, True. `.agent/decisions.md` likewise (pre 3095916 bytes, slice 4608, post 3100524), True,
   the file never read whole. `.agent/plan.md` equals `dry-plan.md`, True. `git diff --cached
   --numstat` read `129 0`, `10 0`, `2 0`, `8 9`, the cells of `sim-readings.txt`. The staged diff
   (24512 bytes) was written to a file and read whole.
2. C2 proofs: the eight prepared files each equal their target, True eight of eight. `git diff
   --cached --numstat` read the eight cells of `sim-readings.txt`. The staged diff (25244 bytes)
   was written to a file and read whole.
3. **Gate 1** (`git -C /home/decodeux/Repos/remedy status --porcelain`, after C2): exit 0, empty;
   the byte proofs of C1 and C2 above all True.
4. **Gate 2** (`python3 -m ruff check` on the six Python files): exit 0, `All checks passed!`.
5. **Gate 3** (`python3 -m pytest -q -rfEs` on the block's selection, run once, through a Python
   wrapper capturing the exit code): exit 0, last line `1250 passed in 81.10s (0:01:21)`; no
   FAILED, ERROR or SKIPPED line; `git status --porcelain` empty again after.
6. **Gate 4** (`python3 -m apps.cli.main integrity check --json`): exit 0, `"check_count": 6`, all
   six `pass`, `"fail_count": 0`; then `open_finding_ids`: exit 0, `['R-1138', 'R-1139', 'R-1143',
   'R-1149', 'R-1156', 'R-1157', 'R-1158', 'R-1160', 'R-1162', 'R-1172', 'R-1176']`.
7. **Gate 5** (after the push): reported in the worker's final reply.

## Authored-text proofs

- `block.md` to `.agent/authored/f304-r15.md`: 129 lines, byte-equal, sha256
  `fa859198cdcca9a48f568f436b187df889428c58c0bf17420062759840ec83c0`.
- `append-live_review.txt` and `append-decisions.txt`: post equals pre plus slice in bytes, once
  each (Verification item 1 above).
- `dry-plan.md` to `.agent/plan.md`: byte-equal (Verification item 1 above).
- The eight `pre-*` files to their targets: byte-equal, eight of eight (Verification item 2 above).

## Deviations & assumptions

None.

## Round verdicts

Round 14's PASS is booked by C1. Round 15's verdict is the reviewer's, given after this handback.

## For the operator, in plain sentences

The overview a program reads no longer lists every job ever run. It lists every job that still
needs something, such as an answer, an approval of its result or more work, and the twenty
finished jobs that finished last, and it says how many finished jobs it left out. One switch on
the status command lists them all. With a thousand finished jobs the overview stays at about
twenty-four thousand bytes instead of more than a million. On your own Remedy data folder the
overview stays about ten megabytes, because nearly all of its 11,653 old jobs still carry an open
question, 13,481 in all, and every such job still needs something. The next round decides whether
a small change to an existing repository needs a contract template of its own. Nothing waits for
you.

## Next

1. Phase 1 rule 1 (`.agent/STOP`): if it appears, finish the commit in hand, write the handback
   and stop.
2. Then Phase 1 rule 2, the Open PR Gate.
3. Then T007's template question: measure whether a small change to an existing repository needs a
   contract template of its own, and add one if it does.

Operator questions open: 0.
Open findings: 11 (R-1160, Medium; R-1138, R-1139, R-1143, R-1149, R-1156, R-1157, R-1158, R-1162,
R-1172 and R-1176, Low; all owned by F297).

## Item status

| Item | Status | Reason |
|---|---|---|
| C1: book round 14, DECISION F304 D16, the plan and the block | done | `97b4a534e` |
| C2: the digest lists what needs something and the jobs that ended last | done | `fdd780428` |
| Gates 1 to 4 | done | all green, before this file was written |
| C3: handback | done | this commit |
| Push, gate 5 | open | reported in the worker's final reply |
