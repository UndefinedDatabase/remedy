# Handoff — F269 Contract & contract templates · Round 8 (T005 the remainder proposal)

## Session

SESSION 1 of feature F269 · round 8 · rounds so far 8

Context self-assessment: the round fit in one worker context with room to spare; every gate below was run in this session at C3 `66f59171`, none carried over from memory.

## Range

Review of 5fac20d6..HEAD — branch `feature/f269-contract`.

## Summary

Round 8 lands DECISION F269 D9 (T005):

- C1 books round 7's verdict (ledger), appends DECISION F269 D9, writes the round 8 plan, and saves the payloads (ledger, decisions, plan) and the block.
- C2, D9 (1) and (3)'s two functions, in `packages/orchestration/mission_contract.py`. NEW `CONTRACT_REMAINDER_MARKER = "[contract remainder]"`, `CONTRACT_REMAINDER_YES = "yes"`, `CONTRACT_REMAINDER_OPTIONS = ("yes", "no")`, `contract_blocking_criteria(contract)` (the criteria `contract_blockers` names, in order) and `contract_remainder_order(mission_id, blockers)` = `Meet the acceptance criteria mission <id> left unmet: <text>; <text>.`
  - NEW `raise_contract_remainder_decision(project_id, mission_id, *, root=None, now=None) -> str | None`. It returns None when the contract has no blockers, or when an OPEN decision on any of the mission's jobs (`orchestrator_loop.open_mission_decisions`) has a question starting with the marker, or when the mission has no linked job, the latest job cannot be read, or that job has no task. Otherwise it calls `escalation.enqueue_task_decision` on the latest linked job's first task and then `save_job_plan`. The decision's question is `[contract remainder] Mission <id> stopped at its budget with <n> blocking acceptance criteria not met — C002: <text>; C003: <text>. Start a follow-up mission to meet them?`, with options `yes`/`no`, `safe_default` "" and `impact` = the prefilled order. It returns the decision id.
  - NEW `start_remainder_follow_up_mission(job_id, record, *, root=None, now=None) -> str | None`. It acts only when the record's question starts with the marker, its status is `answered` and its answer is exactly `yes`. It finds the mission through `mission_state.mission_for_job` and reads that mission's current blockers. It then creates a mission in the same project whose goal and `order.text` are the record's `impact`. The new mission's contract is the blockers in order, renumbered from `C001`, keeping text, blocking, origin and check, with `milestones` = (), status `open`, no evidence, template null and no amendments. It returns the new mission's id. Anything else creates nothing and returns None.
- C3, D9 (2) and (3)'s call sites.
  - `orchestrator_loop.run_mission`, at its `iteration_limit` exit, calls `raise_contract_remainder_decision(pid, mission_id, root=root, now=now)`. When a decision is raised it appends `; blocking contract criteria are not met, so remainder decision <id> was raised` to `result.detail`. A `ContractError` appends `; no remainder decision was raised: <error>` instead of raising.
  - `do_sequence`: NEW `do_budget_stop_remainder(ctx, job)`, called in `_step_run`'s not-completed branch. When the job's `stop_source` is `budget` and the walk has a mission, it raises the decision. It then appends `remedy decision resolve <full job id> <decision id> --reason yes` to the Next lines and `; its budget stopped it with blocking contract criteria open, so remainder decision <id> was raised` to the run step's detail. The step still reports `failed`, as it did before.
  - The CLI door, the `td:` branch of `apps/cli/commands/decision.py::_cmd_decision_resolve`: after the answer is saved and the existing lines are printed, it calls `start_remainder_follow_up_mission`. With an id it prints `Follow-up mission <id> started with the unmet criteria as its contract.` and `  Next: remedy mission plan <id>`. A `ContractError` or `MissionError` prints an error and exits 1, and the answer stays recorded.
  - The cockpit door, `ui_server._RemedyHandler._dispatch_decision_resolve`: after `save_job_plan`, it calls the same function and adds `follow_up_mission_id` to the accepted body when a mission was started. `TestCommandDoorImportGuard.ALLOWED_IMPORTS` gains exactly `("packages.orchestration.mission_contract", "start_remainder_follow_up_mission")  # F269 D9`.

## Commits

