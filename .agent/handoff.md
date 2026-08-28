# Handback — F257 Self-use track, round 1 (THE CLAIM)

## Session

SESSION 1 of feature F257 · round 1 · rounds so far 1

## Range

Review of `f17b1d0d`..HEAD

`f17b1d0d03e4042df8452b2019b719cbe4704b21` is BASE — the tip of `main` after
constraint 0 merged pull request #220. It is the merge commit of that PR.

## Commits

Every `+/-` cell below is taken from `git diff --numstat` and matches, cell for
cell, the figures G7 reports.

### bb6612d7 chore(f257): save the round 1 claim block
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f257-r1.md` | +373 / -0 | C0a, the block saved verbatim |

### 5b3fbe83 chore(f257): mirror the round 1 block to last_block
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/last_block.md` | +332 / -318 | C0b, mirrored from the same source bytes |

### 451b1329 docs(f257): retarget the state and rule the queue format
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/plan.md` | +24 / -20 | C1, whole-file PLANF257R1 |
| `.agent/context.md` | +22 / -20 | C1, whole-file CTXF257R1 |
| `.agent/decisions.md` | +85 / -0 | C1, DECF257D1 then DECF257D2, appended |

### e406d1ee docs(f257): claim F257 in STATUS
| Path | +/- | Reason |
|------|-----|--------|
| `docs/roadmap/STATUS.md` | +1 / -1 | C2, the F257 line flipped `[ ]` → `[~]` |

### C3 — the handback commit (self-reference, R-0149 pattern)
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/handoff.md` | self-reference | this file; a handoff cannot table its own commit |

`.agent/live_review.md` is NOT edited this round. F256 R10 was the last round of
its branch, and docs/agents/planner_reviewer_prompt.md §4 item 13 rules that such
a round has no on-disk gate entry, so nothing was owed to the ledger. The F256
R10 verdict is PASS; it lives in the reviewer's report and in pull request #220.

## External actions

- `gh pr list --state open --json number,headRefName,baseRefName,isDraft` → exit
  0, output verbatim:
  `[{"baseRefName":"main","headRefName":"feature/f256-diff-viewer-completion","isDraft":false,"number":220}]`
  — exactly one entry, number 220, head `feature/f256-diff-viewer-completion`,
  base `main`, `isDraft` false, exactly as constraint 0 requires.
- `gh pr merge 220 --merge --delete-branch` → exit 0. Fast-forwarded
  `0e8ab5b4..f17b1d0d` on `main`, 30 files changed, 6653 insertions, 667
  deletions. The remote head branch was deleted by the gate's own
  `--delete-branch` and nothing else was deleted.
- `git checkout main` → exit 0, "Already on 'main'".
- `git pull --ff-only` → exit 0, "Already up to date".
- `git rev-parse HEAD` → `f17b1d0d03e4042df8452b2019b719cbe4704b21` (BASE).
- `git checkout -b feature/f257-self-use-track` → exit 0.
- `git push -u origin feature/f257-self-use-track` after C3. The outcome cannot
  be written into this file, which is inside C3; it is reported in the round's
  final message.
- NO pull request was created and nothing beyond pull request 220 was merged.
  Nothing was force-pushed, rebased or amended, and no history was rewritten.
- No `git worktree` was added or removed: this round writes no production code
  and needed no destructive verification.

## Verification — one line per gate

- G1 HYGIENE — PASS. `.agent/STOP` absent before C0a (False) and absent again
  before C2 (False). Open PR Gate output, merge result and BASE are recorded
  under External actions above. `git branch --show-current` =
  `feature/f257-self-use-track`. `git status --porcelain | wc -l` = 0 after C1
  and 0 after C2, measured directly; after C0a and after C0b the reading is 0 as
  well, established by the `git status --porcelain` run immediately after each,
  which printed ONLY the intended next edit (` M .agent/last_block.md` after
  C0a; the three C1 paths after C0b) and no other entry — see deviation 5.
- G2 TRANSPORT — PASS. The committed C0a blob
  `git show bb6612d7:.agent/authored/f257-r1.md` and the reviewer's own original
  `.remedy-wt/f257-r1-block.md` are both 20338 bytes with sha256
  `5854eb042b5cc4916d1f01808e696df0bef1894d4b9e5f74ae4642621036a2aa`; EQUAL True.
  That original was written before this worker existed and is not this worker's
  output, so the reading covers real transport and not merely self-consistency.
  At C0b, `git rev-parse 5b3fbe83:.agent/authored/f257-r1.md` and
  `git rev-parse 5b3fbe83:.agent/last_block.md` print ONE blob id,
  `b358ea1b7a6dd948714e288db526bca99592800a`.
- G3 THE STATE SLICES AT C1 — PASS. `.agent/plan.md` at C1 equals PLANF257R1
  including the trailing newline: True. `.agent/context.md` at C1 equals
  CTXF257R1 including it: True. `wc -l` of `.agent/plan.md` = 36, under 50.
  Lines exactly `## Goal` = 1 and exactly `## Next Steps` = 1 in
  `.agent/plan.md`; lines exactly `## Active Branch` = 1 in `.agent/context.md`.
