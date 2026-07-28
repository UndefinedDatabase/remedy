# Handback — F251 Full-suite stabilization (R1) — STOP-ON-RED after S2

## Range
Review of `d8ac7fa..HEAD` — `feature/f251-suite-stabilization`, 3 commits,
pushed, **no PR** (reviewer-gated). d8ac7fa = LAST_REVIEWED_SHA.

## Commits
### 6280cb0 chore(f251): claim F251 — round bookkeeping
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f251-r1-1..3.md | +50 | operator texts, sha256-verified |
| .agent/live_review.md | +14 −28 | full replace from f251-r1-1 |
| .agent/plan.md | +35 −51 | full replace from f251-r1-3 |
| docs/roadmap/STATUS.md | +1 −1 | `[ ]`→`[~]` from f251-r1-2 |

### 16817d4 + 977ea47 (self-reference, R-0149 grouped table)
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +40 −27 | 16817d4 — S1 result + S2 decision table |
| .agent/handoff.md | rewrite | 977ea47 — this handback |

## Item status
| Item | Status | Reason |
|---|---|---|
| 1 verdict commit | done | 8aa10d1 (chore branch) |
| 2 merge #157, main clean | done | main d8ac7fa, clean, F251 before F050 |
| 3 F251 claim | done | 6280cb0 |
| 4 S1 baseline | done | 2 full runs + serial + clean-main control |
| 5 S2 decision table | done | 16817d4 |
| 6 S3 fixes / 7 S4 quarantine / 8 S5 proof | **skipped** | stop-on-red (Deviations) |
| 9 canary | done | 42 passed |

Flake classes (19 ids, all `not started`): F-A runtimes supervisor/dev_server/
probe/process-boundary 12 (fix else quarantine) · F-B test_grouped_cli 4 (hermetic)
· F-C test_data_paths 1 (hermetic) · F-D test_runtime_cmd Probe 1 · F-E
test_job_rerun_manifest 1.
Standing red (156 ids, all `BLOCKED`): D1 flat-path doc missing 36 · D14 misc drift
46 · D13 review-zip 11 · D5 CLI needs registered project 11 · D3 apps/ui legacy tsx
10 · D6 MagicMock 9 · D4 `.agent` state-file contracts 9 · D10 discover-commands
rc=1 8 · D7 dev_server private names 6 · D8 flight-plan schema_v 3 · D11 TOML error
class 3 · D9 catalog classification 3 · D12 .claude/agents 1.

## External actions
`gh pr merge 157 --merge --delete-branch` → merged, main 73ac5cc..d8ac7fa ·
`git pull --ff-only` → clean · `gh pr list --state open` → `[]` before branching ·
`git push -u origin feature/f251-suite-stabilization` → new branch · no PR created.

## Verification
    run1  pytest -n auto -q → 168 failed, 14138 passed, 8 skipped, 1 error; real 2m57.371s
    run2  pytest -n auto -q → 167 failed, 14139 passed, 8 skipped;          real 2m53.019s
    diff run1/run2 → 161 common, 8 only-run1, 6 only-run2 (14 churning)
    161 re-run serially            → 156 failed, 5 passed (134.76s)
    same 161 on clean main worktree→ 156 failed, 5 passed (143.98s); comm both
                                     directions EMPTY ⇒ red is pre-existing
    19 flake ids isolated -n auto ×3 → 5 failed each, DIFFERENT ids ⇒ real flake
    19 flake ids isolated serial     → 5 failed, another id set ⇒ order/cache dep
    canary tests/cli/test_golden_path.py -q → 42 passed in 14.78s
    git status --porcelain → empty (before the handoff commit)

## Authored-text proofs
sha256 matched the BEGIN marker BEFORE every commit: pamend-r2-1 `08086518…`,
f251-r1-1 `bbc0f9f5…`, f251-r1-2 `c71e23d8…`, f251-r1-3 `c61db1cd…`. `cmp` exit 0
for live_review←pamend-r2-1, live_review←f251-r1-1, plan←f251-r1-3; containment
exit 0 for f251-r1-2 → STATUS.md (numstat 1/1, no other line touched).

## Deviations & assumptions
- **Stop-on-red; S3–S5 not started.** The step's premise ("~150–215 failures
  churning in both directions") does not hold: counts move only 167↔169 and just
  **14 ids churn**; 156 failures are deterministic and identical on clean main.
  That is standing red from product/docs/test drift, not flake debt. The
  done-definition would need either 156 real fixes (excluded: no product features,
  no CLI work, no executor changes beyond hermetic-test seams) or quarantining 156
  genuinely-red tests — which T1_F251.md forbids in substance. Operator ruling needed.
- **Finding candidate R-0150 (High):** PR #157 took `docs/roadmap/features/` 250 →
  251 and STATUS 250 → 251, breaking both pins in
  `tests/docs/test_docs_consistency.py::TestFeatureLedger` (`TOTAL_FEATURES = 250`).
  Verified 250 @73ac5cc vs 251 @d8ac7fa. The amendment canary was golden-path only.
  T1_F251.md calls F251 a "registered work item", not one of the 250 — so the fix is
  a decision (raise the pin, or exclude work items), not a mechanical edit. Untouched.
- **D4 is self-referential:** 9 tests assert on live `.agent/*.md` content (a
  `Steps N-M` range, an `## Active Branch` heading), so every worker rewrite moves
  the suite; `.agent/context.md` is still F046's. Structural — worth a ruling.
- F-C root cause identified: `resolve_data_root()` falls through to a **cached**
  `get_config()`, so a `data_dir` from an earlier test in the same worker leaks in.
- Scratch transcripts, junit xml and the `main` control worktree lived in the
  session scratchpad (worktree removed); nothing outside the repo remains.

## Next
Operator ruling on the 156 standing-red classes (fix campaign vs mass quarantine vs
re-scope F251 to the 19 flake ids) and on R-0150.
**full suite on main: 0 quarantined, 14 churning, 156 standing red**
