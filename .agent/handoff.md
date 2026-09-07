# Handback — F272 round 22

## Session

SESSION 10 of feature F272 · round 22 · rounds so far 22

Soft limit under amend0906-triage-throughput: 12 sessions and 40 rounds. At
session 10 and round 22 the feature is INSIDE the limit, so no scope report is
owed and no `SITZUNGS-LIMIT` line is emitted.

Context self-assessment: comfortable with wide margin. This was a one-line
repair round; the session read AGENTS.md, the handback template, the 277-line
block and the target region of `docs/system/architecture.md` in full, and ran
every gate serially in the primary checkout without needing a worktree.

## Range

Review of `3ca66aac`..`26045c8e`, the six-commit sequence C0a, C0b, C1, C2, C3,
C4. The C5 commit that writes this file follows `26045c8e` and cannot name its
own SHA, exactly as round 21's handback did.

## Commits

Six commits, every one single-parent, in the block's ordered sequence C0a, C0b,
C1, C2, C3, C4. C5 writes this file and cannot table itself. Every `+/-` cell
below is `git diff --numstat <parent> <commit>` and matches G7 cell for cell.

### b00d732d f272: save the round 22 step block verbatim  (C0a)
| Path | +/- | Reason |
|------|-----|--------|
| .agent/authored/f272-r22.md | +277 / -0 | `shutil.copyfile` of the delivered block, byte for byte |

### ee6aa8c2 f272: mirror the round 22 block into the last-block slot  (C0b)
| Path | +/- | Reason |
|------|-----|--------|
| .agent/last_block.md | +165 / -289 | `shutil.copyfile` of the same bytes over round 21's block |

### b7dd3889 f272: point the plan at the round 21 repair  (C1)
| Path | +/- | Reason |
|------|-----|--------|
| .agent/plan.md | +16 / -15 | replaced byte for byte with PLANF272R22 |

### 61855d98 f272: book the round 21 FAIL verdict and register R-0824  (C2)
| Path | +/- | Reason |
|------|-----|--------|
| .agent/live_review.md | +4 / -0 | append RECORDR22 — the round 21 FAIL gate entry and the R-0824 registration, PERSISTED BEFORE the repair |

### 80c5b6b6 f272: name the deleted run-loop without spelling it as an invocation  (C3)
| Path | +/- | Reason |
|------|-----|--------|
| docs/system/architecture.md | +4 / -1 | pair P1, the repair: the sentence now names `job run-loop` without the `remedy ` prefix |

### 26045c8e f272: resolve R-0824 in the record  (C4)
| Path | +/- | Reason |
|------|-----|--------|
| .agent/live_review.md | +2 / -0 | append DONER22, resolving R-0824 after the repair landed |

### (C5) f272: hand back round 22 on the R-0824 repair
| Path | +/- | Reason |
|------|-----|--------|
| .agent/handoff.md | this file | the handback; a commit cannot table itself (R-0149 pattern) |

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C0a  | done   | `shutil.copyfile` `.remedy-wt/f272-r22-block.md` -> `.agent/authored/f272-r22.md` |
| C0b  | done   | `shutil.copyfile` of the same source -> `.agent/last_block.md` |
| C1   | done   | `.agent/plan.md` byte-equal to PLANF272R22, 2605 bytes, 49 lines |
| C2   | done   | RECORDR22 appended, proved against its own pre-image at 1186986 bytes |
| C3   | done   | P1 applied, FROM 1x->0x and TO 0x->1x |
| C4   | done   | DONER22 appended, proved against its own pre-image at 1193650 bytes |
| C5   | done   | this file, written once |

## External actions

| Command | Outcome |
|---------|---------|
| `git push -u origin feature/f272-one-world-completion` | see the push transcript below; run after C5 |

No worktree was added or removed (block constraint 9), no PR was created,
edited or merged, no `gh` command was run.

## Verification

One line per gate, transcripts below each. Every gate ran with
`bash -c '<cmd>; echo "REAL_EXIT=$?"'`, no pipe between the command and the
echo, in the primary checkout, before C5.

