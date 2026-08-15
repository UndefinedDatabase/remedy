# F083 T001 — Marker Inventory (measured 2026-08-15, R2)

Every number below was produced by a command run in this round at
928120ab..HEAD, and the command stands next to the number. Nothing here is
estimated; a value that was not measured would read `not-measured`, and no such
value occurs. Collected counts are the count of node-id lines in
`python3 -m pytest --collect-only -q` output, i.e. lines containing `::` and not
starting with a space, counted in Python — never parsed out of the summary line.

## Q1 — Which markers exist, and who assigns them

DECLARATION SITE: `pyproject.toml`, table `[tool.pytest.ini_options]`, key
`markers`. Nine markers are declared; the descriptions are the declared strings:

| Marker | Declared description |
|---|---|
| `unit` | Pure logic tests, no I/O, no subprocess, no network |
| `integration` | Tests with temp files, storage, orchestration state |
| `subprocess` | Tests that spawn child processes (CLI, runtime) |
| `smoke` | Smoke contract tests for scripts and infrastructure |
| `slow` | Tests that take >5s individually |
| `real_ollama` | Requires running Ollama server (opt-in via env) |
| `ui_contract` | Python-verifiable frontend/UI contracts |
| `safety` | Resource safety and process isolation guards |
| `architecture` | Structural guards (no step files, imports, namespaces) |

ASSIGNED AUTOMATICALLY AT COLLECTION by `tests/conftest.py`, function
`pytest_collection_modifyitems`. It is the only automatic assigner in the
repository. Measured two ways: `git ls-files | grep conftest` returns exactly two
tracked conftest files, `tests/conftest.py` and
`scripts/gauntlet_sample_project/conftest.py`, and the second one only inserts a
`sys.path` entry and defines no hook; and `git grep -n
'pytest_collection_modifyitems'` returns three hits, of which the only DEFINITION
is `tests/conftest.py` — the other two are a prose mention in
`.agent/f077_t002_inventory.md` and a string literal in
`tests/orchestration/test_job_fulfillment.py` that writes a conftest into a
throwaway temp repo. Its rules, read from that function:

| Marker | Rule | Data symbol (all in `tests/conftest.py`) |
|---|---|---|
| `ui_contract` | `"ui_contracts" in item.path.parts` | — (directory test) |
| `integration` | `"ui_server" in item.path.parts`; PLUS the fallback `"orchestration" or "storage" in parts` when the item has no closest `subprocess`/`real_ollama`/`smoke` marker | — (directory test) |
| `subprocess` | `item.path.name in SUBPROCESS_FILES` | `SUBPROCESS_FILES` — 23 written entries, 22 unique (`test_test_runner.py` is written twice, once commented `# orchestration/` and once `# root level`) |
| `real_ollama` | `item.path.name in REAL_OLLAMA_FILES` | `REAL_OLLAMA_FILES` — 3 entries |
| `smoke` | `item.path.name in SMOKE_FILES` | `SMOKE_FILES` — 3 entries |
| `safety` | `item.path.name in SAFETY_FILES` | `SAFETY_FILES` — 3 entries |
| `architecture` | `item.path.name in ARCHITECTURE_FILES` | `ARCHITECTURE_FILES` — 4 entries |

Entry counts measured by parsing the five set literals out of `tests/conftest.py`
with a Python `re.findall(r'"([^"]+)"', ...)` over each `NAME = { ... }` body and
comparing `len(items)` with `len(set(items))`.

REACHED ONLY THROUGH EXPLICIT TEST-SIDE MARKING — the two markers
`pytest_collection_modifyitems` never adds:

- `unit`. Measured with
  `git grep -rhoE '@pytest\.mark\.[a-zA-Z_]+' -- tests scripts | sort | uniq -c | sort -rn`
  → `48 @pytest.mark.unit`, plus module-level `pytestmark = pytest.mark.unit` in
  `tests/orchestration/test_context_compiler.py` and
  `tests/orchestration/test_run_report.py` (measured with
  `git grep -n 'pytestmark' -- tests scripts`).
