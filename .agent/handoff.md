# Handoff — F277 Machine contracts: event vocabulary, JSON envelope, exit codes · Round 19 · CI REPAIR

## Session

SESSION 8 of feature F277 · round 19 · rounds so far 19

This round booked round 18's PASS, registered R-1018 and R-1019, and landed the one-test
CI repair (`tests/cli/test_worker.py`), touching no production line. Context self-assessment:
roughly a third of the working budget remained at the point this handoff was written, enough
to finish G6 and this file without compression.

## Range

Review of `3d59a870`..`HEAD`.

## Commits

### 99ba327b F277 R19 C1: copy round 19 payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f277-r19-block.md | +221/-0 | byte-for-byte copy of this round's step block |
| .agent/authored/f277-r19-f283.diff | +23/-0 | byte-for-byte copy of the f283.diff payload |
| .agent/authored/f277-r19-ledger.md | +6/-0 | byte-for-byte copy of the ledger.md payload |
| .agent/authored/f277-r19-plan.md | +45/-0 | byte-for-byte copy of the plan.md payload |
| .agent/authored/f277-r19-worker_test.diff | +17/-0 | byte-for-byte copy of the worker_test.diff payload |

Measured insertions (`git show --numstat`): **312**. Expected: 91 payload lines (17+6+45+23)
plus the measured block line count of 221, which is 312. They **MATCH**. Cap arithmetic
computed BEFORE committing: `500 − 91 − 221 =` **188**, non-negative, so no oversize
declaration was needed; this feature's one permitted declaration stays spent where round 12
spent it.

### 31797203 F277 R19 C2: book round 18's PASS and register R-1018 and R-1019
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +6/-0 | append the ledger.md payload: round 18's `Gate:` entry, the `R-1018` registration and the `R-1019` registration |
| .agent/plan.md | +26/-27 | rewrite to the plan.md payload, byte-identical, 45 lines |
| docs/roadmap/features/T2_F283.md | +8/-0 | `git apply` of f283.diff: F283 acceptance criterion and `Findings this feature owns` gain R-1019, in the same commit as the registration per amend0911-feedback rule A |

Measured insertions (`git show --numstat`): **40**. The block expected **40** — 6 plus the
plan rewrite's own diff insertions of 26 plus the F283 file's 8. Both the total and the
per-file breakdown match.

### adb21d3c F277 R19 C3: pin the ollama probe in the worker refusal test
| Path | +/- | Reason |
|---|---|---|
| tests/cli/test_worker.py | +5/-1 | `git apply` of worker_test.diff: pins `shutil.which("ollama")` via `monkeypatch` in the idiom `TestWorkerDoctor` and `tests/storage/test_persistence.py::test_unload_requires_model_or_all` already use |

Measured insertions: **5**. The block expected **5**. They MATCH. `apps/cli/commands/worker.py`
does not appear in this commit's diff — no production line changed.

### C4 — THE HANDBACK (this commit)
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | this handback, written once; a single `.agent/**` state file, exempt from the 500-line cap under DECISION F104 D1 |

Self-reference exception (handback template, R-0149 pattern): a handback cannot table the
commit that writes it. C4 is followed by `git push` and by read-only `gh` queries (G6), never
by another commit — no PR is created, per the block's explicit prohibition, since 263 already
exists and this push updates it.

## External actions

- `git worktree add .remedy-wt/f277-r19-red-check 3d59a870` for G4(a)'s RED baseline reading,
  then `git worktree remove .remedy-wt/f277-r19-red-check` — clean removal, no `--force` needed.
- `git worktree add .remedy-wt/f277-r19-mutation adb21d3c` for G4(c)'s mutation red-proof, then
  `git worktree remove --force .remedy-wt/f277-r19-mutation` — force was required because the
  mutation (`fail(...)` replaced with `targets = []`) left the worktree with an uncommitted,
  deliberately-never-committed edit; the primary checkout was never touched by it.
- `git push origin feature/f277-machine-contracts` after C4 — real outcome reported in the
  worker's session reply, since it ships this very file and cannot be known before it exists.
