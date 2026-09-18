# Handoff — F269 Contract & contract templates · Round 6 (the writer and the deletion)

## Session

SESSION 1 of feature F269 · round 6 · rounds so far 6

Context self-assessment: the round fit in one worker context with room to spare; every gate below was run in this session at C4 `c73ccc6d`, none carried over from memory.

## Range

Review of c93d117d..HEAD — branch `feature/f269-contract`.

## Summary

Round 6 lands DECISION F269 D7:

- C1 books round 5's verdict (ledger), appends DECISION F269 D7, writes the round 6 plan, and saves the payloads (ledger, decisions, plan, opq) and the block.
- C2 (D7 FIRST): NEW `mission_contract.grant_contract_job_repository(mission, job_id, root=None)`. It writes nothing for a mission with no contract or a job with no readable record. Otherwise it writes `metadata["target_repo"]` := the job's `repo_path`, else the project's `canonical_repo_path`, else nothing, never overwriting a `target_repo` already set, and grants `repo_test_run`, `repo_generated_write`, `repo_revert` (NEW `CONTRACT_JOB_GRANTS`) through `permissions.set_permission`. It returns the metadata entries it wrote. It is called beside `merge_contract_slice_into_dod` in `orchestrator_loop.execute_move`, which copies the returned entries onto the in-memory job the executor saves next (like `record_job_milestone`), and in `do_sequence._step_shape`.
- C3 (D7 SECOND, the deletion): the `job.attach-repo` and `job.permit` catalog entries, `_cmd_attach_repo`, `_cmd_set_permission` and their two dispatch entries are gone. `TestRequiredCommands.REQUIRED` loses both ids and `TestDeletedCommands.DELETED` gains them in sorted position. `TestSetPermissionReservedNotice`, `test_permit_arg_order_correct` and `test_missing_args_shows_command_help` (the `job attach-repo` help case) are deleted. The five fixture setups now write the binding or grant straight onto the job record.
- C4 (D7 SECOND, the heir in every string): every production string under `packages/`, the two smoke-script steps, and the `docs/system/` and `docs/guides/` pages that told a reader to run either command now name the heir: "a job gets its repository and grants from its mission's contract", with `remedy job contract <id>`. `stop_reasons.job_attach_repo_tip` is rewritten as `job_contract_repo_tip` (still naming the real job id and, when there is one, the project's real repository path, per R-0811), with NEW `JOB_GRANTS_HEIR`. The tests asserting that guidance follow it, each keeping its property.
- C5 is this handoff, plus the Q5 operator question.

## Commits

### 8fd84d19 F269 R6 C1: bookkeeping — round 5 verdict, DECISION F269 D7, the round 6 plan and payloads
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f269-r6-block.md` | +98 / -0 | Byte copy of block.md |
| `.agent/authored/f269-r6-decisions.md` | +34 / -0 | Byte copy of decisions.md |
| `.agent/authored/f269-r6-ledger.md` | +2 / -0 | Byte copy of ledger.md |
| `.agent/authored/f269-r6-opq.md` | +10 / -0 | Byte copy of opq.md |
| `.agent/authored/f269-r6-plan.md` | +25 / -0 | Byte copy of plan.md |
| `.agent/decisions.md` | +34 / -0 | `c93d117d` bytes + decisions.md (D7) |
| `.agent/live_review.md` | +2 / -0 | `c93d117d` bytes + ledger.md (Gate F269 R5 PASS) |
| `.agent/plan.md` | +8 / -9 | := plan.md |

### 74ef3825 F269 R6 C2: the contract binds each of its jobs to its repository and grants it the three repository capabilities, at dispatch and in do
| Path | +/- | Reason |
|------|-----|--------|
| `packages/orchestration/mission_contract.py` | +63 / -1 | NEW `CONTRACT_JOB_GRANTS`, `JOB_TARGET_REPO_KEY`, `_project_canonical_repo`, `grant_contract_job_repository`. The module docstring names D7 |
| `packages/orchestration/orchestrator_loop.py` | +6 / -0 | `execute_move` calls the writer after the slice merge and copies the returned entries onto the in-memory job |
| `packages/orchestration/do_sequence.py` | +7 / -2 | `_step_shape` calls the writer after each merge. The docstring names D7 |
| `tests/orchestration/test_mission_contract.py` | +130 / -0 | NEW class `TestTheContractBindsAndGrantsItsJobs`, four tests. (1) A job dispatched through `execute_move` for a contract mission of a registered project has `repo_path == ""`, `target_repo` equal to the project's canonical repository and `is_allowed` True for the three grants, on disk and on the in-memory job the executor received. (2) A `remedy do --plan-only --no-llm` job has `target_repo == repo_path ==` the resolved git repository, and the three grants. (3) A mission with no contract, through `execute_move`, writes neither key and all three grants read False. (4) A `target_repo` already set is kept, and the grants are still written. The module docstring names D7 |

### 4a2d74d5 F269 R6 C3: delete job attach-repo and job permit — catalog, handlers, dispatch, their own tests; fixtures write the binding and grants on the job record
| Path | +/- | Reason |
|------|-----|--------|
| `apps/cli/command_catalog.py` | +0 / -22 | The two catalog entries deleted |
| `apps/cli/commands/job.py` | +0 / -55 | `_cmd_attach_repo`, `_cmd_set_permission` and their two `COMMAND_HANDLERS` entries deleted |
| `apps/cli/commands/job_context_cmd.py` | +2 / -2 | The comment now names `grant_contract_job_repository` instead of `job._cmd_attach_repo` |
| `tests/test_command_catalog.py` | +3 / -1 | REQUIRED loses both ids, and DELETED gains `job.attach-repo` (after `job.assumptions`) and `job.permit` (after `job.permissions`) |
| `tests/test_cli_main.py` | +0 / -52 | `TestSetPermissionReservedNotice` and its two docstring bullets deleted |
| `tests/orchestration/test_autonomy.py` | +0 / -8 | `test_permit_arg_order_correct` deleted |
| `tests/test_grouped_cli.py` | +0 / -8 | `test_missing_args_shows_command_help` (the `job attach-repo` help case) deleted |
| `tests/test_command_discovery.py` | +20 / -4 | NEW `_BIND_TARGET_REPO` snippet. Both `_create_job_with_repo` fixtures write `target_repo` on the record through it and assert its exit code 0 |
| `tests/orchestration/test_test_runner.py` | +16 / -2 | Same snippet. `test_permit_runtime_stderr`'s setup binds through it |
| `tests/test_test_runner.py` | +18 / -4 | NEW `_GRANT_REPO_TEST_RUN` snippet. `test_no_target_repo_exits_1` grants `repo_test_run` through it and asserts its exit code 0 |

### c73ccc6d F269 R6 C4: every string advertising job attach-repo or job permit names the heir — a job gets its repository and grants from its mission's contract
| Path | +/- | Reason |
|------|-----|--------|
| `packages/orchestration/stop_reasons.py` | +10 / -7 | `job_attach_repo_tip` → `job_contract_repo_tip`: `remedy job contract <id> — <heir>`, plus `; its project's repository is <path>` when the project has one. NEW `JOB_GRANTS_HEIR`. Its caller is updated |
| `packages/orchestration/autonomy_readiness.py` | +5 / -4 | The level 1 tip uses `job_contract_repo_tip`. The level 2 and 3 grant tips are `remedy job contract <id> — <heir>` |
| `packages/orchestration/agent_loop.py` | +4 / -2 | The BLOCKED hint names the missing capability, the heir and `remedy job contract <id>` |
| `packages/orchestration/autonomy_loop.py` | +1 / -1 | Level 3's blocked command is `remedy job contract <job_id>` |
| `packages/orchestration/brain_detail.py` | +2 / -1 | The blocker node's first next action is `remedy job contract <id> — ... (<capability>) ...` |
| `packages/orchestration/cockpit.py` | +7 / -6 | Two attention items and the next-action hint name the heir |
| `packages/orchestration/self_dogfood_execution.py` | +2 / -1 | The no-target-repo next safe action is `remedy job contract <id>` |
| `packages/orchestration/test_execution_service.py` | +6 / -4 | Permission denied: next safe action `remedy job contract <id>`, and `contract_guidance` carries the heir. No target repo / target repo not a directory: next safe action `remedy job contract <id>` |
| `packages/orchestration/timeline.py` | +3 / -2 | The permission-denied hint names the capability, the heir and `remedy job contract <id>` |
| `packages/orchestration/trust_report.py` | +3 / -2 | The workspace-denied hint names the heir, then `job resume` |
| `scripts/remedy_smoke.sh` | +26 / -5 | Steps 4 and 6i write the binding and grant on the job record through `python3 -c`, with a comment naming the heir and `remedy job contract <job_id>` |
| `docs/system/architecture.md` | +15 / -9 | The "Attaching a repo" paragraph becomes "Binding a repo": the D7 writer, the fallback and the grants, shown by `remedy job contract <job_id>`. The permission-denied hint text is updated. Three `set-permission` hints (the command's pre-F261 name) now say `job contract` (deviation 3) |
| `docs/system/first-fulfilled-job-demo-v0.md` | +4 / -2 | The step-1 line is now `remedy job contract "$JOB_ID"`, with the heir in its comment |
| `docs/system/real-test-execution-v1.md` | +3 / -2 | Dual-gate item 1 and the Guidance row name the heir |
| `docs/guides/do-continue-v1.md` | +2 / -1 | The gate bullet names the heir |
| `docs/guides/resume.md` | +1 / -1 | The `permission_denied` row names the heir |
| `docs/guides/simple-operator-quickstart-v0.md` | +3 / -2 | The demo line is now `remedy job contract "$JOB_ID"`, with the heir in its comment |
| `tests/orchestration/test_stop_reasons.py` | +8 / -5 | Both no-repo tip tests assert the exact new tip, with the project's path when it has one. The placeholder and job-id loops are kept |
| `tests/test_autonomy_readiness.py` | +11 / -7 | `TestAttachRepoTip` → `TestContractRepoTip`. The rendered line ends with the exact new tip, with the project's path when it has one. The no-placeholder checks are kept |
| `tests/cli/test_open_decisions_view.py` | +1 / -1 | `next_safe_action` starts with `remedy job contract <id> `, still with no `<` |
| `tests/test_agent_loop.py` | +4 / -4 | Asserts `remedy job contract <id>` plus the capability, and the `<capability>` fallback |
| `tests/test_brain_detail.py` | +3 / -2 | A next action starts with `remedy job contract <id> ` and names `workspace_write`. The summary shows `job contract` |
| `tests/test_cockpit.py` | +2 / -2 | Asserts `remedy job contract <id>` and `workspace_write` |
| `tests/test_timeline.py` | +3 / -3 | Asserts `remedy job contract <id>` and `workspace_write` |
| `tests/test_trust_report.py` | +2 / -2 | Asserts `remedy job contract <id>` |
| `tests/orchestration/test_test_runner.py` | +11 / -17 | The service source holds `remedy job contract {job.job_id}`, and runtime stderr holds `remedy job contract <job_id>`. `allow repo_test_run` is still absent from both. Readiness actions: at least one is `job contract`, and each such action names the real job id |
| `tests/orchestration/test_test_execution_service.py` | +3 / -1 | `test_permission_denied_blocked`: `repo_test_run` is in `safe_summary`, and `next_safe_action == remedy job contract <id>` (deviation 5) |
| `tests/orchestration/test_mission_contract.py` | +1 / -1 | The D7 class docstring no longer spells the deleted commands with their group, so G4 (a) holds |
| `tests/test_repo_applicator.py` | +1 / -1 | The section comment no longer names `_cmd_attach_repo` |

### C5 (this commit) F269 R6 C5: handoff and operator question Q5
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/operator_questions.md` | +10 / -0 | `c93d117d` bytes + opq.md (Q5) |
| `.agent/handoff.md` | rewrite | This file |

## External actions

- For G5: `git worktree add --detach .remedy-wt/f269-r6-g5 HEAD` (at `c73ccc6d`), then `git worktree remove --force .remedy-wt/f269-r6-g5`. `git worktree list` afterwards: `/home/decodeux/Repos/remedy  c73ccc6d [feature/f269-contract]`.
- `git push` runs after this commit. Its outcome and G6 are in the worker's final report.
- No PR was created, edited or merged.

## Verification

All gates ran at C4 `c73ccc6d` with a clean tree. The scripts are under `.remedy-wt/f269-r6/`, and each exit code is a subprocess return code.

G1 transport + state, `python3 .remedy-wt/f269-r6/g1.py`, exit code 0:
```
ledger.md sha256 77c7fab0471286bbfef4b0576af48328ba8c35667dfd0eafd90e3f0bef7c9e7f matches: True
decisions.md sha256 66027d1798f131c4c24ce0eae46c7298b7cd941407d0ccadc5f71c8ad765b8fb matches: True
plan.md sha256 abfa1a3fee20c976e034153a48e782f7d67eb58603ad35d1549163310148becb matches: True
opq.md sha256 daabfd5178d1d7f15c0dd56876f34ac8ef4ab9a8437b0c61997d1f4863be4140 matches: True
block.md sha256 8efe3d4d889f0dd05a401991d94fb05969d22d32befdfad6746c046df45535b4
plan.md equals payload: True
live_review.md equals base + ledger.md: True
decisions.md equals base + decisions.md: True
authored f269-r6-ledger.md equals payload: True
authored f269-r6-decisions.md equals payload: True
authored f269-r6-plan.md equals payload: True
authored f269-r6-opq.md equals payload: True
authored f269-r6-block.md equals payload: True
```

G2, `python3 .remedy-wt/f269-r6/g2.py c93d117d..HEAD g2`, which runs `python3 -m pytest -q -p no:cacheprovider` over these 24 paths: the 18 test files C2 to C4 created or edited, plus the block's list (`tests/orchestration/test_mission_contract.py` and `tests/test_command_catalog.py` are in both):
`tests/cli/test_open_decisions_view.py tests/orchestration/test_autonomy.py tests/orchestration/test_mission_contract.py tests/orchestration/test_stop_reasons.py tests/orchestration/test_test_execution_service.py tests/orchestration/test_test_runner.py tests/test_agent_loop.py tests/test_autonomy_readiness.py tests/test_brain_detail.py tests/test_cli_main.py tests/test_cockpit.py tests/test_command_catalog.py tests/test_command_discovery.py tests/test_grouped_cli.py tests/test_repo_applicator.py tests/test_test_runner.py tests/test_timeline.py tests/test_trust_report.py tests/cli/test_advertised_commands.py tests/orchestration/test_orchestrator_loop.py tests/cli/test_do_sequence_cli.py tests/cli/test_golden_path.py tests/orchestration/test_import_reachability.py tests/docs/`. Exit code 0:
```
1808 passed in 118.43s (0:01:58)
```

G3, `python3 -m ruff check` over the 34 `.py` files C2 to C4 touched (the 16 production files `apps/cli/command_catalog.py apps/cli/commands/job.py apps/cli/commands/job_context_cmd.py packages/orchestration/{agent_loop,autonomy_loop,autonomy_readiness,brain_detail,cockpit,do_sequence,mission_contract,orchestrator_loop,self_dogfood_execution,stop_reasons,test_execution_service,timeline,trust_report}.py`, plus the 18 test files above). Exit code 0:
```
All checks passed!
```

G4 absence sweep, `python3 .remedy-wt/f269-r6/g4.py <rev>`. It runs the three `git grep -n -E` commands of the block verbatim.

At `c93d117d`:
```
G4 (a) at c93d117d: exit 0, 66 line(s)
  c93d117d:apps/cli/commands/job.py:870:def _cmd_attach_repo(job_id_str: str, repo_path_str: str) -> None:
  c93d117d:apps/cli/commands/job.py:893:def _cmd_set_permission(job_id_str: str, action: str, capability_str: str) -> None:
  c93d117d:apps/cli/commands/job.py:2351:    "job.attach-repo": lambda args: _cmd_attach_repo(args.job_id, args.repo_path),
  c93d117d:apps/cli/commands/job.py:2352:    "job.permit": lambda args: _cmd_set_permission(args.job_id, args.action, args.permission),
  c93d117d:apps/cli/commands/job_context_cmd.py:91:# field, while `job._cmd_attach_repo` and `job_fulfillment` record a target repo
  c93d117d:docs/guides/do-continue-v1.md:58:- a safe target repository is attached (`remedy job attach-repo`);
  c93d117d:docs/guides/resume.md:60:| `permission_denied` | Job lacks required permission | `remedy job permit <job_id> repo_test_run allow` |
  c93d117d:docs/guides/simple-operator-quickstart-v0.md:80:remedy job attach-repo "$JOB_ID" /path/to/repo
  c93d117d:docs/system/architecture.md:286:remedy job attach-repo <job_id> /path/to/my-repo
  c93d117d:docs/system/architecture.md:906:concrete `remedy job permit <job_id> workspace_write` allow command.
  c93d117d:docs/system/first-fulfilled-job-demo-v0.md:34:remedy job attach-repo "$JOB_ID" /path/to/demo/repo  # see Repo Requirements below
  c93d117d:docs/system/real-test-execution-v1.md:11:1. **Permission granted**: `remedy job permit <job_id> repo_test_run allow`
  c93d117d:docs/system/real-test-execution-v1.md:153:| Permission missing | `remedy job permit <job_id> repo_test_run allow` |
  c93d117d:packages/orchestration/agent_loop.py:423:            f"      remedy job permit {full_id} {cap_arg} allow"
  c93d117d:packages/orchestration/autonomy_loop.py:210:                "remedy job permit <job_id> repo_test_run allow", "missing_permission")
  c93d117d:packages/orchestration/autonomy_readiness.py:300:        from packages.orchestration.stop_reasons import job_attach_repo_tip
  c93d117d:packages/orchestration/autonomy_readiness.py:302:               None if signals.get("attached_repo") else job_attach_repo_tip(job))
  c93d117d:packages/orchestration/autonomy_readiness.py:308:        _check("repo_generated_write", f"remedy job permit {job_id} repo_generated_write allow")
  c93d117d:packages/orchestration/autonomy_readiness.py:315:        _check("repo_test_run", f"remedy job permit {job_id} repo_test_run allow")
  c93d117d:packages/orchestration/brain_detail.py:620:        f"remedy job permit {job_id_str} {capability} allow",
  c93d117d:packages/orchestration/cockpit.py:282:            "grant with: remedy job permit <job_id> workspace_write allow"
  c93d117d:packages/orchestration/cockpit.py:325:            "remedy job permit <job_id> repo_generated_write allow"
  c93d117d:packages/orchestration/cockpit.py:401:            f"      remedy job permit {job_id_str} workspace_write allow"
  c93d117d:packages/orchestration/self_dogfood_execution.py:493:        elig.next_safe_action = f"remedy job attach-repo {jid} <path>"
  c93d117d:packages/orchestration/stop_reasons.py:204:def job_attach_repo_tip(job: Any) -> str:
  c93d117d:packages/orchestration/stop_reasons.py:205:    """The `remedy job attach-repo` command for *job*: its project's repo, else what to pass."""
  c93d117d:packages/orchestration/stop_reasons.py:211:        return f"remedy job attach-repo {job_id} {shlex.quote(repo)}"
  c93d117d:packages/orchestration/stop_reasons.py:212:    return (f"remedy job attach-repo {job_id} followed by the path of the "
  c93d117d:packages/orchestration/stop_reasons.py:246:            next_actions=(job_attach_repo_tip(job),),
  c93d117d:packages/orchestration/test_execution_service.py:607:        result.next_safe_action = f"remedy job permit {job.job_id} repo_test_run allow"
  c93d117d:packages/orchestration/test_execution_service.py:608:        result.contract_guidance = f"remedy job permit {job.job_id} repo_test_run allow"
  c93d117d:packages/orchestration/test_execution_service.py:625:            result.next_safe_action = f"remedy job attach-repo {job.job_id} <repo_path>"
  c93d117d:packages/orchestration/test_execution_service.py:632:        result.next_safe_action = f"remedy job attach-repo {job.job_id} <repo_path>"
  c93d117d:packages/orchestration/timeline.py:414:            f"      remedy job permit {job_id_str} {cap} allow"
  c93d117d:packages/orchestration/trust_report.py:465:            f"      remedy job permit {job.job_id} workspace_write allow\n"
  c93d117d:scripts/remedy_smoke.sh:333:    remedy job attach-repo "${JOB_ID}" "${TARGET_REPO}"
  c93d117d:scripts/remedy_smoke.sh:334:    remedy job permit "${JOB_ID}" repo_generated_write allow
  c93d117d:scripts/remedy_smoke.sh:560:        remedy job permit "${JOB_ID}" repo_test_run allow
  c93d117d:tests/cli/test_open_decisions_view.py:363:    assert status["next_safe_action"].startswith(f"remedy job attach-repo {job.job_id} ")
  c93d117d:tests/orchestration/test_autonomy.py:430:        """remedy job permit order: <job_id> <permission> <action>."""
  c93d117d:tests/orchestration/test_stop_reasons.py:230:    assert tip == f"remedy job attach-repo {job.job_id} {repo}"
  c93d117d:tests/orchestration/test_stop_reasons.py:248:    assert tip.startswith(f"remedy job attach-repo {job.job_id} ")
  c93d117d:tests/orchestration/test_test_runner.py:172:        """Permission guidance must show: remedy job permit <id> repo_test_run allow"""
  c93d117d:tests/orchestration/test_test_runner.py:254:            if "job permit" in action:
  c93d117d:tests/orchestration/test_test_runner.py:255:                # Must be: remedy job permit <id> <permission> allow
  c93d117d:tests/test_agent_loop.py:22:  - next action uses concrete capability: "remedy job permit … workspace_write allow"
  c93d117d:tests/test_agent_loop.py:534:        assert "job permit" in out
  c93d117d:tests/test_agent_loop.py:552:        assert "job permit" in out
  c93d117d:tests/test_autonomy_readiness.py:308:        assert line.endswith(f"remedy job attach-repo {job.job_id} {repo}")
  c93d117d:tests/test_autonomy_readiness.py:320:        assert f"remedy job attach-repo {job.job_id} " in line
  c93d117d:tests/test_brain_detail.py:425:        assert any("job permit" in a for a in detail.next_actions)
  c93d117d:tests/test_brain_detail.py:594:        assert "job permit" in out
  c93d117d:tests/test_cli_main.py:49:        from apps.cli.commands.job import _cmd_set_permission
  c93d117d:tests/test_cli_main.py:51:        _cmd_set_permission(str(job.job_id), "allow", "repo_overwrite")
  c93d117d:tests/test_cli_main.py:58:        from apps.cli.commands.job import _cmd_set_permission
  c93d117d:tests/test_cli_main.py:60:        _cmd_set_permission(str(job.job_id), "deny", "shell_exec")
  c93d117d:tests/test_cli_main.py:67:        from apps.cli.commands.job import _cmd_set_permission
  c93d117d:tests/test_cli_main.py:69:        _cmd_set_permission(str(job.job_id), "allow", "repo_generated_write")
  c93d117d:tests/test_cli_main.py:75:        from apps.cli.commands.job import _cmd_set_permission
  c93d117d:tests/test_cli_main.py:77:        _cmd_set_permission(str(job.job_id), "deny", "workspace_write")
  c93d117d:tests/test_cli_main.py:83:        from apps.cli.commands.job import _cmd_set_permission
  c93d117d:tests/test_cli_main.py:86:        _cmd_set_permission(str(job.job_id), "allow", "repo_overwrite")
  c93d117d:tests/test_cockpit.py:404:        assert "job permit" in out
  c93d117d:tests/test_repo_applicator.py:498:# attach-repo validation (mirrors _cmd_attach_repo logic)
  c93d117d:tests/test_timeline.py:732:        assert "job permit" in out
  c93d117d:tests/test_trust_report.py:616:        assert "job permit" in out
G4 (b) at c93d117d: exit 0, 6 line(s)
  c93d117d:apps/cli/command_catalog.py:324:        command_id="job.attach-repo",
  c93d117d:apps/cli/command_catalog.py:332:        command_id="job.permit",
  c93d117d:apps/cli/commands/job.py:2351:    "job.attach-repo": lambda args: _cmd_attach_repo(args.job_id, args.repo_path),
  c93d117d:apps/cli/commands/job.py:2352:    "job.permit": lambda args: _cmd_set_permission(args.job_id, args.action, args.permission),
  c93d117d:tests/orchestration/test_autonomy.py:432:        cmd = get_command("job.permit")
  c93d117d:tests/test_command_catalog.py:268:        "job.list", "job.show", "job.attach-repo", "job.permit",
G4 (c) at c93d117d: exit 0, 13 line(s)
  c93d117d:apps/cli/command_catalog.py:326:        subcommand="attach-repo",
  c93d117d:apps/cli/command_catalog.py:334:        subcommand="permit",
  c93d117d:apps/cli/command_catalog.py:452:        subcommand="attach-repo",
  c93d117d:tests/orchestration/test_test_runner.py:232:            [sys.executable, "-m", "apps.cli.main", "job", "attach-repo", job_id, str(repo)],
  c93d117d:tests/orchestration/test_test_runner.py:257:                # Find "permit" index
  c93d117d:tests/orchestration/test_test_runner.py:258:                idx = parts.index("permit")
  c93d117d:tests/test_autonomy_readiness.py:291:        [line] = [ln for ln in text.splitlines() if "attach-repo" in ln]
  c93d117d:tests/test_command_discovery.py:573:            ["python3", "-m", "apps.cli.main", "job", "attach-repo", job_id, str(repo)],
  c93d117d:tests/test_command_discovery.py:975:            ["python3", "-m", "apps.cli.main", "job", "attach-repo", job_id, str(repo)],
  c93d117d:tests/test_grouped_cli.py:123:            "create-job", "list-jobs", "show-job", "attach-repo",
  c93d117d:tests/test_grouped_cli.py:384:        stdout, stderr, rc = _capture_grouped(["job", "attach-repo"])
  c93d117d:tests/test_grouped_cli.py:430:        "attach-repo", "set-permission", "show-permissions",
  c93d117d:tests/test_test_runner.py:875:             "job", "permit", job_id, "repo_test_run", "allow"],
