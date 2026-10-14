# Handback — F308 round 1 — claim F308, book F306 R12, and take the three structural steps into `packages/orchestration/run_task_list.py`

## Session

SESSION 1 of feature F308 · round 1 · rounds so far 1

Context self-assessment: all four commits and all six gates landed exactly as the block ordered on
the first attempt, every digest check, byte comparison and numstat reading matched, and context held
comfortably throughout.

Fortschritt: ~30 % (claim and the structural steps landed · T001 to T003 open) — Schätzung

## Range

Review of `1622c16d7`..`df3b496e1`

## Commits

### 22788eabc F308 R1 C1: claim F308, book F306 R12, re-head the ledger, DECISION F308 D1

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f308-r1.md` | +201/-0 | NEW FILE, byte copy of `block.md` (201 lines, sha256 `ba3c0cbc7363e101f498cb3d6dc37714fc52656db1e9f9b68eb341caa294d521`) |
| `docs/roadmap/STATUS.md` | +1/-1 | F308's line `[ ]` becomes `[~]`, byte-identical to `dry-STATUS.md` |
| `.agent/live_review.md` | +23/-21 | re-headed at the F308 claim, F306 R12's verdict booked at the end, byte-identical to `dry-live_review.md` |
| `.agent/decisions.md` | +12/-0 | DECISION F308 D1 appended, byte-identical to `dry-decisions.md` |
| `.agent/plan.md` | +11/-11 | rewritten for this round, byte-identical to `dry-plan.md` |
| `.agent/context.md` | +10/-9 | rewritten for this round, byte-identical to `dry-context.md` |

### 2738b77a6 F308 R1 C2: the expectation of a task without a run leaves _collect_calls (structure step)

| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/run_task_list.py` | +57/-0 | NEW FILE, module docstring plus `expect_task_without_run`, moved unchanged (indentation only) from `_collect_calls`'s `if not run_id:` body |
| `packages/orchestration/run_manifest.py` | +2/-30 | top-of-file import of `expect_task_without_run` added; `_collect_calls` calls it and its own `TASK_BLOCKED`/`TASK_FAILED`/`TASK_VETOED` imports (unused after the move) removed |
| `docs/system/structure-ledger-v1.md` | +4/-3 | `_collect_calls` row 303→274, `run_manifest.py` file row 6260→6232, `_collect_calls` bullet gains its step-(2) sentence |
| `tests/test_structure_ratchet.py` | +2/-2 | `MAX_FUNCTION_LINES` 30651→30622, `MAX_FILE_LINES` 73740→73712 |
| `tests/orchestration/import_reachability_allowlist.txt` | +1/-0 | `packages.orchestration.run_task_list` added in sorted position |

### 598d777b4 F308 R1 C3: the split of a task over its class cap leaves run_job (structure step)

| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/run_task_list.py` | +64/-0 | `split_task_over_class_cap` added, moved unchanged from `run_job`'s `else:` branch, with its three named changes (`_persist_job`→`save_job_plan`, `continue`→`return True`, trailing `return False`) |
| `packages/orchestration/pingpong_job.py` | +3/-41 | `run_job`'s `else:` branch reduced to the import, the call and `continue` |
| `docs/system/structure-ledger-v1.md` | +7/-3 | `run_job` row 1486→1448, `pingpong_job.py` file row 5393→5355, both bullets gain their "Outside those steps" sentence |
| `tests/test_structure_ratchet.py` | +2/-2 | `MAX_FUNCTION_LINES` 30622→30584, `MAX_FILE_LINES` 73712→73674 |

### df3b496e1 F308 R1 C4: the declared task list and its check across episodes leave run_manifest.py (structure step)

| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/run_task_list.py` | +29/-0 | `declared_job_input_task_ids` moved unchanged, `task_list_chain_problems` added (the moved agreement check) |
| `packages/orchestration/run_manifest.py` | +7/-27 | top-of-file import gains the two new names; `declared_job_input_task_ids` deleted; `validate_run_manifest` and `validate_task_lifecycle_chain` each reduced to a one-line call |
| `docs/system/structure-ledger-v1.md` | +12/-4 | `validate_run_manifest` row 235→230 with its new boundary bullet, `validate_task_lifecycle_chain` row (101) deleted, `run_manifest.py` file row 6232→6212, its bullet gains the "Outside those steps" sentence |
| `tests/orchestration/test_run_manifest_task_history_chain.py` | +1/-1 | its one import of `declared_job_input_task_ids` re-pointed to `run_task_list` |
| `tests/test_structure_ratchet.py` | +3/-3 | `MAX_FUNCTION_ROWS` 160→159, `MAX_FUNCTION_LINES` 30584→30478, `MAX_FILE_LINES` 73674→73654 |

