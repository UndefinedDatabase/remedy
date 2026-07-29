# Handback — F252 R3 (R-0153 + integration gate + determinism proof)

## Range
Review of fc3e843..6ba3fc6 + the handoff commit · feature/f252-standing-red-paydown ·
R-0153 done · gate complete, zero branch-only failures · 3-run proof green · no STOP.

## Commits
### e2cff74 chore(f252): persist R2 verdict + R-0153
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f252-r3-1/2.md · live_review.md · plan.md · last_block.md | +196/-40 | authored texts (sha256-verified) applied by copy; R3 block |
### 6ba3fc6 test(f252): drop a dead assertion from the README pin (R-0153)
| Path | +/- | Reason |
|---|---|---|
| tests/docs/test_docs_consistency.py · .agent/live_review.md | +1/-6 | `assert unaccepted <= named`, its now-unused binding and its comment removed; the accepted-blocks loop untouched. `Done: R-0153` |
### handoff commit (self-reference exception)
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md · .agent/last_block.md | rewrite · +1/-1 | this handback; OUTCOME → executed |

## External actions
2 pushes to origin/feature/f252-standing-red-paydown, handoff commit last. `git worktree
add <scratch>/base-wt 7baff1d` for the base run, then `remove --force` + `prune`;
`git worktree list` shows the primary checkout only. No PR, merge, evidence job or zip.

## Verification
R-0153: `pytest tests/docs/ -q` → 0, "292 passed in 0.31s"; canary
`pytest tests/cli/test_golden_path.py -q` → 0, "42 passed in 14.92s".

Integration gate (docs/agents/integration_gate.md, step by step):
1. BRANCH `python3 -m pytest -n auto -q` → exit 0, "14295 passed, 19 skipped in 175.82s
   (0:02:55)", real 2m57.6s; `grep '^FAILED' | sort > branch_failed.txt` → **0 lines**.
2. BASE, same command in a throwaway worktree at merge-base 7baff1d → exit 1,
   "161 failed, 14139 passed, 14 skipped in 196.93s (0:03:16)", real 3m18.7s;
   `base_failed.txt` → 161 lines. Worktree removed + pruned (see External actions).
3. COMPARE `comm -13 base_failed.txt branch_failed.txt` (branch-only) → **EMPTY**;
   `comm -23` (fixed by the branch) → **161**.
4. ATTRIBUTION: no branch-only ids exist — nothing to classify, no serial re-runs, no
   BLOCKER. 5. BUDGET: 2m58s / 3m19s, under the ~5 min threshold; verdict is the reviewer's.

Base vs catalog, 161 = 154 − 4 + 11: the 4 non-reproducing ids are the D4 live-state pair
reading `.agent/live_review.md` + `plan.md` — the base worktree checks out its own
PH-v4-era `.agent` (the known F251 live-coupling risk). The 11 extras are outside the
catalog and GREEN on the branch, so not branch-only: `test_self_dogfood_execution_cli`
(2), vitest (1), tsc (1), `test_live_state.py::TestUIServerIntegration` (7).

Determinism proof — 3× `pytest -n auto -q --junitxml=…/f252-run<i>.xml`, nothing changed
in between: run1 exit 0 "14295 passed, 19 skipped in 131.77s" (real 2m12.3s); run2 exit 0
"…122.42s" (2m04.3s); run3 exit 0 "…133.55s" (2m15.5s).
- junitxml failing-id sets (LC_ALL=C sorted): run1 = run2 = run3 = **EMPTY** (0 ids);
  pairwise diff 1↔2, 2↔3, 1↔3 all IDENTICAL.
- Skips 19/19/19; run3 xml breakdown: **11** carrying "quarantine (F252)" (10× D3,
  1× D12) + **8** env-gated (4× REMEDY_*_OLLAMA_*, 4× "UI source not found").
- All three ~2 min, inside the §3 budget — no perf note required.

## Authored-text proofs
f252-r3-1 (1f07b06c…) and f252-r3-2 (dc3e03cc…): on-disk `sha256sum` matched the BEGIN
markers exactly BEFORE any commit; applied by copy, `cmp` exit 0 for live_review.md and
plan.md. live_review.md was then edited in one place only, as ordered: `Done: R-0153`.

## Deviations & assumptions
- None. The change is exactly the two authored replacements plus the five deleted lines
  in `tests/docs/test_docs_consistency.py`; no product code touched this round.
- Recorded, not acted on: the base run's 11 extra failures are merge-base environment
  noise (real Ollama, a vitest/tsc toolchain, a live UI server), in no F252 class.

## Next
Reviewer verdict on R3 (the gate verdict is the reviewer's); then R4, the closure round.