```

At C4 (`HEAD` = `c73ccc6d`):
```
G4 (a) at HEAD: exit 1, 0 line(s)
G4 (b) at HEAD: exit 0, 2 line(s)
  HEAD:tests/test_command_catalog.py:349:        "job.attach-repo",
  HEAD:tests/test_command_catalog.py:359:        "job.permit",
G4 (c) at HEAD: exit 0, 3 line(s)
  HEAD:apps/cli/command_catalog.py:430:        subcommand="attach-repo",
  HEAD:tests/test_grouped_cli.py:123:            "create-job", "list-jobs", "show-job", "attach-repo",
  HEAD:tests/test_grouped_cli.py:422:        "attach-repo", "set-permission", "show-permissions",
```
(a) prints no line (`git grep` exit 1 means no match). (b) prints exactly the two `TestDeletedCommands.DELETED` lines. Why each (c) line stays:
- `apps/cli/command_catalog.py:430` is `project.attach-repo`'s subcommand. That command writes the project's canonical repository, which D7's writer falls back to, and constraint 2 keeps it.
- `tests/test_grouped_cli.py:123` is in `test_no_old_flat_commands_in_help`, a list of pre-grouping flat names asserted ABSENT from root help. It is an absence guard, and it still holds.
- `tests/test_grouped_cli.py:422` is in `TestRootHelpNoOldFlatCommands.OLD_FLAT`, the same kind of absence guard over root help.

G5 mutation red-proofs, `python3 .remedy-wt/f269-r6/g5.py`: one worktree at `c73ccc6d`, running `python3 -B -m pytest -q -p no:cacheprovider tests/orchestration/test_mission_contract.py` from the worktree root. `__pycache__` was purged before each run, each mutation was an exact one-occurrence line replacement, and the original bytes were written back after each run:
```
worktree add: 0 []
[control, unmutated] mission_contract imported from: /home/decodeux/Repos/remedy/.remedy-wt/f269-r6-g5/packages/orchestration/mission_contract.py
[control, unmutated] exit code 0; 74 passed in 0.67s
[(a) the writer grants nothing] mutated: packages/orchestration/mission_contract.py | 2 +-
 1 file changed, 1 insertion(+), 1 deletion(-)
