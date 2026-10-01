# F294 Test load diet, part two — Acceptance audit (amend0930b-slow-cap hardening stage)

I read only `docs/roadmap/features/T2_F294.md`, `AGENTS.md`, the amend0930b-slow-cap paragraph of
`docs/agents/self_drive_protocol.md`, and the repository's code, tests and git history (`git log`,
`git diff 020bc9a16..HEAD -- packages apps tests scripts`). I did not read `.agent/handoff.md`,
`.agent/live_review.md`, `.agent/live_review_archive.md`, `.agent/authored/`, `.agent/plan.md`,
`.agent/decisions.md`, `.agent/prose_slips.md`, or any `.remedy-wt/f294-*` file. All mutations ran
in the disposable worktree `/home/decodeux/Repos/remedy/.remedy-wt/f294-audit-wt`, created
detached at HEAD `b9b98bf6e` (branch `feature/f294-test-load-diet-two`, forked from `main` at
`020bc9a16`). Every pytest invocation used `python3 -B -m pytest -q -n auto -p no:cacheprovider`
against one file, one class or one node id at a time; no command set `REMEDY_TEST_MAX_WORKERS` or a
larger `-n`, no two commands ran at once, and no run printed "the run left ... process(es) behind".
No full suite ran at any point. The primary checkout was never edited; `git status --porcelain`
there stayed empty throughout.

The Acceptance heading's one statement is carried "word for word" from the Goal & Done heading
(the feature file says so explicitly), so the CPU-target clause and the DECISION-alternative clause
below audit both headings' text as one claim each, rather than double-counting an identical
sentence under two headings.

The cuts this branch made (`git diff 020bc9a16..HEAD -- packages apps tests scripts`): DECISION
F294 D1 (one discovery of configured git helpers per `worktree_identity` reading, memoized in
`packages/orchestration/run_manifest.py`), D3 (`git submodule status` asked only when the index
holds a gitlink), D2 (`tests/conftest.py`'s `_data_root_allocator`, one `tmp_path_factory.mktemp`
parent per test session), D4 (`tests/cli/test_golden_path.py` runs `init`/`do`/`status` in-process
via `tests/cli/in_process_cli.py`), and D5 (`tests/cli/test_scoped_listings.py` runs its `init`/
`do`/`project current` setup in-process, while every listing it asserts on still runs as a real
child process through `_run_cli`).

Total claims audited: 8. Proven at once: 4. Gaps: 3. Measurement-only (not run): 1.

## Claim 1 (Goal & Done + Acceptance) — the 40 percent CPU target

> "The full suite costs at least 40 percent less CPU time than F293's T001 baseline, 1,246.09 CPU
> seconds... DONE when the full suite's CPU seconds, read from the test load record, are at most
> 747.65..." / Acceptance: "the full suite's CPU seconds in the test load record are at least 40
> percent below T001's baseline."

Test node id(s): none can measure the claim itself; `tests/regression/test_test_load_governor.py::
TestRunRecord::test_a_child_run_leaves_exactly_one_well_formed_line` guards the mechanism that
produces the CPU-seconds reading the claim is read from.

Mutation (of the reading mechanism, to show it is guarded): `tests/load_governor.py`, the
`cpu_seconds` field of `build_record`.
Before: `"cpu_seconds": round(_cpu_seconds() - start["cpu"], 2),`
After: `"cpu_seconds": 0.0,`

Red: `python3 -B -m pytest -q -n auto -p no:cacheprovider
tests/regression/test_test_load_governor.py::TestRunRecord::test_a_child_run_leaves_exactly_one_well_formed_line`
→ `assert record["cpu_seconds"] > 0` → `AssertionError: assert 0.0 > 0` → `1 failed in 1.30s`.

Green (mutation reverted, same command): `1 passed in 1.30s`.

Reaches the user: no (the guarding test spawns a child pytest run and reads the record file; the
40 percent figure itself is a cross-run comparison, not a single CLI invocation).

