# Handback — F272 round 23

## Session

SESSION 11 of feature F272 · round 23 · rounds so far 23

Soft limit under amend0906-triage-throughput: 12 sessions and 40 rounds. At
session 11 and round 23 the feature is INSIDE the limit, so no scope report is
owed and no `SITZUNGS-LIMIT` line is emitted.

Context self-assessment: comfortable with wide margin. The session read
AGENTS.md, the handback template and the 367-line block in full, read both
target regions of `do_cmd.py` and `job_evidence.py` before editing them, and ran
every gate for real; the only long call was G5's `tests/orchestration/` at 12m19s.

## Range

Review of `67515ab7`..`222c211e`, the seven-commit sequence C0a, C0b, C1, C2, C3,
C4, C5. The C6 commit that writes this file follows `222c211e` and cannot name
its own SHA, exactly as rounds 21 and 22 did.

## Commits

Seven commits, every one single-parent, in the block's ordered sequence C0a, C0b,
C1, C2, C3, C4, C5. C6 writes this file and cannot table itself. Every `+/-` cell
below is taken from `git diff --numstat <parent> <commit>` and was compared cell
for cell against G7's figures.

### 79f6dd8f f272: save the round 23 block verbatim as the authored record
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f272-r23.md` | +367 / -0 | C0a — `shutil.copyfile` of `.remedy-wt/f272-r23-block.md`, 30290 bytes, 367 lines |

### 9edd01d2 f272: mirror the round 23 block into the last block slot
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/last_block.md` | +265 / -175 | C0b — same `shutil.copyfile`, replacing the round 22 block |

### b021f398 f272: point the plan at round 23 and the R-0825 repair
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/plan.md` | +29 / -29 | C1 — replaced byte for byte with the PLANF272R23 slice, 2592 bytes, 49 lines |

### 5249cd6e f272: book the round 22 PASS verdict and register R-0825
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/live_review.md` | +4 / -0 | C2 — RECORDR23 appended: the round 22 PASS gate entry owed by amend0827 rule 1, and the R-0825 registration; findings persist before the repair |

### 5de6f81a f272: record the two round 21 prose slips
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/prose_slips.md` | +4 / -0 | C3 — SLIPSR23 appended, the two dated round 21 lines round 22's handback records as owed |

### b63a88b6 f272: make both retired JobPlan status readers read state, pinned by behaviour tests and a standing scan
| Path | +/- | Reason |
|------|-----|--------|
| `apps/cli/commands/do_cmd.py` | +2 / -2 | C4 — pair P1: `getattr(_existing, "status", "") == "stopped"` becomes `_existing.state == JOB_STOPPED`, with the constant imported beside `load_job_plan` |
| `packages/orchestration/job_evidence.py` | +2 / -1 | C4 — pair P2: `_linked_job_summary` reads `state` through the `str(getattr(_state, "value", _state) or "")` idiom |
| `tests/orchestration/test_job_plan_state_reads.py` | +155 / -0 | C4 — NEW standing scan, `shutil.copyfile` of `.remedy-wt/f272-r23-new-guard.py`, 6473 bytes, 155 lines |
| `tests/orchestration/test_job_state_field.py` | +50 / -0 | C4 — `shutil.copyfile` of `.remedy-wt/f272-r23-state-field.py`, 8135 bytes, 169 lines; additions only plus the `import pytest` line, ZERO deletions, as constraint 4 requires |

### 222c211e f272: resolve R-0825 in the record
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/live_review.md` | +2 / -0 | C5 — DONER23 appended, resolving R-0825; it runs after C4 and after G4, per constraints 6 and 7 |

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C0a  | done   | |
| C0b  | done   | |
| C1   | done   | |
| C2   | done   | |
| C3   | done   | |
| C4   | done   | |
| C5   | done   | |
| C6   | done   | this commit; it rewrites this file and cannot table itself |

No commit was added, dropped or reordered. The bundle landed exactly as ordered.

## External actions

