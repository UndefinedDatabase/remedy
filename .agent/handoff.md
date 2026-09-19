# Handoff — F273 Findings paydown v1 · Round 4

## Session

SESSION 1 of feature F273 · round 4 · rounds so far 4

Context self-assessment: the worker read the block, AGENTS.md, DECISION F273 D4, the handback template, the three code diffs and the questions-file rule of the self-drive protocol; every figure below comes from a command run in this round, and the worker's context held all of it without loss.

## Range

Review of 4862e71a..HEAD — branch `feature/f273-findings-paydown-v1`.

## Summary

Round 4 books round 3's verdict, lands DECISION F273 D4 and builds T002's eight live repairs as the reviewer's dry run built them.
- C1 books Gate F273 R3 (VERDICT PASS) and the resolutions of R-0671, R-0689 and R-0690, lands DECISION F273 D4, rewrites the plan and saves the four payload copies.
- C2 (R-0518, R-0569, R-0649, R-0664): `test_vitest_passes` skips, naming the reason, when `apps/ui/node_modules` is absent; `write_runtime_config` defaults to `worker_port(2)`, with a test that two workers get two ports; the emitter walk skips any path with `node_modules` among its parts, with a red control; two source guards pin the feed card's `#{row.seq}` and the shell's one `onSelectNode`.
- C3 (R-0691, R-0708, R-0734, R-0815): the two helper assertions are renamed to what they hold and the class docstring states the residual; `test_command_channel.py` and `test_live_state.py` wait through `wait_for_server_info`; the stopped run is read through `load_run` and asserted unconditionally.
- C4 adds `tests/ui_server/server_start.py` (the one wait: absent, empty or half-written info is "not started yet", the wait lasts while the server thread lives, a 120-second backstop) with `tests/ui_server/test_server_start.py`, and switches the six other server-start copies to it.
- C5 is this handoff.

Landed: R-0518 — `43760c74`
Landed: R-0569 — `43760c74`
Landed: R-0649 — `43760c74`
Landed: R-0664 — `43760c74`
Landed: R-0691 — `5206ece6`
Landed: R-0708 — `5206ece6` (the named copy in `test_live_state.py`); the helper it now calls arrived in `b00a826f`
Landed: R-0734 — `5206ece6` (the named copy in `test_command_channel.py`); the helper it now calls arrived in `b00a826f`
Landed: R-0815 — `5206ece6`

## Commits

### 42268f04 F273 R4 C1: bookkeeping — round 3's verdict and three resolutions booked, DECISION F273 D4 landed
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f273-r4-block.md` | +109 / -0 | Byte copy of the block |
| `.agent/authored/f273-r4-decisions.md` | +43 / -0 | Byte copy of decisions.md |
| `.agent/authored/f273-r4-ledger.md` | +8 / -0 | Byte copy of ledger.md |
| `.agent/authored/f273-r4-plan.md` | +26 / -0 | Byte copy of plan.md |
| `.agent/decisions.md` | +43 / -0 | `4862e71a` bytes + decisions.md (DECISION F273 D4) |
| `.agent/live_review.md` | +8 / -0 | `4862e71a` bytes + ledger.md (Gate F273 R3, `Done:` R-0671, R-0689, R-0690) |
| `.agent/plan.md` | +10 / -13 | := plan.md |

237 insertions, 13 deletions (`git show --numstat`).

### 43760c74 F273 R4 C2: R-0518, R-0569, R-0649, R-0664 — vitest skips without node_modules, the smoke port is per worker, the emitter walk skips vendored files, the feed seq and the one callback are pinned
| Path | +/- | Reason |
|------|-----|--------|
| `tests/orchestration/test_product_smoke.py` | +25 / -1 | R-0569: default port `worker_port(2)`, two-worker test — `git apply .remedy-wt/f273-proto-t002a.diff` |
| `tests/orchestration/test_test_runner.py` | +10 / -0 | R-0518: `skipif` absent `apps/ui/node_modules` — same diff |
| `tests/ui_contracts/test_brain_stream_ring.py` | +29 / -0 | R-0664: feed card prints `#{row.seq}`; shell hands one `onSelectNode` — same diff |
| `tests/ui_contracts/test_humanize_catalog.py` | +50 / -14 | R-0649: `emitter_sources` skips `node_modules`, `literals_emitted_by`, red-controlled test — same diff |

114 insertions, 15 deletions.