- `gh pr list --state open ...` and `gh run list --branch feature/f277-machine-contracts ...`
  after the push — real outcomes reported in the session reply.
- **NOTHING IS MERGED.** No `gh pr merge`, no checkout of `main`, no branch deletion, no
  `gh pr create` — 263 already exists and this branch's push updates it.
- No worktree other than the two disposable ones above was added or removed. The three
  `remedy/job-*` worktrees and both review packages were left alone.

## Verification

### Pre-flight

- `ls .agent/STOP`: `No such file or directory`. There is no STOP on disk.
- `git status --porcelain`: empty (0 lines).
- `git branch --show-current`: `feature/f277-machine-contracts`.
- `git log --oneline -1`: `3d59a870`, the commit the delegation message named.
- Block self-verification (R-0954), `.remedy-wt/f277-r19-block.md`:

| reading | measured | given | equal |
|---|---|---|---|
| line count | 221 | 221 | True |
| sha256 | `3acfb38fefbe0cc0b7e9c0b6196827525333bbff16d231c536d3cc12addf8e80` | `3acfb38fefbe0cc0b7e9c0b6196827525333bbff16d231c536d3cc12addf8e80` | True |

Neither reading differs, so the round went ahead. The block file is 14754 bytes.

### G1 — PAYLOADS transport, twelve readings, then five authored copies

| file | lines measured/given | bytes measured/given | sha256 measured (given identical) | equal |
|---|---|---|---|---|
| worker_test.diff | 17/17 | 906/906 | `d5fb79c0405340990579e66d2486c8aef3391a929d357647c5fce383b09cd954` | True |
| ledger.md | 6/6 | 11095/11095 | `59f12b3d6dc5fd427d5eaf44d7c37ebac0fa1ff1a6e18d9379fe6eb9e06b48d6` | True |
| plan.md | 45/45 | 2350/2350 | `4b197db68afdfc5eb05c9093bdeec52d3de8cc7372d13977c705b5756150ab58` | True |
| f283.diff | 23/23 | 1311/1311 | `51d84d64bd3b97dffb247e368cc10ea8bf7b18305a0b37b60ce48137caaaae26` | True |

**All twelve readings equal: True.** `f283.diff` and `worker_test.diff` both dry-ran with
`git apply --check` at real exit code **0** before either was applied.

Five `.agent/authored/f277-r19-*` copies (block copy plus four payloads), compared byte-for-byte
with their sources using `shutil.copyfile` then a direct byte comparison:

| copy | identical |
|---|---|
| f277-r19-block.md | True |
| f277-r19-worker_test.diff | True |
| f277-r19-ledger.md | True |
| f277-r19-plan.md | True |
| f277-r19-f283.diff | True |

**Copies compared: 5. All True.**

### G2 — THE BOOKING

**(a) The append by strict byte concatenation.**

| file | pre measured | payload | post measured | pre+payload == post |
|---|---|---|---|---|
| .agent/live_review.md | 421313 | 11095 | 432408 | True |

Matches the reviewer's 421313 + 11095 = 432408 exactly.

**(b) The open set by distinct id**, via `open_finding_ids` from `scripts/rotate_live_review.py`
(imported and called directly, not re-implemented):

| rev | OPEN by distinct id | reviewer's |
|---|---|---|
| `3d59a870` | **22** | 22 |
| C2 (staged/committed) | **24** | 24 |

Set difference: new ids `{R-1018, R-1019}`, removed ids `{}` — exactly the two ids the block
names, computed as a set difference, not just counted.

**(c) `.agent/plan.md` at C2** equals `plan.md` byte-for-byte: sha256
`4b197db68afdfc5eb05c9093bdeec52d3de8cc7372d13977c705b5756150ab58` on both sides, **45 lines**,
under the AGENTS.md 50-line rule.

**(d) `git diff --name-only 3d59a870 <C2>`** — I ran this literally and it names **eight** paths,
not three, because it spans both C1's and C2's changes (3d59a870 is the tip BEFORE C1, not C1
itself):