| Command | Outcome |
|---------|---------|
| `git worktree add /home/decodeux/Repos/remedy/.remedy-wt/r23-base 67515ab77f0d6a9103cdb4c521182ead37663590 --detach` | EXIT 0 — `Preparing worktree (detached HEAD 67515ab7)` |
| `git worktree remove --force /home/decodeux/Repos/remedy/.remedy-wt/r23-base` | EXIT 0, removed BY EXACT PATH; `git worktree list` afterwards shows only the primary checkout and the twelve pre-existing `remedy/job-*` product worktrees, no `r23-base`; `os.path.exists` on that exact path is `False` |
| `git push -u origin feature/f272-one-world-completion` (after C5) | EXIT 0 — `67515ab7..222c211e  feature/f272-one-world-completion -> feature/f272-one-world-completion`; branch set up to track origin |
| second `git push` carrying C6 | executed immediately after this commit; its real output is in the round report — a handback cannot contain the transcript of a push of itself |

No PR was created, nothing was merged, nothing was force-pushed, no history was
rewritten. No `gh` command was run.

## Verification

Every gate was run with `bash -c '<cmd>; echo "REAL_EXIT=$?"'`, no pipe between
the command and the echo. G1 through G6 all ran before C6; G4 additionally ran
before C5, as the block's gate preamble orders, because DONER23 states G4's
outcome. G2's C5 half and G7 are the readings that follow C5.

### G1 TRANSPORT — PASS, REAL_EXIT=0, 4 artifacts compared

    DELIVERED .remedy-wt/f272-r23-block.md
              sha256 4463fbcc8c9cf39bc51056ccb43e9c6be9449f16686e6ddc4058c3c250c44a0f
              30290 bytes, 367 lines
    COMMITTED .agent/authored/f272-r23.md
              sha256 4463fbcc8c9cf39bc51056ccb43e9c6be9449f16686e6ddc4058c3c250c44a0f
              30290 bytes, 367 lines   EQUALS_DELIVERED=True
    COMMITTED .agent/last_block.md
              sha256 4463fbcc8c9cf39bc51056ccb43e9c6be9449f16686e6ddc4058c3c250c44a0f
              30290 bytes, 367 lines   EQUALS_DELIVERED=True
    COMMITTED tests/orchestration/test_job_plan_state_reads.py
              sha256 573be0549248c8a7535d9bb2cd6e3ca68d32a31fd3c82dbad564cead2ff3bbf7
              6473 bytes, 155 lines
              MATCHES_CONSTRAINT4=True  EQUALS_DELIVERY_ARTIFACT=True
    COMMITTED tests/orchestration/test_job_state_field.py
              sha256 69e13d0d5e37156fece0d2979a3411072e356484d66852ec8a3569a8af8374f3
              8135 bytes, 169 lines
              MATCHES_CONSTRAINT4=True  EQUALS_DELIVERY_ARTIFACT=True
    ARTIFACTS_COMPARED=4

The delivered block's sha256, byte length and line count were verified against
the three figures the delegation stated BEFORE the block was read, and matched.

### G2 THE RECORD — PASS, REAL_EXIT=0 on both appends

(a) BYTE, C2:

    SLICE RECORDR23  6681 bytes, 3 lines, sha256 ca92ddd65fa22fdc56198a7c26fed4a7f24939cf99f3b511eb9ed202e343e2b9
    pre_len=1195379  pre_sha256=88040b630cc1a85df824001c22d4a5736124d4a6e991c28829bf7f800b8efcb8
    post_len=1202061 post_sha256=9fe9b8cd9f39341585d1f85ee1a22783eb7c09ea637383f9a74d25e8f1f5f186
    pre_terminal_12=b'e document.\n'  pre_trailing_nl_run=1
    post_terminal_12=b'_job_plan`.\n' post_trailing_nl_run=1
    PRE_IS_BYTE_EXACT_PREFIX_OF_POST True
    POST_EQUALS_PRE_NL_SLICE True

The C2 pre-image is 1195379 bytes at sha256 `88040b63…`, which is exactly the
figure the block states for the base commit.

