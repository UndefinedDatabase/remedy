# Handback — F033 Hunk-level diff approval, round 21

## Session

SESSION 6 of feature F033 · round 21 · rounds so far 21

Four rounds of headroom remain against the 25-round soft limit; no scope report
is owed yet. `.agent/plan.md` records that steps 2, 3 and 4 of its Next Steps are
four rounds of work, so session 6 may owe that report before the limit.

## Range

Review of `98ce168e`..HEAD, where HEAD is C6 — the commit that writes this file.
C6's own SHA is deliberately NOT stated here: it does not exist while this file
is being written, and an SHA nobody measured is worse than none. The last
MEASURED commit is C5, `90fdaee5`.

Branch: `feature/f033-hunk-approval-v2`. Base for this round: `98ce168e`.
Every gate G1-G8 was run at C5 (`90fdaee5`), BEFORE this file was written, so
every reading below is quoted from a run that had already happened.

## Commits

### 38643092 docs(f033): save the round 21 block verbatim
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f033-r21.md` | +300 / -0 | C0a. The round's step block, copied BYTE FOR BYTE from `.remedy-wt/f033-r21-block.md` with `shutil.copyfile`. Not retyped. |

### d9f7dec0 docs(f033): mirror the round 21 block into last_block
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/last_block.md` | +298 / -0 | C0b. The same bytes mirrored, `cmp` silent against the source. |

### 693d1c46 docs(f033): advance the plan to round 21
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/plan.md` | +13 / -14 | C1. FULL REWRITE from slice PLAN21, applied byte for byte by script. |

### e0c9ce2d docs(f033): book the round 20 verdict
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/live_review.md` | +2 / -0 | C2. Slice RECORD21 appended after one blank-line separator. Books the R20 PASS that `.agent/handoff.md` has carried since `b5a29a74`, per operator amendment amend0827 rule 1. |

### 972968e1 docs(f033): append the two round 20 prose slips
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/prose_slips.md` | +4 / -0 | C3. Slice SLIPS21 appended after one blank-line separator. Two paragraphs, blank-separated. |

### 06443151 feat(f033): carry rejected hunks into the builder prompt as a steering segment
| Path | +/- | Reason |
|------|-----|--------|
| `packages/orchestration/pingpong_loop.py` | +55 / -1 | C4, SPEC A. A1 the `render_rejection_findings` import; A2 the keyword-only `hunk_ledger: Any = None`; A3 the `builder_hunk_rejections` STEERING segment between `builder_repair` and `builder_directive`; A4 exactly ONE guard, the emptiness test; A5 both deliberate absences documented in the idiom; A6 `_build_builder_prompt` forwards the parameter unchanged. |

### 90fdaee5 test(f033): pin the verbatim rejection reason through prompt composition
| Path | +/- | Reason |
|------|-----|--------|
| `tests/orchestration/test_builder_prompt_hunk_rejections.py` | +338 / -0 | C5, SPEC B. New file, 14 tests covering B1-B7. The three rendered-vocabulary constants are IMPORTED by name and never retyped. |

### C6 (SHA unmeasurable from inside) docs(f033): hand back the builder prompt rejection segment
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/handoff.md` | full rewrite, not an append | C6, this file. A handback cannot table the commit that writes it (R-0149 pattern), and it cannot name that commit's SHA either. Its insertion count is not gated this round, by Constraint 8; the reviewer measures both. |

## External actions

- `git worktree add /home/decodeux/Repos/remedy/.remedy-wt/r21-mut 90fdaee5 --detach`
  — OK, "HEAD is now at 90fdaee5". All G6 mutations ran ONLY there.
- `git -C .remedy-wt/r21-mut status --porcelain` — EMPTY before removal.
- `git worktree remove /home/decodeux/Repos/remedy/.remedy-wt/r21-mut` — OK.
  Run WITHOUT `--force`; the plain form succeeded and no force was needed.
- `git worktree prune`; `git worktree list` — only the primary checkout remains,
  at `90fdaee5 [feature/f033-hunk-approval-v2]`.
- `git push origin feature/f033-hunk-approval-v2` — REAL exit 0,
  `98ce168e..90fdaee5`. Run BEFORE C6 so this line quotes a measured outcome
  rather than a prediction. The C6 commit is pushed immediately after this file
  is committed; that second push is not covered by the reading above.
