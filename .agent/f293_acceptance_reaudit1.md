# F293 acceptance re-audit (amend0930b-slow-cap) — two claims

Repo: /home/decodeux/Repos/remedy, branch feature/f293-test-load-diet, HEAD cd189f212.
Fork point (`git merge-base HEAD origin/main`): `8a067a3b93fb3d7080053f9cf742379534bed447`.
Worktree used for every mutation: `/home/decodeux/Repos/remedy/.remedy-wt/f293-reaudit-wt`
(created `git worktree add --detach ... HEAD`, removed `git worktree remove --force ...` as the
last action; `git worktree list` afterward shows it gone, leaving only the pre-existing `job-*`
worktrees that were not touched). Primary checkout `git status --porcelain` was empty before and
after the audit; no file in it was edited, created or deleted.

Guarding test file for both claims: `tests/regression/test_f293_acceptance.py`.

---

## Claim 1

**Text (Acceptance, T001):** "`.agent/f293_inventory.md` exists and holds the six readings named
above from one run."

**Guarding test node ids:**
- `tests/regression/test_f293_acceptance.py::TestTheInventoryHoldsItsSixReadings::test_the_six_readings_are_there_in_order`
- `tests/regression/test_f293_acceptance.py::TestTheInventoryHoldsItsSixReadings::test_the_slowest_tests_are_a_hundred_rows_of_the_one_run`
- `tests/regression/test_f293_acceptance.py::TestTheInventoryHoldsItsSixReadings::test_the_totals_are_the_record_of_that_run`

**Mutation A (straightforward).** File `.agent/f293_inventory.md`, line 193.
- Original: `## 4. Tests that start a child process`
- Replacement: `## 4. Tests that start a subprocess`
- Red: `python3 -B -m pytest tests/regression/test_f293_acceptance.py -q -n auto -p no:cacheprovider`
  → exit 1, `1 failed, 4 passed in 0.93s` (`test_the_six_readings_are_there_in_order` failed,
  `AssertionError: ['## 4. Tests that start a child process']`).
- Green (reverted): same command → exit 0, `5 passed in 1.08s`.

**Mutation B (hard to catch).** File `.agent/f293_inventory.md`, one digit in one row of 100 in the
"100 slowest tests" table (line 141).
- Original: `| 50 | 3.68 | call | \`tests/cli/test_do_sequence_cli.py::test_force_job_on_an_order_naming_ten_files_yields_one_job_of_ten_tasks\` |`
- Replacement: same row with `3.68` → `3.69` (every other character unchanged; confirmed
  `.agent/authored/f293-r1-durations.txt` has a `3.68s call` line for that node and no `3.69s call`
  line for it).
- Red: same command → exit 1, `1 failed, 4 passed in 0.92s`
  (`test_the_slowest_tests_are_a_hundred_rows_of_the_one_run` failed, the mutated row's seconds/
  phase/node combination is not found anywhere in the one committed durations file).
- Green (reverted): same command → exit 0, `5 passed in 1.08s`.

**Is the claim true today?** Yes, by reading. `.agent/f293_inventory.md` exists and its six `##`
headings appear in order (verified with `grep -n "^## " .agent/f293_inventory.md`: sections 1–6 at
lines 11, 25, 80, 193, 209, 246). Section 3's 100 rows are ranks 1..100 and each row's exact
`<seconds>s <phase> <node>` line is present verbatim in the single committed
`.agent/authored/f293-r1-durations.txt`. The totals line quotes `collected` 21102, `wall_seconds`
355.02, `cpu_seconds` 1246.09, matching the same run's own text. All three guarding tests pass
unmutated.

**Verdict: PROVEN.** Both mutations — a renamed heading and a single mis-keyed digit buried in row
50 of 100 — turn the guard red, and the guard is green with the original content; the claim holds
against the repository as it stands.

---

## Claim 2

**Text (Goal & Done):** the cut comes "without losing a single assertion" (read against every test
module this branch changed since the fork point).

**Guarding test node id:**
- `tests/regression/test_f293_acceptance.py::TestNoAssertionWasLost::test_no_module_f293_changed_has_fewer_assertions_than_where_f293_began`

