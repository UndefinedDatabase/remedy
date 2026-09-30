# F293 acceptance re-audit — "without losing a single assertion" (amend0930b-slow-cap)

Scope: `docs/roadmap/features/T2_F293.md` `## Goal & Done`, the clause "without losing a single
assertion", read against every test module F293's branch changed since it left `main`.

Fork point: `git merge-base HEAD origin/main` = `8a067a3b93fb3d7080053f9cf742379534bed447`.
Current branch tip: `ea594a6b9`.

Test modules changed since the fork point (`git diff --stat <fork>..HEAD -- tests/`):
`tests/cli/test_mission_cmd.py`, `tests/cli/test_worker_facade_cmd.py`, `tests/conftest.py`,
`tests/load_governor.py` (not a test module), `tests/orchestration/test_closure_suite_cost.py`
(new), `tests/orchestration/test_dead_command_check.py`, `tests/orchestration/test_job_budgets.py`,
`tests/orchestration/test_job_task_runner.py`,
`tests/orchestration/test_review_gate_sensitive_metadata.py`,
`tests/orchestration/test_run_manifest_security.py`, `tests/regression/test_f293_acceptance.py`
(new), `tests/regression/test_test_load_governor.py` (new), `tests/runtimes/test_dev_server.py`,
`tests/test_no_orphan_modules.py`.

## The guarding tests found

`tests/regression/test_f293_acceptance.py` already exists on this branch and carries two classes
that guard exactly this clause, against a hard-coded per-module floor (`FLOOR`, measured at the
fork commit) and a hard-coded allow-list of intentional changes (`ALLOWED_REMOVALS`,
`ALLOWED_CHANGES`):

- `TestNoAssertionWasLost.test_no_module_f293_changed_has_fewer_assertions_than_where_f293_began`
  — counts `ast.Assert` nodes and `.raises`/`.warns` attribute uses per module, fails if any
  module's count fell below its fork-point count minus its declared allowed removals.
- `TestNoAssertionWasWeakened.test_every_assertion_that_existed_where_f293_began_is_still_there_word_for_word`
  — for each changed module, diffs a `Counter` of `ast.unparse(node)` text for every `assert`/
  `.raises`/`.warns` node between the fork-point blob (`git show <fork>:<path>`) and the working
  file; fails if any text present at the fork is gone now, except the declared `ALLOWED_CHANGES`.

These two are the modules "the guard" for the rest of this report. All mutations below were made
to `tests/cli/test_mission_cmd.py` (the largest changed module, 266 assertions today, floor 266)
inside a disposable worktree, then proved by running only
`tests/regression/test_f293_acceptance.py`.

Baseline (unmutated, HEAD `ea594a6b9`, worktree):

    PYTHONDONTWRITEBYTECODE=1 python3 -B -m pytest tests/regression/test_f293_acceptance.py -q -n auto -p no:cacheprovider -rs
    exit 0
    .......                                                                  [100%]
    7 passed in 0.97s

## Mutations

### (a) Delete an assertion

File: `tests/cli/test_mission_cmd.py`, `TestStart.test_start_json_carries_the_record`.
Original (4 lines):

    assert body["mission"]["goal"] == "Keep it working"
    assert body["mission"]["status"] == "active"
    assert body["mission"]["job_links"] == []
    assert body["mission"]["dossier_ref"] == ""

Replacement (3 lines, last line removed):

    assert body["mission"]["goal"] == "Keep it working"
    assert body["mission"]["status"] == "active"
    assert body["mission"]["job_links"] == []

Reading: **RED**, exit code 1.

    .....FF                                                                  [100%]
    2 failed, 5 passed in 0.96s

Both guard tests fired: the floor test reported
`{'tests/cli/test_mission_cmd.py': {'floor': (266, 0), 'now': (265, 0)}}`; the word-for-word test
reported `{'tests/cli/test_mission_cmd.py': ["assert body['mission']['dossier_ref'] == ''"]}`.

### (b) Empty one in place

Same test. Original: `assert body["mission"]["status"] == "active"`.
Replacement: `assert True`.

Reading: **RED**, exit code 1.

    ......F                                                                  [100%]
    1 failed, 6 passed in 0.89s

Only the word-for-word test fired (the assertion count is unchanged, one `assert` swapped for
another, so the floor test stayed green): reported
`{'tests/cli/test_mission_cmd.py': ["assert body['mission']['status'] == 'active'"]}`.

### (c) Weaken a comparison

File: `tests/cli/test_mission_cmd.py`, `TestStart.test_start_prints_the_new_mission_id`.
Original: `assert len(mission_id) == 32`.
Replacement: `assert len(mission_id) >= 0`.

Reading: **RED**, exit code 1.

    ......F                                                                  [100%]
    1 failed, 6 passed in 0.89s

Only the word-for-word test fired (again, same count, different text): reported
`{'tests/cli/test_mission_cmd.py': ['assert len(mission_id) == 32']}`.

### (d) Hardest: neutralize the check without touching the assert's own text

Same test, the two lines just after (a):

Original:

    listing = _run(["mission", "list", "--project", project_id], data_root).stdout
    assert mission_id[:12] in listing
    assert "Keep the importer working" in listing