**G1 TRANSPORT — PASS, REAL_EXIT=0.** All three files share one sha256, one byte
length and one line count.

    .remedy-wt/f272-r22-block.md   13d10059a62be82131c8d5ea90f2a1fe419c8aa490f8a8b60c78d599942ad73b   22595 bytes  277 lines
    .agent/authored/f272-r22.md    13d10059a62be82131c8d5ea90f2a1fe419c8aa490f8a8b60c78d599942ad73b   22595 bytes  277 lines
    .agent/last_block.md           13d10059a62be82131c8d5ea90f2a1fe419c8aa490f8a8b60c78d599942ad73b   22595 bytes  277 lines
    ONE_SHA256   True 13d10059a62be82131c8d5ea90f2a1fe419c8aa490f8a8b60c78d599942ad73b
    ONE_BYTELEN  True 22595
    ONE_LINECNT  True 277
    DELIVERED_DIGEST_MATCHES_BRIEF True
    REAL_EXIT=0

**G2(a) BYTE, twice, each against its OWN pre-image — PASS.** The C2 pre-image is
1186986 bytes, exactly as the block stated.

    === C2 (slice RECORDR22) ===
    pre_len             1186986
    pre_sha256          57d68efac9db84febae0f91c4b5aaeb8973f4e08f93733c6ce2afb9aa0371ccf
    pre_terminal12      b'st of T004.\n'
    pre_trailing_nl_run 1
    post_len            1193650
    post_sha256         9e316f3dbbc8021b8bf86826a1d36759707c98cd94f04ba9f2c1fd6d667fe205
    post_terminal12     b'es nothing.\n'
    post_trailing_nl_run 1
    PRE_IS_BYTE_EXACT_PREFIX_OF_POST True
    POST_EQUALS_PRE_NL_SLICE         True

    === C4 (slice DONER22) ===
    pre_len             1193650
    pre_sha256          9e316f3dbbc8021b8bf86826a1d36759707c98cd94f04ba9f2c1fd6d667fe205
    pre_terminal12      b'es nothing.\n'
    pre_trailing_nl_run 1
    post_len            1195379
    post_sha256         88040b630cc1a85df824001c22d4a5736124d4a6e991c28829bf7f800b8efcb8
    post_terminal12     b'e document.\n'
    post_trailing_nl_run 1
    PRE_IS_BYTE_EXACT_PREFIX_OF_POST True
    POST_EQUALS_PRE_NL_SLICE         True

**G2(b) STRUCTURAL, twice — PASS.** N is counted by the script from each slice,
never read from the block: 2 for RECORDR22, 1 for DONER22.

    C2: N (counted from slice) 2   units_before 723   units_after 725
        LAST_N_UNITS_EQUAL_SLICE_PARAS_IN_ORDER True
        EVERYTHING_BEFORE_UNCHANGED             True
    C4: N (counted from slice) 1   units_before 725   units_after 726
        LAST_N_UNITS_EQUAL_SLICE_PARAS_IN_ORDER True
        EVERYTHING_BEFORE_UNCHANGED             True

**G2(c) NEGATIVE CONTROL — PASS.** One byte flipped in the FIRST paragraph C2
appended, in memory only; both readers rejected it and the disk was re-read and
found byte-identical to the real post-image.

    NEGCTRL_flipped_offset_in_first_para 50
    NEGCTRL_BYTE_READER_REJECTS       True
    NEGCTRL_STRUCT_READER_REJECTS     True
    NEGCTRL_DISK_UNTOUCHED            True
    NEGCTRL_DISK_SHA256               9e316f3dbbc8021b8bf86826a1d36759707c98cd94f04ba9f2c1fd6d667fe205

**G2(d) COUNTS — PASS, REAL_EXIT=0.** All seven ordered counts measured, none
adjusted. "before" is `git show 3ca66aac:.agent/live_review.md`, "after" is disk.

    ^- R-\d{4} distinct       307 ->  308   ordered  307 ->  308   MATCH
    ^Done: R-\d{4} distinct   250 ->  251   ordered  250 ->  251   MATCH
    open set BY DISTINCT ID     57 ->   57   ordered   57 ->   57   MATCH
    ^Gate:                      44 ->   45   ordered   44 ->   45   MATCH
    ^Gate: F272 R21              0 ->    1   ordered    0 ->    1   MATCH
    ^- R-0824                    0 ->    1   ordered    0 ->    1   MATCH
    ^Done: R-0824                0 ->    1   ordered    0 ->    1   MATCH

    OPEN FINDINGS BY DISTINCT ID, arithmetic:
      before: registered distinct 307 - resolved distinct 250 = open 57
      after : registered distinct 308 - resolved distinct 251 = open 57
      delta : +1 minted (R-0824), +1 resolved (R-0824), open unchanged at 57
      R-0825 free (not registered): True
    ALL_ORDERED_COUNTS_MATCH True
    REAL_EXIT=0

