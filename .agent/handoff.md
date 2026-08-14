# Handoff — F057 rate-limit scheduler, round R9

## Range
Review of 37e88970..HEAD (branch feature/f057-rate-limit-scheduler).

## Commits

### 09285393 chore(f057): save the R9 block verbatim and re-mirror the plan ledger
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f057-r9.md | +206/-0 | R9 block, `cp`'d byte for byte from reviewer scratch |
| .agent/last_block.md | +191/-75 | same bytes, same sha256 |
| .agent/plan.md | +20/-19 | FULL REPLACEMENT from the PLAN slice (R-0377: ledger was false on disk) |

### bf4392b9 docs(f057): record the R8 verdict and three reviewer findings
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +8/-0 | GATE-R8, R-0376, R-0377, R-0378 appended; 4 slices + 4 blank separators |

### 0d798e4f test(f057): pin the reviewer parse-retry rate limit end to end
| Path | +/- | Reason |
|---|---|---|
| tests/orchestration/test_provider_retry.py | +80/-0 | one end-to-end test through `run_pingpong`; nothing existing touched |

### C3 (this handoff, self-reference exception)
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | the handback itself — a handoff cannot table its own commit |

## Item status
| Item | Status | Reason |
|---|---|---|
| C0 | done | block saved verbatim; plan.md full-replaced in the round's FIRST commit |
| C1 | done | four slices appended, byte-identical, append-shaped |
| C2 | done | one test added inside the F057 seam section, reusing SeamFakeClock/_seam_governor |
| C3 | done | this file |

## External actions
`git push -u origin feature/f057-rate-limit-scheduler` after each of C0, C1, C2, C3 — all OK.
`git worktree add .remedy-wt/r9red HEAD --detach` → OK; `git worktree remove --force` + `git worktree prune` → OK, list back to one line.
No `gh` commands, no merge, no force-push.

## Verification — all 15 gates, measured
1. `git status --porcelain` → empty (baseline empty).
2. `git worktree list` → `/home/decodeux/Repos/remedy  0d798e4f [feature/f057-rate-limit-scheduler]` — one line.
3. `cmp .agent/authored/f057-r9.md .agent/last_block.md` → exit 0, no output. sha256 (both, and `git show HEAD:` of the committed file) `14f52a4c4321e91d4776b1db895f8271fdc18b498600c652d974d626b9aa7e20`; 206 lines each.
4. `wc -l .agent/plan.md` → `37` (< 50). `cmp` of the PLAN slice extracted from the COMMITTED block (lines 152–188) against `.agent/plan.md` → exit 0, no output.
5. `.agent/live_review.md` line-anchored: `^Gate: R8 — PASS`=1, `^- R-0376 — `=1, `^- R-0377 — `=1, `^- R-0378 — `=1, `^## Steps`=1. Whole-file SUBSTRING count of `## Steps` = 9 — UNCHANGED from the 9 the reviewer measured at 37e88970.
6. `git show --numstat bf4392b9 -- .agent/live_review.md` → `8	0` — 8 insertions, deletion column 0.
7. `python3 -m pytest tests/orchestration/test_provider_retry.py -q` → `30 passed in 0.25s`, exit 0. Baseline 29; C2 adds exactly one.
8. `python3 -m pytest tests/orchestration/test_rate_governor.py -q` → `59 passed in 0.08s`, exit 0 — unchanged from baseline 59.
9. four regression files together → `294 passed in 38.99s`, exit 0 — exactly the ordered value.
10. `python3 -m pytest tests/cli/test_golden_path.py -q` → `42 passed in 15.88s`, exit 0 — baseline 42.
11. `python3 -m ruff check packages/orchestration/pingpong_loop.py tests/orchestration/test_provider_retry.py` → `All checks passed!`, exit 0.
12. RED-PROOF, in the disposable worktree `.remedy-wt/r9red` only. Resolved import path printed from INSIDE it: `/home/decodeux/Repos/remedy/.remedy-wt/r9red/packages/orchestration/pingpong_loop.py`. Removed the single line `rate_governor=_rate_governor,` from the parse-retry `_call_with_retry` (the `retry_out` one) — `git -C … diff --stat` → `1 file changed, 1 deletion(-)`. Re-ran the new test: it FAILED. Failing id `tests/orchestration/test_provider_retry.py::TestRateGovernorSeam::test_parse_retry_rate_limit_is_paced_end_to_end`; assertion `assert provider.review_calls == 3` → `E assert 2 == 3`. Worktree removed and pruned.
13. `git diff --name-only 37e88970..HEAD` → `.agent/authored/f057-r9.md`, `.agent/last_block.md`, `.agent/live_review.md`, `.agent/plan.md`, `tests/orchestration/test_provider_retry.py` — five at C2, and `.agent/handoff.md` arrives with C3 itself, making the ordered six and no seventh.
14. `git diff --stat 37e88970..HEAD -- packages/ apps/` → EMPTY. No production code changed.
15. `git diff --stat 21c8148e..HEAD -- packages/orchestration/provider_timeouts.py packages/orchestration/stream_evidence.py` → EMPTY (declared branch-point base, per the block's own gate text).

## Authored-text proofs
Disk to disk against the COMMITTED `.agent/authored/f057-r9.md`, per-line sha256 (source line → live_review line), all equal:
GATE-R8 192→79 `c9a251a16e3c856e7ce18a1865edc6174fe41e1cec992fa3f12a7fbb8dffe79d`;
R-0376 196→81 `69ee888fc95cc42638c4336d4e0f588d7b4bb00c967a6a2aa7d3fff0f740065e`;
R-0377 200→83 `8a0e6889763ab35923a9670a728646fb940f47698dd919fdc90db38b52930cba`;
R-0378 204→85 `f47ec5e9cd34ef235a57dfae66dc1eaa887f9e8d4e0acaad0150e6100ef9b67d`.
Lines 78, 80, 82, 84 are each the empty line (`01ba4719…`), so every slice is one physical line preceded by exactly one blank. No `Done:` paragraph authored.

## Deviations & assumptions
- Handoff length: this file is over the 60-line cap. DECISION D15 stated cause — the mandated content is the 15-gate verification transcript, the four per-commit changed-files tables, the item-status table and the four-line authored-text proof. No section dropped.
- The test passes for the reason the block names, and the red-proof says so rather than the colour alone: with `rate_governor=` removed from the parse-retry call site the rate-limited retry never happens (`review_calls` 2, not 3). No other deviation: no production file was edited, no gate was re-based, nothing was changed to make a gate pass.
- Fixture choice (block left it to the worker): the reviewer's parse retry returns `provider_error: RuntimeError: 429 Too Many Requests` — prefixed so the `is_reject` rule exempts it, and free of `exited`/timeout wording so no pre-existing transport predicate retries it. The WHY comment above the test names that dependency and points at R-0378.

## Open findings
13 open: R-0361, R-0362, R-0363, R-0364, R-0367, R-0368, R-0369, R-0371, R-0374, R-0375, R-0376, R-0377, R-0378. None resolved this round by design. R-0374's subject is now pinned on disk, but only reviewer-authored text may close it.

## Next
Reviewer verdict on R9 at 37e88970..HEAD; then T003 part 2 item 2 — the report surfaces (`rate_limit_waits` in `export_pingpong_json`, the wait line in `summarize_pingpong`).
