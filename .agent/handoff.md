# Handoff — F283 Machine contracts, part two: refusal sweep, JSON gap, exit-code taxonomy · Round 1 · CLAIM + SLICE A

## Session

SESSION 1 of feature F283 · round 1 · rounds so far 1

This round claimed F283 from `main` at `d0d40e89`, booked F277 round 19's PASS, resolved
R-1018, emptied `.agent/candidates.md`, re-headed the live review record, and landed T001's
first product slice: the twenty already-flagged `sys.exit` refusal sites in
`apps/cli/commands/job.py` migrated onto the shared `fail()` helper, with its new pinning
test. Context self-assessment: roughly two-thirds of the working budget remained at the
point this handoff was written — no compression was needed.

## Range

Review of `d0d40e89`..`HEAD`.

## Commits

### 40f0edcc F283 R1 C1a: copy round 1 block into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f283-r1-block.md | +282/-0 | byte-for-byte copy of this round's step block |

Measured insertions (`git show --numstat`): **282**. Expected: the block's own measured
line count, 282. They **MATCH**. Well under the 500-line cap.

### bb42e30c F283 R1 C1b: copy round 1 bookkeeping payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f283-r1-candidates.diff | +40/-0 | byte-for-byte copy of candidates.diff |
| .agent/authored/f283-r1-context.md | +64/-0 | byte-for-byte copy of context.md |
| .agent/authored/f283-r1-ledger.md | +4/-0 | byte-for-byte copy of ledger.md |
| .agent/authored/f283-r1-plan.md | +49/-0 | byte-for-byte copy of plan.md |
| .agent/authored/f283-r1-rehead.diff | +61/-0 | byte-for-byte copy of rehead.diff |
| .agent/authored/f283-r1-slips.md | +1/-0 | byte-for-byte copy of slips.md |
| .agent/authored/f283-r1-status.diff | +11/-0 | byte-for-byte copy of status.diff |

Measured insertions (`git show --numstat`): **230**. Expected: **230**
(40+64+4+49+61+1+11). They **MATCH**.

### 9e6d74aa F283 R1 C1c: copy round 1 product payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f283-r1-job.diff | +274/-0 | byte-for-byte copy of job.diff |
| .agent/authored/f283-r1-test_job_refusal_envelope.py | +186/-0 | byte-for-byte copy of the new test file |

Measured insertions: **460**. Expected: **460** (274+186). They **MATCH**.

### 17be08e7 F283 R1 C2: claim F283, book round 19's PASS and resolve R-1018
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +34/-22 | `git apply` rehead.diff (+30/-22), then append ledger.md's round-19 `Gate:` entry and `Done: R-1018` resolution (+4 more, cumulative +34/-22) |
| docs/roadmap/STATUS.md | +1/-1 | `git apply` status.diff: F283's line flips to `[~]` |
| .agent/candidates.md | +1/-33 | `git apply` candidates.diff: all three prior entries retired, replaced with the single EMPTY line |
| .agent/plan.md | +36/-32 | rewrite to plan.md payload, byte-identical |
| .agent/context.md | +36/-21 | rewrite to context.md payload, byte-identical |
| .agent/prose_slips.md | +1/-0 | append slips.md by strict byte concatenation |

Measured insertions (`git show --numstat`): **109** (1+36+34+36+1+1). Expected: **109**.
They **MATCH**. Deletions also total 109 (33+21+22+32+0+1), matching insertions exactly —
confirmed with `git diff --shortstat` independently of `git commit`'s own summary line,
which is discussed under Deviations.

### 3f754a9c F283 R1 C3: migrate job's twenty flagged refusals onto the shared fail
| Path | +/- | Reason |
|---|---|---|
| apps/cli/commands/job.py | +76/-64 | `git apply` job.diff: the twenty `print(...); sys.exit(...)` pairs whose handler already carries `json_output` migrated onto `fail()`; `_plan_rejected_error` split into itself plus `_plan_rejected_message` |
| tests/cli/test_job_refusal_envelope.py | +186/-0 | new file, copied whole from the payload; pins the migration and guards against a reverted site |

Measured insertions: **262** (76+186). Expected: **262**. They **MATCH**.

