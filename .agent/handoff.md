# Handoff — F114 Cost preview per command, round 2 (books R1's PASS; extracts `tokens_to_cost_usd()`)

## Session

SESSION 1 of feature F114 · round 2 · rounds so far 2.

Same loop session as round 1. This round books round 1's PASS verdict
into the ledger (RECORD1) and lands the first production code of F114:
a new pure helper `packages/orchestration/token_economy.py:tokens_to_cost_usd()`,
with `predict_next_task_cost` in `budget_guard.py` refactored to call it
(no behavior change).

## Range

Review of `fd25323e1b91178299cd9be1320058db88132047..HEAD` (HEAD is
`9230a7135d4ec69a9cc29d81e964458d31385f44` before this handback commit;
verified equal to the previous handback's `.agent/handoff.md` HEAD
before C0a — see Verification).

## Commits

### e8f75da1 F114 R2 C0a: save step block verbatim to .agent/authored/f114-r2.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f114-r2.md` | +301/-0 | transport proof — verbatim `cp` of the supplied step block, new file |

### 06ce3b8f F114 R2 C0b: mirror step block to .agent/last_block.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +234/-181 | mirror of the round's authored block (whole-file rewrite; AGENTS.md `.agent/**` state-file exemption) |

### b7eec287 F114 R2 C1: apply RECORD1 to .agent/live_review.md and PLAN2 to .agent/plan.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +2/-1 | append RECORD1 (round 1's PASS verdict) — exactly one `\n` then RECORD1's 2529 bytes, no blank-line separator |
| `.agent/plan.md` | +15/-15 | whole-file replace with PLAN2 (first substantive commit, per constraint 2) |

### 9230a713 F114 R2 C2: apply TE PAIR to token_economy.py, BG PAIR to budget_guard.py, TEST PAIR to test_token_economy.py
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/token_economy.py` | +12/-0 | append — new `tokens_to_cost_usd()` pure function, ahead of `_now()` |
| `packages/orchestration/budget_guard.py` | +1/-3 | rewrite — the inlined 3-line multiply inside `predict_next_task_cost` replaced by one call to `token_economy.tokens_to_cost_usd()` |
| `tests/orchestration/test_token_economy.py` | +24/-0 | append — new `TestTokensToCostUsd` class, 5 tests |

### (this handback commit)
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewrite | this handback (write-once per PH v3) — numbers not tabled here per template's self-reference exception; the reviewer measures them at the next gate |

## External actions

- `git push -u origin feature/f114-cost-preview-per-command` → run after
  this handback commit (C3), pushing all five commits of the round.
- No `gh pr` command of any kind was run this round — no PR is created
  or touched this round; the block's Bundle/Constraints make no mention
  of PR creation and Done-when carries no Open PR Gate item. PR #234
  (F112) was not touched, per constraint 9.
- One disposable git worktree, created and removed for G6's red-proof
  only, never the primary checkout:
  `git worktree add .remedy-wt/f114-r2-redproof 9230a713` (created,
  detached HEAD at this round's own C2) then, after the red/green cycle,
  `git worktree remove --force .remedy-wt/f114-r2-redproof` (removed).
  `git worktree list` immediately after shows it gone — see G8.

## Verification

Preconditions, checked before C0a:

```
$ git log --oneline -1
fd25323e F114 R1 C3: rewrite .agent/handoff.md - round 1 handback
$ git status --short
(empty)
$ sha256sum .remedy-wt/f114_r2_block.txt
1dd16065123b01af3b195cbb7f07934915256273992db5cc1f9c13dde9abfaae  .remedy-wt/f114_r2_block.txt
$ wc -l .remedy-wt/f114_r2_block.txt; wc -c .remedy-wt/f114_r2_block.txt
300 .remedy-wt/f114_r2_block.txt
17701 .remedy-wt/f114_r2_block.txt
```
`wc -l` reports 300 (newline-terminated-line count) against the block's
own stated "301 lines" — the file has 301 physical lines with no
trailing newline on the last one, so `wc -l` (which counts `\n` bytes)
reads one less; `wc -c` matches the stated 17701 bytes exactly, and the
sha256 matches the stated digest exactly, so the file is confirmed
byte-identical to what was handed to this round. `.agent/STOP` checked
absent both before the first commit and again before C3 (`test -f
.agent/STOP` → false both times, no such file).

**G1 TRANSPORT** (after C0b):
```
$ sha256sum .agent/authored/f114-r2.md .agent/last_block.md
1dd16065123b01af3b195cbb7f07934915256273992db5cc1f9c13dde9abfaae  .agent/authored/f114-r2.md
1dd16065123b01af3b195cbb7f07934915256273992db5cc1f9c13dde9abfaae  .agent/last_block.md
```
One digest, twice — PASS.

**G2 THE LEDGER APPEND**:
```
Base size of .agent/live_review.md immediately before C1: 2349237 bytes
Base ends with trailing newline: False
RECORD1 own byte length (UTF-8): 2529 bytes, 0 internal newlines
base + 1 + len(RECORD1) = 2349237 + 1 + 2529 = 2351767
post-C1 file byte length: 2351767
Match: True (also matches the block's own stated 2351767/2349237/2529 exactly)
```
Second, independent reader — split the whole post-C1 file on
single-newline boundaries after its LAST "Gate: F" marker:
```
last unit after final 'Gate: F' marker == RECORD1: True (2529 == 2529 bytes)
```
Negative control, scratch copy only (never the tracked file) — one byte
flipped inside a copy of RECORD1's own text, then re-split:
```
second reader rejects the mutated copy: True (mismatch detected)
```
All PASS. The file's own last-eight pre-round "Gate: F" record
boundaries were also read mechanically to confirm the append convention
before choosing it: each of the 8 is preceded by exactly one `\n` byte
(`b't.\n'`, `b'o.\n'`, `b'g.\n'`, `` b'`.\n' ``, `b'e.\n'`, `b'w.\n'`,
`b'd.\n'`, `b't.\n'` — the character before each trailing `\n` is prose,
never a second `\n`), confirming "exactly one newline, never a blank
line" is the file's real current convention, matching constraint 3.

