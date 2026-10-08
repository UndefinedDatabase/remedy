# Handoff — F304 session 3, round 13: T006's second part, an order's cap may be any one job budget (DECISION F304 D14)

## Session

SESSION 3 of feature F304 · round 13 · rounds so far 13

Context self-assessment: the session ends after round 13's review, at five delegated rounds (F304's
rounds 9 to 13), below the six-to-eight target and above the floor of four, because the reviewer's
context is long after five full dry runs, and the next round, T006's last part, starts with a new
measurement: the reviewer's notes say a fake run's builder and reviewer calls are not counted as
provider calls, so an order capped by calls cannot stop with the fake providers as they are, and
how the budget engine counts calls and tokens has to be read before any change is designed. A
fresh session starts that reading better.

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
- None else before round 13's handback was committed. Round 13's worker then pushed once, without
  a retry, and the reviewer read `4e3452161` as both the local tip and
  `origin/feature/f304-machine-client-contract-v1-1-part-two`, with the tree clean. This
  session-close commit is pushed by its own worker, whose reply carries that push.
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

Round 13: VERDICT PASS, given by the reviewer of F304's third session after this handback. Drafted
for the next round's first commit, to be appended to `.agent/live_review.md` by that round's
reviewer:

`Gate: F304 R13 — the F304 round 13 entry, T006's caps, over `2494ac701`..`4e3452161` (3 commits,
each single-parent; insertions by `git show --numstat`: `b136478d6` 144, `e244347e7` 137,
`4e3452161` 62), followed by the session's closing commit, which touches only `.agent/handoff.md`.
VERDICT PASS, verified by dry run, bytes identical, compared at `b136478d6` and `e244347e7` against
the prepared files of the reviewer's dry run on `2494ac701`. `.remedy-wt/f304-r13/review13.py`,
whose readings are saved beside it as `review13-readings.txt`, read the saved block,
`.agent/plan.md` and the two appended records at `b136478d6` and the five C2 files at `e244347e7`,
equal to the prepared files and to the dry tree, nine of nine, and every one of them unchanged at
`4e3452161`, which touches only `.agent/handoff.md`. The dry run's readings, saved as
`.remedy-wt/f304-r13/dry-readings.txt`: ruff clean on the four Python files, the round's selection
`954 passed` at exit 0, and eight mutations, each red and green again after: the parser dropping
the header's total-tokens cap, the handler dropping the header's provider-calls cap and its
wall-clock cap, only the cost counting as a cap, the header winning over the flag, a
single-valued key repeating, the wall-clock key unknown to the header, and the refusal leaving out
a flag. A header cap that is no number was measured in the dry run before it was pinned:
`invalid_budget`, exit 2, no mission filed. The worker's one run of the same selection on the same
bytes read `954 passed`. The worker also ran a read-only `gh pr list` that the block did not
order; it answered `[]` and changed nothing. Every reflog entry after `2494ac701` is one of the
round's commits, the local tip equalled the pushed branch and the tree was clean. The worker
declared no deviation. The open set is `['R-1138', 'R-1139', 'R-1143', 'R-1149', 'R-1156',
'R-1157', 'R-1158', 'R-1160', 'R-1162', 'R-1172', 'R-1176']`.`

The outer backticks of the drafted paragraph mark where it begins and ends; it is booked without
them, on one line.

## For the operator, in plain sentences

An order written as a file no longer has to carry a spending limit in dollars: it may instead
carry a limit on tokens, on calls to a model, or on minutes of running time, written at the top
of the file or given on the command line. An order with none of the four limits is still refused
before anything runs, and the refusal now names all four. A limit given on the command line still
wins over the one in the file. The next round writes down exactly which tokens the token limit
counts and shows that a run really stops at a token or call limit, and nothing waits for the
operator.

This session ended after five working rounds. In them, the overview a program reads gained a
card for every finished job, with what changed, what was checked, the mission's conditions and a
one-word recommendation and risk; every job's calls and tokens; and orders gained limits by
tokens, calls or minutes. Each round was checked by the reviewer and passed. The next session
starts by finding out how Remedy counts calls and tokens against a limit, because the test models
seem not to count, before it proves that a run stops at such a limit.

## Next

1. Phase 1 rule 1 (`.agent/STOP`): if it appears, finish the commit in hand, write the handback
   and stop.
2. Then Phase 1 rule 2, the Open PR Gate.
3. Then confirm that `origin`'s tip equals the tip of this branch before delegating.
4. Then, in the next round's first commit: book round 13's verdict, drafted above, as written.
5. Then T006's last part. Its first round reads, before any design: how a provider call and its
   tokens reach a job's budget actuals and the budget check (`packages/orchestration/budget_guard.py`,
   whose line 65 states that the fake provider is skipped, `packages/orchestration/job_burn.py`,
   and where `run_job` in `packages/orchestration/pingpong_job.py` records `provider_call_count`
   and `total_tokens`), and measures in its dry run whether an order capped only by
   `max-provider-calls: 1` or `max-total-tokens: 1` stops with the fake providers. If it does not,
   that round decides between a test provider that reports usage and counts, and a finding, and
   the page states exactly which tokens the token budget counts (F298's claim measurement read
   that a job's `total_tokens` adds input and output tokens and leaves cache tokens out).
6. Then T007, the hardening stage of operator amendment amend0930b-slow-cap, and the closure
   sequence; the closure's one full suite builds `apps/ui` first (DECISION F304 D5 (7)).

Operator questions open: 0.
Open findings: 11 (R-1160, Medium; R-1138, R-1139, R-1143, R-1149, R-1156, R-1157, R-1158, R-1162,
R-1172 and R-1176, Low; all owned by F297).

## Item status

| Item | Status | Reason |
|---|---|---|
| C1: book round 12, DECISION F304 D14, the plan and the block | done | `b136478d6` |
| C2: an order's cap may be any one job budget | done | `e244347e7` |
| Gates 1 to 4 | done | all green, before this file was written |
| C3: handback | done | `4e3452161` |
| Push, gate 5 | done | `4e3452161` equalled `origin/feature/f304-machine-client-contract-v1-1-part-two` after one push |
| Session close: round 13's verdict, the session's end and the next session's first steps | done | this commit |