**G3 THE PLAN — PASS, REAL_EXIT=0.** 2605 bytes, 49 lines against the AGENTS.md
cap of 50, byte-equal to PLANF272R22, both headings present.

    plan_bytes             2605
    plan_lines             49
    AGENTS_md_cap          50
    UNDER_CAP              True
    slice_sha256           7bd36621d7af51788080dc0f850d36b16db3bc9ddd2a5042bfcc130bc62d4bb2
    disk_sha256            7bd36621d7af51788080dc0f850d36b16db3bc9ddd2a5042bfcc130bc62d4bb2
    BYTE_EQUAL_TO_SLICE    True
    HAS_GOAL_HEADING       True
    HAS_NEXT_STEPS_HEADING True
    REAL_EXIT=0

**G4 THE ORDERED COLOUR — PASS.** (i) REAL_EXIT=1 at the base commit BEFORE C3,
(ii) REAL_EXIT=0 at C3 with 5 passed. The red was OBSERVED on disk, not
manufactured: it was the branch's real state at `3ca66aac`. The failing test is
the one round 21 added, node id
`tests/cli/test_advertised_commands.py::test_every_operator_facing_advertised_command_exists_in_the_catalog`
in both runs.

    (i) at 3ca66aac, before C3:
    $ python3 -B -m pytest tests/cli/test_advertised_commands.py -q -p no:randomly
    .F...                                                                    [100%]
    FAILED tests/cli/test_advertised_commands.py::test_every_operator_facing_advertised_command_exists_in_the_catalog
    E   AssertionError: an operator-facing script or page advertises commands the catalog does
        not carry — delete a command's advertisements in the same commit as the command:
    E     docs/system/architecture.md:927: remedy job run-loop
    E   assert not ['docs/system/architecture.md:927: remedy job run-loop']
    1 failed, 4 passed in 0.30s
    REAL_EXIT=1

    THE UNRESOLVED LIST IN FULL, one entry:
      docs/system/architecture.md:927: remedy job run-loop
    NO OTHER PATH appears in it.

    (ii) at C3 (80c5b6b6):
    $ python3 -B -m pytest tests/cli/test_advertised_commands.py -q -p no:randomly
    .....                                                                    [100%]
    5 passed in 0.34s
    REAL_EXIT=0

    Node id present in both runs, from --collect-only at C3:
    tests/cli/test_advertised_commands.py::test_every_operator_facing_advertised_command_exists_in_the_catalog

**G5 NOTHING ELSE MOVED — PASS, four suites run serially, every REAL_EXIT=0.**

    $ python3 -B -m pytest tests/cli/test_product_spine.py -q -p no:randomly
    72 passed in 0.28s
    REAL_EXIT=0

    $ python3 -B -m pytest tests/test_remedy_smoke_script.py -q -p no:randomly
    191 passed in 0.44s
    REAL_EXIT=0

    $ python3 -B -m pytest tests/docs/ -q -p no:randomly
    303 passed in 0.49s
    REAL_EXIT=0

    $ python3 -B -m pytest tests/cli/test_golden_path.py -q -p no:randomly
    42 passed in 21.02s
    REAL_EXIT=0

    Collector counts at C3, PRINTED and not asserted:
    production collector      seen=738 unresolved=0 []
    operator-facing collector seen=403 unresolved=0 []
    (base-commit reference figures: 738 and 404)
    REAL_EXIT=0

**G6 THE STRING IS GONE FROM THE SWEPT CORPUS — PASS, REAL_EXIT=0.** Zero in all
three trees, over TRACKED files.

    docs/system/   files=68   occurrences of 'remedy job run-loop' = 0
    scripts/       files=65   occurrences of 'remedy job run-loop' = 0
    docs/guides/   files=20   occurrences of 'remedy job run-loop' = 0
    docs/guides/   bare 'job run-loop' (prefix-less, must be > 0): 1
    architecture.md BEFORE bytes 147890 lines 3065
    architecture.md AFTER  bytes 148040 lines 3068
    REAL_EXIT=0

