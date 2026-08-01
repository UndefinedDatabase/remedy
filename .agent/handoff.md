# Handoff — F062 R3 (repair: R-0167)

## Range
Review of `4d78cd12..HEAD` — R-0167 Done: a disabled smoke refuses before any
process starts.

## Commits
### c3461930 chore(f062): persist the R2 verdict + register R-0167
| Path | +/- | Reason |
| --- | --- | --- |
| `.agent/authored/f062-r3-{1,2,3}.md`, `live_review.md`, `last_block.md` | +159/-125 | authored texts sha256-verified; three FROM→TO blocks by copy; R3 block verbatim |

### b6efe456 fix(f062): a disabled smoke refuses before starting anything
| Path | +/- | Reason |
| --- | --- | --- |
| `dod_runners.py`, `product_smoke.py`, `tests/.../test_product_smoke.py` | +154/-4 | `REASON_SMOKE_DISABLED` + early refusal after the not-applicable check; `DISABLED_MESSAGE` one shared constant; 7 tests incl. the marker-file process fact |

### 2c1907c3 + final handoff commit (grouped self-reference, R-0149)
| Path | +/- | Reason |
| --- | --- | --- |
| `.agent/live_review.md`, `.agent/{handoff,last_block}.md` | +1 + rewrite | 2c1907c3 the `Done: R-0167 (commit b6efe456).` line; final commit: this report + OUTCOME executed |

## External actions
- `git push` after commit 1 and before handback (head == remote). No PR.
- `worktree add -b tmp/f062-r3-redproof <path> HEAD` for the red-proof; then
  `remove --force`, `prune`, `branch -D`; `worktree list` → primary only. A
  first attempt cut it at the Part-0 commit; removed and redone at the fix.

## Verification
    $ pytest tests/orchestration/{test_product_smoke,test_dod_runners,
        test_dod_compiler}.py tests/orchestration/schemas -q  244 passed EXIT=0
    $ pytest tests/cli/test_golden_path.py -q  42 passed EXIT=0    (smoke: 76)
    $ git status --porcelain  (empty)
    Red-proof (early refusal deleted, worktree at b6efe456): 5 failed EXIT=1 ←
      TestDisabledStartsNothing; the marker file existed ("the app was started
      despite smoke.enabled=false"). Unmutated: 7 passed EXIT=0

## Authored-text proofs
`f062-r3-1` → 76fb2f88… · `-2` → 7f0fe391… · `-3` → 92b8207e…, all matching
their BEGIN markers. **`f062-r3-3` arrived with no `--- END ---` marker**; the
boundary I inferred is confirmed by its hash — nothing truncated. r3-1/2: FROM
1× before, 0× after, TO 1× after. r3-3's TO embeds its FROM, so the surviving
count-1 hit IS the TO.

## Deviations & assumptions
1. **`DISABLED_MESSAGE` hoisted to a shared constant** for the compile-time row
   and the run-time refusal — value byte-identical, so the pinned row is
   unchanged; it only makes drift impossible.
2. **Refusal ordered after not-applicable** — no runtime still reports
   `smoke_not_applicable`; "no app here" stays distinct from "we didn't look".
3. **All three smoke kinds refuse early** when disabled, not only `app_starts`.
4. **Gating machinery untouched**: a stored `blocking=True` row still holds the
   job; the disabled row the block contributes only reports. All four pinned.

## Next
Handing back to Window 1 for review of `4d78cd12..HEAD`.