- No pull request was created, edited or merged. `main` was not touched. No
  force-push. No `gh` command was run.

## Verification

Every gate below was captured as `bash -c '<cmd>; echo "REAL_EXIT=$?"'` with NO
PIPE anywhere in the command, per Constraint 5. Where the work needed counting or
hashing it ran from a script file under `.remedy-wt/` rather than an inline
heredoc, because the sandbox denies a heredoc nested inside `bash -c`.

**G1 TRANSPORT — REAL exit 0. GREEN.**
`python3 .remedy-wt/g1_g2.py`

    G1 .agent/authored/f033-r21.md bytes: 21541
    G1 sha256: 105c5c4dabbab8970fe432f4ccb20ad20bcd477d2b5849998de0e9845ad60432
    G1 identical to the .remedy-wt source: True

That digest is the one the round order stated, computed independently with
`sha256sum` before any work began and again from the COMMITTED blob at `90fdaee5`.

**G2 THE PROSE FILES — REAL exit 0. GREEN.** (same script, same run)

    G2 plan.md bytes: 2509 lines: 45
    G2 plan.md byte-EQUAL to PLAN21: True
    G2 plan.md under 50 lines: True
    G2 plan.md contains '## Goal': True
    G2 plan.md contains 'Steps': True
    G2 prose_slips base: 29663 +1+ slice: 1143 = 30807
    G2 prose_slips committed size: 30807 MATCH: True
    G2 prose_slips prefix_ok: True
    G2 prose_slips suffix_ok: True
    G1G2_ALL_TRUE: True

The three numbers G2 asks for: base 29663, slice 1143, committed 30807.
`tests/ui_server/test_dashboard_contract.py::test_plan_md_references_current_steps`
needs `## Goal` and `Steps`; both are present.

**G3 THE RECORD APPEND — REAL exit 0. GREEN.**
`python3 .remedy-wt/g3.py`

    G3 base bytes: 1575558 +1+ slice bytes: 4635 = 1580194
    G3 committed bytes: 1580194 MATCH: True
    G3 N (blank-line paragraphs counted IN THIS SCRIPT from the slice): 1
    G3 blank-line units in the committed file: 714
    G3 blank-line units in the pre-commit file: 713
    G3 READER A accepts the committed file: True
    G3 READER B accepts the committed file: True
    G3   (B detail) prefix_ok: True separator: b'\n' suffix_ok: True
    G3 first appended paragraph span: bytes 1575559 to 1580193 (length 4634 )
    G3 that span is the slice's first paragraph: True
    G3 FLIP offset: 1577876 inside the first appended paragraph: True
    G3 byte at that offset before/after: b'N' -> b'n'
    G3 flip changed exactly one byte: True and length is unchanged: True
    G3 READER A rejects the FLIPPED file: True
    G3 READER B rejects the FLIPPED file: True
    G3_ALL_TRUE: True

N was COUNTED in the script from the slice's own bytes and is 1 — RECORD21 is a
single blank-line unit. READER A splits both file and slice into blank-line units
and compares the file's LAST N against the slice's paragraphs in order; READER B
is the independent byte reader (prefix, separator, exact suffix, arithmetic). The
negative control flips byte 1577876, proved to lie in the span 1575559..1580193
which the script also proves IS the first appended paragraph, and both readers
reject it while both accept the unflipped bytes. The flip lives in memory only;
nothing was written to the working tree, which is why `git status --porcelain`
is still empty at G8.

**G4 THE LEDGER — REAL exit 0. GREEN.**
`python3 .remedy-wt/g4.py`, reading the COMMITTED blobs at `693d1c46` (C1, the
commit immediately before the append) and `90fdaee5` (C5).

    G4 registered_lines: before=307 after=307
    G4 registered_distinct: before=307 after=307
    G4 done_lines: before=52 after=52
    G4 done_distinct: before=50 after=50
    G4 landed_lines: before=18 after=18
    G4 landed_distinct: before=15 after=15
    G4 gate_r20: before=0 after=1
    G4 open_set: before=257 after=257
    G4_ALL_TRUE: True