(a) BYTE, C5:

    SLICE DONER23  2737 bytes, 1 line, sha256 bc38a879826f8b8dc2cabe6ed644545366bb741eaffa7b01236fe2f83dba0240
    pre_len=1202061  pre_sha256=9fe9b8cd9f39341585d1f85ee1a22783eb7c09ea637383f9a74d25e8f1f5f186
    post_len=1204799 post_sha256=0a3287c979d7ebc52510df56b9c1c149571d6413b152bf61ba0e734e945c3315
    pre_terminal_12=b'_job_plan`.\n' pre_trailing_nl_run=1
    post_terminal_12=b' it CANNOT.\n'  post_trailing_nl_run=1
    PRE_IS_BYTE_EXACT_PREFIX_OF_POST True
    POST_EQUALS_PRE_NL_SLICE True

Each append was proved against its OWN pre-image: C5's pre-image sha256 is
byte-identical to C2's post-image sha256, so the two proofs chain.

(b) STRUCTURAL, C2 and C5. The reader strips the single terminal newline, splits
on `\n{2,}`, and compares the LAST N units against the slice's paragraphs in
order. N is counted by the script from the slice itself and was never taken from
the block:

    C2  N_COUNTED_FROM_SLICE=2  UNITS_BEFORE=726  UNITS_AFTER=728
        LAST_N_UNITS_EQUAL_SLICE_PARAGRAPHS_IN_ORDER True
        EVERYTHING_BEFORE_UNCHANGED True
    C5  N_COUNTED_FROM_SLICE=1  UNITS_BEFORE=728  UNITS_AFTER=729
        LAST_N_UNITS_EQUAL_SLICE_PARAGRAPHS_IN_ORDER True
        EVERYTHING_BEFORE_UNCHANGED True

(c) NEGATIVE CONTROL on the first paragraph appended by C2, in memory only, one
byte flipped by XOR at offset 1779, which is inside that first paragraph:

    NEGCTRL flipped_byte_offset=1779 inside_first_paragraph=True
    NEGCTRL BYTE_READER_REJECTS True
    NEGCTRL STRUCTURAL_READER_REJECTS True
    NEGCTRL FILE_UNTOUCHED_AFTER_CONTROL True
            sha256=9fe9b8cd9f39341585d1f85ee1a22783eb7c09ea637383f9a74d25e8f1f5f186

BOTH readers rejected the flipped image, and the file re-read after the control
is byte-identical to the real post-image. The same control was additionally run
for C5 (offset 1368) and for C3's SLIPSR23 (offset 258); both rejected by both
readers, both files untouched.

(d) COUNTS, each measured at the base commit via `git show` and at HEAD, none
adjusted to agree:

    ^- R-\d{4} distinct        308 -> 309
    ^Done: R-\d{4} distinct    251 -> 252
    ^Gate:                      45 -> 46
    ^Gate: F272 R22              0 -> 1
    ^- R-0825                    0 -> 1
    ^Done: R-0825                0 -> 1
    Done: LINES                253 -> 254

All seven ordered figures reproduce exactly. The `Done:` LINE count confirms the
block's arithmetic note: 253 lines carry 251 distinct ids at the base, because
two ids each carry a two-paragraph resolution.

    OPEN FINDINGS BY DISTINCT ID base = 308 - 251 = 57
    OPEN FINDINGS BY DISTINCT ID head = 309 - 252 = 57

The open set is UNCHANGED at 57 because this round both mints and resolves
R-0825. `R-0826` stays free: `^- R-0826` matches 0 times at HEAD.

### G3 THE TWO PROSE FILES — PASS, REAL_EXIT=0

    .agent/plan.md  2592 bytes, 49 lines
                    sha256 478442d29f3151bf3f45372e679d2def46a9f8985daa0b9818f32fbc8a1aa71a
    BYTE_EQUAL_TO_PLANF272R23 True
    LINES 49 against the AGENTS.md cap of 50 — UNDER_CAP True
    HAS_GOAL_HEADING True
    HAS_NEXT_STEPS_HEADING True

    .agent/prose_slips.md  pre_len=147269  post_len=148270
    POST_EQUALS_PRE_NL_SLICE True
    LINES_GAINED=4

