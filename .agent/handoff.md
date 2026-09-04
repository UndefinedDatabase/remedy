# Handoff — F114 Cost preview per command, round 3 (books R2's PASS; ships cost_preview.py + its tests, completes T001)

## Session

SESSION 1 of feature F114 · round 3 · rounds so far 3.

Same loop session as rounds 1 and 2. This round books round 2's PASS
verdict into the ledger (RECORD2) and completes T001: a new pure module
`packages/orchestration/cost_preview.py` (`estimate_cost_band`,
`CostBandEstimate`, `ESTIMATE_UNAVAILABLE`) that computes a real USD
cost band — never a fabricated point — from two `TokenBand` values, a
repeat count and a `PredictiveBudgetConfig`, reusing round 2's
`token_economy.tokens_to_cost_usd()`. Its unit tests land in
`tests/orchestration/test_cost_preview.py` (13 passed, brand new file).
Neither file has any production caller yet — that is T002, not started.

## Range

Review of `80d469c26d927bf16294edd83efd6d058f90f014..HEAD` (HEAD is
`539b291dc4e4edff683608843133483233e7a865` before this handback commit;
verified equal to the previous handback's own HEAD before C0a — see
Verification).

## Commits

### 6b7d394c F114 R3 C0a: save step block verbatim to .agent/authored/f114-r3.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f114-r3.md` | +395/-0 | transport proof — verbatim `cp` of the supplied step block, new file |

### 1fb5c49a F114 R3 C0b: mirror step block to .agent/last_block.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +293/-199 | mirror of the round's authored block (whole-file rewrite; AGENTS.md `.agent/**` state-file exemption) |

### 63622705 F114 R3 C1: apply RECORD2 to .agent/live_review.md and PLAN3 to .agent/plan.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +2/-1 | append RECORD2 (round 2's PASS verdict) — exactly one `\n` then RECORD2's 4018 bytes, no blank-line separator |
| `.agent/plan.md` | +16/-19 | whole-file replace with PLAN3 (first substantive commit, per constraint 2) |