Patterns: `^- (R-\d+) — `, `^Done: (R-\d+) — `, `^Landed: `, `^Gate: F033 R20 — `.
Every ordered numeral matched: 307 distinct registered UNMOVED; `Done:` 52 lines
over 50 distinct UNMOVED; `Landed:` 18 lines over 15 distinct UNMOVED; the R20
gate line 0 before and exactly 1 after; the open set 257 UNMOVED.

**G5 THE CODE AGAINST THE SPEC — REAL exit 0 for both halves. GREEN.**

`python3 -m ruff check packages/orchestration/pingpong_loop.py tests/orchestration/test_builder_prompt_hunk_rejections.py`

    All checks passed!
    REAL_EXIT=0

`python3 .remedy-wt/g5.py` — AST, not grep, plus a run of the shipped function:

    G5 A1 ImportFrom hunk_repair_findings render_rejection_findings nodes: 1
    G5 compose_builder_prompt kwonly: ['round_number', 'findings', 'staged_state', 'safe_diff', 'task_body', 'scope_contract', 'test_result', 'hunk_ledger']
    G5 compose_builder_prompt positional: ['goal', 'context']
    G5 compose_builder_prompt hunk_ledger keyword-only: True | last in signature: True | default is None: True | not positional: True
    G5 _build_builder_prompt kwonly: ['round_number', 'findings', 'staged_state', 'safe_diff', 'task_body', 'scope_contract', 'test_result', 'hunk_ledger']
    G5 _build_builder_prompt positional: ['goal', 'context']
    G5 _build_builder_prompt hunk_ledger keyword-only: True | last in signature: True | default is None: True | not positional: True
    G5 A3 'builder_hunk_rejections' spec tuples: ['SegmentStabilityRank.STEERING']
    G5 A4 comparisons whose left operand is `hunk_ledger`: []
    G5 shipped manifest: ['builder_system', 'builder_context', 'builder_task', 'builder_hunk_rejections', 'builder_directive']
    G5 shipped rank of builder_hunk_rejections: 5 == SegmentStabilityRank.STEERING: True
    G5_ALL_TRUE: True

The STEERING claim is made twice by different routes: by AST, the only three-tuple
whose first element is the constant `"builder_hunk_rejections"` carries the rank
expression `SegmentStabilityRank.STEERING`; and by RUNNING the shipped function,
the manifest entry of that name compares equal to `SegmentStabilityRank.STEERING`.
The A4 line is the counter-measure the block's SPEC A4 ordered: there is no
`Compare` node anywhere in the module whose left operand is `hunk_ledger`, so the
emptiness test is demonstrably the ONLY guard, and G6(i) can therefore redden.

**G6 MUTATION RED-PROOFS — REAL exit 0 for the driver. GREEN, all three RED as ordered.**
`python3 .remedy-wt/g6.py`, in the disposable worktree `.remedy-wt/r21-mut` at
`90fdaee5`, never in the primary checkout. Every pytest run used `python3 -B` and
`-p no:cacheprovider`, and a `__pycache__` purge ran immediately before each run.
Committed blob under mutation:
`sha256 0a35f998cda641bb1ca61ff6fc4ddfb8326e614edbb9908328e321cfaa838dc2`, 197463
bytes. Selection for every run, control included:
`tests/orchestration/test_builder_prompt_hunk_rejections.py` plus
`tests/orchestration/test_builder_prompt_golden.py`.

    G6 CONTROL (unmutated): REAL exit 0 | 35 passed in 0.35s | __pycache__ dirs purged 0
    G6 CONTROL failing: [] errors: []