`prose_slips.md`'s pre-image is 147269 bytes, exactly the figure the block states
for the base commit, and it gains 4 lines: the two dated slip lines plus the two
blank separators the paragraph convention carries.

### G4 THE ORDERED COLOUR — PASS. (i) REAL_EXIT=1 as required, (ii) REAL_EXIT=0

(i) In a disposable worktree at the BASE commit `67515ab7`, with ONLY the two
test artifacts copied in by `shutil.copyfile` and both production files left at
their base bytes — verified by digest before the run:

    UNTOUCHED apps/cli/commands/do_cmd.py
              sha256 c19a93a09ccccb32b395329e1ee36c3b0bc0de2d08eb5319a149ae6082890bb6, 126114 bytes
    UNTOUCHED packages/orchestration/job_evidence.py
              sha256 03e9adf25ef6fc9ae2f6ce9890f969692fadc6964fbfd3d821943070631b27a0, 141004 bytes
    PYCACHE_DIRS_PURGED=0   (the fresh worktree carried none)

An import-path probe was run first, because an editable install can shadow a
worktree; it does not here:

    packages.orchestration.job_evidence -> .remedy-wt/r23-base/packages/orchestration/job_evidence.py
    apps.cli.commands.do_cmd            -> .remedy-wt/r23-base/apps/cli/commands/do_cmd.py

Then, from the worktree root:

    python3 -B -m pytest tests/orchestration/test_job_state_field.py \
        tests/orchestration/test_job_plan_state_reads.py -q -p no:randomly
    3 failed, 14 passed in 2.64s
    REAL_EXIT=1

Exactly the three ordered node ids failed and no others:

    tests/orchestration/test_job_state_field.py::TestTheRenameLeftNoSilentReaderBehind::test_budget_flags_are_refused_on_a_stopped_job
    tests/orchestration/test_job_state_field.py::TestTheRenameLeftNoSilentReaderBehind::test_a_linked_job_that_loads_reports_its_real_state
    tests/orchestration/test_job_plan_state_reads.py::TestNoRetiredJobPlanStateReads::test_no_production_site_reads_the_retired_status_off_a_job_plan

The red is OBSERVED, not manufactured — the defect is its own mutation. The first
failure's captured stdout carries the product effect the finding names:

    Job 0123456789abcdef:
    Status: stopped
    ...
    WARNING: Real target repo was NOT mutated. ...
    Cost recorded to the ledger. See: remedy stats cost
    E       Failed: DID NOT RAISE <class 'SystemExit'>

The second failure prints the self-contradicting document:

    E   AssertionError: {'job_id': '0123456789abcdee', 'provider_call_count': None,
                         'source': 'persisted_job_state', 'status': 'unknown'}
    E   assert 'unknown' == 'completed'

The guard's own failure message IN FULL, and it names the two ordered sites AND
NO OTHER:

    E   AssertionError: a production site reads the retired `status` spelling off a
        JobPlan; F272 round 9 renamed that field to `state`, and a `getattr` with a
        default answers silently instead of raising — read `.state` instead:
    E       apps/cli/commands/do_cmd.py:1456: getattr(_existing, "status", ...)
    E       packages/orchestration/job_evidence.py:1494: getattr(j, "status", ...)
    E   assert ['apps/cli/co...tatus", ...)'] == []
    E     Left contains 2 more items, first extra item: 'apps/cli/commands/do_cmd.py:1456: getattr(_existing, "status", ...)'

(ii) In the PRIMARY checkout at C4 `b63a88b6`, the same command:

    17 passed in 2.23s
    REAL_EXIT=0

