# Interim handback — F251 R1 (repair of R-0150)

## Range
Review of `d8ac7fa..HEAD` — `feature/f251-suite-stabilization`, pushed, no PR.
`8aa10d1` is NOT in this range: it landed on the chore branch and reached main
through the #157 merge, so it is an ancestor of d8ac7fa. Tabled below anyway.

## Commits
### 8aa10d1 chore(plan): persist the amendment R1 PASS verdict — on chore/plan-amendment-flake-debt, merged via #157
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/pamend-r2-1.md | +30 | operator verdict text, sha256 08086518… |
| .agent/live_review.md | +22 −3 | full replace from pamend-r2-1 (cmp 0) |

### 6280cb0 chore(f251): claim F251 — round bookkeeping
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f251-r1-1..3.md | +50 | operator texts, sha256-verified |
| .agent/live_review.md | +14 −28 | full replace from f251-r1-1 (cmp 0) |
| .agent/plan.md | +35 −51 | full replace from f251-r1-3 (cmp 0) |
| docs/roadmap/STATUS.md | +1 −1 | `[ ]`→`[~]` from f251-r1-2 (containment 0) |

### 16817d4 docs(f251): S1 baseline result and S2 per-class decision table
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +40 −27 | S1 measured result + S2 per-class table |

### 977ea47 chore(f251): handback for round 1 (stop-on-red after S2)
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | +116 −91 | round-1 handback (116 lines — over the cap) |

### da61a40 chore(f251): trim handback to the AGENTS.md line cap
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite → 91 lines | still over ≤60; flagged, not hidden |

### 69cabd6 + this commit (self-reference, R-0149 grouped table)
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f251-r1-4.md | +34 | 69cabd6 — R-0150 verdict text, sha256 413ee9fe… |
| .agent/live_review.md | +28 −4 | 69cabd6 — full replace from f251-r1-4 (cmp 0) |
| .agent/handoff.md | rewrite | this commit — the R-0150 repair |

## Item status — standing block steps 1–9
| Item | Status | Reason |
|---|---|---|
| 1 verdict commit (pamend-r2-1) | done | 8aa10d1, cmp 0, pushed |
| 2 merge #157, main clean | done | main 73ac5cc..d8ac7fa, porcelain empty |
| 3 F251 claim (branch, STATUS `[~]`) | done | 6280cb0, pushed |
| 4 S1 baseline | done | ran in full; transcripts below; files not yet committed |
| 5 S2 decision table | done | 16817d4 (in .agent/plan.md) |
| 6 S3 root-cause fixes | skipped | stop-on-red — see Deviations |
| 7 S4 quarantine | skipped | stop-on-red — see Deviations |
| 8 S5 triple-run proof | skipped | unreachable under the declared scope |
| 9 canary | done | 42 passed |

## External actions
`gh pr merge 157 --merge --delete-branch` → merged, main 73ac5cc..d8ac7fa ·
`git checkout main && git pull --ff-only` → up to date, clean ·
`gh pr list --state open` → `[]` before branching ·
`git push -u origin feature/f251-suite-stabilization` → new branch, then pushes at
977ea47, da61a40, 69cabd6 · `git worktree add`/`remove` of a clean-main control
tree under the session scratchpad (removed; `git worktree list` clean) ·
no PR created — reviewer-gated.

## Verification
    run1  time python3 -m pytest -n auto -q
          → 168 failed, 14138 passed, 8 skipped, 1 error in 176.97s; real 2m57.371s
    run2  time python3 -m pytest -n auto -q
          → 167 failed, 14139 passed, 8 skipped in 172.56s;          real 2m53.019s
    set diff run1/run2 → 161 common, 8 only-run1, 6 only-run2 (14 churning ids)
    161 re-run serially (--tb=line) → 156 failed, 5 passed in 134.76s
    same 161 on a clean main worktree → 156 failed, 5 passed in 143.98s;
          comm both directions EMPTY ⇒ the 156 are pre-existing on main
    19 flake ids isolated, -n auto ×3 → 5 failed/14 passed each, DIFFERENT ids
    19 flake ids isolated, serial     → 5 failed, another id set
    canary python3 -m pytest tests/cli/test_golden_path.py -q → 42 passed in 14.78s
    git status --porcelain → empty (before this commit)
Baseline transcripts are still in the session scratchpad; committing them under
`.agent/f251_baseline/` is the next action of this repair round.

## Authored-text proofs
sha256 matched the BEGIN marker BEFORE every commit: pamend-r2-1 `08086518…`,
f251-r1-1 `bbc0f9f5…`, f251-r1-2 `c71e23d8…`, f251-r1-3 `c61db1cd…`,
f251-r1-4 `413ee9fe…`. `cmp` exit 0 for each full replace of `.agent/live_review.md`
and `.agent/plan.md`; containment exit 0 for f251-r1-2 → STATUS.md (numstat 1/1).

## Deviations & assumptions
- **R-0150 range note (not a dispute of the finding):** the stale handback is real
  for the reviewed range `d8ac7fa..6280cb0`. It was rewritten later on the same
  branch at 977ea47 and trimmed at da61a40, i.e. two commits past the reviewed tip,
  so HEAD already carried a round handback before this repair. This commit makes it
  compliant per the template regardless. Resolved: this commit.
- **Cap breach, self-reported:** 977ea47 wrote a 116-line handoff and da61a40 cut it
  to 91; the AGENTS.md cap is ≤60 (≤100 only with >5 commit tables). This file has
  6 commit tables, so ≤100 now applies.
- **Stop-on-red at S3.** 156 of the 161 stable failures are deterministic and
  identical on clean main — standing red from product/docs/test drift, not flake.
  Only 14 ids churn. Fixing them needs product-code change beyond a hermetic-test
  seam; quarantining them would mark genuine regressions as quarantined. Both are
  excluded by T1_F251.md. Operator ruling requested.
- **Finding candidate (renumbered R-0151, was reported as R-0150 last round):**
  PR #157 took `docs/roadmap/features/` 250 → 251 and STATUS 250 → 251, breaking
  both pins in `tests/docs/test_docs_consistency.py::TestFeatureLedger`
  (`TOTAL_FEATURES = 250`). Verified 250 @73ac5cc vs 251 @d8ac7fa. Untouched.

## Next
Commit the baseline files under `.agent/f251_baseline/`, then the S2 table commit
and the final handback of this repair round.