[(a) the writer grants nothing] mission_contract imported from: /home/decodeux/Repos/remedy/.remedy-wt/f269-r6-g5/packages/orchestration/mission_contract.py
[(a) the writer grants nothing] exit code 1; 3 failed, 71 passed in 0.71s
   FAILED tests/orchestration/test_mission_contract.py::TestTheContractBindsAndGrantsItsJobs::test_a_dispatched_job_gets_the_projects_repository_and_the_three_grants
   FAILED tests/orchestration/test_mission_contract.py::TestTheContractBindsAndGrantsItsJobs::test_a_do_job_is_bound_to_its_own_repo_path_and_granted
   FAILED tests/orchestration/test_mission_contract.py::TestTheContractBindsAndGrantsItsJobs::test_a_target_repo_already_set_is_not_overwritten
[(a) the writer grants nothing] reverted, status of target: (clean)
[(b) the writer binds no target_repo] mutated: packages/orchestration/mission_contract.py | 2 +-
 1 file changed, 1 insertion(+), 1 deletion(-)
[(b) the writer binds no target_repo] mission_contract imported from: /home/decodeux/Repos/remedy/.remedy-wt/f269-r6-g5/packages/orchestration/mission_contract.py
[(b) the writer binds no target_repo] exit code 1; 2 failed, 72 passed in 0.70s
   FAILED tests/orchestration/test_mission_contract.py::TestTheContractBindsAndGrantsItsJobs::test_a_dispatched_job_gets_the_projects_repository_and_the_three_grants
   FAILED tests/orchestration/test_mission_contract.py::TestTheContractBindsAndGrantsItsJobs::test_a_do_job_is_bound_to_its_own_repo_path_and_granted