### a6045b51 F269 R8 C1: bookkeeping — round 7 verdict, DECISION F269 D9, the round 8 plan and payloads
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f269-r8-block.md` | +97 / -0 | Byte copy of block.md |
| `.agent/authored/f269-r8-decisions.md` | +41 / -0 | Byte copy of decisions.md |
| `.agent/authored/f269-r8-ledger.md` | +2 / -0 | Byte copy of ledger.md |
| `.agent/authored/f269-r8-plan.md` | +26 / -0 | Byte copy of plan.md |
| `.agent/decisions.md` | +41 / -0 | `5fac20d6` bytes + decisions.md (D9) |
| `.agent/live_review.md` | +2 / -0 | `5fac20d6` bytes + ledger.md (Gate F269 R7 PASS) |
| `.agent/plan.md` | +9 / -7 | := plan.md |

### 859f114e F269 R8 C2: the remainder decision is raised once per open remainder naming every blocker, and a yes to it starts the follow-up mission with the blockers as its contract
| Path | +/- | Reason |
|------|-----|--------|
| `packages/orchestration/mission_contract.py` | +148 / -0 | NEW remainder section: the three constants, `contract_blocking_criteria`, `contract_remainder_order`, `raise_contract_remainder_decision` and `start_remainder_follow_up_mission`. The module docstring names D9 |
| `tests/orchestration/test_mission_contract.py` | +191 / -0 | NEW fixture helper `_remainder_mission`: four criteria, where C001 is met, C002 is a blocking open planner criterion scoped to M1, C003 is blocking, unmet and compiled, and C004 is advisory; plus one linked job with one task. NEW `TestTheRemainderDecision`: (1) two blockers give one decision on the job's first task, whose question starts with the marker, names the mission and `C002: …` and `C003: …` but not C001 or C004, with options `["yes","no"]`, safe default `""` and the exact prefilled `impact`; (2) a second raise while it is open returns None, and the job still holds one record; (3) no blockers returns None and writes nothing; (4) no job returns None. NEW `TestTheRemainderAnswer`: (5) `yes` creates a second mission whose goal and order are the impact and whose criteria are exactly `C001` (C002's text, planner) and `C002` (C003's text, template), whole-mission, `open`, no evidence, with C002's check relabelled; (6) `no`, (7) `yes please` and (8) a non-remainder decision answered `yes` each create nothing. `from dataclasses import replace` is added, and the docstring names D9 |

### 66f59171 F269 R8 C3: the loop's iteration limit and a do job's budget stop raise the remainder decision, and a yes at either answer door starts the follow-up mission
| Path | +/- | Reason |
|------|-----|--------|
| `packages/orchestration/orchestrator_loop.py` | +20 / -1 | `run_mission` raises the remainder decision at `iteration_limit` and names it in the detail. The docstring is updated |
| `packages/orchestration/do_sequence.py` | +34 / -1 | NEW `do_budget_stop_remainder`, called in `_step_run`'s not-completed branch. The module docstring names D9 (2) (deviation 2) |
| `apps/cli/commands/decision.py` | +18 / -0 | The `td:` branch calls `start_remainder_follow_up_mission` and prints the follow-up id and `remedy mission plan <id>` |
| `packages/orchestration/ui_server.py` | +16 / -2 | `_dispatch_decision_resolve` calls the same function and returns `follow_up_mission_id`. The docstring names the one mission this door creates |
| `tests/orchestration/test_mission_gate.py` | +123 / -0 | NEW `TestTheRemainderAtBudgetEnd`, THE ACCEPTANCE TEST. It uses the `planned` fixture's three-criterion contract, where C003 can never pass; the real `dod_gate.run_job_gate` in the tmp `workdir` through the `execute` seam; an `evidence` seam that reports what that gate decided; a scripted orchestrator (dispatch M001, declare M001 done, declare achieved); and `LoopLimits(max_iterations=3)`. (1) The run ends `iteration_limit`; the one refused entry is `declare_mission_achieved`, whose detail reads `blocking contract criteria are not met: C003`; the statuses are C001 and C002 `met` and C003 `unmet`; exactly one open remainder decision names `C003: tests/test_c.py passes` and not C001 or C002; and the result detail names its id. (2) `main(["decision","resolve",<job>,<id>,"--reason","yes"])` exits 0 and prints `Follow-up mission <id> started` and `remedy mission plan <id>`. The follow-up's contract is exactly `[("C001","tests/test_c.py passes","open")]`, its order is the impact, and no remainder decision is left open |
| `tests/ui_server/test_command_channel.py` | +48 / -0 | `ALLOWED_IMPORTS` gains the one D9 entry. NEW `test_yes_to_a_contract_remainder_decision_starts_the_follow_up_mission`: a real server, a job linked to a mission with one unmet blocker, the decision raised, and a `yes` POST. The response is 200 with keys `command, decision_id, follow_up_mission_id, outcome`, and the follow-up's contract is exactly the unmet criterion |
| `tests/cli/test_do_sequence_cli.py` | +34 / -0 | NEW `test_a_job_its_budget_stops_with_blockers_raises_the_remainder_and_names_its_answer`: `do --json --contract cli-tool --deadline 2000-01-01T00:00:00+00:00` exits 1; the job is not completed, with `stop_source` `budget` and `stop_reason` `budget_exhausted:deadline`; the run step's detail names the raised decision; that decision's question starts with the marker and names every id in `unmet_blocking_criteria`; and `next` holds `remedy decision resolve <job> <id> --reason yes` (deviation 2) |

### C4 (this commit) F269 R8 C4: handoff
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/handoff.md` | rewrite | This file |

