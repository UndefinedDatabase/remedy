# F141 seam inventory — where each action of the permission matrix happens today

> T001 of `docs/roadmap/features/T7_F141.md`, read at `43e470560` (the merge commit of pull request
> 373). One section per action of DECISION F141 D1: the enforcement point, what the code does there
> today, and where the check goes. Functions are named, not line numbers, because the rounds that
> follow move code. `PO` is `packages/orchestration/`.

## read
- Point: `compile_task_context` in `PO/context_compiler.py`, called by `run_pingpong` in
  `PO/pingpong_loop.py` for every builder call; `apps/cli/commands/job_context_cmd.py` calls it to
  show a context and changes nothing.
- Today: no permission check; the context is chosen by the job's fenced paths and their import
  neighbours, within a size cap.
- Check: once per call in `run_pingpong`, before the context is compiled. It allows at every level.

## write_worktree
- Point: `apply_job` and `_apply_from_workspace` in `PO/job_apply.py` write a job's result into the
  operator's project, one file at a time, after the "Apply files" banner.
- Today: without `--approve` the apply only previews; with it, the blocked paths, the containment of
  source and destination, the baseline and the file modes are checked first.
- Not this action: the worker's writes inside the job's own workspace (`_strict_apply_to_workspace`
  and `task_fence_refusal` in `PO/pingpong_job.py`; `apply_structured_patch` in
  `PO/source_apply.py`; `apply_patch_intent` in `PO/patch_apply.py`; `apply_task_output_to_repo` in
  `PO/repo_applicator.py`). The fences of `PO/scope_fences.py` (`check_path`, `check_change_set`,
  `enforce_change_set`) say where those may write; the matrix does not repeat them.
- Check: in the apply, after the refusals of its flags and before the first file is written, with
  `--approve` as the instance approval.

## commit
- Point: `_commit_applied_files` (`--commit`, `--commit-auto`) and `_merge_job_branch`
  (`--commit-with-history`) in `PO/job_apply.py`.
- Today: only the operator's commit flags commit; `commit_flags_refusal`, `_commit_refusals`,
  `_history_refusals` and `_flag_refusals` refuse clashing or unsafe flags before the preview and
  again before writing.
- Not this action: Remedy's commits on a job's own branch inside its worktree (`commit_job_worktree`
  in `PO/worktrees.py`, reached from `_commit_applied_task` in `PO/pingpong_job.py` and from
  `PO/subtree_rerun.py`) and the baseline commit of `PO/dirty_baseline.py`, which stay inside the job.
- Check: beside `_flag_refusals`, so the preview shows the answer too, with the commit flag as the
  instance approval.

## push
- Point: `push_to_upstream` in `PO/job_apply.py`, the one place that runs `git push`, never with
  force; reached by `_push_landed_commit` (`remedy job apply --push`) and by `do_push_mission` in
  `PO/do_apply.py` (`remedy do` with its push flag). The public API lists `push` among its apply flags
  (`PO/public_api_writes.py`).
- Today: a push needs a commit flag; `upstream_push_refusals`, `mission_push_refusals`,
  `_push_refusals` and `do_mission_push_refusals` refuse a push without an upstream or with a blocking
  criterion unmet.
- Check: in `push_to_upstream`, which both paths reach, with `--push` as the instance approval and
  `autonomy.allow_push` read there.

## dependency_change
- Point: none exists. No ADR detector and no manifest parser is in the code; F138 is unbuilt. The
  nearest pieces are `_MANIFEST_NAMES` and `_classify_path` in `PO/context_inspector.py`; the
  manifest readers of `PO/project_constitution.py` extract commands, not changes.
- Check: a predicate over the paths the apply plans to write, true when one of them is a dependency
  manifest by its file name, at the same place as `write_worktree`'s check.

## destructive
- Point: none exists. `job_apply` copies files and never deletes; a staged file that is missing
  blocks the apply. The one way a deletion reaches the project is `--commit-with-history`, whose merge
  brings whatever the job branch holds. `_apply_file_op` in `PO/source_apply.py` refuses a `delete`
  operation in the job's workspace. Migrations are named only by patterns in `PO/do_lane.py` and
  `PO/project_constitution.py`.
- Check: a documented predicate — a path the change deletes, or a path under a migrations folder —
  before the merge of `--commit-with-history` and before the apply writes.

## expensive
- Point: `confirm_cost_preview` in `apps/cli/cost_preview_confirm.py`, with the estimate of
  `estimate_cost_band` and the threshold of `resolve_confirm_above_usd` in `PO/cost_preview.py`
  (`cost_preview.confirm_above_usd`, default 0.5 dollars). Callers: `remedy job resume`
  (`apps/cli/commands/job.py`), `remedy job rerun` (`apps/cli/commands/job_rerun_cmd.py`) and
  `PO/subtree_rerun.py`.
- Today: above the threshold, or with no estimate, the command asks; `--yes` answers for it and is
  logged.
- Check: `confirm_cost_preview` becomes a consumer of the matrix, with `--yes` as the instance
  approval.

## external_call
- Point: the network column of the exec policies in `PO/exec_guard.py`: `test_command_exec_policy`
  and `dod_process_exec_policy` deny network, `runtime_build_exec_policy` allows it,
  `runtime_server_exec_policy` and `dod_app_exec_policy` take the default; `plan_child_spawn` applies
  it. `PO/tool_sandbox.py` runs its children with no network except through `ProviderRelay`.
- Today: network is granted per command class, the same at every level.
- Check: the policy that grants network asks the matrix once per spawn; it allows at every level
  (DECISION F141 D1 (2)).

## The level a job runs at
- No job records its level. `autonomy_start_scope` in `PO/autonomy_gate.py` holds it in a context
  variable for one command; `remedy mission run` prints it and keeps nothing. The integers named
  `autonomy_level` in `PO/autonomy_loop.py`, `PO/run_contract.py` and `run_builder_bridge` in
  `PO/builder_bridge.py` are other scales, not F078's levels.

## Decisions
- `list_decisions` in `PO/decision_queue.py` builds decisions from a job's state; `DECISION_TYPES` is
  a closed set pinned by `tests/orchestration/test_decision_inbox.py`. `enqueue_task_decision` and
  `answer_task_decision` in `PO/escalation.py` raise and answer a `task_decision`, as
  `raise_scope_question` in `PO/scope_question.py` does.

## Parameters shaped like a bypass
- `yes` of `confirm_cost_preview` (the operator's own answer on the command line); `skip_blocked` of
  the apply (narrows what is written); `target_repo_override` of `apply_patch_intent` (redirects, does
  not widen); `force_job` and `force_mission` of `PO/do_targets.py` (choose a run's shape).
- `set_permission` and `job.metadata["permissions"]` of `PO/permissions.py`: a per-job grant of
  capabilities, the widest surface of the kind (DECISION F141 D1 (10)).

## The structure ledger at the seams
- Functions: `run_job` 1434, `run_pingpong` 1314, `list_decisions` 887, `_apply_from_workspace` 346,
  `apply_patch_intent` 280, `apply_job` 220, `compile_task_context` 190, `_strict_apply_to_workspace`
  190, `apply_structured_patch` 186, `run_builder_bridge` 168, `run_guarded` 122.
- Files: `PO/pingpong_job.py` 5331, `PO/pingpong_loop.py` 5231, `PO/job_apply.py` 2541,
  `PO/context_compiler.py` 1199, `PO/decision_queue.py` 1182. The ledger's boundary for
  `job_apply.py` names "the history, commit and push policy" as a module of its own: the commit and
  push seams live there.