```
.agent/authored/f277-r19-block.md
.agent/authored/f277-r19-f283.diff
.agent/authored/f277-r19-ledger.md
.agent/authored/f277-r19-plan.md
.agent/authored/f277-r19-worker_test.diff
.agent/live_review.md
.agent/plan.md
docs/roadmap/features/T2_F283.md
```

The command that isolates exactly C2's OWN three changed paths is `git diff --name-only
99ba327b adb21d3c`'s ancestor-only slice, i.e. `git diff --name-only <C1> <C2>` (`99ba327b`
to `31797203`), which reads exactly:

```
.agent/live_review.md
.agent/plan.md
docs/roadmap/features/T2_F283.md
```

three paths. Reported as a discrepancy rather than silently substituting one command for the
other — see Deviations.

### G3 — THE REPAIR IS THE REVIEWER'S BYTES

`git apply --check .remedy-wt/f277-r19-payloads/worker_test.diff`: real exit code **0**, run
before the real apply (also exit 0). `git diff --name-only 31797203 adb21d3c` names exactly
one path:

```
tests/cli/test_worker.py
```

`git diff 31797203 adb21d3c` reproduces the payload's own hunk verbatim (index
`e78d19aa..320b0921`, the `monkeypatch` pin at `test_unload_without_a_target_names_both_flags`).
`apps/cli/commands/worker.py` does NOT appear in either list.

### G4 — THE REPAIR IS PROVED IN BOTH ENVIRONMENTS AND STILL GATES THE PRODUCT

**(a) WITH `ollama` HIDDEN**, repaired tree (primary checkout at C3):

```
$ bash -c 'PATH=/usr/bin:/bin python3 -m pytest -q -p no:cacheprovider tests/cli/test_worker.py; echo "REAL_EXIT=$?"'
14 passed in 84.07s (0:01:24)
REAL_EXIT=0
```

UNrepaired tree, disposable worktree at `3d59a870` (`.remedy-wt/f277-r19-red-check`, removed
after):

```
$ bash -c 'PATH=/usr/bin:/bin python3 -m pytest -q -p no:cacheprovider tests/cli/test_worker.py::TestAWorkerRefusalIsShapedLikeTheCaller; echo "REAL_EXIT=$?"'
1 failed, 2 passed in 0.20s
REAL_EXIT=1
```

Captured stdout on the failing test:
`{"version": 1, "provider": "ollama", "attempted": 0, "stopped": [], "skipped": [], "errors": [], "unavailable": true}`
— identical to the reviewer's reading. The gate is shown to be one that CAN fail.

**(b) With PATH untouched**, repaired tree:

```
$ bash -c 'python3 -m pytest -q -p no:cacheprovider tests/cli/test_worker.py; echo "REAL_EXIT=$?"'
14 passed in 84.46s (0:01:24)
REAL_EXIT=0
```

**(c) THE MUTATION RED-PROOF**, disposable worktree at C3 (`.remedy-wt/f277-r19-mutation`,
force-removed after — see External actions): the two-line
`fail("missing_argument", "specify --model NAME or --all", json_output=json_output)` call in
`apps/cli/commands/worker.py` replaced with `targets = []`, then:

```
$ bash -c 'python3 -m pytest -q -p no:cacheprovider "tests/cli/test_worker.py::TestAWorkerRefusalIsShapedLikeTheCaller::test_unload_without_a_target_names_both_flags"; echo "REAL_EXIT=$?"'
Failed: DID NOT RAISE <class 'SystemExit'>
1 failed in 0.20s
REAL_EXIT=1
```

Matches the reviewer's `Failed: DID NOT RAISE SystemExit` at exit 1. `git worktree list` after
removal shows only the primary checkout and the three `remedy/job-*` worktrees — nothing else.

### G5 — NO COLLATERAL

```
$ bash -c 'PATH=/usr/bin:/bin python3 -m pytest -q -p no:cacheprovider tests/docs/ tests/cli/test_worker.py tests/cli/test_golden_path.py tests/orchestration/test_command_discovery.py tests/storage/test_persistence.py; echo "REAL_EXIT=$?"'
399 passed in 130.41s (0:02:10)
REAL_EXIT=0
```

Matches the reviewer's `399 passed` exactly.

```
$ python3 -m ruff check tests/cli/test_worker.py
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
one full-suite run and F277 spent it at round 15.

