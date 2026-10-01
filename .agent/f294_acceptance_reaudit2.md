# F294 Test load diet, part two — Second repeat acceptance audit (amend0930b-slow-cap hardening stage)

I read `docs/roadmap/features/T2_F294.md`, `AGENTS.md`, the `amend0930b-slow-cap` paragraph in
`docs/agents/self_drive_protocol.md` (the paragraph starting "Operator amendment amend0930b-slow-cap"
and continuing through "deleting DECISION amend0930b D1 to D3"), and the repository's code, tests and
git history (`git log`, `git diff 020bc9a16..HEAD` on non-`.agent/` paths). I did not read anything
under `.agent/`, any earlier audit, any verdict, or any `.remedy-wt/f294-*` file. All mutations ran in
the disposable worktree `/home/decodeux/Repos/remedy/.remedy-wt/f294-reaudit2-wt`, created detached at
HEAD `cb959bda376eac592cd35ffb7e978e13ee051daf` with `git worktree add --detach ... HEAD`. Every pytest
run used exactly `python3 -B -m pytest <paths> -q -n auto -p no:cacheprovider`, scoped to
`tests/test_data_root_isolation.py` only; no full suite ran. The primary checkout was never touched.

Total statements audited: 1. Proven: 0. Gaps: 1.

## Statement 1 — the allocator never numbers or finds its root by listing a directory

> Every test's data root comes from one parent per test process, so no test lists the whole base
> temporary directory to number its root (D2).

Subject: `_data_root_allocator` (`tests/conftest.py:38-56`) and its `_isolated_data_root` user
(`tests/conftest.py:59-87`).

**Guarding node ids**
- `tests/test_data_root_isolation.py::test_a_root_is_made_without_numbering_the_base_directory` — the
  direct guard: monkeypatches `os.scandir`, `os.listdir` and `Path.iterdir` to raise
  `AssertionError("allocating a root listed a directory")`, then calls the allocator twice.
- `tests/test_data_root_isolation.py::test_every_root_is_a_new_directory_under_one_parent` — guards
  the "one parent per test process" half: asserts `resolve_data_root()`'s root and two
  allocator-made roots share one `.parent` and are three distinct directories.
- `tests/test_data_root_isolation.py::test_the_resolved_root_is_under_the_pytest_temp_base` — guards
  that the resolved root sits under `tmp_path_factory.getbasetemp()`, catching an allocator that
  stops using the pytest temp tree at all.

Control run before any mutation (and after every revert below), same command each time:

    cd .remedy-wt/f294-reaudit2-wt && python3 -B -m pytest tests/test_data_root_isolation.py -q -n auto -p no:cacheprovider
    -> 5 passed in <1s (green)

### Mutation 1 — number by `Path.iterdir()` count on the parent
`tests/conftest.py:51-54`, before:

    def allocate():
        root = parent / str(next(numbers))
        root.mkdir(mode=0o700)
        return root

after:

    def allocate():
        root = parent / str(len(list(parent.iterdir())))
        root.mkdir(mode=0o700)
        return root

Red: `test_a_root_is_made_without_numbering_the_base_directory` FAILED —
`AssertionError: allocating a root listed a directory`, raised from the patched `Path.iterdir`
inside `allocate()` (`tests/conftest.py:52`). 1 failed, 4 passed.
Green after revert: 5 passed.

### Mutation 2 — number by `os.listdir(parent)` count
`tests/conftest.py:47-54`, before: same as Mutation 1's "before". After:

    import itertools
    import os
    parent = tmp_path_factory.mktemp("remedy-data")
    numbers = itertools.count()

    def allocate():
        root = parent / str(len(os.listdir(parent)))
        root.mkdir(mode=0o700)
        return root

Red: `test_a_root_is_made_without_numbering_the_base_directory` FAILED — same AssertionError, raised
from the patched `os.listdir` inside `allocate()`. 1 failed, 4 passed.
Green after revert: 5 passed.

### Mutation 3 — number by `os.scandir(parent)` entry count
After:

    import itertools
    import os
    parent = tmp_path_factory.mktemp("remedy-data")
    numbers = itertools.count()

    def allocate():
        with os.scandir(parent) as entries:
            count = sum(1 for _ in entries)
        root = parent / str(count)
        root.mkdir(mode=0o700)
        return root

Red: `test_a_root_is_made_without_numbering_the_base_directory` FAILED — same AssertionError, raised
from the patched `os.scandir`. 1 failed, 4 passed.
Green after revert: 5 passed.