### (this commit) F308 R1 C5: handback

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | this commit | full rewrite per `docs/agents/handback_template.md` |

## External actions

- No worktree added or removed. No `gh pr merge`, `gh pr edit`, no `gh pr create` (the block orders
  no PR this round). No branch created beyond C0's `feature/f308-run-manifest-task-split`, no stash
  touched.
- `gh pr list --state open --json number,headRefName,baseRefName,isDraft` read `[]` before C0, so the
  Open PR Gate passed with nothing to merge.
- Push (`git push -u origin feature/f308-run-manifest-task-split`) runs after this commit; its
  outcome is reported in the session's final reply only, per the write-once rule — it did not exist
  when this file was written.

## Verification

Preconditions confirmed before C0: `git status --porcelain` was empty on `main`; `git rev-parse HEAD`
read `1622c16d70546143def6be8d441aa59a2522f623`. `git checkout -b feature/f308-run-manifest-task-split`
left `HEAD` at the same SHA. `git branch --show-current` read
`feature/f308-run-manifest-task-split` before every commit, as ordered.

`block.md` was verified first: 201 lines, sha256
`ba3c0cbc7363e101f498cb3d6dc37714fc52656db1e9f9b68eb341caa294d521` — matches the digest given in the
prompt that delivered it. Every one of the eight prepared files the Bundle names (`dry-STATUS.md`,
`dry-live_review.md`, `dry-decisions.md`, `dry-plan.md`, `dry-context.md`, `verify.py`,
`run_selection.py`, `selection.txt`) was checked by a Python sha256 reader before any use — all
eight `OK`.

C1: the block and the five `dry-*` files were written by a read-only-source Python copy script,
proved byte-equal to their sources by `filecmp.cmp` in the same script, then
`git diff --cached --numstat` read exactly `201 0 .agent/authored/f308-r1.md`, `10 9 .agent/context.md`,
`12 0 .agent/decisions.md`, `23 21 .agent/live_review.md`, `11 11 .agent/plan.md`,
`1 1 docs/roadmap/STATUS.md` — the block file's insertions equal its `wc -l` (201), and no other path
appeared.

C2–C4: each commit's diff was read in full (`git diff --cached`) before committing, checked against
the block's own description of the move (names, signatures, the three named changes in C3, the
one-line replacements in C4) and against a direct read of the source functions beforehand; ruff was
run over every file the block names after each edit, `All checks passed!` every time; the structure
ratchet and import-reachability tests were run after C2 and after C4, and a targeted sample of
`run_manifest`/`pingpong_job`/`run_task_list`-adjacent test files was run after each commit — all
green, reported below.

Measures were read with the test's own `measure_repository(REPO, paths=SCOPE)` (the same scope
`tests/test_structure_ratchet.py` uses) rather than the bare `remedy integrity structure` command,
because that command's default `--path` covers more of the repository than the ledger's scope and
does not reproduce the ledger's numbers; this is reported as a deviation below.

Per-commit test runs during development (not the gate):
- After C2: `pytest tests/test_structure_ratchet.py tests/orchestration/test_import_reachability.py`
  — 8 passed. `pytest tests/orchestration/test_run_manifest.py
  tests/orchestration/test_run_manifest_zero_call_expectations.py
  tests/orchestration/test_run_manifest_call_expectation_lifecycle.py
  tests/orchestration/test_run_manifest_task_lifecycle_binding.py` — 106 passed.
- After C3: `pytest tests/test_structure_ratchet.py tests/orchestration/test_import_reachability.py`
  — 8 passed. `pytest tests/orchestration/test_job_task_runner.py
  tests/orchestration/test_task_granularity.py` — 245 passed.
  `pytest tests/orchestration/test_f018_package_pipeline_e2e.py` — 29 passed (covers the
  `_persist_job` monkeypatch path through `save_job_plan`).
- After C4: `pytest tests/test_structure_ratchet.py tests/orchestration/test_import_reachability.py
  tests/orchestration/test_run_manifest_task_history_chain.py` — 32 passed. `pytest
  tests/orchestration/test_run_manifest.py tests/orchestration/test_run_manifest_zero_call_expectations.py
  tests/orchestration/test_run_manifest_call_expectation_lifecycle.py
  tests/orchestration/test_run_manifest_task_lifecycle_binding.py
  tests/orchestration/test_run_manifest_ledger_chain_continuity.py
  tests/orchestration/test_run_manifest_terminal_consistency.py
  tests/orchestration/test_run_manifest_terminal_ledger_finality.py` — 159 passed.

