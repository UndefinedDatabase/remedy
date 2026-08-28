# Handback — F256 Diff viewer completion, round 8 (THE RECORDED MEASUREMENT)

## Session

SESSION 2 of feature F256 · round 8 · rounds so far 8

## Range

Review of b8a918a1..HEAD (branch `feature/f256-diff-viewer-completion`).

## Commits

### 8569ef20 chore(f256): save the round 8 block
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f256-r8.md` | +322 / -0 | C0a: the block copied byte for byte from `.remedy-wt/f256-r8-block.md` |

### 3f21db4b chore(f256): mirror the round 8 block
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +226 / -324 | C0b: written from the COMMITTED C0a blob, so the two are one blob id |

### 21cc5157 docs(f256): advance the plan to the recorded measurement round
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +14 / -18 | C1: whole-file replacement by the `PLANF256R8` slice |

### cb2f3ce1 docs(f256): book the round 7 verdict and its prose slip
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +12 / -0 | C2: append of the `GATEF256R7` slice |
| `.agent/prose_slips.md` | +2 / -0 | C2: append of the `SLIPF256R7` slice, one dated line |

### f6d5d064 docs(f256): record the measured Built State in the feature file
| Path | +/- | Reason |
|---|---|---|
| `docs/roadmap/features/T5_F256.md` | +87 / -0 | C3: append of the `BUILTF256` slice; no existing line changed |

### C4 (this commit) chore(f256): hand back round 8
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewrite | C4: this handback; a handoff cannot table the commit that writes it |

Every `+/-` cell above was taken from `git diff --numstat <sha>^ <sha>` and agrees
cell for cell with the figures G1 reports below.

## External actions

- `gh pr list --state open --json number,headRefName` → `[]` (constraint 0; no PR
  created, none merged).
- `git push -u origin feature/f256-diff-viewer-completion` after C4 — outcome
  recorded in the round report; no PR create, no merge, no force-push, no rebase.
- No `git worktree add` and no `git worktree remove`: constraint 5 orders no
  destructive verification this round, because the round ships no code.

## Verification

STOP sentinel, both ordered reads with `os.path.exists`:
`/home/decodeux/Repos/remedy/.agent/STOP` — before C0a: `False`; before C3: `False`.

`git rev-parse HEAD` before C0a = `b8a918a16b1e3b2491f13fa333e1cc76014131e3`,
which is the ordered base `b8a918a1`. `git branch --show-current` =
`feature/f256-diff-viewer-completion`. `git status --porcelain | wc -l` = 0 after
each of C0a, C0b, C1, C2 and C3.

G1 HYGIENE AND STRUCTURE — PASS. `git diff --name-only b8a918a1..f6d5d064` lists
exactly six paths: `.agent/authored/f256-r8.md`, `.agent/last_block.md`,
`.agent/live_review.md`, `.agent/plan.md`, `.agent/prose_slips.md`,
`docs/roadmap/features/T5_F256.md`. With `.agent/handoff.md` set aside, both
residues are empty: expected−actual `[]`, actual−expected `[]`. Insertions per
commit, each under 500 and each single-parent: C0a 322, C0b 226, C1 14, C2 14,
C3 87. Marker sweep at C3, lines beginning `<<<SLICE ` / `<<<END `:
`.agent/plan.md` 0/0, `.agent/live_review.md` 0/0, `.agent/prose_slips.md` 0/0,
`docs/roadmap/features/T5_F256.md` 0/0, beside the non-zero control
`.agent/authored/f256-r8.md` 4/4 and `.agent/last_block.md` 4/4.
`git ls-files .remedy-wt | wc -l` = 0.
`git diff --name-only b8a918a1..HEAD -- apps/ packages/ tests/ docs/roadmap/STATUS.md docs/roadmap/ROADMAP.md`
is EMPTY.

G2 TRANSPORT — PASS. `git show 8569ef20:.agent/authored/f256-r8.md` is 22031 bytes,
sha256 `619bf5d68f82d88878248b3ed66e19825f24ade29ae829e1bbbcd6acf352d9dd`; the
reviewer's own original `.remedy-wt/f256-r8-block.md` is 22031 bytes with the same
digest; EQUAL `True`. That original predates this worker and was not written by it,
so the reading covers the reviewer-to-disk transport and not merely this worker's
self-consistency. At C0b, `.agent/authored/f256-r8.md` and `.agent/last_block.md`
are ONE blob id: `21a3cfc8a6a8f3b91558a61d8fb6e9ae788cc3a7` for both.

G3 THE PLAN AT C1 — PASS. `.agent/plan.md` at `21cc5157` equals `PLANF256R8`
including the trailing newline: `True`. `wc -l` 33, under 50. Lines exactly
`## Goal`: 1. Lines exactly `## Next Steps`: 1.