**Scope check.** `git diff --name-only 8a067a3b93fb3d7080053f9cf742379534bed447 HEAD -- tests`
lists 14 changed paths under `tests/`. Of those, `tests/conftest.py` and `tests/load_governor.py`
are not `test_*.py` modules (out of the claim's scope by its own wording); `tests/regression/test_f293_acceptance.py`
is the guard itself, newly added by this audit's predecessor; `tests/orchestration/test_closure_suite_cost.py`
did not exist at the fork point (`git cat-file -e <fork>:tests/orchestration/test_closure_suite_cost.py`
→ "Not a valid object name" — a brand-new file has no floor to fall below). The remaining 10 are
exactly the 10 keys of `FLOOR` in the guard. The guard's module list is complete against the
branch's actual diff — no changed pre-existing test module is left unguarded.

**Mutation A (straightforward).** File `tests/test_no_orphan_modules.py` (in the worktree only),
line 291, inside `test_every_allowed_unwired_entry_carries_a_reason`.
- Original:
  ```
      for path, reason in ALLOWED_UNWIRED:
          assert reason.strip() and "\n" not in reason, path
  ```
- Replacement:
  ```
      for path, reason in ALLOWED_UNWIRED:
          pass
  ```
- Red: same pytest command → exit 1, `1 failed, 4 passed in 0.72s`
  (`test_no_module_f293_changed_has_fewer_assertions_than_where_f293_began` failed:
  `{'tests/test_no_orphan_modules.py': {'floor': (8, 0), 'now': (7, 0)}}`).
- Green (reverted to the original two lines): same command → exit 0, `5 passed in 0.71s`.

**Mutation B (hard to catch — content-preserving).** Same file, same line.
- Original: `        assert reason.strip() and "\n" not in reason, path`
- Replacement: `        assert True, path`
- Reading: same pytest command → exit 0, `5 passed in 0.72s`. **The guard stays green.** Reverted
  to the original line; re-run confirms `5 passed in 0.73s`.

**Is the claim true today?** Measured directly (not from the guard): for every one of the 10
pre-existing FLOOR modules, I parsed the file's `ast.Assert` and `pytest.raises`/`pytest.warns`
attribute-access counts at the fork commit and at HEAD (script run: `python3 -B
.remedy-wt/f293-reaudit-measure.py`, reading both revisions with `git show <rev>:<path>`, no
worktree needed since this is read-only). Results:

| Module | at fork | at HEAD | declared allowed removal | verdict |
|---|---|---|---|---|
| tests/cli/test_mission_cmd.py | (271, 0) | (266, 0) | (5, 0) | OK, exactly the allowed drop |
| tests/cli/test_worker_facade_cmd.py | (148, 4) | (156, 4) | — | grew |
| tests/orchestration/test_dead_command_check.py | (3, 0) | (8, 0) | — | grew |
| tests/orchestration/test_job_budgets.py | (225, 43) | (225, 43) | — | unchanged |
| tests/orchestration/test_job_task_runner.py | (525, 2) | (525, 2) | — | unchanged |
| tests/orchestration/test_review_gate_sensitive_metadata.py | (8, 0) | (13, 0) | — | grew |
| tests/orchestration/test_run_manifest_security.py | (13, 3) | (19, 3) | — | grew |
| tests/regression/test_test_load_governor.py | (47, 0) | (62, 0) | — | grew |
| tests/runtimes/test_dev_server.py | (64, 6) | (64, 6) | — | unchanged |
| tests/test_no_orphan_modules.py | (8, 0) | (8, 0) | — | unchanged |

Every `FLOOR` value I measured at the fork commit matches the value hard-coded in the guard
exactly (10 of 10). Every HEAD count is at or above (floor − declared allowed removal). The only
net reduction anywhere is the declared 5 asserts in `test_mission_cmd.py`, which the guard's own
comment and F293 D11 explain: five child-process calls that asserted `proc.returncode == 0`
became in-process calls that raise on failure instead of returning a code to assert on, so the
check moved from an explicit assert to an implicit raise rather than disappearing. Taken as
"no assert-statement count dropped below its fork-point value, net of one declared and reasoned
exception," the claim is true today by direct measurement, independent of the guard.

However, the guard proves only a **count**, not that any given assertion still checks what it
checked at the fork point. Mutation B shows this concretely: gutting a real condition down to
`assert True` while keeping the `assert` statement (and its count) in place is a literal loss of
the thing the claim's English actually promises — no check was left behind, only a stub — and the
guard does not see it. This is a genuine gap in what "without losing a single assertion" is
actually proven to mean by `test_no_module_f293_changed_has_fewer_assertions_than_where_f293_began`;
it proves "no assert statements were deleted," not "no assertion's check was weakened."

**Verdict: GAP.** The count-based guard is real and catches outright deletion (Mutation A, red),
and the ten-module floor is measured accurately against the true fork point (my own independent
count matches the guard's FLOOR table in all 10 cases) with the one documented, reasoned exception
in `test_mission_cmd.py`. But the guard cannot detect — and Mutation B proves it does not detect —
an assertion whose condition is replaced by a tautology while its statement count is preserved, so
the claim "without losing a single assertion" is proven only in the narrower sense of "assert
statement count," not in the sense a plain reading of the English promises.