The CONTROL RAN FIRST, and its 35-passed/exit-0 reading is the baseline every
mutation below is read against.

  (i) remove SPEC A3's emptiness guard so the segment registers unconditionally.
      Anchor occurrences in `packages/orchestration/pingpong_loop.py`: **1**.

    REAL exit 1 | 9 failed, 26 passed in 0.38s | __pycache__ dirs purged 0
    FAILED tests/orchestration/test_builder_prompt_golden.py::test_only_the_minimal_shape_is_byte_identical_to_the_frozen_render
    FAILED tests/orchestration/test_builder_prompt_golden.py::test_segments_reassemble_into_the_frozen_render[full]
    FAILED tests/orchestration/test_builder_prompt_golden.py::test_segments_reassemble_into_the_frozen_render[minimal]
    FAILED tests/orchestration/test_builder_prompt_golden.py::test_segments_reassemble_into_the_frozen_render[scope_task]
    FAILED tests/orchestration/test_builder_prompt_golden.py::test_segments_reassemble_into_the_frozen_render[staged]
    FAILED tests/orchestration/test_builder_prompt_golden.py::test_the_full_shape_registers_the_ten_segments_in_rank_order
    FAILED tests/orchestration/test_builder_prompt_hunk_rejections.py::test_a_ledger_whose_second_entry_is_broken_registers_nothing_at_all
    FAILED tests/orchestration/test_builder_prompt_hunk_rejections.py::test_a_malformed_ledger_composes_without_raising_and_registers_nothing
    FAILED tests/orchestration/test_builder_prompt_hunk_rejections.py::test_no_rejection_registers_no_segment_and_changes_no_byte
    restore byte-identical to the committed blob: True

      `test_builder_prompt_golden.py` went RED as ordered — SIX of its tests,
      including the exact ten-name manifest tuple the block predicted. Three
      tests in the new file also reddened; the block ordered only the golden, so
      the extra red is reported here rather than suppressed (deviation D5).

  (ii) register the rejections spec AFTER the `builder_directive` spec instead of
       before it. Anchor occurrences: **1**.

    REAL exit 1 | 10 failed, 25 passed in 0.87s | __pycache__ dirs purged 0
    FAILED tests/orchestration/test_builder_prompt_hunk_rejections.py::test_a_hostile_reason_reaches_the_composed_prompt_as_an_exact_substring
    FAILED tests/orchestration/test_builder_prompt_hunk_rejections.py::test_a_reason_ending_in_a_newline_keeps_that_newline
    FAILED tests/orchestration/test_builder_prompt_hunk_rejections.py::test_build_builder_prompt_forwards_the_parameter_unchanged
    FAILED tests/orchestration/test_builder_prompt_hunk_rejections.py::test_each_hostile_feature_survives_on_its_own
    FAILED tests/orchestration/test_builder_prompt_hunk_rejections.py::test_manifest_ranks_stay_non_decreasing_with_the_segment_present
    FAILED tests/orchestration/test_builder_prompt_hunk_rejections.py::test_rejections_sit_between_the_repair_findings_and_the_directive
    FAILED tests/orchestration/test_builder_prompt_hunk_rejections.py::test_the_directive_is_still_the_last_segment_when_rejections_are_present
    FAILED tests/orchestration/test_builder_prompt_hunk_rejections.py::test_the_segment_hash_and_span_agree_with_the_composed_text
    FAILED tests/orchestration/test_builder_prompt_hunk_rejections.py::test_the_segment_is_registered_at_steering_rank
    FAILED tests/orchestration/test_builder_prompt_hunk_rejections.py::test_two_rejections_keep_the_ledger_order_and_both_reasons
    restore byte-identical to the committed blob: True

      The new test file went RED as ordered, and every one of the ten failures is
      in it — `test_builder_prompt_golden.py` stayed GREEN, which is right,
      because no golden shape supplies a ledger.

  (iii) register `rejection_text.strip()` instead of `rejection_text`.
        Anchor occurrences: **1**.

    REAL exit 1 | 4 failed, 31 passed in 0.37s | __pycache__ dirs purged 0
    FAILED tests/orchestration/test_builder_prompt_hunk_rejections.py::test_a_hostile_reason_reaches_the_composed_prompt_as_an_exact_substring
    FAILED tests/orchestration/test_builder_prompt_hunk_rejections.py::test_build_builder_prompt_forwards_the_parameter_unchanged
    FAILED tests/orchestration/test_builder_prompt_hunk_rejections.py::test_each_hostile_feature_survives_on_its_own
    FAILED tests/orchestration/test_builder_prompt_hunk_rejections.py::test_the_segment_hash_and_span_agree_with_the_composed_text
    restore byte-identical to the committed blob: True

      The new test file went RED as ordered. These are exactly the four tests
      that assert a RAW reason as a substring — a strip eats the hostile reason's
      trailing spaces, which is the verbatim rule failing, and nothing else in
      the file notices. That is the discriminator working.

    G6 final restore byte-identical: True

Each anchor was asserted UNIQUE by the script before it was applied (the count is
printed above for all three, and the script raises if it is not 1), the file was
restored after each mutation and PROVED byte-identical to the committed blob at
`90fdaee5` every time, and the final restore was proved again.