- `slow`. The same two greps find NO `@pytest.mark.slow` anywhere and exactly one
  writer: the module-level `pytestmark = [pytest.mark.subprocess, pytest.mark.slow]`
  in `tests/runtimes/test_apps_ui_probe.py`. That single line is the whole
  population of the `slow` marker, which Q2 measures at 7 — all 7 node ids are in
  that file.

Markers reached BOTH ways: `subprocess` (10 decorator occurrences, plus
module-level `pytestmark` in `tests/runtimes/test_apps_ui_probe.py`,
`tests/runtimes/test_runtime_cli_process_boundary.py` and
`tests/runtimes/test_supervisor_portability.py`) and `integration` (module-level
`pytestmark` in `tests/cli/test_job_report.py` and
`tests/orchestration/test_run_report_hook.py`, on top of the automatic rule).

Markers with ZERO explicit marking anywhere under `tests/` or `scripts/` —
`smoke`, `real_ollama`, `ui_contract`, `safety`, `architecture`. Asserted from the
two greps above, whose full output is the five-row `uniq -c` table
(`parametrize` 286, `unit` 48, `skipif` 21, `skip` 11, `subprocess` 10) and the
fifteen-line `pytestmark` list; none of the five names appears in either.

RECORDED DISAGREEMENT, not resolved here: the comment above the fallback rule in
`pytest_collection_modifyitems` reads "Default: if no specific mark, it's unit or
integration", but the code under it adds `pytest.mark.integration` only. No code
path anywhere adds `pytest.mark.unit`. The comment over-promises; the 208 `unit`
items of Q2 are all explicitly marked.

## Q2 — Collected count per marker, and the suite total

Command per row: `python3 -m pytest -m "<MARKER>" --collect-only -q`, node-id
lines counted in Python. Total row: `python3 -m pytest --collect-only -q`.
Every one of the ten runs returned exit code 0, read from the `CompletedProcess`
object and not from a pipe.

| Selection | Collected |
|---|---|
| `unit` | 208 |
| `integration` | 10961 |
| `subprocess` | 1585 |
| `smoke` | 23 |
| `slow` | 7 |
| `real_ollama` | 79 |
| `ui_contract` | 397 |
| `safety` | 33 |
| `architecture` | 71 |
| WHOLE SUITE (no `-m`) | 17007 |

