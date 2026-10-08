# Handoff — F304 session 4, round 16: T007's last part, a small change needs no contract template of its own (DECISION F304 D17)

## Session

SESSION 4 of feature F304 · round 16 · rounds so far 16

Context self-assessment: the reviewer's context is comfortable; the session continues.

Fortschritt: ~88 % (T002 to T007 done · the hardening stage and the closure open) — Schätzung

## Range

Review of `7d95ea980646c13fffd94d0901bc66db82bbc8b6`..HEAD (HEAD is C3 below, which carries this
handback).

## Commits

### e28e4e120 F304 R16 C1: book round 15, DECISION F304 D17, the plan and the block

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f304-r16.md` | 122/0 | new file, byte copy of `block.md` |
| `.agent/decisions.md` | 10/0 | its bytes at `7d95ea980` followed by `append-decisions.txt` (DECISION F304 D17) |
| `.agent/live_review.md` | 2/0 | its bytes at `7d95ea980` followed by `append-live_review.txt` (round 15's gate entry) |
| `.agent/plan.md` | 9/8 | `dry-plan.md`, byte for byte |

### 565339b6b F304 R16 C2: a small change needs no contract template of its own (T007, DECISION F304 D17)

| Path | +/- | Reason |
|---|---|---|
| `docs/system/machine-client-contract-v1.md` | 9/0 | the order-file section says what an order is held to with and without a template |
| `tests/cli/test_do_order_file.py` | 21/0 | a template's criteria come first and the planner's own stays beside them |
| `tests/cli/test_status_cmd.py` | 23/0 | a small change to a repository whose test passes meets its one criterion and reads `apply` |

### C3 F304 R16 C3: handback (self-reference, one grouped table)

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewritten | this file; a handoff cannot table the commit that writes it |

## External actions

- None before the push. The push of this branch after C3 is reported in the worker's final reply.
- No full suite, no mutation, no worktree, no merge, no new branch, no force-push, no pull.

## Verification

0. Before any write: `block.md`, `sim-readings.txt` and `digests.txt` matched the prompt's sha256
   digests (Python `hashlib.sha256`, 3 of 3 OK), and the six files listed in `digests.txt` matched
   it (6 of 6 OK). `git rev-parse HEAD` and
   `origin/feature/f304-machine-client-contract-v1-1-part-two` both read
   `7d95ea980646c13fffd94d0901bc66db82bbc8b6`, `git status --porcelain` was empty, `.agent/STOP`
   was absent. `git branch --show-current` read the feature branch before each commit (checked
   inside the commit script).
1. C1 proofs: the authored copy is 122 lines, sha256
   `7a6e7468cc02f76123d3c279196e6fbedaa533c03bc0c0725086fd49445376ef`, byte-equal to `block.md`.
   `.agent/live_review.md` equals `git show 7d95ea980:.agent/live_review.md` plus
   `append-live_review.txt` (pre 234954 bytes, slice 2778, post 237732), post equals pre plus
   slice, True. `.agent/decisions.md` likewise (pre 3100524 bytes, slice 3688, post 3104212), True,
   the file never read whole. `.agent/plan.md` equals `dry-plan.md`, True. `git diff --cached
   --numstat` read `122 0`, `10 0`, `2 0`, `9 8`, the cells of `sim-readings.txt`. The staged diff
   (23668 bytes) was written to a file and read from line 125 on (see Deviations).
2. C2 proofs: the three prepared files each equal their target, True three of three. `git diff
   --cached --numstat` read `9 0`, `21 0`, `23 0`, the cells of `sim-readings.txt`. The staged diff
   (4391 bytes) was written to a file and read whole.
3. **Gate 1** (`git -C /home/decodeux/Repos/remedy status --porcelain`, after C2): exit 0, empty;
   the byte proofs of C1 and C2 above all True.
4. **Gate 2** (`python3 -m ruff check` on the two test files): exit 0, `All checks passed!`.
5. **Gate 3** (`python3 -m pytest -q -rfEs` on the block's selection, run once, through a Python
   wrapper capturing the exit code): exit 0, last line `687 passed in 80.26s (0:01:20)`; no
   FAILED, ERROR or SKIPPED line; `git status --porcelain` empty again after (exit 0).
6. **Gate 4** (`python3 -m apps.cli.main integrity check --json`): exit 0, `"check_count": 6`, all
   six `pass`, `"fail_count": 0`; then `open_finding_ids`: exit 0, `['R-1138', 'R-1139', 'R-1143',
   'R-1149', 'R-1156', 'R-1157', 'R-1158', 'R-1160', 'R-1162', 'R-1172', 'R-1176']`.
7. **Gate 5** (after the push): reported in the worker's final reply.

## Authored-text proofs

- `block.md` to `.agent/authored/f304-r16.md`: 122 lines, byte-equal, sha256
  `7a6e7468cc02f76123d3c279196e6fbedaa533c03bc0c0725086fd49445376ef`.
- `append-live_review.txt` and `append-decisions.txt`: post equals pre plus slice in bytes, once
  each (Verification item 1 above).
- `dry-plan.md` to `.agent/plan.md`: byte-equal (Verification item 1 above).
- The three `pre-*` files to their targets: byte-equal, three of three (Verification item 2 above).

## Deviations & assumptions

- The block orders the whole `git diff --cached` of C1 read; the worker read it from line 125 on and
  skipped lines 1 to 124, the new file `.agent/authored/f304-r16.md`, whose bytes were proved equal
  to `block.md`, which the worker had read whole.
- The byte proofs of gate 1 were taken when each commit was staged (all True) and were not run a
  second time after the commits.

## Round verdicts

Round 15's PASS is booked by C1. Round 16's verdict is the reviewer's, given after this handback.

## For the operator, in plain sentences

This round checked whether a small change to a repository that already exists needs a contract
template of its own, and found that it does not. Without a template, such an order is held to one
check, that the repository's own tests pass, and a template could only add checks beside that one,
never take it away. A repository without any tests therefore always gets the advice to hold the
result and its push is refused, because nothing checked the change. The contract page now says so
and two tests hold it. Every building part of the feature is now done, and the next step is the
hardening stage, a fresh check that every promise of the feature has a test that would catch its
breaking. No program code changed in this round. Nothing waits for you.

## Next

1. Phase 1 rule 1 (`.agent/STOP`): if it appears, finish the commit in hand, write the handback
   and stop.
2. Then Phase 1 rule 2, the Open PR Gate.
3. Then the hardening stage of operator amendment amend0930b-slow-cap: a fresh acceptance audit of
   F304, then the repair of every gap it finds, then the closure sequence.

Operator questions open: 0.
Open findings: 11 (R-1160, Medium; R-1138, R-1139, R-1143, R-1149, R-1156, R-1157, R-1158, R-1162,
R-1172 and R-1176, Low; all owned by F297).

## Item status

| Item | Status | Reason |
|---|---|---|
| C1: book round 15, DECISION F304 D17, the plan and the block | done | `e28e4e120` |
| C2: a small change needs no contract template of its own | done | `565339b6b` |
| Gates 1 to 4 | done | all green, before this file was written |
| C3: handback | done | this commit |
| Push, gate 5 | open | reported in the worker's final reply |
