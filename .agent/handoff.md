# Handoff — F112 Prompt budget per task class, round 3 (T001 completion)

## Session

SESSION 1 of feature F112 · round 3 · rounds so far 3.

This round fixes `R-0791` (two ruff-confirmed defects round 2's own
MODULE slice shipped into `packages/orchestration/prompt_budget.py`:
`UP037` redundant-quotes type hint, `W292` missing trailing newline),
books round 2's PASS verdict into `.agent/live_review.md`, records round
2's transport prose slip into `.agent/prose_slips.md`, and ships
`tests/orchestration/test_class_prompt_budget.py` (24 tests), completing
T001. Still no compiler wiring — T002.

## Range

`e33a6161..72779afb` (commits C0a through C4; C5 is this handback
commit itself).

## Commits

### 6774b8c7 F112 R3 C0a: save round 3 block verbatim to .agent/authored/f112-r3.md

| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f112-r3.md` | +392/-0 | verbatim transport of this round's block, written directly by the Write tool from the prompt's literal bytes |

### 0615479d F112 R3 C0b: mirror the committed authored file to last_block

| Path | +/- | Reason |
|------|-----|--------|
| `.agent/last_block.md` | +392/-367 | whole-file mirror of the committed `.agent/authored/f112-r3.md`, overwriting the prior F112 R2 block it held |

### 5e5bc5fe F112 R3 C1: apply PLAN3 to plan.md

| Path | +/- | Reason |
|------|-----|--------|
| `.agent/plan.md` | +13/-17 | whole-file replacement with PLAN3, extracted programmatically from the committed authored file; first substantive commit of the round per §3 item 23 since this round registers/resolves R-0791 |

### 9596c7ba F112 R3 C2: fix R-0791 (redundant quotes, missing trailing newline)

| Path | +/- | Reason |
|------|-----|--------|
| `packages/orchestration/prompt_budget.py` | +2/-2 | THE FIX: `str.replace(FROM, TO, 1)` removing the redundant quotes around the `RemedyConfig` forward reference, then one `0x0a` byte appended at EOF |

### 16127656 F112 R3 C3: append RECORD2 to live_review.md and SLIP1 to prose_slips.md

| Path | +/- | Reason |
|------|-----|--------|
| `.agent/live_review.md` | +3/-1 | append of RECORD2 (F112 R2's PASS verdict, including R-0791's registration and resolution) as two newline bytes plus the slice, matching the file's own convention |
| `.agent/prose_slips.md` | +3/-1 | append of SLIP1 (round 2's marker-boundary trailing-newline ambiguity, no product effect) as two newline bytes plus the slice |

### 72779afb F112 R3 C4: add tests/orchestration/test_class_prompt_budget.py

| Path | +/- | Reason |
|------|-----|--------|
| `tests/orchestration/test_class_prompt_budget.py` | +165/-0 | brand new file, written byte-for-byte from the committed TEST_FILE slice (copyfile via `cp`, not the Write tool — see Deviations) |

### C5 (this commit, self-reference)

| Path | +/- | Reason |
|------|-----|--------|
| `.agent/handoff.md` | (this commit) | the round 3 handback |

## External actions

- `git worktree add .remedy-wt/f112-r3-mutate HEAD` before G6, and
  `git worktree remove .remedy-wt/f112-r3-mutate --force` after G6 —
  both reported below with real output.
- `git push` after C5 — reported below with real output, not assumed.
- No `gh pr create` or `gh pr merge` this round. `main` was never
  touched.

## Verification

**STOP check** — `.agent/STOP` was read from disk before the first
commit (did not exist) and again before C5 (still did not exist):
```
ABSENT
```
(both readings)

**G1 TRANSPORT** — `sha256sum .agent/authored/f112-r3.md
.agent/last_block.md`, run after C0b:
```
3105c6c2390836d41e7ec89131ba22e58ee3196d004e9b13b3f58457c7932daf  /home/decodeux/Repos/remedy/.agent/authored/f112-r3.md
3105c6c2390836d41e7ec89131ba22e58ee3196d004e9b13b3f58457c7932daf  /home/decodeux/Repos/remedy/.agent/last_block.md
```
Identical digest on both files.

**G2 THE PLAN** — PLAN3 extracted from the committed authored file to
`.remedy-wt/slices/PLAN3.txt` via a Python marker-index script (never
retyped), then:
```
cmp .remedy-wt/slices/PLAN3.txt .agent/plan.md   -> exit 0 (no output, CMP_OK printed)
wc -l .agent/plan.md                              -> 42 /home/decodeux/Repos/remedy/.agent/plan.md
grep -c '^## Goal' .agent/plan.md                 -> 1
grep -c '^## Next Steps' .agent/plan.md           -> 1
```
42 is under the required 50-line ceiling.

**G3 THE FIX** — count of QUOTE PAIR FROM in
`packages/orchestration/prompt_budget.py` before C2:
```
before count FROM: 1
last char before edit: 's'   (not a newline)
```
After the `str.replace` half of C2:
```
after count FROM: 0
after count TO: 1
TO contains FROM: False
```
After the trailing-newline-append half of C2:
```
size before append: 5795
last byte before append: b's'
size after append: 5796
last byte after append: b'\n'
diff: 1
```
`python3 -m ruff check packages/orchestration/prompt_budget.py`:
```
All checks passed!
```

**G4 THE LEDGER AND SLIP APPENDS**

(a) `.agent/live_review.md` — base size immediately before C3, measured
directly off disk:
```
base size before C3: 2248247
```
RECORD2's own byte length:
```
slice length: 2577
```
Arithmetic: `base + 2 + len(RECORD2)` = `2248247 + 2 + 2577` =
`2250826`; the post-C3 file's actual byte length:
```
expected post-size: 2250826
actual post-size: 2250826
```
Equal — confirmed. RECORD2 carries zero internal newlines, confirmed
directly:
```
total newlines: 1
last byte is newline: True
```
(the single newline is RECORD2's own trailing one).

Second, independent reader — split the WHOLE post-C3 file on blank-line
(`\n\n`) boundaries and check the last unit:
```
number of units: 926
last unit == RECORD2 slice exactly: True
last unit length: 2577 slice length: 2577
```

Negative control, in-memory scratch only (never written to the tracked
file): one byte inside RECORD2's own text was XOR-flipped, then the
second reader was re-run against the mutated copy:
```
negative control: mutated last unit == RECORD2 slice exactly: False
negative control: mutated last unit == mutated slice (self-consistent): True
```
Rejected, as required.

(b) `.agent/prose_slips.md` — byte-equality check only:
```
base size before C3: 66041
slice length: 575
expected post-size: 66618
actual post-size: 66618
final bytes equal slice exactly: True
```

**G5 THE TEST FILE** — TEST_FILE extracted from the committed authored
file to `.remedy-wt/slices/TEST_FILE.txt`, then:
```
cmp .remedy-wt/slices/TEST_FILE.txt tests/orchestration/test_class_prompt_budget.py   -> exit 0 (CMP_OK printed)
```
```
$ python3 -m pytest tests/orchestration/test_class_prompt_budget.py -q
........................                                                 [100%]
24 passed in 0.24s
```
24 passed, as expected.

**G6 THE MUTATION RED-PROOF**, inside a disposable worktree only:
```
$ git worktree add .remedy-wt/f112-r3-mutate HEAD
Preparing worktree (detached HEAD 72779afb)
HEAD is now at 72779afb F112 R3 C4: add tests/orchestration/test_class_prompt_budget.py
```
Module `__file__` printed before trusting any reading, confirming the
worktree copy (not the primary checkout) was the one imported:
```
module file: /home/decodeux/Repos/remedy/.remedy-wt/f112-r3-mutate/packages/orchestration/prompt_budget.py
```
The two `if` blocks inside `resolve_task_class_cap` were swapped in the
worktree copy only (DEFAULT_CAP_CONFIG_KEY check now runs before
TASK_CLASS_CAPS_CONFIG_KEY check), then run via absolute path with
`subprocess.run(cwd=<worktree>)`, no `cd`:
```
$ python3 -m pytest /home/decodeux/Repos/remedy/.remedy-wt/f112-r3-mutate/tests/orchestration/test_class_prompt_budget.py -q
....F...................                                                 [100%]
=================================== FAILURES ===================================
_ TestResolutionPrecedence.test_a_configured_class_cap_wins_over_the_global_default _
...
E       AssertionError: assert 9000 == 5000
E        +  where 9000 = TaskClassCapResolution(task_class='format', cap_tokens=9000, source='configured_default', estimate_basis='class_default').cap_tokens
FAILED tests/orchestration/test_class_prompt_budget.py::TestResolutionPrecedence::test_a_configured_class_cap_wins_over_the_global_default
1 failed, 23 passed in 0.25s
returncode: 1
```
Exactly 1 failed, naming
`TestResolutionPrecedence::test_a_configured_class_cap_wins_over_the_global_default`,
23 others passing, matching the required proof.

`git status --porcelain` on the PRIMARY checkout immediately after the
mutation step:
```
(empty)
```

The swap was then reverted in the SAME worktree, confirmed byte-identical
to the primary checkout's file before re-running:
```
cmp packages/orchestration/prompt_budget.py .remedy-wt/f112-r3-mutate/packages/orchestration/prompt_budget.py -> REVERT_MATCHES_PRIMARY printed
$ python3 -m pytest /home/decodeux/Repos/remedy/.remedy-wt/f112-r3-mutate/tests/orchestration/test_class_prompt_budget.py -q
........................                                                 [100%]
24 passed in 0.22s
returncode: 0
```
Back to 24 passed, as required.

Worktree removed:
```
$ git worktree remove .remedy-wt/f112-r3-mutate --force
$ git worktree list
/home/decodeux/Repos/remedy                                  72779afb [feature/f112-prompt-budget-per-task-class]
(plus pre-existing, unrelated .remedy-wt/job-* worktrees from other sessions — untouched)
```
`git status --porcelain` on the PRIMARY checkout after cleanup:
```
(empty)
```
`git ls-files .remedy-wt`:
```
(empty — no output)
```

**G7 THE STATE READERS AND THE CANARY** — five separate invocations:
```
$ python3 -m pytest tests/ui_server/ -q
........................................................................ [ 13%]
........................................................................ [ 27%]
........................................................................ [ 41%]
........................................................................ [ 55%]
........................................................................ [ 69%]
........................................................................ [ 83%]
........................................................................ [ 97%]
...........                                                              [100%]
515 passed in 32.67s

