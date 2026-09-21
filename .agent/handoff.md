# Handoff — F283 Machine contracts, part two: refusal sweep, JSON gap, exit-code taxonomy · Round 3 · R-1020's FIRST REPAIR

## Session

SESSION 1 of feature F283 · round 3 · rounds so far 3

This round booked round 2's PASS, corrected R-1020's registration on the record with a
`DECISION F283 D1` record (not a second registration line), and landed the repair layer
`apps/cli/job_id_arg.py::resolve_job_id_or_fail`, which catches what `lookup_job_id`
raises and refuses through `fail()`. `job.py`'s six `resolve_job_id(` call sites moved
onto it and the round-2 strict xfail turned green with its mark deleted in the same
commit (C3). `resolve_job_id` itself, under `packages/`, was not touched. Context
self-assessment: roughly a third of the working budget remained at the point this
handoff was written.

## Range

Review of `fc8dfd85`..`HEAD`.

## Block self-verification (R-0954)

| reading | measured | given | equal |
|---|---|---|---|
| line count | 239 | 239 | True |
| sha256 | `ad8a1cba0a3c0d7ef686008734cb04eec0b39717d2a63a1a2ede4523bbd31c77` | `ad8a1cba0a3c0d7ef686008734cb04eec0b39717d2a63a1a2ede4523bbd31c77` | True |

Neither reading differed, so the round went ahead.

## Pre-flight

- `ls .agent/STOP`: `No such file or directory`. No STOP on disk.
- `git status --porcelain`: empty.
- `git branch --show-current`: `feature/f283-machine-contracts-part-two`.
- `git log --oneline -1`: `fc8dfd85`, matching the delegation message.

## Commits

### 2dc60bdc F283 R3 C1a: copy round 3 block into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f283-r3-block.md | +239/-0 | byte-for-byte copy of this round's step block |

Measured insertions (`git show --numstat`): **239**. Expected: the block's own measured
line count, 239. They **MATCH**. Well under the 500-line cap.

### 3a3f513c F283 R3 C1b: copy round 3 payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f283-r3-allowlist.diff | +12/-0 | byte-for-byte copy of allowlist.diff |
| .agent/authored/f283-r3-job.diff | +70/-0 | byte-for-byte copy of job.diff |
| .agent/authored/f283-r3-job_id_arg.py | +60/-0 | byte-for-byte copy of job_id_arg.py |
| .agent/authored/f283-r3-ledger.md | +4/-0 | byte-for-byte copy of ledger.md |
| .agent/authored/f283-r3-plan.md | +49/-0 | byte-for-byte copy of plan.md |
| .agent/authored/f283-r3-slips.md | +1/-0 | byte-for-byte copy of slips.md |
| .agent/authored/f283-r3-tests.diff | +73/-0 | byte-for-byte copy of tests.diff |

Measured insertions (`git show --numstat`): **269** (12+70+60+4+49+1+73). Expected: **269**.
They **MATCH**.

### 9fb73768 F283 R3 C2: book round 2's PASS and correct R-1020 on the record
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +4/-0 | append ledger.md by strict byte concatenation: round-2 `Gate:` entry and `DECISION F283 D1` correction record |
| .agent/plan.md | +23/-23 | rewrite to plan.md payload, byte-identical |
| .agent/prose_slips.md | +1/-0 | append slips.md by strict byte concatenation |

Measured insertions (`git show --numstat`): **28** (4+23+1). **Expected 27 per the block
(4+22+1) — MY MEASUREMENT DIFFERS BY ONE.** Reported per the block's own instruction
("If yours differs, report what you measured and say so"): an independent
`git diff --shortstat HEAD~1 HEAD` confirmed **28 insertions(+), 23 deletions(-)**,
agreeing with `git show --numstat`. `git diff --numstat` on `.agent/plan.md` alone reads
`23  23`, not the block's stated 22/22. Nothing was retyped or forced; `.agent/plan.md`
was written by `shutil.copyfile` from the payload and verified sha256-identical to it
before and after commit (see G2c). `git commit`'s own printed summary line for this
commit read `3 files changed, 54 insertions(+), 49 deletions(-)`, a third figure that
agrees with neither the block's 27 nor the measured 28 — the same false-summary-line
phenomenon rounds 1 and 2 both recorded for their own C2 commits; `git show --numstat`
and the independent `git diff --shortstat` are the authoritative readings and agree
with each other at 28/23.