G4 THE RECORD AT C2 — PASS. (a) `.agent/live_review.md`: base blob + `\n` +
`GATEF256R7` equals the C2 blob `True`, pre-round blob is a byte PREFIX `True`;
NEGATIVE CONTROL flipped one byte at offset 1361469, which the script confirms lies
inside the first appended paragraph spanning [1361321, 1361618), and equality became
`False`. `.agent/prose_slips.md`: base + `\n` + `SLIPF256R7` equals the C2 blob
`True`, prefix `True`; NEGATIVE CONTROL at offset 14729 inside the first appended
paragraph spanning [14550, 14908), equality became `False`.
(b) Paragraph counts were counted by the script from each slice, not taken from the
block: N=6 for `GATEF256R7` and N=1 for `SLIPF256R7`; the last N blank-line units of
each file match those paragraphs IN ORDER — `[True × 6]` and `[True]`.
`.agent/prose_slips.md` lines matching `^\d{4}-\d{2}-\d{2} · F`: 6 at base, 7 at C2,
gained exactly ONE, and the first six are unchanged (`True`).

G5 THE LEDGER AT C2 — PASS, and it moved exactly as a round that registers and
resolves nothing should. Base `b8a918a1` → C2 `cb2f3ce1`: `^- R-\d+ — ` 293 → 293,
all DISTINCT in both; `^Done: R-\d+ — ` 43 → 43; `^Landed: R-` 11 → 11; the OPEN SET
as a set 252 → 252; `^Gate: F\d+ R\d+ — ` 103 → 104, a rise of exactly ONE.
`Gate: F256 R7` occurs exactly 1 time.

G6 THE BUILT STATE AT C3 AND ITS CROSS-CHECK — PASS. The `b8a918a1` blob of
`docs/roadmap/features/T5_F256.md` plus a newline plus `BUILTF256` equals the C3
blob: `True`. The pre-round blob is a byte PREFIX: `True`. `## Built State` occurs
exactly once. The CROSS-CHECK was taken over the C3 BLOB of the feature file, and
every figure is present on BOTH sides — feature-file count first, source-file count
second, both at least 1 in every row:

- `tests/ui_server/test_diff_endpoint.py` — `0.1331` 1/1, `0.1282` 1/1,
  `0.1489` 1/1, `1,045,960` 1/1, `4.97` 1/1
- `apps/ui/src/api/diffViewModel.test.ts` — `0.678` 1/1, `0.271` 1/1, `1.408` 1/1,
  `10,002` 2/3, `100,020` 1/1
- `tests/orchestration/test_diff_parser.py` — `0.105` 1/1
- `apps/ui/src/components/diff/DiffView.module.css` — `.filePath` 1/3,
  `.fileMeta` 1/2, `.statAdd` 1/2, `.statDel` 1/2

The prose claims resolve too: `packages/orchestration/diff_parser.py` reads
`DIFF_VIEW_MAX_BODY_LINES = 20_000`, `tests/ui_server/test_diff_endpoint.py` reads
`DIFF_ENDPOINT_SCALE_RATIO_CEILING = 20`, `tests/orchestration/test_diff_parser.py`
reads `HUGE_DIFF_PARSE_CEILING_SECONDS = 0.5`, and both
`apps/ui/src/api/diffHighlightGrammars.ts` and `apps/ui/src/api/diffHighlight.test.ts`
EXIST. No recorded number was missing from the file that produced it, so
constraint 8's stop condition was not reached.

G7 THE SUITES AT C3 — PASS, one pytest process at a time from the repository root,
each exit 0:

    python3 -m pytest tests/docs/ -q                                → 295 passed in 0.44s        · exit 0
    python3 -m pytest tests/ui_contracts/ -q                        → 664 passed, 4 skipped in 5.41s · exit 0
    python3 -m pytest tests/ui_server/ -q                           → 497 passed in 30.34s       · exit 0
    python3 -m pytest tests/orchestration/test_diff_parser.py -q    → 43 passed in 2.34s         · exit 0
    python3 -m pytest tests/cli/test_golden_path.py -q              → 42 passed in 20.55s        · exit 0

No gate came back red, so no failure list is reproduced here.

## Authored-text proofs