### 5206ece6 F273 R4 C3: R-0691, R-0708, R-0734, R-0815 — the helper assertions say what they hold, two server starts wait on the thread, the stopped run is read through its store
| Path | +/- | Reason |
|------|-----|--------|
| `tests/orchestration/test_job_stop_integration.py` | +10 / -7 | R-0815: read through `load_run`, absence fails, assertion unconditional — `git apply .remedy-wt/f273-proto-t002b.diff` |
| `tests/ui_contracts/test_decision_answer_wiring.py` | +14 / -5 | R-0691: two assertions renamed, class docstring states the residual — same diff |
| `tests/ui_server/test_command_channel.py` | +5 / -8 | R-0734: waits through `wait_for_server_info` — same diff |
| `tests/ui_server/test_live_state.py` | +3 / -8 | R-0708: waits through `wait_for_server_info` — same diff |

32 insertions, 28 deletions.

### b00a826f F273 R4 C4: the six other server-start copies wait on the thread through one helper, pinned by its own tests
| Path | +/- | Reason |
|------|-----|--------|
| `tests/ui_server/server_start.py` | +71 / -0 | New: `read_server_info`, `wait_for_server_info`, `SERVER_START_BACKSTOP_S` — `git apply .remedy-wt/f273-proto-t002c.diff` |
| `tests/ui_server/test_server_start.py` | +98 / -0 | New: half-written file retried, slow live start waited for, dead thread fails at once, backstop ends a hung start — same diff |
| `tests/ui_server/test_command_dispatch.py` | +4 / -7 | Waits through the helper — same diff |
| `tests/ui_server/test_decisions_endpoint.py` | +5 / -9 | Same — same diff |
| `tests/ui_server/test_diff_endpoint.py` | +9 / -14 | Same, both copies — same diff |
| `tests/ui_server/test_digest_route.py` | +5 / -9 | Same — same diff |
| `tests/ui_server/test_server_concurrency.py` | +4 / -9 | Same — same diff |

196 insertions, 48 deletions.