**G7 THE SUITES — SERIALLY, in the PRIMARY checkout, every REAL exit 0. GREEN.**

| # | Command | REAL exit | Result |
|---|---------|-----------|--------|
| 1 | `python3 -m pytest tests/orchestration/test_builder_prompt_hunk_rejections.py -q --no-header` | 0 | 14 passed in 0.26s |
| 2 | `python3 -m pytest tests/orchestration/test_builder_prompt_golden.py -q --no-header` | 0 | 21 passed in 0.31s |
| 3 | `python3 -m pytest tests/orchestration/test_prompt_cache_prefix.py -q --no-header` | 0 | 16 passed in 0.28s |
| 4 | `python3 -m pytest tests/orchestration/test_hunk_repair_findings.py -q --no-header` | 0 | 17 passed in 0.22s |
| 5 | `python3 -m pytest tests/orchestration/test_pingpong_cli.py -q --no-header` | 0 | 172 passed in 2.54s |
| 6 | `python3 -m pytest tests/orchestration/test_repair_loop.py -q --no-header` | 0 | 131 passed in 1.58s |
| 7 | `python3 -m pytest tests/cli/test_golden_path.py -q` (canary) | 0 | 42 passed in 20.71s |

Seven separate invocations, one per call, never in parallel and never chained.

**G8 STRUCTURE — REAL exit 0. GREEN.**
`python3 .remedy-wt/g8.py`

    G8 git status --porcelain (repr): ''
    G8 working tree EMPTY: True
    G8 branch tip: 90fdaee518e06a68ba4ab7d97e472e5f13ee1390
    G8 branch: feature/f033-hunk-approval-v2
    G8 per-commit insertions (500-line cap):
    G8   C0a 38643092 insertions=300 under_500=True parents=1 files=['.agent/authored/f033-r21.md']
    G8   C0b d9f7dec0 insertions=298 under_500=True parents=1 files=['.agent/last_block.md']
    G8   C1 693d1c46 insertions=13 under_500=True parents=1 files=['.agent/plan.md']
    G8   C2 e0c9ce2d insertions=2 under_500=True parents=1 files=['.agent/live_review.md']
    G8   C3 972968e1 insertions=4 under_500=True parents=1 files=['.agent/prose_slips.md']
    G8   C4 06443151 insertions=55 under_500=True parents=1 files=['packages/orchestration/pingpong_loop.py']
    G8   C5 90fdaee5 insertions=338 under_500=True parents=1 files=['tests/orchestration/test_builder_prompt_hunk_rejections.py']
    G8 path set over 98ce168e..C5: ['.agent/authored/f033-r21.md', '.agent/last_block.md', '.agent/live_review.md', '.agent/plan.md', '.agent/prose_slips.md', 'packages/orchestration/pingpong_loop.py', 'tests/orchestration/test_builder_prompt_hunk_rejections.py']
    G8 declared change set minus .agent/handoff.md: ['.agent/authored/f033-r21.md', '.agent/last_block.md', '.agent/live_review.md', '.agent/plan.md', '.agent/prose_slips.md', 'packages/orchestration/pingpong_loop.py', 'tests/orchestration/test_builder_prompt_hunk_rejections.py']
    G8 measured MINUS declared (must be empty): []
    G8 declared MINUS measured (must be empty): []
    G8 sets EQUAL in BOTH directions: True
    G8_ALL_TRUE: True

All seven commits are single-parent, the largest insertion count is 338, and the
path set equals the declared change set minus `.agent/handoff.md` in BOTH
directions. `git status --porcelain` was MEASURED EMPTY at C5. The only
working-tree change made after that reading is this file, which C6 commits; the
post-C6 emptiness is therefore the reviewer's to measure, not mine to assert. The
scratch under `.remedy-wt/` is gitignored and appears in no reading.

### Gate summary — one line each

