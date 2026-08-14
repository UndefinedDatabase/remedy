# Handoff — F057 Rate-limit-aware scheduler, round R7

Review of 3ab9d964..HEAD. Branch feature/f057-rate-limit-scheduler. No PR this round.

## Item status
| Item | Status | Reason |
|------|--------|--------|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | deviated | test 3 builds the reject WITH a rate-limit error, not the errorless shape the existing tests use — see Deviations |
| C4 | done | |

## Commits
### 6d70b2ef chore(f057): save the R7 block verbatim
| Path | +/- | Reason |
|------|-----|--------|
| .agent/authored/f057-r7.md | +229/-0 | the R7 block, verbatim |

### 6b4c3f56 chore(f057): point last_block at the R7 block
| Path | +/- | Reason |
|------|-----|--------|
| .agent/last_block.md | +175/-331 | full rewrite of one .agent state file (F104 D1 exempt) |

### 475f4ab8 docs(f057): record the R6 verdict and register R-0372 and R-0373
| Path | +/- | Reason |
|------|-----|--------|
| .agent/live_review.md | +6/-0 | GATE-R6, FINDING-372, FINDING-373 appended; no line edited or removed |

### 1f74beb5 fix(f057): pace the reviewer parse-retry provider call too
| Path | +/- | Reason |
|------|-----|--------|
| packages/orchestration/pingpong_loop.py | +1/-0 | R-0372: `rate_governor=_rate_governor` at the third call site |

### c0984caa fix(f057): retry a rate limit at the governor seam so it is reachable
| Path | +/- | Reason |
|------|-----|--------|
| packages/orchestration/pingpong_loop.py | +17/-2 | R-0373: import `is_rate_limit_error`; guarded predicate; retry decision; docstring |
| tests/orchestration/test_provider_retry.py | +93/-2 | 3 unit tests, `BARE_RATE_LIMIT_ERROR`; a now-false comment corrected |

### C4 handoff (this commit, grouped — a handoff cannot table itself)
| Path | +/- | Reason |
|------|-----|--------|
| .agent/plan.md | rewrite | PLAN slice applied verbatim |
| .agent/handoff.md | rewrite | this file |

## External actions
`git push -u origin feature/f057-rate-limit-scheduler` after each of C0a, C0b, C1, C2, C3, C4 — exit 0 each.
`git worktree add .remedy-wt/r7-redproof HEAD --detach` -> created at c0984caa; `git worktree remove --force` + `git worktree prune` -> `git worktree list` is one line. No gh command, no PR.

## Authored-text proofs
| Slice | sha256 | Disk-to-disk |
|-------|--------|--------------|
| block file (whole) | fc3c50e915797c98dba976772dffaeb64a1ac58fab42021221ed7205cf34a02d | `cmp` authored vs last_block exit 0, 229 lines |
| GATE-R6 | cd9129042ac1029c33068ea8534d08095a92e63f65170d5764727fde39579031 | identical to live_review.md line 63 |
| FINDING-372 | 49ff189f82e744bc3debbe8bbf55a74606904e3f49c33f3023cc69216608816d | identical to live_review.md line 65 |
| FINDING-373 | ffdd80f4be3b5cbcc56373b6b7f1f4e4ffb82aac168d2e9b21a705b2880fc4a5 | identical to live_review.md line 67 |
| PLAN | 1a4e43ef16ee22c0bdbeff159559325595cd440686f6a086629c3b0f53db4e1d | identical to .agent/plan.md in full |
Each slice was extracted from the COMMITTED `.agent/authored/f057-r7.md` (via `git show HEAD:`), never retyped.