The `docs/guides/` reading is the one the block asked for as a survival check
rather than a sweep check: the migration-table row still carries `job run-loop`
WITHOUT the `remedy ` prefix, so its zero above proves the row survived rather
than that it was deleted.

**G7 THE TREE — PASS, REAL_EXIT=0.** `git status --porcelain` was EMPTY at every
commit boundary; the real output was captured after each of C0a, C0b, C1, C2,
C3, C4 and was the empty string every time.

    commits in 3ca66aac..HEAD: 6
    C0a  b00d732d  insertions=277  under_500=True  parents=1  f272: save the round 22 step block verbatim
             .agent/authored/f272-r22.md +277 -0
    C0b  ee6aa8c2  insertions=165  under_500=True  parents=1  f272: mirror the round 22 block into the last-block slot
             .agent/last_block.md +165 -289
    C1   b7dd3889  insertions=16   under_500=True  parents=1  f272: point the plan at the round 21 repair
             .agent/plan.md +16 -15
    C2   61855d98  insertions=4    under_500=True  parents=1  f272: book the round 21 FAIL verdict and register R-0824
             .agent/live_review.md +4 -0
    C3   80c5b6b6  insertions=4    under_500=True  parents=1  f272: name the deleted run-loop without spelling it as an invocation
             docs/system/architecture.md +4 -1
    C4   26045c8e  insertions=2    under_500=True  parents=1  f272: resolve R-0824 in the record
             .agent/live_review.md +2 -0
    git ls-files .remedy-wt -> '' (EMPTY=True)
    git status --porcelain -> '' (EMPTY=True)
    REAL_EXIT=0

Every per-commit insertion count is under the DECISION F104 D1 cap of 500; the
largest is C0a at 277. C5 is excluded, because a commit cannot count its own
insertions while it is being written.

THE THREE `.agent/STOP` READINGS, all with `os.path.exists`, per constraint 8:

    before C0a: False
    before C3 : False
    before C5 : False

No ruff reading is owed: no `.py` file changed this round.

## Authored-text proofs

Every authored slice was extracted PROGRAMMATICALLY from the committed
`.agent/authored/f272-r22.md` by `.remedy-wt/r22_slice.py`, between its
`<<<BEGIN NAME>>>` and `<<<END NAME>>>` lines, inclusive of the newline ending
the last content line. Nothing was retyped.

| Slice | Target | Disk-to-disk result |
|-------|--------|---------------------|
| PLANF272R22 | .agent/plan.md | BYTE_EQUAL_TO_SLICE True; both sha256 `7bd36621d7af51788080dc0f850d36b16db3bc9ddd2a5042bfcc130bc62d4bb2` |
| RECORDR22 | .agent/live_review.md (append) | POST_EQUALS_PRE_NL_SLICE True; LAST_N_UNITS_EQUAL_SLICE_PARAS_IN_ORDER True at N=2 |
| DONER22 | .agent/live_review.md (append) | POST_EQUALS_PRE_NL_SLICE True; LAST_N_UNITS_EQUAL_SLICE_PARAS_IN_ORDER True at N=1 |
| P1 FROM / P1 TO | docs/system/architecture.md | pre-edit FROM 1x, TO 0x, `TO contains FROM: False`; post-edit FROM 0x, TO 1x |

## Deviations & assumptions

NO DEPARTURE FROM THE BLOCK'S ORDERED COMMIT SEQUENCE. Six commits, C0a, C0b,
C1, C2, C3, C4, in that order, with C5 writing this file — no extra commit, no
dropped one, no reordering. No path outside the declared change set was touched:
`tests/cli/test_advertised_commands.py` was NOT edited, and neither was anything
under `tests/`, `packages/`, `apps/` or `scripts/`.

