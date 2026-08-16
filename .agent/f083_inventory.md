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

## Q9 — Stage runtime, measured at R11

Every reading below was taken at R11 from the repository root by a Python driver
calling `subprocess.run([sys.executable, "-m", "pytest", ...], cwd=REPO,
capture_output=True)` DIRECTLY — never through `scripts/remedy_pytest_runner.py`,
whose default timeout would truncate the serial `fast` reading. The exit code is
`CompletedProcess.returncode` read from that process (R-0438); the wall time is
`time.monotonic()` around the call. Marker expressions were READ from `CI_STAGES`
in `packages.orchestration.ci_stages`, never retyped. `os.cpu_count()` on this
machine reports 24 — the number `-n auto` resolves against, without which the
parallel readings mean nothing.

COLLECTED PER STAGE, via
`python3 -m pytest --collect-only -q -p no:cacheprovider -m "<expression>"`:

| Stage | Collected | Deselected | Suite total | Exit |
|---|---|---|---|---|
| fast | 3975 | 13070 | 17045 | 0 |
| standard | 12579 | 4466 | 17045 | 0 |
| ui | 397 | 16648 | 17045 | 0 |
| smoke | 23 | 17022 | 17045 | 0 |
| excluded | 79 | 16966 | 17045 | 0 |

The instrument can go red: the same command with `-m "no_such_marker_at_all"`
exits 5 and its last line is `no tests collected (17045 deselected) in 3.42s`, so
an empty selection is distinguishable from a green one and the timings below are
readings rather than decoration.

WALL TIME AND OUTCOME. Each run was its own process, run serially with respect to
the others; the summary line is pytest's own final line, verbatim:

| Stage | Run | Wall (driver) | Exit | pytest summary line |
|---|---|---|---|---|
| fast | serial | 391.9 s | 0 | `3968 passed, 7 skipped, 13070 deselected in 390.53s (0:06:30)` |
| fast | `-n auto` | 55.4 s | 0 | `3968 passed, 7 skipped in 55.17s` |
| standard | `-n auto` | 138.8 s | 0 | `12578 passed, 1 skipped in 138.32s (0:02:18)` |
| ui | `-n auto` | 12.2 s | 0 | `393 passed, 4 skipped in 10.23s` |
| smoke | `-n auto` | 14.0 s | 0 | `22 passed, 1 skipped in 13.77s` |
| excluded | not run | not measured | not measured | not measured |

No summary line above names a failed count and every exit code read from the
process is 0. The serial wall time of `standard`, `ui` and `smoke` is `not
measured`: only `fast` was run both ways. `excluded` was NOT run — its selection
is `real_ollama`, which needs a live server — and its own `manual_command`, read
from the stage table, is:

    python3 -m pytest -m real_ollama -q  # needs a running Ollama server

THE DETERMINISM CANDIDATE SET. The glob `tests/orchestration/test_run_manifest_*.py`
matches 45 files, which collect 850 tests at exit 0. Containment was MEASURED as
a Python set operation over collected node ids — the 850 candidate ids against
the 12579 ids the `standard` selection collects — not reasoned about from
markers: the result is True with 0 ids outside `standard`.

THE TWO FACTS R12 NEEDS. Long pole: under `-n auto` on this 24-CPU machine
`standard` at 138.8 s is the slowest stage measured, while `fast` — the stage the
plan's standing risk names — costs 391.9 s serially and 55.4 s under `-n auto`.
Determinism set: the run-manifest suite already sits wholly inside `standard`,
containment True with 0 ids outside, so no new selection is required to run it.

This section is evidence and carries no recommendation and no budget number;
choosing the budget belongs to R12.

## Q10 — Serial stage cost through the production runner, measured at R13

