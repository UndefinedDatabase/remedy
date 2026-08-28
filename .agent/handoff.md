# Handback — F037 R11

## Session

SESSION 3 of feature F037 · round 11 · rounds so far 11

## Range

Review of `dc938d0e`..`HEAD` (branch `feature/f037-rendered-diff-viewer`).

## Commits

### b64a34f5 docs(agent): save the F037 R11 step block
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f037-r11.md` | +326 | C0a: the block file's bytes saved verbatim |

### b99748e9 docs(agent): mirror the F037 R11 block into last_block
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +227/−202 | C0b: mirror; one git blob with the saved copy |

### ab94c844 docs(agent): point the plan at the F037 R11 corpus round
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +18/−20 | C1: PLANF037R11 applied byte for byte |

### 25c46e8f docs(agent): book the R10 gate verdict and register R-0721
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +4 | C2: appends GATER10 then FIND0721; nothing resolved |

### 6cc09705 test(orchestration): add the huge-diff corpus shape and record its budget
| Path | +/- | Reason |
|---|---|---|
| `tests/orchestration/test_diff_parser.py` | +194 | C3: SPEC S1–S6; `import time` plus one new section, additions only |

### C4 (this commit) docs(agent): hand back F037 R11
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewrite | C4: this handback; a handoff cannot table the commit that writes it |

## External actions

- `git worktree add .remedy-wt/f037-r11-g6 6cc09705` — exit 0.
- `git worktree remove .remedy-wt/f037-r11-g6` — exit 0; `git worktree prune` exit 0.
- `git worktree add .remedy-wt/f037-r11-base dc938d0e` — exit 0 (G7 base wall-clock).
- `git worktree remove .remedy-wt/f037-r11-base` — exit 0; `git worktree prune` exit 0.
- `gh pr list --state open --json number,headRefName,baseRefName,isDraft` — exit 0, stdout `[]`.
- `git push` of `feature/f037-rendered-diff-viewer` after this commit.
- No PR created, nothing merged.

## Verification

**G1 hygiene.** `.agent/STOP` read from disk before C0a: DOES NOT EXIST. Read again
before C4: DOES NOT EXIST. `git rev-parse HEAD` before C0a =
`dc938d0e2faa11c84fc1da459e967cc0bc655c82`, which EQUALS the block's base.
`git branch --show-current` = `feature/f037-rendered-diff-viewer`.
`git status --porcelain` line count after C0a 0, after C0b 0, after C1 0, after C2 0,
after C3 0.

**G2 transport, one digest comparison.** `git rev-parse HEAD:.agent/authored/f037-r11.md`
= `9cf846287e22e52a6596f23d92b5630a07712626`; `git rev-parse HEAD:.agent/last_block.md`
= `9cf846287e22e52a6596f23d92b5630a07712626`; SAME BLOB HASH: True. Working copy of
`.agent/authored/f037-r11.md`: sha256
`d44846216a9cf57accbb7575308622452d020fe1244838c50ad4b59ac9b1a242`, 26435 bytes,
326 lines — identical to the sha256 measured on the block file at
`.remedy-wt/f037-r11-block.md` before C0a. THE CHAIN COVERS: the saved copy and its
mirror. It does not certify how the block's bytes reached that scratch path.

**G3 extraction and caps** — measured on the COMMITTED C0a blob, no figure carried
from the block's prose.

| Slice | content lines |
|---|---|
| PLANF037R11 | 46 |
| GATER10 | 1 |
| FIND0721 | 1 |
| CONTENT | 48 |
| TOTAL | 326 |
| PROSE = TOTAL − CONTENT | 278 |

TOTAL at most 490: True. PROSE at most 400: True.

**G4 the plan at C1.** `.agent/plan.md` byte-equal to PLANF037R11 including the
trailing newline: True. NEGATIVE CONTROL against the slice minus its trailing
newline: False. Lines exactly `## Goal`: 1. Lines exactly `## Next Steps`: 1.
`wc -l` = 46; STRICTLY under 50: True.

**G5 the record at C2.**

