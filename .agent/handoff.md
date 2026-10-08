# Handoff — F304 session 3, round 12: T006's first part, each job's calls and tokens by kind, and the day's tokens (DECISION F304 D13)

## Session

SESSION 3 of feature F304 · round 12 · rounds so far 12

Context self-assessment: the reviewer's context is comfortable; the session continues.

Fortschritt: ~70 % (T002 to T005 done · T006's calls and tokens landed · T006's cap and
token sentence, T007, the hardening stage and the closure open) — Schätzung

## Range

Review of `59687dfe75906dbacff302b3b3de2730c105064e`..HEAD (HEAD is C3 below, which carries this
handback).

## Commits

### d934cf7a2 F304 R12 C1: book round 11, DECISION F304 D13, the plan and the block

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f304-r12.md` | 125/0 (new) | byte copy of `block.md` (125 lines, sha256 `4e0a5d6634414006c888f919e5bbe637b934236e106c88af3c1427aba2bbdb5a`) |
| `.agent/decisions.md` | 10/0 | its bytes at `59687dfe7` followed by `append-decisions.txt` (DECISION F304 D13) |
| `.agent/live_review.md` | 2/0 | its bytes at `59687dfe7` followed by `append-live_review.txt` (round 11's gate entry) |
| `.agent/plan.md` | 8/7 | `dry-plan.md`, byte for byte |

### 0798adf5c F304 R12 C2: each job in the digest carries its calls and tokens by kind (T006, DECISION F304 D13)

| Path | +/- | Reason |
|---|---|---|
| `apps/cli/client_interface.py` | 12/3 | `TOKENS_BY_KIND_KEY_TREE`; the digest's two new job keys, `calls` and `tokens`, and `cost_today`'s new `tokens` key |
| `docs/system/machine-client-contract-v1.md` | 14/5 | the read section's new sentence on calls and tokens by kind, the regenerated key and answer-key tables |
| `packages/orchestration/client_digest.py` | 73/15 | `_tokens_by_kind`, `_known_sum`, `_merged_usage`, `_day_tokens`, the ledger reads inside `build_client_digest`, each job's `calls` and `tokens`, and `cost_today`'s `tokens` |
| `packages/orchestration/token_ledger.py` | 20/0 | `ledger_usage_by_job`, one grouped read per ledger, nulls kept, rows without a job id left out |
| `tests/cli/test_status_cmd.py` | 20/0 | the command-line test reads a real fake run's calls and null tokens, held to `query_cost` |
| `tests/orchestration/test_client_digest.py` | 81/3 | the kinds, the sums, a job no ledger names, two ledgers' rows added, an unreadable ledger |
| `tests/orchestration/test_token_ledger.py` | 27/0 | `ledger_usage_by_job`'s grouped read, nulls kept, never creating the ledger |

## External actions

- None before this file is committed. The push of the branch and its outcome (every attempt) are
  in the worker's final reply (write-once rule; not known when this file is written).
- No `gh` command, no full suite, no mutation, no worktree, no merge, no new branch, no
  force-push, no pull.

## Verification

0. Before any write: `block.md` (125 lines), `sim-readings.txt` and `digests.txt` matched the
   prompt's sha256 digests (Python `hashlib.sha256`, 3 of 3 True), and the ten other prepared
   files listed in `digests.txt` matched it (10 of 10 True). `git rev-parse HEAD` and
   `origin/feature/f304-machine-client-contract-v1-1-part-two` both read
   `59687dfe75906dbacff302b3b3de2730c105064e`, `git status --porcelain` was empty, `.agent/STOP`
   was absent. `git branch --show-current` read the feature branch before each commit (checked
   inside each commit's script).
1. C1 proofs: the authored copy is 125 lines, sha256
   `4e0a5d6634414006c888f919e5bbe637b934236e106c88af3c1427aba2bbdb5a`, byte-equal to `block.md`.
   `.agent/live_review.md` and `.agent/decisions.md` each equal `git show 59687dfe7:<path>` plus
   their append file, True (the decisions proof by byte and sha256 comparison of the built bytes
   against the file on disk, the file itself never read whole). `.agent/plan.md` equals
   `dry-plan.md`, True. `git diff --cached --numstat` read `125 0`, `10 0`, `2 0`, `8 7`, the
   cells of `sim-readings.txt`. The staged diff (187 lines, 23111 bytes) was written to a file and
   read whole.
2. C2 proofs: the seven prepared files each equal their target, True seven of seven, each
   verified byte for byte against `digests.txt`'s own sha256 before the copy and against the file
   on disk after. `git diff --cached --numstat` read `12 3`, `14 5`, `73 15`, `20 0`, `20 0`,
   `81 3`, `27 0`, the cells of `sim-readings.txt`. `git status --porcelain` showed exactly the
   seven C2 paths staged, nothing else. The staged diff (465 lines, 25264 bytes) was written to a
   file and read whole.
3. **Gate 1** (`git -C /home/decodeux/Repos/remedy status --porcelain`, after C2): exit 0, empty;
   the byte proofs of C1 and C2 above all True.
4. **Gate 2** (`python3 -m ruff check packages/orchestration/client_digest.py
   apps/cli/client_interface.py packages/orchestration/token_ledger.py
   tests/orchestration/test_client_digest.py tests/cli/test_status_cmd.py
   tests/orchestration/test_token_ledger.py`): exit 0, `All checks passed!`.
5. **Gate 3** (`python3 -m pytest -q -rfEs` on the block's selection, run once, through a Python
   wrapper capturing the exit code): exit 0, last line `765 passed in 112.22s (0:01:52)`; the full
   transcript was scanned for FAILED, ERROR and SKIPPED lines, none found; `git status
   --porcelain` empty again after.
6. **Gate 4** (`python3 -m apps.cli.main integrity check --json`): exit 0, `"check_count": 6`, all
   six `pass`, `"fail_count": 0`; then `open_finding_ids`: exit 0, `['R-1138', 'R-1139', 'R-1143',
   'R-1149', 'R-1156', 'R-1157', 'R-1158', 'R-1160', 'R-1162', 'R-1172', 'R-1176']`.
7. **Gate 5** (after the push): reported in the worker's final reply.

## Authored-text proofs

- `block.md` to `.agent/authored/f304-r12.md`: 125 lines, byte-equal, sha256
  `4e0a5d6634414006c888f919e5bbe637b934236e106c88af3c1427aba2bbdb5a`.
- `append-live_review.txt` and `append-decisions.txt`: post equals pre plus slice in bytes, once
  each (Verification item 1 above).
- `dry-plan.md` to `.agent/plan.md`: byte-equal (Verification item 1 above).
- The seven C2 files (`pre-client_digest.py`, `pre-client_interface.py`, `pre-token_ledger.py`,
  `pre-machine-client-contract-v1.md`, `pre-test_client_digest.py`, `pre-test_status_cmd.py`,
  `pre-test_token_ledger.py`) to their targets: byte-equal, seven of seven (Verification item 2
  above).

## Deviations & assumptions

None.

## Round verdicts

Round 11's PASS is booked by C1.

Round 12's verdict is the reviewer's.

## For the operator, in plain sentences

The overview a program reads from Remedy now names, for every job, how many calls it made to a
model and how many tokens those calls used, split into input, output, tokens read from the cache
and tokens written to the cache, and the same token split for each project's day beside the day's
cost and calls. These numbers come from the cost records Remedy already keeps for each project,
read once per project. A kind of token no model reported stays empty instead of reading zero,
which is what the test models do, because they report no usage. If a project's cost records
cannot be read, the overview says so. Letting an order be capped by tokens, calls or minutes
instead of money follows in the next round, and nothing waits for the operator.

## Next

1. Phase 1 rule 1 (`.agent/STOP`): if it appears, finish the commit in hand, write the handback
   and stop.
2. Then Phase 1 rule 2, the Open PR Gate.
3. Then T006's next part: an order's mandatory cap may be any one job budget.

Operator questions open: 0.
Open findings: 11 (R-1160, Medium; R-1138, R-1139, R-1143, R-1149, R-1156, R-1157, R-1158, R-1162,
R-1172 and R-1176, Low; all owned by F297).

## Item status

| Item | Status | Reason |
|---|---|---|
| C1: book round 11, DECISION F304 D13, the plan and the block | done | `d934cf7a2` |
| C2: each job in the digest carries its calls and tokens by kind | done | `0798adf5c` |
| Gates 1 to 4 | done | all green, before this file was written |
| C3: handback | done | this commit |
| Push, gate 5 | pending at write time | outcomes in the worker's final reply |