INSTRUMENT, imported and never retyped. A Python driver run from the repository
root imports `CI_STAGES` and `CiStage` from `packages.orchestration.ci_stages`
and `run_ci_stage` and `stage_command` from `packages.orchestration.ci_run`.
Marker expressions were READ from `CI_STAGES`. Every sample is its own process
calling `run_ci_stage(stage, repo_root)` with the repository root as
`repo_root`; the exit code is the one that process returned (R-0438) and the
wall second is `run_ci_stage`'s own `duration_s`, i.e. `time.monotonic()` around
the call. The argv is `stage_command`'s own, verbatim, here for `standard`:

    ['/usr/bin/python3', '/home/decodeux/Repos/remedy/scripts/remedy_pytest_runner.py', '--', '-m', '(integration or subprocess) and not real_ollama', '-q']

RED CONTROL, run FIRST and before any timing sample: `CiStage(name="bogus",
description="red control", marker_expression="no_such_marker_at_all",
runs_in_ci=True, manual_command="")` through the same `run_ci_stage` returns
EXIT CODE 5, its whole output being the line `17045 deselected in 3.67s`. The
instrument can tell an empty selection from a green one, so the readings below
are readings and not decoration.

SAMPLES, three per stage, run one after another, with NO environment override —
at `scripts/remedy_pytest_runner.py`'s own 600-second `REMEDY_PYTEST_TIMEOUT_SEC`
default. One row per SAMPLE, never one per stage; nothing is averaged. The
summary line is pytest's own final line, verbatim, read from that sample's own
log file. No log came near `MAX_OUTPUT_BYTES` (512 KiB) — the largest is 14062
bytes — so no line below is quoted out of a truncated stream.

| Stage | Sample | Wall s | Exit | pytest's own final summary line |
|---|---|---|---|---|
| fast | 1 of 3 | 391.82 | 0 | `3968 passed, 7 skipped, 13070 deselected in 390.37s (0:06:30)` |
| fast | 2 of 3 | 391.07 | 0 | `3968 passed, 7 skipped, 13070 deselected in 389.65s (0:06:29)` |
| fast | 3 of 3 | 397.45 | 0 | `3968 passed, 7 skipped, 13070 deselected in 396.05s (0:06:36)` |
| standard | 1 of 3 | 600.06 | 124 | not measured — killed at the default, so pytest printed no final line |
| standard | 2 of 3 | 600.06 | 124 | not measured — killed at the default, so pytest printed no final line |
| standard | 3 of 3 | 600.06 | 124 | not measured — killed at the default, so pytest printed no final line |
| ui | 1 of 3 | 7.99 | 0 | `393 passed, 4 skipped, 16648 deselected in 6.73s` |
| ui | 2 of 3 | 8.09 | 0 | `393 passed, 4 skipped, 16648 deselected in 6.88s` |
| ui | 3 of 3 | 7.99 | 0 | `393 passed, 4 skipped, 16648 deselected in 6.75s` |
| smoke | 1 of 3 | 11.07 | 0 | `22 passed, 1 skipped, 17022 deselected in 9.84s` |
| smoke | 2 of 3 | 11.07 | 0 | `22 passed, 1 skipped, 17022 deselected in 9.85s` |
| smoke | 3 of 3 | 11.06 | 0 | `22 passed, 1 skipped, 17022 deselected in 9.84s` |
| excluded | not run | not measured | not measured | not run |

THE ANSWER TO THE QUESTION R13 EXISTED TO SETTLE: today's `remedy ci` TRUNCATES
its largest stage. All three `standard` samples returned 124 — `run_ci_stage`'s
`PYTEST_TIMEOUT_EXIT_CODE` — with the note `timed out`, and the last line of each
log is `ERROR: pytest timed out after 600 seconds.`. The last progress marker
each killed run printed was `[ 70%]`, `[ 73%]` and `[ 71%]` respectively; that is
where the kill landed, and no completion figure is derived from it here.

UNCAPPED PROBE, the ONLY run in this section that overrides the default: because
`standard` returned 124, one further sample was run with the environment variable
`REMEDY_PYTEST_TIMEOUT_SEC` set to `5400`. `fast`, `ui` and `smoke` returned no
124 in any sample, so no uncapped probe was run for them and none was needed.