**Verdict: MEASUREMENT-ONLY.** The 40 percent / 747.65-CPU-second reading can only be produced by
one full-suite run (`python3 -m pytest -n auto -q`) compared against F293 T001's recorded 1,246.09,
which amend0930-test-load forbids in this audit and which happens only at the integration-gate
round; the mechanism that writes the reading (`tests/load_governor.build_record`/`append_record`,
invoked from `tests/conftest.py`'s session-finish hook) is guarded by the test above, proven red
and green here, so a broken reading would be caught even though the threshold itself cannot be.

## Claim 2 (Goal & Done) — without losing a single assertion

> "...without losing a single assertion."

Test node id(s): `tests/regression/test_f293_acceptance.py::TestNoAssertionWasLost::
test_no_module_f293_changed_has_fewer_assertions_than_where_f293_began` — the only assertion-floor
test in the repository, and the test for the mutated file itself,
`tests/cli/test_golden_path.py::TestDoMission::test_do_mission_creates_and_runs_one_job`.

Mutation (of the guarded artifact — a test file this branch changed): `tests/cli/test_golden_path.py`,
inside `TestDoMission.test_do_mission_creates_and_runs_one_job`.
Before:
```
        assert "1 task(s)" in out
        assert "to completed" in out
```
After:
```
        assert "to completed" in out
```
(one assertion deleted)

Red/Green readings: both runs were green. With the assertion removed, `python3 -B -m pytest -q
-n auto -p no:cacheprovider "tests/cli/test_golden_path.py::TestDoMission::
test_do_mission_creates_and_runs_one_job"` → `1 passed in 2.43s` (the mutated test itself cannot
notice its own missing assertion), and `python3 -B -m pytest -q -n auto -p no:cacheprovider
tests/regression/test_f293_acceptance.py` → `6 passed, 1 skipped in 0.91s` (unchanged from the
unmutated baseline). Mutation reverted; the file matches `git status --porcelain` empty again.

Reaches the user: no.

**Verdict: GAP.** `TestNoAssertionWasLost`'s `FLOOR` dict lists only the test modules F293 itself
changed (`tests/cli/test_mission_cmd.py`, `test_worker_facade_cmd.py`, etc.); none of F294's own
changed files — `tests/cli/test_golden_path.py`, `tests/cli/test_scoped_listings.py`,
`tests/conftest.py`, `tests/orchestration/test_run_manifest_integrity.py`,
`tests/test_data_root_isolation.py` — appear in it, so an assertion deleted from any of them is
invisible to every test in the repository, as demonstrated. Closing it needs F294's changed files
and their current assertion/`raises` counts added to `FLOOR` (or an equivalent floor keyed to this
feature's fork commit `020bc9a16`).

## Claim 3 (Goal & Done + Acceptance) — the DECISION alternative

> "...OR the ranking shows that what remains cannot be made cheaper without weakening a test, and a
> dated DECISION says so with the numbers." / Acceptance: "...or a dated DECISION shows with
> numbers that what remains cannot be made cheaper without weakening a test."

Test node id(s): none. `grep -rln "ranking" tests/ scripts/` and `grep -rln "cannot be made
cheaper"` both return no files.

Mutation: not applicable — there is no mechanism in `tests/` or `scripts/` to mutate; the clause
names a reviewer judgment call (a ranking read by a human) and a `.agent/decisions.md` entry,
neither of which any test inspects.

Reaches the user: no.

**Verdict: GAP.** No test, script, or CI check verifies that a dated DECISION with numbers
accompanies a closure that falls short of the 40 percent target, or that the "ranking" referred to
was actually produced. The rule is enforced only by the reviewer under
`docs/agents/planner_reviewer_prompt.md`, outside any automated gate. Closing it fully is not
realistically mechanizable (the clause asks for a human ranking judgment), but a narrower guard is
possible: a check that when the test load record's newest full-suite CPU reading exceeds 747.65,
`.agent/decisions.md` carries a dated DECISION line for this feature with both numbers in it. No
such check exists today.

## Claim 4 (T002 / DECISION F294 D1) — one discovery of configured git helpers per reading

> "Every changed test keeps a red-proof: a mutation of the production line it guards still turns it
> red," applied to D1: "A reading of a repository's identity discovers the configured helpers once
> instead of before each of its six git commands."

Test node id(s): `tests/orchestration/test_run_manifest_integrity.py::
TestOneHelperDiscoveryPerReading::test_a_reading_discovers_the_helpers_once`,
`::test_a_failed_discovery_is_retried_by_the_next_command`, `::test_the_next_reading_discovers_afresh`.

Mutation: `packages/orchestration/run_manifest.py`, `_helper_neutralizing_args`, line 335.
Before: `    if memo is not None and cwd in memo:`
After: `    if False and memo is not None and cwd in memo:`

Red: `python3 -B -m pytest -q -n auto -p no:cacheprovider
"tests/orchestration/test_run_manifest_integrity.py::TestOneHelperDiscoveryPerReading"` →
`FAILED ...test_a_reading_discovers_the_helpers_once`, `FAILED
...test_a_failed_discovery_is_retried_by_the_next_command`, `FAILED
...test_the_next_reading_discovers_afresh` → `3 failed, 1 passed in 0.79s` (one test in the class
does not count discoveries and stayed green, as expected).

Green (mutation reverted, same command): `4 passed in 0.75s`.

Reaches the user: no (calls `worktree_identity()` directly against a fixture repo).

**Verdict: PROVEN.** The memo short-circuit this cut added is exactly what the three failing tests
check; disabling it collapses one discovery per reading back to one discovery per git command, and
they catch it immediately.

## Claim 5 (T002 / DECISION F294 D2) — data root from one parent per test process

> "Every test's data root comes from one parent per test process, so no test lists the whole base
> temporary directory to number its root (D2)."

Test node id: `tests/test_data_root_isolation.py::test_every_root_is_a_new_directory_under_one_parent`.

Mutation: `tests/conftest.py`, the `_data_root_allocator` fixture's `allocate()` closure.
Before:
```
    def allocate():
        root = parent / str(next(numbers))
        root.mkdir(mode=0o700)
        return root
```
After:
```
    def allocate():
        return tmp_path_factory.mktemp(f"remedy-data-{next(numbers)}")
```
(this reintroduces exactly the pre-F294 mechanism the Built State describes: a fresh
`tmp_path_factory.mktemp` call, which numbers itself by listing the whole base temporary directory,
for every allocated root)

Red/Green readings: both green. `python3 -B -m pytest -q -n auto -p no:cacheprovider
"tests/test_data_root_isolation.py::test_every_root_is_a_new_directory_under_one_parent"` →
`1 passed in 0.59s` under the mutation. Reverted, same command on the full file: `4 passed in
0.64s`; `git status --porcelain` in the worktree returned empty, confirming the revert.

Reaches the user: no.

**Verdict: GAP.** The guarding test only checks the shape of the result — a common parent directory
and three distinct, empty paths — which `tmp_path_factory.mktemp` also produces (its numbered
directories are always siblings under the same pytest base temp dir). It does not detect that the
cheap, pre-computed-parent path was replaced by a `mktemp` call per allocation, which is the actual
mechanism D2 removed to stop every test (and every `tmp_path`) from listing a growing temporary
directory. Closing it needs a test that counts or forbids `tmp_path_factory.mktemp` calls inside
`allocate()` after its one setup call — e.g. monkeypatching `tmp_path_factory.mktemp` to fail after
the fixture's first call and asserting `allocate()` still succeeds twice.

## Claim 6 (T002 / DECISION F294 D3) — submodule status only when the index holds a submodule

> "...runs `git submodule status`, a shell script on the operator's git, only when the index holds
> a submodule (D3)."

Test node id: `tests/orchestration/test_run_manifest_integrity.py::
TestSubmoduleStatusOnlyWithASubmodule::test_without_a_submodule_it_never_runs_and_the_identity_is_unchanged`.

Mutation: `packages/orchestration/run_manifest.py`, `_submodule_status`.
Before:
```
    ok, staged, _ = _git_bytes(repo_path, ["ls-files", "--stage", "-z"])
    if ok and not any(entry.startswith(b"160000 ") for entry in staged.split(b"\0")):
        return True, b"", ""
    return _git_bytes(repo_path, ["submodule", "status"])
```
After:
```
    return _git_bytes(repo_path, ["submodule", "status"])
```

Red: `python3 -B -m pytest -q -n auto -p no:cacheprovider
"tests/orchestration/test_run_manifest_integrity.py::TestSubmoduleStatusOnlyWithASubmodule"` →
`FAILED ...test_without_a_submodule_it_never_runs_and_the_identity_is_unchanged` →
`AssertionError: assert [[...'submodule', 'status']] == []` → `1 failed, 3 passed in 0.82s`.

Green (mutation reverted, same command): `4 passed in 0.81s`.

Reaches the user: no.

**Verdict: PROVEN.** Removing the `ls-files --stage` short-circuit makes `git submodule status` run
unconditionally again, and the test that checks it never runs without a gitlink in the index
catches it directly.

## Claim 7 (T002 / DECISION F294 D4) — golden-path tests run init/do/status in-process

> "The golden-path tests run `init`, `do` and `status` in the test process... through
> `tests/cli/in_process_cli.py`, while every other command those files assert on still runs as a
> child process (D4, D5)."

Test node id: `tests/cli/test_golden_path.py::TestGoldenPathSmoke::test_init_do_status_stop_flow`
(the one test in the file that asserts on `_init_project`'s own return code).

Mutation: `apps/cli/commands/init_cmd.py`, line 135, the project-registration call `_handle_init`
makes.
Before: `            project = register_project_repo(project_name, root)`
After: `            project = register_project_repo(project_name, root / "f294-audit-mutation")`

Red: `python3 -B -m pytest -q -n auto -p no:cacheprovider
"tests/cli/test_golden_path.py::TestGoldenPathSmoke::test_init_do_status_stop_flow"` →
`assert init.returncode == 0, init.stderr` → `AssertionError: ... Error: NotAGitRepoError: Not a
git repository: '.../repo/f294-audit-mutation'` → `assert 1 == 0` → `1 failed in 0.72s`.

Green (mutation reverted, same command): `1 passed in 2.33s`.

Reaches the user: no — `run_cli_in_process` calls `apps.cli.grouped.main(argv)` in this test
process (that is D4's whole point: no child process is started for `init`/`do`/`status`), so this
proof exercises the same command dispatch a user's shell would reach but not a real command line.
Claim 8 below supplies the command-line proof for this feature.

**Verdict: PROVEN.** The one test in `test_golden_path.py` that checks `init`'s own exit code still
turns red when `init`'s project registration is broken, after the switch from a real subprocess to
`run_cli_in_process`; the test's red-proof survived the cut.

## Claim 8 (T002 / DECISION F294 D5) — scoped-listing tests run their setup in-process, listings stay child processes

> "...the scoped-listing tests their setup, through `tests/cli/in_process_cli.py`, while every
> other command those files assert on still runs as a child process (D4, D5)."

Test node id: `tests/cli/test_scoped_listings.py::TestScopedListingsCLI::test_full_isolation_and_flags`.

Mutation: `packages/orchestration/project_scope.py`, `job_in_scope`'s final line.
Before: `    return job.project_id == scope.project_id`
After: `    return True`

Red: `python3 -B -m pytest -q -n auto -p no:cacheprovider
"tests/cli/test_scoped_listings.py::TestScopedListingsCLI::test_full_isolation_and_flags"` →
`assert "beta job one" not in result.stdout` → `AssertionError: 'beta job one' is contained here:
... beta job one` → `1 failed in 5.99s`.

Green (mutation reverted, same command): `1 passed in 6.17s`.

Reaches the user: **yes.** `_run_cli` in `tests/cli/test_scoped_listings.py` runs
`subprocess.run([sys.executable, "-m", "apps.cli.grouped", "job", "list", ...])` — a real child
process started the way a terminal user invokes `remedy job list` — and the mutation of the
project-scoping predicate is caught through that real command-line path, not only through a unit
test.

**Verdict: PROVEN.** `_init_project`'s and `_create_job`'s move to `run_cli_in_process` left the
file's real-subprocess listing assertions exactly as sensitive to a scoping defect as before the
cut; this is the audit's command-line proof for F294.

## Worktree cleanup

`git worktree remove --force /home/decodeux/Repos/remedy/.remedy-wt/f294-audit-wt` was run as the
last action. `git worktree list` and `git status --porcelain` in the primary checkout afterward are
reported in the summary message, not here.