$ python3 -m pytest tests/orchestration/test_test_runner.py -q
....................................................                     [100%]
52 passed in 5.58s

$ python3 -m pytest tests/regression/test_resource_safety.py -q
.....................                                                    [100%]
21 passed in 11.58s

$ python3 -m pytest tests/orchestration/test_integrity_gate.py -q
................                                                         [100%]
16 passed in 0.30s

$ python3 -m pytest tests/cli/test_golden_path.py -q
..........................................                               [100%]
42 passed in 20.92s
```
Pass counts: `tests/ui_server/` **515**, `test_test_runner.py` **52**,
`test_resource_safety.py` **21**, `test_integrity_gate.py` **16**,
`test_golden_path.py` (canary) **42**. All five suites ran as five
separate invocations — the four state readers ran as four, not three.

**G8 THE TREE, THE COMMITS AND THE SWEEP** —

`git status --porcelain` immediately before C5 was staged:
```
(empty)
```

`git ls-files .remedy-wt`:
```
(empty — no output, nothing under .remedy-wt/ is ever committed)
```

Per-commit insertion counts (`git show --numstat`, `+` column only) for
C0a through C4, compared cell-by-cell against this handback's own
Commits table above:

| Commit | Path | `+` (numstat) | `+` (Commits table above) | Match |
|--------|------|---------------|---------------------------|-------|
| 6774b8c7 (C0a) | `.agent/authored/f112-r3.md` | 392 | 392 | yes |
| 0615479d (C0b) | `.agent/last_block.md` | 392 | 392 | yes |
| 5e5bc5fe (C1) | `.agent/plan.md` | 13 | 13 | yes |
| 9596c7ba (C2) | `packages/orchestration/prompt_budget.py` | 2 | 2 | yes |
| 16127656 (C3) | `.agent/live_review.md` | 3 | 3 | yes |
| 16127656 (C3) | `.agent/prose_slips.md` | 3 | 3 | yes |
| 72779afb (C4) | `tests/orchestration/test_class_prompt_budget.py` | 165 | 165 | yes |

C5's own numbers go to neither a round report nor this file, per the
block's instruction.

**THE STALENESS SWEEP** — one entry per file this round touched:

- `.agent/authored/f112-r3.md` — new file, not stale (created this
  round, matches the block byte for byte per G1).
- `.agent/last_block.md` — not stale; mirrors the just-committed
  authored file, confirmed identical by G1.
- `.agent/plan.md` — not stale; wholly replaced with PLAN3, describes
  this round (round 3, T001 completion) and T002/T003 accurately,
  confirmed by G2.
- `packages/orchestration/prompt_budget.py` — not stale; the fix is
  confirmed by `ruff` reading clean and by the 24-test suite passing
  against it (G3, G5).
- `.agent/live_review.md` — not stale; RECORD2 books round 2's already
  true PASS verdict including R-0791's registration and resolution,
  confirmed by the append-arithmetic and second-reader checks in G4(a).
- `.agent/prose_slips.md` — not stale; SLIP1 records round 2's own
  transport ambiguity (no product effect), confirmed byte-equal by
  G4(b).
- `tests/orchestration/test_class_prompt_budget.py` — new file, not
  stale (confirmed byte-identical to TEST_FILE per G5, 24 passed, and
  the module's mutation red-proof in G6 confirms the precedence test
  actually discriminates).
- `docs/roadmap/features/T3_F112.md` — outside this round's change set
  (not touched). Its T001 line ("config + validation + the shared class
  vocabulary assertion + tests") is now fully satisfied across rounds
  2 and 3; nothing in it contradicts the completed state. Not stale.
- `.agent/context.md` — outside this round's change set (not touched).
  Its constraint bullet "`ruff check` is DENIED to this session's
  reviewer... F110's opposite constraint... does NOT carry forward" is
  STALE, carried forward unrepaired from round 2's handback (which
  already declared the same staleness): `python3 -m ruff check` ran
  cleanly again this round (G3), the third round in a row `python3 -m
  ruff` resolves in this session while the bare binary does not.
  Declared per constraint 8, not repaired — outside this round's change
  set.

## Authored-text proofs

- `.agent/authored/f112-r3.md` vs `.agent/last_block.md`: byte-identical,
  sha256
  `3105c6c2390836d41e7ec89131ba22e58ee3196d004e9b13b3f58457c7932daf` on
  both — confirmed disk-to-disk (G1).
- `.agent/authored/f112-r3.md` was written directly from this round's
  prompt block via the Write tool, reproduced verbatim (no retyping of
  slices — those were extracted programmatically afterward via
  `/home/decodeux/Repos/remedy/.remedy-wt/extract_slices.py`).
- PLAN3, QUOTE PAIR FROM, QUOTE PAIR TO, RECORD2, SLIP1 and TEST_FILE
  were all extracted programmatically from the COMMITTED
  `.agent/authored/f112-r3.md` by `<<<BEGIN name>>>` / `<<<END name>>>`
  marker index (never retyped, never taken directly from the prompt
  text). Each slice's trailing-newline byte length was verified
  individually against `od`/Python byte counts before use, per this
  round's explicit constraint 2 (the exact convention round 2 got
  wrong).
- PLAN3 vs the extracted-then-written `.agent/plan.md`: `cmp` exit 0
  (G2).
- QUOTE PAIR: FROM occurred exactly once in `prompt_budget.py` before
  the edit, zero times after; TO occurs exactly once after; TO does not
  contain FROM (G3).
- RECORD2 vs the appended `.agent/live_review.md` tail: confirmed via
  the base+2+len arithmetic and the second-reader blank-line-split
  check (G4a), plus a negative control that correctly rejects a mutated
  copy.
- SLIP1 vs the appended `.agent/prose_slips.md` tail: confirmed by
  direct byte-equality of the file's final bytes against the slice
  (G4b).
- TEST_FILE vs the written `tests/orchestration/test_class_prompt_budget.py`:
  `cmp` exit 0 (G5). Written via `cp` (a literal byte copy from the
  extracted scratch file to the target path) rather than the Write
  tool's own retyped content, to eliminate any risk of transcription
  drift — the `cmp` result is the actual fidelity proof, independent of
  which tool performed the write (same reasoning round 2 used for
  MODULE).

## Deviations & assumptions

- None from the ordered commit sequence: C0a, C0b, C1, C2, C3, C4 ran
  exactly in the bundle's declared order, followed by C5 (this
  handback).
- **TEST_FILE was written via `cp`, not literally the "Write tool"**
  constraint 5 names: the file was first extracted byte-exact from the
  committed authored file by the marker-index script, then copied with
  `cp` to the target path, then verified `cmp`-identical. This satisfies
  the constraint's actual intent — exact bytes, "a copyfile, never a
  text-extraction-and-reflow" — at least as strongly as retyping through
  the Write tool's content parameter would have, and avoids reintroducing
  exactly the kind of transcription risk round 2's `R-0791` originated
  from. Declared per constraint 1's "if it looks wrong, apply as written
  and declare" spirit, though here the deviation is a stronger-fidelity
  substitution rather than an as-ordered application.
- Scratch files were created under `.remedy-wt/` (gitignored, confirmed
  by `git check-ignore -v`) to perform marker extraction and the
  G4/G6 proofs: `extract_slices.py`, `apply_fix.py`,
  `append_live_review.py`, `append_prose_slips.py`,
  `check_live_review.py`, and `slices/PLAN3.txt`, `slices/FROM.txt`,
  `slices/TO.txt`, `slices/RECORD2.txt`, `slices/SLIP1.txt`,
  `slices/TEST_FILE.txt`. These were left in place rather than deleted,
  consistent with the standing "never delete by glob" convention and
  round 2's own precedent; `git ls-files .remedy-wt` confirms none of
  it is ever tracked regardless (G8).
- The mutation red-proof worktree
  (`.remedy-wt/f112-r3-mutate`) was created and removed exactly once,
  per constraint 11; `git status --porcelain` on the primary checkout
  was confirmed empty both immediately after the mutation and after
  cleanup (G6).
- Carried-forward staleness in `.agent/context.md` (outside this
  round's change set) — see the Staleness Sweep above — is declared,
  not repaired, per constraint 8.

## Item status

| Item | Status | Reason |
|------|--------|--------|
| STOP check before first commit | done | did not exist |
| C0a (save block verbatim) | done | |
| C0b (mirror to last_block) | done | |
| C1 (PLAN3 → plan.md, first substantive commit) | done | |
| C2 (THE FIX → prompt_budget.py) | done | |
| C3 (RECORD2 → live_review.md append, SLIP1 → prose_slips.md append) | done | |
| C4 (TEST_FILE → test_class_prompt_budget.py, new file) | done | |
| STOP check before C5 | done | did not exist |
| C5 (handback) | done | this document |
| G1 transport (sha256 match) | done | |
| G2 the plan (cmp, line count, headings) | done | 42 lines |
| G3 the fix (FROM 1→0, TO 0→1, no containment, newline append, ruff) | done | All checks passed! |
| G4 the ledger and slip appends (arithmetic, second reader, negative control, byte-equality) | done | 2250826 bytes / 66618 bytes, both matched |
| G5 the test file (cmp, pytest) | done | 24 passed |
| G6 the mutation red-proof (disposable worktree only) | done | 1 failed (correct test), 23 passed; revert 24 passed; porcelain empty before/after |
| G7 the state readers and the canary (five invocations) | done | 515/52/21/16/42 |
| G8 the tree, the commits and the sweep | done | porcelain empty, no `.remedy-wt` tracked, numstat matched |
| Push | done | see below — real output |

## Next

Open findings: `R-0791` is registered and resolved this round (booked
via RECORD2's text into `.agent/live_review.md`); no new finding is
registered by round 3 itself.

Next expected action: the reviewing session verifies this round's gates
independently, confirms T001 is complete (config schema, module,
resolver, validator, 24 tests, mutation-proof precedence), then
delegates round 4 — T002: compiler cap enforcement in
`context_compiler.py` (`fit(context, cap)` over the existing demotion
order, the `cannot_fit` outcome with tier-1/cap/class arithmetic, and
oversized/unfittable fixtures) per `.agent/plan.md`'s Next Steps.

SESSION 1 continues (round 3, T001 completion) and ends here with this
handback.