### C4 — THE HANDBACK (this commit)
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | this handback, written once; a single `.agent/**` state file, exempt from the 500-line cap under DECISION F104 D1 |

Self-reference exception (handback template, R-0149 pattern): a handback cannot table the
commit that writes it. No trailing bookkeeping commit follows C4 — push and read-only `gh`
queries come next, never another commit.

## External actions

- `git checkout -b feature/f283-machine-contracts-part-two` from `main` at `d0d40e89` —
  branch created.
- `git worktree add .remedy-wt/f283-r1-mutation-a 3f754a9c` for G5's two mutation
  red-proofs, then `git worktree remove --force .remedy-wt/f283-r1-mutation-a` — force was
  required because the second mutation (the restored `print`/`sys.exit` pair) left the
  worktree with an uncommitted, deliberately-never-committed edit; the primary checkout was
  never touched by either mutation.
- `git push -u origin feature/f283-machine-contracts-part-two` after C4 — real outcome
  reported in the worker's session reply, since it ships this very file and cannot be known
  before it exists.
- `gh pr list --state open ...` and `gh run list --branch
  feature/f283-machine-contracts-part-two ...` after the push — real outcomes reported in
  the session reply.
- **NOTHING IS MERGED.** No `gh pr merge`, no `gh pr create` (the block explicitly forbids
  opening a PR at claim time), no checkout of `main`, no branch deletion.
- No worktree other than the one disposable one above was added or removed. The three
  `remedy/job-*` worktrees were left alone throughout.

## Verification

### Pre-flight

- `ls .agent/STOP`: `No such file or directory`. There is no STOP on disk.
- `git status --porcelain`: empty.
- `git branch --show-current`: `main`.
- `git log --oneline -1`: `d0d40e89`, the commit the delegation message named.
- Block self-verification (R-0954), `.remedy-wt/f283-r1-block.md`:

| reading | measured | given | equal |
|---|---|---|---|
| line count | 282 | 282 | True |
| sha256 | `46144bc3f0f046f38181f8eabdd303a12b09f4650821e06589c2f14e2c3091fa` | `46144bc3f0f046f38181f8eabdd303a12b09f4650821e06589c2f14e2c3091fa` | True |

