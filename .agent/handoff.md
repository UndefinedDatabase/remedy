## Range

Review of 78f5f608..HEAD (branch feature/f056-missions)

## Commits

### 0eefae30 chore(f056): claim STATUS, reset live review, reset agent state
| Path | +/- | Reason |
|---|---|---|
| docs/roadmap/STATUS.md | +1/-1 | F056 claimed `[~]` (authored, byte-copy) |
| .agent/live_review.md | +21/-39 | full replacement (authored, byte-copy) |
| .agent/authored/f056-r1-{1,2}.md | +26 | the two authored texts, saved verbatim |
| .agent/{plan,context}.md | +90/-114 | rewritten for feature+branch (R-0162) |
| .agent/last_block.md | +153/-49 | received block verbatim, OUTCOME pending |

### 97ee09d4 feat(f056): add the mission record and its project-scoped store
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/mission_state.py | +365 | record, store, listing, goal immutability |
| packages/orchestration/data_paths.py | +9 | missions_dir(), the queue_dir convention |

### 0c0a3233 test(f056): cover the record, listing order and goal immutability
| Path | +/- | Reason |
|---|---|---|
| tests/orchestration/test_mission_state.py | +228 | round-trip, order, scoping, corruption, immutability |

### f94f135c feat(f056): link jobs into a mission chain and render it
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/mission_state.py | +155/-2 | link validators, status, id resolve, rendering |
| tests/orchestration/test_mission_state.py | +227 | both validators, missing/unreadable job labels |

### eedda00b feat(f056): wire remedy mission start, list and show
| Path | +/- | Reason |
|---|---|---|
| apps/cli/commands/mission_cmd.py | +174 | three handlers, F148 scoping, --json |
| apps/cli/command_catalog.py, commands/__init__.py | +43/-2 | mission.start/list/show, group description, registration |
| tests/cli/test_mission_cmd.py | +282 | catalog, scoping, corruption, missing job |

### ee1a738f feat(f056): offer the mission opt-in in the approval, defaulting to no
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/schemas/models.py | +5 | JobIntake.mission_candidate (additive) |
| packages/orchestration/intake.py | +33/-1 | phrase heuristic + prompt line |
| packages/orchestration/decision_queue.py | +20/-1 | mission_offer on the existing fp:approval |
| apps/cli/commands/decision.py, command_catalog.py | +79/-1 | --as-mission opt-in, its refusals, show rendering |
| tests/{orchestration,cli}/test_mission_*.py | +299 | offer/hint tests + negative do-flow proof |

### 945ff11b feat(f056): inject the verify task a follow-up plan must begin with
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/mission_state.py | +302/-1 | build/inject/assert verify-first, runner, record |
| tests/{orchestration/test_mission_state,cli/test_mission_cmd}.py | +154/-5 | structure via dag_schedule, runner outcomes |

### 8518c074 feat(f056): add mission continue and the verify-first execution path
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/mission_state.py | +154 | continue_mission, execute_mission_followup |
| apps/cli/commands/mission_cmd.py, command_catalog.py | +69/-4 | mission.continue and its handler |
| tests/cli/test_mission_cmd.py | +90 | continue surface + refusals |

### decd970e + c9077a31 (tests only)
| Path | +/- | Reason |
|---|---|---|
| tests/orchestration/test_mission_state.py | +187/-14 | decd970e: two-job fixture end to end |
| tests/cli/test_worker_facade_cmd.py | +8/-4 | c9077a31: facade guard by name, not group size |

## External actions

`gh pr list --state open --json number,headRefName,baseRefName,isDraft` -> `[]`; nothing merged. `git checkout main && git pull` -> already up to date at 78f5f608; `git checkout -b feature/f056-missions`.
No push, no PR, no merge, no worktree — SPLIT round.

## Verification

    pytest tests/docs/ -q         (state commit, and again at round close)  293 passed  exit 0
    pytest tests/orchestration/test_mission_state.py tests/cli/test_mission_cmd.py -q
        T001 gate 64 passed exit 0  ·  T003 gate (same command) 117 passed exit 0
    T002 gate: that command plus tests/schemas/test_job_intake.py, tests/test_command_catalog.py,
        tests/orchestration/{test_intake,test_bundled_clarification}.py,
        tests/cli/{test_plan_approval,test_decision_answers}.py -q      260 passed  exit 0
    pytest tests/cli/test_golden_path.py -q   (canary)           42 passed  exit 0
    pytest -n auto -q   (full suite)      14727 passed, 19 skipped          exit 0
    git status --porcelain -> empty

## Authored-text proofs

- f056-r1-1: `sha256sum` of the saved file = 617f083e…1ca0dd, matches its BEGIN marker. Its bytes occur in docs/roadmap/STATUS.md exactly once (disk-to-disk substring check).
- f056-r1-2: `sha256sum` = 0fc3cbd8…7c95593, matches. `cmp .agent/live_review.md .agent/authored/f056-r1-2.md` -> identical.

## Deviations & assumptions

- A9: achieve/abandon/pause CLI subcommands NOT added — the ordered CLI list was start/continue/list/show. `set_mission_status` exists and is tested; the transition surface awaits a reviewer order.
- A9: a previous job with no recorded verification does NOT block the follow-up; it is recorded `unverifiable` and named in the message, never as a pass. Blocking would make the path unusable on pre-F056 jobs.
- A9: `execute_mission_followup` never marks work COMPLETED itself; a caller-supplied `work_runner` does. Running follow-up work is the orchestrator loop's job (out of scope).
- The `mission` group keeps `user_facing=False`; only its description changed — help visibility was not ordered. In-scope repair: tests/cli/test_worker_facade_cmd.py asserted that group holds exactly 2 commands; it now guards the facade's two entries by name.
- Pre-existing, untouched: ruff UP035 in packages/orchestration/dag_schedule.py. No commit exceeds the 500-line cap — the bundle is 9 commits for that reason.

## Next

Reviewer gates R1 (Review of 78f5f608..HEAD).