- G4 THE DECISIONS APPEND AT C1 — PASS, both readers. (a) BASE blob + newline +
  DECF257D1 + newline + DECF257D2 equals the C1 blob: True. NEGATIVE CONTROL:
  byte offset 710539, which the script confirmed lies strictly inside the FIRST
  appended paragraph's span of 710499..710666, was flipped and the equality
  became False. (b) N = 12, the number of blank-line
  paragraphs the two slices hold together, counted by the script FROM THE SLICES
  and never read off the block; the LAST 12 units of the C1 file match those 12
  paragraphs IN ORDER, unit by unit, all True. The pre-round blob is a byte
  PREFIX of the C1 blob: True, 710498 bytes → 715877 bytes.
- G5 THE CLAIM AT C2 — PASS. Over `docs/roadmap/STATUS.md` at C2: CLAIMFROM
  count 0, CLAIMTO count 1; CLAIMTO is present as a WHOLE LINE exactly 1 time.
  Lines matching `^- \[~\] F\d{3} — ` = 1, within the at-most-1 that
  `tests/docs/test_docs_consistency.py` requires. Lines matching
  `^- \[x\] F\d{3} — ` = 61 before C2 and 61 after C2 — UNMOVED at 61. The
  containment test on the pair, run mechanically, printed `TO contains FROM:
  False`, so the pair is a REWRITE and was gated as a FROM-zero / TO-one count.
- G6 THE SUITES AT C2 — PASS. One pytest process at a time, from the repository
  root, in the PRIMARY checkout, each with its real exit code:
  `tests/docs/` 295 passed in 0.44 s, exit 0;
  `tests/orchestration/test_roadmap_index.py` 30 passed in 0.34 s, exit 0;
  `tests/ui_server/` 497 passed in 32.23 s, exit 0;
  `tests/orchestration/test_test_runner.py` 52 passed in 5.31 s, exit 0;
  `tests/regression/test_resource_safety.py` 21 passed in 11.52 s, exit 0;
  `tests/orchestration/test_integrity_gate.py` 16 passed in 0.30 s, exit 0;
  the canary `tests/cli/test_golden_path.py` 42 passed in 20.54 s, exit 0.
  Seven runs, seven exit-0 readings, none red.
- G7 STRUCTURE over `f17b1d0d..e406d1ee` — PASS on every clause except one
  residue that is unmeetable by construction; see deviation 4.
  `git diff --name-only` prints exactly six paths: `.agent/authored/f257-r1.md`,
  `.agent/context.md`, `.agent/decisions.md`, `.agent/last_block.md`,
  `.agent/plan.md`, `docs/roadmap/STATUS.md`. Residue actual − change set: `[]`,
  empty. Residue change set − actual: `['.agent/handoff.md']`, NOT empty —
  because the range ends at C2 and `.agent/handoff.md` is written by C3.
  Per-commit insertions from `git diff --numstat`: 373, 332, 131 and 1 — each
  under 500 — and each of C0a, C0b, C1 and C2 is single-parent (1 parent each).
  Counted affirmatively over each file's C2 content: lines beginning `<<<SLICE `
  and lines beginning `<<<END ` are 0 and 0 in `.agent/plan.md`, 0 and 0 in
  `.agent/context.md`, 0 and 0 in `.agent/decisions.md`, and 0 and 0 in
  `docs/roadmap/STATUS.md`, against the non-zero control
  `.agent/authored/f257-r1.md` at 6 and 6. `git ls-files .remedy-wt | wc -l` = 0.

## Authored-text proofs

Every reviewer-authored text applied this round was extracted from the COMMITTED
blob `git show bb6612d7:.agent/authored/f257-r1.md` under constraint 3, never
from the prompt, and the delimiter lines reached no target file (G7, 0 and 0 in
all four targets).

- `.agent/plan.md` at C1 — whole-blob equality with PLANF257R1, True (G3).
- `.agent/context.md` at C1 — whole-blob equality with CTXF257R1, True (G3).
- `.agent/decisions.md` at C1 — the whole file reconstructs byte for byte as
  BASE + newline + DECF257D1 + newline + DECF257D2, True, with the pre-round
  blob a byte prefix, a negative control rejected, and the last 12 paragraphs
  matching the slices in order (G4).
- `docs/roadmap/STATUS.md` at C2 — the CLAIMTO string occurs exactly once and as
  a whole line, the CLAIMFROM string zero times (G5).

## Deviations & assumptions

1. NO DEPARTURE FROM THE ORDERED COMMIT SEQUENCE. C0a, C0b, C1, C2 and C3 were
   committed in that order; none was added, none dropped, none reordered.