The nine marker counts sum to 13364, which is smaller than 17007 and larger than
any single row: the markers neither partition nor cover the suite, and 3970 items
(Q4's `fast`) carry none of the six markers `fast` excludes.

## Q3 — The feature file's five names against disk

`docs/roadmap/features/T2_F083.md` names "integration, subprocess, ui-contract,
live-provider, smoke". Measured with the declared marker list of Q1 plus two
greps restricted to the code and doc trees, so that this round's own `.agent/`
scratch cannot pad the answer:

    git grep -l -- 'ui-contract'   -- pyproject.toml tests packages apps scripts docs
    git grep -l -- 'live-provider' -- pyproject.toml tests packages apps scripts docs

The first returns one file, `docs/roadmap/features/T2_F083.md`. The second
returns two, `docs/roadmap/ROADMAP.md` and
`docs/roadmap/features/T2_F083.md`. Neither hyphenated name occurs in
`pyproject.toml`, in `tests/`, in `packages/`, in `apps/` or in `scripts/` — both
exist only as roadmap prose.

| Feature-file name | Exists on disk as a marker? | Where |
|---|---|---|
| `integration` | YES | `pyproject.toml` `[tool.pytest.ini_options] markers`; assigned in `tests/conftest.py::pytest_collection_modifyitems` |
| `subprocess` | YES | same declaration site; same assigner plus explicit marking |
| `ui-contract` | NO — no marker of that spelling | its only hit outside `.agent/` scratch is the feature file's own sentence; the marker that exists is `ui_contract`, underscore, declared in `pyproject.toml` |
| `live-provider` | NO — no marker of that spelling | its only hits outside `.agent/` scratch are `docs/roadmap/ROADMAP.md` and the feature file; none is in `pyproject.toml`, `tests/conftest.py` or any test file |
| `smoke` | YES | `pyproject.toml` declaration; assigned from `tests/conftest.py::SMOKE_FILES` |

THE MARKER THAT CARRIES THE LIVE-PROVIDER ROLE is `real_ollama`, declared in
`pyproject.toml` as "Requires running Ollama server (opt-in via env)", assigned
automatically from `tests/conftest.py::REAL_OLLAMA_FILES`
(`test_real_ollama_smoke.py`, `test_real_do_ollama_smoke.py`,
`test_builder_eval.py`), and run by `scripts/remedy_test_real_providers.sh`,
which exports `REMEDY_REAL_OLLAMA_SMOKE=1` and `REMEDY_REAL_OLLAMA_EVAL=1` behind
the opt-in `REMEDY_RUN_REAL_OLLAMA=1` and selects `-m real_ollama`.

The disagreement is recorded, not resolved: the feature file's two hyphenated
names have no counterpart in code, and R3 must pick the code's spellings
(`ui_contract`, `real_ollama`) or change the feature file in its own diff.

## Q4 — The five candidate selections: counts, coverage, disjointness

Command per row: `python3 -m pytest -m "<EXPRESSION>" --collect-only -q`,
node-id lines written to a file per selection. All five returned exit code 0.

| Stage | Selection expression | Collected |
|---|---|---|
| fast | `not integration and not subprocess and not real_ollama and not ui_contract and not smoke and not slow` | 3970 |
| standard | `(integration or subprocess) and not real_ollama` | 12546 |
| ui | `ui_contract and not real_ollama` | 397 |
| smoke | `smoke and not real_ollama` | 23 |
| excluded | `real_ollama` | 79 |

COVERAGE, computed over the collected NODE IDS as Python sets (union of the five
files against the whole-suite file):

- union size 17007; whole-suite collected 17007; UNCOVERED node ids: 0, so the
  uncovered list is empty.
- the union contains no node id absent from the whole suite (0), so the five
  selections neither miss nor invent an item.

DISJOINTNESS, all ten pairs, sizes measured from the same sets:

| Pair | Overlap size |
|---|---|
| fast ∩ standard | 0 |
| fast ∩ ui | 0 |
| fast ∩ smoke | 0 |
| fast ∩ excluded | 0 |
| standard ∩ ui | 0 |
| standard ∩ smoke | 8 |
| standard ∩ excluded | 0 |
| ui ∩ smoke | 0 |
| ui ∩ excluded | 0 |
| smoke ∩ excluded | 0 |

The five are therefore NOT disjoint. The single overlap is
`standard ∩ smoke` = 8 node ids, all in one file, `tests/cli/test_pytest_runner.py`:
`test_runner_exists`, `test_runner_failing_pytest`, `test_runner_no_shell_true`,
`test_runner_passing_pytest`, `test_runner_timeout_returns_124`,
`test_runner_uses_devnull`, `test_runner_uses_start_new_session`,
`test_runner_uses_temp_files`. Cause, read from `tests/conftest.py`: that
filename is written into BOTH `SUBPROCESS_FILES` and `SMOKE_FILES`, so the item
carries `subprocess` and `smoke` at once and satisfies both expressions.

The arithmetic closes: 3970 + 12546 + 397 + 23 + 79 = 17015, and
17015 − 17007 = 8, exactly the one overlap.

## Q5 — Measured wall time and outcome per stage

Every stage was launched from a Python driver with
`subprocess.run([sys.executable, '-m', 'pytest', ...], cwd=REPO, capture_output=True)`;
the exit code is `CompletedProcess.returncode` and the duration is
`time.time()` around that call. No pipe was used to derive an exit code
(R-0438). The six runs are serial with respect to one another; only `standard`
used `-n auto`, as ordered.

| Stage | Exact command | Exit | Collected | Passed | Failed | Skipped | Wall time |
|---|---|---|---|---|---|---|---|
| fast | `python3 -m pytest -m "not integration and not subprocess and not real_ollama and not ui_contract and not smoke and not slow" -q` | 0 | 3970 | 3963 | 0 | 7 | 391.8 s (driver) / 390.40 s (pytest) |
| ui | `python3 -m pytest -m "ui_contract and not real_ollama" -q` | 0 | 397 | 393 | 0 | 4 | 8.1 s / 6.92 s |
| smoke | `python3 -m pytest -m "smoke and not real_ollama" -q` | 0 | 23 | 22 | 0 | 1 | 11.1 s / 9.88 s |
| safety | `python3 -m pytest -m "safety and not real_ollama" -q` | 0 | 33 | 33 | 0 | 0 | 19.4 s / 17.82 s |
| architecture | `python3 -m pytest -m "architecture and not real_ollama" -q` | 0 | 71 | 71 | 0 | 0 | 4.8 s / 3.60 s |
| standard | `python3 -m pytest -m "(integration or subprocess) and not real_ollama" -q -n auto` | 0 | 12546 | 12545 | 0 | 1 | 134.1 s / 133.71 s |

Collected is derived, not guessed: pytest's own tail line gives passed + skipped
and a `deselected` count, and for all five SERIAL stages
passed + skipped + deselected = 17007 exactly — matching Q4's counts for `fast`,
`ui` and `smoke` and Q2's counts for `safety` and `architecture`. The `standard`
tail under `-n auto` prints no deselected figure; its 12545 + 1 = 12546 equals
Q4's collected count for that selection.
DECISION F083 D1 was therefore never exercised — no stage was red, every exit
code is 0, and the total failed count across all six runs is 0.

Sum of the six wall times as the driver measured them: 569.3 s. The serial five
alone are 435.2 s, of which `fast` is 391.8 s — `fast` is the slowest stage in
the repository by an order of magnitude and it is the one the feature file calls
"pure unit". `standard` runs 12546 items in 134.1 s under `-n auto` while `fast`
runs 3970 items in 391.8 s serially; the split as named is inverted with respect
to cost.

THE `excluded` STAGE WAS NOT RUN. Reason: its selection is `real_ollama`, whose
79 items require a running Ollama server and are opt-in by environment
(`pyproject.toml`: "Requires running Ollama server (opt-in via env)"), and the
feature file lists live-provider suites as deliberately excluded from CI. The
exact command an operator would use is the repository's own wrapper:

    REMEDY_RUN_REAL_OLLAMA=1 scripts/remedy_test_real_providers.sh

which internally exports `REMEDY_REAL_OLLAMA_SMOKE=1` and
`REMEDY_REAL_OLLAMA_EVAL=1` and runs
`scripts/remedy_pytest.sh tests/ -q --cache-clear -m real_ollama`.

## Q6 — Does a `ci` command already exist?

NO. These greps were run this round and every one produced empty output:

    git grep -n -- '"ci"' -- apps packages scripts tests
    git grep -nE 'command_id="ci|GroupDef\("ci|def ci_|ci_cmd' -- apps packages scripts tests
    git grep -rn --name-only -iE 'ci_cmd|def cmd_ci|remedy ci' -- apps packages scripts tests

plus a path scan over `git ls-files apps packages scripts tests` (1082 tracked
files) filtered in Python by `re.search(r'(^|/)ci([._-]|$)', p, re.I)` → 0 hits.
`apps/cli/command_catalog.py::GROUPS` holds no `ci` group; the file
`tests/cli/test_ci_cmd.py` the feature file suggests does not exist.

## Q7 — Do hosted workflow files exist?

NO. Checked `.github/` and `.github/workflows/` with `ls -la`: both report
"No such file or directory" — the repository has no `.github` directory at all.
A `find . -maxdepth 3 -name '*.yml' -o -maxdepth 3 -name '*.yaml'` outside
`node_modules` and `.data` returned nothing. There is no hosted CI configuration
of any kind to mirror or migrate; T003 starts from zero.

## Q8 — What the stage runner must reuse rather than reimplement

- RUNS PYTEST AS A SUBPROCESS TODAY: `scripts/remedy_pytest_runner.py`, function
  `run(pytest_args)`. It uses `subprocess.Popen` with `start_new_session=True`,
  redirects stdout/stderr to temp files instead of inherited pipes, caps output
  at `MAX_OUTPUT_BYTES` (512 KiB per stream) and kills the process group on
  timeout via `_kill_pg` / `_ensure_pg_dead`; `REMEDY_PYTEST_TIMEOUT_SEC`
  (default 600) is its budget knob and exit 124 is its timeout code. Its shell
  front door is `scripts/remedy_pytest.sh`, which adds an `flock` lock so two
  pytest runs cannot overlap on one machine. A stage runner that shells out to
  bare `pytest` would lose the process-group cleanup, the pipe safety and the
  lock in one step.
- NOT the same thing, and named here so R3 does not confuse them:
  `packages/orchestration/test_runner.py`, function `run_tests_local(job,
  workspace_root, *, timeout_sec=60)` with its `TestRunRecord` dataclass, runs a
  DISCOVERED test command inside a TARGET repository under a closed executable
  allowlist. It is Remedy-acting-on-a-customer-repo, not Remedy testing itself.
- CLI COMMAND-REGISTRATION SEAM: three symbols, in this order.
  `apps/cli/command_catalog.py::GROUPS` (a `dict[str, GroupDef]`) declares the
  group; `apps/cli/command_catalog.py::CATALOG` (a `tuple[CommandEntry, ...]`)
  declares each subcommand with its `ArgDef` list and `action_class`; a new
  module under `apps/cli/commands/` exposes
  `COMMAND_HANDLERS: dict[str, Callable[[argparse.Namespace], None]]` and is
  imported inside `apps/cli/commands/__init__.py::collect_all_handlers`, which
  merges every module's table with `table.update(mod.COMMAND_HANDLERS)`.
  `apps/cli/grouped.py::_get_dispatch_table` reads that merged table, and
  `pyproject.toml` `[project.scripts]` binds `remedy = "apps.cli.grouped:main"`.
  `apps/cli/commands/bench_cmd.py` is the most recent worked example of the
  whole seam.
- PARALLEL EXECUTION: `pytest-xdist`, version 3.8.0, measured with
  `python3 -m pip show pytest-xdist`; declared in `pyproject.toml`
  `[project.optional-dependencies] dev`. pytest itself is 9.0.3
  (`python3 -m pytest --version`). `-n auto` is what `standard` used in Q5.
- EXISTING LANE SCRIPTS the runner should absorb or supersede rather than
  duplicate: `scripts/remedy_test_fast.sh` (a hardcoded EIGHT-FILE list, not a
  marker selection — it does not correspond to Q4's `fast`),
  `scripts/remedy_test_integration.sh` (three smoke supervisors, then
  `-m "not real_ollama and not slow"`), `scripts/remedy_test_full.sh`,
  `scripts/remedy_test_runtime.sh` (per-node timeouts and a stale-process sweep)
  and `scripts/remedy_test_real_providers.sh` (the excluded lane).
  `tests/test_test_categories.py` already asserts properties of these scripts and
  of the marker declarations in `pyproject.toml`.

LOOKED FOR AND DID NOT FIND, each from a command recorded above: a `.github/`
directory or any workflow file (Q7); any `ci` command, module, group or test file
(Q6); a `determinism` marker and a `budgets` marker — neither name appears in the
nine declared markers in `pyproject.toml`, although the feature file's suggested
shape names both as stages; and `tests/cli/test_ci_cmd.py`, the test path the
feature file suggests.

## OPEN QUESTIONS — what R3 cannot decide from this data

1. Whether the `standard ∩ smoke` overlap of 8 should be removed (by dropping
   `test_pytest_runner.py` from one conftest set) or accepted and documented.
   Removing it edits marker semantics, which the feature file's Do-not-touch list
   forbids.
2. Where `safety` (33) and `architecture` (71) belong. Q5 timed them as separate
   stages, but they are already inside Q4's five: measured as set intersections
   over the same collected node ids, `safety` splits 21 into `fast` and 12 into
   `standard`, and all 71 `architecture` items sit in `fast`. Promoting either to
   a stage of its own would create overlaps Q4 does not currently have — and
   `safety` would straddle two stages.
3. What to do about `fast` costing 391.8 s while `standard` costs 134.1 s. Whether
   the answer is `-n auto` for `fast` too, a different selection, or a renamed
   stage, is a design decision this inventory deliberately does not make.
4. Whether the `determinism` and `budgets` stages the feature file names become
   marker selections (requiring new markers, i.e. a marker-semantics change) or
   script invocations outside the marker system.
5. Whether the feature file's `ui-contract` / `live-provider` spellings get
   corrected to `ui_contract` / `real_ollama`, or the markers get renamed.
6. What the documented runtime budget should be. This round measured one machine,
   once, with an unrelated stale process present; a budget needs a repeat and a
   hosted reading, and no hosted runner exists yet (Q7).
