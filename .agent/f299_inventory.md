# F299 T001 — the three scratch targets, measured

> Measured on `main` at `1acd5ac39` for DECISION F299 D1. The readings below are printed by the
> reviewer's script `.remedy-wt/f299-r1/measure.py` (gitignored scratch) and copied verbatim; the
> worker's run of the same script at the round's base printed the same bytes. Paths, job ids and
> durations are replaced by placeholders, so two runs can be compared byte for byte.

## The targets
- **python**: a git repository with `pyproject.toml`, `tests/test_dep.py` importing
  `only_in_project_venv`, and a `.gitignore` naming `.venv/`; its own virtual environment `.venv`,
  made without pip, holds that module in its site-packages and nothing else of its own. Remedy's
  environment does not have the module.
- **node**: a git repository with a `package.json` whose `test` script is `node --test` and one
  test under `test/`, needing no installed package.
- **no-tests**: a git repository holding only `README.md`.

Each target was driven once with `remedy do` and the order "Write a CONTRIBUTING.md", with the
fake builder and reviewer and `--no-llm`, its own scratch data root, `--no-ui` and `--yes`. Then
the mission's contract, the job's gate result and F270's push rule (`mission_push_refusals`) were
read back from that data root.

## What was measured, with the fake providers
In all three, the mission's one criterion is the planner's (the deterministic plan's one
milestone) and carries the compiler's fallback check: kind `pytest`, selector `tests`, run as
`<remedy-python> -m pytest -p no:cacheprovider tests -q`, Remedy's own interpreter. It runs in
the job's worktree `<target>/.remedy-wt/job-<job>`, which holds neither `.venv` nor
`node_modules`, while the Python target's own checkout holds `.venv`. Each job ends `completed`
and its gate releases it, because a contract check enters a `do` job's definition of done
non-blocking; each criterion ends `unmet`, and the push is refused.
- python: exit 2, `ModuleNotFoundError: No module named 'only_in_project_venv'` while collecting.
- node and no-tests: exit 4, `file or directory not found: tests`.

```text
order: Write a CONTRIBUTING.md
command: python3 -m apps.cli.main do run <order> --repo <target> --json --no-llm --no-ui --yes --builder-provider fake --reviewer-provider fake

## target python
do exit code: 0
do ok: True
do unmet_blocking_criteria: ['C001']
template: None
criterion C001 origin=planner blocking=True status=unmet check={"acceptance_refs": ["C001:0"], "blocking": true, "description": "The mission goal is met in full: Write a CONTRIBUTING.md", "id": "ctr-C001", "kind": "pytest", "source": "plan_acceptance", "spec": {"selector": "tests"}}
job state: completed
job workspace: <target>/.remedy-wt/job-<job>
  workspace holds .venv: False; node_modules: False
  target holds .venv: True
gate released: True
check ctr-C001 kind=pytest blocking=False status=failed reason=nonzero_exit exit=2
  command=<remedy-python> -m pytest -p no:cacheprovider tests -q
  tail| ImportError while importing test module '<target>/.remedy-wt/job-<job>/tests/test_dep.py'.
  tail| E   ModuleNotFoundError: No module named 'only_in_project_venv'
  tail| !!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
  tail| 1 error in <secs>
push refusals: ["The mission's blocking contract criteria C001 are unmet, so nothing is pushed."]
push still open: []

## target node
do exit code: 0
do ok: True
do unmet_blocking_criteria: ['C001']
template: None
criterion C001 origin=planner blocking=True status=unmet check={"acceptance_refs": ["C001:0"], "blocking": true, "description": "The mission goal is met in full: Write a CONTRIBUTING.md", "id": "ctr-C001", "kind": "pytest", "source": "plan_acceptance", "spec": {"selector": "tests"}}
job state: completed
job workspace: <target>/.remedy-wt/job-<job>
  workspace holds .venv: False; node_modules: False
  target holds .venv: False
gate released: True
check ctr-C001 kind=pytest blocking=False status=failed reason=nonzero_exit exit=4
  command=<remedy-python> -m pytest -p no:cacheprovider tests -q
  tail| no tests ran in <secs>
  tail| ERROR: file or directory not found: tests
push refusals: ["The mission's blocking contract criteria C001 are unmet, so nothing is pushed."]
push still open: []

## target no-tests
do exit code: 0
do ok: True
do unmet_blocking_criteria: ['C001']
template: None
criterion C001 origin=planner blocking=True status=unmet check={"acceptance_refs": ["C001:0"], "blocking": true, "description": "The mission goal is met in full: Write a CONTRIBUTING.md", "id": "ctr-C001", "kind": "pytest", "source": "plan_acceptance", "spec": {"selector": "tests"}}
job state: completed
job workspace: <target>/.remedy-wt/job-<job>
  workspace holds .venv: False; node_modules: False
  target holds .venv: False
gate released: True
check ctr-C001 kind=pytest blocking=False status=failed reason=nonzero_exit exit=4
  command=<remedy-python> -m pytest -p no:cacheprovider tests -q
  tail| no tests ran in <secs>
  tail| ERROR: file or directory not found: tests
push refusals: ["The mission's blocking contract criteria C001 are unmet, so nothing is pushed."]
push still open: []
```

