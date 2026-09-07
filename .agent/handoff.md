# Handback — F272 round 29

## Session

SESSION 12 of feature F272 · round 29 · rounds so far 29

SOFT LIMIT, under operator amendment amend0906-triage-throughput rule 2, which sets F272's
limit at 12 SESSIONS and 40 ROUNDS by name: the SESSION half REMAINS REACHED — this is still
session 12 of 12. The round half is not: this is round 29 of 40. The SPLIT half of the
amend0905-throughput split-and-close default was executed in round 26 (F274 registered,
DECISION F272 D16); this round is the fourth step of the CLOSE half — it registers what
round 28's self-use run surfaced and rules closure precondition 1.

CONTEXT SELF-ASSESSMENT (amend0905-throughput, one sentence): context is comfortable — this
round wrote no production code and read none, handled all four large state files
(`live_review.md` 1.24 MB, `decisions.md` 869 KB, `prose_slips.md` 153 KB) by measurement
rather than by reading them, and spent its budget on the block, AGENTS.md and the protocol.

SITZUNGS-LIMIT ERREICHT — OPERATOR-BERICHT IN DER ÜBERGABE

The scope report the limit obliges was written in full in round 26's handback and is on disk
and durable as the `## Built State` section of `docs/roadmap/features/T2_F272.md`, which
states what F272 built, which slices moved to F274, and what remains open. It is not
re-derived here. What is finished as of this round: T001, T002 and T003 complete; closure
preconditions 1 (this round, by DECISION F272 D17), 2 (round 27's integration gate), 4
(Built State) and 6 (round 28, booked into the record by this round's C3) all discharged.
What is missing: preconditions 3 and 5 — `remedy integrity check --json`, and the evidence
job, review zip, ledger rotation and closure commit. The proposal is unchanged from round 26
and already executed: close F272 at DECISION F272 D16's scope, PASS_WITH_RISKS, with F274
carrying T004's remainder and T005.

## Range

Review of `f321fefc`..`afa5ab60`.

The range ends at C5, the last commit that EXISTS while this file is being written. C6 is the
commit that writes this file and cannot state its own SHA; the reviewer's range is
`f321fefc`..HEAD once C6 lands.

## Commits

### e5ec4f33 f272: save the round 29 step block as authored text  (C0a)
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f272-r29.md | +259 / -0 | `shutil.copyfile` of `.remedy-wt/f272-r29-block.md` per constraint 3 |

### 5c2ab8f7 f272: mirror the round 29 step block into last_block  (C0b)
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +172 / -194 | the same `shutil.copyfile`, the mirror |

### 839ce00c f272: point the plan at round 29, the defect registration round  (C1)
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +15 / -17 | replaced byte for byte with the PLANF272R29 slice |

### e4198f43 f272: register R-0826, R-0827 and R-0828 from the round 28 self-use run  (C2)
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +6 / -0 | append of FINDINGSR29 — three registration paragraphs and their two blank separators; FINDINGS PERSIST FIRST, IN THEIR OWN COMMIT, per §4 item 4 and constraint 5 |

### e7f626bc f272: book the round 28 PASS verdict into the record  (C3)
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2 / -0 | append of RECORDR29, the `Gate: F272 R28` PASS entry, which also carries the R-0807 / R-0753 corroboration that mints no id; a SECOND append to the SAME file in a SECOND commit, never folded into C2 |

### 954e364b f272: rule closure precondition 1 as DECISION F272 D17  (C4)
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | +14 / -0 | append of D17SLICE, the closure-precondition-1 ruling |

### afa5ab60 f272: record the round 28 block prose slip on the run outcome enumeration  (C5)
| Path | +/- | Reason |
|---|---|---|
| .agent/prose_slips.md | +2 / -0 | append of SLIPSR29, one dated line, no id spent |

### C6 f272: hand back round 29
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | (self-referential) | this file; a handoff cannot table the commit that writes it (R-0149 pattern) |

Every `+/-` cell above is the real `git diff --numstat <parent> <commit>` figure and was
compared cell for cell against G7's per-commit table below. They agree.

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a | done | `.agent/authored/f272-r29.md`, copyfile, digest-identical to the delivered block |
| C0b | done | `.agent/last_block.md`, same copyfile, digest-identical |
| C1  | done | `.agent/plan.md` byte-equal to PLANF272R29, 1934 bytes, 38 lines |
| C2  | done | FINDINGSR29 appended; R-0826, R-0827, R-0828 each exactly one `^- R-XXXX ` registration |
| C3  | done | RECORDR29 appended in its OWN commit against the post-C2 image; `^Gate:` 51 -> 52 |
| C4  | done | D17SLICE appended; `^## DECISION F272 D17 ` heads exactly one section |
| C5  | done | SLIPSR29 appended, `POST_EQUALS_PRE_NL_SLICE` true |
| C6  | done | this handback |

No item was skipped and none deviated.

## External actions

| Action | Command | Outcome |
|---|---|---|
| push (after C5) | `git push -u origin feature/f272-one-world-completion` | `f321fefc..afa5ab60`, exit 0, upstream set |
| push (after C6) | `git push` | a second push after the final commit, expected and accepted; see the reviewer's own `git log origin/...` |
| worktree add | none | constraint 9 forbids creating one, and no round work needed one |
| worktree remove | none | constraint 9 forbids removing any; `git worktree list` is 14 before and 14 after |
| PR create / edit / merge | none | the block orders none; the closure PR is a later round |
| `gh` commands | none | none was ordered and none was run |

## Verification

Every gate was run as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`, with no pipe between the
command and the echo. No gate went red. `git status --porcelain` was read at every commit
boundary and was EMPTY every time.

**RECEIPT CHECK, before the block was opened.** The three stated measurements were verified
against the file on disk and all three agreed:

    wc -c -l .remedy-wt/f272-r29-block.md -> 259 lines, 31158 bytes
    sha256sum                             -> 96cac5e8428eda1c76f4230aa1171ab1f997c7ed5c5786febc69114524642a89
    stated: 31158 bytes / 259 lines / 96cac5e8...  ALL THREE AGREE

**G1 TRANSPORT — exit 0, PASS.** One digest comparison over three artefacts; all three
identical and all three equal to the reviewer's stamp.

    .remedy-wt/f272-r29-block.md (as delivered, on disk) len=31158 lines=259 sha=96cac5e8428eda1c76f4230aa1171ab1f997c7ed5c5786febc69114524642a89
    .agent/authored/f272-r29.md  (committed at C0a)      len=31158 lines=259 sha=96cac5e8428eda1c76f4230aa1171ab1f997c7ed5c5786febc69114524642a89
    .agent/last_block.md         (committed at C0b)      len=31158 lines=259 sha=96cac5e8428eda1c76f4230aa1171ab1f997c7ed5c5786febc69114524642a89
    REAL_EXIT=0

All three are byte-identical. Per §3 item 37 this chain covers those three artefacts and is
not a claim about the bytes emitted into a prompt.

**G2 THE FINDINGS APPEND at C2, against the file as it stands at C1 — exit 0, PASS.** Every
count landed on the block's stated figure; none was adjusted to agree.

    === G2(a) BYTE ===
    pre_len = 1225920  pre_lines = 2137
    pre_sha256 = 495c5cea046dfe0a7211dc89d18123b4ac64e903b6f152b19bb8790b3f0dfde0
    pre_tail12 = b'tion round.\n'  pre_trailing_nl_run = 1
    post_len = 1233736  post_lines = 2143
    post_sha256 = ae2804d2eb88ba957e631fb895a2949cdda0a5c46639f09bc1c141e648923db9
    post_tail12 = b'ed nothing.\n'  post_trailing_nl_run = 1
    slice_len = 7815  slice_sha256 = 04d733985aefa9a2214d36875fe8b2227962e1fe50b1ccbb6041af6dd83f8933
    PRE_IS_BYTE_EXACT_PREFIX_OF_POST = True
    POST_EQUALS_PRE_NL_SLICE = True
    === G2(b) STRUCTURAL ===
    N_COUNTED_FROM_SLICE = 3
    units_before = 734  units_after = 737
    EVERYTHING_BEFORE_UNCHANGED = True
    LAST_N_UNITS_EQUAL_SLICE_PARAGRAPHS_IN_ORDER = True
      appended unit 0 first 44 bytes: b"- R-0826 \xe2\x80\x94 Medium, THE SELF-USE TRACK'S OW"
      appended unit 1 first 44 bytes: b'- R-0827 \xe2\x80\x94 High, NO RUN MANIFEST CAN EVER '
      appended unit 2 first 44 bytes: b'- R-0828 \xe2\x80\x94 Medium, A JOB STOPPED BY ITS OW'
    === G2(c) NEGATIVE CONTROL (memory only) ===
    flip_offset = 1225951  inside_first_appended_paragraph = True
    byte_before = b'U'  context = b" THE SELF-USE TRACK'"
    byte_after  = b'u'
    FIRST_APPENDED_PARAGRAPH_IS_R0826 = True
    FIRST_APPENDED_PARAGRAPH_IS_NOT_R0828 = True
    BYTE_READER_REJECTS_MUTANT = True
    STRUCT_READER_REJECTS_MUTANT = True
    BOTH_READERS_ACCEPT_REAL_POST = True
    === G2(d) COUNTS (pre -> post) ===
      reg_distinct        309 ->    312
      done_distinct       252 ->    252
      reg_lines           309 ->    312
      done_lines          254 ->    254
      r0826                 0 ->      1
      r0827                 0 ->      1
      r0828                 0 ->      1
      r0829                 0 ->      0
      r0826_anywhere        7 ->      8
      done_any            254 ->    254
    OPEN_SET_BY_DISTINCT_ID pre  = 309 - 252 = 57
    OPEN_SET_BY_DISTINCT_ID post = 312 - 252 = 60
    NO_DONE_LINE_ADDED = True (^Done: lines 254 -> 254 )
    NEW_DISTINCT_IDS = [b'0826', b'0827', b'0828']
    === WRITTEN ===
    DISK_EQUALS_REAL_POST = True
    DISK_UNCHANGED_BY_NEGATIVE_CONTROL = True
    disk_len = 1233736  disk_sha256 = ae2804d2eb88ba957e631fb895a2949cdda0a5c46639f09bc1c141e648923db9
    REAL_EXIT=0

N was COUNTED BY THE SCRIPT from the slice (`len(units(SLICE))` = 3) and was never taken from
the block. The negative control flipped byte 1225951, which sits 31 bytes into the FIRST
appended paragraph — R-0826's, not R-0828's, as G2(c) requires and as
`FIRST_APPENDED_PARAGRAPH_IS_R0826 = True` confirms — in memory only; the file on disk was
re-read afterwards and is byte-identical to the real post-image. `r0826_anywhere 7 -> 8`
confirms constraint 7's statement that R-0826 occurs 7 times as PROSE at `f321fefc`: the
eighth occurrence is the registration this round adds, and the seven older ones are untouched.
No `^Done: ` line was added: 254 before, 254 after.

**G3 THE GATE-ENTRY APPEND at C3, against the file as it stands at C2 — exit 0, PASS.** The
pre-image is C2's post-image and is demonstrably NOT the base image.

    pre_len = 1233736  pre_lines = 2143
    pre_sha256 = ae2804d2eb88ba957e631fb895a2949cdda0a5c46639f09bc1c141e648923db9
    pre_tail12 = b'ed nothing.\n'  pre_trailing_nl_run = 1
    PRE_EQUALS_C2_POST_IMAGE = True
    PRE_IS_NOT_THE_BASE_IMAGE = True
    slice_len = 4542  slice_sha256 = 2af5da66b2fbb79c9afafd78606b4e85788296b52db23591232f7db006025fe0
    post_len = 1238279  post_lines = 2145
    post_sha256 = 3b6622ba52c6b814af4d7932a845c080a8136a54708e3d846bbadc9cc9ef7761
    post_tail12 = b'ted for it.\n'  post_trailing_nl_run = 1
    PRE_IS_BYTE_EXACT_PREFIX_OF_POST = True
    POST_EQUALS_PRE_NL_SLICE = True
      ^Gate:               51 ->   52
      ^Gate: F272 R28       0 ->    1
      ^- R-0826             1 ->    1
      ^- R-0827             1 ->    1
      ^- R-0828             1 ->    1
      ^- R-0829             0 ->    0
    OPEN_SET_BY_DISTINCT_ID pre  = 312 - 252 = 60
    OPEN_SET_BY_DISTINCT_ID post = 312 - 252 = 60
    DISK_EQUALS_POST = True
    disk_len = 1238279  disk_sha256 = 3b6622ba52c6b814af4d7932a845c080a8136a54708e3d846bbadc9cc9ef7761
    REAL_EXIT=0

The three registration counts are UNCHANGED by C3 at 1, 1 and 1, and the open set is 60 both
before and after it, as the gate requires. `PRE_EQUALS_C2_POST_IMAGE` and
`PRE_IS_NOT_THE_BASE_IMAGE` are stated explicitly because this is the one arithmetic the
round could most easily have got wrong: C3's pre-image is 1233736 bytes, not the base's
1225920.

**G4 THE DECISION RECORD at C4 — exit 0, PASS.**

    pre_len = 865296  pre_lines = 10873
    pre_sha256 = 3d2ca7f6b95c1f488062ead175c070abce1acc29e3c3c30ae5c88d75333ee331
    pre_tail12 = b'er unowned.\n'  pre_trailing_nl_run = 1
    slice_len = 4145  slice_sha256 = 939b9297469b88ceb1debd5fddbb4f4586698d120ab7ef53077d1326ec51cf9b
    post_len = 869442  post_lines = 10887
    post_sha256 = f369060b43a9dce22bc7b37862b3f569c72197256c92f6a122ae1aa65f56084d
    post_tail12 = b'teral text.\n'  post_trailing_nl_run = 1
    PRE_IS_BYTE_EXACT_PREFIX_OF_POST = True
    POST_EQUALS_PRE_NL_SLICE = True
      ^## DECISION F272 D        1 ->   2
      ^## DECISION F272 D17      0 ->   1
      ^## DECISION F272 D16      1 ->   1
      ^## DECISION F272 D18      0 ->   0
    D17_HEADS_EXACTLY_ONE_SECTION = True (count = 1 )
    D17_DUPLICATE_IS_A_STOP -> triggered = False
    pre_headings_F272 = [b'## DECISION F272 D16']
    post_headings_F272 = [b'## DECISION F272 D16', b'## DECISION F272 D17']
    REAL_EXIT=0

The pre-image is 865296 bytes at 10873 lines, exactly as the block stated.
`^## DECISION F272 D` went 1 -> 2 and `^## DECISION F272 D17 ` heads exactly one section, so
the duplicate-D17 STOP did not fire.

**G5 THE TWO PROSE FILES — exit 0, PASS.**

`.agent/plan.md`, re-read from disk at C5:

    PLAN_BYTE_EQUAL_TO_PLANF272R29 = True
    plan_len = 1934  plan_lines = 38  sha = 8f95b065ec45891c6573a22e2375cb38600e5cf01dd750c395482317fb018eae
    plan_lines_vs_AGENTS_cap_50 = 38 <= 50 -> True
    HAS_GOAL_HEADING = True
    HAS_NEXT_STEPS_HEADING = True
    REAL_EXIT=0

1934 bytes, 38 newline-terminated lines against the AGENTS.md cap of 50; `## Goal` and
`## Next Steps` both present, both confirmed by re-reading the file after the write.

`.agent/prose_slips.md`, the byte append check only:

    pre_len = 152214  pre_lines = 567
    pre_sha256 = e52d1332646895a89914fc9077aedfe710555332dee718f040f653904376b690
    pre_tail12 = b' exist yet.\n'  pre_trailing_nl_run = 1
    PRE_MATCHES_BLOCK_STATED_152214_567 = True
    slice_len = 903  slice_sha256 = 363008e6b7a345fc832d0b3e64df22dba6e55fc252670f0c9a68a69c231b9db2
    post_len = 153118  post_lines = 569
    post_sha256 = 1f3951808f796f135bb1730b29efaceb439375fc0bb47eb9456aaf6a0faee7a0
    post_tail12 = b'acceptable.\n'  post_trailing_nl_run = 1
    PRE_IS_BYTE_EXACT_PREFIX_OF_POST = True
    POST_EQUALS_PRE_NL_SLICE = True
    REAL_EXIT=0

pre_len 152214 and pre_lines 567 are the block's own figures, met exactly.

**G6 THE CANARY — exit 0, PASS.** Run in the PRIMARY checkout at C5, not in a worktree.

    $ python3 -B -m pytest tests/cli/test_golden_path.py -q -p no:randomly
    ..........................................                               [100%]
    42 passed in 20.85s
    REAL_EXIT=0

42 passed at exit 0 reproduces the reviewer's `b865f001` figure exactly. No `.py` file changed
this round, so no ruff reading is owed and none was taken; no production line moved, so no
red-proof was ordered or possible.

**G7 THE TREE — exit 0, PASS.**

    git status --porcelain exit 0 -> output = ''
    PORCELAIN_EMPTY_NOW = True
    git ls-files .remedy-wt exit 0 -> output = ''
    LS_FILES_REMEDY_WT_EMPTY = True
    git worktree list exit 0  entries = 14
        /home/decodeux/Repos/remedy                                  afa5ab60 [feature/f272-one-world-completion]
        /home/decodeux/Repos/remedy/.remedy-wt/job-020c1ef366af4f07  4d5edd71 [remedy/job-020c1ef366af4f07]
        /home/decodeux/Repos/remedy/.remedy-wt/job-101fad068c0741f4  3c10561b [remedy/job-101fad068c0741f4]
        /home/decodeux/Repos/remedy/.remedy-wt/job-1cbb6972bf7c4ffc  db21957a [remedy/job-1cbb6972bf7c4ffc]
        /home/decodeux/Repos/remedy/.remedy-wt/job-21c19578b8754287  79a73b5a [remedy/job-21c19578b8754287]
        /home/decodeux/Repos/remedy/.remedy-wt/job-2ac1522a7034440b  3afc78c5 [remedy/job-2ac1522a7034440b]
        /home/decodeux/Repos/remedy/.remedy-wt/job-48a379ab5ca44ec5  f0e6b9a3 [remedy/job-48a379ab5ca44ec5]
        /home/decodeux/Repos/remedy/.remedy-wt/job-5e91e080219342d9  9fdb3b4b [remedy/job-5e91e080219342d9]
        /home/decodeux/Repos/remedy/.remedy-wt/job-6f74dd7367704fd5  cf0e00e9 [remedy/job-6f74dd7367704fd5]
        /home/decodeux/Repos/remedy/.remedy-wt/job-7d1c93e2dc98415a  f0e6b9a3 [remedy/job-7d1c93e2dc98415a]
        /home/decodeux/Repos/remedy/.remedy-wt/job-848fc4c67d7b405b  7bea3efc [remedy/job-848fc4c67d7b405b]
        /home/decodeux/Repos/remedy/.remedy-wt/job-962cb3c9b96244ed  05852956 [remedy/job-962cb3c9b96244ed]
        /home/decodeux/Repos/remedy/.remedy-wt/job-98e9364a83a34872  21a45836 [remedy/job-98e9364a83a34872]
        /home/decodeux/Repos/remedy/.remedy-wt/job-f76686b8435640e9  4b49af98 [remedy/job-f76686b8435640e9]
    WORKTREE_COUNT_IS_14 = True
    JOB_020c1ef366af4f07_PRESENT = True
    REAL_EXIT=0

14 entries at the base and 14 at the end, unchanged per constraint 9 — the primary plus
thirteen `remedy/job-*`, including round 28's retained `remedy/job-020c1ef366af4f07`. I
created no worktree and removed none.

`git status --porcelain` at every commit boundary, real output each time:

    after C0a: ''    after C0b: ''    after C1: ''    after C2: ''
    after C3:  ''    after C4:  ''    after C5: ''

(The only non-empty reading in the whole round was BEFORE C0a, ` M .agent/last_block.md` and
`?? .agent/authored/f272-r29.md` — the C0a/C0b change-set entries sitting unstaged before
their own commits. That is not a commit boundary.)

Per-commit insertions, `git diff --numstat <parent> <commit>`, C0a through C5 (C6 excluded,
because a commit cannot count its own insertions while it is being written):

    C0a  e5ec4f33  ins=259  del=0    under_500=True   +259 -0  .agent/authored/f272-r29.md
    C0b  5c2ab8f7  ins=172  del=194  under_500=True   +172 -194  .agent/last_block.md
    C1   839ce00c  ins=15   del=17   under_500=True   +15 -17  .agent/plan.md
    C2   e4198f43  ins=6    del=0    under_500=True   +6 -0  .agent/live_review.md
    C3   e7f626bc  ins=2    del=0    under_500=True   +2 -0  .agent/live_review.md
    C4   954e364b  ins=14   del=0    under_500=True   +14 -0  .agent/decisions.md
    C5   afa5ab60  ins=2    del=0    under_500=True   +2 -0  .agent/prose_slips.md
    REAL_EXIT=0

Every one is under the DECISION F104 D1 cap of 500 INSERTIONS. These are the figures in the
per-commit tables above, compared cell for cell; they agree. No commit is oversize, so no
inseparability declaration is owed.

The three `.agent/STOP` readings, all by `os.path.exists`, per constraint 8:

    STOP_BEFORE_C0A_EXISTS = False
    STOP_BEFORE_C2_EXISTS  = False
    STOP_BEFORE_C6_EXISTS  = False

**OPEN FINDINGS COUNT — 60 BY DISTINCT ID, measured at HEAD after C3.**

    .agent/live_review.md at HEAD: 1238279 bytes, 2145 lines, sha256 3b6622ba52c6b814af4d7932a845c080a8136a54708e3d846bbadc9cc9ef7761
    distinct ^- R-dddd registrations   = 312
    distinct ^Done: R-dddd resolutions = 252
    OPEN SET BY DISTINCT ID = 312 - 252 = 60
    registration LINES = 312 ; resolution LINES = 254
    resolution ids appearing on more than one Done line = [R-0721, R-0725]
    resolutions naming an id never registered = []
      R-0826  registered=True   ^- lines=1  occurrences anywhere=10
      R-0827  registered=True   ^- lines=1  occurrences anywhere=2
      R-0828  registered=True   ^- lines=1  occurrences anywhere=2
      R-0829  registered=False  ^- lines=0  occurrences anywhere=0
    ^Gate: lines = 52 ; ^Gate: F272 R28  lines = 1
    triple_newline occurrences in live_review.md = 0
    REAL_EXIT=0

THE ARITHMETIC. 57 open at `f321fefc` (309 distinct registrations minus 252 distinct
resolutions) plus the THREE ids this round minted — **R-0826** (Medium, the self-use defect
reporter is blind to a budget stop and a failed run-manifest write), **R-0827** (High, no run
manifest can be published on the `ollama` provider because `ollama-legacy` is not in
`VALID_CALL_MODES`) and **R-0828** (Medium, a budget-stopped job is left recorded as
`RUNNING` with a blank `finished_at`) — minus ZERO resolved, since this round wrote no
`Done:` line, gives 60. Counted by DISTINCT ID and not by line, per §3 item 10: there are 254
`^Done: ` lines against 252 distinct ids, because R-0721 and R-0725 each carry a two-paragraph
resolution. That is pre-existing, is unchanged by this round, and is exactly why the formula
subtracts distinct ids rather than lines. `R-0829` is still free, as constraint 7 requires.

## Authored-text proofs

All five slices were extracted PROGRAMMATICALLY from the COMMITTED
`.agent/authored/f272-r29.md`, between the `<<<BEGIN NAME ...>>>` and `<<<END NAME>>>` lines,
exclusive of both marker lines and INCLUSIVE of the newline ending the last content line.
Nothing was retyped and nothing was taken from the delegating message. The extractor asserts
exactly one BEGIN and exactly one END marker per name and fails loudly otherwise.

| Slice | Bytes | Lines | sha256 | Proof |
|---|---|---|---|---|
| PLANF272R29 | 1934 | 38 | `8f95b065ec45891c6573a22e2375cb38600e5cf01dd750c395482317fb018eae` | `.agent/plan.md` byte-equal to the slice: `PLAN_BYTE_EQUAL_TO_PLANF272R29 = True` |
| FINDINGSR29 | 7815 | 5 | `04d733985aefa9a2214d36875fe8b2227962e1fe50b1ccbb6041af6dd83f8933` | `POST_EQUALS_PRE_NL_SLICE = True` on `.agent/live_review.md` at C2, plus the structural reader (N=3) and the negative control |
| RECORDR29 | 4542 | 1 | `2af5da66b2fbb79c9afafd78606b4e85788296b52db23591232f7db006025fe0` | `POST_EQUALS_PRE_NL_SLICE = True` at C3, against C2's post-image |
| D17SLICE | 4145 | 13 | `939b9297469b88ceb1debd5fddbb4f4586698d120ab7ef53077d1326ec51cf9b` | `POST_EQUALS_PRE_NL_SLICE = True` on `.agent/decisions.md` at C4 |
| SLIPSR29 | 903 | 1 | `363008e6b7a345fc832d0b3e64df22dba6e55fc252670f0c9a68a69c231b9db2` | `POST_EQUALS_PRE_NL_SLICE = True` on `.agent/prose_slips.md` at C5 |

Every slice ends in exactly one newline (`endswith_nl = True` for all five), and every append
target had a trailing-newline run of exactly 1 both before and after, so no append introduced
a blank-line drift. This round carried no FROM/TO pair, as constraint 2 states.

## Deviations & assumptions

The block's ordered commit sequence C0a, C0b, C1, C2, C3, C4, C5, C6 was followed EXACTLY: no
extra commit, no dropped commit, no reordering. C2 and C3 are two separate commits against the
same file, as constraint 5 requires, and C3 was proved against C2's post-image rather than the
base.

**1. DECLARED DISAGREEMENT WITH CONSTRAINT 2's MARKER WORDING, applied as written and not
silently corrected.** Constraint 2 says the slices lie "between its `<<<BEGIN NAME>>>` and
`<<<END NAME>>>` lines". The BEGIN lines in the block do not have that form: every one carries
an attribute before the closing `>>>`, e.g. `<<<BEGIN PLANF272R29 target=.agent/plan.md>>>`
and `<<<BEGIN FINDINGSR29 target=.agent/live_review.md mode=append>>>`. A literal reader
matching `<<<BEGIN NAME>>>` would find zero BEGIN markers and extract nothing. I applied the
constraint's INTENT by matching the prefix `<<<BEGIN <NAME> ` — including the trailing space,
which is what makes the match unambiguous — and the END lines exactly as `<<<END <NAME>>>`.
The END wording is literally correct as stated; only the BEGIN wording is not. Declaring it
rather than correcting the block.

**2. DECLARED, on a claim in the D17SLICE text I applied verbatim.** D17SLICE's CONTEXT
paragraph says four Highs are open before this round and that R-0827 makes five. I did not
independently verify the SEVERITY of R-0803, R-0804, R-0806 and R-0807 against the ledger —
no gate ordered that measurement and I did not invent one — so the count of five is applied on
the reviewer's authority, not on mine. What I did measure is that the ledger holds 60 open
findings by distinct id at HEAD, and that R-0827 is registered `High` in its own text. A
reviewer relying on "five" for the closure paragraph should re-derive it.

**3. OBSERVATION, not a deviation — the `^Done: ` line/id gap.** `.agent/live_review.md`
carries 254 `^Done: R-dddd` LINES against 252 distinct ids: R-0721 and R-0725 each have a
two-paragraph resolution. This is pre-existing at `f321fefc`, is untouched by this round, and
is not repaired here. It is recorded because a reader who counts LINES rather than distinct
ids would compute an open set of 58 instead of 60 and would then disagree with the block's
stated 57 -> 60 without either of them being wrong about the file.

**4. DECLARED — a probe of mine had a persistence side effect, and it changed nothing.** The
G1 gate reading was taken by re-running the same script that performed C0a and C0b
(`.remedy-wt/r29_c0.py`), which re-executes `shutil.copyfile` before printing the three
digests. The bytes written were byte-identical to the already-committed ones — the same run's
three digests are all `96cac5e8...`, and `git status --porcelain` was EMPTY immediately
afterwards, which is the proof nothing moved. It is still a probe that writes, which is a
shape to avoid, and I name it rather than let it pass as a read-only measurement.

**5. TOOLING — scratch scripts under `.remedy-wt/`, deleted by exact path.** This session's
bash guard rejects heredocs, brace quantifiers, loops, `$( )` and multi-operation compounds by
shape, so every multi-step measurement was written to a file under the gitignored
`.remedy-wt/` and run with `python3 -B`. The TEN files were `.remedy-wt/r29_probe0.py`,
`.remedy-wt/r29_c0.py`, `.remedy-wt/r29_extract.py`, `.remedy-wt/r29_c1.py`,
`.remedy-wt/r29_c2.py`, `.remedy-wt/r29_c3.py`, `.remedy-wt/r29_c4.py`,
`.remedy-wt/r29_c5.py`, `.remedy-wt/r29_g7.py` and `.remedy-wt/r29_final.py`, and each was
deleted BY ITS EXACT PATH after the gates were taken, never by a glob. `python3 -B` was used
throughout, so no `__pycache__` was written for the imported extractor.
`.remedy-wt/f272-r29-block.md` was NOT deleted: it is
G1's first link. `git ls-files .remedy-wt` is empty, so none of this ever touched the review
subject.

**6. NOT DONE, deliberately, per constraint 6.** No `Done:` paragraph and no `Landed:` line
was written for R-0826, R-0827 or R-0828, and no repair was attempted. Their fix clauses bind
the feature that takes them — F273, per D17SLICE — not this round. No production file moved:
nothing under `packages/`, `apps/`, `tests/`, `scripts/` or `docs/` changed, and no STATUS
line was touched, so the change set is exactly the seven declared paths and nothing else. No
measurement forced a path outside the list.

**7. NOT DONE — no PR, no merge, no force-push, no history rewrite, no branch switch.** None
was ordered. The branch was pushed twice: once after C5 and once after C6, which the round's
transport note declares as expected.

## Next

The reviewer reviews `f321fefc`..HEAD and rules on this round. The open set stands at 60 by
distinct id, and the closure round reads that number from here. The substantive question
handed over is whether DECISION F272 D17 is the right ruling on closure precondition 1 — it
rules that F272 closes PASS_WITH_RISKS naming all five open High findings with F273 as their
owner, rather than waiting for a feature Rule A5 cannot reach — and, if it is, the remaining
closure work is preconditions 3 and 5: `remedy integrity check --json`, the evidence job and a
FRESH review zip with `base_commit` at the FORK POINT `b18fad57`, ledger rotation by
`scripts/rotate_live_review.py` as its own commit, and then the closure commit carrying the
STATUS `[x]` line, the README capability sync and SU-012's `consumed_by` together, followed by
the PR. The PR is not merged this session.