1. OBSERVATION, not a deviation — THE OPERATOR-FACING COLLECTOR'S `seen` COUNT
   FELL 404 TO 403. The block printed 404 as the base-commit figure and
   explicitly ordered this count PRINTED rather than asserted. The drop of
   exactly one is the arithmetic the repair predicts: the deleted string
   `remedy job run-loop` was itself one of the 404 matches, and it was the one
   unresolved match, so removing it takes `seen` down by one and `unresolved`
   down from one to zero. The production collector is unmoved at 738, as
   expected: no `.py` file changed. Both collectors remain far above the
   guard's anti-blindness floors, so neither went blind.

2. ASSUMPTION — THE APPEND SEPARATOR IS A SINGLE BLANK LINE. `POST_EQUALS_PRE_NL_SLICE`
   was read as `post == pre + b"\n" + slice`. This was probed rather than
   assumed from convention: at the pre-image the file ends in exactly one
   newline (`trailing_nl_run 1`) and contains 722 occurrences of `\n\n` and ZERO
   of `\n\n\n`, so one blank line is the file's only paragraph separator and any
   other separator would have produced a run of three newlines this file has
   never contained.

3. ASSUMPTION — THE STRUCTURAL READER SPLITS ON `\n{2,}`. Since the file
   contains no `\n\n\n`, this is identical to splitting on `\n\n` on the real
   data; the wider pattern is used only so that a future multi-blank-line append
   could not silently pass the reader.

4. NO DISAGREEMENT WITH THE BLOCK. Every constraint was satisfiable as written
   and no gate contradicted another. Constraint 4's stated pre-edit readings
   were re-measured before applying P1 rather than trusted: FROM 1x, TO 0x,
   `TO contains FROM: False`, all confirmed. Constraint 10's claim that neither
   collector's corpus reaches `.agent/` is consistent with G5's counts being
   unchanged in the production collector after two `.agent/live_review.md`
   appends that between them contain two literal `remedy job run-loop` strings.

5. SCRATCH — eight helper scripts were written under the gitignored
   `.remedy-wt/`: `r22_slice.py`, `r22_append.py`, `r22_g1.py`, `r22_g2d.py`,
   `r22_g3.py`, `r22_g5_counts.py`, `r22_g6.py` and `r22_g7.py` — counted from
   that enumeration, which holds eight names. `git ls-files .remedy-wt` is
   EMPTY, so none of them reached the index.

## Next

The classic store deletion that leads T004, per `.agent/plan.md` Next Step 1:
the next-action rails advertising `remedy job run-next` all sit in functions
typed `job: Job`, so the classic record must move before the advertisements can,
and DECISION F272 D13 forbids deleting a command ahead of its advertisements.
Awaiting the reviewer's verdict on round 22 and the round 23 block.

## Reviewer verdict — round 22

VERDICT PASS. Every gate was RE-RUN by the reviewer rather than read, in the primary
checkout at `b926992b`.

- Range `3ca66aac`..`b926992b`, seven commits, every one single-parent, in exactly the
  ordered sequence C0a, C0b, C1, C2, C3, C4, C5. The change set is exactly the six
  ordered paths and nothing else — `git diff --stat` names `.agent/authored/f272-r22.md`,
  `.agent/handoff.md`, `.agent/last_block.md`, `.agent/live_review.md`, `.agent/plan.md`
  and `docs/system/architecture.md`. Nothing under `tests/`, `packages/`, `apps/` or
  `scripts/` moved, which is the constraint that matters most this round: THE GUARD WAS
  NOT EDITED.
- G1 TRANSPORT IS A REAL CHAIN AND NOT MERELY SELF-CONSISTENT: the reviewer's own scratch
  original `.remedy-wt/f272-r22-block.md`, written and hashed BEFORE delegation, and the
  committed `.agent/authored/f272-r22.md` and `.agent/last_block.md` are all 22595 bytes
  at 277 lines and all hash to
  `13d10059a62be82131c8d5ea90f2a1fe419c8aa490f8a8b60c78d599942ad73b`. Per §3 item 37 that
  chain covers those three artefacts and is not a claim about the bytes emitted into a
  prompt.
