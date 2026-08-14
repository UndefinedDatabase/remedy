# Handoff — F057 Rate-limit-aware scheduler, Round 5 (R4 verdict, R-0370 fix, T003 seam inventory)

Branch: feature/f057-rate-limit-scheduler. Base 5de503c6 → HEAD C4 (below).
No PR exists for this branch; none was created. No `.agent/STOP` at any point.

## Per-commit changed files
| Commit | Item | Files | numstat |
|---|---|---|---|
| 94932714 | C0a | .agent/authored/f057-r5.md | 268 / 0 |
| ebd3863e | C0b | .agent/last_block.md | 177 / 249 |
| ecfd59c4 | C1 | .agent/live_review.md | 6 / 0 |
| a01e8a97 | C2 | tests/orchestration/test_rate_governor.py, .agent/live_review.md | 14 / 0, 2 / 0 |
| d7956d1d | C3 | .agent/f057_t003_seam_inventory.md | 261 / 0 |
| (this) | C4 | .agent/plan.md, .agent/context.md, .agent/handoff.md | handback |

## Item status
| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | deviated | the `Landed:` line cannot carry its own commit's SHA — see Deviations |
| C3 | done | |
| C4 | done | |

## Extracted slice sha256 (disk to disk, from the COMMITTED .agent/authored/f057-r5.md)
Source file sha256 `1e4e6b6acfc31fae30322b1b32d7e73d3c003a07893eaad444cbcdda6cad6561`.
| Slice | sha256 | bytes | target |
|---|---|---|---|
| GATE-R4 | 1505dda079c590ecd34aee3b32efd0d26f8b4b4debe22c2818cd95669b7968fe | 4011 | .agent/live_review.md |
| FINDING-369 | 9040708b147ef5f23dfbf40edd158aa03a628aaa4d76ac3eeb8c453c02dfabef | 1927 | .agent/live_review.md |
| FINDING-370 | 51c435d4af9fbd981c3c196603199d7afa0d5f6c0630550f5de790dda6da10a7 | 1463 | .agent/live_review.md |
| PLAN | 5f02d9d64eee81d76f61aad389d426c59f6ff16b22d89a642ba51ee1d5038c5c | 1899 | .agent/plan.md |
| CONTEXT | 1be4a3a322fe3fc07ccc8c2e54247ff8fb29fa95314fc592694876cb95f99c5a | 2290 | .agent/context.md |
Each was re-read after writing and asserted byte-equal to the extracted bytes.

## Gates, executed
1. `git status --porcelain` → empty (at C4).
2. `git worktree list` → 1 line (`/home/decodeux/Repos/remedy`).
3. `git branch --show-current` → feature/f057-rate-limit-scheduler.
4. `cmp .agent/authored/f057-r5.md .agent/last_block.md` → exit 0, no output. Shared sha256
   `1e4e6b6acfc31fae30322b1b32d7e73d3c003a07893eaad444cbcdda6cad6561`; block is 268 lines
   (≤ 400, checkpoint passed, C1-C4 performed).
5. live_review.md after C1, line-anchored vs whole-file substring:
   `^Gate: R4 — PASS` 1 / 1; `^- R-0369 — ` 1 / 1; `^- R-0370 — ` 1 / 1;
   `^## Steps` 1 / 5 — the four extra `## Steps` hits are inside R-0369's own prose,
   which is the difference R-0369's counter-measure exists to keep visible. The
   `- R-0361 ` line still hashes to
   `70a8c9fb1a6ddebd2a1592b467cf9cb7e18f43ad0449c245d110bc0f1f056a7b` (line plus its
   trailing newline).
6. `git show --numstat ecfd59c4 -- .agent/live_review.md` → `6  0`. 6 insertions, 0
   deletions: pure append.
7. `python3 -m pytest tests/orchestration/test_rate_governor.py -q` → exit 0,
   `59 passed in 0.12s`. The 58 present at 5de503c6 plus the C2 test; 0 failed.
8. `python3 -m ruff check packages/orchestration/rate_governor.py
   tests/orchestration/test_rate_governor.py` → `All checks passed!`, exit 0.
