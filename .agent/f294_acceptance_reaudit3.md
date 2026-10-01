# F294 Test load diet, part two — Third repeat acceptance audit (amend0930b-slow-cap hardening stage)

I read `docs/roadmap/features/T2_F294.md`, `AGENTS.md`, the amend0930b-slow-cap paragraph of
`docs/agents/self_drive_protocol.md` (the hardening-stage rule, rules (1)-(6)), and the repository's
code, tests and git history (`git log`, `git diff 020bc9a16..HEAD` scoped to non-`.agent/` paths,
`git show` on `tests/conftest.py` and `tests/test_data_root_isolation.py`). I did not read anything
under `.agent/`, any `.remedy-wt/f294-*` file, or any earlier audit or verdict, as ordered. All
mutations ran in a disposable worktree, `git worktree add --detach
/home/decodeux/Repos/remedy/.remedy-wt/f294-reaudit3-wt HEAD`, HEAD `8ceb35ef8` on
`feature/f294-test-load-diet-two`. Every pytest invocation used
`python3 -B -m pytest <paths> -q -n auto -p no:cacheprovider`, one or two files at a time, and the
full suite was never run. The primary checkout was never edited and stayed `git status --porcelain`
clean throughout.

Total statements audited: 1. Proven: 0. Gaps: 1.

## Statement 1 — one parent per test process, no listing to number the root

> Every test's data root comes from one parent per test process, so no test lists the whole base
> temporary directory to number its root (D2).

Guarding node ids (both in `tests/test_data_root_isolation.py`):
- `test_a_root_is_made_without_numbering_the_base_directory` — the direct guard: patches every
  listing/spawn route it names to raise, then calls the allocator twice and asserts both roots exist
  and differ.
- `test_every_root_is_a_new_directory_under_one_parent` — the "one parent" half: asserts the
  resolved root and two further allocations share one `.parent` and that none of the three already
  held files.

Baseline (unmutated worktree, `tests/test_data_root_isolation.py` alone): `5 passed in 0.89s`,
including both node ids above — green before any mutation, as required.

The allocator (`tests/conftest.py::_data_root_allocator`) makes its parent once via
`tmp_path_factory.mktemp("remedy-data")` and then does `root = parent / str(next(numbers));
root.mkdir(mode=0o700)` with `numbers = itertools.count()` — no listing call anywhere in the
unmutated allocate(). `_isolated_data_root` (line 85) calls `_data_root_allocator()` for every test
that has not already set `REMEDY_DATA_DIR` itself; this wiring was not touched by any mutation
below, and the baseline's own `test_each_test_gets_a_fresh_empty_root` and
`test_the_resolved_root_is_under_the_pytest_temp_base` passing green confirms the per-test root still
comes from the allocator.

Six mutations of `tests/conftest.py`, each applied alone to the allocator's body (`tests/conftest.py`
lines 47-54 in the unmutated file), then reverted (checksum-verified back to `e2abc7dae9f9e7b0ac68
d64df569117c`) before the next:

1. **Early-bound `os.scandir` alias.** Added `import os as _os_early_bind` /
   `_SCANDIR = _os_early_bind.scandir` at module import time (before `pytest`'s fixtures or any
   test's `monkeypatch` run), then changed `allocate()` from the counter to:
   `existing = [int(e.name) for e in _SCANDIR(parent) if e.name.isdigit()]; root = parent /
   str(max(existing, default=-1) + 1)`. The guard's `monkeypatch.setattr(os, "scandir", refused)`
   replaces the attribute on the live `os` module, but `_SCANDIR` was already bound to the original
   function object at conftest import time — long before the test's `with monkeypatch.context()`
   block exists — so the patch never touches it.
   Result: **`5 passed in 0.89s`/`0.87s`, GREEN** (the targeted node id passed, verified alone too:
   `1 passed in 0.45s`). This is a real, ordinary-Python regression: the allocator genuinely lists
   `parent` on every call to number the root, and the guard does not notice.

2. **Reintroduce `tmp_path_factory.mktemp()` per call** (the literal anti-pattern D2/D9 describe):
   `allocate()` became `return tmp_path_factory.mktemp("remedy-data", numbered=True)`.
   Result: **RED** — `1 failed, 4 passed`, failing inside pytest's own `make_numbered_dir` →
   `find_prefixed` → `os.scandir(root)`, caught by the patched `os.scandir`.

3. **Shell subprocess count** (`ls -1 <parent> | wc -l` via `subprocess.run(..., shell=True)`) to
   compute the next number.
   Result: **RED** — fails inside `subprocess.run`'s own `Popen(...)` call, caught by the patched
   `subprocess.Popen`.

4. **`os.walk(parent)`** to read the parent's immediate subdirectory names and number from their max.
   Result: **RED** — `os.walk`'s internal `scandir_it = scandir(top)` resolves `scandir` from the
   `os` module's own globals at call time, so the patched `os.scandir` catches it too.

5. **Module-level `glob.glob(str(parent / "*"))`** (not `pathlib.Path.glob`, which the guard patches
   directly) to list and number.
   Result: **RED** — CPython's `glob._iterdir` calls `os.scandir(arg)` by qualified attribute, so
   the patched `os.scandir` catches this route as well, even though `glob.glob` itself is never
   named in the guard's `routes` tuple.

6. **`ctypes` call into libc's `system()`** (`ctypes.CDLL(None).system(b"ls -1 <parent> | wc -l >
   <parent>/.count")`, then reading the count file) — a foreign-function call that never touches any
   Python-level `os`/`subprocess`/`pathlib` attribute at all.
   Result: **GREEN** — `5 passed in 0.89s`. This evades the guard completely, but I do **not** count
   it toward the GAP: the mutation order asks for "ordinary Python a developer could plausibly
   write," and shelling out to libc's raw `system(3)` via `ctypes` to list a directory, inside a
   pytest fixture, is not code anyone would plausibly write for this purpose — it exists only to
   defeat monkeypatching. Mutation 1, by contrast, is a one-line, idiomatic micro-optimization
   (binding a hot stdlib function to a local name at import time) that any contributor could write
   for an unrelated reason and still trip this exact blind spot, so it is the one that counts.

Reaches the user: no — this is a test-infrastructure fixture (`tests/conftest.py`), not product code
reachable through the CLI or cockpit; the amend0930b-slow-cap rule's "reaches the user through the
command line or headless browser" requirement applies to the feature's product proofs as a whole
(satisfied elsewhere, e.g. the in-process CLI cuts), not to this internal-only guard statement.

**Verdict: GAP.** Mutation 1 — binding `os.scandir` to a module-level name before any test's
`monkeypatch` runs, then using it to list `parent` and number the root by its contents — turns the
allocator back into exactly the pattern D2/D9 forbid while every test in
`tests/test_data_root_isolation.py` stays green, because the guard patches live attributes on `os`,
`Path` and `subprocess` rather than intercepting the kernel-level listing operation itself; the test
that would close it watches for the actual `getdents`/`getdents64` syscall against the base temp
directory during allocation (e.g. via an `strace`/`ptrace`-based wrapper or an `LD_PRELOAD` shim),
which an early-bound alias cannot route around the way it routes around a `monkeypatch.setattr`.
