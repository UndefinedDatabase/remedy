# F293 re-audit (amend0930b-slow-cap): "without losing a single assertion"

Scope: the test modules F293's branch changed since it forked from `origin/main`. Fork point,
measured with `git merge-base HEAD origin/main`: `8a067a3b93fb3d7080053f9cf742379534bed447`.
This matches the `FORK` constant already hard-coded in `tests/regression/test_f293_acceptance.py`.

## Changed test modules (pre-existing, modified) since the fork

`git diff --name-status <fork> HEAD` restricted to test files shows:

- Modified (existed at fork): `tests/cli/test_mission_cmd.py`, `tests/cli/test_worker_facade_cmd.py`,
  `tests/conftest.py`, `tests/orchestration/test_dead_command_check.py`,
  `tests/orchestration/test_job_budgets.py`, `tests/orchestration/test_job_task_runner.py`,
  `tests/orchestration/test_review_gate_sensitive_metadata.py`,
  `tests/orchestration/test_run_manifest_security.py`,
  `tests/regression/test_test_load_governor.py`, `tests/runtimes/test_dev_server.py`,
  `tests/test_no_orphan_modules.py`.
- Added (new, not pre-existing): `tests/orchestration/test_closure_suite_cost.py`,
  `tests/regression/test_f293_acceptance.py`, `tests/load_governor.py` (production-side helper,
  not a test module).

Nature of the modifications, read from the diffs:
- `test_mission_cmd.py`: five setup helpers (`_make_project`, `_start`, `_link_job`,
  `_pending_plan_job`, `TestContinue._green_job`, `_append_trip_entry`) rewritten from
  `subprocess.run([sys.executable, "-c", ...])` to an in-process call wrapped in a new
  `_in_data_root` context manager (T002: child process is not what the test is about). Each
  helper's old `assert proc.returncode == 0, proc.stderr` is gone; the in-process call raises on
  its own failure instead. No test method's own assertions were touched.
- `test_worker_facade_cmd.py`: two existing key-set assertions extended to also require the new
  `"test_load"` key (a widening, not a weakening); one new test class added (T004 coverage).
- `conftest.py`: new session-scoped fixture that freezes `remedy_worktree_identity()` once per
  process, and a `pytest_sessionfinish` hook that fails the run and kills any process left behind
  carrying the run's mark (T003). No existing assertion touched.
- `test_dead_command_check.py`: three new test methods appended; no existing line changed.
- `test_job_budgets.py`: `test_callback_fires_on_retry` gained a `unittest.mock.patch` of the
  30-second retry sleep plus a new `mock_sleep.assert_called_once_with(...)` assertion; the two
  pre-existing assertions below it are untouched.
- `test_job_task_runner.py`: a new `_install_fake_claude_cli` helper added; two existing tests
  gained a `monkeypatch` fixture parameter and one call to the helper so a real paid `claude` CLI
  call is faked. No assertion in either test body was changed.
- `test_review_gate_sensitive_metadata.py`, `test_run_manifest_security.py`,
  `test_test_load_governor.py`: only new tests/classes appended.
- `test_dev_server.py`: the deadline-loop and `wait_ready()` call in one existing test wrapped in
  `try/finally` so a leaked server is stopped; the assertions on `res` after the block are
  unchanged text, unchanged position relative to the call that feeds them.
- `test_no_orphan_modules.py`: one new entry added to the `ALLOWED_UNWIRED` allow-list for a new
  script the feature added (`scripts/closure_suite_cost.py`); no existing assertion changed.

## The guard already in the repository

`tests/regression/test_f293_acceptance.py`'s `TestNoAssertionWasLost` and
`TestNoAssertionWasWeakened` are the tests that exist specifically to fail if this Goal & Done
line stopped being true:
- `test_no_module_f293_changed_has_fewer_assertions_than_where_f293_began` — counts `ast.Assert`
  nodes and `pytest.raises`/`pytest.warns` uses per changed file and compares against a `FLOOR`
  recorded at the fork commit (minus a documented, reviewed `ALLOWED_REMOVALS`).
- `test_every_unit_that_existed_where_f293_began_is_unchanged_or_reviewed` — for every function,
  method and module-level assignment that existed in a changed file at the fork commit, compares
  its `ast.unparse` text today against then; any difference must match a hash recorded in
  `REVIEWED_CHANGES`, or the test fails.

