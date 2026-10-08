# F304 acceptance re-audit 1 (amend0930b-slow-cap hardening stage)

Commit audited: `2a51ff0bafdd02afd0c9a68e82f20a9f96892d56` (branch `feature/f304-machine-client-contract-v1-1-part-two`).

## What was read, and what was not

Read: `docs/roadmap/features/T12_F304.md` (as given), the rows of `.agent/f304_acceptance_audit.md`, `tests/cli/test_machine_client_paths.py`, the `_remedy`, `_StdinNobodyMayRead` and `_scratch_repo` helpers in `tests/cli/test_machine_client_contract.py`, and the production code `_order_repo` in `apps/cli/commands/do_cmd.py` and `decline_job_result` in `packages/orchestration/job_apply.py`. Not read: `.agent/handoff.md`, `live_review*.md`, `plan.md`, `decisions.md`, `prose_slips.md`, anything under `.agent/authored/`, and any other `.remedy-wt/f304-*` folder.

Reading checks. Row 3: `_project_order` registers the repository with `project register --repo` from `tmp_path/elsewhere`, an empty folder that is no repository; the order file names the project in a `project:` header; `do`, `job show` and `job apply` all run with that folder as cwd; the test also asserts the folder is still empty. Row 7: the decline test runs `do`, `status`, `job decline`, `status` and `job ownership` from the same folder. Every command in both tests goes through `_remedy`, which calls `apps.cli.grouped.main` in process with a stdin whose `read` and `readline` raise AssertionError.

## How the mutations ran

Worktree `/home/decodeux/Repos/remedy/.remedy-wt/f304-reaudit-wt` at the audited commit. Script `run.py` in this folder: for each row, one control run of the single node (`python3 -B -m pytest -q -p no:cacheprovider <node>`, cwd the worktree), one edit of one production file, a 2 second wait, the same node again, then `git checkout -- .` and `git status --porcelain` in the worktree (empty both times). Raw output is in `row3_control.txt`, `row3_mutated.txt`, `row7_control.txt`, `row7_mutated.txt`. No model runs; the tests use `--no-llm` and the fake provider.

## Claims and proofs

| # | Claim | Test | Mutation (production file, exact change) | Control | Mutated | Verdict |
|---|-------|------|------------------------------------------|---------|---------|---------|
| 3 | The second gate test drives, through `apps.cli.grouped.main`, an order that runs in the repository of the project it names wherever the client stands | `tests/cli/test_machine_client_paths.py::test_an_order_naming_its_project_runs_in_that_projects_repository_wherever_the_client_stands` | `apps/cli/commands/do_cmd.py`, `_order_repo`: `if repo is None:` then `return registered` becomes `return str(Path.cwd())` | 0 (1 passed) | 1 (1 failed: `do` fails at step `init`, `assert 1 == 0`, because the client's folder is no repository) | PROVED (CLI) |
| 7 | The second gate test drives a result that is declined | `tests/cli/test_machine_client_paths.py::test_a_client_declines_a_completed_result_and_it_waits_for_nothing` | `packages/orchestration/job_apply.py`, `decline_job_result`: `job.metadata = {**(job.metadata or {}), JOB_METADATA_DECLINE_KEY: record}` becomes `job.metadata = dict(job.metadata or {})` (the decline is not kept) | 0 (1 passed) | 1 (1 failed: `('completed', True) == ('completed', False)`, the declined job still waits for its apply) | PROVED (CLI) |

## Gaps

None.

## Counts

Rows re-audited: 2. PROVED (CLI): 2. GAP: 0. Mutations: 2, each restored; the worktree was clean after each.