Gate 1: `git status --porcelain` — empty. Then
`python3 /home/decodeux/Repos/remedy/.remedy-wt/f308-r1/prep/verify.py /home/decodeux/Repos/remedy` —
every line started `True`, last line `ALL True`:
```
True 22788eabc has the single parent 1622c16d7 (F308 R1 C1)
True 2738b77a6 has the single parent 22788eabc (F308 R1 C2)
True 598d777b4 has the single parent 2738b77a6 (F308 R1 C3)
True df3b496e1 has the single parent 598d777b4 (F308 R1 C4)
True exactly one commit with the subject prefix F308 R1 C1
True exactly one commit with the subject prefix F308 R1 C2
True exactly one commit with the subject prefix F308 R1 C3
True exactly one commit with the subject prefix F308 R1 C4
True at most one commit with the subject prefix F308 R1 C5
True the range holds C1 to C4 and at most C5 (4)
True C1 .agent/authored/f308-r1.md equals block.md
True C1 docs/roadmap/STATUS.md equals dry-STATUS.md
True C1 .agent/live_review.md equals dry-live_review.md
True C1 .agent/decisions.md equals dry-decisions.md
True C1 .agent/plan.md equals dry-plan.md
True C1 .agent/context.md equals dry-context.md
True C1 names exactly its paths []
True C2 stays inside its paths []
True C2 insertions 66 below 500
True C3 stays inside its paths []
True C3 insertions 76 below 500
True C4 stays inside its paths []
True C4 insertions 52 below 500
True the test file changed only in import lines [...]
True run_task_list imports neither module at its top ['__future__', 'datetime', 'typing']
True run_task_list defines [] missing
True run_manifest no longer defines the reader
True the runless branch left _collect_calls
True run_job calls split_task_over_class_cap and no longer splits itself
True the chain's task-list check left validate_task_lifecycle_chain
True no consumer imports the reader from run_manifest 
ALL True
```
Exit 0.

Gate 2: `python3 -m ruff check packages/orchestration/run_task_list.py
packages/orchestration/run_manifest.py packages/orchestration/pingpong_job.py
tests/test_structure_ratchet.py tests/orchestration/test_run_manifest_task_history_chain.py` —
exit 0, `All checks passed!`.

Gate 3: `python3 /home/decodeux/Repos/remedy/.remedy-wt/f308-r1/prep/run_selection.py
/home/decodeux/Repos/remedy /home/decodeux/Repos/remedy/.remedy-wt/f308-r1-worker/selection-output.txt`
— exit 0. Paths: `191 paths`. Summary: `7250 passed, 5 skipped in 95.58s (0:01:35)`. No FAILED,
ERROR or `process(es) behind` line. Every SKIPPED line:
```
SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252): .claude/agents/remedy-reviewer.md was deleted deliberately in 219dd32 (finding R-0074 — superseded by the split workflow's Window 1, docs/agents/planner_reviewer_prompt.md). The read-only reviewer contract now lives there. Backlog: re-pin this contract on the split-workflow docs, or retire the test.
SKIPPED [1] tests/regression/test_f293_acceptance.py:191: main holds F293, so its own changes are history
SKIPPED [1] tests/regression/test_f294_acceptance.py:73: main holds F294, so its own changes are history
SKIPPED [1] tests/test_install_smoke.py:175: install smoke is opt-in: set REMEDY_INSTALL_SMOKE=1 on a host with network access
SKIPPED [1] tests/test_repair_context_reviewer_memory.py:257: UI source not found
```

Gate 4: `python3 -m apps.cli.main integrity check --json` — exit 0:
```
{"check_count": 6, "checks": [{"message": "handlers=188", "name": "handler_import", "status": "pass"}, {"message": "last Gate verdict PASS", "name": "live_review_verdict", "status": "pass"}, {"message": "unchecked=0, context_complete=False", "name": "plan_consistency", "status": "pass"}, {"message": "untracked=0, relevant=0", "name": "relevant_untracked", "status": "pass"}, {"message": "no reviewer scratch, evidence dir or archive at the root", "name": "repo_root_hygiene", "status": "pass"}, {"message": "no open blocker/high findings", "name": "high_blockers_open", "status": "pass"}], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}
```
Six checks, all `pass`; `"fail_count": 0`.

Gate 5: `python3 -c "import scripts.rotate_live_review as r; print(r.open_finding_ids(open('.agent/live_review.md').read()))"`
— exit 0, list `['R-1246', 'R-1252', 'R-1276', 'R-1277', ..., 'R-1313']` (R-1246, R-1252, then
R-1276 to R-1313 in order), length 40.

Gate 6: `python3 -m apps.cli.main integrity structure` — first five lines:
```
Measured 9161 tracked text files and 31660 Python functions in /home/decodeux/Repos/remedy.
Functions above 100 lines: 182
    1448  packages/orchestration/pingpong_job.py:2455  run_job
    1318  packages/orchestration/pingpong_loop.py:2911  run_pingpong
     910  packages/orchestration/decision_queue.py:154  list_decisions
```
No line of the full output names `run_task_list` (grep count 0): no function in
`packages/orchestration/run_task_list.py` is named.