Four reviewer-authored slices were applied this round, every one extracted from the
COMMITTED blob `git show 8569ef20:.agent/authored/f256-r8.md` per constraint 3 and
never from the prompt text. The committed `.agent/authored/f256-r8.md` is byte-equal
to the reviewer's original `.remedy-wt/f256-r8-block.md` at 22031 bytes, sha256
`619bf5d68f82d88878248b3ed66e19825f24ade29ae829e1bbbcd6acf352d9dd` (G2).

| Slice | Target | Disk-to-disk result |
|---|---|---|
| `PLANF256R8` | `.agent/plan.md` | whole-file equality including trailing newline, `True` (G3) |
| `GATEF256R7` | `.agent/live_review.md` | base + `\n` + slice equals the C2 blob, `True`; negative control `False` (G4) |
| `SLIPF256R7` | `.agent/prose_slips.md` | base + `\n` + slice equals the C2 blob, `True`; negative control `False` (G4) |
| `BUILTF256` | `docs/roadmap/features/T5_F256.md` | base + `\n` + slice equals the C3 blob, `True`; prefix `True` (G6) |

The `<<<SLICE` / `<<<END` delimiters reached no target file: G1's marker sweep reads
0/0 in all four targets, against 4/4 in the two authored controls.

## Deviations & assumptions

The ordered commit sequence was followed exactly — C0a, C0b, C1, C2, C3, C4, in that
order, with no extra commit, no dropped commit and no reordering. No slice was
reflowed, reworded, shortened or corrected; no number in `BUILTF256` was adjusted.

1. GUARD RE-EXPRESSION (constraint 6). The spelling
   `python3 -m pytest tests/docs/ -q 2>&1 | tail -20; echo "EXIT=${PIPESTATUS[0]}"`
   was refused by this session's shell guard with `Contains expansion` — the guard
   rejects `${...[...]}` indexing by FORM. It was re-expressed, not weakened, as the
   script `.remedy-wt/r8_run.py`, which runs the same `python3 -m pytest <target> -q`
   through `subprocess.run` and prints the FULL stdout plus the real
   `returncode`. All five G7 suites ran through it, untruncated. The check became
   strictly stronger, since the refused spelling would have truncated output to the
   last 20 lines.
2. ASSUMED (no ruling needed): every slice-application, digest, ledger, paragraph
   and cross-check computation ran from script files under the gitignored
   `.remedy-wt/` — `r8_c0a.py`, `r8_c0b.py`, `r8_slices.py`, `r8_c1.py`, `r8_c2.py`,
   `r8_c3.py`, `r8_g1.py`, `r8_g2345.py`, `r8_g6_cross.py`, `r8_g6_cross_blob.py`,
   `r8_run.py` — because /tmp is denied to this session. `git ls-files .remedy-wt`
   is 0, so none of them entered the commit range.
3. NOTED, not a deviation: the G6 cross-check was additionally run once against the
   WORKING-TREE copy of the feature file before C3 was committed, so that a missing
   number would have stopped the round before the commit rather than after it. It
   was then re-run against the C3 BLOB, which is the reading reported above. Both
   runs agree on every row.
4. NOTED: `packages/orchestration/diff_parser.py` spells the ceiling
   `DIFF_VIEW_MAX_BODY_LINES = 20_000`, a Python underscore literal, where the
   `BUILTF256` slice's prose says "is 20,000". The VALUE is the same 20000; only the
   digit grouping differs, so G6's claim holds. Reported because the block ordered
   the literal reading and this is what the file literally carries.
5. `.agent/context.md` and `.agent/decisions.md` were NOT touched: the change set
   names neither, this round makes no new technical decision of its own, and the
   scope and constraints of the branch are unchanged from round 7.

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a save the block | done | `8569ef20` |
| C0b mirror the block | done | `3f21db4b` |
| C1 advance the plan | done | `21cc5157` |
| C2 book the verdict and the slip | done | `cb2f3ce1` |
| C3 append the Built State | done | `f6d5d064` |
| C4 rewrite the handback | done | this commit |
| G1 hygiene and structure | done | PASS |
| G2 transport | done | PASS |
| G3 the plan at C1 | done | PASS |
| G4 the record at C2 | done | PASS |
| G5 the ledger at C2 | done | PASS |
| G6 the Built State and its cross-check | done | PASS |
| G7 the suites at C3 | done | PASS, all five exit 0 |

## Next

Run the integration gate over the whole branch, and then the two-round closure
sequence — the evidence bundle and the review zip in one round, the
`docs/roadmap/STATUS.md` closure commit with its README and ledger pins in a round
of its own.
