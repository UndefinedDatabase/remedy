# Handoff — F057 Rate-limit-aware scheduler, R6 (T003 part 1: the seam)

## Range
Review of 33fab24e..HEAD (HEAD = C5, the commit that writes this file).

## Commits
### 89ae4311 chore(f057): save the R6 step block verbatim (C0a)
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f057-r6.md | +385/-0 | the block verbatim, 385 lines (cap 400) |
### a16f310f chore(f057): point last_block at the R6 block (C0b)
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +356/-239 | identical bytes; `cmp` exit 0 |
### 098594a1 docs(f057): record the R5 verdict, register R-0371, resolve R-0370 (C1)
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +6/-0 | GATE-R5, FINDING-371, DONE-370 appended |
### 281caf58 docs(f057): record DECISIONS D3, D4 and D5 for the T003 seam (C2)
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | +65/-0 | D3 pacing, D4 no deadline_s, D5 empty provider |
### 4493d56b feat(f057): pace provider calls through the rate governor (C3)
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/pingpong_loop.py | +76/-0 | import, `rate_limit_waits`, `_record_rate_limit_wait`, first-call + retry pacing, one governor per run |
### 28d1206c test(f057): pin the five seam properties of the wiring (C4)
| Path | +/- | Reason |
|---|---|---|
| tests/orchestration/test_provider_retry.py | +216/-0 | 5 seam tests, injected FakeClock |
### HEAD (C5) — grouped, self-referential (R-0149)
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | rewrite | PLAN slice applied whole, 35 lines |
| .agent/context.md | 2 pairs | CONTEXT1 + CONTEXT2 rewritten |
| .agent/handoff.md | rewrite | this file |

## Item status
| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | deviated | block said "BOTH" call sites; there are THREE (2849/3061/3117). Wired the two it named; parse-retry site left unpaced — see Deviations |
| C4 | done | |
| C5 | done | |

## Authored-text proofs
`cmp .agent/authored/f057-r6.md .agent/last_block.md` -> exit 0; shared sha256
`c5dfac96f25f5a995d2ef118631d17a6123cdbb59bad5702a4fe26b0e4d7f6be`, 385 lines.
Slices extracted from the COMMITTED authored file, never retyped; each FROM
occurred exactly once and each TO zero times before replacement.
| Slice | sha256 of body bytes |
|---|---|
| GATE-R5 | 88b5ef6e5809834a57493568c2fc2def4bc4be09854bb96ceddec482506eff33 |
| FINDING-371 | 8c1880a08298de2df5f8a43dd49b0eaa301ebfd607b567b5bde3571b2dc9ba4a |
| DONE-370 | 95cafee5692e338c22bf5f5fa3c280dd624263dbc6f875f4063c539e7ffcdfb5 |
| DECISIONS | 1959e47d1af36af9167a4aee342de88fa2f9bbe92a725bf3ecf1ac2edb6c6eeb |
| PLAN | 83db269c4e16f5337c5fb952a2481aed7ea610ea6cb3744958128b9bd0511041 |
| CONTEXT1-FROM | e7260683975cb8c0dd358df288b0c27cf6fd570fe335c1f7732597807ff33eae |
| CONTEXT1-TO | d7fdc5980ee60a66d02f1d9a7927aebf805a14ade95eaccb031a29efe27b59e6 |
| CONTEXT2-FROM | 77c1ae83d74c96a3dd6d4dca56c7f7d3ee04b16d69cc085f3190eff72aede145 |
| CONTEXT2-TO | b8abffc4a051180ef9a0ea878fce806be21a4c990e2f44b2a9cde3c492ba6e22 |

## Verification — all 16 gates, real output
1. `git status --porcelain` -> empty (measured at C4; C5 commits its own files).
2. `git worktree list` -> 1 line, `/home/decodeux/Repos/remedy 28d1206c [feature/f057-rate-limit-scheduler]`.
3. `git branch --show-current` -> `feature/f057-rate-limit-scheduler`.
4. `cmp` -> exit 0; sha256 and 385 lines as above.
5. line-anchored: `^Gate: R5 — PASS` 1, `^- R-0371 — ` 1, `^Done: R-0370 — ` 1,
   `^Landed: R-0370 —` 1, `^## Steps` 1. Substring `## Steps` = 6, CHANGED from 5:
   the GATE-R5 slice itself contains the literal "`^## Steps` 1" in its own counts.