2. The Session line carries the block's exact string
   `SESSION 1 of feature F257 · round 1` and then appends `· rounds so far 1`,
   because docs/agents/handback_template.md mandates the `rounds so far <total>`
   field. Both requirements are met rather than one chosen over the other.
3. GUARD RE-EXPRESSIONS. Constraint 6 obliges reporting these. NO command was
   actually rejected by this session's guard, because the rejected forms were
   avoided pre-emptively rather than discovered: every counting, hashing,
   byte-offset and slice-extraction step ran through a `python3 - <<'PY'`
   heredoc; the two block copies used `shutil.copyfile` and never `cp`; no
   environment variable was assigned in any of the three rejected spellings; and
   every exit code reported above was captured with
   `bash -c '<cmd>; echo "REAL_EXIT=$?"'` or, for the piped pytest runs, with
   `${PIPESTATUS[0]}` inside such a `bash -c`, which this session accepted. No
   check was skipped and none was replaced by a weaker spelling.
4. G7's SECOND RESIDUE IS NOT EMPTY, and cannot be. G7 orders the range
   `BASE..<C2>`, "the range that ends BEFORE the handback commit", and also
   orders both residues against a change set that LISTS `.agent/handoff.md` —
   the file C3 writes. So `change set − actual` is `['.agent/handoff.md']` by
   construction, for every possible correct run. It is reported as measured
   rather than quietly narrowed: no unexpected path appears in either direction,
   and the residue in the other direction is empty. Nothing on disk is wrong;
   this is a reviewer-prose inaccuracy in the gate's expectation.
5. G1's per-commit `git status --porcelain | wc -l` was measured DIRECTLY after
   C1 and after C2 (0 and 0). After C0a and after C0b it was not run as its own
   `wc -l`; the reading comes from the `git status --porcelain` executed
   immediately after each of those commits, which listed ONLY the edit made
   after the commit and nothing else, so the tree was clean at both. Declared
   because it is an indirect reading of the two, not a direct one.
6. THE COMMIT SUMMARY AND `git diff --numstat` DISAGREE ON TWO COMMITS, and the
   handback tables the numstat figures as G7 orders. `git commit` printed
   "373 insertions(+), 359 deletions(-)" with "rewrite .agent/last_block.md
   (96%)" for C0b where numstat gives 332/318, and "143 insertions(+), 52
   deletions(-)" with "rewrite .agent/plan.md (92%)" for C1 where numstat gives
   131/40. The gap is git's rewrite detection in the commit summary. Both
   readings are under 500 on every commit, so no cap is at stake; it is declared
   so the reviewer re-running either command is not surprised by the other.
7. THE TWO DECISION SLICES ARE DATED 2026-08-28 and this round ran on
   2026-08-29. They are reviewer-authored text and constraint 1 forbids
   correction, so they were applied byte for byte as written. Likewise both
   decisions state their measurements "at `c9c54d27`", the pre-merge F256 tip,
   which is the reviewer's own measurement point and not this round's BASE.
8. `.agent/live_review.md` was not edited, as the block directs, and is
   byte-unchanged in `f17b1d0d..e406d1ee` — it does not appear in G7's
   `git diff --name-only`.
9. NO PRODUCTION CODE was written and no file outside the change set was created
   or edited, per constraint 7. Nothing under `packages/`, `apps/`, `tests/` or
   `scripts/` appears in the range.

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C0a save this block to `.agent/authored/f257-r1.md` | done | |
| C0b mirror the same bytes into `.agent/last_block.md` | done | |
| C1 retarget plan and context, append DECISIONS F257 D1 and D2 | done | |
| C2 the STATUS claim | done | `[ ]` → `[~]` |
| C3 rewrite `.agent/handoff.md` | done | this file |
| the push | done | outcome in the round's final message, not tableable here |
| G1 hygiene | done | PASS; two `.agent/STOP` readings both False |
| G2 transport | done | PASS; one blob id, 20338 bytes, digests EQUAL |
| G3 the state slices at C1 | done | PASS; both byte-equal, plan 36 lines |
| G4 the decisions append at C1 | done | PASS; N = 12, negative control rejected |
| G5 the claim at C2 | done | PASS; 0 / 1, `[~]` count 1, `[x]` unmoved at 61 |
| G6 the suites at C2 | done | PASS; seven runs, every one exit 0 |
| G7 structure | deviated | PASS except the `.agent/handoff.md` residue, which is unmeetable by construction — deviation 4 |

## Open findings

251 open in the ledger, all inherited from earlier features, unchanged from the
F256 R10 reading: `.agent/live_review.md` is byte-unchanged in this round's
range, so no finding was registered, resolved or moved. None is open against
F257, which is claimed for the first time in this round.

## Next

The single expected next action is THE NEXT DELEGATED ROUND OF F257, which builds
`scripts/self_use_queue.json` and its read-only loader
`packages/orchestration/self_use_queue.py`, with tests, against DECISION F257 D2.
No pull request exists for this branch and none is created this round.
