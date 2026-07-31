# Handoff — F053 · R3 (worker)

`feature/f053-run-report`, pushed. No verdict written, nothing merged, no
closure work. GATE NOT CLEAN — one branch-only id, ruling needed (below).

## Range
Review of 1a5af0da..HEAD.

## Commits

### fd5698b6 chore(f053): persist R2 verdict (PASS) + register R-0161 + DECISION D3
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +49/-6 | R3 step, R2 PASS, R-0161 + D3 (f053-r3-1/2/3) |
| docs/agents/integration_gate.md | +9/-2 | step 2 replaced: base worktree ON a branch (f053-r3-4) |
| .agent/authored/f053-r3-{1..4}.md | +59 | authored texts, verbatim |
| .agent/last_block.md | +106/-54 | R3 block, OUTCOME pending |

### c2d9f790 fix(f053): refuse job report --final on a run still in progress
| Path | +/- | Reason |
|---|---|---|
| apps/cli/commands/job.py | +25 | --final guard reading REPORTED_TERMINALS; text + json refusal |
| tests/cli/test_job_report.py | +82/-2 | refusal tests, 5 terminals allowed, one R2 test moved to a terminal job |

### 9e0b4035 feat(f053): cap the capability lines like every other list
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/run_report.py | +16/-3 | MAX_CAPABILITY_LINES=10 via _capped, both lists |
| tests/orchestration/test_run_report.py | +20 | 30→10 + honest count; goldens stay below cap |

### handoff commit (self-reference, R-0149 pattern)
| Path | +/- | Reason |
|---|---|---|
| .agent/{handoff,plan,decisions,last_block}.md | rewrite/+25 | this file; R3 done + ruling needed; gate-parity decision; OUTCOME executed |

No commit exceeded 500 lines.

## External actions
`git push` x3 -> 1a5af0da..9e0b4035. No PR. Gate worktree:
`git worktree add -b tmp/base-gate <scratchpad>/base-gate-wt 15105dbe`
(ON A BRANCH per the amended step 2 — `git branch --show-current` printed
`tmp/base-gate`), then removed, pruned, branch deleted.
`git worktree list` shows only the primary; `git status --porcelain` empty.

## Verification
    $ pytest tests/cli/test_job_report.py -q            → 30 passed, exit 0
    $ pytest tests/orchestration/test_run_report.py -q   → 68 passed, exit 0
    $ pytest tests/docs/ -q                              → 293 passed, exit 0
    $ pytest tests/cli/test_golden_path.py -q (canary)   → 42 passed, exit 0
ruff clean on every file touched.

### Gate step 1 — branch run (HEAD 9e0b4035)
    $ python3 -m pytest -n auto -q
    1 failed, 14609 passed, 19 skipped in 126.00s (0:02:05)   exit 1
branch_failed.txt (1):
    FAILED tests/ui_server/test_dashboard_contract.py::TestLiveReviewAndAgentStateRefs::test_context_md_no_stale_steps

### Gate step 2 — base run (15105dbe, worktree on branch tmp/base-gate)
    $ python3 -m pytest -n auto -q
    6 failed, 14484 passed, 19 skipped in 106.85s (0:01:46)   exit 1
base_failed.txt (6):
    FAILED tests/ui_server/test_dashboard_contract.py::TestJobSummaryCommandContract::test_typescript_compiles
    FAILED tests/ui_server/test_live_state.py::TestUIServerIntegration::test_api_invalid_token_403
    FAILED tests/ui_server/test_live_state.py::TestUIServerIntegration::test_api_missing_job_404
    FAILED tests/ui_server/test_live_state.py::TestUIServerIntegration::test_brain_endpoint
    FAILED tests/ui_server/test_live_state.py::TestUIServerIntegration::test_dashboard_no_raw_leaks
    FAILED tests/ui_server/test_live_state.py::TestUIServerIntegration::test_put_rejected

### Gate step 3 — comm (both raw)
`comm -13 base branch` (BRANCH-ONLY, 1):
    FAILED tests/ui_server/test_dashboard_contract.py::TestLiveReviewAndAgentStateRefs::test_context_md_no_stale_steps
