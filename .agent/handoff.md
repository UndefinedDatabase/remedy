# Handoff — F299 round 2: claim, T001's measurement, and T002 (the check kind `project_tests`)

## Session

SESSION 1 of feature F299 · round 2 · rounds so far 2

Context self-assessment: the reviewer's context is comfortable; the session continues.

Fortschritt: ~35 % (claim, T001 and T002 · T003 and T004 open) — Schätzung

## Range

Review of `5eaca8c78`..HEAD (five commits on `feature/f299-acceptance-checks-other-repos`: C1
through C4 and this handback; round 1's base `5eaca8c78` is round 1's own single handoff commit,
on top of `1acd5ac39`, the merge of pull request 317/F253).

## Commits

### `f6a1809de` F299 R2 C1: save the round 2 block

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f299-r2.md` | 310/0 | NEW FILE — a verbatim copy of `block.md`; sha256 and line count checked equal to the source (both `61d527520b2b3cda824ef0560a370427f8263931c507b558c6481e47061e9e84`, 310 lines) |

### `e710f603e` F299 R2 C2: claim F299, book F253 R38 and F299 R1, T001's measurement, DECISION F299 D1, the plan

| Path | +/- | Reason |
|---|---|---|
| `docs/roadmap/STATUS.md` | 1/1 | F299's line `[ ]` → `[~]` (claimed) |
| `.agent/live_review.md` | 31/25 | re-headed at the F299 claim; books `Gate: F253 R38` (PASS) and `Gate: F299 R1` (FAIL) |
| `.agent/decisions.md` | 10/0 | appends DECISION F299 D1 (the `project_tests` check kind, its order, the environment lookup, the contract remap) |
| `.agent/plan.md` | 19/18 | rewritten for F299's goal, round 2's current step and next steps |
| `.agent/prose_slips.md` | 1/0 | appends the round 1 prose-slip (reviewer's stale `dry-measure.txt`) |
| `.agent/context.md` | 11/14 | rewritten for F299's scope, do-not-touch list and active assumptions |
| `docs/roadmap/features/T7_F299.md` | 9/0 | appends the "Amendment — DECISION F299 D1" section |
| `.agent/f299_inventory.md` | 154/0 | NEW FILE — T001's measurement of the three scratch targets, copied from the prepared file |

### `426a3dceb` F299 R2 C3: the module that finds a project's own test command and environment (T002, DECISION F299 D1)

| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/project_tests.py` | 243/0 | NEW FILE — `find_project_test_command`, `project_environment`, `project_python`, `project_lookup_dirs`, `find_virtualenv`, `find_node_bin`, `read_configured_command`, `ProjectTestCommand`, `ProjectTestConfigError` |
| `tests/orchestration/test_project_tests.py` | 241/0 | NEW FILE — the order, the npm placeholder/blank/unparseable cases, the pytest-argv pin, `read_configured_command`'s five error cases, the real-`git worktree`-backed environment-lookup tests |

Taken from round 1's stashed draft (`stash@{0}`), read whole against the block's C3 spec and
corrected in one place (see Deviations & assumptions), then committed.

### `aa4bcb597` F299 R2 C4: the check kind project_tests, run in the project's environment, as the contract's default check (T002, DECISION F299 D1)

| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/dod_runners.py` | 84/19 | `REASON_NO_TEST_COMMAND`/`REASON_TEST_COMMAND_INVALID`; `_spawn_check` extracted with `env_overlay`; new `_run_project_tests`; `RUNNER_REGISTRY["project_tests"]` |
| `packages/orchestration/dod_schema.py` | 6/1 | `CheckKind` gains `"project_tests"`; `_SPEC_KEYS["project_tests"] = frozenset()` |
| `packages/orchestration/exec_guard.py` | 13/3 | `dod_process_exec_policy`/`run_guarded_dod_process_command` gain `env_overlay` |
| `packages/orchestration/mission_contract.py` | 15/2 | `compile_contract_criteria` remaps the compiler's `pytest`/`tests` fallback to `project_tests`/`{}` |
| `tests/cli/test_do_sequence_cli.py` | 2/2 | the two asserts reading a contract check's kind as `pytest` now read `project_tests` |
| `tests/orchestration/import_reachability_allowlist.txt` | 1/0 | adds `packages.orchestration.project_tests` — reachable only from this commit on (see Deviations & assumptions) |
| `tests/orchestration/test_contract_templates.py` | 3/2 | the no-check-line criterion now compiles to `project_tests` |
| `tests/orchestration/test_dod_runners.py` | 157/4 | `TestProjectTestsKind` (no-command, disallowed-executable, broken-config, tests-folder-via-stand-in, real Python target + red pytest control, real Node target pass/fail); `RUNNER_REGISTRY` set test; the seam stand-in's `env_overlay` keyword |
| `tests/orchestration/test_exec_guard.py` | 21/0 | the overlay-cannot-unset-the-bytecode-key test |
| `tests/orchestration/test_mission_contract.py` | 9/0 | a no-test-path criterion compiles to `project_tests`/`{}` |

### This commit (self-reference) — F299 R2 C5: handback

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | this commit | this file |

## External actions

- `git stash pop stash@{0}` after C2, applied cleanly (no conflicts) — recovered round 1's C3/C4
  draft for review and commit as C3 and C4.
- `git push origin feature/f299-acceptance-checks-other-repos` after C5 — reported in the worker's
  final reply.
- No `gh pr create`, no `gh pr merge`, no worktree add/remove outside the gate-5/gate-1 measurement
  scripts' own scratch targets (under `.remedy-wt/f299-r2-worker/`), no mutation, no force-push, no
  stash entry other than `stash@{0}` touched.

## Verification

**Gate 1** (after C0, before C1), from the primary checkout:
```
python3 -B /home/decodeux/Repos/remedy/.remedy-wt/f299-r2/measure.py .../scratch .../measure-base.txt
```
Exit 0. `measure-base.txt` == `dry-measure.txt` byte-for-byte: **True** (the reviewer's
re-captured reference is now reproducible; round 1's staleness is gone).

**Gate 2** (after C4): `git status --porcelain` empty; C2 step 2's six byte-equality proofs
re-run at `aa4bcb597`, all **True** (decisions.md, prose_slips.md, and the four copied+1 new state
files each equal their prepared file).

**Gate 3** (once, after C4):
```
python3 -m pytest -q -rfEs @/home/decodeux/Repos/remedy/.remedy-wt/f299-r2/selection.txt
```
Exit 0. `4594 passed, 9 skipped in 319.82s (0:05:19)`. No FAILED or ERROR line. The 9 SKIPPED
lines, verbatim:
```
SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252): .claude/agents/remedy-reviewer.md was deleted deliberately in 219dd32 (finding R-0074 — superseded by the split workflow's Window 1, docs/agents/planner_reviewer_prompt.md). The read-only reviewer contract now lives there. Backlog: re-pin this contract on the split-workflow docs, or retire the test.
SKIPPED [1] tests/test_install_smoke.py:175: install smoke is opt-in: set REMEDY_INSTALL_SMOKE=1 on a host with network access
SKIPPED [1] tests/test_repair_context_reviewer_memory.py:257: UI source not found
SKIPPED [1] tests/regression/test_named_bugs.py:295: D3 quarantine (F252): the pre-rebuild apps/ui legacy/*.tsx sources this asserts are not in the tree; the UI is rebuilt in Tier 5 (F019+). Backlog: Tier 5 UI build (F019+).
SKIPPED [1] tests/regression/test_named_bugs.py:312: D3 quarantine (F252): the pre-rebuild apps/ui legacy/*.tsx sources this asserts are not in the tree; the UI is rebuilt in Tier 5 (F019+). Backlog: Tier 5 UI build (F019+).
SKIPPED [1] tests/regression/test_named_bugs.py:321: D3 quarantine (F252): the pre-rebuild apps/ui legacy/*.tsx sources this asserts are not in the tree; the UI is rebuilt in Tier 5 (F019+). Backlog: Tier 5 UI build (F019+).
SKIPPED [1] tests/regression/test_named_bugs.py:383: D3 quarantine (F252): the pre-rebuild apps/ui legacy/*.tsx sources this asserts are not in the tree; the UI is rebuilt in Tier 5 (F019+). Backlog: Tier 5 UI build (F019+).
SKIPPED [1] tests/regression/test_named_bugs.py:392: D3 quarantine (F252): the pre-rebuild apps/ui legacy/*.tsx sources this asserts are not in the tree; the UI is rebuilt in Tier 5 (F019+). Backlog: Tier 5 UI build (F019+).
SKIPPED [1] tests/regression/test_named_bugs.py:399: D3 quarantine (F252): the pre-rebuild apps/ui legacy/*.tsx sources this asserts are not in the tree; the UI is rebuilt in Tier 5 (F019+). Backlog: Tier 5 UI build (F019+).
```
All 9 are pre-existing quarantines unrelated to this round's files.

**Gate 4**:
```
python3 -m ruff check packages/orchestration/project_tests.py packages/orchestration/dod_runners.py packages/orchestration/dod_schema.py packages/orchestration/exec_guard.py packages/orchestration/mission_contract.py tests/orchestration/test_project_tests.py tests/orchestration/test_dod_runners.py tests/orchestration/test_exec_guard.py tests/orchestration/test_mission_contract.py tests/orchestration/test_contract_templates.py tests/cli/test_do_sequence_cli.py
```
Exit 0. `All checks passed!`

**Gate 5** (after C4, same measurement on the new code): exit 0; the file in full:
```
order: Write a CONTRIBUTING.md
command: python3 -m apps.cli.main do run <order> --repo <target> --json --no-llm --no-ui --yes --builder-provider fake --reviewer-provider fake

## target python
do exit code: 0
do ok: True
do unmet_blocking_criteria: []
template: None
criterion C001 origin=planner blocking=True status=met check={"acceptance_refs": ["C001:0"], "blocking": true, "description": "The mission goal is met in full: Write a CONTRIBUTING.md", "id": "ctr-C001", "kind": "project_tests", "source": "plan_acceptance", "spec": {}}
job state: completed
job workspace: <target>/.remedy-wt/job-<job>
  workspace holds .venv: False; node_modules: False
  target holds .venv: True
gate released: True
check ctr-C001 kind=project_tests blocking=False status=passed reason= exit=0
  command=<target>/.venv/bin/python -m pytest -p no:cacheprovider tests -q
  tail| .                                                                        [100%]
  tail| 1 passed in <secs>
push refusals: []
push still open: []

## target node
do exit code: 0
do ok: True
do unmet_blocking_criteria: []
template: None
criterion C001 origin=planner blocking=True status=met check={"acceptance_refs": ["C001:0"], "blocking": true, "description": "The mission goal is met in full: Write a CONTRIBUTING.md", "id": "ctr-C001", "kind": "project_tests", "source": "plan_acceptance", "spec": {}}
job state: completed
job workspace: <target>/.remedy-wt/job-<job>
  workspace holds .venv: False; node_modules: False
  target holds .venv: False
gate released: True
check ctr-C001 kind=project_tests blocking=False status=passed reason= exit=0
  command=npm test
  tail| # todo 0
  tail| # duration_ms 41.521256
push refusals: []
push still open: []

## target no-tests
do exit code: 0
do ok: True
do unmet_blocking_criteria: ['C001']
template: None
criterion C001 origin=planner blocking=True status=unmet check={"acceptance_refs": ["C001:0"], "blocking": true, "description": "The mission goal is met in full: Write a CONTRIBUTING.md", "id": "ctr-C001", "kind": "project_tests", "source": "plan_acceptance", "spec": {}}
job state: completed
job workspace: <target>/.remedy-wt/job-<job>
  workspace holds .venv: False; node_modules: False
  target holds .venv: False
gate released: True
check ctr-C001 kind=project_tests blocking=False status=failed reason=no_test_command exit=None
  command=
  tail| the project names no test command: no 'command' in the [tests] table of its .remedy/config.toml, no 'test' script in its package.json and no 'tests' folder, so no check ran
push refusals: ["The mission's blocking contract criteria C001 are unmet, so nothing is pushed."]
push still open: []
```
Matches the block's expectation exactly: python and node `status=met` with `kind=project_tests`
(python command beginning `<target>/.venv/bin/python -m pytest`, node command `npm test`);
no-tests `status=unmet` with `reason=no_test_command`.

**Gate 6**:
```
python3 -m apps.cli.main integrity check --json
```
Exit 0: six checks `pass`, `"fail_count": 0`.
```
python3 -c "import scripts.rotate_live_review as r; print(r.open_finding_ids(open('.agent/live_review.md').read()))"
```
`['R-1138', 'R-1139', 'R-1143', 'R-1149', 'R-1156', 'R-1157', 'R-1158', 'R-1160', 'R-1162', 'R-1172', 'R-1176', 'R-1196', 'R-1219', 'R-1220', 'R-1225']` — matches exactly.

## Authored-text proofs

`.agent/authored/f299-r2.md` (the saved block, C1) equals `block.md` byte for byte: sha256
`61d527520b2b3cda824ef0560a370427f8263931c507b558c6481e47061e9e84` on both sides, 310 lines each.
No other reviewer-authored text (as distinct from the prepared state files proved in C2 step 2 and
re-proved at gate 2) was applied this round.

## Deviations & assumptions

- **C0**: all of C0's checks (HEAD at `5eaca8c78`, `git status --porcelain` empty, `.agent/STOP`
  absent, `stash@{0}`'s message, the branch name before every commit) held exactly as the block
  states; no write happened before they and gate 1 were done.
- **The reachability allowlist line (C3 vs. C4), measured rather than assumed**: the block orders
  "add the line in C3 only if `tests/orchestration/test_import_reachability.py` already needs it
  then, else in C4." Before committing C3, this round computed the D11 (c) reachable closure with
  every OTHER production file held at its round-base (`5eaca8c78`) blob — i.e. with
  `project_tests.py` existing but `dod_runners.py` not yet importing it — and
  `packages.orchestration.project_tests` was **not** in that closure (321 modules total, module
  absent). So the line was committed in C4 (where `dod_runners.py`'s new import makes the module
  reachable), not C3. This is the block's own stated contingency resolved by measurement, not a
  departure from it.
- **One correction to round 1's stashed C3/C4 draft**: the draft was read whole against the
  block's full C3 and C4 spec, line by line (module docstring and order, every public name's WHY
  comment, `project_lookup_dirs`'s git-call shape and resolution against `worktrees.ensure_ignored`,
  the environment/interpreter functions, `read_configured_command`'s error cases,
  `find_project_test_command`'s order, every C4 change to `dod_schema.py`/`exec_guard.py`/
  `dod_runners.py`/`mission_contract.py`, and every ordered test). It matched the spec everywhere
  but one stylistic point: `tests/orchestration/test_project_tests.py::test_a_string_command_is_refused`
  carried `assert str(path.relative_to(tmp_path)) in str(exc.value) or ".remedy/config.toml" in
  str(exc.value)` — both branches are the identical string on POSIX (`.remedy/config.toml`), so the
  `or` was a tautology. Simplified to the single `assert ".remedy/config.toml" in str(exc.value)`
  the other four `read_configured_command` tests already use. No behavior change; the same code
  path and the same message content are still exercised.
- **Gates**: all six gates ran exactly as the block ordered, in order, each green on its first and
  only run; none was rerun.

## Round verdicts

F253's round 38 (PASS) and F299's round 1 (FAIL) are booked into `.agent/live_review.md` by C2, as
the gate entries `Gate: F253 R38` and `Gate: F299 R1`. Round 2's own verdict is the reviewer's, not
yet written.

## For the operator, in plain sentences

The public web interface feature is merged into the main line after both of GitHub's checks
passed. The new feature makes the checks of a mission work on a project that is not Remedy itself.
Until now such a check always ran Remedy's own Python test command with Remedy's own Python, so a
Python project with its own environment, a JavaScript project and a project without tests were all
judged as failing. This round measured that on three small sample projects and made the check run
the project's own command, found in a small settings file of the project, else in its
`package.json`, else in its `tests` folder, with the project's own environment. A project with no
tests is still marked as failing until the next round. The round's first attempt stopped at its
first check because the reviewer had saved an out-of-date copy of a measurement, which is
corrected. Nothing waits for the operator.

## Next

1. Phase 1 rule 1 (`.agent/STOP`): if it appears, finish the commit in hand, write the handback and
   stop.
2. Phase 1 rule 2 (the Open PR Gate):
   `gh pr list --state open --json number,headRefName,baseRefName,isDraft` before any further
   branch work.
3. Book round 2's verdict in the next round's first commit.
4. T003: a criterion state that reads "no check ran", its words, and its push rule.

Operator questions open: 0.
Open findings: 15 (R-1160, Medium; R-1138, R-1139, R-1143, R-1149, R-1156, R-1157, R-1158, R-1162,
R-1172, R-1176, R-1196, R-1219, R-1220 and R-1225, Low; all owned by F297).

## Item status

| Item | Status | Reason |
|---|---|---|
| C0: base checks + gate 1 | done | HEAD, status, STOP, stash message and branch all confirmed before any write; gate 1 green on the re-captured reference |
| C1: save the block | done | `.agent/authored/f299-r2.md`, byte- and line-identical to `block.md` |
| C2: claim, book F253 R38 + F299 R1, T001, DECISION D1, plan | done | all copies and appends byte-proved against the prepared files |
| C3: `project_tests` module + tests | done | taken from `stash@{0}`, reviewed whole, one stylistic correction, committed |
| C4: check kind `project_tests` + contract remap + tests | done | taken from `stash@{0}`, reviewed whole, no correction needed, committed with the reachability allowlist line |
| C5: handback | done | this commit |
| Gate 1 | passed | `measure-base.txt` == `dry-measure.txt`, byte for byte |
| Gate 2 | passed | status clean; all C2 byte proofs True at `aa4bcb597` |
| Gate 3 | passed | `4594 passed, 9 skipped`, no FAILED/ERROR |
| Gate 4 | passed | `ruff check` clean |
| Gate 5 | passed | python/node `met`/`project_tests`, no-tests `unmet`/`no_test_command`, exactly as expected |
| Gate 6 | passed | integrity six-for-six; open findings list matches |
| Push | done | reported in the worker's final reply |