Existing tests whose pinned behaviour D9 changes: only `TestCommandDoorImportGuard.ALLOWED_IMPORTS` in `tests/ui_server/test_command_channel.py`, which gains the one ruled import. Its property, that the door imports exactly the ruled set, is kept by the equality test. No other existing test changed or needed to: G2 read 0 failed with the rest untouched.

## External actions

- For G4, first attempt: `git worktree add --detach .remedy-wt/f269-r8-g4 66f59171`, then `git worktree remove --force`. Its control was red (deviation 3).
- Diagnosis: `git worktree add --detach .remedy-wt/f269-r8-g4diag 66f59171`, then removed.
- For G4, second attempt (the one reported): `git worktree add --detach .remedy-wt/f269-r8-g4 66f59171`, then `git worktree remove --force`. `git worktree list` afterwards: `/home/decodeux/Repos/remedy  66f59171 [feature/f269-contract]`.
- `git push` runs after this commit. Its outcome and G5 are in the worker's final report.
- No PR was created, edited or merged.

## Verification

All gates ran at C3 `66f59171` with a clean tree. The scripts are under `.remedy-wt/f269-r8/`, and each exit code is a subprocess return code (`gate.py` wraps a command and prints `[exit code N]`).

G1 transport + state, `python3 .remedy-wt/f269-r8/gate.py python3 .remedy-wt/f269-r8/g1.py`:
```
payload digests match: True
authored copies equal payloads: True
plan.md equals payload: True
live_review.md equals base + ledger: True
decisions.md equals base + decisions: True
[exit code 0]
```

G2, `python3 .remedy-wt/f269-r8/g2.py`, runs `python3 -m pytest -q -p no:cacheprovider` over the block's list verbatim. The four test files this round edited (`test_mission_contract.py`, `test_mission_gate.py`, `test_command_channel.py`, `test_do_sequence_cli.py`) are all in it, and it creates no new test file:
```
1422 passed in 107.69s (0:01:47)
exit 0
```

G3, `python3 -m ruff check` over the 9 `.py` files C2 and C3 touched (`packages/orchestration/{mission_contract,orchestrator_loop,do_sequence,ui_server}.py apps/cli/commands/decision.py tests/orchestration/{test_mission_contract,test_mission_gate}.py tests/ui_server/test_command_channel.py tests/cli/test_do_sequence_cli.py`):
```
All checks passed!
[exit code 0]
```

G4 mutation red-proofs, `python3 .remedy-wt/f269-r8/gate.py python3 .remedy-wt/f269-r8/g4.py`. It runs in one worktree at C3 and uses `python3 -B -m pytest -q -p no:cacheprovider` from the worktree root, over `tests/orchestration/test_mission_contract.py tests/orchestration/test_mission_gate.py tests/ui_server/test_command_channel.py tests/cli/test_do_sequence_cli.py`. `__pycache__` is purged before each run. Each mutation is reverted with `git checkout -- <path>`, and the script asserts a clean `git status` after each revert.
```
mission_contract resolves to: /home/decodeux/Repos/remedy/.remedy-wt/f269-r8-g4/packages/orchestration/mission_contract.py
warm-up (one cockpit start): 1 passed in 4.53s [exit code 0]
control (unmutated): 278 passed in 55.84s [exit code 0]
(a) the raise ignores an open remainder decision: 1 failed, 277 passed in 55.18s [exit code 1]
    FAILED tests/orchestration/test_mission_contract.py::TestTheRemainderDecision::test_a_second_raise_while_it_is_open_returns_none
(b) the actor acts on any answer, not only yes: 2 failed, 276 passed in 55.42s [exit code 1]
    FAILED tests/orchestration/test_mission_contract.py::TestTheRemainderAnswer::test_no_creates_nothing
    FAILED tests/orchestration/test_mission_contract.py::TestTheRemainderAnswer::test_another_answer_creates_nothing
(c) run_mission raises nothing at iteration_limit: 2 failed, 276 passed in 56.80s [exit code 1]
    FAILED tests/orchestration/test_mission_gate.py::TestTheRemainderAtBudgetEnd::test_the_run_ends_blocked_with_one_remainder_decision_naming_the_criterion
    FAILED tests/orchestration/test_mission_gate.py::TestTheRemainderAtBudgetEnd::test_yes_at_the_cli_starts_the_follow_up_mission_holding_the_unmet_criterion
worktree removed
/home/decodeux/Repos/remedy  66f59171 [feature/f269-contract]
[exit code 0]
```
The mutation texts were:
- (a): the three lines `if any(... .startswith(CONTRACT_REMAINDER_MARKER) for record in open_mission_decisions(mission)): return None` are deleted.
- (b): `if (record.get("status") != ESCALATION_STATUS_ANSWERED or record.get("answer") != CONTRACT_REMAINDER_YES): return None` becomes `if record.get("status") != ESCALATION_STATUS_ANSWERED: return None`.
- (c): `remainder = raise_contract_remainder_decision(pid, mission_id, root=root, now=now)` becomes `remainder = None`.

