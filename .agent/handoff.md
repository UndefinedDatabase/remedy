# Handoff — F111 Diff-only repair, Round 17 (T003, apply half)

Branch: feature/f111-diff-only-repair, base c0ed5dd1 (R16 PASS), no PR by design.
Commits: 7506d5cc (C1), 4c6a4fbe (C2), bda7e81e (C3), 71319adc (C4),
19797836 (C5), this commit (C6).

## Item status
| Item | Status | Reason |
|------|--------|--------|
| C1 authored block | done | 366 lines saved verbatim |
| C2 last_block mirror | done | byte-identical to C1 |
| C3 live_review TEXT-A | done | R16 verdict + DECISIONS D8, D9 appended |
| C4 diff channel | done | 4 edits; module-level imports, NO cycle |
| C5 three loop tests | done | see Deviations for the byte-comparison reading |
| C6 plan + handoff | done | plan.md is TEXT-B verbatim, 44 lines |

## Changed files
| Path | Commit | + / - |
|------|--------|-------|
| .agent/authored/f111-r17-1.md | 7506d5cc | 366 / 0 |
| .agent/last_block.md | 4c6a4fbe | 305 / 255 |
| .agent/live_review.md | bda7e81e | 71 / 0 |
| packages/orchestration/builder_bridge.py | 71319adc | 95 / 15 |
| tests/orchestration/test_builder_repair_loop.py | 19797836 | 164 / 0 |
| .agent/plan.md, .agent/handoff.md | C6 | this commit |

## Gates (all commands run for real)
a. TRANSPORT: `cmp` exit 0, both digests
   a21506ddee38218bba4c6fb0f051c6b175d1eeaadffe8c476af3096598a07332,
   20623 bytes, 366 lines (< 400), zero trailing-whitespace lines.
b. live_review: `^Done:` 11; `^- R-0` 42; `^### R16 — PASS` 1; `^Landed:` 0.
c. builder_bridge.py: `diff_repair_fell_back` 2, `diff_repair_applied` 1,
   `diff_response` 10.
d. VALUE PROBE, diff lands: mode = diff, applied = True, files_modified = 1,
   loop.success = True. calc.py after the loop:
   '# MARGIN_ANCHOR_TOP: no hunk in these tests names this line\ndef add(a, b):
   \n    return a + b\n\n\ndef unchanged_helper():\n    return 1\n' — the
   untouched neighbours prove a hunk landed, not a whole-file rewrite.
e. VALUE PROBE, conflict: mode = full_fallback, fallback_reason =
   'apply_failed:calc.py: diff hunks did not apply cleanly', files_modified = 0,
   rollback_incomplete = False, calc.py bytes unchanged across the attempt =
   True. The reason is `apply_failed:`, so the diff reached the applicator and
   was rejected there — the discard is not a cheap validation-stage skip.
f. `pytest tests/orchestration/test_builder_repair_loop.py -q` -> 12 passed
   (was 9).
g. three diff-repair files -> 71 passed, unmoved.
h. IMPORT FALLOUT, nine files -> 137 passed, 1 skipped. No drop.
i. CANARY `tests/cli/test_golden_path.py -q` -> 42 passed.
j. MUTATION PROBE in a disposable worktree (removed; `git worktree list` shows
   the primary checkout only): making the rejected diff set
   `result.apply_success = True` without returning gives 1 failed, 11 passed —
   `test_a_conflicting_diff_is_discarded_whole_and_the_round_falls_back` fails
   at the missing `repair_round_fell_back_to_full_file` event. No OTHER suite
   catches it (test_diff_repair_apply / test_builder_bridge / test_stop_reasons
   / test_repair_loop_hardened: 36 passed), so the conflict path is pinned by
   the new test alone.
k. `git status --porcelain` empty at every commit; `git diff --name-only
   c0ed5dd1..HEAD` = exactly the seven scoped paths; per-commit insertions
   366 / 305 / 71 / 95 / 164 for C1-C5, each under 500;
   `git rev-list --left-right --count origin/...HEAD` -> 0 and 0 after the
   final push.

## Deviations, declared
- 85 lines, over the 60-line base cap and inside the ≤100 allowance: the
  mandated six-row item-status table, the six-row changed-files table and the
  eleven ordered gate results a-k are what exceed it. No section dropped.
- C5, "read calc.py before the loop and compare bytes": cycle 1 must apply a
  patch for a diff-mode repair context to exist at all, so the bytes taken
  BEFORE the loop are not the bytes the discarded attempt started from. The
  test records both: `pre_loop_bytes` is asserted equal to what cycle 1 found,
  and the acceptance line compares what cycle 2 found against what cycle 3
  found — the true pre- and post-attempt bytes. Reading it literally would
  have made the assertion measure cycle 1's legitimate write.
- No import cycle appeared, so all three new symbols are module-level imports
  beside the R16 `diff_repair` import, as the block preferred.

Open findings: 31 (42 registered minus 11 resolved). None is High. Next free
finding ID: R-0318. No finding was resolved this round.

Next expected action: reviewer verdict on R17, then R18 — the measurement
(payload character counts per repair round plus the fixture comparison test,
DECISION F111 D9), which is the feature's DONE line.

Fortschritt: ~86 % (T001 ✅ · T002 ✅ · T003 Prompt-Hälfte ✅ · T003
Apply-Hälfte in dieser Runde · Messung offen) — Schätzung