| Gate | REAL exit | Verdict |
|------|-----------|---------|
| G1 TRANSPORT | 0 | GREEN — 21541 bytes, sha256 `105c5c4d…ad60432`, identical to source |
| G2 THE PROSE FILES | 0 | GREEN — plan byte-equal to PLAN21 at 45 lines; slips 29663+1+1143=30807 |
| G3 THE RECORD APPEND | 0 | GREEN — 1575558+1+4635=1580194, N=1, both readers reject the flip at byte 1577876 |
| G4 THE LEDGER | 0 | GREEN — 307 / 52-over-50 / 18-over-15 UNMOVED, R20 gate 0→1, open set 257 UNMOVED |
| G5 THE CODE AGAINST THE SPEC | 0 (ruff) + 0 (AST) | GREEN — both signatures keyword-only, STEERING by AST and by run, zero `hunk_ledger` comparisons |
| G6 MUTATION RED-PROOFS | 0 (driver) | GREEN — control 35 passed exit 0; (i) exit 1 golden RED, (ii) exit 1 new file RED, (iii) exit 1 new file RED |
| G7 THE SUITES | 0 ×7 | GREEN — 14, 21, 16, 17, 172, 131 and 42 passed, serially |
| G8 STRUCTURE | 0 | GREEN — tree empty, max 338 insertions, path set equal both ways |

No gate came out RED. Nothing was repaired on my own initiative and no test or
assertion was weakened.

**Open findings: 257** (307 distinct registered minus 50 distinct resolved,
measured by G4 at `90fdaee5`; UNMOVED across this round, which registered and
resolved nothing).

## Authored-text proofs

Three reviewer-authored texts were applied this round; all three are slices of the
one authored file, and none was retyped, reflowed or re-wrapped.

- `.agent/authored/f033-r21.md` — copied from `.remedy-wt/f033-r21-block.md` with
  `python3 -c "import shutil; shutil.copyfile(...)"`. `cmp` against the source:
  **SILENT** (exit 0). `sha256` of both: `105c5c4dabbab8970fe432f4ccb20ad20bcd477d2b5849998de0e9845ad60432`,
  21541 bytes — the digest the round order stated, verified before any work began.
- `.agent/last_block.md` — the same bytes. `cmp` against the source: **SILENT**.
  Same sha256, same length.
- PLAN21 → `.agent/plan.md`: extracted BY SCRIPT (`.remedy-wt/r21_extract.py`,
  raw bytes, marker lines excluded) at 2509 bytes / 45 lines,
  sha256 `715c97d6d9a8e81f79fb581f8f7e99a779a94b93153120b2a6faa5c29fec852a`.
  The committed file is byte-EQUAL to the slice (G2).
- RECORD21 → `.agent/live_review.md`: 4635 bytes,
  sha256 `81d5c2d77c9876471169b45f4d4b672600452e20b79c803c0e5aea3866e89786`.
  Exact byte SUFFIX of the committed file, base an exact PREFIX (G3).
- SLIPS21 → `.agent/prose_slips.md`: 1143 bytes,
  sha256 `258da7c76ec6eecf99add14290b9bac52d71d813a4c3f06131bf35af82bb4c21`.
  Exact byte SUFFIX of the committed file, base an exact PREFIX (G2).

HONEST LIMIT OF THIS CHAIN: `cmp` walks the saved copy, its mirror and the
working copy — three artefacts that are all this worker's own output — so it
establishes SELF-CONSISTENCY against `.remedy-wt/f033-r21-block.md` and the
stated digest. It is not a claim about bytes emitted anywhere else. The R20
record makes the same reservation about its own chain and it is repeated here
rather than quietly dropped.

## Item status — every Bundle item