`comm -23 base branch` (BRANCH-FIXED, 6): exactly the six base ids above.

Attribution — every `comm -23` id, direct evidence:
| id | evidence |
|---|---|
| test_typescript_compiles | `npx tsc` → `Cannot find module '<base-wt>/apps/ui/node_modules/.bin/tsc'` (MODULE_NOT_FOUND) |
| the 5 TestUIServerIntegration ids (invalid_token_403, missing_job_404, put_rejected, dashboard_no_raw_leaks, brain_endpoint) | each: `[remedy-ui] npm install failed: … exit status 217` → "ERROR: React UI not built" → "Server did not start in time" |
All six are the doc's UI-artifact environment class. Parity was ATTEMPTED
first (symlinked apps/ui/node_modules + dist) and DEFEATED: the auto-build
ran `npm install`, replacing the node_modules symlink with a real partial
install. Empirical confirmation instead — re-run at base with parity
restored AND `REMEDY_UI_NO_AUTO_BUILD=1`: **17 passed, exit 0**. So none
of the six is a genuine base failure. Side effect, declared: the
auto-build wrote through the `dist` symlink into the PRIMARY checkout's
`apps/ui/dist` (gitignored, tree clean, `tests/ui_server/` 259 passed —
artifact valid). `.agent/decisions.md`: copy, not symlink, next time.

### Gate step 4 — attribution of the branch-only id
Serial re-run: `1 failed in 0.08s`, exit 1 → serial-FAIL, reproducible,
not an xdist flake. Passes at base (absent from base_failed.txt).
Cause: the test asserts the substring `"Steps"` in `.agent/context.md`;
the R1 rewrite dropped the section carrying it. NOT coupled to feature
code — no F053 module involved. Same state-file contract class as the
F046 `plan.md` / F047 `live_review.md` repairs (decisions.md 2026-07-26).

### Gate step 5 — wall clock
Branch 126s, base 107s. Both under ~5 min; no perf pass needed.

## Authored-text proofs
All four sha256-verified BEFORE use, applied by `cp`, never retyped:
r3-1 `d0df7eca…3005b7` · r3-2 `7cbf3bc2…d733b5` · r3-3 `6b59aa65…c7f7a4` ·
r3-4 `b261f51a…cf6fc1` — all equal the block's BEGIN-marker digests.
Saved-copy `cmp` vs the verified scratchpad originals: exit 0 x4.
APPLIED-REGION cmp (region extracted from the target file, cmp'd against
the original): exit 0 x4, each occurring exactly once — r3-1/2/3 in
.agent/live_review.md, r3-4 in docs/agents/integration_gate.md.

## Item status
| Item | Status | Reason |
|---|---|---|
| COMMIT A verdict + R-0161 + D3 + gate-doc amendment | done | 4 regions, cmp 0 each |
| COMMIT B R-0161 --final guard | done | Done: R-0161 |
| COMMIT C capability cap (A9) | done | |
| Gate step 1 branch run | done | 1 failed / 14609 passed |
| Gate step 2 base run | done | 6 failed / 14484 passed, worktree on a branch |
| Gate step 3 comm + attribution | done | all 6 comm -23 attributed empirically |
| Gate step 4 branch-only attribution | done | serial-fail, state-file class, NOT fixed |
| Gate step 5 wall clock | done | 126s / 107s |

## Deviations & assumptions
- The one branch-only failure was NOT fixed. The block forbids fixes
  inside the gate round, and the doc's BLOCKER definition is a failure
  coupled to FEATURE code — this is a `.agent/context.md` state-file
  contract, not feature code. Handed back raw rather than repaired
  unilaterally. RULING NEEDED: the repair is one line — give
  `.agent/context.md` a real `## Next Steps` heading (F046/F047
  precedent). A reviewer-authored text or an explicit go-ahead, plus a
  re-run of gate step 1, closes it.
- Base parity used symlinks; that is also a write path (see above).

## Next
Reviewer verdict on R3 + the ruling on `test_context_md_no_stale_steps`.
Closure is R4, its own round.
