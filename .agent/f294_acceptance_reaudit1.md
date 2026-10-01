# F294 Test load diet, part two — Repeat acceptance audit (amend0930b-slow-cap hardening stage)

Read only: `docs/roadmap/features/T2_F294.md`, `AGENTS.md`, the `amend0930b-slow-cap` paragraph of
`docs/agents/self_drive_protocol.md` (lines 557-600), and the repository's code, tests and git
history (`git diff --stat 020bc9a16..HEAD -- tests`, `git diff 020bc9a16..HEAD -- tests/...`,
`git show`). Nothing under `.agent/` and no `.remedy-wt/f294-*` file was read; no earlier audit or
verdict was consulted. All mutations ran in the disposable worktree
`/home/decodeux/Repos/remedy/.remedy-wt/f294-reaudit-wt`, created `git worktree add --detach` from
HEAD `01c05e0277980a7d730df7af0f69ca96eb65fa08` (branch `feature/f294-test-load-diet-two`, forked
from `main` at `020bc9a16`). Every pytest run used
`python3 -B -m pytest <paths> -q -n auto -p no:cacheprovider`, one or two files at a time; no full
suite ran. No run printed "the run left ... process(es) behind". The primary checkout was never
edited and stayed `git status --porcelain` empty throughout.

Total statements audited: 2. Proven: 0. Gaps: 2.

## Statement 1 — Goal & Done: no assertion lost

> The cuts came "without losing a single assertion" — for every test module this branch changed
> (`git diff --stat 020bc9a16..HEAD -- tests`), an assertion that existed at `020bc9a16` and is
> deleted, OR weakened while the count stays the same, must turn some test red.

Files this branch changed under `tests/` (`git diff --name-status 020bc9a16..HEAD -- tests`):
`tests/cli/in_process_cli.py` (A, helper, no test functions, 0 asserts both sides), `tests/cli/
test_golden_path.py` (M), `tests/cli/test_scoped_listings.py` (M), `tests/conftest.py` (M),
`tests/orchestration/test_run_manifest_integrity.py` (M), `tests/regression/test_f294_acceptance.py`
(A, the guard itself — no fork-point content to lose), `tests/test_data_root_isolation.py` (M).

Guard node ids:
- `tests/regression/test_f294_acceptance.py::TestNoAssertionWasLost::test_no_module_f294_changed_has_fewer_assertions_than_where_f294_began`
- `tests/regression/test_f294_acceptance.py::TestNoAssertionWasWeakened::test_every_unit_that_existed_where_f294_began_is_unchanged_or_reviewed`

Fork-point floor vs. current count (asserts, raises/warns), read with the guard's own `_assertions`:
`test_golden_path.py` 144/0 → 144/0 (no margin); `test_scoped_listings.py` 69/0 → 69/0 (no margin);
`test_run_manifest_integrity.py` 26/4 → 43/4 (margin 17); `test_data_root_isolation.py` 6/0 → 11/0
(margin 5); `conftest.py` 0/0 → 0/0.

**Mutation 1 — deletion, `tests/cli/test_golden_path.py:98`.**
Before: `        assert "to completed" in out`. After: line removed (file has no margin here, 144→143).
Command: `python3 -B -m pytest tests/regression/test_f294_acceptance.py -q -n auto -p no:cacheprovider`.
Red: both guard tests fail —
`AssertionError: assert {'tests/cli/test_golden_path.py': {'floor': (144, 0), 'now': (143, 0)}} == {}`
and `AssertionError: ... {'tests/cli/test_golden_path.py': ['TestDoMission.test_do_mission_creates_and_runs_one_job']} == {}`.
Green after revert: `2 passed in 0.68s`.

**Mutation 2 — weakened, count unchanged, `tests/cli/test_scoped_listings.py:133`.**
Before: `        assert "beta job one" not in result.stdout`.
After: `        assert "beta job one" not in result.stdout or True` (same assert-statement count, now
a tautology). Command: same as above. Red: `TestNoAssertionWasWeakened` fails —
`AssertionError: ... {'tests/cli/test_scoped_listings.py': ['TestScopedListingsCLI.test_full_isolation_and_flags']} == {}`;
`TestNoAssertionWasLost` stays green (count identical), confirming the count check alone would have
missed this and the content/digest check is what catches it. Green after revert: `2 passed in 0.69s`.

**Mutation 3 — deletion in a module whose count sits above its fork-point floor,
`tests/orchestration/test_run_manifest_integrity.py:179`.**
Before: `        assert all("filter.canary.clean=cat" in argv for argv in commands)`
(inside `test_every_command_of_a_reading_is_neutralized`, a test F294 itself added — it did not
exist at `020bc9a16`). After: line removed (43→42 asserts, still above the floor of 26). Command:
same as above, and separately
`python3 -B -m pytest tests/orchestration/test_run_manifest_integrity.py::TestOneHelperDiscoveryPerReading -q -n auto -p no:cacheprovider`.
Result: **no test turns red** — the guard: `2 passed in 0.67s`; the functional test class itself:
`4 passed in 0.75s`. This is the right outcome for the statement as literally worded: the deleted
assertion did not exist at `020bc9a16` (it is new, added by this branch), so the statement makes no
claim about it, and the module's fork-point floor (26) is still cleared by the remaining 42. It is
not a counter-example to the statement — but it does mean an assertion F294 added to guard F294's
own cuts carries no ratchet protection of its own until a later feature registers today's count as
its floor. Reverted; green confirmed together with mutations 1-2's revert:
`7 passed in 0.70s` (both files).