## What was measured, with the configured planner
The configured planner is the local Ollama service (`planner.provider` unset, the default). The
reviewer ran the script once with `--planner --only=python`, which drops `--no-llm`; the run took
about eleven minutes. The planner wrote five criteria, each with its own text, and every one of
them carries the same fallback check: kind `pytest`, selector `tests`. `remedy do` exited 1 with
the mission's jobs still `planned` and none run, so no criterion was evaluated and every one reads
`open`; the script did not capture why the walk stopped, and that is not needed here, because the
check is fixed before any job runs. The code agrees: `write_planner_criteria`,
`amend_mission_contract` and `compile_contract_template` call `compile_contract_criteria` with no
planner call, so the planner writes a criterion's text and never its check. The planner was not
run on the other two targets (DECISION F299 D1 (1)).

```text
order: Write a CONTRIBUTING.md
command: python3 -m apps.cli.main do run <order> --repo <target> --json --no-ui --yes --builder-provider fake --reviewer-provider fake

## target python
do exit code: 1
do ok: False
do unmet_blocking_criteria: ['C001', 'C002', 'C003', 'C004', 'C005']
template: None
criterion C001 origin=planner blocking=True status=open check={"acceptance_refs": ["C001:0"], "blocking": true, "description": "Existing contribution norms and documentation inventory is complete", "id": "ctr-C001", "kind": "pytest", "source": "plan_acceptance", "spec": {"selector": "tests"}}
criterion C002 origin=planner blocking=True status=open check={"acceptance_refs": ["C002:0"], "blocking": true, "description": "Existing contribution norms and documentation inventory is complete", "id": "ctr-C002", "kind": "pytest", "source": "plan_acceptance", "spec": {"selector": "tests"}}
criterion C003 origin=planner blocking=True status=open check={"acceptance_refs": ["C003:0"], "blocking": true, "description": "Existing contribution norms and documentation inventory is complete", "id": "ctr-C003", "kind": "pytest", "source": "plan_acceptance", "spec": {"selector": "tests"}}
criterion C004 origin=planner blocking=True status=open check={"acceptance_refs": ["C004:0"], "blocking": true, "description": "Existing contribution norms and documentation inventory is complete", "id": "ctr-C004", "kind": "pytest", "source": "plan_acceptance", "spec": {"selector": "tests"}}
criterion C005 origin=planner blocking=True status=open check={"acceptance_refs": ["C005:0"], "blocking": true, "description": "Existing contribution norms and documentation inventory is complete", "id": "ctr-C005", "kind": "pytest", "source": "plan_acceptance", "spec": {"selector": "tests"}}
job state: planned
job workspace: None
  target holds .venv: True
gate released: None
job state: planned
job workspace: None
  target holds .venv: True
gate released: None
job state: planned
job workspace: None
  target holds .venv: True
gate released: None
push refusals: []
push still open: ['C001', 'C002', 'C003', 'C004', 'C005']
```

## What exists to build on, read at `1acd5ac39`
- `packages/orchestration/dod_compiler.py`: `DEFAULT_TEST_SELECTOR = "tests"`, the fallback for
  an acceptance line that names no test path.
- `packages/orchestration/dod_runners.py`: `PYTEST_PYTHON = sys.executable or "python3"`; the
  `pytest` kind is exempt from the closed list, which binds `lint`, `build` and `custom_cmd`.
- `packages/orchestration/test_runner.py`: `_EXECUTION_SAFE_EXECUTABLES`, the closed list; it
  holds `npm` and `python3`, matched by name.
- `packages/orchestration/exec_guard.py`: `dod_process_exec_policy` builds a check's environment
  from Remedy's own, filtered to `DOD_PROCESS_ENV_ALLOWLIST`, which holds `PATH` and
  `VIRTUAL_ENV`.
- `packages/runtimes/runtime_config.py`: the project's own `.remedy/config.toml`, read today for
  its `[runtime]` table only.
- `packages/orchestration/command_discovery.py`: `select_best_test_candidate`, which returned
  `npm test # node --test` for the Node target and a bare `pytest` for the Python target.
- `packages/orchestration/study.py`: four free-text cards; no test command is recorded.
- `packages/orchestration/mission_contract.py`: three criterion states, `open`, `met` and
  `unmet`; `record_contract_results` writes `met` or `unmet` from the gate's evidence.
- `packages/orchestration/job_apply.py`: `mission_push_refusals` refuses a push while a blocking
  criterion is `unmet`.
