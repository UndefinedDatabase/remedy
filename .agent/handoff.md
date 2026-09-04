# Handoff — F114 Cost preview per command, round 4 (books R3's PASS; starts T002 — config key + resolve_confirm_above_usd())

## Session

SESSION 1 of feature F114 · round 4 · rounds so far 4.

Same loop session as rounds 1-3. This round books round 3's PASS verdict
into the ledger (RECORD3) and starts T002: registers config key
`cost_preview.confirm_above_usd` (default 0.5, F114 Design: "around half
a dollar") in `packages/orchestration/config.py`, and adds resolver
`resolve_confirm_above_usd()` (env > TOML > default, same authority as
`resolve_predictive_budget_config`) to `cost_preview.py` itself. No CLI
file touched this round — that lands in round 5, per constraint 8. 6 new
tests land in `tests/orchestration/test_cost_preview.py` (19 passed
total: 13 existing + 6 new).

## Range

Review of `8b296131eff88cbdbe13bd47b839c95f5c4490d6..HEAD` (HEAD is
`6978e949ece539b59e635ed899b23d557422fa3c` before this handback commit).

## Item Status

| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | this handback |
| G1 TRANSPORT | done | PASS |
| G2 THE LEDGER APPEND | done | PASS |
| G3 THE PLAN | done | PASS |
| G4 THE FOUR CODE PAIRS | done | PASS |
| G5 COMPILE AND LINT | done | PASS (ruff denied, as expected) |
| G6 THE RED-PROOF | done | PASS (1 failed / 19 green) |
| G7 THE SUITES | done | PASS (all 13 measured) |
| G8 THE TREE, THE COMMITS AND THE SWEEP | done | PASS |

## Commits

### 8bb227b8 F114 R4 C0a: save step block verbatim to .agent/authored/f114-r4.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f114-r4.md` | +388/-0 | transport proof — verbatim `cp` of the supplied step block, new file |

### db8c8e73 F114 R4 C0b: mirror block to .agent/last_block.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +264/-271 | mirror of the round's authored block (whole-file rewrite; AGENTS.md `.agent/**` state-file exemption) |

### 4d46e293 F114 R4 C1: append RECORD3 to live_review.md, replace plan.md with PLAN4
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +2/-1 | append RECORD3 (round 3's PASS verdict) — exactly one `\n` then RECORD3's 4490 bytes, no blank-line separator |
| `.agent/plan.md` | +16/-16 | whole-file replace with PLAN4 (first substantive commit, per constraint 2) |

### 6978e949 F114 R4 C2: register cost_preview.confirm_above_usd config key and resolve_confirm_above_usd()
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/config.py` | +10/-0 | CONFIG PAIR append — new `ConfigKeySpec` for `cost_preview.confirm_above_usd` |
| `packages/orchestration/cost_preview.py` | +41/-0 | IMPORT PAIR (rewrite, `Path` import) + APPEND PAIR (append, `DEFAULT_CONFIRM_ABOVE_USD` + `resolve_confirm_above_usd()`), applied in that order per constraint 7 |
| `tests/orchestration/test_cost_preview.py` | +49/-0 | TEST PAIR append — `TestResolveConfirmAboveUsd`, 6 new tests |

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
  `git worktree add .remedy-wt/f114-r4-redproof 6978e949` (created,
  detached HEAD at this round's own C2) then, after the red/green cycle,
  `git worktree remove --force .remedy-wt/f114-r4-redproof` (removed).
  `git worktree list` immediately after shows it gone — see G8.

## Verification

Preconditions, checked before C0a:

```
$ git log --oneline -1
8b296131 F114 R3 C3: rewrite .agent/handoff.md - round 3 handback
$ git status --short
(empty)
$ sha256sum .remedy-wt/f114_r4_block.txt
c0b99055ee4cb5f5b7c65d83240ba2339c829dfb12e5fd22c2d2a18713957b5b  .remedy-wt/f114_r4_block.txt
$ wc -l .remedy-wt/f114_r4_block.txt; wc -c .remedy-wt/f114_r4_block.txt
387 .remedy-wt/f114_r4_block.txt
23167 .remedy-wt/f114_r4_block.txt
```
`wc -l` reports 387 (newline-terminated-line count) against the round
instructions' own stated "388 lines" — the file has 388 physical lines
with no trailing newline on the last one, so `wc -l` (which counts `\n`
bytes) reads one less; `wc -c` matches the stated 23167 bytes exactly,
and the sha256 matches the stated digest exactly — same pattern rounds
2 and 3 both hit. `.agent/STOP` checked absent both before the first
commit and again before C3 (`test -f .agent/STOP` → false both times, no
such file).

**G1 TRANSPORT** (after C0b):
```
$ sha256sum .agent/authored/f114-r4.md .agent/last_block.md
c0b99055ee4cb5f5b7c65d83240ba2339c829dfb12e5fd22c2d2a18713957b5b  .agent/authored/f114-r4.md
c0b99055ee4cb5f5b7c65d83240ba2339c829dfb12e5fd22c2d2a18713957b5b  .agent/last_block.md
```
One digest, twice — PASS.

**G2 THE LEDGER APPEND**:
```
Base size of .agent/live_review.md immediately before C1: 2355786 bytes
Base ends with trailing newline: False
RECORD3 own byte length (extracted from committed authored file): 4490 bytes, 0 internal newlines
base + 1 + len(RECORD3) = 2355786 + 1 + 4490 = 2360277
post-C1 file byte length: 2360277
Match: True (also matches the round instructions' own stated 2360277/2355786/4490 exactly)
```
Second, independent reader — sliced the post-C1 file's bytes from the
measured `base` offset (2355786) to end-of-file and compared against
`"\n" + RECORD3` directly:
```
tail (base..end) == "\n" + RECORD3: True
```
Negative control, scratch copy only (never the tracked file) — one byte
flipped inside a Python `bytearray` copy of RECORD3's own text (byte at
offset 0, XORed with 0xFF), then re-compared against the real post-C1
tail:
```
second reader REJECTS the mutated copy: True (tail != "\n" + mutated)
```
All PASS.

**G3 THE PLAN**:
```
$ cmp <PLAN4 extracted from committed authored file> .agent/plan.md
(no output — exit 0)
$ wc -l .agent/plan.md
39 .agent/plan.md
$ grep -c '^## Goal' .agent/plan.md
1
$ grep -c '^## Next Steps' .agent/plan.md
1
```
`cmp` exit 0, `wc -l` 39 (under 50 — PASS), both grep counts 1 — PASS.

**G4 THE FOUR CODE PAIRS**:

Unlike round 3, this round's constraint 4 stated each slice's newline
convention explicitly, so no ambiguity needed resolving: IMPORT PAIR
FROM/TO carry no trailing newline in either (bare 2-3 line snippets);
APPEND PAIR FROM/TO and TEST PAIR FROM/TO each carry the target file's
own real trailing newline (extracted slice text + one `\n`, confirmed a
suffix via `.endswith()` before applying); CONFIG PAIR FROM/TO carry no
trailing newline of their own (a mid-file entry, immediately followed by
the next entry on the next line).

Pre-C2 FROM counts (immediately before C2, from the actual pre-round
file contents):
```
IMPORT PAIR FROM count in cost_preview.py (before edits): 1
APPEND PAIR FROM count in cost_preview.py (before edits): 1
CONFIG PAIR FROM count in config.py: 1
TEST PAIR FROM count in test_cost_preview.py: 1
```
All exactly 1 — PASS. `APPEND PAIR FROM is suffix of cost_preview.py:
True` and `TEST PAIR FROM is suffix of test_cost_preview.py: True`,
confirmed via `.endswith()` before either was applied.

Applied IMPORT PAIR first (constraint 7 — its FROM is nearer the top,
unaffected by APPEND PAIR's own tail edit), then re-counted APPEND PAIR
FROM in the post-IMPORT-PAIR content before applying it:
```
APPEND PAIR FROM count in cost_preview.py (after IMPORT PAIR, before APPEND PAIR): 1
```
Containment checks, matching constraints 5/6 exactly:
```
IMPORT PAIR: TO contains FROM: false   (a rewrite)
APPEND PAIR: TO contains FROM: true    (an append)
CONFIG PAIR: TO contains FROM: true    (an append)
TEST PAIR:   TO contains FROM: true    (an append)
```

Byte-exact reconstruction, INDEPENDENT of the write path — each target's
pre-C2 content read via `git show HEAD:<path>` (the C1 commit, before
C2 touched anything), the same FROM/TO pairs applied in the
constraint-7 order to a scratch in-memory copy, then compared against
the actual post-C2 file on disk:
```
cost_preview.py scratch == actual: True
config.py scratch == actual: True
test_cost_preview.py scratch == actual: True
```
All three exit-0-equivalent (`True`) — PASS.

**G5 COMPILE AND LINT**:
```
$ python3 -m py_compile packages/orchestration/cost_preview.py packages/orchestration/config.py tests/orchestration/test_cost_preview.py
(no output — exit 0)
$ ruff check packages/orchestration/cost_preview.py packages/orchestration/config.py
Permission to use Bash has been denied. IMPORTANT: You *may* attempt to
accomplish this action using other tools that might naturally be used
to accomplish this goal [...] If you believe this capability is
essential to complete the user's request, STOP and explain to the user
what you were trying to do and why you need this permission. Let the
user decide how to proceed.
```
`py_compile` exit 0 on all three touched/created `.py` files — PASS.
`ruff check` produced the exact session-level refusal text above
(reported verbatim per constraint 9, not assumed) — `ruff` is denied to
this session, consistent with rounds 1-3's own notes.

**G6 THE RED-PROOF, INSIDE A DISPOSABLE GIT WORKTREE ONLY**:
```
$ git worktree add .remedy-wt/f114-r4-redproof 6978e949
Preparing worktree (detached HEAD 6978e949)
HEAD is now at 6978e949 F114 R4 C2: ...
```
Inside the worktree, `resolve_confirm_above_usd`'s own `if value > 0:`
line (line 127) changed to `if value >= 0:` — allowing a configured
zero through instead of falling back to the default:
```
$ python3 -m pytest tests/orchestration/test_cost_preview.py -q
1 failed, 18 passed in 0.26s
FAILED tests/orchestration/test_cost_preview.py::TestResolveConfirmAboveUsd::test_zero_configured_value_falls_back_to_default
```
1 failure (> 0) —
`TestResolveConfirmAboveUsd::test_zero_configured_value_falls_back_to_default`
(asserted `resolve_confirm_above_usd(config_path=str(toml)) ==
DEFAULT_CONFIRM_ABOVE_USD` with a configured `confirm_above_usd = 0`,
got `0.0` instead of `0.5` since the mutated `>= 0` now lets the
configured zero through) — proving the zero-falls-back-to-default
branch is real, reachable code, not dead, despite having no CLI caller
yet (constraint 8). Edit reverted inside the same worktree:
```
$ python3 -m pytest tests/orchestration/test_cost_preview.py -q
19 passed in 0.23s
```
Fully green again (the unmutated control) — 19 passed, matching the
primary checkout's own G7 reading for this suite. Worktree removed:
```
$ git worktree remove --force .remedy-wt/f114-r4-redproof
$ git worktree list
(no .remedy-wt/f114-r4-redproof entry — confirmed gone)
```
PASS. The mutation was applied and tested exclusively inside
`.remedy-wt/f114-r4-redproof/`, never the primary checkout
(self_drive_protocol.md guardrail G5); the primary checkout's own
`cost_preview.py` was never touched by this gate.

**G7 THE SUITES, SERIALLY, PRIMARY CHECKOUT**:
```
$ python3 -m pytest tests/orchestration/test_cost_preview.py -q
19 passed in 0.24s
$ python3 -m pytest tests/orchestration/test_config.py -q
81 passed in 0.30s
$ python3 -m pytest tests/test_no_interactive_guard.py -q
6 passed in 1.19s
$ python3 -m pytest tests/orchestration/test_predictive_budget.py -q
75 passed in 2.13s
$ python3 -m pytest tests/orchestration/test_budget_guard.py -q
92 passed in 1.60s
$ python3 -m pytest tests/orchestration/test_token_economy.py -q
42 passed in 0.28s
$ python3 -m pytest tests/docs/ -q
295 passed in 0.45s
$ python3 -m pytest tests/orchestration/test_roadmap_index.py -q
30 passed in 0.36s
$ python3 -m pytest tests/ui_server/ -q
515 passed in 32.44s
$ python3 -m pytest tests/orchestration/test_test_runner.py -q
52 passed in 5.66s
$ python3 -m pytest tests/regression/test_resource_safety.py -q
21 passed in 11.36s
$ python3 -m pytest tests/orchestration/test_integrity_gate.py -q
16 passed in 0.28s
$ python3 -m pytest tests/cli/test_golden_path.py -q
42 passed in 20.66s
```
`test_cost_preview.py` reads 19 passed (13 existing + 6 new) — matches
the gate's stated expectation exactly. `test_config.py` reads 81 passed
— together with `test_cost_preview.py`'s 19, this is 100 passed
combined across the two files, matching the round instructions' own
statement that the reviewer's independent dry run measured "100 passed
across test_cost_preview.py and test_config.py combined" exactly. Every
other count (6/75/92/42/295/30/515/52/21/16/42) is a moved-count check
against round 3's own stated reviewer-verified baseline — all IDENTICAL
to round 3's own figures, nothing moved outside this round's own change
set. These are the REAL, measured counts, not forced to any assumption.
`tests/ui_server/`, `test_test_runner.py`, `test_resource_safety.py`
and `test_integrity_gate.py` were run as all four named, not fewer, per
the gate's own instruction.

**G8 THE TREE, THE COMMITS AND THE SWEEP**:
```
$ git status --porcelain
(empty — checked immediately before C3 staged)
$ git ls-files .remedy-wt
(no output — nothing under .remedy-wt/ is ever committed)
$ git worktree list
/home/decodeux/Repos/remedy                                  6978e949 [feature/f114-cost-preview-per-command]
(plus 8 pre-existing, unrelated .remedy-wt/job-* worktrees from other
job runs — none created or touched by this round's G6, confirmed by
name: none is "f114-r4-redproof")
```
Per-commit insertion cross-check (`git show --numstat`, `+` column
only) against this handback's own Commits table above — all cells
match:

| Commit | File | numstat `+` | Table `+` | Match |
|---|---|---|---|---|
| 8bb227b8 (C0a) | `.agent/authored/f114-r4.md` | 388 | 388 | yes |
| db8c8e73 (C0b) | `.agent/last_block.md` | 264 | 264 | yes |
| 4d46e293 (C1) | `.agent/live_review.md` | 2 | 2 | yes |
| 4d46e293 (C1) | `.agent/plan.md` | 16 | 16 | yes |
| 6978e949 (C2) | `packages/orchestration/config.py` | 10 | 10 | yes |
| 6978e949 (C2) | `packages/orchestration/cost_preview.py` | 41 | 41 | yes |
| 6978e949 (C2) | `tests/orchestration/test_cost_preview.py` | 49 | 49 | yes |

C3's own numbers go to neither this table nor a round report, per G8's
own instruction.

Staleness sweep, one entry per file this round touched:

| File | Stale? | Why |
|---|---|---|
| `.agent/authored/f114-r4.md` | NOT stale | immutable historical stamp of this round's instructions |
| `.agent/last_block.md` | NOT stale | current mirror of this round's block; accurate until round 5 overwrites it |
| `.agent/live_review.md` | NOT stale | RECORD3 books round 3's real PASS verdict, append-only ledger |
| `.agent/plan.md` | NOT stale | reflects F114 round 4's actual current step and real next steps |
| `packages/orchestration/config.py` | NOT stale | the new `cost_preview.confirm_above_usd` key is live and read by `resolve_confirm_above_usd()` |
| `packages/orchestration/cost_preview.py` | NOT stale | `DEFAULT_CONFIRM_ABOVE_USD`/`resolve_confirm_above_usd()` are live and tested; no CLI caller yet, by design (T002 completes in round 5, per constraint 8) |
| `tests/orchestration/test_cost_preview.py` | NOT stale | 6 new tests directly cover the new resolver, all passing, 19 total |
| `.agent/handoff.md` | N/A | this handback itself, written last, freshest by construction |

Outside the change set: no NEW stale sentence was found this round.
`.agent/context.md` line 36 ("No `cost_preview.py` or expensive-command
registry exists today...") and line 29 (the `budget_guard.py:482-484`
reference) — round 2's and round 3's own declared staleness — both
stand unrepeated, per constraint 10's explicit instruction not to
repeat them. `docs/roadmap/features/T3_F114.md` line 29 already names
`confirm_above_usd (config, default around half a dollar)` as an
expected design item — this round fulfills part of that design rather
than contradicting it, so no new staleness there.
`docs/roadmap/STATUS.md`'s F114 line (`- [~] F114`) is untouched and
still correctly claimed (in progress).

## Authored-text proofs

- `.agent/authored/f114-r4.md` (copied via `cp`, never retyped) sha256
  `c0b99055ee4cb5f5b7c65d83240ba2339c829dfb12e5fd22c2d2a18713957b5b` at
  23167 bytes, 388 lines — matches the round instructions' own stamp
  exactly (verified before C0a and again after commit, via `cmp` against
  the scratch source at `.remedy-wt/f114_r4_block.txt`).
- `.agent/last_block.md` after C0b: same sha256 as above — confirmed
  equal (G1).
- All ten slices (RECORD3, PLAN4, IMPORT PAIR FROM/TO, APPEND PAIR
  FROM/TO, CONFIG PAIR FROM/TO, TEST PAIR FROM/TO) were extracted from
  the COMMITTED `.agent/authored/f114-r4.md` by a Python script
  (`.remedy-wt/extract_slices.py`) reading delimiter indices
  (`<<<BEGIN ...>>>` / `<<<END ...>>>`), splitting the file on `\n`
  bytes and re-joining the lines strictly between each pair of markers
  — never by hand-retyping (constraint 1). The naive marker-to-marker
  join carries no trailing newline for any slice by construction; per
  constraint 4's explicit statement (not left implicit this round, in
  contrast with round 3), one trailing `\n` was added back onto APPEND
  PAIR FROM/TO and TEST PAIR FROM/TO only — both real source-file tails
  — and confirmed a byte-exact suffix of their respective target files
  via `.endswith()` before either was applied; IMPORT PAIR and CONFIG
  PAIR took the extracted bytes as-is, no addition.
- RECORD3: 4490 bytes, 0 internal newlines, matches the round
  instructions' own stated figure exactly; appended to
  `.agent/live_review.md` as exactly one `\n` + RECORD3 (G2, above).
- PLAN4: 1738 bytes, no trailing newline (matches `.agent/plan.md`'s own
  pre-round no-trailing-newline convention); `.agent/plan.md` reproduces
  it byte-identical (`cmp` exit 0).
- IMPORT PAIR FROM (63 bytes) / TO (88 bytes): both no trailing newline,
  matched the pre-round `cost_preview.py`'s own import block exactly
  once, and IMPORT PAIR's TO does not contain FROM as a substring
  (rewrite), confirmed.
- APPEND PAIR FROM (80 bytes raw + 1 restored `\n` = 81 bytes applied) /
  TO (1599 bytes raw + 1 restored `\n` = 1600 bytes applied): FROM
  confirmed a byte-exact suffix of the pre-round `cost_preview.py`
  before applying; `packages/orchestration/cost_preview.py` reproduces
  the combined IMPORT+APPEND result byte-identical to an independent
  `git show HEAD:...`-based scratch reconstruction (G4, above).
- CONFIG PAIR FROM (317 bytes) / TO (670 bytes): neither carries a
  trailing newline of its own, matched the pre-round `config.py`'s
  `budget.class_default_tokens_high` entry exactly once;
  `packages/orchestration/config.py` reproduces the result
  byte-identical to the independent scratch reconstruction.
- TEST PAIR FROM (288 bytes raw + 1 restored `\n` = 289 bytes applied) /
  TO (2634 bytes raw + 1 restored `\n` = 2635 bytes applied): FROM
  confirmed a byte-exact suffix of the pre-round
  `tests/orchestration/test_cost_preview.py`;
  `tests/orchestration/test_cost_preview.py` reproduces the result
  byte-identical to the independent scratch reconstruction.

## Deviations & assumptions

None. Constraint 4 stated each slice's newline convention explicitly
this round (in contrast with round 3, where the same class of
convention had to be reverse-engineered from the block's own stated
byte counts); this round applied the stated convention directly and it
reproduced every stated/measured number exactly (RECORD3's 4490 bytes,
the G2 arithmetic, and the G4 byte-exact reconstructions), so no
ambiguity needed resolving or declaring. The bundle's commit order
(C0a, C0b, C1, C2, C3) was followed exactly; the change set touched
exactly the eight declared paths and nothing else (`apps/cli/` and
`command_catalog.py` were never opened for writing, per constraint 8);
no slice's content looked wrong, so nothing needed declaring under
constraint 1's "apply as written... declare" clause; `.agent/STOP` was
absent at both checkpoints; `resolve_confirm_above_usd()` has zero CLI
callers, exactly as constraint 8 expects at this stage — G6's red-proof
is what proves the code is real despite that, not a "dead code" defect.

## Next

Round 5 completes T002: the actual CLI confirm helper, a new shared
module `apps/cli/cost_preview_confirm.py` — the render+confirm helper,
tty/non-tty semantics (pipe never hangs), `--yes` audited — reusing
`loop_cmd.py`'s `_confirm_materialization`/`_stdin_is_a_tty` shape,
calling this round's `resolve_confirm_above_usd()` and
`estimate_cost_band()`. Its own tests land in
`tests/cli/test_cost_preview_confirm.py`. No PR exists yet and none is
expected until T002 (or later) lands enough of the feature to warrant
one.
