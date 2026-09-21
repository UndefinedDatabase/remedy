# Handoff — F283 Machine contracts, part two: refusal sweep, JSON gap, exit-code taxonomy · Round 2 · SLICE B PART ONE + R-1020

## Session

SESSION 1 of feature F283 · round 2 · rounds so far 2

This round booked round 1's PASS, registered R-1020 (52 of 111 `supports_json` commands
reach a shared EXITING helper under `packages/` that prints prose and exits before the
handler's own failure path, so threading `json_output` alone cannot meet T001's Acceptance
line), and migrated eleven more refusal sites of `apps/cli/commands/job.py`: five in
`_cmd_create_job`, one in `_cmd_show_job` (threaded), and five in `_cmd_plan_job_local`, plus
`_refuse_budget_set` itself and its six callers threaded. R-1020 is pinned executable with a
`strict` xfail, not fixed — it reports XFAIL, not XPASS. Context self-assessment: roughly
half the working budget remained at the point this handoff was written.

## Range

Review of `2aa0a6f8`..`HEAD`.

## Block self-verification (R-0954)

| reading | measured | given | equal |
|---|---|---|---|
| line count | 265 | 265 | True |
| sha256 | `2dcc1e0c0f0a56ce7aa118783f0caf554e2f2fdd6844e0cfcc3e2805f75b7734` | `2dcc1e0c0f0a56ce7aa118783f0caf554e2f2fdd6844e0cfcc3e2805f75b7734` | True |

Neither reading differed, so the round went ahead.

## Pre-flight

- `ls .agent/STOP`: `No such file or directory`. No STOP on disk.
- `git status --porcelain`: empty.
- `git branch --show-current`: `feature/f283-machine-contracts-part-two`.
- `git log --oneline -1`: `2aa0a6f8`, matching the delegation message.

## Commits

### 4d1fe176 F283 R2 C1a: copy round 2 block into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f283-r2-block.md | +265/-0 | byte-for-byte copy of this round's step block |

Measured insertions (`git show --numstat`): **265**. Expected: the block's own measured line
count, 265. They **MATCH**. Well under the 500-line cap.

### 5fc0ca59 F283 R2 C1b: copy round 2 payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f283-r2-f283.diff | +25/-0 | byte-for-byte copy of f283.diff |
| .agent/authored/f283-r2-job.diff | +229/-0 | byte-for-byte copy of job.diff |
| .agent/authored/f283-r2-ledger.md | +4/-0 | byte-for-byte copy of ledger.md |
| .agent/authored/f283-r2-plan.md | +49/-0 | byte-for-byte copy of plan.md |
| .agent/authored/f283-r2-tests.diff | +52/-0 | byte-for-byte copy of tests.diff |

Measured insertions (`git show --numstat`): **359**. Expected: **359**
(25+229+4+49+52). They **MATCH**.

### b5b7d1ac F283 R2 C2: book round 1's PASS and register R-1020
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +4/-0 | append ledger.md by strict byte concatenation: round-1 `Gate:` entry and `- R-1020` registration |
| .agent/plan.md | +31/-31 | rewrite to plan.md payload, byte-identical |
| docs/roadmap/features/T2_F283.md | +9/-0 | `git apply` of f283.diff |

Measured insertions (`git show --numstat`): **44** (4+31+9). **Expected 45 per the block —
MY MEASUREMENT DIFFERS BY ONE.** Reported per the block's own instruction ("If yours differs,
report what you measured and say so"): `git diff --shortstat` independently confirmed **44
insertions(+), 31 deletions(-)**, and `git show --numstat` on the committed tree gives the
same three per-path numbers (4, 31, 9) that sum to 44. The block's own prose for this commit
also states the `f283.diff` hunk as `(+10/-0)`; reading the applied diff and the resulting
`git diff --numstat` both give **9**, not 10 — the diff's two hunks add 2 and 7 lines
respectively, summing to 9. I did not force either number to match; I retyped nothing and
applied the payload exactly as given. `git commit`'s own printed summary line for this commit
read `62 insertions(+), 49 deletions(-)`, a third figure that agrees with neither reading —
the same false-summary-line phenomenon round 1's handoff recorded under Deviations for its
own C2; `git show --numstat` and an independent `git diff --shortstat` (44/31) are the
authoritative readings and agree with each other.