Baseline run, this worktree, unmutated:
```
PYTHONDONTWRITEBYTECODE=1 python3 -B -m pytest -q -n auto -p no:cacheprovider -rs tests/regression/test_f293_acceptance.py
7 passed in 1.07s   (exit 0, no skips)
```

## Own measurement of the claim, today

Re-ran the same `ast`-based count independently (script written in the worktree, not the FLOOR
table itself) against every file in `FLOOR`:

| file | now (asserts, raises) | floor (after ALLOWED_REMOVALS) | meets floor |
|---|---|---|---|
| tests/cli/test_mission_cmd.py | (266, 0) | (266, 0) | yes |
| tests/cli/test_worker_facade_cmd.py | (156, 4) | (148, 4) | yes |
| tests/orchestration/test_dead_command_check.py | (8, 0) | (3, 0) | yes |
| tests/orchestration/test_job_budgets.py | (225, 43) | (225, 43) | yes |
| tests/orchestration/test_job_task_runner.py | (525, 2) | (525, 2) | yes |
| tests/orchestration/test_review_gate_sensitive_metadata.py | (13, 0) | (8, 0) | yes |
| tests/orchestration/test_run_manifest_security.py | (19, 3) | (13, 3) | yes |
| tests/regression/test_test_load_governor.py | (62, 0) | (47, 0) | yes |
| tests/runtimes/test_dev_server.py | (64, 6) | (64, 6) | yes |
| tests/test_no_orphan_modules.py | (8, 0) | (8, 0) | yes |

Every module meets or exceeds its floor by count, matching the guard's own verdict. Combined with
manual reading of every diff above (no pre-existing assertion's text differs from the fork version
except through the six `REVIEWED_CHANGES` entries, each of which is a documented, in-scope
mechanical change — subprocess-to-in-process setup, a widened key-set check, a mocked sleep, a
faked CLI call, or a try/finally wrap — none of which drops or weakens what the test checks), the
claim reads as true today by my own measurement, subject to the one gap below.

## Mutations

All five run from `/home/decodeux/Repos/remedy/.remedy-wt/f293-reaudit3-wt`, one at a time, each
verified to parse first, each run as
`PYTHONDONTWRITEBYTECODE=1 python3 -B -m pytest -q -n auto -p no:cacheprovider -rs tests/regression/test_f293_acceptance.py`
(or, for the follow-up production-side probes under mutation (e), the single targeted test node),
and each reverted immediately after before the next.