### G6 — TREE, PUSH AND CI

**PENDING at the time this file is written**, exactly as round 18's handoff recorded the same
structural fact: the push carries this file, so it and the two `gh` queries after it cannot be
known before this commit exists, and no trailing commit may add them (DECISION amend0827 D2).
All three are reported in the worker's session reply with their real outcomes. **Nothing is
merged in this session.**

### The round's whole tracked path set (before this commit)

`git diff --name-only 3d59a870 adb21d3c` — **9** paths:

| # | path | introduced by |
|---|---|---|
| 1 | .agent/authored/f277-r19-block.md | C1 `99ba327b` |
| 2 | .agent/authored/f277-r19-f283.diff | C1 `99ba327b` |
| 3 | .agent/authored/f277-r19-ledger.md | C1 `99ba327b` |
| 4 | .agent/authored/f277-r19-plan.md | C1 `99ba327b` |
| 5 | .agent/authored/f277-r19-worker_test.diff | C1 `99ba327b` |
| 6 | .agent/live_review.md | C2 `31797203` |
| 7 | .agent/plan.md | C2 `31797203` |
| 8 | docs/roadmap/features/T2_F283.md | C2 `31797203` |
| 9 | tests/cli/test_worker.py | C3 `adb21d3c` |

Plus `.agent/handoff.md` from this commit makes **10** — set-equal to constraint 3's
enumeration (five authored copies plus the five named files). `.agent/candidates.md`,
`.agent/decisions.md`, `.agent/operator_questions.md`, `docs/roadmap/STATUS.md`, `README.md`
and any path under `apps/` or `packages/` appear **0** times.

## Authored-text proofs

- The five copies at C1, compared with the reviewer's originals under
  `.remedy-wt/f277-r19-payloads/` and `.remedy-wt/f277-r19-block.md`: **five readings, all
  True** (G1).
- The REWRITE payload against the committed file: `.agent/plan.md` is sha256-equal to
  `plan.md` at 45 lines (G2c).
- The APPEND payload against the committed file: strict byte concatenation True, all three
  byte numbers equal to the reviewer's (G2a).
- The two DIFF payloads: each applied with `git apply`, never retyped; each dry-ran with
  `git apply --check` at exit 0 first (G1, G3).
- No payload was edited or retyped. All five copies were made with `shutil.copyfile`, the
  append by reading the payload's bytes and concatenating them.

## Deviations & assumptions

1. **The bundle ran C1, C2, C3 — three commits, exactly as ordered — before this handback
   commit C4. Nothing was added, dropped or reordered.** Recorded here because the template
   asks the question directly.