### 8741ea88 F283 R2 C3: thread the json flag into job show and budget set, migrate eleven refusals
| Path | +/- | Reason |
|---|---|---|
| apps/cli/commands/job.py | +58/-44 | `git apply` job.diff: eleven sites migrated onto `fail()`; `_cmd_show_job` and `_refuse_budget_set` gain `json_output`; `job.show` dispatch lambda threads `getattr(args, "json", False)` |
| tests/cli/test_job_refusal_envelope.py | +30/-3 | `git apply` tests.diff: ratchet's expected count 20→8, plus the new `strict` xfail pinning R-1020 |

Measured insertions: **88** (58+30). Expected: **88** (58 for job.py, 30 for the test file).
They **MATCH**.

### C4 — THE HANDBACK (this commit)
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | this handback, written once; a single `.agent/**` state file, exempt from the 500-line cap under DECISION F104 D1 |

Self-reference exception (handback template, R-0149 pattern): a handback cannot table the
commit that writes it.

## External actions

- `git worktree add .remedy-wt/f283-r2-mutation 8741ea88` for G5, detached HEAD — used for
  both the threading proof and the two mutation red-proofs, then
  `git worktree remove --force .remedy-wt/f283-r2-mutation` — force was required because the
  ratchet mutation (b) left the worktree with an uncommitted, deliberately-never-committed
  edit; the primary checkout was never touched.
- `git push -u origin feature/f283-machine-contracts-part-two` after C4 — real outcome
  reported in the session reply, since it ships this very file.
- `gh pr list --state open ...` after the push — real outcome reported in the session reply.
- **NOTHING IS MERGED.** No `gh pr merge`, no `gh pr create`, no checkout of `main`, no branch
  deletion.
- No worktree other than the one disposable G5 worktree was added or removed. The three
  `remedy/job-*` worktrees were left alone throughout.

## Verification

### G1 — PAYLOADS transport, fifteen readings, then six authored copies

| file | lines measured/given | bytes measured/given | sha256 equal |
|---|---|---|---|
| f283.diff | 25/25 | 1428/1428 | True |
| job.diff | 229/229 | 10824/10824 | True |
| ledger.md | 4/4 | 7749/7749 | True |
| plan.md | 49/49 | 2586/2586 | True |
| tests.diff | 52/52 | 2841/2841 | True |

**All fifteen readings equal: True.** The three diffs (`f283.diff`, `job.diff`, `tests.diff`)
each dry-ran with `git apply --check` at real exit code **0** before any real apply.

Six `.agent/authored/f283-r2-*` copies (the block copy plus five payloads), each compared
byte-for-byte with its source via `filecmp.cmp(..., shallow=False)` at copy time:

| copy | identical |
|---|---|
| f283-r2-block.md | True |
| f283-r2-f283.diff | True |
| f283-r2-job.diff | True |
| f283-r2-ledger.md | True |
| f283-r2-plan.md | True |
| f283-r2-tests.diff | True |

**Copies compared: 6. All True.**

### G2 — THE BOOKING

**(a) `.agent/live_review.md` append by strict byte concatenation**:

| stage | bytes |
|---|---|
| pre (post-round-1, pre-append) | 438701 |
| payload (ledger.md) | 7749 |
| post (measured) | 446450 |
| pre + payload == post | True |

Matches the reviewer's `438701 + 7749 = 446450` exactly.

**(b) Open set by distinct id**, via `open_finding_ids` from `scripts/rotate_live_review.py`
(imported and called directly against `git show <rev>:.agent/live_review.md` text):

| rev | OPEN by distinct id | reviewer's |
|---|---|---|
| `2aa0a6f8` | **23** | 23 |
| C2 (`b5b7d1ac`) | **24** | 24 |

Set difference: added exactly `{R-1020}`, removed `{}` (empty) — exactly the block's claim.

