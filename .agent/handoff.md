# Handoff — F293 Test load diet, round 2

## Session

SESSION 1 of feature F293 · round 2 · rounds so far 2

This session continues from round 1's own session (context remained comfortable throughout
round 2; no `.agent/prose_slips.md` line was written). Round 2 wrote DECISION F293 D1 (resolving
the tension between round 1's own claim text and T002's Acceptance line — see below) and DECISION
F293 D2 (the caching design), implemented the fix, proved it with two new tests and two mutation
red-proofs in a disposable worktree, and measured its effect with targeted (not full-suite) runs.

## Range

Review of `fb565b944`..`HEAD` — five commits on `feature/f293-test-load-diet`: `5a311394b`,
`1130c3194`, `494713d33`, `acdb3b35b`, and this handback commit (not yet made at the time this
line was drafted).

## Commits

### `5a311394b` F293 R2 C1: DECISION F293 D1 (the full-suite-run tension) and D2 (the caching design)

| Path | +/- | Reason |
|---|---|---|
| `.agent/decisions.md` | +22/-0 | two new DECISION entries appended verbatim, per the round block's exact text |

`git show --numstat 5a311394b`: 22 `.agent/decisions.md` — **22 insertions total**.

### `1130c3194` F293 R2 C2: cache dead_command_ids' file scan per search root (DECISION F293 D2)

| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/dead_command_check.py` | +34/-10 | split the file-scan out of `dead_command_ids` into a new `_scan_search_root`, cached module-level in `_SCAN_CACHE` keyed by resolved `root`; `dead_command_ids` itself now reads `texts, pairs = _scan_search_root(root)` instead of re-scanning inline |

`git show --numstat 1130c3194`: 34/10 `packages/orchestration/dead_command_check.py` — **44
lines changed total**. `git diff` confirmed only this one span changed — the module docstring,
`_REPO_ROOT`, `_SEARCH_DIRS`, `_handler_names`, `_iter_search_files`, `_adjacent_string_pairs`,
and the rest of `dead_command_ids` from `dead: list[str] = []` onward are byte-identical to
before.

### `494713d33` F293 R2 C3: two new tests proving the per-root cache (DECISION F293 D2)

| Path | +/- | Reason |
|---|---|---|
| `tests/orchestration/test_dead_command_check.py` | +35/-0 | `test_the_file_scan_is_not_repeated_for_the_same_root` (call-count assertion via a counting wrapper on `_iter_search_files`) and `test_two_different_roots_never_share_a_cache_entry` (correctness assertion: same command_id dead under one root, alive under another) appended to `TestDeadCommandIds` |

`git show --numstat 494713d33`: 35 `tests/orchestration/test_dead_command_check.py` — **35
insertions total**.

### `acdb3b35b` F293 R2 C4: mutation red-proofs for the dead_command_ids cache

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f293-r2-mutations.txt` | +152/-0 (new file) | transcript of both mutations run in the disposable worktree `.remedy-wt/f293-r2-mut`, per G5 |

`git show --numstat acdb3b35b`: 152 `.agent/authored/f293-r2-mutations.txt` — **152 insertions
total**.

### This handback commit — F293 R2 C5: targeted verification and handback

| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +17/-3 | Current Step rewritten for round 2's result; Next Steps kept |
| `.agent/handoff.md` | full rewrite | this file |

## External actions

`git worktree add .remedy-wt/f293-r2-mut HEAD` (commit 4) and `git worktree remove
.remedy-wt/f293-r2-mut` + `git worktree prune` (commit 4, same step, as its last action) — `git
worktree list` before and after both showed the same 11 entries (primary checkout + 10
pre-existing, unrelated `.remedy-wt/job-*` worktrees belonging to other running sessions on this
shared machine; untouched). `git push origin feature/f293-test-load-diet` — run after this
handback commit; outcome reported in the session's reply, not in this file. No PR created this
round — the worker does not create PRs; that is the reviewer's action after reading the diff. No
`gh pr` commands.

## Verification

**Open PR Gate / state probe, before any work:**
```
$ cat .agent/STOP
cat: .agent/STOP: No such file or directory
$ git branch --show-current
feature/f293-test-load-diet
$ git status --porcelain
(empty)
```

**Two new tests, commit 3:**
```
$ python3 -m pytest tests/orchestration/test_dead_command_check.py -v
tests/orchestration/test_dead_command_check.py::TestDeadCommandIds::test_a_command_referenced_nowhere_is_dead PASSED [ 20%]
tests/orchestration/test_dead_command_check.py::TestDeadCommandIds::test_an_argv_list_pair_counts_as_a_reference PASSED [ 40%]
tests/orchestration/test_dead_command_check.py::TestDeadCommandIds::test_the_real_catalog_has_no_dead_commands PASSED [ 60%]
tests/orchestration/test_dead_command_check.py::TestDeadCommandIds::test_the_file_scan_is_not_repeated_for_the_same_root PASSED [ 80%]
tests/orchestration/test_dead_command_check.py::TestDeadCommandIds::test_two_different_roots_never_share_a_cache_entry PASSED [100%]
5 passed in 2.81s
```

