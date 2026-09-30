# Handoff — F293 Test load diet, round 8

## Session

SESSION 4 of feature F293 · round 8

Context self-assessment: the reviewer's context is comfortable and has room for several more
rounds this session.

## Range

Review of `382c9cbec`..`HEAD` — three commits on `feature/f293-test-load-diet`: `fd8114021`,
`fd3783412`, and this handback commit (not yet made at the time this line was drafted).

## Commits

### `fd8114021` F293 R8 C1: book round 7, record DECISION F293 D5, save the round 8 block

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f293-r8.md` | +134/-0 | NEW FILE at `.agent/authored/f293-r8.md`; byte-for-byte copy of this round's step block, `cmp`-verified against `.remedy-wt/f293-r8-block.md` before commit (`wc -l` 134, sha256 `4b6cd7892999e28c40dc3f238ad67298b950919834a420883449e2276ea6e9a7`) |
| `.agent/live_review.md` | +2/-0 | the F293 R7 Gate entry appended verbatim (bytes from `.remedy-wt/f293-r8-append-live_review.txt`); pre-commit blob (`git show 382c9cbec:.agent/live_review.md`) + append bytes verified byte-equal to the new file (`True`) |
| `.agent/decisions.md` | +12/-0 | DECISION F293 D5 appended verbatim (bytes from `.remedy-wt/f293-r8-append-decisions.txt`); pre-commit blob + append bytes verified byte-equal to the new file (`True`) |
| `.agent/plan.md` | +12/-10 | replaced whole-file by `cp` from `.remedy-wt/f293-r8-plan.md`; `cmp` silent |

`git show --numstat fd8114021`: `134 0 .agent/authored/f293-r8.md`, `12 0 .agent/decisions.md`,
`2 0 .agent/live_review.md`, `12 10 .agent/plan.md` — **160 insertions total**, well under the
500-insertion cap. The two appends' numstat matched the block's stated `2 0` and `12 0` exactly,
checked with `git diff --cached --numstat` before the commit.

### `fd3783412` F293 R8 C2: cache the run manifest's key check per key and use

| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/run_manifest.py` | +11/-1 | applied via `cp` of the reviewer's dry-run file `.remedy-wt/f293-r8-dry-run_manifest.py` (DECISION F293 D5): `import functools` added between `import errno` and `import hashlib`; `_is_safe_key` reduced to an `isinstance` check and a call to the new `_is_safe_str_key`, which carries `@functools.lru_cache(maxsize=4096)`, a docstring naming DECISION F293 D5, and the old body minus its `isinstance` test |
| `tests/orchestration/test_run_manifest_security.py` | +28/-0 | applied via `cp` of the reviewer's dry-run file `.remedy-wt/f293-r8-dry-test_run_manifest_security.py`: new class `TestSafeKeyAnswersPerKeyAndUse` added at the end of the file, with `test_the_detectors_run_once_per_key` and `test_a_dotted_key_is_answered_apart_for_each_use` |

`git show --numstat fd3783412`: `11 1 packages/orchestration/run_manifest.py`,
`28 0 tests/orchestration/test_run_manifest_security.py` — matching the block's stated numstat
exactly; **39 insertions total**, well under the 500-insertion cap. `git diff` before committing
showed only the changes the block named (`import functools` added between `import errno` and
`import hashlib`; `_is_safe_key` reduced to its string check and a call of `_is_safe_str_key`;
the new cached function with its DECISION F293 D5 docstring; and the one new test class at the
end of the file) and nothing else — read as this round's self-review, per the block's instruction.

### This handback commit — F293 R8 C3: handback

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | full rewrite | this file |

## External actions

No `git worktree` used this round (the block forbids mutation red-proofs this round — amend0930-
test-load rule 4 — the reviewer already ran them in the dry run per DECISION F293 D5). No `gh pr`
commands — no PR opened, none reviewed; `git fetch origin` confirmed `origin/feature/f293-test-
load-diet` equalled this session's starting `HEAD` (`382c9cbec`) before any commit was made, so no
peer session had pushed ahead. `git push origin feature/f293-test-load-diet` — run after this
handback commit; outcome reported in the session's own reply, not in this file.

## Verification

All six gates below were run once each, after C2 and before this commit, in the order the block
lists.