### 539b291d F114 R3 C2: write packages/orchestration/cost_preview.py and tests/orchestration/test_cost_preview.py
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/cost_preview.py` | +88/-0 | new file — `estimate_cost_band`, `CostBandEstimate`, `ESTIMATE_UNAVAILABLE`, written whole-file per MODULE, verified `cmp` against the extracted slice |
| `tests/orchestration/test_cost_preview.py` | +104/-0 | new file — 13 tests across 6 classes covering `estimate_cost_band`, written whole-file per TESTMODULE, verified `cmp` against the extracted slice |

### (this handback commit)
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewrite | this handback (write-once per PH v3) — numbers not tabled here per template's self-reference exception; the reviewer measures them at the next gate |

## External actions

- `git push -u origin feature/f114-cost-preview-per-command` → run after
  this handback commit (C3), pushing all five commits of the round.
- No `gh pr` command of any kind was run this round — no PR is created
  or touched this round; the block's Bundle/Constraints make no mention
  of PR creation and Done-when carries no Open PR Gate item.
- One disposable git worktree, created and removed for G6's red-proof
  only, never the primary checkout:
  `git worktree add .remedy-wt/f114-r3-redproof 539b291d` (created,
  detached HEAD at this round's own C2) then, after the red/green cycle,
  `git worktree remove --force .remedy-wt/f114-r3-redproof` (removed).
  `git worktree list` immediately after shows it gone — see G8.

## Verification

Preconditions, checked before C0a:

```
$ git log --oneline -1
80d469c2 F114 R2 C3: rewrite .agent/handoff.md - round 2 handback
$ git status --short
(empty)
$ sha256sum .remedy-wt/f114_r3_block.txt
8fee890a26670158becee84733669803e416a781f7e21273fa12d19a337cc740  .remedy-wt/f114_r3_block.txt
$ wc -l .remedy-wt/f114_r3_block.txt; wc -c .remedy-wt/f114_r3_block.txt
394 .remedy-wt/f114_r3_block.txt
22523 .remedy-wt/f114_r3_block.txt
```
`wc -l` reports 394 (newline-terminated-line count) against the block's
own stated "395 lines" — the file has 395 physical lines with no
trailing newline on the last one, so `wc -l` (which counts `\n` bytes)
reads one less; `wc -c` matches the stated 22523 bytes exactly, and the
sha256 matches the stated digest exactly, so the file is confirmed
byte-identical to what was handed to this round (same pattern as round
2's own precondition read). `.agent/STOP` checked absent both before
the first commit and again before C3 (`test -f .agent/STOP` → false
both times, no such file).

**G1 TRANSPORT** (after C0b):
```
$ sha256sum .agent/authored/f114-r3.md .agent/last_block.md
8fee890a26670158becee84733669803e416a781f7e21273fa12d19a337cc740  .agent/authored/f114-r3.md
8fee890a26670158becee84733669803e416a781f7e21273fa12d19a337cc740  .agent/last_block.md
```
One digest, twice — PASS.

**G2 THE LEDGER APPEND**:
```
Base size of .agent/live_review.md immediately before C1: 2351767 bytes
Base ends with trailing newline: False
RECORD2 own byte length (extracted from committed authored file): 4018 bytes, 0 internal newlines
base + 1 + len(RECORD2) = 2351767 + 1 + 4018 = 2355786
post-C1 file byte length: 2355786
Match: True (also matches the block's own stated 2355786/2351767/4018 exactly)
```
Second, independent reader — sliced the post-C1 file's bytes from the
measured `base` offset (2351767) to end-of-file and compared against
`"\n" + RECORD2` directly:
```
tail (base..end) == "\n" + RECORD2: True (4019 == 4019 bytes)
```
Negative control, scratch copy only (never the tracked file) — one byte
flipped inside a Python `bytearray` copy of RECORD2's own text (byte at
offset 100, XORed), then re-compared against the real post-C1 tail:
```
second reader REJECTS the mutated copy: True (tail != "\n" + mutated)
```
All PASS.

**G3 THE PLAN**:
```
$ cmp <PLAN3 extracted from committed authored file> .agent/plan.md
(no output — exit 0)
$ wc -l .agent/plan.md
39 .agent/plan.md
$ grep -c '^## Goal' .agent/plan.md
1
$ grep -c '^## Next Steps' .agent/plan.md
1
```
`cmp` exit 0, `wc -l` 39 (under 50 — PASS), both grep counts 1 — PASS.

**G4 THE TWO NEW FILES**:
```
$ cmp <MODULE extracted from committed authored file> packages/orchestration/cost_preview.py
(no output — exit 0)
$ cmp <TESTMODULE extracted from committed authored file> tests/orchestration/test_cost_preview.py
(no output — exit 0)
$ wc -c packages/orchestration/cost_preview.py tests/orchestration/test_cost_preview.py
3414 packages/orchestration/cost_preview.py
4614 tests/orchestration/test_cost_preview.py
```
MODULE 3414 bytes, TESTMODULE 4614 bytes — both match the block's own
stated expected byte lengths exactly, recomputed independently. Both
`cmp` exit 0 — PASS. (Extraction note: the naive delimiter-slice — text
strictly between the BEGIN/END marker lines, joined without a trailing
`\n` — measured 3413/4613, one byte short of the stated 3414/4614 in
each case; the file's own real trailing newline, structurally consumed
as the line-separator immediately before each `<<<END ...>>>` marker
line, was restored for MODULE and TESTMODULE only — both are real
source files that end with `\n` by ordinary convention — while RECORD2
(4018 bytes, matching its own stated size with no addition) and PLAN3
(no trailing newline, matching `.agent/plan.md`'s own pre-round
no-trailing-newline convention, confirmed by reading the base file's
own last byte before this round touched it) took none. This
per-slice rule was confirmed by recomputing all four against the
block's own stated/implied byte counts, not assumed uniformly — see
Authored-text proofs below for the full derivation.)

**G5 COMPILE AND LINT**:
```
$ python3 -m py_compile packages/orchestration/cost_preview.py
(no output — exit 0)
$ python3 -m py_compile tests/orchestration/test_cost_preview.py
(no output — exit 0)
$ ruff check packages/orchestration/cost_preview.py tests/orchestration/test_cost_preview.py
Permission to use Bash has been denied. IMPORTANT: You *may* attempt to
accomplish this action using other tools that might naturally be used
to accomplish this goal [...] If you believe this capability is
essential to complete the user's request, STOP and explain to the user
what you were trying to do and why you need this permission. Let the
user decide how to proceed.
```
`py_compile` exit 0 on both new `.py` files — PASS. `ruff check`
produced the exact session-level refusal text above (reported verbatim
per constraint 7, not assumed) — `ruff` is denied to this session,
consistent with rounds 1 and 2's own notes.

**G6 THE RED-PROOF, INSIDE A DISPOSABLE GIT WORKTREE ONLY**:
```
$ git worktree add .remedy-wt/f114-r3-redproof 539b291d
Preparing worktree (detached HEAD 539b291d)
HEAD is now at 539b291d F114 R3 C2: ...
```
Inside the worktree, `cost_preview.py`'s own final line changed from
`return CostBandEstimate(min(usd_a, usd_b), max(usd_a, usd_b), basis,
inputs)` to `return CostBandEstimate(max(usd_a, usd_b), max(usd_a,
usd_b), basis, inputs)` — both bounds now `max`:
```
$ python3 -m pytest tests/orchestration/test_cost_preview.py -q
1 failed, 12 passed in 0.25s
FAILED tests/orchestration/test_cost_preview.py::TestSpanningBand::test_low_and_high_span_produces_a_real_range
```
1 failure (> 0) — `TestSpanningBand::test_low_and_high_span_produces_a_real_range`
(asserted `e.band_usd_low == pytest.approx(0.16)`, got `2.4` since the
mutated `min→max` collapsed both bounds to the higher figure) —
proving the low/high band computation is real, reachable code, not
dead. Edit reverted inside the same worktree:
```
$ python3 -m pytest tests/orchestration/test_cost_preview.py -q
13 passed in 0.22s
```
Fully green again (the unmutated control) — 13 passed, matching the
primary checkout's own G7 reading for this new suite; the reverted
worktree file was also confirmed byte-identical to the primary
checkout's `cost_preview.py` via `cmp` before the worktree was removed.
Worktree removed:
```
$ git worktree remove --force .remedy-wt/f114-r3-redproof
$ git worktree list
(no .remedy-wt/f114-r3-redproof entry — confirmed gone)
```
PASS. The mutation was applied and tested exclusively inside
`.remedy-wt/f114-r3-redproof/`, never the primary checkout
(self_drive_protocol.md guardrail G5); the primary checkout's own
`cost_preview.py` was never touched by this gate.

**G7 THE SUITES, SERIALLY, PRIMARY CHECKOUT**:
```
$ python3 -m pytest tests/orchestration/test_cost_preview.py -q
13 passed in 0.23s
$ python3 -m pytest tests/test_no_interactive_guard.py -q
6 passed in 1.17s
$ python3 -m pytest tests/orchestration/test_predictive_budget.py -q
75 passed in 2.13s
$ python3 -m pytest tests/orchestration/test_budget_guard.py -q
92 passed in 1.62s
$ python3 -m pytest tests/orchestration/test_token_economy.py -q
42 passed in 0.28s
$ python3 -m pytest tests/docs/ -q
295 passed in 0.44s
$ python3 -m pytest tests/orchestration/test_roadmap_index.py -q
30 passed in 0.36s
$ python3 -m pytest tests/ui_server/ -q
515 passed in 32.59s
$ python3 -m pytest tests/orchestration/test_test_runner.py -q
52 passed in 5.56s
$ python3 -m pytest tests/regression/test_resource_safety.py -q
21 passed in 11.53s
$ python3 -m pytest tests/orchestration/test_integrity_gate.py -q
16 passed in 0.28s
$ python3 -m pytest tests/cli/test_golden_path.py -q
42 passed in 20.67s
```
`test_cost_preview.py` reads 13 passed — matches the gate's stated
expectation for a brand new file exactly. Every other count
(6/75/92/42/295/30/515/52/21/16/42) is checked against round 2's own
stated reviewer-verified baseline: `test_no_interactive_guard.py` is
newly added to this round's suite list (not present in round 2's G7)
so it carries no prior baseline to compare against — reported as
measured, 6 passed, all real (this module scans production packages,
including the new `cost_preview.py`, for interactive-input calls and
found none, consistent with the module's own docstring claim of
purity). `test_predictive_budget.py` (75), `test_budget_guard.py` (92),
`test_token_economy.py` (42), `tests/docs/` (295),
`test_roadmap_index.py` (30), `tests/ui_server/` (515),
`test_test_runner.py` (52), `test_resource_safety.py` (21),
`test_integrity_gate.py` (16) and `test_golden_path.py` (canary, 42)
are ALL IDENTICAL to round 2's own stated reviewer-verified figures —
nothing moved outside this round's own change set. These are the
REAL, measured counts, not forced to any assumption.

**G8 THE TREE, THE COMMITS AND THE SWEEP**:
```
$ git status --porcelain
(empty — checked immediately before C3 staged)
$ git ls-files .remedy-wt
(no output — nothing under .remedy-wt/ is ever committed)
$ git worktree list
/home/decodeux/Repos/remedy                                  539b291d [feature/f114-cost-preview-per-command]
(plus 8 pre-existing, unrelated .remedy-wt/job-* worktrees from other
job runs — none created or touched by this round's G6, confirmed by
name: none is "f114-r3-redproof")
```
Per-commit insertion cross-check (`git show --numstat`, `+` column
only) against this handback's own Commits table above — all cells
match:

| Commit | File | numstat `+` | Table `+` | Match |
|---|---|---|---|---|
| 6b7d394c (C0a) | `.agent/authored/f114-r3.md` | 395 | 395 | yes |
| 1fb5c49a (C0b) | `.agent/last_block.md` | 293 | 293 | yes |
| 63622705 (C1) | `.agent/live_review.md` | 2 | 2 | yes |
| 63622705 (C1) | `.agent/plan.md` | 16 | 16 | yes |
| 539b291d (C2) | `packages/orchestration/cost_preview.py` | 88 | 88 | yes |
| 539b291d (C2) | `tests/orchestration/test_cost_preview.py` | 104 | 104 | yes |

Note: `git commit`'s own terminal echo for C0b read "395 insertions(+),
301 deletions(-)" with a "rewrite .agent/last_block.md (75%)" note —
this is git's rewrite-detection stat (whole-file delete+insert counted
against the OLD file's 301 lines and the NEW file's 395 lines) and
differs from `git show --numstat`'s line-level diff (293/199) used in
the table above, per G8's own explicit instruction to use `git show
--numstat`. Both are real git output; they measure different things
(rewrite-heuristic stat vs. line diff), not a defect — same pattern
round 2's own handback declared, reproduced again this round.

Staleness sweep, one entry per file this round touched:

| File | Stale? | Why |
|---|---|---|
| `.agent/authored/f114-r3.md` | NOT stale | immutable historical stamp of this round's instructions |
| `.agent/last_block.md` | NOT stale | current mirror of this round's block; accurate until round 4 overwrites it |
| `.agent/live_review.md` | NOT stale | RECORD2 books round 2's real PASS verdict, append-only ledger |
| `.agent/plan.md` | NOT stale | reflects F114 round 3's actual current step and real next steps |
| `packages/orchestration/cost_preview.py` | NOT stale | `estimate_cost_band`/`CostBandEstimate`/`ESTIMATE_UNAVAILABLE` are live and tested; no caller yet, by design (T002) |
| `tests/orchestration/test_cost_preview.py` | NOT stale | 13 tests directly cover the new module, all passing |
| `.agent/handoff.md` | N/A | this handback itself, written last, freshest by construction |

Outside the change set: `.agent/context.md` line 36 — "No
`cost_preview.py` or expensive-command registry exists today
(confirmed by search); T001/T003 are new files, not refactors of
existing ones" — is now PARTIALLY STALE. `packages/orchestration/cost_preview.py`
now exists as of this round's C2; the "no `cost_preview.py`" clause no
longer holds (the "no expensive-command registry" clause and the
"T001/T003 are new files" framing both still hold — T001 is now
complete but was indeed a new file, not a refactor, and T003's registry
still does not exist). `.agent/context.md` is not in this round's
change set (Change set section lists exactly 7 paths, `.agent/context.md`
is not among them), so per constraint 8 this is DECLARED here and NOT
repaired this round. Round 2's own separate `.agent/context.md` line 29
declaration (the `budget_guard.py:482-484` reference) stands unrepeated,
per this round's own constraint 8 instruction. No other new stale
sentence was found: `docs/roadmap/features/T3_F114.md`'s "Design
(suggested shape)" section (line 25, `estimate(command_context) →
{band_usd_low, band_usd_high, basis, inputs}`) is explicitly labelled
SUGGESTED, not a factual claim of what was built, and PLAN3's own Risks
section already documents that this round's real shape
(`estimate_cost_band(band_a, band_b, *, repeat_count, config)`)
deviates deliberately — not a staleness, a declared design choice; the
file's "Suggested tests: tests/cli/test_cost_preview.py" line (line 66,
under "Do not touch") refers to T002's future CLI-level tests, a
different, not-yet-built layer, not this round's
`tests/orchestration/test_cost_preview.py` (T001's own package-level
unit tests) — no conflict. `docs/roadmap/STATUS.md`'s F114 line
(`- [~] F114`) is untouched and still correctly claimed (in progress).

## Authored-text proofs

- `.agent/authored/f114-r3.md` (copied via `cp`, never retyped) sha256
  `8fee890a26670158becee84733669803e416a781f7e21273fa12d19a337cc740` at
  22523 bytes, 395 lines — matches the block's own stamp exactly
  (verified before C0a and again after commit).
- `.agent/last_block.md` after C0b: same sha256 as above — confirmed
  equal (G1).
- All four slices (RECORD2, PLAN3, MODULE, TESTMODULE) were extracted
  from the COMMITTED `.agent/authored/f114-r3.md` by a Python script
  (`.remedy-wt/extract_slices.py`) reading delimiter indices
  (`<<<BEGIN ...>>>` / `<<<END ...>>>`), splitting the file on `\n`
  bytes and re-joining the lines strictly between each pair of markers
  — never by hand-retyping (constraint 1).
- This naive join-without-trailing-newline extraction reproduced RECORD2
  exactly at its own stated 4018 bytes (0 internal newlines) and PLAN3
  at 1740 bytes with no trailing newline (matching `.agent/plan.md`'s
  own pre-round last-byte convention, confirmed by reading the base
  file directly: `d.endswith(b'\n')` → `False`) — both taken as-is, no
  adjustment. For MODULE and TESTMODULE it undershot the block's own
  stated expected byte counts (3414/4614) by exactly one byte each
  (3413/4613): both are real Python source files whose own trailing
  `\n` was structurally consumed as the line-separator immediately
  before their respective `<<<END ...>>>` marker line (no blank line
  separates the last content line from the marker in the raw block —
  confirmed by reading the raw file directly around both boundaries),
  so that one byte was restored for these two slices only, bringing
  them to the stated 3414/4614 exactly. This is a recomputation against
  the block's own explicitly stated expected values (G4), not an
  assumption — the same per-slice-nature judgment round 2's own
  handback made for its TEST PAIR FROM ("raw form, trailing newline
  included") versus its TE/BG PAIR FROM (stripped).
- RECORD2: 4018 bytes, 0 internal newlines, matches block's stated
  figure exactly; appended to `.agent/live_review.md` as exactly one
  `\n` + RECORD2 (G2, above).
- PLAN3: 1740 bytes, ending `...not a rewrite.` with no trailing
  newline (matches `.agent/plan.md`'s own pre-round no-trailing-newline
  convention); `.agent/plan.md` reproduces it byte-identical (`cmp`
  exit 0).
- MODULE: 3414 bytes (trailing `\n` restored per the above), ending
  `...basis, inputs)\n`; `packages/orchestration/cost_preview.py`
  reproduces it byte-identical (`cmp` exit 0), written whole-file with
  the Write tool (a copyfile, never a text-extraction-and-reflow).
- TESTMODULE: 4614 bytes (trailing `\n` restored per the above), ending
  `...repeat_count": 2}\n`; `tests/orchestration/test_cost_preview.py`
  reproduces it byte-identical (`cmp` exit 0), written whole-file with
  the Write tool.

