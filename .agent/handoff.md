# Handoff — F057 Rate-limit-aware scheduler, Round 4 (T002, the governor)

Branch: feature/f057-rate-limit-scheduler. Base dae401e1 → HEAD C5 (below).
No PR exists for this branch; none was created. No `.agent/STOP` at any point.

## Per-commit changed files
| Commit | Item | Files | numstat |
|---|---|---|---|
| 1fc1998b | C0a | .agent/authored/f057-r4.md | 340 / 0 |
| 0fe54d6e | C0b | .agent/last_block.md | 281 / 141 |
| 684a6304 | C1 | .agent/live_review.md | 4 / 0 |
| afc22df9 | C2 | .agent/decisions.md | 32 / 0 |
| 48310766 | C3 | packages/orchestration/rate_governor.py | 228 / 11 |
| 5dc31ecc | C4 | tests/orchestration/test_rate_governor.py | 247 / 7 |
| (this) | C5 | .agent/plan.md, .agent/context.md, .agent/handoff.md | handback |

## Item status
| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |
| C5 | done | |

## Extracted slice sha256 (disk to disk, from committed .agent/authored/f057-r4.md)
Source file sha256 `ee03a6e0647678d584e778653554ca68577a4c1ee5dd27d5c78c2c4bc48c6254`.
| Slice | sha256 | bytes | target |
|---|---|---|---|
| GATE-R3 | a7d7d2e27c93148f35f852bc38c040022abb9ea921d6ec73046e88f0cec3aa9e | 2439 | .agent/live_review.md |
| FINDING-368 | 727df6ce8c830290e66ae6fa76769e6f66a39e40776962bbab06d757f85c9397 | 1639 | .agent/live_review.md |
| DECISION-D2 | b3b8d54e37733dcfd527eb613a4f948dcb3ffb9a6fac1dda12ddce874124d7e8 | 1995 | .agent/decisions.md |
| PLAN | db795289b03820e0b80eee11cc45fa0934c4faa900c3981be9cf7059df9b33c0 | 1567 | .agent/plan.md |
| CONTEXT | 1c54b06bb2f968b018f666a6c09c19ef5af62d7dfcdfcc5ed317258f7e8bc2d6 | 2001 | .agent/context.md |
Each was re-read after writing and asserted byte-equal to the extracted bytes.

## Gates, executed
1. `git status --porcelain` → empty (at C5).
2. `git worktree list` → 1 line (`/home/decodeux/Repos/remedy`).
3. `git branch --show-current` → feature/f057-rate-limit-scheduler.
4. `cmp .agent/authored/f057-r4.md .agent/last_block.md` → exit 0. Shared sha256
   `ee03a6e0647678d584e778653554ca68577a4c1ee5dd27d5c78c2c4bc48c6254`; block is
   340 lines (≤ 400, checkpoint passed, C1-C5 performed).
5. live_review.md after C1: `Gate: R3 — PASS` 1x, `- R-0368 — ` 1x, `## Steps` 1x;
   the `- R-0361 ` line hashes to
   `70a8c9fb1a6ddebd2a1592b467cf9cb7e18f43ad0449c245d110bc0f1f056a7b` (line plus its
   trailing newline, the convention the R2/R3 entries used).
6. `git show --numstat 684a6304 -- .agent/live_review.md` → `4  0`. 4 insertions, 0
   deletions: pure append.
7. `.agent/decisions.md`: `## DECISION F057 D2 (2026-08-14)` 1x;
   `git show --numstat afc22df9 -- .agent/decisions.md` → `32  0`, 0 deletions.
8. `python3 -m pytest tests/orchestration/test_rate_governor.py -q` → exit 0,
   `58 passed in 0.12s`. 46 at dae401e1 + 12 new; 0 failed.
9. `python3 -m ruff check packages/orchestration/rate_governor.py
   tests/orchestration/test_rate_governor.py` → `All checks passed!`, exit 0.
10. Canary `python3 -m pytest tests/cli/test_golden_path.py -q` → exit 0,
    `42 passed in 15.82s`.
11. Do-not-touch `git diff --stat 21c8148e..HEAD` over provider_timeouts.py,
    pingpong_loop.py, stream_evidence.py → EMPTY output.
12. `git diff --name-only dae401e1..HEAD` → the nine bundle paths, no tenth.
13. `wc -l < .agent/plan.md` → 31.
14. `grep -c "time.sleep" tests/orchestration/test_rate_governor.py` → 0.
15. RED-PROOF in worktree `.remedy-wt/redproof` (detached at 5dc31ecc), witness test
    printed `IMPORTED MODULE __file__:
    /home/decodeux/Repos/remedy/.remedy-wt/redproof/packages/orchestration/rate_governor.py`
    FIRST in both runs, so the mutated copy was the one under test.
    (a) stop probe deleted from acquire()'s per-slice loop → `1 failed, 58 passed`;
    failing id `tests/orchestration/test_rate_governor.py::
    test_stop_beats_wait_when_the_stop_arrives_mid_wait` (`'granted' == 'stopped'`).
    (b) cooldown cap replaced by the uncapped product → `1 failed, 58 passed`;
    failing id `tests/orchestration/test_rate_governor.py::
    test_observe_without_a_hint_escalates_and_never_passes_the_cap` (`64.0 == 60.0`).
    Worktree removed and pruned; gate 2 above is the proof.

## Deviations, declared
- This handoff is 90 lines. The cause is mandated content: the per-commit table, the
  item-status table, the five-row slice-sha256 table and the real output of all 15
  gates including the two red-proof runs (DECISION D15). No section was dropped.
- `cmp` and several shell forms are denied session-wide by the sandbox in composite
  commands; `cmp` run alone is permitted and was executed for gate 4. Byte-copy for
  C0b used a Python read/write of the COMMITTED authored file, then `cmp`; no slice
  was retyped.

## State
Open findings: SIX — R-0361, R-0362, R-0363, R-0364, R-0367, R-0368. Next id R-0369.
Next expected action: reviewer re-runs every gate above against dae401e1..HEAD and
issues the R4 verdict. Phase 1 rule 1 first — re-read `.agent/STOP` from disk — then
rule 2, the Open PR Gate. Then T003, the `_call_with_retry` seam.