**1. `git status --porcelain`, then three `cmp` proofs:**
```
$ git status --porcelain
(empty)
$ cmp .agent/authored/f293-r8.md /home/decodeux/Repos/remedy/.remedy-wt/f293-r8-block.md
(silent)
$ cmp packages/orchestration/run_manifest.py /home/decodeux/Repos/remedy/.remedy-wt/f293-r8-dry-run_manifest.py
(silent)
$ cmp tests/orchestration/test_run_manifest_security.py /home/decodeux/Repos/remedy/.remedy-wt/f293-r8-dry-test_run_manifest_security.py
(silent)
```
All exit 0.

**2. `python3 -m ruff check packages/orchestration/run_manifest.py tests/orchestration/test_run_manifest_security.py`:**
```
$ python3 -m ruff check packages/orchestration/run_manifest.py tests/orchestration/test_run_manifest_security.py
All checks passed!
```
Exit 0.

**3. `python3 -m pytest tests/orchestration/test_job_task_runner.py -q -n 0 -p no:cacheprovider`:**
```
$ python3 -m pytest tests/orchestration/test_job_task_runner.py -q -n 0 -p no:cacheprovider
........................................................................ [ 33%]
........................................................................ [ 67%]
......................................................................   [100%]
214 passed in 37.34s
```
Exit 0. **214 passed**, matching the block's stated done-when exactly. Test load record's newest
line:
```
{"collected": 214, "command": "pytest tests/orchestration/test_job_task_runner.py -q -n 0 -p no:cacheprovider", "cpu_seconds": 38.15, "exit_status": 0, "utc": "2026-09-30T19:57:14Z", "wall_seconds": 37.35, "workers": 1}
```
`cpu_seconds` **38.15** — see Deviations below: the block states this is the primary checkout's
first reading after the change, not compared with the reviewer's worktree pair (70.59 before,
54.17 after); the prior primary-checkout reading at `b0faefe61` was 41.0, so 38.15 is consistent
with a real, if modest, reduction measured in the same tree.

**4. `python3 -m pytest tests/orchestration/test_run_manifest.py tests/orchestration/test_run_manifest_call_task_binding.py tests/orchestration/test_run_manifest_episode_graph.py tests/orchestration/test_run_manifest_hash_bindings.py tests/orchestration/test_run_manifest_ledger_semantics.py tests/orchestration/test_run_manifest_prework_resume.py tests/orchestration/test_run_manifest_role_agreement.py tests/orchestration/test_run_manifest_schema.py tests/orchestration/test_run_manifest_security.py tests/orchestration/test_run_manifest_strict_boundaries.py tests/orchestration/test_run_manifest_task_lifecycle_binding.py tests/orchestration/test_run_manifest_zero_call_expectations.py -q -n auto`:**
```
$ python3 -m pytest tests/orchestration/test_run_manifest.py tests/orchestration/test_run_manifest_call_task_binding.py tests/orchestration/test_run_manifest_episode_graph.py tests/orchestration/test_run_manifest_hash_bindings.py tests/orchestration/test_run_manifest_ledger_semantics.py tests/orchestration/test_run_manifest_prework_resume.py tests/orchestration/test_run_manifest_role_agreement.py tests/orchestration/test_run_manifest_schema.py tests/orchestration/test_run_manifest_security.py tests/orchestration/test_run_manifest_strict_boundaries.py tests/orchestration/test_run_manifest_task_lifecycle_binding.py tests/orchestration/test_run_manifest_zero_call_expectations.py -q -n auto
bringing up nodes...
........................................................................ [ 28%]
........................................................................ [ 56%]
........................................................................ [ 84%]
.........................................                                [100%]
257 passed in 8.52s
```
Exit 0. **257 passed**, matching the block's stated done-when exactly.

**5. `python3 -m pytest tests/cli/test_golden_path.py -q -n auto`:**
```
$ python3 -m pytest tests/cli/test_golden_path.py -q -n auto
bringing up nodes...
..........................................                               [100%]
42 passed in 7.72s
```
Exit 0. **42 passed**, matching the block's stated done-when exactly.