Full suite: not run (amend0917-throughput).

## Authored-text proofs

In G1 above, each of the four payloads matches its block digest and is byte-equal to its `.agent/authored/f269-r8-*` copy. `.agent/plan.md`, `.agent/live_review.md` and `.agent/decisions.md` equal their ordered construction.

## Deviations & assumptions

1. The follow-up's checks are RELABELLED. D9 (3) says each blocker is copied "with its … check". The copied check keeps its kind, spec and every other field. Its `id` and `acceptance_refs`, however, become `ctr-<new id>` and `[<new id>:0]`, so that D4 (1)'s link from check to criterion holds in the new contract rather than naming an id that is not in it (C2's test (5) pins this). The follow-up's `template` is null, because D9 names the criteria and nothing else.
2. `do`'s rule reads `stop_source`, not the state. D9's CONTEXT measured that "a `do` job stopped by its budget ends `stopped` with `stop_source` budget". Measured this round, `run_job`'s pre-work budget stop for a deadline already past leaves the job `planned` with `stop_source` `budget` and `stop_reason` `budget_exhausted:deadline`. So `do_budget_stop_remainder` raises for any job that did not complete and whose `stop_source` is `budget`. The `do` test uses that real path, because the fake builder and reviewer report no provider calls or tokens: `--max-provider-calls 1` and `--max-total-tokens 1` both let a three-task job complete (probed; not committed).
3. G4 ran twice. In the first attempt, the unmutated control read `1 failed, 277 passed` (exit 1), with `tests/ui_server/test_command_channel.py::TestCommandChannelDoor::test_post_to_non_commands_path_is_405` failing, and each mutation run passed that same test. Diagnosis: in a fresh worktree, the first cockpit start builds `apps/ui/dist` (one run of that test took 4.63s cold and 0.40s warm), and a cold start can outlast the test's five-second server-start wait. The reported attempt runs that one test once as a declared warm-up (not the control) and then the unmutated control, which read `278 passed` (exit 0). The first attempt's mutation readings matched the reported ones.
4. At the CLI door, the existing `Resume the run: remedy job resume …` line still prints before the follow-up lines for every `td:` answer. D9 adds lines and removes none. The `do` run step still reports `failed` for a budget-stopped job, so `do` exits 1 as before.
5. Observations for the reviewer, not changed:
   - (a) A blocker whose origin is `planner` is copied with that origin, as D9 rules. `remedy mission plan <follow-up>` then replaces every planner criterion (`write_planner_criteria`, D4 (2)), so such a blocker survives only as the new plan's milestones.
   - (b) At the cockpit, a `ContractError` or `MissionError` raised while starting the follow-up, after the answer was saved, takes D18 clause four's `rejected_effect` 500 while the answer stays recorded.
   - (c) No docs page describes the remainder decision. The plan's next step 2 (the Built State and docs) owns that, and the change set excludes `docs/`.

| Item | Status | Reason |
|------|--------|--------|
| C1 bookkeeping | done | |
| C2 raise + act | done | deviation 1 |
| C3 call sites + acceptance test | done | deviation 2, 4 |
| G1 to G4 at C3 | done | deviation 3 |
| C4 handoff + push | done | |

## Next

1. Phase 1 rule 1: check `.agent/STOP`.
2. Then the review of round 8 (D9: the remainder decision, its raise at the loop's iteration limit and at a `do` job's budget stop, and `yes` at both answer doors), with its verdict booked in the next round's first commit.
3. Then the closure sequence: the Built State of `docs/roadmap/features/T2_F269.md` and any docs page the shipped commands need, the integration-gate suite once, evidence, package, STATUS.

Operator questions open: 5