**Miss found (defeats the statement's own guard, not just a corner case it declines to cover).**
Repeating mutation 2 (the tautology on `tests/cli/test_scoped_listings.py:133`) but *also* adding,
in the same hypothetical commit, a matching entry to `REVIEWED_CHANGES` in
`tests/regression/test_f294_acceptance.py` —
`"TestScopedListingsCLI.test_full_isolation_and_flags": ("eaf10b7f4739df0f", "round 5: flake-proofed
(fabricated for the audit's miss probe)")`, where `eaf10b7f4739df0f` is the real sha256[:16] of the
mutated function's `ast.unparse` text (computed and verified in the worktree) — makes **both guard
tests pass**: `python3 -B -m pytest tests/regression/test_f294_acceptance.py -q -n auto -p
no:cacheprovider` → `2 passed in 0.67s`, even though the fork-point assertion on `test_scoped_
listings.py:133` was weakened to an unconditional tautology that can never fail again. The check
only compares a digest computed from the current file text against a table that lives in the same
file an author of a weakening commit can also edit; nothing cross-checks the quoted "round" reason
against an actual reviewed round. Reverted (both the test file and the fabricated table entry);
green confirmed: `2 passed in 0.69s`.

Reaches the user: no — this is a test-suite integrity guard, not a path a user drives directly;
it protects the assertions that in turn cover CLI-facing behaviour (e.g. the `remedy do` output
checked at `test_golden_path.py:98`), but the statement itself and its guard are internal to the
repository's test discipline.

**Verdict: GAP** — mutations 1-3 behave exactly as specified (and mutation 3 correctly shows the
statement makes no claim about assertions younger than the fork point), but the found miss is a
direct counter-example to the statement's own wording ("must turn some test red"): a fork-point
assertion was weakened to a tautology and nothing turned red, because the guard trusts a digest an
author of the very weakening can also supply. Closing test: an independent check that every
`REVIEWED_CHANGES` entry's claimed round actually appears with a PASS verdict in `.agent/
live_review.md` or its archive (a record the same commit cannot also author), not merely that a
digest the current file computes matches a table in the same file.

## Statement 2 — T002's red-proof applied to the data-root allocator

> T002's "Every changed test keeps a red-proof: a mutation of the production line it guards still
> turns it red", applied to the Built State's sentence "Every test's data root comes from one
> parent per test process, so no test lists the whole base temporary directory to number its root"
> (the `_data_root_allocator` fixture in `tests/conftest.py`). Reintroducing a per-root
> `tmp_path_factory.mktemp` call (which numbers by listing the base temporary directory) must turn
> some test red.

Node id: `tests/test_data_root_isolation.py::test_a_root_is_made_without_numbering_the_base_directory`.

Confirmed first, by reading pytest 9.0.3's own source
(`_pytest.tmpdir.TempPathFactory.mktemp`), that a numbered `mktemp` call always resolves
`root=self.getbasetemp()` and lists that whole directory via `make_numbered_dir` — so the mutation
below reproduces exactly the cost the Built State sentence describes.

**Mutation — reintroduce the per-root `mktemp` call, `tests/conftest.py:51-54`.**
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
        next(numbers)
        root = tmp_path_factory.mktemp("remedy-data-root")
        return root
```
Command: `python3 -B -m pytest tests/test_data_root_isolation.py -q -n auto -p no:cacheprovider`.
Red: `FAILED tests/test_data_root_isolation.py::test_a_root_is_made_without_numbering_the_base_directory`
— `AssertionError: mktemp lists the whole base temporary directory` (raised by the test's own
monkeypatch of `tmp_path_factory.mktemp`), `1 failed, 4 passed in 0.66s`. Green after revert:
`5 passed in 0.64s`.

**Miss found.** The guard monkeypatches only the `tmp_path_factory.mktemp` *attribute*. Replacing
the allocator with a call to pytest's own underlying numbering function, bypassing that attribute
but reproducing the identical regression (listing the whole base temp directory to pick the next
number), passes clean:
```
    def allocate():
        from _pytest.pathlib import make_numbered_dir
        next(numbers)
        root = make_numbered_dir(root=tmp_path_factory.getbasetemp(), prefix="remedy-data-root",
                                  mode=0o700)
        return root
```
Command: `python3 -B -m pytest tests/test_data_root_isolation.py -q -n auto -p no:cacheprovider` →
`5 passed in 0.64s` — all five tests pass, including the one meant to catch exactly this. The
allocator lists `tmp_path_factory.getbasetemp()` on every call here (verified against pytest's
source: `make_numbered_dir(root=..., ...)` lists `root` to find the next free number), which is the
literal behaviour the Built State sentence forbids, yet the test the statement names does not
notice because it asserts against one named method rather than against the directory-listing
symptom. Reverted; green confirmed again: `5 passed in 0.64s`.

Reaches the user: no — this guards the test suite's own CPU cost (fewer `os.listdir` calls across
21k+ tests), not a behaviour a user drives through the CLI or UI.

**Verdict: GAP** — the required mutation (literally reintroducing `tmp_path_factory.mktemp` per
root) is caught, but a mutation that reproduces the exact forbidden behaviour the Built State
sentence names — numbering a root by listing the whole base temporary directory — through pytest's
own internal numbering function instead of through the named method is not. Closing test: assert
on the symptom instead of the named call, e.g. wrap `os.scandir`/`os.listdir` (or count directory
entries) on `tmp_path_factory.getbasetemp()` itself across two `_data_root_allocator()` calls and
assert the base directory's own entry count does not grow, which no choice of numbering API can
evade.