| Stage | Sample | Wall s | Exit | pytest's own final summary line |
|---|---|---|---|---|
| standard | uncapped probe, REMEDY_PYTEST_TIMEOUT_SEC=5400 | 927.72 | 0 | `12578 passed, 1 skipped, 4466 deselected in 926.15s (0:15:26)` |

SPREAD, over the three default-timeout samples of each stage, min / max /
max-minus-min in seconds:

- fast — min 391.07, max 397.45, max−min 6.38.
- standard — min 600.06, max 600.06, max−min 0.01. All three are the runner's
  own kill, not the stage's cost, so this spread measures the timeout and not
  `standard`; the stage's own serial cost is measured once, by the uncapped
  probe above, and its spread is `not measured` at one sample.
- ui — min 7.99, max 8.09, max−min 0.10.
- smoke — min 11.06, max 11.07, max−min 0.01.

THE `excluded` STAGE WAS NOT RUN, and not by choice of the driver: its
`runs_in_ci` is False, so `run_ci_stage` returned `ran=False`, `exit_code=None`,
`duration_s=0.0` and the note it carries, without starting anything. The
`manual_command` read from the stage table is:

    python3 -m pytest -m real_ollama -q  # needs a running Ollama server

CONTEXT, measured this round and not recalled. `os.cpu_count()` reports 24 —
recorded because every `-n auto` reading in `## Q9` resolves against it, while
nothing in `## Q10` does. `python3 -m pytest --version` prints `pytest 9.0.3`
at exit code 0. `python3 -m ruff check .`, run from the repository root against
the repository's own `pyproject.toml` (`select = ["E", "F", "W", "I", "UP"]`,
`line-length = 120`, ruff 0.15.17), ends `Found 26 errors.` and
`[*] 25 fixable with the --fix option.` at EXIT CODE 1. Twenty-six is the lint
baseline R-0468 needs on the record before any lint gate can be written, and
recording it is the whole of what R13 does about R-0468.

This section is evidence. It carries no ceiling, no budget number and no
recommendation; choosing them from these samples is R14's work.

## Q11 — The three-sample serial cost of `standard`, completed at R14

INSTRUMENT, imported and never retyped. A Python driver run from the repository
root imports `CI_STAGES` and `CiStage` from `packages.orchestration.ci_stages`
and `run_ci_stage` and `stage_command` from `packages.orchestration.ci_run`. The
`standard` stage is READ from `CI_STAGES` by name and its marker expression is
never retyped. Every sample is its own process calling
`run_ci_stage(stage, repo_root)` with the repository root as `repo_root` and with
NO `run_command=` argument, so every sample really goes through the production
`_run_via_subprocess`; the exit code is the one that process returned (R-0438)
and the wall second is `run_ci_stage`'s own `duration_s`, i.e. `time.monotonic()`
around the call. The argv is `stage_command`'s own, verbatim:

    ['/usr/bin/python3', '/home/decodeux/Repos/remedy/scripts/remedy_pytest_runner.py', '--', '-m', '(integration or subprocess) and not real_ollama', '-q']

RED CONTROL, run FIRST and before either timing sample: `CiStage(name="bogus",
description="red control", marker_expression="no_such_marker_at_all",
runs_in_ci=True, manual_command="")` through the same `run_ci_stage` returns
EXIT CODE 5, its whole output being the line `17045 deselected in 3.47s`. The
instrument can tell an empty selection from a green one, so the readings below
are readings and not decoration.

PRECISION CONVENTION, binding on this section and stated on its face (R-0476):
every wall second is published at exactly two decimals, and every derived value
below — min, max, max−min — is computed from the numbers AS PUBLISHED in the
table, never from the unrounded `duration_s`. Subtracting the published bounds
reproduces the published spread exactly.

SAMPLES, three, of `standard` ONLY, each with the environment variable
`REMEDY_PYTEST_TIMEOUT_SEC` set to `5400` — an OVERRIDE of
`scripts/remedy_pytest_runner.py`'s own 600-second default, the same override the
R13 probe used. Samples 2 and 3 were run at R14, one after the other, each its
own process; sample 1 is COPIED from `## Q10` and was not re-measured here. One
row per SAMPLE; nothing is averaged. The summary line is pytest's own final line,
verbatim, read from that sample's own log file. Neither R14 log came near
`MAX_OUTPUT_BYTES` (512 KiB) — each is 14062 bytes — so no line below is quoted
out of a truncated stream.