6. `git show --numstat 098594a1 -- .agent/live_review.md` -> `6	0`; deletions 0.
7. `pytest tests/orchestration/test_rate_governor.py -q` -> `59 passed`, exit 0 — unchanged.
8. `pytest tests/orchestration/test_provider_retry.py -q` -> `26 passed`, exit 0 (21 + 5).
9. the four regression files together -> `294 passed in 39.15s`, exit 0.
10. `ruff check pingpong_loop.py rate_governor.py test_provider_retry.py` -> `All checks passed!`, exit 0.
11. canary `pytest tests/cli/test_golden_path.py -q` -> `42 passed`, exit 0.
12. the three .agent contract readers -> `142 passed`, exit 0.
13. `wc -l < .agent/plan.md` -> 35.
14. `git diff --name-only 33fab24e..HEAD` at C4 -> .agent/authored/f057-r6.md,
    .agent/decisions.md, .agent/last_block.md, .agent/live_review.md,
    packages/orchestration/pingpong_loop.py, tests/orchestration/test_provider_retry.py;
    C5 adds .agent/plan.md, .agent/context.md, .agent/handoff.md. Nothing beyond the nine.
15. `git diff --stat 21c8148e..HEAD -- provider_timeouts.py stream_evidence.py` -> EMPTY.
16. RED-PROOF in `.remedy-wt/r6_red`, removed and pruned (gate 2 is the proof).
    Import path printed FIRST, from a pytest run inside it: `MODULE __file__:
    /home/decodeux/Repos/remedy/.remedy-wt/r6_red/packages/orchestration/pingpong_loop.py`.
    (A bare `python3` there imported the PRIMARY checkout via the editable install;
    redone under pytest, whose rootdir pythonpath wins. R-0337 nearly bit.)
    (i) delete retry-path `acquire(...)` + `return out` guard -> `2 failed, 25 passed`:
    `test_rate_limited_retry_waits_and_records_one_event` at `assert clock.sleeps`
    -> `assert []`; `test_stop_during_the_wait_ends_the_call_without_counting_a_retry`
    at `assert calls[0] == 1` -> `assert 3 == 1`.
    (ii) delete retry-path `observe(...)` -> `2 failed, 25 passed`, same two ids and
    same two assertions: with no cooldown announced, nothing waits.
    Extra probes (the block asks whether all five tests discriminate):
    (iii) drop `and provider` from both guards -> 1 failed,
    `test_empty_provider_skips_the_governor_entirely`, `assert result.rate_limit_waits == []`
    vs two events under provider `''`.
    (iv) delete the first-call pacing -> 1 failed,
    `test_first_call_is_paced_by_a_cooldown_already_running`, `assert 0 == 1`.
    (v) drop `rate_governor is not None` from both guards -> 1 failed,
    `test_no_governor_leaves_retry_behaviour_identical`,
    `AttributeError: 'NoneType' object has no attribute 'acquire'`.
    All five C4 tests discriminate their stated property.

## External actions
`git push` after each of C0a, C0b, C1, C2, C3, C4, C5 — all fast-forward, never forced.
`git worktree add .remedy-wt/r6_red HEAD --detach` -> created; `git worktree remove
--force` + `git worktree prune` -> gone. No PR created (the block forbids one).

## Deviations & assumptions
- Handoff length, DECISION D15 stated cause: this file exceeds the 60-line cap and
  the 100-line >5-commit allowance. Cause is mandated content only — per-commit
  tables for SEVEN commits, the 9-row slice-sha table, the item-status table and
  the raw output of 16 gates including five red-proof probes. No section dropped.
- C3, block-defect candidate: the block orders the governor passed to "BOTH
  `_call_with_retry` call sites — the builder site and the reviewer site". There are
  THREE in `run_pingpong`: 2849 builder, 3061 reviewer attempt, 3117 reviewer PARSE
  RETRY. The seam inventory the block cites names all three itself (its line 129).
  Applied literally: the two named sites are wired; a reviewer parse retry is
  currently UNPACED. Wiring it would be a change the block did not name, against
  "Nothing else in this file changes". Reviewer to rule: R7 wiring, or a documented
  deliberate absence.
- No other drift: every symbol and anchor the block cites was re-grepped on disk
  and matched before editing.

## Open findings
9: R-0361, R-0362, R-0363, R-0364, R-0367, R-0368, R-0369, R-0371, plus the C3
call-site defect candidate above (unnumbered; the reviewer owns ids).
Resolved: R-0365, R-0366, R-0370.

## Next
Reviewer re-runs all 16 gates at HEAD, rules on the third call site, and issues the
R6 verdict; then R7 = T003 part 2 (report surfaces + limit-emitting fixture).