| Append | before (bytes) | after (bytes) | reader (a) byte identity | reader (b) N units in order | NEGATIVE CONTROL (a)/(b) |
|---|---|---|---|---|---|
| GATER10 | 1185228 | 1189883 | True | True, N=1 | False / False |
| FIND0721 | 1189883 | 1193281 | True | True, N=1 | False / False |

Reader (a) is `result == before + b"\n" + slice` re-read from disk. The negative
control flips ONE byte inside the first appended paragraph; both readers come back
False for both appends. The pre-round blob of `.agent/live_review.md` is a byte
PREFIX of the result: True.

Line-anchored counts over `.agent/live_review.md` after C2: `^- R-\d+ — ` 282;
`^Done: R-\d+ — ` 29; `^Landed: R-` 1; `^Gate: F\d+ R\d+ — ` 81. Open set size 253.
Every registered id distinct: True. `R-0721` occurs exactly once as a registration:
True. `R-0721` occurs ZERO times as a resolution (`Done:` + `Landed:`): True — it is
registered OPEN, as constraint 6 orders.

**G6 the corpus round's red-proofs.** All runs inside the disposable worktree
`.remedy-wt/f037-r11-g6` at the C3 tree; `__pycache__` purged and `python3 -B` used
before EVERY run; the parser restored between runs and each restore verified
byte-identical against sha256
`35d29f7f47ab8d52b5c142ff829f7eb48f081f6e9c7478855bc7fffdc7433944`.

UNMUTATED CONTROL — `python3 -B -m pytest tests/orchestration/test_diff_parser.py -q`:
exit 0, `32 passed in 0.72s`.

Mutation (a), a cap on parsed body lines. Exact string replaced:
`                hunk["lines"].append(\n`; occurrences in the file BEFORE the edit: 1.
Guard inserted immediately before it at that statement's own indentation, skipping the
append once the hunk holds 100 lines. REAL exit code 1, summary `3 failed, 29 passed in 0.32s`.
Node ids that FAIL as measured:
`tests/orchestration/test_diff_parser.py::test_the_huge_single_file_diff_parses_to_one_complete_file`,
`::test_line_numbering_survives_the_whole_huge_file`,
`::test_the_huge_diff_parses_inside_the_recorded_perf_budget`. Restore byte-identical: True.

Mutation (b), a cap on file regions. Exact string replaced:
`        regions.append(current)\n`; occurrences BEFORE the edit: 1. Replaced with the
same append guarded by `len(regions) < 10`. REAL exit code 1, summary
`1 failed, 31 passed in 0.59s`. Node id that FAILS as measured:
`tests/orchestration/test_diff_parser.py::test_the_many_file_diff_keeps_every_file_distinct_and_in_input_order`.
Restore byte-identical: True. THE ORDERED PROPERTY — the colour — holds: both RED.

THIRD READING, the blindness control (not ordered; run in the same disposable
worktree, primary checkout never mutated). With the BASE corpus checked out from
`dc938d0e` into that worktree: unmutated exit 0 `28 passed in 0.29s`; with mutation
(a) exit 0 `28 passed in 0.24s`; with mutation (b) exit 0 `28 passed in 0.24s`. Both
truncations are therefore INVISIBLE to the twenty-eight pre-existing tests and are
seen only by the four C3 adds. The worktree's test file and parser were restored
byte-identically and its index reset before removal; `git status --porcelain` in the
worktree read 0 lines at removal.

Afterwards: `git worktree remove` exit 0, `git worktree prune` exit 0,
`git worktree list` line count 1, `git status --porcelain` in the primary checkout
0 lines.

**G7 suite, lint and canary at C3.** One pytest process at a time throughout.

- `python3 -m pytest tests/orchestration/test_diff_parser.py tests/orchestration/test_diff_view_source.py -q`
  — exit 0, `41 passed in 0.60s`. Lines matching `^FAILED`: 0.
  EXTRACTOR-BLINDNESS CONTROL: the same counter over a control string that does begin
  with `FAILED` returns 2, so the 0 above is a measurement.