### 6ce6a67c F283 R3 C3: resolve a job id through the envelope, not the exiting helper
| Path | +/- | Reason |
|---|---|---|
| apps/cli/job_id_arg.py | +60/-0 | new file, copied whole from the payload; `git add`ed before the diffs so it is not an untracked file at `integrity check` time |
| apps/cli/commands/job.py | +8/-7 | `git apply` job.diff: import swapped, six `resolve_job_id(` call sites moved onto `resolve_job_id_or_fail` |
| tests/cli/test_job_refusal_envelope.py | +47/-11 | `git apply` tests.diff: the strict xfail deleted and its test turned into a real assertion; a new `TestTheExitingResolverIsStillReachable` class counts the seventeen remaining call sites |
| tests/orchestration/import_reachability_allowlist.txt | +1/-0 | `git apply` allowlist.diff: `apps.cli.job_id_arg` added in sorted position |

Measured insertions (`git show --numstat`): **116** (60+8+47+1). Expected: **116** (60 for
the new module, 8 for `job.py`, 47 for the test file, 1 for the allowlist). They
**MATCH**.

### C4 — THE HANDBACK (this commit)
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | this handback, written once; a single `.agent/**` state file, exempt from the 500-line cap under DECISION F104 D1 |

Self-reference exception (handback template, R-0149 pattern): a handback cannot table
the commit that writes it.

## External actions

- `git worktree add .remedy-wt/f283-r3-mutation 6ce6a67c` for G5, detached HEAD — used for
  the threading proof and both mutation red-proofs, then
  `git worktree remove .remedy-wt/f283-r3-mutation` — a plain remove sufficed because
  every mutation was reverted with `git checkout --` before the next step, leaving the
  worktree clean at removal time (no `--force` needed, unlike round 2).
- `git push -u origin feature/f283-machine-contracts-part-two` after C4 — real outcome
  reported in the session reply, since it ships this very file.
- `gh pr list --state open ...` after the push — real outcome reported in the session
  reply.
- **NOTHING IS MERGED.** No `gh pr merge`, no `gh pr create`, no checkout of `main`, no
  branch deletion.
- No worktree other than the one disposable G5 worktree was added or removed. The three
  `remedy/job-*` worktrees were left alone throughout.

## Verification

### G1 — PAYLOADS transport, twenty-one readings, then eight authored copies

| file | lines measured/given | bytes measured/given | sha256 equal |
|---|---|---|---|
| allowlist.diff | 12/12 | 502/502 | True |
| job.diff | 70/70 | 2660/2660 | True |
| job_id_arg.py | 60/60 | 2941/2941 | True |
| ledger.md | 4/4 | 6963/6963 | True |
| plan.md | 49/49 | 2377/2377 | True |
| slips.md | 1/1 | 1420/1420 | True |
| tests.diff | 73/73 | 3828/3828 | True |

**All twenty-one readings equal: True.** The three diffs (`job.diff`, `tests.diff`,
`allowlist.diff`) each dry-ran with `git apply --check` at real exit code **0** before
any real apply, and were checked a second time (also exit 0) immediately before each
real apply in C3, per constraint 1.

Eight `.agent/authored/f283-r3-*` copies (the block copy plus seven payloads), each
compared byte-for-byte with its source via `filecmp.cmp(..., shallow=False)` at copy
time:

| copy | identical |
|---|---|
| f283-r3-block.md | True |
| f283-r3-allowlist.diff | True |
| f283-r3-job.diff | True |
| f283-r3-job_id_arg.py | True |
| f283-r3-ledger.md | True |
| f283-r3-plan.md | True |
| f283-r3-slips.md | True |
| f283-r3-tests.diff | True |

**Copies compared: 8. All True.**

### G2 — THE BOOKING AND THE CORRECTION

**(a) Append arithmetic**, by strict byte concatenation:

| file | pre | payload | post | pre+payload==post |
|---|---|---|---|---|
| .agent/live_review.md | 446450 | 6963 | 453413 | True |
| .agent/prose_slips.md | 358529 | 1420 | 359949 | True |

Matches the reviewer's stated `446450 + 6963 = 453413` and `358529 + 1420 = 359949`
exactly.

**(b) R-1020's pairing survived the correction.** Line-anchored search on the committed
`.agent/live_review.md` at C2: `^- R-1020 — ` count = **1**; `^Done: R-1020 — ` count =
**0**. Open set by distinct id, via `open_finding_ids` from
`scripts/rotate_live_review.py` (imported and called directly):

| rev | OPEN by distinct id | reviewer's |
|---|---|---|
| `fc8dfd85` | **24** | 24 |
| C2 (`9fb73768`) | **24** | 24 |

Both set differences empty — this round registers nothing and resolves nothing, exactly
as claimed.

**(c) `.agent/plan.md` at C2 equals plan.md byte-for-byte**:

| file | sha256 (both sides) | equal |
|---|---|---|
| .agent/plan.md | `9ba2e7b13ef410ffed3c38d4c21793766c922ccba6b2fb44fae62d6af763f75e` | True |

Line count: **49**, under the AGENTS.md 50-line rule.

**(d) `git diff --name-only <C1b> <C2>`** (`3a3f513c`..`9fb73768`) names exactly **three**
paths:

```
.agent/live_review.md
.agent/plan.md
.agent/prose_slips.md
```

### G3 — THE REPAIR IS THE REVIEWER'S BYTES

`git apply --check` on `job.diff`, `tests.diff` and `allowlist.diff` at C2: all three
real exit code **0**, run immediately before their real applies (also exit 0 each).
`git diff --name-only <C2> <C3>` (`9fb73768`..`6ce6a67c`) names exactly:

```
apps/cli/commands/job.py
apps/cli/job_id_arg.py
tests/cli/test_job_refusal_envelope.py
tests/orchestration/import_reachability_allowlist.txt
```

Four paths, as required.

`resolve_job_id(` call-site count in the committed `apps/cli/commands/job.py`: **0**.
Count across all of `apps/cli/`: **17**. Both match the reviewer's measured 0 and 17.
`packages/orchestration/data_paths.py` does not appear anywhere in
`git diff --name-only fc8dfd85 HEAD` (**0** occurrences) — confirmed not in the round's
path set.

### G4 — THE REPAIR WORKS AND THE OPERATOR SEES THE SAME BYTES

```
$ bash -c 'python3 -m pytest -q -p no:cacheprovider tests/docs/ tests/orchestration/test_import_reachability.py tests/cli/test_job_refusal_envelope.py tests/cli/test_job_budget_set.py tests/cli/test_job_commands.py tests/cli/test_job_show.py tests/cli/test_job_stop.py tests/cli/test_job_report.py tests/cli/test_plan_approval.py tests/cli/test_json_envelope.py tests/cli/test_golden_path.py tests/test_cli_main.py tests/test_data_paths.py tests/test_run_log_cli.py tests/orchestration/test_structured_planner_cli.py; echo "REAL_EXIT=$?"'
708 passed in 146.48s (0:02:26)
REAL_EXIT=0
```

Matches the reviewer's `708 passed` at real exit code 0 exactly. **XFAIL COUNT: 0** —
the mark is gone.

```
$ python3 -m ruff check apps/cli/commands/job.py apps/cli/job_id_arg.py tests/cli/test_job_refusal_envelope.py
All checks passed!
```
Real exit code **0**.