| Sample | Round taken | Wall s | Exit | pytest's own final summary line |
|---|---|---|---|---|
| 1 of 3 | R13 — copied from the uncapped probe recorded in `## Q10`, not re-measured at R14 | 927.72 | 0 | `12578 passed, 1 skipped, 4466 deselected in 926.15s (0:15:26)` |
| 2 of 3 | R14 | 935.14 | 0 | `12578 passed, 1 skipped, 4466 deselected in 933.59s (0:15:33)` |
| 3 of 3 | R14 | 916.36 | 0 | `12578 passed, 1 skipped, 4466 deselected in 914.74s (0:15:14)` |

SPREAD, over the three uncapped samples, under the convention stated above:
min 916.36, max 935.14, max−min 18.78. No sample returned 124 and all three ended
at exit 0, so the three-sample set is COMPLETE at the uncapped setting. All three
report the same `12578 passed, 1 skipped, 4466 deselected`, so the readings time
the same selection and not three different ones.

PROVENANCE, measured and not assumed, because sample 1 was taken at R13 and
samples 2 and 3 at R14. `git diff --name-only fb9ddf12..HEAD -- packages/
scripts/`, run from the repository root, printed NOTHING — its measured output is
empty. That is the proof the instrument is byte-identical across all three
samples: fb9ddf12, `fix(f083): anchor the CI stage run and make an empty run
red`, is the newest commit in this branch's history that touches either path, and
nothing under `packages/` or `scripts/` has moved since. The three readings are
one set.

CONTEXT, measured this round and not recalled. `os.cpu_count()` reports 24, which
EQUALS the 24 recorded in `## Q10`. `python3 -m pytest --version` prints
`pytest 9.0.3` at exit code 0, which EQUALS the `pytest 9.0.3` recorded there.
Neither differs, so neither the machine nor the tooling moved between sample 1
and samples 2 and 3.

WHAT THIS SECTION DID NOT MEASURE, said rather than left blank. No further
`standard` sample was taken at the runner's own 600-second default: those three
kills are recorded in `## Q10` and re-running them would re-measure a settled
number, so `standard`'s R14 wall second at the default is `not measured`. `fast`,
`ui` and `smoke` were `not run` this round, for the same reason — each already
carries three samples — so their R14 wall seconds are `not measured` too. The
`excluded` stage was `not run`, as at R13, because its `runs_in_ci` is False.

This section is evidence. It carries no ceiling, no budget number and no
recommendation; choosing them from these samples is R15's work.

## Q12 — The three-sample cost of the `budgets` SELECTION, measured at R18

WHAT WAS MEASURED, and why it is a selection rather than a stage. The `budgets`
stage does not exist in `CI_STAGES` when this section is written — C4 adds it,
and C4's `timeout_sec` is computed from the numbers below. So the subject here is
the SELECTION the stage will make, driven directly, which needs no stage to
exist. The driver command is recorded verbatim and was not retyped into the
table:

    ['/usr/bin/python3', '-m', 'pytest', '-m', 'not real_ollama', '-q', 'tests/orchestration/test_scratch_file_guard.py', 'tests/test_no_interactive_guard.py', 'tests/test_test_categories.py', 'tests/orchestration/test_ci_budgets.py']

Every sample is its own `subprocess.run` from the repository root
`/home/decodeux/Repos/remedy`, with `capture_output=True`; the exit code is the
one THAT process returned (R-0438) and the wall second is `time.monotonic()`
around that one call. No sample was averaged with another and no sample was
dropped: a failing sample would be recorded with its failure.

PRECISION CONVENTION, the same one `## Q11` states and binding here too (R-0476):
every wall second is published at exactly two decimals, and every derived value —
min, max, max−min — is computed from the numbers AS PUBLISHED in the table.