9. Canary `python3 -m pytest tests/cli/test_golden_path.py -q` → exit 0, `42 passed in 15.91s`.
10. Do-not-touch `git diff --stat 21c8148e..HEAD` over provider_timeouts.py,
    pingpong_loop.py, stream_evidence.py → EMPTY output. `git diff --name-only
    5de503c6..HEAD` contains no path under `packages/` or `apps/` at all.
11. `git diff --name-only 5de503c6..HEAD` → the eight bundle paths, no ninth:
    .agent/authored/f057-r5.md, .agent/context.md, .agent/f057_t003_seam_inventory.md,
    .agent/handoff.md, .agent/last_block.md, .agent/live_review.md, .agent/plan.md,
    tests/orchestration/test_rate_governor.py.
12. `wc -l < .agent/plan.md` → 35.
13. `^Landed: R-0370 —` → 1 line; `^Done: R-0370` → 0 lines.
14. RED-PROOF in worktree `.remedy-wt/r5_red` (detached at d7956d1d). Import path printed
    FIRST: `IMPORTED MODULE __file__:
    /home/decodeux/Repos/remedy/.remedy-wt/r5_red/packages/orchestration/rate_governor.py`,
    and `inspect.getsource(ProviderRateGovernor.observe)` confirmed the `max(...)` guard
    gone inside that copy. With `self._cooldown_until[provider] = now + duration`:
    `1 failed, 58 passed in 0.12s`; the single failing id is
    `tests/orchestration/test_rate_governor.py::test_a_later_signal_never_shortens_a_cooldown_already_running`
    with `AssertionError: assert 1.0 == 30.0`. That is the C2 test and only the C2 test,
    so the new test discriminates the invariant. Worktree removed and pruned; gate 2 is
    the proof.
15. Inventory citations: 66 unique `path:line` (71 occurrences) extracted mechanically
    from `.agent/f057_t003_seam_inventory.md` and re-read out of `git show 5de503c6:<path>`;
    0 failed to resolve, and each printed line was compared against the claim it supports.
    Eight were WIDENED to ranges before C3 because the quoted sentence spanned two lines
    (T2_F057.md 10-11/14-16/31-32/33-34/65-66, failure_postmortem.py 228-229,
    pingpong_job.py 1970-1975, pingpong_loop.py 4389-4393) — corrected before the commit,
    not declared after it. Regression scope reported in the inventory: the five files
    referencing `_call_with_retry` → `315 passed in 39.25s`, exit 0, the exact sum of
    their collect-only counts (135+62+58+39+21).

## Deviations, declared
- This handoff is 112 lines. The cause is mandated content: the per-commit table, the
  item-status table, the five-row slice-sha256 table and the real output of all 15 gates
  including gate 5's dual counts, gate 14's red-proof and gate 15's citation audit
  (DECISION D15). No section was dropped.
- C2 is marked `deviated`. The block ordered the `Landed:` line to carry "your real
  commit SHA" AND to live in the same commit as the test. A commit's SHA is a hash over
  the tree that contains that line, so a self-referential SHA is not reachable by any
  correct application of the bundle — the R-0367/R-0368 class. Nothing was fabricated and
  no number was edited toward: the line names what changed and identifies its commit as
  "R5's C2, the same commit as this line, whose SHA the handback reports", and the real
  SHA is `a01e8a9712aead26eb88888db352d0bb72492cb9`. Gate 13's shape check passes
  unchanged.
- Composite shell forms (`for`, `echo $?`), `cp` and `grep -P` are denied session-wide by
  the sandbox. Every gate ran as a single command or through `python3` for byte work and
  exit-code capture; no slice was retyped and no check was skipped.

## State
Open findings: EIGHT — R-0361, R-0362, R-0363, R-0364, R-0367, R-0368, R-0369, R-0370.
Next free id: R-0371. R-0370 stays OPEN carrying its `Landed:` line; only
reviewer-authored text may close it.
Next expected action, in order: Phase 0 of docs/agents/self_drive_protocol.md (the
deterministic state probe); then Phase 1 rule 1 — re-read `.agent/STOP` from disk —
BEFORE rule 2, the Open PR Gate; then T003, the `_call_with_retry` seam, starting from
`.agent/f057_t003_seam_inventory.md` as its evidence. This was the session's last round
under its declared round cap.