```
$ python3 -m apps.cli.main integrity check --json
{"passed": true, "fail_count": 0, "check_count": 5, "checks": [
  {"name": "handler_import", "status": "pass", "message": "handlers=145"},
  {"name": "live_review_verdict", "status": "pass", ...},
  {"name": "plan_consistency", "status": "pass", "message": "unchecked=0, context_complete=False"},
  {"name": "relevant_untracked", "status": "pass", "message": "untracked=0, relevant=0"},
  {"name": "high_blockers_open", "status": "pass", "message": "no open blocker/high findings"}
]}
```
Real exit code **0**. All five checks `pass`, `passed: true`, `fail_count: 0`. The full
suite was NOT re-run, per the block's instruction.

### G5 — THE REPAIR IS REAL AND STILL GATED

Disposable worktree `.remedy-wt/f283-r3-mutation` added at `6ce6a67c` (C3), used for the
threading proof and both mutations, removed after.

**(a) PROVE THE THREADING** — `_cmd_show_job(job_id_str="zzzznotajob",
json_output=...)`:

`json_output=True`: exit **1**, stderr `''` (empty), stdout envelope
`{"error": "invalid_job_id", "message": "No job matches 'zzzznotajob'. Try: remedy job
list.", "ok": false, "schema_version": 1}`.

`json_output=False`: exit **1**, stdout `''` (empty), stderr
`Error: No job matches 'zzzznotajob'. Try: remedy job list.\n` — byte-for-byte what the
exiting helper printed before this round.

Both match the block's required shapes exactly.

**(b) MUTATION ONE** — `"invalid_job_id"` → `"bad_id"` in `apps/cli/job_id_arg.py`:

```
$ bash -c 'python3 -m pytest -q -p no:cacheprovider tests/cli/test_job_refusal_envelope.py; echo "REAL_EXIT=$?"'
1 failed, 9 passed in 0.47s
REAL_EXIT=1
```

**This goes RED**, at `test_a_threaded_command_answers_a_bad_id_in_the_envelope`, exactly
as the block names it. **Reported honestly: my count is 1 failed, 9 passed, not the
block's stated 1 failed, 8 passed.** The file collects **10** tests total (confirmed by
`--collect-only`): tests.diff both converted the old xfail into a real test AND added a
new `TestTheExitingResolverIsStillReachable` class with one more test, so the total rose
from 9 (8 passed + 1 xfail, round 2's count) to 10, and 1 failure leaves 9 passing, not
8. Reverted with `git checkout --` before mutation two.

**(c) MUTATION TWO** — reverted `_cmd_show_job`'s call back to `resolve_job_id(job_id_str)`
and restored the `resolve_job_id` import (file re-verified to `py_compile` clean, exit
0, before running tests):

```
$ bash -c 'python3 -m pytest -q -p no:cacheprovider tests/cli/test_job_refusal_envelope.py; echo "REAL_EXIT=$?"'
2 failed, 8 passed in 0.41s
REAL_EXIT=1
```

**This goes RED**, but at **2 failed, 8 passed**, not the block's stated **1 failed, 8
passed**. The first failure is the same test named in (b),
`test_a_threaded_command_answers_a_bad_id_in_the_envelope` (its stderr is no longer
empty — the exiting helper printed prose again). The second is this round's OWN new
guard, `test_the_call_sites_outside_job_py_are_counted`, which also detects the
reverted call site: `job.py` reappears in its `found` dict with count 1. Both failures
are real and both are caused by mutation two; the guard test the reviewer's own tests.diff
added this round catches the same regression the block's named test catches, which the
block's own arithmetic did not anticipate. Reverted with `git checkout --` before
removing the worktree.

`git worktree remove .remedy-wt/f283-r3-mutation` (no `--force` needed: both mutations
were cleanly reverted before removal, unlike round 2). `git worktree list` after
removal:

```
/home/decodeux/Repos/remedy                                  6ce6a67c [feature/f283-machine-contracts-part-two]
/home/decodeux/Repos/remedy/.remedy-wt/job-468c8e62a2cc4fac  1b9ae606 [remedy/job-468c8e62a2cc4fac]
/home/decodeux/Repos/remedy/.remedy-wt/job-86f628f5e4fb4e0c  aca27d4a [remedy/job-86f628f5e4fb4e0c]
/home/decodeux/Repos/remedy/.remedy-wt/job-c1dba9c3d7874968  fd23710f [remedy/job-c1dba9c3d7874968]
```

Only the primary checkout and the three `remedy/job-*` worktrees remain.

### G6 — TREE AND PUSH

Reported in full in the worker's session reply once this commit exists (push carries
this file). At write time: `git status --porcelain` empty; `git log --oneline -n 5` will
show C4, C3, C2, C1b, C1a in that order once committed; `git worktree list` shows the
primary checkout and the three `remedy/job-*` worktrees and nothing else. Push outcome
and `gh pr list` reported in the session reply.