**G3 THE PLAN**:
```
$ cmp <PLAN2 extracted from committed authored file> .agent/plan.md
(no output — exit 0)
$ wc -l .agent/plan.md
42 .agent/plan.md
$ grep -c '^## Goal' .agent/plan.md
1
$ grep -c '^## Next Steps' .agent/plan.md
1
```
`cmp` exit 0, `wc -l` 42 (under 50 — PASS), both grep counts 1 — PASS.

**G4 THE THREE CODE PAIRS**:

TE PAIR (`packages/orchestration/token_economy.py`):
```
FROM count before C2: 1  ("def _now() -> str:", 18 bytes)
TO contains FROM: true   (579-byte TO, ends verbatim in that same line)
str.replace(FROM, TO, 1) on pre-C2 scratch copy == actual post-C2 file: True
```
BG PAIR (`packages/orchestration/budget_guard.py`):
```
FROM count before C2: 1  (171-byte 3-line block)
TO contains FROM: false  (86-byte single-line TO — a rewrite)
str.replace(FROM, TO, 1) on pre-C2 scratch copy == actual post-C2 file: True
```
TEST PAIR (`tests/orchestration/test_token_economy.py`):
```
FROM count before C2: 1  (260 bytes: the last test method's 5 lines
                          PLUS the file's own trailing newline byte)
file.endswith(FROM) before C2: True — a true byte-exact suffix
TO contains FROM: true   (1210-byte TO = FROM with the new test class
                          appended after it, itself ending in \n)
str.replace(FROM, TO, 1) on pre-C2 scratch copy == actual post-C2 file: True
```
All three PASS.