## Verification — all 17 gates, real output
1. `git status --porcelain` -> empty (exit 0).
2. `git worktree list` -> 1 line: `/home/decodeux/Repos/remedy  c0984caa [feature/f057-rate-limit-scheduler]`.
3. `git branch --show-current` -> `feature/f057-rate-limit-scheduler`.
4. `cmp .agent/authored/f057-r7.md .agent/last_block.md` -> exit 0. sha256 `fc3c50e9…4a02d`, `wc -l` 229 (under the 400 cap).
5. live_review.md line-anchored: `^Gate: R6 — PASS` 1, `^- R-0372 — ` 1, `^- R-0373 — ` 1, `^## Steps` 1. Whole-file SUBSTRING `## Steps` = 8, CHANGED from 6. Cause: the GATE-R6 slice itself contains the literal twice (once reporting its own anchored count, once reporting the R5-round substring move). Reported, not hidden.
6. `git show --numstat 475f4ab8 -- .agent/live_review.md` -> `6  0`. Deletion column 0 as ordered.
7. `pytest tests/orchestration/test_provider_retry.py -q` -> `29 passed in 0.27s`, 0 failed (was 26; C3 adds 3).
8. `pytest tests/orchestration/test_rate_governor.py -q` -> `59 passed in 0.09s`, unchanged from baseline. No finding candidate.
9. Four regression files together -> `294 passed in 39.07s`, exit 0. Exactly the baseline: the pre-F057 path did not move.
10. `python3 -m ruff check packages/orchestration/pingpong_loop.py tests/orchestration/test_provider_retry.py` -> `All checks passed!`, exit 0.
11. Canary `pytest tests/cli/test_golden_path.py -q` -> `42 passed in 15.85s`, 0 failed.
12. dashboard_contract + resource_safety + test_runner -> `142 passed in 17.11s`, exit 0.
13. `wc -l < .agent/plan.md` -> 36 (<50).
14. `grep -n "_call_with_retry(" packages/orchestration/pingpong_loop.py` -> `2172:def`, `2938:builder_out`, `3151:reviewer_out`, `3208:retry_out`. All THREE call sites pass `rate_governor=_rate_governor` (checked by parsing each call's full paren block, not by eyeballing).
15. `git diff --name-only 3ab9d964..HEAD` -> `.agent/authored/f057-r7.md`, `.agent/last_block.md`, `.agent/live_review.md`, `packages/orchestration/pingpong_loop.py`, `tests/orchestration/test_provider_retry.py` (+ `.agent/plan.md`, `.agent/handoff.md` in C4). No path outside the block's list.
16. `git diff --stat 21c8148e..HEAD -- provider_timeouts.py stream_evidence.py` -> EMPTY.
17. RED-PROOF in `.remedy-wt/r7-redproof`, never in the primary checkout. Import path proved UNDER PYTEST first: a throwaway test printed `IMPORTED_FROM: /home/decodeux/Repos/remedy/.remedy-wt/r7-redproof/packages/orchestration/pingpong_loop.py` and asserted the worktree path — `1 passed`. Worktree baseline `29 passed`. Probes:
    (i) decision reverted to plain `should_retry` -> `1 failed, 28 passed`; `test_bare_rate_limit_is_retried_when_a_governor_is_active`, `AssertionError: assert '' == 'ok'`.
    (ii) guard `rate_governor is not None and provider` dropped -> `1 failed, 28 passed`; `test_bare_rate_limit_without_a_governor_is_still_not_retried`, `assert 3 == 1` on the call count.
    (iii) `rate_governor=` removed from the C2 parse-retry site -> KILLS NOTHING. `test_provider_retry.py` + `test_rate_governor.py` -> `88 passed`; the four regression files + the canary -> `336 passed`. 424 tests, all green with C2 reverted. Stated plainly: the C2 wiring change is UNTESTED — a real gap, carried below.
    Extra probe (not ordered): explicit `is_reject or` dropped -> `1 failed, 28 passed`; `test_review_reject_is_never_retried_even_with_a_governor`, `assert 3 == 1`. This is what justifies the C3 deviation.

## Deviations & assumptions
- Length: this handoff is 96 lines, over the 60-line cap — DECISION D15 stated cause: the mandated per-commit changed-files tables (6), the item-status table, the slice-sha256 table and the REAL output of 17 gates including four RED-PROOF probes. No section dropped, no prose padding.
- C3 test 3 shape: the block said "build the reject the way the existing tests in this file build one" (errorless `ReviewerOutput(verdict="needs_repair")`). That shape returns at `_call_with_retry`'s `if not out.error` BEFORE the reject exclusion is reached, so it would pass with or without the exclusion — a vacuous test. Built instead with `error=BARE_RATE_LIMIT_ERROR`, the only shape that reaches the guard. The extra probe above proves the test is load-bearing. Declared before review.
- C3 also edits `_call_with_retry`'s docstring line "Only retries on timeout or nonzero exit", which C3 makes false; leaving it would be the R-0365 defect class. Inside the ordered function, no other symbol touched.
- Commit Gate ordering: C2 and C3 landed while `.agent/plan.md` still described T003 part 1 and said "nothing is contradicted today". The block assigns the plan rewrite to C4; followed the block and note the two-commit window here rather than reorder it.
- Open finding candidate (worker-raised, for the reviewer to accept or reject): the C2 parse-retry wiring has no test — see gate 17 (iii).

## Open findings
10 open: R-0361, R-0362, R-0363, R-0364, R-0367, R-0368, R-0369, R-0371, R-0372, R-0373. R-0372 and R-0373 are FIXED on disk this round and stay OPEN until a reviewer verdict closes them; only reviewer-authored text may close them. Next free id: R-0374.

## Next
This session is at its declared round cap. The NEXT SESSION's first action is Phase 1 rule 1 of docs/agents/self_drive_protocol.md — re-read `.agent/STOP` from disk — BEFORE rule 2, the Open PR Gate. Then: reviewer verdict on R7, then T003 part 2 (the report surfaces and the bare-rate-limit fixture end-to-end, per .agent/plan.md).
