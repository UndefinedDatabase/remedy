# Handback — F251 Full-suite stabilization (R1) — STOP-ON-RED after S2

## Range
Review of `d8ac7fa..HEAD` — branch `feature/f251-suite-stabilization`,
2 commits, pushed, **no PR** (reviewer-gated). d8ac7fa = main head at
branch creation = LAST_REVIEWED_SHA.

## Commits
### 6280cb0 chore(f251): claim F251 — round bookkeeping
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f251-r1-1..3.md | +50 | operator texts, sha256-verified |
| .agent/live_review.md | +14 −28 | full replace from f251-r1-1 |
| .agent/plan.md | +35 −51 | full replace from f251-r1-3 |
| docs/roadmap/STATUS.md | +1 −1 | `[ ]`→`[~]` F251 line from f251-r1-2 |

### handoff/plan commits (self-reference, R-0149 grouped table)
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +40 −27 | 16817d4 — S1 result + S2 decision table |
| .agent/handoff.md | rewrite | this handback |

## Item status
| Item | Status | Reason |
|---|---|---|
| 1 verdict commit (pamend-r2-1) | done | 8aa10d1 on the chore branch |
| 2 merge #157 + main clean | done | main d8ac7fa, tree clean, F251 line before F050 |
| 3 F251 claim (branch, STATUS `[~]`, resets) | done | 6280cb0 |
| 4 S1 baseline | done | 2 full runs + serial + clean-main control |
| 5 S2 decision table | done | 16817d4 |
| 6 S3 root-cause fixes | **skipped** | stop-on-red, see Deviations |
| 7 S4 quarantine | **skipped** | stop-on-red, see Deviations |
| 8 S5 triple-run proof | **skipped** | unreachable under declared scope |
| 9 canary | done | 42 passed |

### Per-class table — flake classes (19 ids, F251's real subject)
| # | Class | ids | Decision | Outcome |
|---|---|---|---|---|
| F-A | runtimes supervisor/dev_server/probe/process-boundary | 12 | fix else quarantine | not started |
| F-B | test_grouped_cli JSON subcommands | 4 | hermetic fix | not started |
| F-C | test_data_paths default root | 1 | hermetic fix | not started |
| F-D | cli/test_runtime_cmd TestProbe | 1 | fix | not started |
| F-E | cli/test_job_rerun_manifest TestCurrentTargetDrift | 1 | investigate | not started |

### Per-class table — standing red (156 ids, deterministic, NOT flake)
D1 flat-path doc/file missing 36 · D14 misc drift 46 · D13 review-zip 11 ·
D5 CLI needs registered project 11 · D3 apps/ui legacy tsx 10 · D6 MagicMock 9 ·
D4 `.agent` state-file contracts 9 · D10 discover-commands rc=1 8 · D7 dev_server
private names 6 · D8 flight-plan schema_v 3 · D11 TOML error class 3 · D9 catalog
classification 3 · D12 .claude/agents 1. **All BLOCKED** — each needs product-code
change beyond a hermetic-test seam, or quarantine of genuinely-red tests.

## External actions
- `gh pr merge 157 --merge --delete-branch` → merged; main `73ac5cc..d8ac7fa`.
- `git checkout main && git pull --ff-only` → up to date, tree clean.
- `gh pr list --state open` → `[]` (gate clean before branching).
- `git push -u origin feature/f251-suite-stabilization` → new branch, tracking set.
- No PR created — reviewer-gated per the step.

## Verification
    run1  time python3 -m pytest -n auto -q → 168 failed, 14138 passed, 8 skipped,
          1 error in 176.97s;  real 2m57.371s
    run2  same command            → 167 failed, 14139 passed, 8 skipped in 172.56s;
          real 2m53.019s
    set diff run1 vs run2 → 161 common, 8 only-run1, 6 only-run2 (14 churning ids)
    serial re-run of the 161 (--tb=line) → 156 failed, 5 passed in 134.76s
    clean `main` worktree, same 161 serially → 156 failed, 5 passed in 143.98s;
          comm both directions EMPTY ⇒ identical set, red is pre-existing
    flake set (19 ids) isolated, -n auto ×3 → 5 failed/14 passed each time, but the
          failing IDS DIFFER between runs ⇒ genuine timing/process flake
    flake set isolated, serial → 5 failed, different 5 ids ⇒ order/cache dependency
    canary python3 -m pytest tests/cli/test_golden_path.py -q → 42 passed in 14.78s
    git status --porcelain → empty (before the handoff commit)

## Authored-text proofs
sha256 matched the BEGIN marker BEFORE every commit: pamend-r2-1
`08086518…`, f251-r1-1 `bbc0f9f5…`, f251-r1-2 `c71e23d8…`, f251-r1-3
`c61db1cd…`. Applications: `cmp` exit 0 for live_review←pamend-r2-1,
live_review←f251-r1-1, plan←f251-r1-3; containment exit 0 for
f251-r1-2 → STATUS.md (numstat 1/1, no other line touched).

## Deviations & assumptions
- **Stop-on-red, S3 onward not started.** The step's premise ("~150–215
  failures churning in both directions") does not hold. Measured: counts move
  only 167↔169 and just **14 ids churn**; 156 failures are deterministic and
  reproduce identically on clean main. That is standing red from accumulated
  product/docs/test drift, not flake debt. Reaching the done-definition would
  require either fixing 156 real defects (excluded: "no product features, no
  CLI work, no executor changes beyond hermetic-test fixes") or quarantining
  156 genuinely-red tests — which T1_F251.md forbids in substance ("never
  weakened assertions"; "a test exposing a REAL product bug is a finding").
  Both S3's rule ("product-code change beyond a hermetic-test seam ⇒ STOP")
  and the S5 stop-on-red rule are triggered. Operator ruling needed.
- **Finding candidate R-0150 (High):** PR #157 took `docs/roadmap/features/`
  from 250 → 251 files and STATUS from 250 → 251 entries, breaking
  `tests/docs/test_docs_consistency.py::TestFeatureLedger` (both pins,
  `TOTAL_FEATURES = 250`). Verified: 250 files at 73ac5cc, 251 at d8ac7fa.
  The amendment round's canary was golden-path only, so it did not surface.
  T1_F251.md calls F251 a "registered work item", not one of the 250 — so the
  fix is a decision (raise the pin to 251, or exclude registered work items
  from the ledger count), not a mechanical edit. Not touched.
- **D4 is self-referential:** 9 tests assert on live `.agent/plan.md`,
  `context.md`, `live_review.md` content (e.g. a `Steps N-M` range, an
  `## Active Branch` heading). Every worker that rewrites those files moves
  the suite. `.agent/context.md` is still F046's. Structural, worth a ruling.
- 5 of the 19 flake ids fail only under `-n auto` (4× test_grouped_cli,
  1× test_runtime_cli_process_boundary); F-C's root cause is identified —
  `resolve_data_root()` falls through to a **cached** `get_config()`, so a
  `data_dir` set by an earlier test in the same worker leaks in.
- Scratch artifacts (baseline transcripts, junit xml, the `main` control
  worktree) live in the session scratchpad, outside the repo.

## Next
Operator ruling on the 156 standing-red classes (fix campaign vs mass
quarantine vs re-scope F251 to the 19 flake ids) and on R-0150.
**full suite on main: 0 quarantined, 14 churning, 156 standing red**