**Ruff, production code and test file (commits 2, 3, and re-checked at commit 5):**
```
$ python3 -m ruff check packages/orchestration/dead_command_check.py tests/orchestration/test_dead_command_check.py
All checks passed!
```

**Mutation A — disable the cache (commit 4, full transcript in `.agent/authored/f293-r2-mutations.txt`):**
```
$ python3 -m pytest tests/orchestration/test_dead_command_check.py -v
... 4 PASSED ...
    monkeypatch.setattr(mod, "_iter_search_files", counting_iter)
    dead_command_ids(catalog, handlers, root=tmp_path)
    dead_command_ids(catalog, handlers, root=tmp_path)
>   assert calls["n"] == 1
E   assert 2 == 1
tests/orchestration/test_dead_command_check.py:62: AssertionError
FAILED tests/orchestration/test_dead_command_check.py::TestDeadCommandIds::test_the_file_scan_is_not_repeated_for_the_same_root
1 failed, 4 passed in 2.56s
```
Exactly the predicted split: only `test_the_file_scan_is_not_repeated_for_the_same_root` goes red, the other 4 stay green.

**Mutation B — break per-root keying (commit 4):**
```
$ python3 -m pytest tests/orchestration/test_dead_command_check.py -v
FAILED ...test_an_argv_list_pair_counts_as_a_reference
FAILED ...test_the_real_catalog_has_no_dead_commands
FAILED ...test_the_file_scan_is_not_repeated_for_the_same_root
FAILED ...test_two_different_roots_never_share_a_cache_entry
4 failed, 1 passed in 0.27s
```
**Deviation from the block's predicted SCOPE (not its predicted mechanism), declared explicitly:**
the block predicted only the target test would fail, with the other 4 staying green. The
whole-file run instead shows 4 of 5 failing. Cause, established by re-running the target test
alone:
```
$ python3 -m pytest tests/orchestration/test_dead_command_check.py::TestDeadCommandIds::test_two_different_roots_never_share_a_cache_entry -v
>   assert dead_command_ids(catalog, handlers, root=root_b) == []
E   AssertionError: assert ['ghost.vanish'] == []
1 failed in 0.21s
```
In isolation, exactly 1 failed — matching the prediction precisely. `_SCAN_CACHE` is a
module-level dict living for the whole pytest process; with a fixed key instead of `root`,
whichever test runs FIRST in the file seeds the one cache slot, and every later test's own
`root=` argument is ignored, reading that first test's stale scan back. This is not a defect in
the production fix or the new tests — it is a stronger demonstration of exactly the defect the
mutation introduces (the fix keys by `root`; this mutation breaks that), surfacing through more
call sites than the one test written to target it directly. Full transcript and explanation:
`.agent/authored/f293-r2-mutations.txt`.

**File restored after each mutation, confirmed empty diff both times** (`git checkout --
packages/orchestration/dead_command_check.py` in the worktree; `git diff` empty).

**`git worktree list` before creating `.remedy-wt/f293-r2-mut` and after removing it — identical
11 entries both times** (primary checkout + 10 unrelated `.remedy-wt/job-*` worktrees).

**Targeted: `tests/cli/test_worker_facade_cmd.py`:**
```
$ python3 -m pytest tests/cli/test_worker_facade_cmd.py -q --durations=0
...
(126 durations < 0.005s hidden.  Use -vv to show these durations.)
56 passed in 22.41s
```
Summed duration-lines (same parse method T001 used): **22.26s over 42 duration-lines**, against
T001's own reading of **125.54s over 40 duration-lines** — a **82.3% reduction**
((125.54-22.26)/125.54).

**Targeted: the other 4 T001-named files:**
```
$ python3 -m pytest tests/orchestration/test_dead_command_check.py tests/orchestration/test_disk_floor.py tests/orchestration/test_self_use_generator.py tests/orchestration/test_self_use_runner.py -q --durations=0
...
(439 durations < 0.005s hidden.  Use -vv to show these durations.)
170 passed in 15.82s
```
Summed duration-lines: **15.19s over 71 duration-lines**, against T001's combined reading of
**33.53s** (2.95 + 16.07 + 6.24 + 8.27) — a **54.7% reduction** ((33.53-15.19)/33.53).

**`tests/cli/` (whole directory), fully green:**
```
$ python3 -m pytest tests/cli/ -q
...
2254 passed in 402.55s (0:06:42)
```
No failures, no new skips.

**Integrity check:**
```
$ python3 -m apps.cli.main integrity check --json
{"check_count": 6, "checks": [
  {"message": "handlers=171", "name": "handler_import", "status": "pass"},
  {"message": "last Gate verdict PASS_WITH_RISKS", "name": "live_review_verdict", "status": "pass"},
  {"message": "unchecked=0, context_complete=False", "name": "plan_consistency", "status": "pass"},
  {"message": "untracked=0, relevant=0", "name": "relevant_untracked", "status": "pass"},
  {"message": "no reviewer scratch, evidence dir or archive at the root", "name": "repo_root_hygiene", "status": "pass"},
  {"message": "no open blocker/high findings", "name": "high_blockers_open", "status": "pass"}
], "fail_count": 0, "ok": true, "passed": true}
```