| Sample | Round taken | Wall s | Exit | pytest's own final summary line |
|---|---|---|---|---|
| 1 of 3 | R18 | 1.32 | 0 | `40 passed in 1.12s` |
| 2 of 3 | R18 | 1.25 | 0 | `40 passed in 1.07s` |
| 3 of 3 | R18 | 1.27 | 0 | `40 passed in 1.07s` |

SPREAD, under the convention above: min 1.25, max 1.32, max−min 0.07. All three
ended at exit 0 and all three report the same `40 passed`, so the readings time
the same selection and not three different ones. The MEASURED MAXIMUM is 1.32 s,
and that is the number C4 feeds to the budget rule.

DERIVED BUDGET, computed by the SAME rule the other four stages already use —
`ceil(BUDGET_HEADROOM_FACTOR * measured_max / BUDGET_ROUNDING_S) *
BUDGET_ROUNDING_S` with the factor 2 and the rounding 300, both pinned in
`tests/orchestration/test_ci_stages.py`: `ceil(2 * 1.32 / 300) * 300 = ceil(0.0088)
* 300 = 1 * 300 = 300`. The `budgets` stage therefore carries `timeout_sec=300`,
which is the rounding floor rather than a headroom the measurement earned — a
1.32-second selection cannot produce a smaller multiple of 300.

CONTEXT, measured this round and not recalled. `os.cpu_count()` reports 24, which
EQUALS the 24 recorded in `## Q10` and `## Q11`. `python3 -m pytest --version`
prints `pytest 9.0.3` at exit code 0, which EQUALS the version recorded there.
Neither the machine nor the tooling moved since the R14 samples.

WHAT THIS SECTION DID NOT MEASURE, said rather than left blank. The four other
stages were NOT re-run at R18: each already carries three samples in `## Q10` or
`## Q11`, and re-running them would re-measure a settled number, so their R18
wall seconds are `not measured`. The selection above deliberately RE-RUNS guard
tests `fast` and `standard` already select; that overlap is the point of a
budgets stage and its cost is the 1.32 seconds above, not a saving to be found.

This section is evidence. The ceiling number it feeds — 26 — is not chosen here:
it is DECISION F083 D5's, recorded in `.agent/decisions.md`, and this section
neither raises nor lowers it.

## Q13 — Why the `ui` stage is red on its first run, measured at R19

WHAT THIS SECTION IS. R-0480 measured first-run reds and second-run greens for
`tests/ui_server/test_dashboard_contract.py` in fresh worktrees and attributed
them to a cold `npx` cache. The measurement is not in question here; the CAUSE
is. Every value below is its own `subprocess.run` from
`/home/decodeux/Repos/remedy` or from a disposable worktree created at 4b52f300,
with `capture_output=True` and the exit code read from the `CompletedProcess`
that produced it and never from a pipe (R-0438). This section carries NO
recommendation and orders no fix: R20 rules.

SAFETY, stated because a cold cache was required. The user's real npm cache at
`/home/decodeux/.npm` was NEVER deleted, moved or modified. Cold conditions were
produced only by setting the environment variable `npm_config_cache` to a new
empty directory under `.remedy-wt/` for the duration of one subprocess call.
Before the readings the real cache held the four top-level entries `_cacache`,
`_logs`, `_npx`, `_update-notifier-last-checked` and eight `_npx` sub-entries;
after every reading below a fresh listing reports the same four and the same
eight.

### 1 — Where the npx cache lives

| Command | Exit | Value it printed |
|---|---|---|
| `npm config get cache` | 0 | `/home/decodeux/.npm` |
| `npx --version` | 0 | `10.9.7` |
| `npm --version` | 0 | `10.9.7` |
| `node --version` | 0 | `v22.22.2` |

The directory EXISTS. A directory listing, not a guess, reports the four
top-level entries named above. `_npx` holds eight entries and one of them,
`1d6e82a4126006c4`, ALREADY CONTAINS a `tsc` entry: its `package.json` reads
`{"dependencies": {"tsc": "^2.0.4"}}` and its `node_modules/tsc/package.json`
reads `"name": "tsc"`, `"version": "2.0.4"`, `"description": "A deprecated
release of the TypeScript compiler"`. Its mtime is 2026-06-02T15:05:58, months
before this round. No `typescript` entry exists anywhere under `_npx`.