Replacement (one inserted line before the two asserts; the assert statements themselves are
byte-for-byte unchanged):

    listing = _run(["mission", "list", "--project", project_id], data_root).stdout
    listing = listing + mission_id[:12] + "Keep the importer working"
    assert mission_id[:12] in listing
    assert "Keep the importer working" in listing

Reading: **GREEN**, exit code 0.

    .......                                                                  [100%]
    7 passed in 0.87s

This mutation stays green. Neither guard inspects anything but the `Assert`/`raises`/`warns`
node's own source text and a bare count; a line inserted just before an assertion that manufactures
the value the assertion checks — forcing containment, equality, truthiness, etc. regardless of
what the production code under test actually did — is invisible to both. The assertion node's
text is identical before and after, so the word-for-word check sees no change, and the assertion
count is unchanged, so the floor check sees no change either. This is a real gap in the kind of
guard the feature relies on: it proves no assertion's SOURCE LINE was deleted or edited, not that
every assertion still discriminates real behavior. (The guard's own module lists exactly this
limitation by scope, not by claiming otherwise — it never states it catches data-flow neutering,
only text and count regressions — so this is a documented boundary, not a contradiction of what
the test module asserts about itself.)

All four mutations were reverted (`git checkout -- tests/cli/test_mission_cmd.py`) before the
worktree was destroyed; `git diff --stat` in the worktree was empty immediately before teardown.

## Is the claim true of the repository today?

Independently of the packaged guard (a from-scratch script run in the worktree, not calling into
`test_f293_acceptance.py`'s own code), for every one of the ten test modules F293's branch has
touched with assertion content (excluding the three brand-new files
`test_closure_suite_cost.py`, `test_f293_acceptance.py`, `test_test_load_governor.py`, which have
no fork-point predecessor to regress against), I recomputed `(assert count, raises/warns count)`
at the fork blob and at the current working file, and the full multiset of assertion source text
(`ast.unparse`) gained and lost between the two:

| Module | Fork (assert, raises/warns) | Now | Text GONE since fork |
|---|---|---|---|
| `tests/cli/test_mission_cmd.py` | (271, 0) | (266, 0) | `assert proc.returncode == 0, proc.stderr` ×5 |
| `tests/cli/test_worker_facade_cmd.py` | (148, 4) | (156, 4) | `assert list(result.keys()) == ['ready', 'checks', 'blockers', 'warnings', 'dead_commands', 'disk']` ×1 |
| `tests/orchestration/test_dead_command_check.py` | (3, 0) | (8, 0) | none |
| `tests/orchestration/test_job_budgets.py` | (225, 43) | (225, 43) | none |
| `tests/orchestration/test_job_task_runner.py` | (525, 2) | (525, 2) | none |
| `tests/orchestration/test_review_gate_sensitive_metadata.py` | (8, 0) | (13, 0) | none |
| `tests/orchestration/test_run_manifest_security.py` | (13, 3) | (19, 3) | none |
| `tests/regression/test_test_load_governor.py` | (47, 0) | (62, 0) | none |
| `tests/runtimes/test_dev_server.py` | (64, 6) | (64, 6) | none |
| `tests/test_no_orphan_modules.py` | (8, 0) | (8, 0) | none |

Every declared `FLOOR` value in `test_f293_acceptance.py` matched my own independent recount at
the fork commit exactly (no fabricated or stale numbers). The only two assertion texts that
disappeared anywhere, across all ten modules, are:

1. `assert proc.returncode == 0, proc.stderr` × 5, in `test_mission_cmd.py`. These were the
   subprocess-exit checks on five setup helpers (`_make_project`, `_start`, `_link_job`,
   `_pending_plan_job`, `_green_job`'s inlined script, `_append_trip_entry`) that the branch
   converted from a spawned `python -c` child process to an in-process call wrapped in
   `_in_data_root` (see the diff of `tests/cli/test_mission_cmd.py` against the fork blob). The
   check these asserts performed — "the setup write did not fail" — is preserved by construction:
   an in-process call that fails raises an exception, which still fails the test; nothing that
   previously turned red now turns green. This matches the module's own comment at
   `ALLOWED_REMOVALS`/`ALLOWED_CHANGES` and DECISION F293 D11.
2. `assert list(result.keys()) == ['ready', 'checks', 'blockers', 'warnings', 'dead_commands', 'disk']`
   × 1, in `test_worker_facade_cmd.py`, replaced by the same comparison with `'test_load'`
   appended to the expected list (T004's new doctor-core key). The new assertion is strictly
   stronger — it requires everything the old one did, plus one more key — never weaker.

Every other change across the ten modules is a pure addition (more `assert`/`raises`/`warns`
nodes than existed at the fork, zero removed). No comparison operator, membership test, or
equality check that existed at the fork was altered in a weakening direction anywhere in scope.

**The claim is true of the repository today**, read over the two justified exceptions above,
neither of which reduces what any test can catch.

## Verdict

**PROVEN**, with one disclosed gap: three of four mutation classes (delete, empty-in-place, weaken
a comparison) turn the guard red as required, but the fourth — shadowing the value under test in
a statement inserted just before an unchanged assert — stays green, so the guard proves textual
and numeric non-regression of assertions, not their continued behavioral strength.