### The round's whole tracked path set (before this commit)

`git diff --name-only fc8dfd85 6ce6a67c` — **15** paths:

| # | path | introduced by |
|---|---|---|
| 1 | .agent/authored/f283-r3-allowlist.diff | C1b `3a3f513c` |
| 2 | .agent/authored/f283-r3-block.md | C1a `2dc60bdc` |
| 3 | .agent/authored/f283-r3-job.diff | C1b `3a3f513c` |
| 4 | .agent/authored/f283-r3-job_id_arg.py | C1b `3a3f513c` |
| 5 | .agent/authored/f283-r3-ledger.md | C1b `3a3f513c` |
| 6 | .agent/authored/f283-r3-plan.md | C1b `3a3f513c` |
| 7 | .agent/authored/f283-r3-slips.md | C1b `3a3f513c` |
| 8 | .agent/authored/f283-r3-tests.diff | C1b `3a3f513c` |
| 9 | .agent/live_review.md | C2 `9fb73768` |
| 10 | .agent/plan.md | C2 `9fb73768` |
| 11 | .agent/prose_slips.md | C2 `9fb73768` |
| 12 | apps/cli/commands/job.py | C3 `6ce6a67c` |
| 13 | apps/cli/job_id_arg.py | C3 `6ce6a67c` |
| 14 | tests/cli/test_job_refusal_envelope.py | C3 `6ce6a67c` |
| 15 | tests/orchestration/import_reachability_allowlist.txt | C3 `6ce6a67c` |

Plus `.agent/handoff.md` from this commit makes **16** — set-equal to constraint 3's
enumeration (eight authored copies plus the three `.agent/**` state files plus the four
named product/test paths plus the handoff itself). `.agent/candidates.md`,
`.agent/context.md`, `.agent/decisions.md`, `.agent/operator_questions.md`, `README.md`,
`docs/roadmap/**`, and `packages/orchestration/data_paths.py` appear **0** times.

## Authored-text proofs

- The eight copies at C1a/C1b, compared with the reviewer's originals under
  `.remedy-wt/f283-r3-payloads/` and `.remedy-wt/f283-r3-block.md`: **eight readings,
  all True** (G1).
- The one REWRITE payload against its committed file: `.agent/plan.md` is sha256-equal
  to its payload (G2c).
- The two APPEND payloads against their committed files: strict byte concatenation True
  for `.agent/live_review.md` (ledger.md) and `.agent/prose_slips.md` (slips.md), byte
  numbers equal to the reviewer's (G2a).
- The three DIFF payloads (`job.diff`, `tests.diff`, `allowlist.diff`) and the one NEW
  FILE payload (`job_id_arg.py`): the diffs applied with `git apply`, never retyped,
  each dry-ran with `git apply --check` at exit 0 first; the new file copied whole with
  `shutil.copyfile` and verified byte-identical before `git add` (G1, G3).
