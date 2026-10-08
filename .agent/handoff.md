# Handoff — F304 session 4, round 14: T006's last part, what the call and token caps count, and a run stopped at each (DECISION F304 D15)

## Session

SESSION 4 of feature F304 · round 14 · rounds so far 14

Context self-assessment: the reviewer's context is comfortable; the session continues.

Fortschritt: ~78 % (T002 to T006 done · T007, the hardening stage and the closure open) —
Schätzung

## Range

Review of `f66e5638c40f6ad56210ea96588335463b02ee37`..HEAD (HEAD is C3 below, which carries this
handback).

## Commits

### ece1bc895 F304 R14 C1: book round 13, DECISION F304 D15, the plan and the block

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f304-r14.md` | 119/0 (new) | byte copy of `block.md` |
| `.agent/decisions.md` | 10/0 | its bytes at `f66e5638c` followed by `append-decisions.txt` (DECISION F304 D15) |
| `.agent/live_review.md` | 2/0 | its bytes at `f66e5638c` followed by `append-live_review.txt` (round 13's gate entry) |
| `.agent/plan.md` | 9/7 | `dry-plan.md`, byte for byte |

### 762319874 F304 R14 C2: what the call and token caps count, and a run stopped at each (T006, DECISION F304 D15)

| Path | +/- | Reason |
|---|---|---|
| `docs/system/machine-client-contract-v1.md` | 8/0 | the order-file section says what `max-provider-calls` and `max-total-tokens` count |
| `tests/cli/test_do_order_file.py` | 105/0 | a test provider that reports usage, an order capped only by calls or only by tokens stopped at its cap, the digest's calls and tokens by kind, the page's sentences |

## External actions

- None before the push. The push of this branch after C3 is reported in the worker's final reply.
- No full suite, no mutation, no worktree, no merge, no new branch, no force-push, no pull.

## Verification

0. Before any write: `block.md`, `sim-readings.txt` and `digests.txt` matched the prompt's sha256
   digests (Python `hashlib.sha256`, 3 of 3 True), and the five other files listed in
   `digests.txt` matched it (5 of 5 True). `git rev-parse HEAD` and
   `origin/feature/f304-machine-client-contract-v1-1-part-two` both read
   `f66e5638c40f6ad56210ea96588335463b02ee37`, `git status --porcelain` was empty, `.agent/STOP`
   was absent. `git branch --show-current` read the feature branch before each commit (checked
   inside the commit script).
1. C1 proofs: the authored copy is 119 lines, sha256
   `67e070e5abdc1977a2408f718e86d4d31f1e711627a820261675a835080d1e83`, byte-equal to `block.md`.
   `.agent/live_review.md` equals `git show f66e5638c:.agent/live_review.md` plus
   `append-live_review.txt` (pre 230830 bytes, slice 1948, post 232778), post equals pre plus
   slice, True. `.agent/decisions.md` likewise (pre 3092053 bytes, slice 3863, post 3095916), True,
   the file never read whole. `.agent/plan.md` equals `dry-plan.md`, True. `git diff --cached
   --numstat` read `119 0`, `10 0`, `2 0`, `9 7`, the cells of `sim-readings.txt`. The staged diff
   (22047 bytes) was written to a file and read whole.
2. C2 proofs: the two prepared files each equal their target, True two of two. `git diff --cached
   --numstat` read `8 0`, `105 0`, the cells of `sim-readings.txt`. The staged diff was written to
   a file and read whole.
3. **Gate 1** (`git -C /home/decodeux/Repos/remedy status --porcelain`, after C2): exit 0, empty;
   the byte proofs of C1 and C2 above all True.
4. **Gate 2** (`python3 -m ruff check tests/cli/test_do_order_file.py`): exit 0,
   `All checks passed!`.
5. **Gate 3** (`python3 -m pytest -q -rfEs` on the block's selection, run once, through a Python
   wrapper capturing the exit code): exit 0, last line `674 passed in 67.17s (0:01:07)`; no
   FAILED, ERROR or SKIPPED line; `git status --porcelain` empty again after.
6. **Gate 4** (`python3 -m apps.cli.main integrity check --json`): exit 0, `"check_count": 6`, all
   six `pass`, `"fail_count": 0`; then `open_finding_ids`: exit 0, `['R-1138', 'R-1139', 'R-1143',
   'R-1149', 'R-1156', 'R-1157', 'R-1158', 'R-1160', 'R-1162', 'R-1172', 'R-1176']`.
7. **Gate 5** (after the push): reported in the worker's final reply.

## Authored-text proofs

- `block.md` to `.agent/authored/f304-r14.md`: 119 lines, byte-equal, sha256
  `67e070e5abdc1977a2408f718e86d4d31f1e711627a820261675a835080d1e83`.
- `append-live_review.txt` and `append-decisions.txt`: post equals pre plus slice in bytes, once
  each (Verification item 1 above).
- `dry-plan.md` to `.agent/plan.md`: byte-equal (Verification item 1 above).
- `pre-machine-client-contract-v1.md` and `pre-test_do_order_file.py` to their targets:
  byte-equal, two of two (Verification item 2 above).

## Deviations & assumptions

None.

## Round verdicts

Round 13's PASS is booked by C1. Round 14's verdict is the reviewer's, given after this handback.

## For the operator, in plain sentences

The contract page now states what the two newer limits count. The limit on calls counts every
call to the model that builds and the model that reviews, a repeated call included. The limit on
tokens counts the tokens sent to and received from those models, never the tokens a provider
serves from its cache. Remedy checks a limit before each call, so the last call can take a run a
little past a token limit. The test models Remedy's own tests use count toward neither limit,
because they cost nothing. A test now shows that a run really stops when it reaches a call limit
or a token limit. No program code changed in this round, and nothing waits for the operator.

## Next

1. Phase 1 rule 1 (`.agent/STOP`): if it appears, finish the commit in hand, write the handback
   and stop.
2. Then Phase 1 rule 2, the Open PR Gate.
3. Then T007: the default digest lists what still needs something and what ended inside a window,
   names the window and how many jobs it left out, and a flag widens it; its first step measures
   the operator's own data root.

Operator questions open: 0.
Open findings: 11 (R-1160, Medium; R-1138, R-1139, R-1143, R-1149, R-1156, R-1157, R-1158, R-1162,
R-1172 and R-1176, Low; all owned by F297).

## Item status

| Item | Status | Reason |
|---|---|---|
| C1: book round 13, DECISION F304 D15, the plan and the block | done | `ece1bc895` |
| C2: what the call and token caps count, and a run stopped at each | done | `762319874` |
| Gates 1 to 4 | done | all green, before this file was written |
| C3: handback | done | this commit |
| Push, gate 5 | open | reported in the worker's final reply |