## Deviations & assumptions

1. G4's extraction: as detailed in Verification and Authored-text
   proofs above, a naive marker-to-marker join (no synthetic bytes
   added or removed beyond the markers themselves) undershot the
   block's own explicitly stated MODULE/TESTMODULE byte counts by
   exactly one byte each. This worker's assumption, confirmed by
   recomputing against the block's own stated figures rather than
   guessed: the structural `\n` immediately preceding each of these two
   slices' own `<<<END ...>>>` marker is the real file's own trailing
   newline (ordinary convention for a `.py` source file), not pure
   marker-line formatting, and belongs in the slice — while the same
   structural `\n` before `<<<END RECORD2>>>` and `<<<END PLAN3>>>`
   does NOT, since RECORD2 is stated to have zero internal newlines
   (a single-line ledger record) and PLAN3 matches `.agent/plan.md`'s
   own pre-round no-trailing-newline file convention. Both readings
   were verified against the block's own numbers/conventions, not
   assumed uniformly; nothing was retyped by hand. Declared per
   constraint 1's "apply as written... declare" spirit — the
   convention was not, in fact, wrong, just non-uniform across the four
   slices, and is fully reconciled by the numbers above.
2. `.agent/context.md` staleness (line 36, the "no `cost_preview.py`
   exists" clause, now partially false) — declared under G8's
   staleness sweep above, per constraint 8. Not repaired this round;
   `.agent/context.md` is not in the change set. Round 2's own separate
   line-29 declaration was correctly NOT repeated, per this round's
   explicit constraint 8 instruction.
3. Tooling note, not a block deviation: this session's Bash tool has
   previously (round 2) rejected `for`/loop-shaped constructs even
   inside a Python `-c` string. This round's slice extraction and both
   file writes were done via a standalone Python script file
   (`.remedy-wt/extract_slices.py`, executed with `python3 -B`) and the
   Write tool directly, rather than inline loop-shaped one-liners, so
   this quirk was not encountered and did not need working around this
   round. Noted for completeness only.

The bundle's commit order (C0a, C0b, C1, C2, C3) was followed exactly;
the change set touched exactly the seven declared paths and nothing
else (`git status --porcelain` after C2 showed only the two intended
new production/test files; constraint 6's excluded files —
`token_economy.py`, `budget_guard.py`, `budget_resolution.py` — were
never opened for writing); no slice's CONTENT looked wrong, so nothing
needed declaring under constraint 1's "apply as written" clause beyond
the extraction-byte-count reconciliation already noted above; `.agent/STOP`
was absent at both checkpoints; no production caller of `cost_preview.py`
was added anywhere, per constraint 5 (T002, not this round).

## Next

T002: the CLI helper in `apps/cli` — threshold confirm, tty/non-tty
semantics (pipe never hangs), `--yes` audited, reusing
`loop_cmd.py`'s `_confirm_materialization`/`_stdin_is_a_tty` pattern,
calling `cost_preview.estimate_cost_band()` for the shown numbers — per
`.agent/plan.md`'s own Next Steps. No PR exists yet and none is
expected until T002 (or later) lands enough of the feature to warrant
one.
