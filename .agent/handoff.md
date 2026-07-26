# Handoff — F046 Multi-cycle loop — Integration gate

Branch: feature/f046-multi-cycle-loop · PR #152 · base main `c14a83a`
Review range: `d87a3e0..HEAD` · LAST_REVIEWED_SHA `d87a3e0`
Gate result: **PASS** — zero F046-attributable regressions.
Open findings: 0. Next expected action: reviewer verdict on the gate, then
closure (not part of this step).

## Item status

| Item | Status | Reason |
|------|--------|--------|
| 0 — Persist round-1 verdict | done | 1055ae0 (verbatim, own commit) |
| 1 — Integration gate (branch vs base, attribution) | done | this handoff |
| — plan.md `## Next Steps` restored | deviated | fixes the only 2 reproducible branch-only failures; state-file-only, AGENTS.md requires the section (see below) |

## Commits this round

**1055ae0** chore(f046): persist the round-1 reviewer verdict; open the integration gate

| file | +/- |
|------|-----|
| .agent/live_review.md | +21 −2 |
| .agent/plan.md | +2 −4 |

**HEAD** chore(f046): integration-gate results; restore plan.md Next Steps

| file | +/- |
|------|-----|
| .agent/plan.md | +4 −0 |
| .agent/decisions.md | +11 −0 |
| .agent/handoff.md | rewritten |

## Run 1 — branch (`1055ae0`)

```
$ python3 -m pytest -n auto -q
... (184 FAILED lines)
184 failed, 13962 passed, 8 skipped in 161.28s (0:02:41)
EXIT=1
```

## Run 2 — base (`c14a83a`, throwaway worktree)

```
$ git worktree add /tmp/f046-base c14a83a
Preparing worktree (detached HEAD c14a83a)
HEAD is now at c14a83a Merge pull request #151 ...

$ (cd /tmp/f046-base && python3 -m pytest -n auto -q)
... (179 FAILED lines)
179 failed, 13912 passed, 14 skipped in 196.88s (0:03:16)
EXIT=1
```

Worktree removed, proven:

```
$ git worktree remove /tmp/f046-base && git worktree list
/home/decodeux/Repos/remedy  1055ae0 [feature/f046-multi-cycle-loop]
```

## Failure-set diff

| set | count |
|-----|-------|
| branch failures | 184 |
| base failures | 179 |
| branch-only | 30 |
| base-only | 25 |

Churn in both directions (30 appear, 25 disappear) with no code path in
common is the signature of the known xdist nondeterminism, not of a
regression: the branch adds 50 net passes and 5 net failures across a
14k-test suite whose failure set is unstable run to run.

## Attribution — all 30 branch-only failures

Serial re-run on the branch, all 30 in one command:

```
$ python3 -m pytest <30 node ids> -q
2 failed, 28 passed in 7.23s
```

| # | branch-only failure | serial | coupled to F046? |
|---|---------------------|--------|------------------|
| 1–2 | `cli/test_runtime_cmd.py` TestProbe/TestServe timeouts | pass | no — pre-existing xdist flake (F135/F052) |
| 3 | `orchestration/test_self_dogfood.py::…::test_roadmap_items_cite_evidence` | pass | no — same class (checked because F046 edits STATUS.md; green serially and on re-run) |
| 4–13 | `orchestration/test_task_execution.py::TestModularArchitectureGuards` (10) | pass | no — same class |
| 14–17 | `regression/test_named_bugs.py` (4) | pass | no — same class |
| 18–21 | `runtimes/` probe / dev-server / process-boundary (4) | pass | no — same class |
| 22 | `test_data_paths.py::…::test_default_ends_with_data` | pass | no — same class |
| 23–26 | `test_grouped_cli.py::TestGroupedExecution` json (4) | pass | no — same class |
| 27 | `ui_server/test_dashboard_contract.py::TestAgentStateFilesCurrentBranch::test_plan_md_references_current_steps` | **FAIL (reproducible)** | no F046 module — caused by `.agent/plan.md` |
| 28 | `ui_server/test_dashboard_contract.py::TestLiveReviewAndAgentStateRefs::test_plan_md_references_current_steps` | **FAIL (reproducible)** | no F046 module — same cause |
| 29–30 | `ui_server/test_dashboard_contract.py::TestUIServer` no-shell / no-external-assets | pass | no — same class |

None of the 30 touches `long_run_executor.py`, `config.py`,
`apps/cli/commands/job.py` or `command_catalog.py`. No BLOCKER.

### The 2 reproducible ones, and the fix

Both assert `"Steps" in .agent/plan.md`. The F046 plan.md rewrite dropped the
`## Next Steps` section that AGENTS.md ("plan.md must contain: Goal, Current
Step, Next Steps") and these two tests both require; the base plan.md (F034)
still had it, which is exactly why the failures are branch-only. Fix is a
state-file edit — permitted this round, no production code touched.

Branch after the fix, same two classes, side by side with base:

```
$ python3 -m pytest tests/ui_server/test_dashboard_contract.py::TestAgentStateFilesCurrentBranch \
                    tests/ui_server/test_dashboard_contract.py::TestLiveReviewAndAgentStateRefs -q
3 failed, 4 passed in 0.10s
FAILED …TestAgentStateFilesCurrentBranch::test_context_md_references_current_branch
FAILED …TestLiveReviewAndAgentStateRefs::test_live_review_has_steps_section
FAILED …TestLiveReviewAndAgentStateRefs::test_context_md_no_stale_steps

$ (cd /tmp/f046-base && python3 -m pytest <same two classes> -q)
3 failed, 4 passed in 0.09s
FAILED …TestAgentStateFilesCurrentBranch::test_context_md_references_current_branch
FAILED …TestLiveReviewAndAgentStateRefs::test_live_review_has_steps_section
FAILED …TestLiveReviewAndAgentStateRefs::test_context_md_no_stale_steps
```

Identical: same 3 failures, same 4 passes. Those 3 are pre-existing on base
(context.md wants a `## Active Branch` heading and the word "Steps";
live_review.md wants "Steps"). They are NOT F046-attributable and were left
alone rather than swept up — a gap item for the backlog, not this round.

## Canary

```
$ python3 -m pytest tests/cli/test_golden_path.py -q
..........................................                               [100%]
42 passed in 18.82s
exit=0
```

## Runtime budget (§3.4)

Branch 161.28s (2:41), base 196.88s (3:16). Both under the ~5 min threshold;
no perf pass needs scheduling. The base run being 35s slower than the branch
is machine noise, not a branch effect.

## Residual risks carried forward

- Pre-existing full-suite nondeterminism (F135/F052): 30 branch-only and 25
  base-only failures churned between two runs of the same suite.
- 3 pre-existing `.agent` state-file contract failures (context.md ×2,
  live_review.md ×1) fail identically on base and branch — backlog gap item.
- From the round-1 verdict: no per-terminal postmortem record is written by
  the conductor itself; the multi-cycle CLI branch is unreachable while
  `CYCLE_SAFETY_CAP == 1`.
