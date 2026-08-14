# Handback — F057 Rate-limit-aware scheduler · Round 1 (T001)

## Range
21c8148e..HEAD, 6 commits, branch feature/f057-rate-limit-scheduler. Every commit
pushed. No PR created, no merge, no `main` commit, no force-push.

## Commits
| SHA | Subject | Item |
| 841a2f10 | chore(f057): save the R1 block verbatim | C0a |
| 122b193f | chore(f057): point last_block at the R1 block | C0b |
| a816e5aa | docs(f057): reset the review record and carry R-0361 forward | C1 |
| 842b4ed3 | docs(f057): claim F057 and reset the round state | C2 |
| 07de4d7d | feat(f057): normalize provider rate-limit signals | C3a |
| 449eabfe | test(f057): cover the rate-limit signal inventory | C3b |
| (this)   | chore(f057): handback R1 | C4 |

## Changed files (21c8148e..449eabfe)
| Path | +/- | Reason |
| .agent/authored/f057-r1.md | +404 | C0a, the R1 block verbatim |
| .agent/last_block.md | rewrite | C0b, `cmp` against the authored file exit 0 |
| .agent/live_review.md | rewrite | C1, reset + R-0362 + R-0361 carried |
| .agent/decisions.md | +46/-0 | C1, DECISION F057 D1 appended only |
| docs/roadmap/STATUS.md | +1/-1 | C2, the single claim line |
| .agent/plan.md | rewrite | C2 |
| .agent/context.md | rewrite | C2 |
| packages/orchestration/rate_governor.py | +294 | C3a, T001 normalization |
| tests/orchestration/test_rate_governor.py | +339 | C3b, 46 tests |

## Item status
| Item | Status | Reason |
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | deviated | split into C3a+C3b: 633 insertions > the AGENTS.md 500 cap |
| C4 | done | |

## Round gates — real output
1 `git status --porcelain` → empty, exit 0 · 2 `git worktree list` → 1 line, exit 0 ·
3 branch → `feature/f057-rate-limit-scheduler` · 4 claimed STATUS line → 1 (via
`grep -n -x`; `grep -c` with a `$` anchor is denied by this session's sandbox, and
a Python re-implementation of the exact regex also returns 1) · 5 `- [ ] F057` → 0 ·
6 `## Steps` → 1 · 7 R-0361 sha256 →
`70a8c9fb1a6ddebd2a1592b467cf9cb7e18f43ad0449c245d110bc0f1f056a7b`, matches, and the
line is 1797 bytes · 8 R-0362 → 1 · 9 DECISION F057 D1 → 1 · 10 `wc -l < plan.md` → 34 ·
11 test_rate_governor.py → 46 passed, exit 0 · 12 tests/docs/ → 295 passed, exit 0 ·
13 dashboard+resource_safety+test_runner → 142 passed, exit 0 · 14 see Deviations ·
15 canary test_golden_path.py → 42 passed, exit 0 · 16 `cmp` authored/last_block → exit 0 ·
17 red-proof below. Also: `grep -rn rate_governor packages/ apps/` outside the module
itself → EMPTY; `git diff --stat 21c8148e..HEAD` for provider_timeouts.py,
pingpong_loop.py, stream_evidence.py → EMPTY; `time.sleep` in the new test → 0.

## Red-proof probe — worktree only, both mutations
Import path proved first: `MODULE
/home/decodeux/Repos/remedy/.remedy-wt/f057_r1_red/packages/orchestration/rate_governor.py`
— inside the worktree, so the probe tests the mutated code.
- Ordered mutation, `is_rate_limit_error` → `return False`: **10 failed, 36 passed**,
  exit 1. Ids: `test_in_repo_fixture_reasons_classify[overloaded_error-…]`,
  `[rate_limit-…]`, and all 8 `test_provider_vocabulary_spellings_classify[…]`.
- The reader tests SURVIVE that mutation: readers reach the wording table through
  `classify_rate_limit_reason`, of which `is_rate_limit_error` is the emptiness test.
  So a second mutation ran, `classify_rate_limit_reason` → `return None`: **17 failed,
  29 passed**, exit 1, adding `test_inventory_shape_1/2/3`,
  `test_normalize_bounds_the_raw_text`, `test_read_run_event_signals_on_a_mixed_event_list`,
  `test_read_retry_reason_signals_on_a_mixed_reason_list`,
  `test_to_json_keeps_a_missing_retry_hint_as_null`. The table is load-bearing everywhere.
Worktree removed and pruned; `git worktree list` back to one line.

## T001 inventory (step 1) — 5 shapes, 1 more than the block seeded
All four seeded shapes confirmed on disk at the exact lines given. `rg -i
'overload|throttl|too many requests|429|rate.?limit' packages/ tests/ apps/` found ONE
additional real sample: `tests/orchestration/fixtures/stream/retry_and_error.jsonl:3`,
`{"type":"api_retry","attempt":2,"reason":"rate_limit"}` — a second literal beside
`overloaded_error` on line 2 of the same fixture. Every other hit is an unrelated
`4294967295`, a step id, or `packages/orchestration/mission_dossier.py:980`, whose
"rate-limits" is `RecallFact` demo prose. All five are in the module docstring with
their file:line. No sample was invented.

## Findings — 2 open
R-0361 (Low, carried forward verbatim) and R-0362 (Medium, registered this round).
Next free id: R-0363. No `Done:` text was written — that is the reviewer's alone.

## Deviations, declared (this handoff is 106 lines; DECISION D15 — the cause is the
## mandated per-commit table, the 17-gate block, the two-mutation red-proof and the
## item-status table, none of which may be dropped)
1. **C3 split into two commits.** 633 insertions together, over the AGENTS.md 500 cap
   (DECISION F104 D1 counts insertions only). Separable — nothing imports the module —
   so the inseparability exception does not apply and AGENTS.md's own remedy (split) was
   used, as at F052 R1 on 2026-07-30. C3a is 294 insertions, C3b is 339.
2. **Gate 14, `python3 -m ruff check`, is RED and was RED before this round.** Exit 1,
   26 errors: 20 I001, 4 F401, 1 F821, 1 UP035 — identical statistics at 21c8148e in a
   throwaway worktree, so this round adds zero. Ruff on the two NEW files → "All checks
   passed!", exit 0. Not repaired here: an unrelated fix may not ride a feature branch.
3. **Authored-text transport used Python, not `sed`.** This session's sandbox denies
   `sed … > target` and every pipe-to-file form. `.remedy-wt/f057_r1_extract.py` does the
   identical marker-delimited slice of the committed `.agent/authored/f057-r1.md`; no text
   was retyped, and `.remedy-wt/f057_r1_prove.py` proved applied == extracted for all four
   texts (LIVE-REVIEW 3578 B, DECISION 2857 B, PLAN 1708 B, CONTEXT 1804 B). Both scripts
   live in gitignored `.remedy-wt/` and are not committed.
4. **The saved block runs to the end of the ROUND GATES section**, i.e. through the
   closing "report the exact output." paragraph rather than stopping at gate item 17.

## Next
Reviewer: re-read `.agent/STOP` (Phase 1 rule 1), then review 21c8148e..HEAD bottom-up
and re-run every gate. Then R2 — T002, the governor: per-provider cooldown state,
`acquire()` with a budget deadline, an injected clock, stop-beats-wait ordering.