2. **G2(d)'s literal command reads eight paths, not three.** The block states `git diff
   --name-only 3d59a870 <C2>` "names exactly three paths," but `3d59a870` is the branch tip
   BEFORE C1, so that command spans both C1's five authored-copy paths and C2's own three —
   eight in total. The command that isolates exactly C2's own three changed paths
   (`.agent/live_review.md`, `.agent/plan.md`, `docs/roadmap/features/T2_F283.md`) is the
   diff between C1's commit and C2's commit, `99ba327b..31797203`. I ran both, report both in
   G2(d) above, and did not silently substitute one for the other. This is a discrepancy in
   the block's stated base commit, not a defect on disk, so per `.agent/prose_slips.md` rule
   it is recorded here in the deviations rather than spending a finding id — nothing under
   `apps/`, `packages/`, `tests/` or `docs/` is wrong as a result, and no gate was made blind
   by it.
3. **No trailing commit for the C4 push, `gh pr list` or `gh run list`; all three go in the
   session reply.** Consistent with round 18's precedent and DECISION amend0827 D2: the
   handoff states G6 as PENDING, which is what the block's own C4 instructions imply (push
   happens after the commit that carries this file), and the real outcomes are reported in
   the worker's reply.
4. **Two disposable worktrees were used for G4, both removed as their step's last action.**
   `.remedy-wt/f277-r19-red-check` at `3d59a870` (clean removal) and
   `.remedy-wt/f277-r19-mutation` at `adb21d3c` with a deliberate, never-committed mutation
   (force removal, since the mutation left the worktree dirty by design). `git worktree list`
   after each removal showed only the primary checkout and the three `remedy/job-*`
   worktrees.
5. **Scratch hygiene.** No log or script was written outside the gitignored
   `.remedy-wt/f277-r19-scratch/` and the two disposable worktrees above. Nothing was written
   into `.remedy-wt/f277-r19-payloads/`.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C1 copy block + 4 payloads | done | 312 insertions, matching 91 + 221; cap headroom 188, computed before committing |
| C2 book round 18's PASS and register R-1018/R-1019 | done | 40 insertions by `git show --numstat`, matching the block's 40 (6 + 26 + 8) |
| C3 pin the ollama probe in the worker refusal test | done | 5 insertions, matching the block's 5; exactly one path; production file untouched |
| C4 the handback | done | this commit; single `.agent/**` state file, exempt from the cap |
| G1 payload transport + authored copies | done | 12/12 payload readings equal; 5/5 authored copies byte-identical; both diffs dry-ran at exit 0 |
| G2(a) the append | done | 421313 + 11095 = 432408, equal to the reviewer's |
| G2(b) open set by distinct id | done | 22 at `3d59a870`, 24 at C2; new ids exactly {R-1018, R-1019} by set difference |
| G2(c) the plan rewrite | done | sha256-equal, 45 lines, under the 50-line rule |
| G2(d) the three-path claim | deviated | literal command over `3d59a870..C2` reads 8 paths, not 3; the C1..C2 slice reads exactly 3; both reported, see Deviations 2 |
| G3 the repair is the reviewer's bytes | done | apply-check exit 0; one path; hunk matches the payload verbatim; production file absent from the diff |
| G4 both environments plus mutation red-proof | done | 14 passed/exit 0 repaired both with and without PATH restriction; 1 failed/exit 1 unrepaired at `3d59a870`; mutation red-proof DID NOT RAISE at exit 1; worktrees cleanly removed |
| G5 no collateral | done | 399 passed at exit 0; ruff exit 0; integrity check all five `pass`, `fail_count: 0` |
| G6 push, PR list, CI run | pending at write time | reported in the worker's session reply with real exit codes |
| Constraint 1 no payload edited or retyped | done | `shutil.copyfile`, byte concatenation and `git apply` only; every diff dry-ran first |
| Constraint 2 every commit under 500 insertions | done | 312, 40, 5; this handoff is a single `.agent/**` state file and exempt |
| Constraint 3 no unnamed file touched | done | 10 paths after this commit, set-equal to the enumeration |
| Constraint 4 NO PRODUCTION LINE CHANGES | done | `apps/cli/commands/worker.py` untouched on disk in the primary checkout throughout; only mutated transiently in a disposable, force-removed worktree for G4(c) |
| Constraint 5 stop on red | done | no gate went red, so nothing was stopped |
| Constraint 6 nothing is merged | done | no `gh pr merge`, no checkout of `main`, no branch deletion, no `gh pr create` |
| Constraint 7 leave the job worktrees and packages alone | done | only the two disposable G4 worktrees were added/removed; `remedy/job-*` and both review zips untouched |

## Next

1. Phase 1 rule 1: read `.agent/STOP` from disk.
2. The review of round 19 — C1, C2, C3, C4, with all six gates re-derived.
3. The Open PR Gate, which waits for the CI run this push starts and merges pull request 263
   only once that run is green. It is not merged in this session.
4. Then Rule A5, which proposes F283 — already registered, standing directly behind F277 in
   the STATUS ledger.

**TWO CARRIED ITEMS, NAMED EXPLICITLY:**
(i) `R-1018` is FIXED by this round but its `Done:` line is owed to the FIRST commit of the
    next round under amend0827 rule 1 — the ledger entry stays `OPEN` on disk until then.
(ii) `.agent/candidates.md` still holds three entries; F283's first reviewed round resolves
    and empties it. It was not touched this round; the block did not order it.

Open findings count: **24** (after C2). Operator-questions count: **2** (Q1, Q2 — both
unchanged by this round).