- G2 THE RECORD reproduces on both appends: `.agent/live_review.md` 1186986 to 1193650 to
  1195379, each proved against its own pre-image, and all seven ordered counts reproduce
  exactly — registrations 307 to 308, resolutions 250 to 251, open set BY DISTINCT ID 57
  unchanged, `^Gate: ` 44 to 45, `^Gate: F272 R21 ` 0 to 1, `^- R-0824 ` 0 to 1 and
  `^Done: R-0824 ` 0 to 1. The open set is unchanged because this round both minted and
  resolved the id; the arithmetic closes at 308 − 251 = 57.
- G3 THE PLAN is 49 lines against the AGENTS.md cap of 50, byte-equal to its slice.
- G4 THE ORDERED COLOUR IS OBSERVED, NOT MANUFACTURED, which is the strongest form this
  gate takes: the red existed on disk at `3ca66aac` before the round began — EXIT 1 with
  an unresolved list of exactly one entry, `docs/system/architecture.md:927: remedy job
  run-loop` — and at C3 the same node id is EXIT 0. No mutation was invented, because the
  defect itself was the mutation.
- G5 and G6 re-run by the reviewer as one serial invocation: 613 passed, EXIT 0, across
  `tests/cli/test_advertised_commands.py`, `tests/cli/test_product_spine.py`,
  `tests/test_remedy_smoke_script.py`, `tests/docs/` and `tests/cli/test_golden_path.py`.
  The exact string `remedy job run-loop` counts 0 in `docs/system/` and 0 in `scripts/`.
- G7 THE TREE: `git status --porcelain` empty, `git ls-files .remedy-wt` empty, and every
  per-commit insertion under the DECISION F104 D1 cap of 500 at a maximum of 277.

THE REPAIR IS THE RIGHT ONE AND WAS VERIFIED BEFORE IT WAS ORDERED. The reviewer ran the
SHIPPED `scan_advertised_commands` over P1's TO before emission and it yields ZERO
advertisements — the check whose absence caused the round 21 failure, run this time
against the widened corpus rather than the old one.

THE WORKER'S DEVIATIONS ARE ACCEPTED AND ITS ONE DECLARED PROSE INACCURACY SPENDS NOTHING.
Deviation 1 is not a deviation but an honest arithmetic note: the operator-facing
collector's `seen` falls 404 to 403 because the deleted string was itself one of the 404
matches, and both collectors stay far above their anti-blindness floors. The note that
`.agent/handoff.md` says "see the push transcript below" where no such transcript exists
is correct, declared, and self-healing — that file is rewritten every round — so under
amend0827 rule 2 it earns no id and no round.

## Session

SESSION 10 OF F272 ENDS HERE, after three delegated rounds — 20, 21 and 22. Round 20
PASSED at the first attempt. ROUND 21 FAILED, on the reviewer's block rather than on the
worker's execution, and round 22 is its repair and PASSED. F272's soft limit under
amend0906-triage-throughput is 12 sessions and 40 rounds; at session 10 and round 22 the
feature is inside it, so NO SCOPE REPORT IS OWED.

Why the session ends below the six-to-eight round target, in one sentence as amend0906
rule 3 requires: the reviewer authored a block that ordered a string written into a file
the same block ordered swept to zero, which cost a FAIL and a repair round out of the
three this session ran, and the honest reading of that is the accumulating-authoring-error
signal amend0905-throughput names as a reason to stop rather than to keep authoring.

CONTEXT SELF-ASSESSMENT (amend0905-throughput): context was substantial but not the
binding constraint; it was spent on a large pre-authoring measurement campaign — the
classic-runner component, the advisory-rail typing and two dry runs of production changes
in disposable worktrees before any block was written — plus three independent gate re-runs
including a full suite, and the reviewer's own error rate rather than its remaining room
is what ends the session.

## Owed by round 23's first commits, per amend0827 rule 1

Exactly these, and nothing else — no id is minted for any of them:

1. The `Gate: F272 R22` PASS entry recorded in the verdict section above, appended to
   `.agent/live_review.md`.