**Canary:**
```
$ python3 -m pytest tests/cli/test_golden_path.py -q
..........................................                               [100%]
42 passed in 44.63s
```

**No full suite run this round** (DECISION F293 D1: the closure's integration-gate run supplies
T002's "after" reading; no `REMEDY_TEST_MAX_WORKERS` set, no custom `-n` passed at any point).

## Authored-text proofs

The two DECISION entries in commit 1 were authored inline in this round's own task block, applied
by exact text append (`Edit`, matching the file's established one-blank-line spacing between
entries, confirmed by reading the tail of `.agent/decisions.md` before appending and re-reading
the resulting `git diff` afterward — one hunk, 22 insertions, no deletions, no trailing
whitespace). The production-code span in commit 2 and the two test methods in commit 3 were also
applied by exact text match against the block's own verbatim FROM/TO text and verbatim test code,
confirmed by `git diff` showing only the ordered span changed in each case. `.agent/authored/f293-r2-mutations.txt`
(commit 4) is this round's own measured transcript, not text applied to a target — its proof is
the pytest output it quotes, reproduced above.

## Deviations & assumptions

1. **Mutation B's failure scope** (see Verification section above, in full): the block predicted
   1 failed / 4 passed for the whole-file run; the actual whole-file run showed 4 failed / 1
   passed, because `_SCAN_CACHE` is a process-global singleton and pytest runs the whole file in
   one process — a fixed cache key lets the FIRST test's scan leak into every later test's result,
   not only the one test written to target the property directly. Confirmed by running the target
   test alone, which reproduced the predicted 1-failed/4-passed shape exactly. This is a stronger
   proof of the same defect, not a different one, and not a defect in the shipped fix (which keys
   by `root`, not a fixed string). Declared here per the instruction to record any departure from
   a block's predicted outcome even when the underlying mechanism is understood and correct.

No other deviations. Constraints honoured: only the six named paths were touched
(`.agent/decisions.md`, `packages/orchestration/dead_command_check.py`,
`tests/orchestration/test_dead_command_check.py`, `.agent/authored/f293-r2-mutations.txt`,
`.agent/plan.md`, `.agent/handoff.md`); no existing test's assertion was weakened, deleted, or had
its expected value changed — `tests/cli/test_worker_facade_cmd.py` and every other touched-area
file passed unchanged; no full suite run; every commit stayed under the 500-insertion cap (22, 44,
35, 152 changed lines respectively); every commit stayed on `feature/f293-test-load-diet`; no PR
opened; `.agent/STOP` did not appear at any point in this round.

## Open findings

**8 open**, unchanged by this round (this round resolved nothing against the ledger and registered
nothing new): `R-0413`, `R-0441`, `R-0471`, `R-0533`, `R-0632`, `R-0672`, `R-1117` (Medium, owned by
F290), `R-1118` (owned by F293 itself, unchanged from round 1's negative-result reading).

## Item-status table

| Item | Status | Reason |
|---|---|---|
| DECISION F293 D1 (full-suite-run tension) | done | written verbatim in commit 1 |
| DECISION F293 D2 (caching design) | done | written verbatim in commit 1 |
| Cache implementation (`_SCAN_CACHE` / `_scan_search_root`) | done | commit 2; `git diff` confirmed only the ordered span changed |
| Ruff clean (production + test file) | done | `All checks passed!`, re-checked at commit 5 |
| Two new tests passing | done | 5 passed (3 pre-existing + 2 new), commit 3 |
| Mutation A: target red, others green | done | 1 failed / 4 passed, exact predicted split |
| Mutation B: target red, others green | PARTIAL, deviation declared | target test failed as predicted; 3 further tests also failed in the whole-file run due to process-global cache pollution under a fixed key — confirmed this is the mutation's own broader effect, not a flaw in the fix or the tests; isolated run of the target test alone matched the prediction exactly |
| Targeted `test_worker_facade_cmd.py` improvement measured | done | 125.54s -> 22.26s, -82.3% |
| Targeted four-file improvement measured | done | 33.53s -> 15.19s, -54.7% |
| `tests/cli/` green | done | 2254 passed, 0 failed |
| Canary green | done | 42 passed |
| Integrity check green | done | fail_count: 0 |
| `.agent/plan.md` updated | done | Current Step rewritten, kept under 50 lines |

## Next

T002 continued: more cuts from `.agent/f293_inventory.md` sections 2-3's remaining top entries
(`test_job_task_runner.py`, `test_supervisor_portability.py`, `test_mission_cmd.py`,
`test_do_sequence_cli.py`, and the rest of the top-30 ranking), each with its own mutation
red-proof, until either the ranking is exhausted of easy wins or a dated DECISION rules no more
can be cut without weakening a test. The 40%-of-1246.09 Acceptance check itself is read at the
closure sequence's integration-gate run, per DECISION F293 D1 — not inside any T002 round.