[(b) the writer binds no target_repo] reverted, status of target: (clean)
worktree remove: 0
/home/decodeux/Repos/remedy  c73ccc6d [feature/f269-contract]
```
The mutations:
- (a) `        set_permission(job, Capability(grant), allow=True)` became `        pass`. The loop still runs, and grants nothing.
- (b) `            job.metadata[JOB_TARGET_REPO_KEY] = str(repo)` became `            pass`.

The full suite was not run (amend0917-throughput).

## Authored-text proofs

- The five payloads (block, decisions, ledger, plan, opq) are committed byte-identical as `.agent/authored/f269-r6-*` (G1 `equals payload: True`).
- `.agent/plan.md` equals plan.md. `.agent/live_review.md` and `.agent/decisions.md` equal their `c93d117d` bytes plus the slice (G1 `True`).
- `.agent/operator_questions.md` (C5) was built as its `c93d117d` bytes + opq.md, and a python check printed `operator_questions equals base + opq.md: True`.

## Deviations & assumptions

1. C3 alone leaves three tests red, and C4 turns them green: `tests/cli/test_advertised_commands.py::test_every_advertised_command_exists_in_the_catalog`, `::test_every_operator_facing_advertised_command_exists_in_the_catalog` and `tests/orchestration/test_autonomy.py::TestGeneratedCommandCatalogConsistency::test_generated_commands_reference_catalog`. Between the deletion and the string sweep, the strings still advertise the deleted words. The block orders deletion before strings, and every gate is measured at C4, where all three pass (G2).
2. The fixture setups write what the deleted command wrote at that step, and no more. The two `test_command_discovery.py` fixtures and `test_permit_runtime_stderr` write only the binding, because they used only `attach-repo`: that test asserts the missing-grant path. `test_test_runner.py::test_no_target_repo_exits_1` writes only `repo_test_run`, because it used only `permit` and asserts the missing-repository path. Each snippet's exit code is now asserted, where the old command's was ignored.
3. `docs/system/architecture.md` lines 561, 618 and 1454 (at `c93d117d`) named `set-permission`, the pre-F261 flat name of `job permit`, as the hint. They are outside G4's patterns, but they tell a reader to run the deleted command, so they now say `job contract`. The neighbouring stale flat names on those lines (`run-next-task-local`, `create-job`) belong to other deleted commands and were not touched.
4. `scripts/remedy_smoke.sh` runs its commands rather than advertising them. Its job is made through `_cmd_create_job` and belongs to no contract, so steps 4 and 6i write the binding and grants on the record through `python3 -c`, the same form as the test fixtures. A comment names the heir and `remedy job contract <job_id>`. `bash -n` passed. The script was not run: it needs the `remedy` entry point and the network.
5. `tests/orchestration/test_test_execution_service.py::test_permission_denied_blocked` is outside G4's patterns. It asserted `"repo_test_run" in next_safe_action` and went red when the action became `remedy job contract <id>`. It now asserts `repo_test_run` in `safe_summary` ("Permission repo_test_run not granted.") and the exact next safe action, which keeps its property that the blocked result names the missing capability. It is in G2. It was found by an extra run over 28 further test files, chosen because they name a touched module or the smoke script (`test_self_dogfood_execution.py`, `test_test_execution_service.py`, `test_remedy_smoke_script.py`, `test_named_bugs.py` and others), plus `tests/test_permissions.py`: 1 failed, 1000 passed, 8 skipped before the fix, and the file passed alone after it (65 passed).
6. Workspace_write guidance (`cockpit`, `trust_report`, `timeline`, `agent_loop`, `architecture.md`) also names the heir, because D7 names every string that tells a reader to run either command. The contract does not grant `workspace_write`. That capability is allowed by default, and only an explicit deny, which nothing but the deleted `job permit` could write, ever denied it. The hints still name the missing capability.
7. The tests asserting the guidance negatively (`"job permit" not in ...`) were not added, because G4 (a) requires no line matching that text in `tests/`. The properties are asserted positively instead (the exact `remedy job contract <id>`), and `allow repo_test_run` absence is kept.
8. `tests/test_repo_applicator.py::TestAttachRepoValidation` (unchanged) still describes "the validation rules applied by attach-repo". D7 SECOND does not name it, it asserts no command, and constraint 4 allows no other deletion. Only the section comment naming `_cmd_attach_repo` changed.
9. The import-reachability allowlist was not regenerated: `test_import_reachability.py` passed without it (G2).
10. Deleting the argparse words leaves no abbreviation: `remedy job attach-repo x /tmp`, `job permit x repo_test_run allow`, `job attach x` and `job perm x` each exit 2 with the `job` group usage.
11. Each commit's insertions are under 500 (largest: C2 at 206). The bundle's commit order was followed with no extra commit.

| Item | Status | Reason |
|------|--------|--------|
| C1 bookkeeping | done | |
| C2 the writer (D7 FIRST) + tests | done | |
| C3 the deletion (D7 SECOND) | done | three advertised-command guards red until C4 (deviation 1) |
| C4 the heir in every string + tests | done | deviations 3 to 8 |
| C5 handoff + Q5 + push | done | push follows this commit |

## Next

1. Phase 1 rule 1: check `.agent/STOP`.
2. Then the review of round 6 (D7: the contract's writer, and the deletion of `job attach-repo` and `job permit`), with its verdict booked in round 7's first commit.

Operator questions open: 5