THIS IS THE FACT THE QUESTION WAS ASKED FOR. The cache is a per-USER directory,
one per machine, and it is WARM — so a fresh `git worktree` does not produce a
cold cache, and "fresh worktree" and "cold cache" are NOT the same condition.
What a fresh worktree does lack is `apps/ui/node_modules`:
`git check-ignore -v apps/ui/node_modules` exits 0 and prints
`.gitignore:221:node_modules/`, and `git ls-files apps/ui/node_modules` returns
0 lines. The primary checkout HAS that directory, with `node_modules/typescript`
and `node_modules/.bin/tsc` both present; a new worktree has neither.

### 2 — What the test actually runs

Read from `tests/ui_server/test_dashboard_contract.py`, lines 420-428,
`TestJobSummaryCommandContract::test_typescript_compiles`:

    result = subprocess.run(
        ["npx", "tsc", "--noEmit"],
        cwd=str(REPO_ROOT / "apps" / "ui"),
        capture_output=True, timeout=30,
    )
    assert result.returncode == 0, f"tsc failed:\n{result.stderr.decode()}"

The argv is exactly `["npx", "tsc", "--noEmit"]` and it carries NEITHER `--yes`
NOR `--no-install`. `cwd` is `REPO_ROOT / "apps" / "ui"`, and `REPO_ROOT` is
`Path(__file__).resolve().parent.parent.parent` at line 19, so it resolves to the
`apps/ui` of whichever checkout the test file itself lives in. The assertion
message interpolates `result.stderr` only, while the stub described below writes
its banner to STDOUT — which is why the failure text after `tsc failed:` is
empty in the transcript.

### 3 — The warm reading

A disposable worktree `.remedy-wt/r19probe` was created at HEAD with
`git worktree add --detach`, and the whole file was run twice with the ambient
cache untouched. The command, each run its own unpiped process from the worktree
root, was `python3 -m pytest tests/ui_server/test_dashboard_contract.py -q`.

| Run | Exit | pytest's own final summary line | Wall s |
|---|---|---|---|
| 1 of 2 | 1 | `1 failed, 69 passed in 5.95s` | 6.18 |
| 2 of 2 | 0 | `70 passed in 3.97s` | 4.16 |

R-0480's OBSERVATION REPRODUCES EXACTLY: first run red, second run green. The
one failing id is
`tests/ui_server/test_dashboard_contract.py::TestJobSummaryCommandContract::test_typescript_compiles`,
and the captured npx STDOUT quoted in the traceback is the deprecated stub's
banner, `This is not the tsc command you are looking for`, followed by `Use npm
install typescript to first add TypeScript to your project before using npx`, at
returncode 1. Reading that stub's own bin file at
`/home/decodeux/.npm/_npx/1d6e82a4126006c4/node_modules/tsc/bin/tsc.js`, its last
statement is `process.exitCode = 1`: the package exits non-zero by design and
compiles nothing.

WHAT CHANGED BETWEEN THE TWO RUNS, measured rather than assumed.
`apps/ui/node_modules` did NOT exist in the worktree before run 1 and DID exist
after it, containing `typescript` and `.bin/tsc`. The installer is inside the
same file, and this was measured directly rather than read off: in a THIRD fresh
worktree `.remedy-wt/r19inst`, running only
`tests/ui_server/test_dashboard_contract.py::TestAutoBuildBehavior::test_auto_build_runs_by_default`
took `node_modules` from absent to present, with `typescript` and `.bin/tsc`
inside it, at exit 0, `1 passed in 4.26s`, 4.47 s wall. That test calls
`packages.orchestration.ui_server._auto_build_frontend()` for real with
auto-build enabled, and that function runs
`["npm", "install", "--no-audit", "--no-fund"]` in `apps/ui` when `node_modules`
is missing (`ui_server.py` lines 2782-2793). It is declared at line 519 of the
test file, 99 lines BELOW `test_typescript_compiles` at line 420, so within one
run the tsc test executes first, against a tree with no local TypeScript yet.
Running the tsc test alone in that same worktree immediately afterwards gave exit
0, `1 passed in 1.65s`.