`--collect-only` in the primary checkout collects 17 tests, REAL_EXIT=0, the same
17 the worktree run accounted for as 3 failed + 14 passed:

    test_job_state_field.py::TestTheFieldIsState::test_the_dataclass_field_is_named_state
    test_job_state_field.py::TestTheFieldIsState::test_the_old_name_is_gone_rather_than_kept_beside_the_new_one
    test_job_state_field.py::TestTheFieldIsState::test_the_default_is_the_unchanged_planned_constant
    test_job_state_field.py::TestTheFieldIsState::test_nothing_was_retyped
    test_job_state_field.py::TestTheStoredKeyDidNotMove::test_the_exporter_still_writes_status_and_never_state
    test_job_state_field.py::TestTheStoredKeyDidNotMove::test_the_importer_reads_the_old_key_into_the_new_field
    test_job_state_field.py::TestTheStoredKeyDidNotMove::test_a_record_without_any_lifecycle_key_still_defaults
    test_job_state_field.py::TestTheStoredKeyDidNotMove::test_the_round_trip_through_json_preserves_a_non_default_state
    test_job_state_field.py::TestTheRenderingIsUnchanged::test_a_blocked_job_renders_and_exports_as_the_plain_word_blocked
    test_job_state_field.py::TestTheRetypeIsComplete::test_the_exported_status_is_a_plain_str_and_not_a_run_state
    test_job_state_field.py::TestTheRetypeIsComplete::test_every_construction_path_settles_as_a_run_state
    test_job_state_field.py::TestTheRetypeIsComplete::test_a_record_whose_status_is_not_a_run_state_value_still_loads
    test_job_state_field.py::TestTheRenameLeftNoSilentReaderBehind::test_budget_flags_are_refused_on_a_stopped_job
    test_job_state_field.py::TestTheRenameLeftNoSilentReaderBehind::test_a_linked_job_that_loads_reports_its_real_state
    test_job_plan_state_reads.py::TestNoRetiredJobPlanStateReads::test_the_scan_reaches_a_real_corpus
    test_job_plan_state_reads.py::TestNoRetiredJobPlanStateReads::test_the_scan_sees_a_retired_read_when_one_is_there
    test_job_plan_state_reads.py::TestNoRetiredJobPlanStateReads::test_no_production_site_reads_the_retired_status_off_a_job_plan

Worktree removed BY EXACT PATH; see External actions for the command and the
`git worktree list` reading.

### G5 NOTHING ELSE MOVED — PASS, five serial runs, every REAL_EXIT=0

    python3 -B -m pytest tests/orchestration/ -q -p no:randomly
        12861 passed, 10 skipped, 1 warning in 739.26s   REAL_EXIT=0
    python3 -B -m pytest tests/cli/test_do_cmd_cli_path.py -q -p no:randomly
        9 passed in 0.71s                                 REAL_EXIT=0
    python3 -B -m pytest tests/cli/test_do_cmd_pingpong_budget.py -q -p no:randomly
        6 passed in 0.35s                                 REAL_EXIT=0
    python3 -B -m pytest tests/docs/ -q -p no:randomly
        303 passed in 0.59s                               REAL_EXIT=0
    python3 -B -m pytest tests/cli/test_golden_path.py -q -p no:randomly
        42 passed in 22.97s                               REAL_EXIT=0

`tests/orchestration/` measures 12861 passed and 10 skipped, which is EXACTLY the
block's expected reading: the base 12856 plus the five tests this round adds,
three in the new guard file and two in the replaced one. The single warning is
`model_routing`'s pre-existing undeclared-role `UserWarning` and is unrelated to
this round. Note that the block's own measurement note describes the base
worktree reading of `tests/orchestration/` as "EXIT 0 at 12855 passed ... the
single failure being `test_vitest_passes`" — a run with a failure is EXIT 1, not
EXIT 0; see Deviations, item 2. That sentence bears on no gate here, because G5
runs in the PRIMARY checkout, where `apps/ui/node_modules` is present and the
vitest test passes.

### G6 RUFF — PASS, REAL_EXIT=0

    python3 -m ruff check apps/cli/commands/do_cmd.py \
        packages/orchestration/job_evidence.py \
        tests/orchestration/test_job_state_field.py \
        tests/orchestration/test_job_plan_state_reads.py
    All checks passed!
    REAL_EXIT=0