### C5 (this commit) F273 R4 C5: handoff
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/handoff.md` | rewritten | This handback |

Every commit is under 500 inserted lines. The largest is C1, with 237.

## External actions

- `git worktree add --detach .remedy-wt/f273-r4-g5 b00a826f` for G5 (exit 0), then `git worktree remove .remedy-wt/f273-r4-g5` (exit 0). `git worktree list` afterwards:
  ```
  /home/decodeux/Repos/remedy                         b00a826f [feature/f273-findings-paydown-v1]
  /home/decodeux/Repos/remedy/.remedy-wt/f273-r4-dry  4862e71a (detached HEAD)
  ```
- After C5: `git push`. No pull request is opened.

## Verification

Exit codes were read through `.remedy-wt/f273-r4/wk_run.py <cwd> <outfile|-> cmd...` (runs with an explicit `cwd`, prints the output or, with an outfile, its last 15 lines and its line count, then `EXIT <returncode>`); every gate ran with `cwd=/home/decodeux/Repos/remedy` except G5, which ran in its own worktree. Interpreter: Python 3.10.12.

- **Transport**, before any write: `sha256sum` of the three payloads, the block and the three diffs matched the block's digests (block.md `c45278f50851556fcb35cbfd25aa897204bbc2bf4ac41e6091a3415ef1d7b192`); `.remedy-wt/f273-r4/wk_c1.py` re-checked the four payloads (MATCH) before writing.
- **G1** (at C4 `b00a826f`, clean tree): `python3 .remedy-wt/f273-r4/wk_g1.py`, EXIT 0:
  ```
  True digest plan.md
  True digest ledger.md
  True digest decisions.md
  True digest block.md
  True digest f273-proto-t002a.diff
  True digest f273-proto-t002b.diff
  True digest f273-proto-t002c.diff
  True plan.md == payload (at C4)
  True live_review.md == 4862e71a bytes + ledger.md (at C4)
  True decisions.md == 4862e71a bytes + decisions.md (at C4)
  True authored f273-r4-plan.md == payload
  True authored f273-r4-ledger.md == payload
  True authored f273-r4-decisions.md == payload
  True authored f273-r4-block.md == payload
  True exactly four f273-r4-* copies: ['.agent/authored/f273-r4-block.md', '.agent/authored/f273-r4-decisions.md', '.agent/authored/f273-r4-ledger.md', '.agent/authored/f273-r4-plan.md']
  ALL True 15 checks
  ```
- **G2**: `git rev-parse b00a826f:tests b00a826f:apps b00a826f:packages`, EXIT 0:
  ```
  f952ccd3491b9516afbe71d2f0cd5e873ff538c5
  669c3a23f24a5dca64f2fc47dbd708c9084a1239
  33e5de700300b3644f0e979824eae0edcf526627
  ```
  All three equal the reviewer's dry-run subtrees.
- **G3** (primary checkout at `b00a826f`, serial, the block's 15 targets, full output in `.remedy-wt/f273-r4/wk_g3.txt`, 19 lines): `python3 -m pytest -q -p no:cacheprovider tests/orchestration/test_product_smoke.py ... tests/cli/test_golden_path.py`:
  ```
  1239 passed, 4 skipped in 182.58s (0:03:02)
  EXIT 0
  ```
  0 failed. `grep -c "R-0803:"` over the full output file printed `0`; `grep -c -i failed` printed `0`. `git status --porcelain` read empty afterwards. `apps/ui/node_modules` exists in the primary checkout, so `test_vitest_passes` ran there rather than skipping.
- **G4** (primary checkout): `python3 -m ruff check --output-format concise` over the 15 Python files C2 to C4 touch, EXIT 1:
  ```
  tests/ui_server/test_live_state.py:465:9: I001 [*] Import block is un-sorted or un-formatted
  tests/ui_server/test_live_state.py:466:16: F401 [*] `datetime` imported but unused
  tests/ui_server/test_live_state.py:500:9: I001 [*] Import block is un-sorted or un-formatted
  tests/ui_server/test_live_state.py:500:40: F401 [*] `apps.cli.commands.ui` imported but unused
  Found 4 errors.
  [*] 4 fixable with the `--fix` option.
  ```
  Exactly the four base findings. Control: the same command over `git show 4862e71a:tests/ui_server/test_live_state.py` saved as `.remedy-wt/f273-r4/wk_base_test_live_state.py` printed the same four codes at 470:9, 471:16, 505:9 and 505:40 (EXIT 1): five lines lower after C3, nothing else.
- **G5** (`python3 .remedy-wt/f273-r4/wk_g5.py`, one worktree at `b00a826f`, `python3 -B -m pytest -q -p no:cacheprovider` from its root, `__pycache__` purged before every run, each mutation's FROM byte-counted first and reverted by its saved bytes, `git status --porcelain` empty after every revert), EXIT 0:
  ```
  apps/ui/node_modules present before first run: False
  tests.ui_server.server_start resolves to: /home/decodeux/Repos/remedy/.remedy-wt/f273-r4-g5/tests/ui_server/server_start.py (inside worktree: True)
  packages.orchestration.pingpong_loop resolves to: /home/decodeux/Repos/remedy/.remedy-wt/f273-r4-g5/packages/orchestration/pingpong_loop.py (inside worktree: True)
  [vitest_skip] exit 0; summary: 1 skipped, 48 deselected in 0.14s
  [vitest_mut] FROM byte-count = 1; exit 1; summary: 1 failed, 48 deselected in 0.80s
      FAILED tests/orchestration/test_test_runner.py::TestVitestFrontendTestFoundation::test_vitest_passes
  [control] exit 0; summary: 430 passed in 35.93s
  (a) FROM byte-count = 1; exit 1; 1 failed, 76 passed
      FAILED tests/orchestration/test_product_smoke.py::test_the_default_port_is_owned_by_the_worker
  (b) FROM byte-count = 1; exit 1; 1 failed, 9 passed
      FAILED tests/ui_contracts/test_humanize_catalog.py::TestDerivation::test_vendored_python_under_node_modules_is_not_walked
  (c) FROM byte-count = 1; exit 1; 1 failed, 68 passed
      FAILED tests/ui_contracts/test_brain_stream_ring.py::TestTheFeedIsFedFromTheStream::test_the_card_prints_each_rows_seq
  (d) FROM byte-count = 1; exit 1; 1 failed, 25 passed
      FAILED tests/orchestration/test_job_stop_integration.py::TestStopDuringAProviderCall::test_a_stop_before_the_parse_retry_leaves_the_malformed_response_alone
  (e) FROM byte-count = 1; exit 1; 4 failed, 3 passed
      FAILED tests/ui_server/test_server_start.py::TestAHalfWrittenFileIsNotStartedYet::test_a_partial_read_is_retried_until_the_file_is_whole[empty]
      FAILED ...::test_a_partial_read_is_retried_until_the_file_is_whole[one-byte]
      FAILED ...::test_a_partial_read_is_retried_until_the_file_is_whole[half]
      FAILED ...::TestAHalfWrittenFileIsNotStartedYet::test_a_partial_read_is_not_info
  (f) FROM byte-count = 1; exit 1; 1 failed, 6 passed
      FAILED tests/ui_server/test_server_start.py::TestTheWaitLastsAsLongAsTheStart::test_a_dead_server_thread_fails_at_once_rather_than_at_a_budget
  (g) FROM byte-count = 1; exit 1; 125 failed, 61 passed
      failing ids in all seven files: test_live_state.py (14, e.g. TestUIServerIntegration::test_server_starts_and_writes_info),
      test_command_channel.py (79, TestCommandChannelDoor::*), test_server_concurrency.py (1, test_two_requests_are_in_flight_at_once),
      test_digest_route.py (7), test_decisions_endpoint.py (4), test_command_dispatch.py (12), test_diff_endpoint.py (8)
  (h) FROM byte-count = 1; exit 1; 1 failed, 54 passed
      FAILED tests/ui_contracts/test_decision_answer_wiring.py::TestTheInFlightHelpersTouchOnlyTheirOwnKey::test_the_add_helper_adds_the_key_it_was_handed
  results: {'vitest_skip': 0, 'vitest_mut': 1, 'control': 0, 'mut_a': 1, 'mut_b': 1, 'mut_c': 1, 'mut_d': 1, 'mut_e': 1, 'mut_f': 1, 'mut_g': 1, 'mut_h': 1}
  G5 PASS
  ```
  The control ran over the twelve test files the mutations name. Every mutation went red; none stayed green. Full per-run output is in `.remedy-wt/f273-r4/wk_g5_*.txt`; (g)'s full list of 125 ids is in `wk_g5_mut_g.txt`.
- **G6** runs after the push and is reported in the round report, because this commit precedes it.
- Full suite: not run (amend0917-throughput).

## Authored-text proofs

- Every edited `.agent/` file was built by `python3 .remedy-wt/f273-r4/wk_c1.py` from `git show 4862e71a:<path>` bytes and the payload bytes. Nothing was hand-edited. G1 re-proves every file and every `.agent/authored/f273-r4-*` copy against its payload.
- The code arrived only by `git apply` of the three reviewer-verified diffs, in the block's order. G2's subtree ids equal the reviewer's dry-run subtrees.

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C1 bookkeeping | done | `42268f04` |
| C2 R-0518, R-0569, R-0649, R-0664 | done | `43760c74` |
| C3 R-0691, R-0708, R-0734, R-0815 | done | `5206ece6` |
| C4 the six other server-start copies | done | `b00a826f` |
| C5 handoff + push | done | This commit, then the push |
| G1 to G5 | done | As above; G4's EXIT 1 is exactly the four base findings the block names |
| G6 | done | After the push; in the round report |

## Open findings

Measured by `.remedy-wt/f273-r4/wk_measure.py`, which loads `scripts/rotate_live_review.py` by path and calls `count_open_findings` (by distinct id) on the committed `.agent/live_review.md`:
- at `b00a826f` (C1 onwards; C2 to C4 do not touch it): **124 open**;
- at `4862e71a`: 127 open.

The fall of three is C1's `Done:` lines for R-0671, R-0689 and R-0690. The eight ids landed this round (R-0518, R-0569, R-0649, R-0664, R-0691, R-0708, R-0734, R-0815) are still open in the ledger, as are R-0499 and R-0662 (DECISION F273 D4 (9) and (10)). Highest registered id R-0985.

## Deviations & assumptions

- **Commit sequence:** as ordered: C1, C2, C3, C4, C5, then the push. No extra commit.
- **C3 alone does not import:** `5206ece6` makes `test_command_channel.py` and `test_live_state.py` import `tests.ui_server.server_start`, which the block's C4 diff creates, so at C3 by itself those two files fail at collection. This is the block's ordered split of the three diffs, applied unchanged; every gate ran at C4, where it resolves (G3, G5). A bisect landing on `5206ece6` would see it.
- **G4 exit code:** ruff exits 1 because the four base findings remain; the block orders exactly those four and nothing else, which is what it printed.
- **Payload copies:** "every payload above" was read as the four files the block lists under PAYLOADS, as in rounds 2 and 3. The three code diffs are listed under CODE and are not copied into `.agent/authored/`.
- **G5 purge:** `python3 -B` writes no `__pycache__` of its own, but the purge before (a) and (e) removed four directories each, written by subprocesses the preceding runs' tests spawn without `-B`; the purge ran before every run.
- **Scratch runner:** the worker's shell cwd was the reviewer's `.remedy-wt/f273-r4-dry` worktree. Nothing was run in it; every git command used `git -C` on the primary checkout and every script used an explicit `cwd`. The worker's scripts carry a `wk_` prefix so the reviewer's own files in `.remedy-wt/f273-r4/` were not overwritten.
- **Scratch:** gitignored, under `.remedy-wt/f273-r4/`: `wk_c1.py`, `wk_g1.py`, `wk_g5.py`, `wk_measure.py`, `wk_run.py`, `wk_check.py`, `wk_base_test_live_state.py`, `wk_g3.txt`, `wk_g5_*.txt`.

## Next

1. Phase 1 rule 1 (`.agent/STOP`), then the review of round 4.

Operator questions open: 5