- `python3 -m pytest tests/orchestration/test_diff_parser.py --collect-only -q` — exit 0,
  `32 tests collected in 0.04s`; node id COUNT 32. The four node ids C3 added
  (derived from collect-only output against the base file's `def test_` set, never
  from `-v` output):
  `tests/orchestration/test_diff_parser.py::test_the_huge_single_file_diff_parses_to_one_complete_file`,
  `::test_line_numbering_survives_the_whole_huge_file`,
  `::test_the_many_file_diff_keeps_every_file_distinct_and_in_input_order`,
  `::test_the_huge_diff_parses_inside_the_recorded_perf_budget`.
- `python3 -m ruff check tests/orchestration/test_diff_parser.py` (repository
  configuration, no `--isolated`) — exit 0, `All checks passed!`.
- Canary `python3 -m pytest tests/cli/test_golden_path.py -q` — exit 0,
  `42 passed in 20.61s`. Base figure `42 passed`; measured `42 passed`; NO DIFFERENCE.
- WALL-CLOCK COST C3 ADDS: parser suite at the base commit `dc938d0e` (measured in a
  disposable worktree) `28 passed in 0.24s`; at C3 `32 passed in 0.57s`. Difference
  +0.33 s, of which the budget test's own timed parse is about 0.105 s and the three
  structural tests parse the 10k-line and 400-file fixtures once each. The suite is
  still well under a second; the whole parser+view_source pair runs in 0.60 s.

**Recorded perf figures S5 booked (read these instead of re-deriving them).** On this
host — Linux x86-64 development workstation, CPython 3, unloaded — the parser is
LINEAR at roughly 10 microseconds per body line: 1000 body lines 0.010 s, 2000 body
lines 0.021 s, 10000 body lines 0.105 s (median of fifteen parses; min 0.1034, max
0.1107). The 400-file shape parses in 0.011 s and a 200-file shape in 0.0055 s, so
the many-files dimension is linear too. `HUGE_DIFF_PARSE_CEILING_SECONDS` is 0.5 s.

**G8 structure, artifacts and the Open PR Gate at C3.**
`git diff --name-only dc938d0e..6cc09705` returns exactly:
`.agent/authored/f037-r11.md`, `.agent/last_block.md`, `.agent/live_review.md`,
`.agent/plan.md`, `tests/orchestration/test_diff_parser.py`.
RESIDUE actual minus expected: `[]`. RESIDUE expected minus actual: `[]`.
`git diff --stat` restricted to `packages/`: EMPTY — this is the reading that proves
constraint 3. Restricted to `docs/`: EMPTY. Restricted to `apps/`: EMPTY. Restricted
to `tests/`: only `tests/orchestration/test_diff_parser.py | 194 ++++`.

| Commit | insertions | under 500 | parents |
|---|---|---|---|
| C0a b64a34f5 | 326 | True | 1 |
| C0b b99748e9 | 227 | True | 1 |
| C1 ab94c844 | 18 | True | 1 |
| C2 25c46e8f | 4 | True | 1 |
| C3 6cc09705 | 194 | True | 1 |

Marker sweep: `.agent/plan.md` at C1 — `^<<<SLICE ` 0, `^<<<END ` 0.
`.agent/live_review.md` at C2 — `^<<<SLICE ` 0, `^<<<END ` 0. The SAME counter over
the C0a blob — `^<<<SLICE ` 3, `^<<<END ` 3, both greater than zero, so the zeros
above are a measurement and not a blind counter.
`git ls-files .remedy-wt` line count: 0.
Open PR Gate, verbatim: `gh pr list --state open --json number,headRefName,baseRefName,isDraft`
exit 0, stdout `[]` — no open PRs. Nothing merged, nothing created.

## Authored-text proofs

- `.agent/authored/f037-r11.md` vs the reviewer's scratch original
  `.remedy-wt/f037-r11-block.md`: sha256 equal
  (`d44846216a9cf57accbb7575308622452d020fe1244838c50ad4b59ac9b1a242`), 26435 bytes,
  326 lines. Not edited in transit.