Neither reading differs, so the round went ahead. `git checkout -b
feature/f283-machine-contracts-part-two` then created the branch (no `git pull`, per the
block's explicit instruction that `main` was already at the merge commit).

### G1 — PAYLOADS transport, twenty-seven readings, then ten authored copies

| file | lines measured/given | bytes measured/given | sha256 equal |
|---|---|---|---|
| candidates.diff | 40/40 | 2721/2721 | True |
| context.md | 64/64 | 3524/3524 | True |
| job.diff | 274/274 | 10716/10716 | True |
| ledger.md | 4/4 | 5446/5446 | True |
| plan.md | 49/49 | 2536/2536 | True |
| rehead.diff | 61/61 | 6758/6758 | True |
| slips.md | 1/1 | 1160/1160 | True |
| status.diff | 11/11 | 1933/1933 | True |
| test_job_refusal_envelope.py | 186/186 | 6879/6879 | True |

**All twenty-seven readings equal: True.** The four diffs (`rehead.diff`, `status.diff`,
`candidates.diff`, `job.diff`) each dry-ran with `git apply --check` at real exit code **0**
before any real apply — `job.diff` was checked twice: once before C1c's copy, once again
immediately before C3's real apply, both exit 0.

Ten `.agent/authored/f283-r1-*` copies (the block copy plus nine payloads), each compared
byte-for-byte with its source via `filecmp.cmp(..., shallow=False)` at copy time:

| copy | identical |
|---|---|
| f283-r1-block.md | True |
| f283-r1-rehead.diff | True |
| f283-r1-ledger.md | True |
| f283-r1-status.diff | True |
| f283-r1-candidates.diff | True |
| f283-r1-plan.md | True |
| f283-r1-context.md | True |
| f283-r1-slips.md | True |
| f283-r1-job.diff | True |
| f283-r1-test_job_refusal_envelope.py | True |

**Copies compared: 10. All True.**

### G2 — THE CLAIM'S BOOKKEEPING

**(a) `.agent/live_review.md` append by strict byte concatenation**, base = file AFTER the
re-head and BEFORE the ledger append:

| stage | bytes |
|---|---|
| pre (post-rehead, pre-append) | 433255 |
| payload (ledger.md) | 5446 |
| post (measured) | 438701 |
| pre + payload == post | True |

Matches the reviewer's `433255 + 5446 = 438701` exactly. (Pre-rehead byte count, for
completeness: 432408, also equal to the reviewer's stated pre-rehead figure.)

**(b) `.agent/prose_slips.md` append**, same method:

| stage | bytes |
|---|---|
| pre | 357369 |
| payload (slips.md) | 1160 |
| post (measured) | 358529 |
| pre + payload == post | True |

Matches the reviewer's `357369 + 1160 = 358529` exactly.

**(c) Open set by distinct id**, via `open_finding_ids` from `scripts/rotate_live_review.py`
(imported and called directly):

| rev | OPEN by distinct id | reviewer's |
|---|---|---|
| `d0d40e89` | **24** | 24 |
| C2 (`17be08e7`) | **23** | 23 |

Set difference: removed `{R-1018}`, added `{}` (empty) — exactly the block's claim.

**(d) `.agent/plan.md` and `.agent/context.md` at C2** equal their payloads byte-for-byte:

| file | sha256 (both sides) | equal |
|---|---|---|
| .agent/plan.md | `2eec9950e3ffe44c769283a155373eea929f50f622a276420f1bd3ee0ff7df61` | True |
| .agent/context.md | `aaefe21dbad44ce009124e1155f766aa067e9ce86a878997baf5a267f7aa441e` | True |

`.agent/plan.md` line count: **49**, under the AGENTS.md 50-line rule.

**(e) STATUS line and candidates.md**, read back in full:

- STATUS: `- [~] F283 — Machine contracts, part two: the refusal sweep, the JSON gap and the exit-code taxonomy` — matches the required `- [~] F283 — ` prefix.
- `.agent/candidates.md` full body carries its standing header and the single line:
  `EMPTY — every entry was registered as a finding and the register is the record.` —
  matches exactly.

**(f) `git diff --name-only <C1c> <C2>`** (`9e6d74aa`..`17be08e7`) names exactly **six**
paths:

```
.agent/candidates.md
.agent/context.md
.agent/live_review.md
.agent/plan.md
.agent/prose_slips.md
docs/roadmap/STATUS.md
```

### G3 — THE SLICE IS THE REVIEWER'S BYTES

`git apply --check .remedy-wt/f283-r1-payloads/job.diff` at C2: real exit code **0**, run
immediately before the real apply (also exit 0). `git diff --name-only <C2> <C3>`
(`17be08e7`..`3f754a9c`) names exactly:

```
apps/cli/commands/job.py
tests/cli/test_job_refusal_envelope.py
```

Two paths, as required. `fail(` call-site count in the committed `apps/cli/commands/job.py`
tree: a line-scan for `fail(` not preceded by a word character (excluding the local `_fail`
helper at lines 916–949 and its five call sites, and excluding two docstring/prose mentions
at lines 40 and 42) yields **20** real call sites, at lines 179, 1141, 1187, 1192, 1198,
1210, 1220, 1409, 1416, 1445, 1447, 1453, 1534, 1539, 1545, 1579, 1590, 1920, 2177, 2218.
The reviewer's table above also lists **20** rows. Both are **20**.

### G4 — THE SLICE WORKS AND THE OPERATOR SEES THE SAME BYTES

```
$ bash -c 'python3 -m pytest -q -p no:cacheprovider tests/docs/ tests/orchestration/test_roadmap_index.py tests/cli/test_job_refusal_envelope.py tests/cli/test_job_budget_set.py tests/cli/test_job_commands.py tests/cli/test_job_show.py tests/cli/test_job_stop.py tests/cli/test_job_report.py tests/cli/test_plan_approval.py tests/cli/test_json_envelope.py tests/cli/test_golden_path.py tests/test_data_paths.py; echo "REAL_EXIT=$?"'
611 passed in 145.16s (0:02:25)
REAL_EXIT=0
```

Matches the reviewer's `611 passed` at real exit code 0 exactly.

```
$ python3 -m ruff check apps/cli/commands/job.py tests/cli/test_job_refusal_envelope.py
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
Real exit code **0**. All five checks `pass`, `passed: true`, `fail_count: 0`, matching the
reviewer's reading. The full suite was NOT re-run — amend0917 rule 1 gives a feature exactly
one full-suite run and F283 has not spent it yet (belongs to its closure).

### G5 — THE NEW TEST GATES THE PRODUCT

Disposable worktree `.remedy-wt/f283-r1-mutation-a` added at `3f754a9c` (C3), used for both
mutations sequentially, removed after both.

**(a) Rename one token** (`fail("invalid_list_option"` → `fail("list_error"` at line 179):

```
$ bash -c 'python3 -m pytest -q -p no:cacheprovider tests/cli/test_job_refusal_envelope.py; echo "REAL_EXIT=$?"'
...F....
FAILED tests/cli/test_job_refusal_envelope.py::TestARefusalIsAnEnvelopeUnderJson::test_an_unknown_sort_field_names_the_condition
AssertionError: assert 'list_error' == 'invalid_list_option'
1 failed, 7 passed in 0.39s
REAL_EXIT=1
```

Matches the reviewer's `1 failed, 7 passed` at exit 1, on
`TestARefusalIsAnEnvelopeUnderJson::test_an_unknown_sort_field_names_the_condition`, exactly.

The mutation was then reverted (`git checkout -- apps/cli/commands/job.py` in the disposable
worktree) before mutation (b).

**(b) Restore one site** (`checkpoint_not_found` at lines 1578–1583 put back to
`print(f"Error: checkpoint not found: {checkpoint_id}", file=sys.stderr); sys.exit(1)`):

```
$ bash -c 'python3 -m pytest -q -p no:cacheprovider tests/cli/test_job_refusal_envelope.py; echo "REAL_EXIT=$?"'
F.......
FAILED tests/cli/test_job_refusal_envelope.py::TestTheFlaggedRefusalsAreAllMigrated::test_no_flagged_print_then_exit_pair_survives
AssertionError: these job.py refusals have `json_output` in scope and still print prose: lines [1580]
1 failed, 7 passed in 0.32s
REAL_EXIT=1
```

Matches the reviewer's `1 failed, 7 passed` at exit 1, on
`TestTheFlaggedRefusalsAreAllMigrated::test_no_flagged_print_then_exit_pair_survives`,
exactly.

`git worktree remove --force .remedy-wt/f283-r1-mutation-a` (force needed: the second
mutation left the worktree dirty by design, never committed). `git worktree list` after
removal:

```
/home/decodeux/Repos/remedy                                  3f754a9c [feature/f283-machine-contracts-part-two]
/home/decodeux/Repos/remedy/.remedy-wt/job-468c8e62a2cc4fac  1b9ae606 [remedy/job-468c8e62a2cc4fac]
/home/decodeux/Repos/remedy/.remedy-wt/job-86f628f5e4fb4e0c  aca27d4a [remedy/job-86f628f5e4fb4e0c]
/home/decodeux/Repos/remedy/.remedy-wt/job-c1dba9c3d7874968  fd23710f [remedy/job-c1dba9c3d7874968]
```

Only the primary checkout and the three `remedy/job-*` worktrees remain.

### G6 — TREE AND PUSH

Reported in full in the worker's session reply once this commit exists (push carries this
file, per DECISION amend0827 D2 — no trailing commit may add these readings after the fact).
Expected at that point: `git status --porcelain` empty; `git log --oneline -n 6` showing C4,
C3, C2, C1c, C1b, C1a in that order; `git worktree list` showing the primary checkout and
the three `remedy/job-*` worktrees and nothing else; the push's real outcome; `gh pr list`
empty (no PR opens at claim time); and the `gh run list` run id/status for this branch.

### The round's whole tracked path set (before this commit)

`git diff --name-only d0d40e89 3f754a9c` — **18** paths:

| # | path | introduced by |
|---|---|---|
| 1 | .agent/authored/f283-r1-block.md | C1a `40f0edcc` |
| 2 | .agent/authored/f283-r1-candidates.diff | C1b `bb42e30c` |
| 3 | .agent/authored/f283-r1-context.md | C1b `bb42e30c` |
| 4 | .agent/authored/f283-r1-ledger.md | C1b `bb42e30c` |
| 5 | .agent/authored/f283-r1-plan.md | C1b `bb42e30c` |
| 6 | .agent/authored/f283-r1-rehead.diff | C1b `bb42e30c` |
| 7 | .agent/authored/f283-r1-slips.md | C1b `bb42e30c` |
| 8 | .agent/authored/f283-r1-status.diff | C1b `bb42e30c` |
| 9 | .agent/authored/f283-r1-job.diff | C1c `9e6d74aa` |
| 10 | .agent/authored/f283-r1-test_job_refusal_envelope.py | C1c `9e6d74aa` |
| 11 | .agent/candidates.md | C2 `17be08e7` |
| 12 | .agent/context.md | C2 `17be08e7` |
| 13 | .agent/live_review.md | C2 `17be08e7` |
| 14 | .agent/plan.md | C2 `17be08e7` |
| 15 | .agent/prose_slips.md | C2 `17be08e7` |
| 16 | docs/roadmap/STATUS.md | C2 `17be08e7` |
| 17 | apps/cli/commands/job.py | C3 `3f754a9c` |
| 18 | tests/cli/test_job_refusal_envelope.py | C3 `3f754a9c` |

Plus `.agent/handoff.md` from this commit makes **19** — set-equal to constraint 3's
enumeration (ten authored copies plus nine named files). `.agent/decisions.md`,
`.agent/operator_questions.md`, `README.md`, any `docs/roadmap/features/*.md`, and any
module other than `job.py` appear **0** times.

## Authored-text proofs

- The ten copies at C1a/C1b/C1c, compared with the reviewer's originals under
  `.remedy-wt/f283-r1-payloads/` and `.remedy-wt/f283-r1-block.md`: **ten readings, all
  True** (G1).
- The two REWRITE payloads against their committed files: `.agent/plan.md` and
  `.agent/context.md` are sha256-equal to their payloads (G2d).
- The two APPEND payloads against their committed files: strict byte concatenation True for
  both `.agent/live_review.md` (ledger.md) and `.agent/prose_slips.md` (slips.md), all byte
  numbers equal to the reviewer's (G2a, G2b).
- The four DIFF payloads: each applied with `git apply`, never retyped; each dry-ran with
  `git apply --check` at exit 0 first (G1, G3).
- No payload was edited or retyped. All ten copies were made with `shutil.copyfile`; the two
  appends by reading the payload's bytes and concatenating them; the four diffs applied with
  `git apply` only.

## Deviations & assumptions

1. **The bundle ran C1a, C1b, C1c, C2, C3 — five commits, exactly as ordered — before this
   handback commit C4.** Nothing was added, dropped or reordered.
2. **`git commit`'s own printed summary line for C2 momentarily read `130 insertions(+), 130
   deletions(-)`** in one intermediate tool-output capture, while `git show --numstat`,
   `git show --stat`, and an independent `git diff --shortstat 9e6d74aa 17be08e7` all agree
   on **109/109**. Re-running `git show --stat HEAD` after the fact confirmed 109/109
   consistently; the 130 reading did not reproduce and no on-disk artifact reflects it. Per
   `.agent/prose_slips.md` rule this is recorded here rather than spent as a finding: nothing
   under `apps/`, `packages/`, `tests/` or `docs/` is affected, and every gate that measured
   this commit's insertions used the reproducible 109 figure.
3. **No trailing commit for the C4 push, `gh pr list`, or `gh run list`; all three go in the
   session reply**, consistent with DECISION amend0827 D2 and F277's own round-19 precedent:
   the push carries this very file, so its outcome cannot be known before the commit exists.
4. **One disposable worktree (`.remedy-wt/f283-r1-mutation-a`) was reused for both G5
   mutations sequentially** rather than two separate worktrees — the block's own phrasing
   ("REMOVE the worktree", singular) supports this reading, and neither mutation was ever
   committed. `git checkout -- apps/cli/commands/job.py` cleanly reverted mutation (a) before
   mutation (b) was applied in the same worktree.
5. **Scratch hygiene.** No log or script was written outside the gitignored
   `.remedy-wt/f283-r1-scratch/` (unused this round — all measurement was done with inline
   `python3` heredocs and reported directly) and the one disposable worktree above. Nothing
   was written into `.remedy-wt/f283-r1-payloads/`.
6. **Constraint 4 held throughout**: only the twenty sites named in the block's token table
   were touched; the twenty slice-B sites (`_cmd_create_job`, `_cmd_show_job`,
   `_cmd_plan_job_local`, `_cmd_run_next_task_local`, `_refuse_budget_set`) and the four
   non-mechanical sites were not migrated, edited, or referenced.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| Pre-flight (STOP, git state, block self-verify) | done | no STOP; tree clean on `main` at `d0d40e89`; block 282 lines / matching sha256 |
| Branch cut | done | `feature/f283-machine-contracts-part-two` created from `main`, no pull |
| C1a copy block | done | 282 insertions, matches block's own line count |
| C1b copy 7 bookkeeping payloads | done | 230 insertions, matches expected 230 |
| C1c copy 2 product payloads | done | 460 insertions, matches expected 460 |
| C2 claim F283, book round 19 PASS, resolve R-1018 | done | 109/109, matches expected 109; all sub-checks (a)-(f) verified |
| C3 migrate job's 20 flagged refusals | done | 262 insertions (76+186), matches expected; 2 paths only |
| C4 the handback | done | this commit |
| G1 payload transport + authored copies | done | 27/27 payload readings equal; 10/10 authored copies byte-identical; 4/4 diffs dry-ran at exit 0 |
| G2(a) live_review.md append | done | 433255 + 5446 = 438701, equal to reviewer's |
| G2(b) prose_slips.md append | done | 357369 + 1160 = 358529, equal to reviewer's |
| G2(c) open set by distinct id | done | 24 at `d0d40e89`, 23 at C2; removed exactly {R-1018}, added {} |
| G2(d) plan.md/context.md rewrites | done | both sha256-equal to payload; plan.md 49 lines, under 50 |
| G2(e) STATUS line + candidates.md | done | `[~] F283 —` prefix; candidates.md carries the single EMPTY line |
| G2(f) six-path diff | done | exactly 6 paths at C1c..C2 |
| G3 slice is reviewer's bytes | done | apply-check exit 0; 2 paths; 20 fail( call sites, matching reviewer's 20-row table |
| G4 slice works, ruff, integrity | done | 611 passed/exit 0; ruff exit 0; integrity all 5 pass, fail_count 0 |
| G5 mutation red-proofs | done | mutation (a) 1 failed/7 passed exit 1 at the named test; mutation (b) 1 failed/7 passed exit 1 at the named test; worktree cleanly force-removed |
| G6 tree, push, PR list, CI run | pending at write time | reported in the worker's session reply with real exit codes |
| Constraint 1 no payload edited/retyped | done | `shutil.copyfile`, byte concatenation, `git apply` only |
| Constraint 2 every commit under 500 insertions | done | 282, 230, 460, 109, 262; this handoff exempt as single `.agent/**` state file |
| Constraint 3 no unnamed file touched | done | 19 paths after this commit, set-equal to the enumeration |
| Constraint 4 no unnamed refusal site migrated | done | only the 20 named sites touched; slice-B and non-mechanical sites untouched |
| Constraint 5 stop on red | done | no gate went red |
| Constraint 6 nothing is merged | done | no `gh pr merge`, no `gh pr create`, no checkout of `main`, no branch deletion |
| Constraint 7 leave job worktrees alone | done | only one disposable G5 worktree added/removed; `remedy/job-*` untouched |

## Next

1. Phase 1 rule 1: read `.agent/STOP` from disk.
2. The review of round 1 — C1a, C1b, C1c, C2, C3, C4, with all six gates re-derived.
3. Then round 2 — SLICE B, which threads `json_output` into `_cmd_show_job`,
   `_cmd_create_job`, `_cmd_plan_job_local`, `_cmd_run_next_task_local` and
   `_refuse_budget_set`, and migrates their twenty sites. `job.show` and `job.run` both
   declare `supports_json: True` and both answer a failure in prose today — the gap T001
   exists to close.

Open findings count: **23** (after C2). Operator-questions count: **2** (Q1, Q2 — both
unchanged by this round).