One invocation, the repository's own configuration, no `--isolated`.

### G7 THE TREE — PASS, REAL_EXIT=0

`git status --porcelain` was read after EVERY commit and was EMPTY every time —
after C0a, C0b, C1, C2, C3, C4 and C5. At the C5 boundary:

    git status --porcelain OUTPUT=''
    git ls-files .remedy-wt OUTPUT=''

Per-commit insertions from `git diff --numstat <parent> <commit>`, C6 excluded
because a commit cannot count its own insertions while it is being written:

    C0a 79f6dd8f  367 insertions  UNDER_CAP_500=True
    C0b 9edd01d2  265 insertions  UNDER_CAP_500=True
    C1  b021f398   29 insertions  UNDER_CAP_500=True
    C2  5249cd6e    4 insertions  UNDER_CAP_500=True
    C3  5de6f81a    4 insertions  UNDER_CAP_500=True
    C4  b63a88b6  209 insertions  UNDER_CAP_500=True
    C5  222c211e    2 insertions  UNDER_CAP_500=True

Maximum 367, against the DECISION F104 D1 cap of 500 counting INSERTIONS only.
No commit is oversize and no overage is declared.

The three `.agent/STOP` readings by `os.path.exists`, as constraint 8 orders:

    before C0a  False
    before C4   False
    before C6   False

## Authored-text proofs

Every slice was extracted PROGRAMMATICALLY from the COMMITTED
`.agent/authored/f272-r23.md` by `.remedy-wt/r23_slices.py`, which locates the
unique `<<<BEGIN NAME …>>>` and `<<<END NAME>>>` lines, asserts there is exactly
one of each, and joins the lines strictly between them — inclusive of the newline
ending the last content line, exclusive of the markers. Nothing was retyped.

    P1 FROM       196 bytes,  3 lines  f861d07a24fc49cbcf1bc39d4aa93620f057efe9cfe3e0973098e0201d3b7db1
    P1 TO         194 bytes,  3 lines  66d1b088b404fc54ebd8b33eaa22ebe183bb01fb33ceafa7e35cbec81672acca
    P2 FROM        62 bytes,  1 line   5e4c7a91ef3571b332b55fa498781724bfe191db76ad4e72b06ef2b2ed149778
    P2 TO         107 bytes,  2 lines  fce5aca6a73bf09684e0ba692e31aabfc96e22b3e37d216893277140b0d68a31
    PLANF272R23  2592 bytes, 49 lines  478442d29f3151bf3f45372e679d2def46a9f8985daa0b9818f32fbc8a1aa71a
    RECORDR23    6681 bytes,  3 lines  ca92ddd65fa22fdc56198a7c26fed4a7f24939cf99f3b511eb9ed202e343e2b9
    SLIPSR23     1000 bytes,  3 lines  cd10ed33b29de1c0072995f5a0ad0f5ac26d5d45dff615a1fad12769c0b22de6
    DONER23      2737 bytes,  1 line   bc38a879826f8b8dc2cabe6ed644545366bb741eaffa7b01236fe2f83dba0240

Disk-to-disk comparison results:

- `.agent/plan.md` is byte-equal to PLANF272R23 — G3, `BYTE_EQUAL_TO_PLANF272R23 True`.
- `.agent/live_review.md` after C2 is byte-equal to its pre-image plus a newline
  plus RECORDR23 — G2(a), `POST_EQUALS_PRE_NL_SLICE True`.
- `.agent/prose_slips.md` after C3 is byte-equal to its pre-image plus a newline
  plus SLIPSR23 — G3, `POST_EQUALS_PRE_NL_SLICE True`.
- `.agent/live_review.md` after C5 is byte-equal to its pre-image plus a newline
  plus DONER23 — G2(a), `POST_EQUALS_PRE_NL_SLICE True`.