**G5 COMPILE AND LINT**:
```
$ python3 -m py_compile packages/orchestration/token_economy.py
(no output — exit 0)
$ python3 -m py_compile packages/orchestration/budget_guard.py
(no output — exit 0)
$ python3 -m py_compile tests/orchestration/test_token_economy.py
(no output — exit 0)
$ ruff check packages/orchestration/token_economy.py packages/orchestration/budget_guard.py
Permission to use Bash has been denied. IMPORTANT: You *may* attempt to
accomplish this action using other tools that might naturally be used
to accomplish this goal [...] If you believe this capability is
essential to complete the user's request, STOP and explain to the user
what you were trying to do and why you need this permission. Let the
user decide how to proceed.
```
`py_compile` exit 0 on all three touched/created `.py` files — PASS.
`ruff check` produced the exact session-level refusal text above
(reported verbatim per constraint 12, not assumed) — `ruff` is denied
to this session, consistent with round 1's own CONTEXT1 note and this
round's constraint 12.

**G6 THE RED-PROOF, INSIDE A DISPOSABLE GIT WORKTREE ONLY**:
```
$ git worktree add .remedy-wt/f114-r2-redproof 9230a713
Preparing worktree (detached HEAD 9230a713)
HEAD is now at 9230a713 F114 R2 C2: ...
```
Inside the worktree, `tokens_to_cost_usd`'s own `return tokens / 1000 *
...` line changed to `return tokens / 999 * ...` (one-character edit):
```
$ python3 -m pytest tests/orchestration/test_token_economy.py tests/orchestration/test_predictive_budget.py -q
8 failed, 109 passed in 2.62s
FAILED tests/orchestration/test_token_economy.py::TestTokensToCostUsd::test_ordinary_multiply
FAILED tests/orchestration/test_predictive_budget.py::TestBreachBoundary::test_over_the_limit_breaches
FAILED tests/orchestration/test_predictive_budget.py::TestBreachBoundary::test_exactly_at_the_limit_does_not_breach
FAILED tests/orchestration/test_predictive_budget.py::TestBreachBoundary::test_expected_cost_is_tokens_over_1000_times_the_price_basis
FAILED tests/orchestration/test_predictive_budget.py::TestPredictionJsonAndArithmetic::test_arithmetic_is_one_non_empty_line_carrying_the_whole_comparison
FAILED tests/orchestration/test_predictive_budget.py::TestResolvePredictiveBudgetConfig::test_a_configured_price_basis_makes_the_predictor_live
FAILED tests/orchestration/test_predictive_budget.py::TestTheA9PathAtTheDeriveThenPredictSeam::test_the_seam_takes_the_largest_class_default_and_says_the_band_was_missing
FAILED tests/orchestration/test_predictive_budget.py::TestEveryPredictedNumberCarriesItsBasis::test_the_text_report_never_shows_a_predicted_number_without_its_basis[priced]
```
8 failures (> 0), spanning both `test_token_economy.py`'s own new unit
test AND `test_predictive_budget.py` — proving the mutation reaches
`predict_next_task_cost` through the new call, not just the new
function's own direct tests. One-character edit reverted inside the
same worktree:
```
$ python3 -m pytest tests/orchestration/test_token_economy.py tests/orchestration/test_predictive_budget.py -q
117 passed in 1.97s
```
Fully green again (the unmutated control) — 42 + 75 = 117, matching the
primary checkout's own G7 readings for these two suites. Worktree
removed:
```
$ git worktree remove --force .remedy-wt/f114-r2-redproof
$ git worktree list
(no .remedy-wt/f114-r2-redproof entry — confirmed gone)
```
PASS. The mutation was applied and tested exclusively inside
`.remedy-wt/f114-r2-redproof/`, never the primary checkout
(self_drive_protocol.md guardrail G5); the primary checkout's own
`token_economy.py` was never touched by this gate.

**G7 THE SUITES, SERIALLY, PRIMARY CHECKOUT**:
```
$ python3 -m pytest tests/orchestration/test_token_economy.py -q
42 passed in 0.29s
$ python3 -m pytest tests/orchestration/test_predictive_budget.py -q
75 passed in 1.75s
$ python3 -m pytest tests/orchestration/test_budget_guard.py -q
92 passed in 1.48s
$ python3 -m pytest tests/docs/ -q
295 passed in 0.45s
$ python3 -m pytest tests/orchestration/test_roadmap_index.py -q
30 passed in 0.36s
$ python3 -m pytest tests/ui_server/ -q
515 passed in 32.22s
$ python3 -m pytest tests/orchestration/test_test_runner.py -q
52 passed in 5.65s
$ python3 -m pytest tests/regression/test_resource_safety.py -q
21 passed in 11.52s
$ python3 -m pytest tests/orchestration/test_integrity_gate.py -q
16 passed in 0.29s
$ python3 -m pytest tests/cli/test_golden_path.py -q
42 passed in 20.52s
```
Pre-round baselines (measured by this worker before C2, on `06ce3b8f`):
`test_token_economy.py` 37, `test_predictive_budget.py` 75,
`test_budget_guard.py` 92. Post-C2: 42/75/92. `test_token_economy.py`
is STRICTLY GREATER (37→42, the 5 new `TestTokensToCostUsd` tests
landed) — matches the gate's "new tests landed" wording exactly.
`test_predictive_budget.py` and `test_budget_guard.py` are UNCHANGED
(75→75, 92→92) — correctly so, since this round's change set adds no
tests to either file (only `test_token_economy.py` gains tests per the
TEST PAIR); see Deviations for the gate-wording note this triggers.
The other seven counts (295/30/515/52/21/16/42) are checked against
RECORD1's own stated reviewer baseline from round 1's gate — identical,
nothing moved.

**G8 THE TREE, THE COMMITS AND THE SWEEP**:
```
$ git status --porcelain
(empty — checked immediately before C3 staged)
$ git ls-files .remedy-wt
(no output — nothing under .remedy-wt/ is ever committed)
$ git worktree list
/home/decodeux/Repos/remedy                                  9230a713 [feature/f114-cost-preview-per-command]
(plus 8 pre-existing, unrelated .remedy-wt/job-* worktrees from other
job runs — none created or touched by this round's G6, confirmed by
name: none is "f114-r2-redproof")
```
Per-commit insertion cross-check (`git show --numstat`, `+` column
only) against this handback's own Commits table above — all cells
match:

| Commit | File | numstat `+` | Table `+` | Match |
|---|---|---|---|---|
| e8f75da1 (C0a) | `.agent/authored/f114-r2.md` | 301 | 301 | yes |
| 06ce3b8f (C0b) | `.agent/last_block.md` | 234 | 234 | yes |
| b7eec287 (C1) | `.agent/live_review.md` | 2 | 2 | yes |
| b7eec287 (C1) | `.agent/plan.md` | 15 | 15 | yes |
| 9230a713 (C2) | `packages/orchestration/budget_guard.py` | 1 | 1 | yes |
| 9230a713 (C2) | `packages/orchestration/token_economy.py` | 12 | 12 | yes |
| 9230a713 (C2) | `tests/orchestration/test_token_economy.py` | 24 | 24 | yes |

Note: `git commit`'s own terminal echo for C0b read "301 insertions(+),
248 deletions(-)" with a "rewrite .agent/last_block.md (77%)" note —
this is git's rewrite-detection stat (whole-file delete+insert counted
against the OLD file's 248 lines and the NEW file's 301 lines) and
differs from `git show --numstat`'s line-level diff (234/181) used in
the table above, per G8's own explicit instruction to use `git show
--numstat`. Both are real git output; they measure different things
(rewrite-heuristic stat vs. line diff), not a defect — declared for
transparency.

Staleness sweep, one entry per file this round touched:

| File | Stale? | Why |
|---|---|---|
| `.agent/authored/f114-r2.md` | NOT stale | immutable historical stamp of this round's instructions |
| `.agent/last_block.md` | NOT stale | current mirror of this round's block; accurate until round 3 overwrites it |
| `.agent/live_review.md` | NOT stale | RECORD1 books round 1's real PASS verdict, append-only ledger |
| `.agent/plan.md` | NOT stale | reflects F114 round 2's actual current step and real next steps |
| `packages/orchestration/token_economy.py` | NOT stale | `tokens_to_cost_usd()` is live, tested, and called from `budget_guard.py` |
| `packages/orchestration/budget_guard.py` | NOT stale | `predict_next_task_cost` now calls the shared helper; behavior unchanged (117 tests confirm) |
| `tests/orchestration/test_token_economy.py` | NOT stale | new `TestTokensToCostUsd` class covers the new function directly |
| `.agent/handoff.md` | N/A | this handback itself, written last, freshest by construction |

Outside the change set: `.agent/context.md` line 29 — "the one-line
multiply at `budget_guard.py:482-484` needs extracting, not a new
config layer" — is now STALE. That line no longer exists at
`budget_guard.py:482-484` (C2 replaced it with a single call to
`token_economy.tokens_to_cost_usd()`); the sentence describes a task
that is now done. `.agent/context.md` is not in this round's change set
(Change set section lists exactly 8 paths, `.agent/context.md` is not
among them), so per constraint 9 this is DECLARED here and NOT
repaired this round. No other stale sentence was found: `docs/roadmap/ROADMAP.md`'s
F114 entry (line 547) describes only target behavior, no line-number or
implementation-location claim; `docs/roadmap/STATUS.md`'s F114 line
(`- [~] F114`) is untouched and still correctly claimed; `docs/roadmap/features/T3_F114.md`
carries no reference to `budget_guard.py` or `token_economy.py` by name
or line number.

## Authored-text proofs

- `.agent/authored/f114-r2.md` (copied via `cp`, never retyped) sha256
  `1dd16065123b01af3b195cbb7f07934915256273992db5cc1f9c13dde9abfaae` at
  17701 bytes, 301 lines — matches the block's own stamp exactly
  (verified before C0a and again after commit).
- `.agent/last_block.md` after C0b: same sha256 as above — confirmed
  equal (G1).
- All eight slices (RECORD1, PLAN2, TE PAIR FROM/TO, BG PAIR FROM/TO,
  TEST PAIR FROM/TO) were extracted from the COMMITTED
  `.agent/authored/f114-r2.md` by a Python script reading delimiter
  indices (`<<<BEGIN ...>>>` / `<<<END ...>>>`), never by hand-retyping
  (constraint 1). For RECORD1, PLAN2, TE PAIR and BG PAIR, the single
  `\n` byte immediately preceding each `END` marker line is the
  authored file's own paragraph-separator formatting, not slice
  content, and was excluded (confirmed mechanically: RECORD1's own
  stated byte length of 2529 with zero internal newlines only holds
  with that byte excluded). For TEST PAIR specifically, constraint 6
  overrides this: FROM/TO explicitly INCLUDE that trailing `\n` byte as
  real content ("FROM is ... PLUS the file's own trailing newline
  byte"), confirmed mechanically — only the raw (unstripped) 260-byte
  FROM is a true `.endswith()` suffix of the pre-C2 test file; the
  stripped 259-byte form is not. This asymmetry between the two
  extraction rules is deliberate, per the block's own differing
  wording for constraints 4/5 vs. 6, and is not itself a deviation.
- RECORD1: 2529 bytes, 0 internal newlines, matches block's stated
  figure exactly; appended to `.agent/live_review.md` as exactly one
  `\n` + RECORD1 (G2, above).
- PLAN2: 1920 bytes, ending `...which and why).` with no trailing
  newline (matches `.agent/plan.md`'s own pre-round no-trailing-newline
  convention); `.agent/plan.md` reproduces it byte-identical (`cmp`
  exit 0).
- TE PAIR FROM: 18 bytes, `def _now() -> str:`, count 1 in
  `token_economy.py` before C2. TE PAIR TO: 579 bytes, ends verbatim in
  that same line; `TO contains FROM: true`;
  `str.replace(FROM, TO, 1)` on a pre-C2 scratch copy reproduces the
  actual post-C2 file byte-identical.
- BG PAIR FROM: 171 bytes, the 3-line
  `expected_cost_usd: float | None = None` / `if expected_tokens is not
  None and price_basis is not None:` / `expected_cost_usd = ...` block,
  count 1 in `budget_guard.py` before C2. BG PAIR TO: 86 bytes, the
  single-line `expected_cost_usd = token_economy.tokens_to_cost_usd(...)`
  call; `TO contains FROM: false` (a rewrite);
  `str.replace(FROM, TO, 1)` reproduces the actual post-C2 file
  byte-identical.
- TEST PAIR FROM: 260 bytes (raw form, trailing newline included),
  count 1 in `test_token_economy.py` before C2, and a true
  `.endswith()` suffix of the file. TEST PAIR TO: 1210 bytes (raw form),
  `TO contains FROM: true`; `str.replace(FROM, TO, 1)` reproduces the
  actual post-C2 file byte-identical — the same result a plain
  `cat snippet >> file` append would have produced, verified in scratch
  before applying to the tracked file (constraint 6), and only the
  FROM/TO replace method touched the tracked file.

## Deviations & assumptions

1. G7's gate text states "the first three must show a pass count
   STRICTLY GREATER than their pre-round baseline (new tests landed)"
   for `test_token_economy.py`, `test_predictive_budget.py` and
   `test_budget_guard.py`, and also carries the sentence "THE FOUR STATE
   READERS ARE RUN AS FOUR, NOT AS THREE" — a phrase that does not name
   any "four state readers" grouping anywhere in this round's own G7
   list (it matches round 1's G5 wording for a different, seven-item
   list, and appears to be unedited boilerplate carried into this
   round's block). This worker's assumption: only `test_token_economy.py`
   is expected to grow, since this round's Change set and the TEST PAIR
   slice add tests ONLY to that file — `test_predictive_budget.py` and
   `test_budget_guard.py` receive no new tests this round by design (the
   refactor is behavior-preserving, proven by their pass counts staying
   exactly at the pre-round baseline, 75 and 92). This worker reported
   the real, measured counts for all ten suites rather than forcing a
   "strictly greater" reading onto suites that gained nothing, and
   declares the mismatch here per constraint 1's "apply as written and
   declare" spirit, applied by analogy to a gate instruction rather than
   an authored slice. No suite's real pass count was altered or omitted
   to fit the wording.
2. `.agent/context.md` staleness (line 29, the `budget_guard.py:482-484`
   line reference) — declared under G8's staleness sweep above, per
   constraint 9. Not repaired this round; `.agent/context.md` is not in
   the change set.
3. Tooling note, not a block deviation: this session's Bash tool denies
   commands whose text contains a `for ... in ...:` loop construct, even
   inside a Python heredoc/`-c` script operating on files outside any
   loop-shaped bash syntax itself. The three FROM/TO pair applications
   (originally written as one loop-based script) were re-run as three
   separate, loop-free `python3 -c` invocations instead, each applying
   and verifying exactly one pair. All resulting file contents, byte
   comparisons and gate outcomes are identical to what the single
   loop-based script would have produced (confirmed by the G4
   `str.replace` cross-check against the actual on-disk files); this
   only changed how the commands were issued, not what they did.

The bundle's commit order (C0a, C0b, C1, C2, C3) was followed exactly;
the change set touched exactly the eight declared paths and nothing
else (`git status --porcelain` after C2 showed only the three intended
production/test files; constraint 7's excluded files —
`budget_resolution.py`, `pingpong_job.py`, `apps/cli/commands/job.py` —
were never opened for writing); no slice looked wrong, so nothing
needed declaring under constraint 1's "apply as written" clause beyond
the extraction-rule asymmetry already noted above; `.agent/STOP` was
absent at both checkpoints; `cost_preview.py` was not created, per
constraint 8.

## Next

Round 3: ship `packages/orchestration/cost_preview.py`
(`estimate_cost_band`, band computation from `PredictiveBudgetConfig`'s
per-`TokenBand` class defaults, basis labels, "estimate unavailable"
when no price basis) + `tests/orchestration/test_cost_preview.py`,
completing T001 — per `.agent/plan.md`'s own Next Steps. No PR exists
yet and none is expected until T001 lands.