| Item | Status | Evidence |
|------|--------|----------|
| C0a — save the block verbatim to `.agent/authored/f033-r21.md` | DONE | `38643092`; `cmp` silent; G1 exit 0 |
| C0b — mirror the same bytes into `.agent/last_block.md` | DONE | `d9f7dec0`; `cmp` silent; same sha256 |
| C1 — rewrite `.agent/plan.md` from slice PLAN21 | DONE | `693d1c46`; G2 byte-equal, 45 lines |
| C2 — append RECORD21 to `.agent/live_review.md` | DONE | `e0c9ce2d`; G3 exit 0, G4 R20 gate 0→1 |
| C3 — append SLIPS21 to `.agent/prose_slips.md` | DONE | `972968e1`; G2 29663+1+1143=30807 |
| C4 — SPEC A against `packages/orchestration/pingpong_loop.py` | DONE | `06443151`; G5 exit 0 both halves; G6 all three RED |
| C5 — new file `tests/orchestration/test_builder_prompt_hunk_rejections.py` | DONE | `90fdaee5`; G7 14 passed exit 0 |
| C6 — rewrite `.agent/handoff.md` as the handback | DONE | this file; SHA not stated, see Range |
| SPEC A1 — the `render_rejection_findings` import | DONE | G5: exactly 1 matching `ImportFrom` node |
| SPEC A2 — keyword-only `hunk_ledger: Any = None`, last in signature | DONE | G5 AST: kwonly, last, default `None`, not positional. `Any` was ALREADY imported at line 30; no new typing import was needed |
| SPEC A3 — register between repair and directive, STEERING, one part | DONE | G5 AST + shipped run; G6(ii) reddens the new file when the order is broken |
| SPEC A4 — EXACTLY ONE guard, the emptiness test | DONE | G5: zero `Compare` nodes with `hunk_ledger` as left operand; G6(i) reddens the golden, so the guard is observable |
| SPEC A5(i) — the call site is NOT changed, documented in the idiom | DONE | `compose_builder_prompt`'s docstring, "Remedy deliberately does NOT supply this parameter from the run loop yet"; G8 shows no other production path changed |
| SPEC A5(ii) — the rendered text is NOT capped, documented | DONE | comment beside the registration, contrasting `_REPAIR_DIFF_CAP` explicitly |
| SPEC A6 — `_build_builder_prompt` forwards it unchanged | DONE | G5 AST; B7 test asserts text equality with `compose_builder_prompt(...).text` |
| SPEC B — vocabulary referenced by NAME, never retyped | DONE | the three `REJECTION_FINDINGS_*` constants are imported; no heading string is spelled out in the test file |
| SPEC B1 — hostile reason as an EXACT SUBSTRING | DONE | `test_a_hostile_reason_reaches_the_composed_prompt_as_an_exact_substring` and `test_each_hostile_feature_survives_on_its_own` (8 labelled cases) |
| SPEC B2 — a reason ending in a newline keeps it | DONE | `test_a_reason_ending_in_a_newline_keeps_that_newline` |
| SPEC B3 — no rejection ⇒ no entry, byte-equal to the no-parameter call | DONE | `test_no_rejection_registers_no_segment_and_changes_no_byte`, over `None`, an empty ledger and an approvals-only ledger |
| SPEC B4 — directive still LAST, rejections after repair | DONE | `test_the_directive_is_still_the_last_segment_when_rejections_are_present`, `test_rejections_sit_between_the_repair_findings_and_the_directive` |
| SPEC B5 — ranks stay non-decreasing | DONE | `test_manifest_ranks_stay_non_decreasing_with_the_segment_present`, three shapes |
| SPEC B6 — malformed ledger composes without raising, registers nothing | DONE | `test_a_malformed_ledger_composes_without_raising_and_registers_nothing` (6 malformed inputs) and `test_a_ledger_whose_second_entry_is_broken_registers_nothing_at_all` |
| SPEC B7 — `_build_builder_prompt` forwards the parameter | DONE | `test_build_builder_prompt_forwards_the_parameter_unchanged` |
| Constraint 3 — no path outside the change set | HELD | G8, both directions. `.agent/context.md`, `.agent/decisions.md` and every `docs/` path untouched |
| Constraint 6 — destructive work in a worktree only, primary clean | HELD | worktree added, used, removed, pruned; `git status --porcelain` empty |
| Constraint 7 — `.agent/STOP` re-read before starting | HELD | `ls` reported "No such file or directory" before any work |
| Push the branch | DONE | `98ce168e..90fdaee5`, REAL exit 0 |
| Do not create or merge a PR; do not touch `main` | HELD | no `gh` command run; branch-only work |

Nothing in the Bundle was skipped, deferred or partially applied.

## Deviations & assumptions

The block's ordered commit sequence — C0a, C0b, C1, C2, C3, C4, C5, C6 — was
followed EXACTLY. No commit was added, dropped, reordered or split.

**D1 — I corrected a false symbol name in my OWN prose before committing C4.**
SPEC A5(i) orders the deliberate absence to be documented "where a reader would
search for it" but names no function, so the wording is mine. My first draft
wrote ":func:`run_pingpong_loop`" for the call site that composes the builder
prompt. The mandatory self-review loop caught it: an AST walk of
`packages/orchestration/pingpong_loop.py` shows the two callers of
`compose_builder_prompt` are `_build_builder_prompt` (line 1005) and
`run_pingpong` (line 2556) — there is NO function named `run_pingpong_loop` in
the module at all, only the MODULE is so named. The committed text says
`run_pingpong`. Declared because a doc cross-reference that resolves to nothing
is exactly the kind of unmeasured claim this process exists to catch, and because
the fix happened before the commit rather than after, so the diff does not show it.