**6. `python3 -m apps.cli.main integrity check --json`:**
```
$ python3 -m apps.cli.main integrity check --json
{"check_count": 6, "checks": [
  {"message": "handlers=171", "name": "handler_import", "status": "pass"},
  {"message": "last Gate verdict PASS", "name": "live_review_verdict", "status": "pass"},
  {"message": "unchecked=0, context_complete=False", "name": "plan_consistency", "status": "pass"},
  {"message": "untracked=0, relevant=0", "name": "relevant_untracked", "status": "pass"},
  {"message": "no reviewer scratch, evidence dir or archive at the root", "name": "repo_root_hygiene", "status": "pass"},
  {"message": "no open blocker/high findings", "name": "high_blockers_open", "status": "pass"}
], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}
```
Exit 0. `fail_count` 0.

**No mutation red-proofs run this round** (amend0930-test-load rule 4: the reviewer already ran
them in the dry run per DECISION F293 D5 — without the `lru_cache` decorator the first new test is
red; with the wrapper answering `True` for every use the second new test is red; restored, the file
read 16 passed). **No full suite run this round** (DECISION F293 D1: T001's run and the closure's
integration-gate run are the feature's two full-suite readings; this round is neither).
`REMEDY_TEST_MAX_WORKERS` was never set; gate 3 passed `-n 0`, every other test command passed
`-n auto`; no two test commands ran at the same time; each gate ran exactly once.

## Authored-text proofs

`.agent/authored/f293-r8.md` (commit `fd8114021`): saved as a byte-for-byte copy of the step block
given to this round; `wc -l` read 134 lines, `sha256sum` read
`4b6cd7892999e28c40dc3f238ad67298b950919834a420883449e2276ea6e9a7`, and `cmp` against
`.remedy-wt/f293-r8-block.md` was silent (exit 0) both before and after the commit — re-verified
again in this round's Gate 1 above.

`.agent/live_review.md` (commit `fd8114021`): the pre-commit blob at `382c9cbec` was read with
`git show`, concatenated in Python with the prepared append file's raw bytes
(`.remedy-wt/f293-r8-append-live_review.txt`, sha256
`75ba15f9fe0782fab3fa205638102f9c1493e964132b777e544e5140da31aad9`, matching the block's stated
digest), and compared for byte equality against the resulting committed file: `True`. No text was
retyped.

`.agent/decisions.md` (commit `fd8114021`): the pre-commit blob at `382c9cbec` concatenated with
the prepared append file's raw bytes (`.remedy-wt/f293-r8-append-decisions.txt`, sha256
`05638c5d392b50753a7efa5ad4e7d3e69f93c633ccb21e0101bd60c68855b9cd`, matching the block's stated
digest) compared byte-equal to the committed file: `True`. No text was retyped.

`.agent/plan.md` (commit `fd8114021`): replaced whole-file via `cp` from `.remedy-wt/f293-r8-plan.md`
(sha256 `b058a44ab19c5d6cded7ec3758c4a12ff113647be2926567c0e2504eac0deffa`, matching the block's
stated digest); `cmp` against the source was silent both before and after the commit.

`packages/orchestration/run_manifest.py` (commit `fd3783412`): replaced whole-file via `cp` from
the reviewer's dry-run copy `.remedy-wt/f293-r8-dry-run_manifest.py` (sha256
`b9660a72e30b3202d221a0df87107070c6356ce745a6cb57202c4aa3111b0bb2`, matching the block's stated
digest); `cmp` against the source was silent both before the commit and again in this round's
Gate 1.

`tests/orchestration/test_run_manifest_security.py` (commit `fd3783412`): replaced whole-file via
`cp` from the reviewer's dry-run copy `.remedy-wt/f293-r8-dry-test_run_manifest_security.py`
(sha256 `9b124f8cdb054140884f2fc9e6049e11efda17613d48a1bf5e8db4e691d1a5d5`, matching the block's
stated digest); `cmp` against the source was silent both before the commit and again in this
round's Gate 1.

## Deviations & assumptions

One measurement observation, not a departure from the block's ordered commit sequence: the block
states plainly (§Goal item 2 and Gate 3) that this round's primary-checkout reading of
`tests/orchestration/test_job_task_runner.py` is not compared with the reviewer's worktree
before/after pair (70.59 / 54.17 CPU seconds) because a worktree costs more; it names only the
prior primary-checkout reading, 41.0 at `b0faefe61`, as the comparable figure. This round's primary
reading is 38.15, below that 41.0 baseline and consistent with the cut having an effect, though the
worktree pair's larger drop does not repeat verbatim in this tree — stated here per the rule that
any figure is reported exactly as measured, not adjusted to match a expectation across trees; no
attempt was made to guess around it or re-run the gate a second time (the block orders each gate
run once).

