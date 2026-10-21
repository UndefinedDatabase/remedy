# Permission matrix (v1)

> GENERATED from `PERMISSION_MATRIX`, `PERMISSION_ACTION_WORDS` and `PERMISSION_SEAMS` in
> `packages/orchestration/permission_matrix.py` by `render_permission_matrix_page()`. Do not edit it
> by hand: `tests/docs/test_permission_matrix_page.py` fails whenever the constants and this file
> differ. Regenerate it from the repository root with
> `python3 -c "from packages.orchestration.permission_matrix import write_permission_matrix_page; write_permission_matrix_page()"`.

The permission matrix says what the work Remedy runs may DO at each autonomy level; the autonomy
level itself (`docs/system/autonomy-levels-v1.md`) says who may START that work. Every place that
acts asks one check, `require_permission`, and every answer names its cell as
`(action, level) = cell` (F141, DECISIONs F141 D1 to D6).

## The table

| Action | What it means | L2 | L3 | L4 | L5 |
|---|---|---|---|---|---|
| `read` | read your project's files | allow | allow | allow | allow |
| `write_worktree` | write a job's result into your project's files | ask | ask | allow | allow |
| `commit` | commit in your project's repository | ask | ask | ask | allow |
| `push` | push to your project's remote | ask | ask | ask | ask |
| `dependency_change` | change your project's dependencies | ask | ask | allow | allow |
| `destructive` | delete files or run a migration in your project | ask | ask | ask | ask |
| `expensive` | start work estimated above your cost threshold | ask | ask | ask | allow |
| `external_call` | run a command that reaches the network | allow | allow | allow | allow |

`allow` means the matrix asks nothing more of this one instance. `ask` means the action goes ahead
only with your approval of this one instance: the flag of your own command that names it, your `y`
at the command's own prompt, or your answer `approve` to the decision the apply raises for a
dependency change or a deletion. `deny` means refused, with or without an approval; only a change
of the configuration lifts it. An instance that needs several actions needs every one of their
cells.

A cell never replaces a gate a place already has: the scope fences still say where a job may
write, an apply still needs `--approve`, and budgets and the cost threshold's prompt still apply at
every level.

## The push switch

`autonomy.allow_push`, true by default, set in `remedy.toml` and refused from the environment,
turns every `push` cell into `deny` when it is false, at every level. It can only make the table
stricter.

## Where each action is asked

| Action | Where it is asked, and what approves one instance |
|---|---|
| `read` | `build_builder_context` in `packages/orchestration/builder_context.py`, before the context of a builder's call is built; it allows at every level, and the first check of a job's run records the job's level |
| `write_worktree` | `_flag_refusals` in `packages/orchestration/job_apply.py`, through `apply_permission_refusals`, when `remedy job apply` or a walk of `remedy do run` writes a job's result into your project; approved by `--approve` |
| `commit` | the same place, when the apply commits; approved by `--commit`, `--commit-auto` or `--commit-with-history` |
| `push` | the same place, when the apply pushes, and `do_mission_push_refusals` and `do_push_mission` in `packages/orchestration/do_apply.py` for a walk's push; approved by `--push` or by the key `apply.push_after_mission` |
| `dependency_change` | the apply, when a path it writes is a dependency manifest; approved by your answer `approve` to the decision the apply raises |
| `destructive` | the apply, when a path it writes lies in a `migrations` folder or a `--commit-with-history` branch deletes a file; approved by your answer `approve` to the decision the apply raises |
| `expensive` | `confirm_cost_preview` in `apps/cli/cost_preview_confirm.py`, for `remedy job resume` and `remedy job rerun-subtree` above `cost_preview.confirm_above_usd`; approved by `--yes`, `--unattended` or your `y` at its prompt |
| `external_call` | `plan_child_spawn` in `packages/orchestration/exec_guard.py`, for every child process that keeps the network; it allows at every level |

## The record of approvals

Every `ask` that an approval satisfied leaves one line in
`<data root>/autonomy/permission_grants.jsonl`, with `at`, `action`, `level`, `cell`,
`approval_kind` (`flag`, `prompt` or `decision`), `approval_ref`, `job_id` and `subject`.

## The level a job runs at

A job keeps the level in force at its first context: the first `read` check of its run writes
`autonomy_level.json` into the job's folder, and every later check reads it back, so a level
changed while a job runs never reaches that job. A job without that file reads `L2`, and so does
work that belongs to no job.

## What the matrix does not replace

- The worker's writes inside a job's own workspace are not an action of the matrix: the workspace
  is the job, and the scope fences say where in it the job may write.
- `packages/orchestration/permissions.py` grants a job the capabilities its own steps need inside
  its workspace. It is a layer below the matrix, like the fences, and the matrix still answers for
  everything that reaches your project.
- The integer `autonomy_level` of the builder bridge and the 0 to 7 readiness scale are other
  scales, not the levels `L2` to `L5`.
- Remedy deliberately has no switch that turns the matrix off: the only way past an `ask` is your
  approval of the one instance, and the only way past a `deny` is the configuration.
