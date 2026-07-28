# Plan — F251 Full-suite stabilization (R1, after the R-0150 repair)

## Goal
Three consecutive `pytest -n auto -q` runs with identical failure sets,
empty except explicitly quarantined tests.

## S1 baseline (done — evidence in .agent/f251_baseline/)
run1 169 fail / 2m57.371s · run2 167 fail / 2m53.019s · common 161 ·
churn 14 (8 only-run1, 6 only-run2). The 161 re-run serially: 156 fail,
5 pass. Same 161 serially in a clean `main` worktree: the identical 156.
**Flake debt = 19 ids. Standing red = 156 deterministic ids.**

## S2 per-class decisions
Flake classes — in scope, F251's actual subject:
| # | Class | ids | Churn | Root-cause hypothesis | Decision |
|---|---|---|---|---|---|
| F-A | runtimes supervisor / dev_server / probe / process-boundary | 12 | one set | process ownership + readiness timing under 24-worker load | root-cause fix; quarantine only per-test if it survives (reason + F251 backlog ref) |
| F-B | test_grouped_cli JSON subcommands | 4 | -n auto only | test-order / cached global state | hermetic fix |
| F-C | test_data_paths default root | 1 | one set | `resolve_data_root()` falls through to a **cached** `get_config()`; a `data_dir` from an earlier test in the same worker leaks in | hermetic fix |
| F-D | cli/test_runtime_cmd TestProbe | 1 | one set | same probe/port class as F-A | root-cause fix |
| F-E | cli/test_job_rerun_manifest TargetDrift | 1 | one set | shared tmp/data path | investigate |

Standing-red classes — deterministic, NOT flake (counts: class_map.txt):
| # | Class | ids | Decision |
|---|---|---|---|
| D14 | misc drift (README pinned text, spine docs, CLI timeouts) | 46 | BLOCKED — operator ruling |
| D1 | doc/file missing at pre-restructure flat path | 36 | BLOCKED — operator ruling |
| D13 | review-zip / evidence packaging drift | 11 | BLOCKED — product change |
| D5 | CLI requires a registered project (cwd coupling) | 11 | BLOCKED — product change |
| D3 | apps/ui `legacy/*.tsx` absent | 10 | BLOCKED — unbuilt UI |
| D6 | incomplete MagicMock vs real comparison | 9 | BLOCKED — test rewrite |
| D4 | `.agent` state-file content contracts | 9 | BLOCKED — see risks |
| D10 | discover-commands CLI rc=1 / non-JSON | 8 | BLOCKED — product bug |
| D7 | dev_server private names removed | 6 | BLOCKED — product change |
| D8 | flight-plan `schema_v` regression | 3 | BLOCKED — product bug |
| D11 | malformed TOML raises BudgetConfigError | 3 | BLOCKED — product change |
| D9 | command-catalog classification drift | 3 | BLOCKED — product change |
| D12 | `.claude/agents/remedy-reviewer.md` absent | 1 | BLOCKED — operator ruling |

Named-class mapping from the order: "~14 catalog/discovery" = D9 (3) + D10 (8)
+ F-B (4) = 15. "3 .agent contract failures" = D4, which is **9**, not 3.
"supervisor/probe xdist" = F-A + F-D = 13. "integrity-check
live_review_verdict matcher gap" is **not in the suite failure set** — it is a
`remedy integrity check` warn, no pytest id; nothing to decide here.

## Current Step
S2 delivered. S3/S4/S5 not started — stop-on-red: every D-class needs
product-code change beyond a hermetic-test seam, or quarantine of a
deterministically-red test, both excluded by T1_F251.md.

## Risks
- R-0151 candidate: PR #157 took `docs/roadmap/features/` 250 → 251 and broke
  both `TestFeatureLedger` pins (`TOTAL_FEATURES = 250`).
- D4 couples tests to live `.agent/*.md`, so worker edits move the suite.