**D2 — G6(ii)'s anchor spans TWO adjacent blocks, not one.** "Register the
rejections spec AFTER the `builder_directive` spec instead of before it" is a
REORDERING, and a single-block anchor cannot express one. The anchor is therefore
the guarded rejections append immediately followed by the directive append, and
the replacement is the same two blocks with their order swapped. The script
asserted that composite anchor occurs EXACTLY ONCE (reported as 1) before
applying it, which is the property the block actually asks for. No text was
invented: both blocks are the committed bytes.

**D3 — the `__pycache__` purge found ZERO directories on every run.** The purge
ran before the control and before each mutation, as ordered; the worktree was
freshly created and every run used `python3 -B`, so no cache was ever written.
Reported as the measured 0 rather than presented as "purged", because "0 found"
and "purged a cache" are different facts and only the first was observed.

**D4 — `git worktree remove` was run WITHOUT `--force` and succeeded.** The R20
handback recorded that its worker used `--force` without first trying the plain
form, and was right to say it could not then claim the flag was necessary. I tried
the plain form first: `git -C .remedy-wt/r21-mut status --porcelain` was EMPTY and
`git worktree remove` succeeded with no flag. So on this evidence the flag is NOT
necessary for this workflow.

**D5 — G6(i) reddened three tests in the new file besides the six golden ones.**
The block ordered only that `test_builder_prompt_golden.py` go RED, and it did.
The extra red is correct behaviour — `test_no_rejection_registers_no_segment_and_changes_no_byte`
and the two malformed-ledger tests all assert that NO segment is registered when
there is no rejection, which is precisely what removing the guard breaks — but it
is more than the block predicted, so it is declared rather than folded into a
"as expected". The gate's own condition is met on its own terms.

**D6 — gate scripts were written to files under `.remedy-wt/` instead of inline
heredocs.** The sandbox denies a heredoc nested inside `bash -c '...'`, and
Constraint 5 requires the `bash -c '<cmd>; echo "REAL_EXIT=$?"'` form with no
pipe. The two are only compatible if the command is a script path. Files added:
`r21_extract.py`, `g1_g2.py`, `g3.py`, `g4.py`, `g5.py`, `g6.py`, `g8.py`. All are
ADDITIONS to gitignored scratch; nothing pre-existing under `.remedy-wt/` was
edited or deleted, and `.remedy-wt/f033-r21-block.md` was only ever read.

**D7 — the G3 negative control was applied in MEMORY.** The block says "flip one
byte ... and show BOTH readers reject the flipped file". Writing a flipped file
into the working tree would have made `git status --porcelain` non-empty and put
Constraint 6 and G8 at risk if anything went wrong mid-run. The flip is applied to
the committed bytes in memory and both readers are run over those bytes; the
script proves the flip changed exactly one byte, at a reported offset proved to
lie inside the first appended paragraph's proved span, with the length unchanged.
The property the gate asks for is measured in full; only the storage medium
differs.

**No assumption was made that a measurement could have settled.** Nothing was
guessed, and no gate was weakened, skipped or reinterpreted.

**One observation about the block itself, which is NOT a deviation:** no slice
looked wrong and none needed applying-as-written-under-protest. PLAN21, RECORD21
and SLIPS21 all applied cleanly and every arithmetic figure the block stated in
advance — 1575558, 29663, 307, 52/50, 18/15, 257 — was confirmed by measurement
before it was relied on.

## Next

Hand back to the reviewer for the round 21 verdict. The reviewer re-runs G1-G8 at
`90fdaee5` and reads the real diff. If it PASSES, the next round is the one
`.agent/plan.md` step 2 names: locate where a recorded hunk decision is STORED —
`packages/orchestration/hunk_decision_record.py` builds the ledger and persists
nothing — so that `run_pingpong` can supply the `hunk_ledger` parameter this round
added but deliberately left unfed, and carry the two-round end-to-end the
Acceptance asks for. No pull request is open and none should be created yet.