**(c) `.agent/plan.md` at C2 equals plan.md byte-for-byte**:

| file | sha256 (both sides) | equal |
|---|---|---|
| .agent/plan.md | `a0c9d01a8ebf2140d845cddd4ac207580bb607ace8a53f8cde86fec40cbef405` | True |

Line count: **49**, under the AGENTS.md 50-line rule.

**(d) `git diff --name-only <C1b> <C2>`** (`5fc0ca59`..`b5b7d1ac`) names exactly **three**
paths:

```
.agent/live_review.md
.agent/plan.md
docs/roadmap/features/T2_F283.md
```

### G3 — THE SLICE IS THE REVIEWER'S BYTES

`git apply --check` on `job.diff` and `tests.diff` at C2: both real exit code **0**, run
immediately before their real applies (also exit 0 each). `git diff --name-only <C2> <C3>`
(`b5b7d1ac`..`8741ea88`) names exactly:

```
apps/cli/commands/job.py
tests/cli/test_job_refusal_envelope.py
```

Two paths, as required.

`fail(` call-site count in the committed `apps/cli/commands/job.py` tree: a line-scan for
`fail(` not preceded by a word character finds 34 raw hits; excluding the two docstring/prose
mentions at lines 40 and 42 (same exclusion round 1's handoff used) yields **32** real call
sites. The reviewer's stated count is **32** (20 round 1 + 11 round 2 + 1 inside
`_refuse_budget_set` itself). Both are **32**.