Pairs P1 and P2 — the containment test was RUN in the primary checkout at C4's
pre-image, not rendered from the block:

    P1  TO_CONTAINS_FROM=False  FROM_CONTAINS_TO=False
        PRE  FROM_COUNT=1  TO_COUNT=0
        POST FROM_COUNT=0  TO_COUNT=1
        apps/cli/commands/do_cmd.py 126114 -> 126112 bytes
        ONLY_THE_PAIR_CHANGED=True
    P2  TO_CONTAINS_FROM=False  FROM_CONTAINS_TO=False
        PRE  FROM_COUNT=1  TO_COUNT=0
        POST FROM_COUNT=0  TO_COUNT=1
        packages/orchestration/job_evidence.py 141004 -> 141049 bytes
        ONLY_THE_PAIR_CHANGED=True

Both test artifacts were applied by `shutil.copyfile`, never by text extraction,
and each source was verified against the sha256, byte length AND line count
constraint 4 states BEFORE the copy — `MATCHES_CONSTRAINT4=True` for both. The
`test_job_state_field.py` replacement shows `50 insertions, 0 deletions`: the
`import pytest` line plus one test class of two tests, and NOTHING else changed,
exactly as constraint 4 requires. Had it shown any other deletion the round would
have stopped there.

## Deviations & assumptions

1. NO DEVIATION FROM THE BUNDLE. The block was applied verbatim. Every commit,
   every slice, every gate and every constraint landed as written. The change set
   was not left: `git diff --stat 67515ab7..HEAD` touches only paths on the
   block's list, and nothing under `docs/`, `scripts/` or `apps/ui/` moved.

2. DISAGREEMENT WITH THE BLOCK'S OWN PROSE, declared rather than silently
   corrected, and it binds no gate. The block's measurement note 3 reads
   "`tests/orchestration/` is EXIT 0 at 12855 passed and 10 skipped in a
   worktree, the single failure being `test_vitest_passes`". A run with one
   failure exits 1, so "EXIT 0" and "the single failure" cannot both be true of
   the same reading; the intended sentence is presumably EXIT 1 with 12855 passed
   and one failure. I applied nothing from that sentence — it is background, not
   an order — and the gate it feeds, G5, runs in the PRIMARY checkout, where the
   measured reading is EXIT 0 at 12861 passed and 10 skipped, exactly as G5
   predicts. Under amend0827 rule 2 this is reviewer prose that damaged nothing
   on disk, so it belongs in `.agent/prose_slips.md`, not in an R-id; I have NOT
   appended it myself, because the SLIPSR23 slice is what this round was ordered
   to append and inventing a third line would be silently correcting the block.
   Round 24's slips append is where it belongs.

3. ASSUMPTION on the push, stated because the block orders a push but a handback
   cannot transcribe a push of itself. I pushed once after C5, whose real
   transcript is in External actions above, and push C6 immediately after this
   commit; that second transcript is in the round report. This is the shape round
   22's handback got wrong by promising a transcript "below" that did not exist,
   and the correction is to record the push that HAS happened and to name where
   the one that has not yet happened will be recorded.

4. ASSUMPTION on the G4(i) collect-only reading. The block asks for the node ids
   from `--collect-only` "so the two runs are demonstrably over the same tests".
   I ran `--collect-only` in the PRIMARY checkout, where it collects 17; the
   worktree run at base reports 3 failed + 14 passed = 17 over the same two file
   paths, with the two files byte-identical in both trees by sha256 (G1 and
   G4(i)), so the two runs are over the same 17 tests. I did not re-add the
   worktree solely to collect there.

5. NO SCRATCH LEAKED. Every helper this round wrote lives under the gitignored
   `.remedy-wt/`; `git ls-files .remedy-wt` is empty at HEAD. The one worktree
   created was removed by exact path, never by a glob, and the twelve
   `remedy/job-*` worktrees that `git worktree list` shows are pre-existing
   product artifacts that this round neither created nor touched.

## Next

Round 24: the block's Next Step 1 — a DECISION naming F114's cost-preview carrier
before `job.run` is deleted, since `apps/cli/commands/job.py:726` is the product's
only call site of `confirm_cost_preview` and it sits inside the handler being
removed, while `do.job-run` carries neither `is_expensive` nor `--yes`.