### (a) Delete an assertion
File: `tests/cli/test_mission_cmd.py`, `TestStart.test_start_json_carries_the_record`.
- Original: `        assert body["mission"]["goal"] == "Keep it working"` (line deleted entirely).
- Replacement: line removed.
- Reading: **RED**. `2 failed, 5 passed in 1.09s` (exit 1). Both guard tests failed:
  `test_no_module_f293_changed_has_fewer_assertions_than_where_f293_began` (count dropped to
  265 < floor 266) and `test_every_unit_that_existed_where_f293_began_is_unchanged_or_reviewed`
  (the method's text no longer matches the fork version and has no `REVIEWED_CHANGES` entry).
- Baseline (mutation reverted): green, `7 passed in <1s`.

### (b) Empty an assertion in place
Same file/test.
- Original: `        assert body["mission"]["goal"] == "Keep it working"`
- Replacement: `        assert True`
- Reading: **RED**. `1 failed, 6 passed in 1.08s` (exit 1). The assert-count test stayed green
  (node count unchanged), but `test_every_unit_that_existed_where_f293_began_is_unchanged_or_reviewed`
  caught it (unit text changed, unreviewed). This shows the count-only check alone would have
  missed an in-place emptying; the content-hash check is what actually catches it.
- Baseline (reverted): green.

### (c) Weaken a comparison
Same file/test.
- Original: `        assert body["mission"]["status"] == "active"`
- Replacement: `        assert body["mission"]["status"] in ("active", "inactive", "completed", "archived")`
- Reading: **RED**. `1 failed, 6 passed in 1.08s` (exit 1), same guard
  (`test_every_unit_that_existed_where_f293_began_is_unchanged_or_reviewed`) as (b).
- Baseline (reverted): green.

### (d) Leave the assertion's text untouched, change what feeds it
Same file/test.
- Original: nothing inserted between `body = json.loads(...)` and
  `assert body["mission"]["goal"] == "Keep it working"`.
- Replacement: inserted, before the first assert,
  `        body = {"mission": {"goal": "Keep it working", "status": "active", "job_links": [], "dossier_ref": ""}}`
  — a hard-coded value that makes every following assertion trivially true regardless of what the
  CLI actually printed. No assertion line's own text changed.
- Reading: **RED**. `1 failed, 6 passed in 1.08s` (exit 1),
  `test_every_unit_that_existed_where_f293_began_is_unchanged_or_reviewed` again (the function's
  unparsed text gained a statement, so it no longer matches the fork version).
- Baseline (reverted): green.

### (e) Hardest case: weaken an assertion inside a test that did not exist at the fork
File: `tests/orchestration/test_dead_command_check.py`,
`TestDeadCommandIds.test_the_file_scan_is_not_repeated_for_the_same_root` — this whole method was
added by F293 (absent from the file at the fork commit), so it is not in either guard's "before"
set.
- Original: `        assert calls["n"] == 1`
- Replacement: `        assert calls["n"] >= 0`
- Reading of `tests/regression/test_f293_acceptance.py`: **GREEN**, `7 passed in 0.96s` (exit 0) —
  identical to the unmutated baseline. Neither guard test fired: the assert-count guard only
  enforces a floor (a vacuous extra `assert` still satisfies "at least N"), and the unit-text guard
  only compares units present in the file at the fork commit, so a brand-new test's body is never
  compared to anything.
- The mutated test itself, run alone, also still passes:
  `tests/orchestration/test_dead_command_check.py::TestDeadCommandIds::test_the_file_scan_is_not_repeated_for_the_same_root`
  → `1 passed in 0.77s`.
- To show the weakening is real (not just theoretically possible), the caching it guards
  (`packages/orchestration/dead_command_check.py`, `_SCAN_CACHE` early-return) was disabled in the
  same worktree (`if cached is not None: return cached` → `if False and cached is not None:`).
  With caching fully broken and the weakened assertion (`>= 0`) still in place, the test **still
  passed** (`1 passed in 0.76s`) — a real regression, silently missed. Restoring the assertion's
  original text (`== 1`) against the same broken production code turned it **red**
  (`assert 2 == 1`, `1 failed in 0.77s`), proving the original assertion was a genuine guard that
  this mutation would have lost in practice, not merely on paper. Both files were then reverted to
  the baseline text.

Baseline confirmed once more after all five mutations and reverts: `git diff --stat` in the
worktree is empty for tracked files; `tests/regression/test_f293_acceptance.py` again gives
`7 passed in 0.96s`.

## Verdict

**PROVEN**, with one honestly-reported gap.

Four of five mutations — deleting an assertion, emptying one in place, weakening a comparison, and
changing what feeds an untouched assertion — are all caught (turn `tests/regression/test_f293_acceptance.py`
red) when applied to a test that existed where F293 began, via one or both of its two guard tests.
The fifth mutation — weakening an assertion inside a test added by F293 itself, inside an
otherwise-tracked file — is not caught by either existing guard test, and was independently
confirmed (by disabling the production caching it exercises) to be a real, not merely theoretical,
loss of a working regression check. That gap does not falsify the feature file's claim as written:
the claim and both guard tests are scoped to assertions "that existed where F293 began," and this
mutated assertion was new, added by F293, not one that existed before it. No mutation in this audit
found a pre-existing assertion silently weakened by the feature's actual changes — the gap is a
blind spot in the guard's own coverage (new tests are unchecked), not evidence that the shipped
diff already lost or weakened a pre-existing assertion. By the feature file's own wording ("no
assertion is weakened or deleted" of what existed before), the claim holds for every test module
changed since the fork, confirmed both by direct reading of every diff and by five red/green
mutation trials.

## Worktree cleanup

Worktree used: `/home/decodeux/Repos/remedy/.remedy-wt/f293-reaudit3-wt` (created with
`git worktree add --detach ... HEAD`). Removed as the last action with
`git worktree remove --force`; `git worktree list` afterward shows only the primary checkout.
Primary checkout `git status --porcelain` was empty before and after this audit; no file in it was
edited, created, deleted, committed, pushed, stashed, or checked out.