## Authored-text proofs

- `.agent/authored/f308-r1.md` against `block.md`: byte-equal, 201 lines, sha256
  `ba3c0cbc7363e101f498cb3d6dc37714fc52656db1e9f9b68eb341caa294d521`.
- `docs/roadmap/STATUS.md` (C1) against `dry-STATUS.md`: byte-equal.
- `.agent/live_review.md` (C1) against `dry-live_review.md`: byte-equal.
- `.agent/decisions.md` against `dry-decisions.md`: byte-equal.
- `.agent/plan.md` against `dry-plan.md`: byte-equal.
- `.agent/context.md` against `dry-context.md`: byte-equal.
- C2 to C4 wrote no prepared reviewer-authored text (the structural steps were the worker's own
  code, per the block's "These steps are YOURS to write"); nothing to compare there.

## Deviations & assumptions

1. The block's gate 6 and its own narrative say "read the measures with
   `python3 -m apps.cli.main integrity structure`." That command's default `--path` scope (the
   current directory, no exclusion of `apps/ui/package-lock.json`) measures more of the repository
   than `tests/test_structure_ratchet.py`'s `SCOPE` does, and its raw numbers for the touched
   functions/files did not match the ledger before any edit (183 vs. the ledger's 160 rows).
   Assumption: the measures that matter are the ones the ratchet test itself computes, so every row
   and pin in this round was set from `measure_repository(REPO, paths=SCOPE)` — the test's own
   function, called from a throwaway script under `.remedy-wt/f308-r1-worker/` — which exactly
   reproduced the ledger's pre-round numbers (160 function rows summing 30651, 36 file rows summing
   73740) before any edit. Gate 6 itself (`integrity structure` with no `--path`) is still run and
   reported verbatim, unscoped, exactly as ordered; only the ledger edits used the scoped measure.
2. The Session line in the block reads literally "SESSION 1 of feature F308 · round 1", which is a
   strict subset of the mandatory one-line format `docs/agents/handback_template.md` states
   (`SESSION <n> of feature <Fxxx> · round <r> · rounds so far <total>`). This handback writes
   "SESSION 1 of feature F308 · round 1 · rounds so far 1" — satisfying both the block's literal
   text as a prefix and the template's mandated field — rather than dropping the mandated
   `rounds so far` field.
3. The row-reorder question: lowering a row's line count (e.g. `_collect_calls` 303→274) left it out
   of the "largest first" descending order the page's prose describes, since neither table was
   otherwise re-sorted. The block's instruction was "lower the row... to its new measure," not
   "re-sort the table," and `tests/test_structure_ratchet.py` does not check row order (it reads
   both tables into unordered dicts), so rows were edited in place without re-sorting, to keep each
   diff to exactly the change the block named.

No other departure from the block's ordered commit sequence occurred: C0 through C4 landed in order,
each touching only the paths its own heading named, each self-reviewed over `git diff --cached`
before committing as the block's step 5 in C2–C4 required.

## For the operator, in plain sentences

This round claimed the next clean-up feature and did the groundwork a later round needs before it
can teach the run record what to do when a run splits a piece of work into smaller pieces. Three
small pieces of code moved, unchanged, into a module built to hold them, and every consumer of that
code was pointed at its new home with nothing old left behind to confuse a future reader. Nothing
about how Remedy behaves changed in this round; the proof is that every test that was passing before
is still passing now, by the same count. The next round writes down the shape of the new record and
makes the real behaviour change, proved by tests that fail without it.

## Next

1. Phase 1 rule 1: `.agent/STOP` — absent at this handoff.
2. The Open PR Gate, which runs at the start of the next session.
3. Booking this round's verdict in the next round's first commit.
4. DECISION F308 D2 and T001 to T003.

Operator questions open: 0.
Open findings: 40 (R-1252 owned by F308, the rest by F307).

## Item status

| Item | Status | Reason |
|---|---|---|
| C0 | done | branch created at `1622c16d70546143def6be8d441aa59a2522f623`, no pull |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |
| Gate 1 | done | `git status --porcelain` empty; `verify.py` all `True`, `ALL True` |
| Gate 2 | done | `All checks passed!` |
| Gate 3 | done | exit 0, 191 paths, 7250 passed, 5 skipped, no FAILED/ERROR/process-behind |
| Gate 4 | done | exit 0, six checks `pass`, `fail_count` 0 |
| Gate 5 | done | open set is R-1246, R-1252, R-1276 to R-1313, length 40 |
| Gate 6 | done | first five lines reported; `run_task_list` named zero times |
| C5 | done | this handback |
| Push | pending | runs after this commit; outcome reported in the session's final reply only |