- `.agent/plan.md` vs the PLANF037R11 slice extracted from the COMMITTED C0a blob:
  byte-equal True, trailing-newline negative control False.
- `.agent/live_review.md` vs GATER10 and FIND0721 extracted from the same blob:
  byte identity True for both appends, negative controls False.

## Deviations & assumptions

1. **The perf ceiling is five times the measured figure, not ten.** SPEC S5 says the
   ceiling is set "roughly an order of magnitude above" the measured figure AND that
   it must separate linear from quadratic cost. At this fixture size the two clauses
   collide: the measured median is 0.105 s and the most conservative quadratic
   estimate — a parser scaling as N squared while matching today's cost at 1000 body
   lines — is 100 × 0.010 s ≈ 1.0 s, which is exactly where a ten-times ceiling would
   land. A 1.0 s ceiling would therefore pass BOTH cases and record nothing. I applied
   the purpose clause and set `HUGE_DIFF_PARSE_CEILING_SECONDS = 0.5` — about 4.8×
   the measurement, so a runner five times slower still passes (constraint 9 requires
   three), and 2× below the quadratic figure. The reasoning, both figures and the
   "do not tighten below about 0.35 s" note are in the test's docstring.
2. **The block's own measured figure for a 10k-line parse (0.363 s, in FIND0721) does
   not reproduce here; I measured 0.105 s.** FIND0721 was applied BYTE FOR BYTE and is
   unchanged — the slice wins, and the finding's substance (linear cost, no ceiling)
   is confirmed by my own measurements. The gap is a different generated fixture, not
   a disagreement about the parser: FIND0721's shape produced 10001 parsed line
   objects from 10004 input lines (mostly additions), mine produces 10000 from 10005
   as alternating pairs, which is a different intraline-pairing load. Declared here
   because the round is the one that RECORDS the budget and the next reader will find
   two numbers.
3. **One unordered extra measurement.** The G6 "third reading" — both mutations run
   against the BASE corpus at `dc938d0e` — is not in the block's gate list. It ran
   inside the same disposable worktree, mutated nothing in the primary checkout, and
   is what proves the two mutations are discriminators for C3's tests rather than for
   the existing twenty-eight.
4. **No departure from the ordered commit sequence.** C0a, C0b, C1, C2, C3, C4 in that
   order, one commit each, no extra commit, none dropped, none reordered.
5. **Scratch scripts.** Three throwaway measurement scripts were written under the
   gitignored `.remedy-wt/` and removed by exact path after use; `git ls-files
   .remedy-wt` reads 0.

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a save the block | done | |
| C0b mirror into last_block | done | one blob with the saved copy |
| C1 the plan | done | byte-equal to PLANF037R11 |
| C2 the R10 verdict and R-0721 | done | registered OPEN; nothing resolved |
| C3 the huge-diff corpus shape | done | SPEC S1–S6; 4 tests; both red-proofs RED |
| C4 the handback | done | this file |
| G1 hygiene | PASS | exit codes and readings above |
| G2 transport | PASS | one blob, sha256 matches the scratch original |
| G3 extraction and caps | PASS | TOTAL 326 ≤ 490, PROSE 278 ≤ 400 |
| G4 the plan | PASS | byte-equal, 46 lines, control False |
| G5 the record | PASS | both readers True, both controls False, prefix True |
| G6 red-proofs | PASS | control exit 0; (a) exit 1, (b) exit 1 |
| G7 suite, lint, canary | PASS | exits 0/0/0/0; canary 42 passed, unchanged |
| G8 structure and Open PR Gate | PASS | both residues empty; `packages/` diff EMPTY |
| R-0721 | registered | OPEN; R12 carries the repair |

## Next

Review this round at `dc938d0e..HEAD`, then order R12: the parser enforces a ceiling
on parsed body lines itself and sets the contract's `truncated` flag when it bites,
with the ceiling ABOVE the 10 000-line fixture Acceptance names so that fixture still
renders in full. That is a behaviour change under `packages/` and earns red-proofs of
its own. Phase 1 rule 1 first: re-read `.agent/STOP` from disk before authoring.