No other deviations. Both commits matched the block's named paths exactly. All three `cmp`-pairs in
C1 (block file) and C2 (both dry-run files) were silent. C1's numstat matched the block's stated
`2 0` and `12 0` appends exactly. C2's numstat matched the block's stated `11 1` and `28 0` exactly,
and `git diff` before the C2 commit showed only the named changes (`import functools` added
between `import errno` and `import hashlib`; `_is_safe_key` reduced to its string check and a call
of `_is_safe_str_key`; the new cached function with its DECISION F293 D5 docstring; and the one new
test class at the end of the file) and nothing else. No assertion was removed, weakened or had its
expected value changed. No file outside the named paths was touched. No production code outside
`packages/orchestration/run_manifest.py` was touched, and that file changed only via the C2 `cp`.
No mutation red-proofs run (reserved to the reviewer this round, per amend0930-test-load rule 4).
No full suite run (DECISION F293 D1). `.agent/STOP` did not appear at any point in this round. No
PR opened. No worktree used. `git fetch origin` before C1 confirmed no peer session had pushed
past this session's starting `HEAD` (`382c9cbec`).

## Open findings

`scripts.rotate_live_review.open_finding_ids` over `.agent/live_review.md` at this round's HEAD
(after C1's append) reads **2 open ids: `['R-1117', 'R-1118']`** — matching the block's own stated
ids exactly; this round's C1 append registered a Gate entry and a DECISION, and C1/C2 registered no
new `- R-` finding lines, so the open set is unchanged by this round's own work.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| Round 8 block saved verbatim (`.agent/authored/f293-r8.md`) | done | 134 lines, sha256 `4b6cd7892999e28c40dc3f238ad67298b950919834a420883449e2276ea6e9a7`, `cmp` silent |
| F293 R7 Gate entry booked | done | appended verbatim to `.agent/live_review.md`, byte-equality proof `True` |
| DECISION F293 D5 recorded | done | appended verbatim to `.agent/decisions.md`, byte-equality proof `True` |
| `.agent/plan.md` replaced | done | whole-file `cp`, `cmp` silent |
| `import functools` added | done | via `cp` of reviewer's dry-run file, `cmp` silent |
| `_is_safe_key` reduced to string check + `_is_safe_str_key` call | done | via `cp` of reviewer's dry-run file, `cmp` silent |
| `_is_safe_str_key` cached with `@functools.lru_cache(maxsize=4096)` | done | via `cp` of reviewer's dry-run file, `cmp` silent |
| `TestSafeKeyAnswersPerKeyAndUse` added | done | via `cp` of reviewer's dry-run file, `cmp` silent |
| Gate 1 `git status --porcelain` + three `cmp` proofs | done | empty status, all three `cmp` silent |
| Gate 2 `ruff check` | done | `All checks passed!` |
| Gate 3 file pytest (`-n 0`) + test load record | done | 214 passed; `cpu_seconds` 38.15 (observation noted above; prior primary reading 41.0 at `b0faefe61`) |
| Gate 4 twelve-file pytest | done | 257 passed |
| Gate 5 canary pytest | done | 42 passed |
| Gate 6 integrity check | done | `fail_count` 0 |
| Mutation red-proofs | skipped | reserved to the reviewer this round (amend0930-test-load rule 4); reviewer's dry-run results restated above, not re-run |
| Full suite run | skipped | DECISION F293 D1 reserves it to T001 and the closure's integration-gate round |
| Push to origin | done | `git push origin feature/f293-test-load-diet`, after this commit |
| PR opened | skipped | block orders no PR this round |

## Next

Operator questions open: 0.

1. Phase 1 rule 1 (`.agent/STOP`) — check first.
2. Phase 1 rule 2 (Open PR Gate) — check second.
3. Confirm `origin`'s tip equals the tip this handoff names before delegating.
4. The next T002 cut, ranked by CPU work it removes rather than by wall time: profile a candidate
   from `.agent/f293_inventory.md`'s CPU-share ranking (a wall-clock approximation, stated plainly
   in its own caveat) and propose a cut with a mutation red-proof, or a dated DECISION stating no
   more can be cut without weakening a test.