### Mutation 4 — number by shelling out to `ls` (bypasses `os.scandir`/`os.listdir`/`Path.iterdir`)
After:

    import itertools
    import subprocess
    parent = tmp_path_factory.mktemp("remedy-data")
    numbers = itertools.count()

    def allocate():
        listing = subprocess.run(
            ["ls", "-1", str(parent)], capture_output=True, text=True, check=True,
        ).stdout
        count = len([line for line in listing.splitlines() if line])
        root = parent / str(count)
        root.mkdir(mode=0o700)
        return root

    return allocate

Result: GREEN — `5 passed in 0.65s`, reproduced twice. The allocator now lists the parent directory
on every call (via a child `ls` process) to compute the next number, exactly the behaviour D2 and the
guard test's own docstring forbid ("after its one parent, the allocator lists no directory"), yet
no test in `tests/test_data_root_isolation.py` notices: the forbidding test only monkeypatches
in-process Python callables (`os.scandir`, `os.listdir`, `Path.iterdir`); a subprocess spawns its own
process image and calls its own libc `readdir`, never touching the patched Python attributes.
Green after revert (confirms the mutation, not drift, caused the pass): 5 passed, identical to the
pre-mutation control.

This is a genuine escape, so Statement 1 is a **GAP**, found by a mutation that does not go through
`os.scandir`/`os.listdir`/`Path.iterdir` at all.

### Mutation 5 — does not go through `tmp_path_factory`: hand-rolled parent + `os.listdir`
After (whole fixture body):

    import os
    import tempfile
    from pathlib import Path
    parent = Path(tempfile.mkdtemp(prefix="remedy-data-"))

    def allocate():
        root = parent / str(len(os.listdir(parent)))
        root.mkdir(mode=0o700)
        return root

    return allocate

Red: two tests FAILED —
`test_a_root_is_made_without_numbering_the_base_directory` (patched `os.listdir` raised the same
AssertionError) AND `test_the_resolved_root_is_under_the_pytest_temp_base`
(`PosixPath('/tmp/remedy-data-...')` is not relative to `tmp_path_factory.getbasetemp()`). 2 failed,
3 passed. Green after revert: 5 passed.

### Mutation 6 — `_isolated_data_root` makes its own root another way, bypassing the allocator
`tests/conftest.py:81-87`, before:

    import os
    if os.environ.get("REMEDY_DATA_DIR"):
        yield
        return
    os.environ["REMEDY_DATA_DIR"] = str(_data_root_allocator())
    yield
    os.environ.pop("REMEDY_DATA_DIR", None)

after:

    import os
    import tempfile
    if os.environ.get("REMEDY_DATA_DIR"):
        yield
        return
    os.environ["REMEDY_DATA_DIR"] = tempfile.mkdtemp(prefix="remedy-data-own-")
    yield
    os.environ.pop("REMEDY_DATA_DIR", None)

Red: two tests FAILED —
`test_every_root_is_a_new_directory_under_one_parent` (`root.parent == first.parent` is
`PosixPath('/tmp') == PosixPath('.../remedy-data0')`, false) AND
`test_the_resolved_root_is_under_the_pytest_temp_base` (the ad-hoc `/tmp/remedy-data-own-...` root is
not relative to `tmp_path_factory.getbasetemp()`). 2 failed, 3 passed. A test does notice: the
per-test root silently diverging from the allocator's parent is caught twice, independent of any
directory-listing guard.
Green after revert: 5 passed.

**Reaches the user: no.** `_data_root_allocator` and `_isolated_data_root` live in `tests/conftest.py`
and exist only to keep the test suite's own CPU/IO budget down (DECISION F294 D2); they are never
shipped and never run outside the test process, so no CLI or cockpit path exercises this code the way
a user does. The hardening stage's "reaches the user" proof obligation is met elsewhere in F294 by the
golden-path/scoped-listing in-process-CLI cuts (D4, D5), not by this test-infrastructure statement.

**Verdict: GAP.** Mutation 4 shows the allocator can be made to list a directory (its own parent, via
a child `ls` process) to number every root it hands out, and all five tests in
`tests/test_data_root_isolation.py` stay green; closing it needs a test that also forbids
subprocess-based listing during `allocate()` — for example, monkeypatching `subprocess.run` and
`subprocess.Popen` (or installing a `sys.addaudithook` on process-spawn events) to raise the same
"allocating a root listed a directory" assertion the existing test raises for the in-process APIs,
alongside the three it already patches.