### 4 — The genuinely cold reading

The same `.remedy-wt/r19probe` worktree, one more run of the same suite, with
`npm_config_cache` set to the NEW EMPTY directory `.remedy-wt/coldnpm-cache`
(created by this round, listed as empty immediately before use). Under that
environment `npm config get cache` printed
`/home/decodeux/Repos/remedy/.remedy-wt/coldnpm-cache` at exit 0, so npm really
resolved the empty cache and not the user's.

| Condition | Exit | pytest's own final summary line |
|---|---|---|
| empty `npm_config_cache`, `node_modules` PRESENT | 0 | `70 passed in 3.92s` |

GREEN WITH AN EMPTY CACHE. There is no failing test id and no npx stdout to
quote, because nothing failed. This is the reading that contradicts the
cold-cache attribution head-on: the cache was empty by construction and the suite
passed anyway.

A SECOND disposable worktree `.remedy-wt/r19cold` was created at HEAD to hold the
variable the other way round — `node_modules` ABSENT — with only
`test_typescript_compiles` selected, so nothing in the run could install it:

| Run | `apps/ui/node_modules` before | Exit | pytest's own final summary line |
|---|---|---|---|
| 1 of 2 | absent | 1 | `1 failed in 0.50s` |
| 2 of 2 | absent | 1 | `1 failed in 0.44s` |

`node_modules` was still absent after both. The SECOND run is red too, so "first
run red, second run green" is not a property of the run COUNT at all.

### 5 — Whether `--yes` changes the colour

The argv from question 2 was run DIRECTLY with `subprocess.run` — no test file
was edited — each form with its own new empty `npm_config_cache` directory under
`.remedy-wt/`, `cwd` set to the worktree's `apps/ui`.

| Form | Worktree | `node_modules` | Exit | stdout |
|---|---|---|---|---|
| `npx tsc --noEmit` | r19cold | absent | 1 | the stub banner, `This is not the tsc command you are looking for` |
| `npx --yes tsc --noEmit` | r19cold | absent | 1 | the same stub banner |
| `npx tsc --noEmit` | r19probe | present | 0 | empty |
| `npx --yes tsc --noEmit` | r19probe | present | 0 | empty |

`--yes` CHANGES NOTHING. In the absent case npm's own STDERR reads `npm warn exec
The following package was not found and will be installed: tsc@2.0.4` and `npm
warn deprecated tsc@2.0.4: Package no longer supported.`; adding `--yes` removes
only the first of those two lines, and the exit code stays 1 with the same
STDOUT banner. The colour tracks `node_modules` in both directions across all
four readings, and never `--yes`.

### 6 — The honest conclusion

The numbers show that R-0480's MEASUREMENT is exact and its stated CAUSE is not
supported: the suite is red the first time and green after, but the variable is
`apps/ui/node_modules`, not the `npx` cache. With `node_modules` absent the test
resolves `tsc` to the deprecated stub `tsc@2.0.4`, which exits 1 by design; with
it present it resolves the project's own TypeScript and exits 0; and the suite
installs `node_modules` itself, 99 lines further down the same file, which is why
a second run differs from the first. An empty cache with `node_modules` present
is GREEN and a warm cache with `node_modules` absent is RED, so the cache is not
the variable.

What these numbers do NOT show, said rather than left blank. Nothing here
measures a hosted CI runner, where a workflow step may install `node_modules`
before pytest runs. Nothing here measures whether `_auto_build_frontend` behaves
the same without network access; every reading above had network. Nothing here
measures the `ui` stage as a whole — only
`tests/ui_server/test_dashboard_contract.py` was run, and the stage's other
selected tests are `not-measured` this round. And nothing here measures test
ORDER under a randomising plugin; the observed order is the file's declaration
order in this repository as it stands at 4b52f300.