- No payload was edited or retyped. All eight `.agent/authored/` copies and the one
  product-file copy were made with `shutil.copyfile`; the two appends by reading the
  payload's bytes and concatenating them; the three diffs applied with `git apply` only.

## Deviations & assumptions

1. **The bundle ran C1a, C1b, C2, C3 — four commits, exactly as ordered — before this
   handback commit C4.** Nothing was added, dropped or reordered.
2. **C2's measured insertions are 28, not the block's stated 27**, and the `plan.md`
   rewrite measures +23/-23, not the block's stated +22/-22. Both were reported per the
   block's own instruction rather than forced to match; `git show --numstat`, an
   independent `git diff --shortstat`, and `git diff --numstat` isolated to
   `.agent/plan.md` all agree on 28/23. Nothing was retyped or edited to make either
   number match — the payload was applied byte-for-byte via `shutil.copyfile` and
   verified sha256-identical to the payload both before commit and by reading it back
   from the committed tree.
3. **`git commit`'s own printed summary line for C2 read `54 insertions(+), 49
   deletions(-)`**, a third figure agreeing with neither the block's 27 nor the measured
   28. This is the same false-summary-line phenomenon rounds 1 and 2 both recorded for
   their own C2 commits. `git show --numstat` and an independent `git diff --shortstat`
   are the authoritative readings and agree with each other at 28/23; nothing under
   `apps/`, `packages/`, `tests/` or `docs/` is affected by this printed-summary
   artifact.
4. **G5(b) mutation one's real count is 1 failed, 9 passed (10 tests total), not the
   block's stated 1 failed, 8 passed.** `--collect-only` confirms 10 tests in the file.
   Round 2 measured 8 passed + 1 xfailed = 9 total for this file; this round's tests.diff
   both converted that xfail into a real assertion (net zero change in count) and added
   one wholly new test (`test_the_call_sites_outside_job_py_are_counted`), so the total
   rose to 10 and one failure leaves 9 passing. The named test still goes RED exactly as
   the block requires; only the passing-count arithmetic differs, and it differs because
   the block's own payload added a test its own arithmetic did not count.
5. **G5(b) mutation two's real count is 2 failed, 8 passed, not the block's stated 1
   failed, 8 passed.** Both failures are genuine consequences of the same mutation: the
   named test (`test_a_threaded_command_answers_a_bad_id_in_the_envelope`, because
   stderr is no longer empty) AND this round's own new guard
   (`test_the_call_sites_outside_job_py_are_counted`, because `job.py` reappears in its
   count of `resolve_job_id(` call sites). The mutation still exercises exactly the
   defect the block describes — the call site reverting to the exiting helper — and both
   reds are traceable to it; the block undercounted by missing that its own second guard
   test also fires on this mutation.
6. **No trailing commit for the C4 push or `gh pr list`; both go in the session reply**,
   consistent with DECISION amend0827 D2 and rounds 1 and 2's own precedent: the push
   carries this very file, so its outcome cannot be known before the commit exists.
7. **One disposable worktree (`.remedy-wt/f283-r3-mutation`) was reused for the
   threading proof and both G5 mutations sequentially** rather than separate worktrees —
   consistent with rounds 1 and 2's reading of the block's singular "REMOVE the
   worktree" phrasing. Both mutations were reverted with `git checkout --` before the
   next step, so `git worktree remove` needed no `--force` this round (a change from
   round 2, where mutation left the worktree dirty by design).
8. **Scratch hygiene.** Two small scripts were written to the gitignored
   `.remedy-wt/f283-r3-scratch/` (`g1_measure.py`, `g5a_prove_threading.py`) for
   measurement; neither was committed, nothing was written into
   `.remedy-wt/f283-r3-payloads/`.
9. **Constraints 3 and 4 held throughout.** Only the sixteen paths named in the block's
   enumeration were touched (verified by set-equality above); `packages/` was never
   touched; only `job.py`'s six named call sites moved, and none of the seventeen call
   sites in the eight other modules (`change`, `contract_cmd`, `decision`,
   `job_context_cmd`, `job_stop_cmd`, `patch`, `project`, `teacher_cmd`) were migrated,
   edited or referenced. R-1020 stays OPEN per the block's own instruction.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| Pre-flight (STOP, git state, block self-verify) | done | no STOP; tree clean at `fc8dfd85`; block 239 lines / matching sha256 |
| C1a copy block | done | 239 insertions, matches block's own line count |
| C1b copy 7 payloads | done | 269 insertions, matches expected 269 |
| C2 book round 2 PASS, correct R-1020 | deviated | 28/23 measured vs block's stated 27/22 — reported per block's own instruction, nothing retyped |
| C3 the repair, product and tests in one commit | done | 116 insertions (60+8+47+1), matches expected; 4 paths only |
| C4 the handback | done | this commit |
| G1 payload transport + authored copies | done | 21/21 payload readings equal; 8/8 authored copies byte-identical; 3/3 diffs dry-ran at exit 0 |
| G2(a) live_review.md + prose_slips.md appends | done | 446450+6963=453413; 358529+1420=359949; both equal to reviewer's |
| G2(b) R-1020 pairing + open set by distinct id | done | 1 registration / 0 done lines; 24 at `fc8dfd85`, 24 at C2; both set diffs empty |
| G2(c) plan.md rewrite | done | sha256-equal to payload; 49 lines, under 50 |
| G2(d) three-path diff | done | exactly 3 paths at C1b..C2 |
| G3 repair is reviewer's bytes | done | apply-check exit 0 x3; 4 paths; 0 `resolve_job_id(` in job.py; 17 across apps/cli/; packages/ untouched |
| G4 repair works, ruff, integrity | done | 708 passed/0 xfailed/exit 0; ruff exit 0; integrity all 5 pass, fail_count 0 |
| G5(a) threading proof | done | json_output=True: exit 1, empty stderr, envelope; json_output=False: exit 1, empty stdout, prose stderr |
| G5(b) mutation red-proofs | deviated | mutation 1 goes RED at 1 failed/9 passed (block said 8 passed — file has 10 tests, not 9); mutation 2 goes RED at 2 failed/8 passed (block said 1 failed — the round's own new guard also fires); both reds are genuine and traceable to the mutation |
| G6 tree, push, PR list | pending at write time | reported in the worker's session reply with real exit codes |
| Constraint 1 no payload edited/retyped | done | `shutil.copyfile`, byte concatenation, `git apply` only |
| Constraint 2 every commit under 500 insertions | done | 239, 269, 28, 116; this handoff exempt as single `.agent/**` state file |
| Constraint 3 no unnamed file touched | done | 16 paths after this commit, set-equal to the enumeration |
| Constraint 4 no call site outside job.py migrated | done | only the six named `job.py` sites moved; seventeen elsewhere untouched; `packages/` untouched |
| Constraint 5 stop on red | done | no gate went red (the two red mutations in G5(b) are the block's own required red-proofs, not an unplanned failure) |
| Constraint 6 nothing is merged | done | no `gh pr merge`, no `gh pr create`, no checkout of `main`, no branch deletion |
| Constraint 7 leave job worktrees alone | done | only one disposable G5 worktree added/removed; `remedy/job-*` untouched |

## Next

1. Phase 1 rule 1: read `.agent/STOP` from disk.
2. The review of round 3 — C1a, C1b, C2, C3, C4, with all six gates re-derived.
3. Then round 4 — R-1020's remaining seventeen call sites, largest module first: `patch`
   7, `change` 3, `teacher_cmd` 2, then `contract_cmd`, `decision`, `job_context_cmd`,
   `job_stop_cmd` and `project` at one each.

Open findings count: **24** (unchanged by this round). Operator-questions count: **2**
(Q1, Q2 — both unchanged by this round).