2. TWO dated lines appended to `.agent/prose_slips.md`, both the reviewer's own and
   neither touching disk state, both from the round 21 block:
   - 2026-09-07, F272 round 21 — SMOKESPEC's S1 and S2 bounded each deleted section as
     ending at "the last line before the next `_SMOKE_SECTION=` assignment", which
     swallows the FOLLOWING section's banner comment and contradicts the same spec's S4
     and its own "delete section in full"; the worker measured the conflict and used the
     banner-to-banner reading, which is the one that satisfies both sentences. A span
     ordered for deletion is bounded by the anchor that OPENS the next unit, never by the
     assignment inside it.
   - 2026-09-07, F272 round 21 — the block's change set omitted
     `tests/test_remedy_smoke_script.py` while ordering the deletion of the two smoke
     sections four of its tests pin by text, so the worker had to leave the declared change
     set to keep the suite green; `agent_loop` and `agent_loop_task_exit` both reach zero
     occurrences in the script, so at least two of those deletions were forced. Before
     ordering a section deleted, grep the suite for tests that assert that section's text.

## Next

THE NEXT SESSION'S FIRST ACTION: run Phase 0, the state probe; then check `.agent/STOP`
under Phase 1 rule 1 BEFORE the Open PR Gate under rule 2, in that order. No PR exists for
this branch and none was created.

T001, T002 AND T003 ARE COMPLETE. T004 is under way: round 19 deleted the `job run-loop`
command surface, and rounds 20 through 22 repaired the advertisements that deletion left
behind and shipped `tests/cli/test_advertised_commands.py`, the standing guard that makes
the class visible in every medium an operator reads — tracked `.py` under `packages/` and
`apps/`, tracked `.sh` under `scripts/`, and tracked `.md` under `docs/system/` and
`docs/guides/`.

ROUND 23 IS THE CLASSIC STORE DELETION, AND THE ORDERING THAT PUTS IT FIRST WAS MEASURED
THIS SESSION AT `5f4f0405` RATHER THAN ASSUMED. Every next-action rail that advertises
`remedy job run-next` — in `cockpit.py`, `timeline.py`, `trust_report.py`, `dashboard.py`,
`brain_detail.py`, `agent_loop.py` and `autonomy_loop.py` — sits inside a function whose
job parameter is annotated `job: Job`, the CLASSIC record; not one of them takes a
`JobPlan`. So none can be pointed at `remedy do job-run`, whose argument is a 16-character
JobPlan id, and DECISION F272 D13 forbids deleting a command ahead of its advertisements.
The advertisements cannot move before the classic record does, which is why the store
deletion now LEADS T004 instead of following it.

WHAT ROUND 23 SHOULD NOT RE-DERIVE, all measured this session:

- `.agent/f272_t004_deletion_inventory.md` bounds the store at 199 tracked files, 72 under
  `packages/` and `apps/` and 127 under `tests/`, with `save_job` in 152 and `load_job` in
  105. That file, not a grep, stages the work.
- THE CLASSIC RUNNER IS ONE CONNECTED COMPONENT and cannot be cut piecewise:
  `_cmd_job_run_cycles` (143 lines) calls `_cmd_run_next_task_local` (243);
  `_cmd_job_resume` (150) calls `_cmd_job_run_cycles`, `_resume_preview` (57) and
  `_print_resume_preview` (41); and `agent_loop._run_next_task_step` (4), reached only
  from `run_agent_loop` (127), calls `_cmd_run_next_task_local` as well.
- `agent_loop.py` SURVIVES T004. The round 19 handback called the module
  production-unreachable and that is corrected in DECISION F272 D13: `apps/cli/commands/
  brain.py` imports `derive_agent_loop_state` and `summarize_agent_loop_state` from it for
  `remedy dev agent-loop`, so only `run_agent_loop` and its private helpers are unreachable.
- `job.run` is the catalog's ONLY `is_expensive` command, pinned by three tests in
  `tests/test_command_catalog.py`, so F114's cost preview needs a named carrier before it
  can be deleted.
- `tests/cli/test_plan_approval.py` shells out to `remedy job run-next` at lines 372 and
  716 to prove the approval gate blocks execution; a dry run of the three-line catalog cut
  turned exactly those two red with `Error: Unknown command 'run-next'`.
- THE FULL SUITE IS GREEN AT `b926992b` IN THE PRIMARY CHECKOUT: EXIT 0, 19784 passed, 23
  skipped, measured at round 20's C4 and unchanged by rounds 21 and 22, neither of which
  touched `packages/` or `apps/`. A deletion round's full-suite measurement must name the
  primary checkout: the same run inside a fresh worktree fails about ten tests for want of
  `apps/ui/node_modules`.
