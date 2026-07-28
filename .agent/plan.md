# Plan — F251 Full-suite stabilization (R1)

## Goal
Three consecutive `pytest -n auto -q` runs with identical failure sets,
empty except explicitly quarantined tests.

## S1 baseline (done)
run1 169 fail / 176.97s · run2 167 fail / 172.56s · stable core 161,
churn 14 ids. Serial re-run of the 161: 156 fail, 5 pass. Identical 156
on a clean `main` worktree ⇒ pre-existing, not branch-induced.
**Flake debt = 19 ids. Standing red = 156 deterministic failures.**

## S2 per-class decisions
Flake classes (in scope — F251's actual subject):
| # | Class | ids | Decision |
|---|---|---|---|
| F-A | runtimes supervisor/dev_server/probe/process-boundary | 12 | root-cause fix, else quarantine |
| F-B | test_grouped_cli JSON subcommands (order/cache dep) | 4 | hermetic fix |
| F-C | test_data_paths default root (cached get_config leak) | 1 | hermetic fix |
| F-D | cli/test_runtime_cmd TestProbe | 1 | root-cause fix |
| F-E | cli/test_job_rerun_manifest TestCurrentTargetDrift | 1 | investigate |

Standing-red classes (deterministic; NOT flake):
| # | Class | ids | Decision |
|---|---|---|---|
| D1 | doc/file missing at pre-restructure flat path | 36 | BLOCKED — operator ruling |
| D14 | misc drift (README pinned text, spine docs, timeouts) | 46 | BLOCKED — operator ruling |
| D13 | review-zip / evidence packaging drift | 11 | BLOCKED — product change |
| D5 | CLI requires a registered project (cwd coupling) | 11 | BLOCKED — product change |
| D3 | apps/ui `legacy/*.tsx` absent | 10 | BLOCKED — unbuilt UI |
| D6 | incomplete MagicMock vs real comparison | 9 | BLOCKED — test rewrite |
| D4 | `.agent` state-file content contracts | 9 | BLOCKED — see risk below |
| D10 | discover-commands CLI rc=1 / non-JSON | 8 | BLOCKED — product bug |
| D7 | dev_server private names removed | 6 | BLOCKED — product change |
| D8 | flight-plan `schema_v` regression | 3 | BLOCKED — product bug |
| D11 | malformed TOML raises BudgetConfigError | 3 | BLOCKED — product change |
| D9 | command-catalog classification drift | 3 | BLOCKED — product change |
| D12 | `.claude/agents/remedy-reviewer.md` absent | 1 | BLOCKED — operator ruling |

## Current Step
STOP-ON-RED handback after S2. S3/S4/S5 not started: every standing-red
class needs product-code change beyond a hermetic-test seam, or a
quarantine of genuinely-red tests — both excluded by T1_F251.md.

## Risks
- R-0150 candidate: PR #157 took `docs/roadmap/features/` 250 → 251 and
  broke two pins in tests/docs/test_docs_consistency.py (TOTAL_FEATURES).
- D4 couples tests to live `.agent/*.md`, so worker edits move the suite.
