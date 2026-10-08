# Handoff — F304 session 3, round 13: T006's second part, an order's cap may be any one job budget (DECISION F304 D14)

## Session

SESSION 3 of feature F304 · round 13 · rounds so far 13

Context self-assessment: the reviewer's context is comfortable; the session continues.

Fortschritt: ~73 % (T002 to T005 done · T006's calls, tokens and caps landed · T006's
token sentence and stop at the cap, T007, the hardening stage and the closure open) —
Schätzung

## Range

Review of `2494ac701f460a3cfdce117622bef90e9a88f709`..HEAD (HEAD is C3 below, which carries this
handback).

## Commits

### b136478d6 F304 R13 C1: book round 12, DECISION F304 D14, the plan and the block

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f304-r13.md` | 125/0 (new) | byte copy of `block.md` |
| `.agent/decisions.md` | 10/0 | its bytes at `2494ac701` followed by `append-decisions.txt` (DECISION F304 D14) |
| `.agent/live_review.md` | 2/0 | its bytes at `2494ac701` followed by `append-live_review.txt` (round 12's gate entry) |
| `.agent/plan.md` | 7/8 | `dry-plan.md`, byte for byte |

### e244347e7 F304 R13 C2: an order's cap may be any one job budget (T006, DECISION F304 D14)

| Path | +/- | Reason |
|---|---|---|
| `apps/cli/commands/do_cmd.py` | 17/7 | fills each absent budget flag from the header, refuses only when all four caps are absent, the refusal's sentence names all four |
| `docs/system/machine-client-contract-v1.md` | 7/4 | the order-file section names the four caps and the rule, the refusal token keeps its old name |
| `packages/orchestration/order_file.py` | 25/19 | `ORDER_FILE_CAP_KEYS`, the three new header keys, `OrderFile`'s three new fields, the single-valued parse |
| `tests/cli/test_do_order_file.py` | 65/0 | the refusal's sentence, a header-only cap for each of the three, a flag alone and winning over the header, a cap that is no number |
| `tests/orchestration/test_order_file.py` | 23/0 | every header key read, a file without the other caps, a repeated cap key's line number |

## External actions

- `gh pr list --state open --json number,headRefName,baseRefName,isDraft` (Open PR Gate, before
  any write): `[]`, no open PRs.
- None else before this file is committed. The push of the branch and its outcome (every attempt)
  are in the worker's final reply (write-once rule; not known when this file is written).
- No full suite, no mutation, no worktree, no merge, no new branch, no force-push, no pull.

## Verification

0. Before any write: `block.md` (125 lines), `sim-readings.txt` and `digests.txt` matched the
   prompt's sha256 digests (Python `hashlib.sha256`, 3 of 3 True), and the eight other prepared
   files listed in `digests.txt` matched it (8 of 8 True). `git rev-parse HEAD` and
   `origin/feature/f304-machine-client-contract-v1-1-part-two` both read
   `2494ac701f460a3cfdce117622bef90e9a88f709`, `git status --porcelain` was empty, `.agent/STOP`
   was absent. `git branch --show-current` read the feature branch before each commit (checked
   inside each commit's script).
1. C1 proofs: the authored copy is 125 lines, sha256
   `1f9e6c2d7e31fb4ca3c89283093cc643dc04abae2fdadd6fd3acc1d4150a40aa`, byte-equal to `block.md`.
   `.agent/live_review.md` equals `git show 2494ac701:.agent/live_review.md` plus
   `append-live_review.txt`, proved post-bytes equal pre-bytes plus the append slice, True.
   `.agent/decisions.md` equals its pre-image at `2494ac701` plus `append-decisions.txt`, proved by
   streamed sha256 and length comparison (pre `3088847` bytes, append `3206` bytes, expected post
   `3092053` bytes, expected and actual post sha256 both
   `682af0c5dc8f37c2fff058fba6f47331846733911e321f02ac9cd86fdae73156`), the file itself never read
   whole. `.agent/plan.md` equals `dry-plan.md`, True. `git diff --cached --numstat` read
   `125 0`, `10 0`, `2 0`, `7 8`, the cells of `sim-readings.txt`. The staged diff (187 lines,
   21943 bytes) was written to a file and read whole.
2. C2 proofs: the five prepared files each equal their target, True five of five, each verified
   byte for byte against `digests.txt`'s own sha256 before the copy and against the file on disk
   after. `git diff --cached --numstat` read `17 7`, `7 4`, `25 19`, `65 0`, `23 0`, the cells of
   `sim-readings.txt`. `git status --porcelain` showed exactly the five C2 paths staged, nothing
   else. The staged diff (305 lines, 15259 bytes) was written to a file and read whole.
3. **Gate 1** (`git -C /home/decodeux/Repos/remedy status --porcelain`, after C2): exit 0, empty;
   the byte proofs of C1 and C2 above all True.
4. **Gate 2** (`python3 -m ruff check packages/orchestration/order_file.py
   apps/cli/commands/do_cmd.py tests/orchestration/test_order_file.py
   tests/cli/test_do_order_file.py`): exit 0, `All checks passed!`.
5. **Gate 3** (`python3 -m pytest -q -rfEs` on the block's selection, run once, through a Python
   wrapper capturing the exit code): exit 0, last line `954 passed in 111.06s (0:01:51)`; the full
   transcript was scanned for FAILED, ERROR and SKIPPED lines, none found; `git status
   --porcelain` empty again after.
6. **Gate 4** (`python3 -m apps.cli.main integrity check --json`): exit 0, `"check_count": 6`, all
   six `pass`, `"fail_count": 0`; then `open_finding_ids`: exit 0, `['R-1138', 'R-1139', 'R-1143',
   'R-1149', 'R-1156', 'R-1157', 'R-1158', 'R-1160', 'R-1162', 'R-1172', 'R-1176']`.
7. **Gate 5** (after the push): reported in the worker's final reply.

## Authored-text proofs

- `block.md` to `.agent/authored/f304-r13.md`: 125 lines, byte-equal, sha256
  `1f9e6c2d7e31fb4ca3c89283093cc643dc04abae2fdadd6fd3acc1d4150a40aa`.
- `append-live_review.txt` and `append-decisions.txt`: post equals pre plus slice in bytes, once
  each (Verification item 1 above).
- `dry-plan.md` to `.agent/plan.md`: byte-equal (Verification item 1 above).
- The five C2 files (`pre-order_file.py`, `pre-do_cmd.py`, `pre-machine-client-contract-v1.md`,
  `pre-test_order_file.py`, `pre-test_do_order_file.py`) to their targets: byte-equal, five of
  five (Verification item 2 above).

## Deviations & assumptions

None.

## Round verdicts

Round 12's PASS is booked by C1.

Round 13's verdict is the reviewer's.

## For the operator, in plain sentences

An order written as a file no longer has to carry a spending limit in dollars: it may instead
carry a limit on tokens, on calls to a model, or on minutes of running time, written at the top
of the file or given on the command line. An order with none of the four limits is still refused
before anything runs, and the refusal now names all four. A limit given on the command line still
wins over the one in the file. The next round writes down exactly which tokens the token limit
counts and shows that a run really stops at a token or call limit, and nothing waits for the
operator.

## Next

1. Phase 1 rule 1 (`.agent/STOP`): if it appears, finish the commit in hand, write the handback
   and stop.
2. Then Phase 1 rule 2, the Open PR Gate.
3. Then T006's last part: the page says which tokens the token budget counts, and an order capped
   only by calls or by total tokens is stopped at its cap.

Operator questions open: 0.
Open findings: 11 (R-1160, Medium; R-1138, R-1139, R-1143, R-1149, R-1156, R-1157, R-1158, R-1162,
R-1172 and R-1176, Low; all owned by F297).

## Item status

| Item | Status | Reason |
|---|---|---|
| C1: book round 12, DECISION F304 D14, the plan and the block | done | `b136478d6` |
| C2: an order's cap may be any one job budget | done | `e244347e7` |
| Gates 1 to 4 | done | all green, before this file was written |
| C3: handback | done | this commit |
| Push, gate 5 | pending at write time | outcomes in the worker's final reply |
