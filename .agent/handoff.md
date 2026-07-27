# Handoff — F048 Job queue · round 2 (verdict + T003 + integration gate)

## Range
Review of `7f05857..HEAD` — 6 commits.

## Commits
### fd2e21d chore(f048): persist the R1 PASS verdict
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f048-r2-1.md | +30 | authored verdict text, sha256-verified before use |
| .agent/live_review.md | +20 −8 | full replace from the authored file (cmp exit 0) |
| .agent/plan.md | +33 −35 | rewritten for round 2 |

### 61e664f feat(f048): remedy queue add/list/rm (T003a)
| Path | +/- | Reason |
|---|---|---|
| apps/cli/commands/queue_cmd.py | +215 | new queue group handlers |
| apps/cli/command_catalog.py | +38 | queue group + add/list/rm entries |
| apps/cli/commands/__init__.py | +3 −1 | handler registration |
| packages/orchestration/job_queue.py | +49 −7 | remove_entry, QueueEntryClaimedError, queue_root via data_paths |
| packages/orchestration/data_paths.py | +9 | queue_dir() promotion (round-1 deferral) |

### ed3e2ca test(f048): CLI tests for queue add/list/rm (T003a)
| Path | +/- | Reason |
|---|---|---|
| tests/cli/test_queue_cmd.py | +279 | 21 subprocess tests over the real grouped CLI |

### 042d740 feat(f048): explicit queue reclaim, TTL- and pid-gated (T003b)
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/job_queue.py | +145 | reclaim(), ReclaimRefusedError, TTL resolution, owner probe |
| packages/orchestration/config.py | +12 | queue.reclaim_ttl_minutes (default 60) |
| apps/cli/commands/queue_cmd.py | +27 | queue reclaim handler |
| apps/cli/command_catalog.py | +12 | queue.reclaim entry |
| tests/orchestration/test_job_queue.py | +126 | 8 reclaim tests |
| tests/cli/test_queue_cmd.py | +58 | 3 CLI-level reclaim tests |

### 37da8c6 feat(f048): opt-in executor binding (T003c)
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/long_run_executor.py | +144 −1 | QueuePull, queue_binding_enabled, queued_entry_to_job, idle seam |
| packages/orchestration/config.py | +13 | queue.executor_binding (default false) |
| tests/orchestration/test_queue_executor_binding.py | +188 | 9 end-to-end tests |

### handoff commit (self-reference, R-0149 grouped table)
| Path | +/- | Reason |
|---|---|---|
| .agent/{handoff,plan}.md | rewrite | this file; plan ticks T003a-c, canary, gate |

## External actions
- `git worktree add <scratch>/base_wt 40c7e4d` for the gate base run; removed with `git worktree remove --force` + `git worktree prune`; `git worktree list` now shows only the repo. Both run logs live in the session scratchpad, outside the repo.
- `git push` of feature/f048-job-queue. NO PR, no STATUS `[x]`, no evidence job, no zip — closure is its own round.

## Verification
    pytest tests/cli/test_queue_cmd.py -q                    → 21 passed, exit 0   (T003a)
    pytest tests/orchestration/test_job_queue.py -q          → 34 passed, exit 0   (T003b, incl. 8 reclaim)
    pytest tests/orchestration/test_queue_executor_binding.py → 9 passed, exit 0   (T003c)
    pytest tests/cli/test_golden_path.py -q                  → 42 passed, exit 0   (canary)
    pytest tests/orchestration/test_long_run_executor.py -q  → 49 passed, exit 0   (F046/F047 regression)
    ruff check (every touched file)                          → All checks passed

INTEGRATION GATE — `python3 -m pytest -n auto -q`, per docs/agents/integration_gate.md:

    branch (HEAD)      159 failed, 14147 passed,  8 skipped in 183.61s   exit 1  (wall 184.08s)
    base   (40c7e4d)   201 failed, 14017 passed, 15 skipped, 1 error in 172.52s  exit 1  (wall 172.98s)

`comm -13` branch-only ids: **7**, all runtime/supervisor/probe. Serial re-run of every one: **7/7 PASS** → xdist-flake class (F135/F052), recorded, not a blocker. `comm -23` (failing on base, not on branch): 49 — the same flake population in the other direction; the suite is noisy at this concurrency in both runs. No F048 test id appears in either failure list. The pre-existing `tests/test_command_catalog.py` classification failures are base failures about `do.job-evidence` / `do.repair-attest`, untouched by this round.

## Authored-text proofs
- f048-r2-1.md sha256 `a3337bd…4e807` = BEGIN marker; `cmp .agent/live_review.md .agent/authored/f048-r2-1.md` → exit 0.

## Deviations & assumptions
- **A9 reclaim semantics**: a claim is re-offered only when BOTH the claim is older than `queue.reclaim_ttl_minutes` (default 60) AND the owner is verifiably gone — the owner id names THIS host and its pid is dead. Deliberate refusals: an owner on another host is never declared gone; `PermissionError` from `kill(pid,0)` counts as alive; an unparsable `host#pid` or an unparsable `claimed_at` refuses, because an age that cannot be proven is not an old age. No code path anywhere reclaims on a timer (P2).
- **A9 binding semantics**: the pulled entry becomes what `job create` + `job plan` produce and STOPS at PLANNED. No task is executed and nothing implies `--yes`, so approval rules are untouched by construction. The binding fires only at the idle terminals (`all_green`, `blocked`) and only for the job's own project.
- **A9 add heuristic**: `queue add` treats an argument as a goal-file path only when that file EXISTS; `--path` forces it. A sentence containing a slash stays goal text.
- `--all-projects` widens the LISTING only, over the project directories on disk (including queues whose project was unregistered — hiding them would be dishonest). There is still no cross-project queue.
- `tests/conftest.py` SUBPROCESS_FILES was NOT extended: the new subprocess tests already collect and pass under their default `integration` mark, so the edit was unnecessary rather than deferred.
- `CycleLoopResult.to_json()` gains the `queue_pull` key ONLY when a pull happened, so the default payload shape every existing reader parses is unchanged.

## Next
Window 1 reviews `7f05857..HEAD` and issues the gate verdict. Closure (STATUS `[x]`, evidence job, zip, PR) is its own reviewer-gated round.