Print-then-exit pairs remaining in a handler WITHOUT `json_output`, counted via the test
module's own `_refusal_sites()` helper: **8**, at lines `[870, 918, 860, 876, 931, 935, 939,
943]`. Locating each by AST function boundary: all eight resolve to `_cmd_run_next_task_local`
and no other function. Matches the reviewer's 8, all in `_cmd_run_next_task_local`.

### G4 — THE SLICE WORKS AND THE OPERATOR SEES THE SAME BYTES

```
$ bash -c 'python3 -m pytest -q -p no:cacheprovider tests/docs/ tests/cli/test_job_refusal_envelope.py tests/cli/test_job_budget_set.py tests/cli/test_job_commands.py tests/cli/test_job_show.py tests/cli/test_job_stop.py tests/cli/test_job_report.py tests/cli/test_plan_approval.py tests/cli/test_json_envelope.py tests/cli/test_golden_path.py tests/test_cli_main.py tests/test_data_paths.py tests/test_run_log_cli.py tests/orchestration/test_structured_planner_cli.py; echo "REAL_EXIT=$?"'
703 passed, 1 xfailed in 145.60s (0:02:25)
REAL_EXIT=0
```

Matches the reviewer's `703 passed, 1 xfailed` at real exit code 0 exactly. **XFAIL COUNT: 1**
— not an XPASS.

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
Real exit code **0**. All five checks `pass`, `passed: true`, `fail_count: 0`. The full suite
was NOT re-run — amend0917 rule 1 gives F283 exactly one full-suite run, spent at closure.

### G5 — THE NEW BEHAVIOUR IS REAL AND THE GUARD STILL GATES

Disposable worktree `.remedy-wt/f283-r2-mutation` added at `8741ea88` (C3), used for the
threading proof and both mutations, removed after.

**(a) PROVE THE THREADING** — `_cmd_job_budget_set(job_id="zzzznotajob",
field_name="not_a_field", raw_value="5", json_output=...)`:

`json_output=True`: exit **2**, stderr `''` (empty), stdout envelope
`{"error": "unknown_budget_field", "message": "unknown budget field 'not_a_field'. Settable:
...", "ok": false, "schema_version": 1}`.

`json_output=False`: exit **2**, stdout `''` (empty), stderr
`Error: unknown budget field 'not_a_field'. Settable: ...\n`.

Both match the block's required shapes exactly.

**(b) MUTATE AND SHOW RED — reported honestly, including the one that does not go red.**

Mutation 1 — rename the token (`"unknown_budget_field"` → `"bad_field"` at the
`_refuse_budget_set` call site inside `_cmd_job_budget_set`, since the token is passed through
`_refuse_budget_set(...)` rather than directly as `fail("unknown_budget_field"...)` — the
block's literal `fail(` phrasing names the shared helper's own effect, not its call-site
spelling; I mutated the token string this round's diff introduced at line 2166):

```
$ bash -c 'python3 -m pytest -q -p no:cacheprovider tests/cli/test_job_refusal_envelope.py; echo "REAL_EXIT=$?"'
.......x.
8 passed, 1 xfailed in 0.36s
REAL_EXIT=0
```

**This does NOT go red.** No test in `tests/cli/test_job_refusal_envelope.py` names the
`unknown_budget_field` token, so renaming it is invisible to the suite — exactly the gap the
block calls "the reviewer's own gap," reported here rather than hidden. Reverted with
`git checkout -- apps/cli/commands/job.py` in the disposable worktree before mutation 2.

Mutation 2 — the ratchet (`assert len(unflagged) == 8` → `== 9` in
`test_the_unflagged_sites_are_counted_not_forgotten`):

```
$ bash -c 'python3 -m pytest -q -p no:cacheprovider .../test_job_refusal_envelope.py -k test_the_unflagged_sites_are_counted_not_forgotten; echo "REAL_EXIT=$?"'
F
AssertionError: expected the 9 sites whose handler has no json flag, found 8 at lines [870, 918, 860, 876, 931, 935, 939, 943]
1 failed, 8 deselected in 0.23s
REAL_EXIT=1
```

**This goes RED** at `test_the_unflagged_sites_are_counted_not_forgotten`, exactly as the
block names it.

`git worktree remove --force .remedy-wt/f283-r2-mutation` (force needed: mutation 2 left the
worktree dirty by design, never committed). `git worktree list` after removal:

```
/home/decodeux/Repos/remedy                                  8741ea88 [feature/f283-machine-contracts-part-two]
/home/decodeux/Repos/remedy/.remedy-wt/job-468c8e62a2cc4fac  1b9ae606 [remedy/job-468c8e62a2cc4fac]
/home/decodeux/Repos/remedy/.remedy-wt/job-86f628f5e4fb4e0c  aca27d4a [remedy/job-86f628f5e4fb4e0c]
/home/decodeux/Repos/remedy/.remedy-wt/job-c1dba9c3d7874968  fd23710f [remedy/job-c1dba9c3d7874968]
```

Only the primary checkout and the three `remedy/job-*` worktrees remain.

### G6 — TREE AND PUSH

Reported in full in the worker's session reply once this commit exists (push carries this
file). At write time: `git status --porcelain` empty; `git log --oneline -n 5` shows C4, C3,
C2, C1b, C1a in that order (`8741ea88`, `b5b7d1ac`, `5fc0ca59`, `4d1fe176` below this commit);
`git worktree list` shows the primary checkout and the three `remedy/job-*` worktrees and
nothing else. Push outcome and `gh pr list` reported in the session reply.

### The round's whole tracked path set (before this commit)

`git diff --name-only 2aa0a6f8 8741ea88` — **11** paths:

| # | path | introduced by |
|---|---|---|
| 1 | .agent/authored/f283-r2-block.md | C1a `4d1fe176` |
| 2 | .agent/authored/f283-r2-f283.diff | C1b `5fc0ca59` |
| 3 | .agent/authored/f283-r2-job.diff | C1b `5fc0ca59` |
| 4 | .agent/authored/f283-r2-ledger.md | C1b `5fc0ca59` |
| 5 | .agent/authored/f283-r2-plan.md | C1b `5fc0ca59` |
| 6 | .agent/authored/f283-r2-tests.diff | C1b `5fc0ca59` |
| 7 | .agent/live_review.md | C2 `b5b7d1ac` |
| 8 | .agent/plan.md | C2 `b5b7d1ac` |
| 9 | docs/roadmap/features/T2_F283.md | C2 `b5b7d1ac` |
| 10 | apps/cli/commands/job.py | C3 `8741ea88` |
| 11 | tests/cli/test_job_refusal_envelope.py | C3 `8741ea88` |

Plus `.agent/handoff.md` from this commit makes **12** — set-equal to constraint 3's
enumeration (six authored copies plus the five named tracked paths plus the handoff itself).
`.agent/candidates.md`, `.agent/context.md`, `.agent/decisions.md`,
`.agent/operator_questions.md`, `README.md`, `docs/roadmap/STATUS.md`, and any module other
than `job.py` appear **0** times.

## Authored-text proofs

- The six copies at C1a/C1b, compared with the reviewer's originals under
  `.remedy-wt/f283-r2-payloads/` and `.remedy-wt/f283-r2-block.md`: **six readings, all
  True** (G1).
- The one REWRITE payload against its committed file: `.agent/plan.md` is sha256-equal to its
  payload (G2c).
- The one APPEND payload against its committed file: strict byte concatenation True for
  `.agent/live_review.md` (ledger.md), byte numbers equal to the reviewer's (G2a).
- The three DIFF payloads (`f283.diff`, `job.diff`, `tests.diff`): each applied with
  `git apply`, never retyped; each dry-ran with `git apply --check` at exit 0 first (G1, G3).
- No payload was edited or retyped. All six copies were made with `shutil.copyfile`; the one
  append by reading the payload's bytes and concatenating them; the three diffs applied with
  `git apply` only.

## Deviations & assumptions

1. **The bundle ran C1a, C1b, C2, C3 — four commits, exactly as ordered — before this handback
   commit C4.** Nothing was added, dropped or reordered.
2. **C2's measured insertions are 44, not the block's stated 45**, and the `f283.diff` hunk
   for `docs/roadmap/features/T2_F283.md` measures +9/-0, not the block's stated +10/-0. Both
   were reported per the block's own instruction rather than forced to match; `git show
   --numstat`, an independent `git diff --shortstat`, and a direct read of the applied diff's
   two hunks (2 lines + 7 lines = 9) all agree on 44/9. Nothing was retyped or edited to make
   either number match — the payload was applied byte-for-byte via `git apply` exactly as
   given.
3. **`git commit`'s own printed summary line for C2 read `62 insertions(+), 49 deletions(-)`**,
   a third figure agreeing with neither the block's 45 nor the measured 44. This is the same
   false-summary-line phenomenon round 1's handoff recorded for its own C2 (there: printed 130
   insertions/130 deletions against a reproducible 109/109). `git show --numstat` and an
   independent `git diff --shortstat` are the authoritative readings and agree with each other
   at 44/31; nothing under `apps/`, `packages/`, `tests/` or `docs/` is affected by this
   printed-summary artifact.
4. **G5(b) mutation 1 targeted the token string at the `_refuse_budget_set` call site**
   (`"unknown_budget_field"` → `"bad_field"`), since this round's own diff routes that
   condition through `_refuse_budget_set(token, message, json_output=...)` rather than a
   direct `fail("unknown_budget_field"...)` call — the shared helper is what the block's
   `fail(` phrasing names by effect. The mutation still exercises the exact behaviour the block
   describes (a token silently renamed with no test noticing) and reproduced the reviewer's
   stated non-red result exactly.
5. **No trailing commit for the C4 push or `gh pr list`; both go in the session reply**,
   consistent with DECISION amend0827 D2 and round 1's own precedent: the push carries this
   very file, so its outcome cannot be known before the commit exists.
6. **One disposable worktree (`.remedy-wt/f283-r2-mutation`) was reused for the threading proof
   and both G5 mutations sequentially** rather than separate worktrees — consistent with round
   1's reading of the block's singular "REMOVE the worktree" phrasing. Neither mutation was
   ever committed; `git checkout --` cleanly reverted mutation 1 before mutation 2 was applied
   in the same worktree.
7. **Scratch hygiene.** Three small scripts were written to the gitignored
   `.remedy-wt/f283-r2-scratch/` (`count_fail_sites.py`, `find_unflagged_pairs.py`,
   `locate_functions.py`, `prove_threading.py`) for measurement; none were committed, nothing
   was written into `.remedy-wt/f283-r2-payloads/`.
8. **Constraint 4 held throughout**: only the eleven sites named in the block's token table
   were touched (`_cmd_create_job` ×5, `_cmd_show_job` ×1, `_cmd_plan_job_local` ×5, plus
   `_refuse_budget_set` and its six callers); `_cmd_run_next_task_local`'s eight sites and the
   four non-mechanical sites were not migrated, edited, or referenced. R-1020 was registered,
   not repaired — the xfail reports XFAIL (1 xfailed in G4, confirmed again isolated in G5),
   never XPASS.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| Pre-flight (STOP, git state, block self-verify) | done | no STOP; tree clean at `2aa0a6f8`; block 265 lines / matching sha256 |
| C1a copy block | done | 265 insertions, matches block's own line count |
| C1b copy 5 payloads | done | 359 insertions, matches expected 359 |
| C2 book round 1 PASS, register R-1020 | deviated | 44/9 measured vs block's stated 45/10 — reported per block's own instruction, nothing retyped |
| C3 migrate 11 refusals, thread json_output | done | 88 insertions (58+30), matches expected; 2 paths only |
| C4 the handback | done | this commit |
| G1 payload transport + authored copies | done | 15/15 payload readings equal; 6/6 authored copies byte-identical; 3/3 diffs dry-ran at exit 0 |
| G2(a) live_review.md append | done | 438701 + 7749 = 446450, equal to reviewer's |
| G2(b) open set by distinct id | done | 23 at `2aa0a6f8`, 24 at C2; added exactly {R-1020}, removed {} |
| G2(c) plan.md rewrite | done | sha256-equal to payload; 49 lines, under 50 |
| G2(d) three-path diff | done | exactly 3 paths at C1b..C2 |
| G3 slice is reviewer's bytes | done | apply-check exit 0 ×2; 2 paths; 32 fail( sites; 8 unflagged pairs all in `_cmd_run_next_task_local` |
| G4 slice works, ruff, integrity | done | 703 passed/1 xfailed/exit 0; ruff exit 0; integrity all 5 pass, fail_count 0 |
| G5(a) threading proof | done | json_output=True: exit 2, empty stderr, envelope; json_output=False: exit 2, empty stdout, prose stderr |
| G5(b) mutation red-proofs | done | mutation 1 does NOT go red (8 passed/1 xfailed, exit 0) — reported honestly; mutation 2 goes RED (1 failed, exit 1) at the named test; worktree cleanly force-removed |
| G6 tree, push, PR list | pending at write time | reported in the worker's session reply with real exit codes |
| Constraint 1 no payload edited/retyped | done | `shutil.copyfile`, byte concatenation, `git apply` only |
| Constraint 2 every commit under 500 insertions | done | 265, 359, 44, 88; this handoff exempt as single `.agent/**` state file |
| Constraint 3 no unnamed file touched | done | 12 paths after this commit, set-equal to the enumeration |
| Constraint 4 no unnamed refusal site migrated, R-1020 not repaired | done | only the 11 named sites touched; xfail reports XFAIL, not XPASS |
| Constraint 5 stop on red | done | no gate went red |
| Constraint 6 nothing is merged | done | no `gh pr merge`, no `gh pr create`, no checkout of `main`, no branch deletion |
| Constraint 7 leave job worktrees alone | done | only one disposable G5 worktree added/removed; `remedy/job-*` untouched |

## Next

1. Phase 1 rule 1: read `.agent/STOP` from disk.
2. The review of round 2 — C1a, C1b, C2, C3, C4, with all six gates re-derived.
3. Then round 3 — R-1020's repair, which the reviewer rules comes BEFORE any further group
   migration, because T001's catalog half is worth nothing while 52 of the 111
   `supports_json` commands answer a bad argument in prose. Round 3 must delete the `xfail`
   mark in the same commit that turns it green.

Open findings count: **24** (after C2). Operator-questions count: **2** (Q1, Q2 — both
unchanged by this round).
