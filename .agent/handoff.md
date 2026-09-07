# Handback — F272 round 31 — THE CLOSURE ROUND

F272 is CLOSED. `docs/roadmap/STATUS.md` carries the `[x]` line, `README.md` carries the
matching capability sync in the SAME commit (R-0154), SU-012's `consumed_by` reads `F272`,
and this file is the final `.agent/` state the closure protocol's step 5 asks for. The pull
request is created after this commit and is NOT merged by this session.

## Session

SESSION 12 of feature F272 · round 31 · rounds so far 31

SITZUNGS-LIMIT ERREICHT — OPERATOR-BERICHT IN DER ÜBERGABE

The session half of F272's operator-set soft limit (amend0906-triage-throughput rule 2: 12
SESSIONS and 40 ROUNDS by name) REMAINS REACHED — this is still session 12 of 12. The round
half is not: this is round 31 of 40. The SPLIT half of the amend0905-throughput
split-and-close default was executed in round 26 (F274 registered, DECISION F272 D16); this
round is the LAST step of the CLOSE half — closure algorithm steps 4 and 5.

The scope report the limit obliges is durable on disk as the `## Built State` section of
`docs/roadmap/features/T2_F272.md` and is not re-derived here. WHAT IS FINISHED: T001, T002
and T003 complete, plus the `run-loop` half of T004; all six closure preconditions and all
five closure algorithm steps that belong to this branch. WHAT IS MISSING: nothing on this
branch — T004's remainder (the atomic classic-to-unified record flip) and T005 (the prototype
cluster deletion) are F274's by DECISION F272 D16, and F274 is registered directly after F272
in the ledger by amend0906-split-placement. The only act left anywhere is the MERGE of the
pull request, which happens at the NEXT feature's start through the Open PR Gate.

CONTEXT SELF-ASSESSMENT (amend0905-throughput, one sentence): context is comfortable — this
round read the block, AGENTS.md, the closure protocol, the self-drive protocol, the handback
template, `README.md` and the previous handoff in full, and handled every large state file
(`decisions.md` 872 KB, `prose_slips.md` 154 KB, `live_review.md` 493 KB) by measurement
rather than by reading it.

## Range

Review of `e388c603`..HEAD.

This file is written BEFORE the commit that carries it exists, so C5's own SHA, its own
numstat row and the PR number cannot appear here — the R-0149 self-reference exception. The
worker's round report to Window 1 carries all three as measured values.

## Commits

### 33c6acb8 f272: save the round 31 step block  (C0a)
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f272-r31.md | +347 / -0 | `shutil.copyfile` of `.remedy-wt/f272-r31-block.md` per constraint 3 |

### e347d91c f272: mirror the round 31 step block into the last block state  (C0b)
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +276 / -233 | the same `shutil.copyfile`, the mirror |

### bed400a7 f272: set the plan to round 31, the closure round  (C1)
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +20 / -21 | replaced byte for byte with the PLANF272R31 slice |

### 672db03e f272: book the round 30 PASS verdict into the record  (C2)
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2 / -0 | append of RECORDR31, the `Gate: F272 R30` PASS entry |

### 4304b56d f272: record the round 30 block prose slip on the manifest module path  (C3)
| Path | +/- | Reason |
|---|---|---|
| .agent/prose_slips.md | +2 / -0 | append of SLIPSR31, one dated line, no id spent |

### d2e9da48 f272: rule the ledger rotation oversize exception as decision D18  (C4)
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | +10 / -0 | append of D18SLICE, DECISION F272 D18 |

### (C5) f272: close F272 in the ledger and the README and consume the self-use item
| Path | +/- | Reason |
|---|---|---|
| docs/roadmap/STATUS.md | +1 / -1 | STATUSPAIR — the `[~]` F272 line becomes the `[x]` closure line |
| README.md | +14 / -3 | READMECOUNTPAIR 74→75, READMETIERPAIR Tier 2 Done 17→18, READMECAPPAIR the F272 capability paragraph |
| scripts/self_use_queue.json | +1 / -1 | QUEUEPAIR — SU-012's `consumed_by` set to `F272`, closure precondition 6 |
| .agent/handoff.md | full rewrite | this file; it cannot table its own line counts before it is written (R-0149) |

C5 is the LAST commit on this branch. No fix-up, no second handback, no trim follows it.

## External actions

Performed AFTER this file is written, in this order, and reported with their real outcomes in
the round report:

1. `git push -u origin feature/f272-one-world-completion` — the closure commit pushed.
2. `gh pr create --base main --head feature/f272-one-world-completion --title 'F272 — One
   world completion: the run re-key, the unified record and the migrated consumers'
   --body-file <scratch path>` — the PR number and URL are in the round report; this file
   predates them.
3. `gh pr list --state open --json number,headRefName,baseRefName,isDraft` — confirming the
   PR is open, targets `main`, comes from this branch and is not a draft.

`gh pr merge` IS NOT RUN. Guardrail G1 of `docs/agents/self_drive_protocol.md` forbids the
session that created a PR from merging it, and closure protocol step 6 defers the merge to
the next feature's start through the Open PR Gate — that gap is the operator's manual-review
window.

No worktree was added or removed: `git worktree list` reads 14 entries at every boundary of
this round, unchanged from `e388c603`.

## Verification

Every gate was RUN. Exit codes are real; no gate is reported as a word.

**G1 TRANSPORT — one digest comparison over three artefacts.** All three are identical,
and the digest equals the one the reviewer stated when it delivered the block. Every hex
string below is the untruncated 64-character value the script printed; none is abbreviated.

    .remedy-wt/f272-r31-block.md  bytes=28287 lines=347
        sha256=cd3ecd6d4c1499eead29cab5f571ec8c9d051038bf5a6939927254d62b368079
    .agent/authored/f272-r31.md   bytes=28287 lines=347
        sha256=cd3ecd6d4c1499eead29cab5f571ec8c9d051038bf5a6939927254d62b368079
    .agent/last_block.md          bytes=28287 lines=347
        sha256=cd3ecd6d4c1499eead29cab5f571ec8c9d051038bf5a6939927254d62b368079

    ALL_THREE_IDENTICAL          = True
    MATCHES_REVIEWER_STATED_SHA  = True

The three delivered measurements — 28287 bytes, 347 lines and that digest — were verified
against the file on disk BEFORE the block was opened, as the round order required.

**G2 THE FINDING RECORD (C2), against its own pre-image.**

(a) BYTE.

    pre_len    = 487792   pre_lines  = 535
    pre_sha256 = 90bb842f424f8dea43d8a3e2338b43da65f4277967f27926f85f4ca2d8d8a737
    pre terminal 12 bytes = b'ng to hold.\n'      pre trailing newline run = 1
    SLICE RECORDR31 bytes=5432 lines=1
    post_len   = 493225   post_lines = 537
    post_sha256 = 9b104c3cb3fbd36b9aaf4cb1d4340f9812b768bda128805cc5c08aaf71201438
    post terminal 12 bytes = b'd or an id.\n'     post trailing newline run = 1
    PRE_IS_BYTE_EXACT_PREFIX_OF_POST = True
    POST_EQUALS_PRE_NL_SLICE         = True

(b) STRUCTURAL. N counted by the script from the slice, not stated to it.

    N (counted from the slice) = 1
    units before = 205   units after = 206
    LAST_N_EQUAL_SLICE_PARAGRAPHS_IN_ORDER = True
    EVERYTHING_BEFORE_UNCHANGED            = True

(c) NEGATIVE CONTROL, in memory only, on the FIRST paragraph the append adds — byte 40 of the
slice, `r` flipped to `R`:

    BYTE_READER_REJECTS_FLIPPED       = True
    STRUCTURAL_READER_REJECTS_FLIPPED = True
    BYTE_READER_ACCEPTS_REAL          = True
    STRUCTURAL_READER_ACCEPTS_REAL    = True
    FILE_ON_DISK_UNCHANGED_BY_CONTROL = True (re-read sha256 equals the real post-image)

(d) COUNTS, with the open-set arithmetic:

    distinct ^- R-\d{4}      62 -> 62
    distinct ^Done: R-\d{4}   2 ->  2   (R-0721, R-0725)
    OPEN SET BY DISTINCT ID  pre  62 - 2 = 60
    OPEN SET BY DISTINCT ID  post 62 - 2 = 60
    ^Gate:                   30 -> 31
    ^Gate: F272 R30          0 -> 1
    ^- R-0829                0 -> 0     (the next free id is still free, constraint 6)

**G3 THE TWO PROSE FILES.**

`.agent/plan.md` — byte-equal to PLANF272R31:

    PLAN_BYTE_EQUAL_TO_SLICE = True
    bytes = 1838   lines = 37   AGENTS.md cap = 50   UNDER_CAP = True
    HAS_GOAL = True   HAS_NEXT_STEPS = True   (HAS_CURRENT_STEP = True as well)

`.agent/prose_slips.md` — byte append only:

    pre_len 153776 (block stated 153776)   pre_lines 571 (block stated 571)
    SLICE SLIPSR31 bytes=695 lines=1
    post_len 154472   post_lines 573
    PRE_IS_BYTE_EXACT_PREFIX_OF_POST = True
    POST_EQUALS_PRE_NL_SLICE         = True

**G4 THE DECISION RECORD (C4).**

    pre_len 869442 (block stated 869442)   pre_lines 10887 (block stated 10887)
    pre_sha256  = f369060b43a9dce22bc7b37862b3f569c72197256c92f6a122ae1aa65f56084d
    SLICE D18SLICE bytes=3042 lines=9
    post_len 872485   post_lines 10897
    post_sha256 = 6db4150fe9437cc702fcbd1199be58a5342e80678183f05944f14ba6a5e73993
    PRE_IS_BYTE_EXACT_PREFIX_OF_POST = True
    POST_EQUALS_PRE_NL_SLICE         = True
    ^## DECISION F272 D     2 -> 3   (D16, D17, D18)
    ^## DECISION F272 D18   heads exactly 1 section

**G5 THE CLOSURE COMMIT.**

(a) The staged path set of C5, read with `git diff --cached --name-only` immediately before
the commit, is EXACTLY: `README.md`, `docs/roadmap/STATUS.md`,
`scripts/self_use_queue.json`, `.agent/handoff.md` — four paths, nothing else, which is the
block's list. The equivalent post-commit reading, `git diff --name-only d2e9da48 <C5>`, is
taken after this file is committed and its real output is in the round report.

(b) Per pair, in the ordered form the block asked for — FROM before, FROM after, TO after,
and the boolean that the post-image is the pre-image with that ONE replacement and nothing
else:

    STATUSPAIR      docs/roadmap/STATUS.md       1 -> 0   TO=1   ONE_REPLACEMENT_ONLY=True
    READMECOUNTPAIR README.md                    1 -> 0   TO=1   ONE_REPLACEMENT_ONLY=True
    READMETIERPAIR  README.md                    1 -> 0   TO=1   ONE_REPLACEMENT_ONLY=True
    READMECAPPAIR   README.md                    1 -> 0   TO=1   ONE_REPLACEMENT_ONLY=True
    QUEUEPAIR       scripts/self_use_queue.json  1 -> 0   TO=1   ONE_REPLACEMENT_ONLY=True

    docs/roadmap/STATUS.md      39632 -> 40038 bytes
    README.md                   15225 -> 16057 bytes (three sequential replacements)
    scripts/self_use_queue.json 38741 -> 38745 bytes

Every pair was re-classified before use: `TO.find(FROM) >= 0` is FALSE for all five, so all
five are REWRITES and none carries an append obligation — the reviewer's table is confirmed
by measurement, not accepted on report.

(c) The F272 STATUS line in the post-image is BYTE-EQUAL to the STATUSPAIR_TO slice, at 520
bytes:

    - [x] F272 — One world completion — the run re-key, the consumers, the classic runner and the cluster deletion (T001–T003 complete and the `run-loop` half of T004; accepted 2026-09-07 · live review PASS_WITH_RISKS — ACCEPTED · Evidence job abf14422b1badab6 · package remedy-review-20260907-173909-READY_FOR_REVIEW.zip · SHA-256 8bbce2fa27ddd6c68398d381d1367e6e509b49cbacac0a29ff06329d9aebb706 · package path /home/decodeux/Repos/remedy-history/zips · accepted HEAD 7f71b30ac3b2f1fefb2da6063f0453d650d3835a)

(d) `^- \[~\] ` occurs ZERO times in `docs/roadmap/STATUS.md` after the edit — F272 was the
only `[~]` line in the ledger and it is now `[x]`. `^- \[x\] F272 ` occurs 1 time.

(e) README pins:

    contains "75 of 274 registered items accepted."          = True
    contains "| 2 | Minimal Self-Build Runtime | 18 | 27 |"   = True
    "F272" occurrences inside the "Accepted in Tier 2 so far:" block = 1

Every F-id inside EVERY `Accepted…:` block was resolved against STATUS and every one is `[x]`
there — Tier 0 block 16 ids, Tier 1 block 13, Tier 2 block 10 (now including F272), Tier 3
block 6, Tier 5 block 13. The list of ids in an Accepted block that are NOT `[x]` in STATUS
is EMPTY.

(f) SU-012's `consumed_by` reads `F272` and every other item's `consumed_by` is unchanged —
the full map read back from disk is SU-001 F257, SU-002 F258, SU-003 F106, SU-004 F108,
SU-005 F109, SU-006 F110, SU-007 F112, SU-008 F114, SU-009 F262, SU-010 F259, SU-011 F260,
SU-012 F272. Through the SHIPPED reader
`packages.orchestration.self_use_queue`:

    pending_self_use_items() = ()      -> EMPTY = True
    next_self_use_item()     = None
    item count = 12 (unchanged)   schema_version = 2 (unchanged)

The self-use track is EXHAUSTED again: the next feature's closure will need
`generate_and_append_if_empty` (F258 T001) before it can consume an item.

(g) `json.loads` succeeds on `scripts/self_use_queue.json`.

**G6 THE LEDGER GATES — run SERIALLY in the primary checkout with C5's content on disk.**
Every command was run as `bash -c '<cmd>; echo "REAL_EXIT=$?"'` with no pipe between the
command and the echo.

    python3 -B -m pytest tests/docs/ -q -p no:randomly
        303 passed in 0.59s          REAL_EXIT=0
    python3 -B -m pytest tests/orchestration/test_roadmap_index.py -q -p no:randomly
        30 passed in 0.43s           REAL_EXIT=0
    python3 -B -m pytest tests/orchestration/test_self_use_queue.py -q -p no:randomly
        23 passed in 0.30s           REAL_EXIT=0
    python3 -B -m pytest tests/cli/test_golden_path.py -q -p no:randomly
        42 passed in 20.99s          REAL_EXIT=0

The measured counts — 303, 30, 23 and the canary's 42 — equal the four the reviewer measured
in its own disposable worktree at `e388c603` with these same five edits applied. Neither
README pin is a gate that cannot fail: the reviewer showed
`test_the_readme_tier_table_done_column_matches_the_ledger` reddens when the Tier 2 Done cell
goes back to 17 with F272 `[x]`, and
`test_the_readme_accepted_count_equals_the_status_count` reddens when the accepted count goes
back to 74 — one failure each. That mutation proof was the reviewer's and is not re-derived
here; this round ran the four suites and reports what it measured.

**G7 THE TREE.**

    git status --porcelain    Run immediately BEFORE each of C0a, C0b, C1, C2, C3 and C4, it
                              listed EXACTLY the one path that commit was about and nothing
                              else — `A  .agent/authored/f272-r31.md`, then `M
                              .agent/last_block.md`, `M  .agent/plan.md`, `M
                              .agent/live_review.md`, `M  .agent/prose_slips.md`, `M
                              .agent/decisions.md` — so each commit consumed the whole working
                              set and the tree was EMPTY at every one of those boundaries. The
                              reading at C5's own boundary is in the round report, taken after
                              the commit this file rides in.
    git ls-files .remedy-wt   EMPTY — the scratch directory is gitignored and untracked.
    git worktree list         14 entries at the start and 14 at the end; none added, none
                              removed (constraint 7).

Per-commit insertions from `git diff --numstat <parent> <commit>`, C5 excluded because it
carries the handoff that would have to count itself, against the DECISION F104 D1 cap of 500:

    C0a 33c6acb8  1 parent  347 insertions  under_500 = True
    C0b e347d91c  1 parent  276 insertions  under_500 = True
    C1  bed400a7  1 parent   20 insertions  under_500 = True
    C2  672db03e  1 parent    2 insertions  under_500 = True
    C3  4304b56d  1 parent    2 insertions  under_500 = True
    C4  d2e9da48  1 parent   10 insertions  under_500 = True

Every commit in this round is SINGLE-PARENT. No oversize commit was created this round, so
F272's single declared-oversize allowance remains spent exactly once — on round 30's ledger
rotation, which DECISION F272 D18 (appended at C4 above) now rules on as a standing answer.

**THE THREE `.agent/STOP` READINGS**, taken with `os.path.exists` as constraint 8 requires:

    before C0a                 False
    before C5                  False
    before the PR is created   reported in the round report — this file predates that reading

## Authored-text proofs

Every applied text was extracted PROGRAMMATICALLY from the committed
`.agent/authored/f272-r31.md` by prefix-matching the BEGIN line `<<<BEGIN <NAME> ` and
exact-matching the END line `<<<END <NAME>>>`; nothing was retyped. Each name matched exactly
one BEGIN and one END line, asserted in the extractor. Whole texts were read INCLUSIVE of the
newline ending their last content line; every `_FROM`/`_TO` pair half was read with that final
newline STRIPPED (constraint 2).

| Text | Convention | Disk-to-disk result |
|---|---|---|
| PLANF272R31 | whole | `.agent/plan.md` BYTE-EQUAL to the slice (1838 bytes) |
| RECORDR31 | whole | `POST_EQUALS_PRE_NL_SLICE = True`, prefix True, ordered paragraph equality True |
| SLIPSR31 | whole | `POST_EQUALS_PRE_NL_SLICE = True`, prefix True |
| D18SLICE | whole | `POST_EQUALS_PRE_NL_SLICE = True`, prefix True |
| STATUSPAIR_FROM/_TO | pair | FROM 1→0, TO 1, one-replacement equality True; the applied line is byte-equal to _TO |
| READMECOUNTPAIR_FROM/_TO | pair | FROM 1→0, TO 1, one-replacement equality True |
| READMETIERPAIR_FROM/_TO | pair | FROM 1→0, TO 1, one-replacement equality True |
| READMECAPPAIR_FROM/_TO | pair | FROM 1→0, TO 1, one-replacement equality True |
| QUEUEPAIR_FROM/_TO | pair | FROM 1→0, TO 1, one-replacement equality True |

Every FROM was counted BEFORE anything was written, and the script was built to ABORT without
touching a single file had any FROM not occurred exactly once. None had to.

## Deviations & assumptions

1. NO DEPARTURE FROM THE BLOCK'S ORDERED COMMIT SEQUENCE. C0a, C0b, C1, C2, C3, C4, C5 were
   committed in that order, one commit each, with the block's declared path set and nothing
   else. No commit was added, dropped or reordered.

2. ASSUMPTION — THE SESSION NUMBER. The block does not state it and the previous handback
   records `SESSION 12 · round 30`. This round is booked as SESSION 12, round 31, on the
   ground that no session boundary was crossed between round 30's handback and this round's
   block: the reviewer gated round 30 in the primary checkout at `e388c603` and issued round
   31 in continuation. If Window 1 knows a boundary WAS crossed, the correct reading is
   session 13, and the F272 session soft limit is then breached by one — which changes
   nothing about this closure, because the split-and-close default was already executed in
   round 26 and this round is the close it prescribes. Recorded here rather than guessed
   silently.

3. SELF-REFERENCE, three values this file cannot carry. C5's own SHA, C5's own `numstat` row
   for `.agent/handoff.md`, and the PR number and URL do not appear above, because the file
   is written before the commit exists and the PR is created after it (the R-0149 pattern the
   handback template names). All three are measured and reported in the round report to
   Window 1. The `.agent/STOP` reading before the PR is created is in the same position.

4. NO DISAGREEMENT WITH ANY SLICE OR PAIR. Constraint 1 asks that a slice believed wrong be
   applied as written and the disagreement declared. Every slice and every pair was applied
   verbatim and none was believed wrong: all five FROM counts were 1 as stated, all five
   `TO.find(FROM)` classifications came back REWRITE as the block's table said, and every
   base measurement the block asserted — `live_review.md` 487792/535 with sha256 beginning
   `90bb842f424f8dea`, `prose_slips.md` 153776/571, `decisions.md` 869442/10887, the three
   triple-newline counts of 0, 1 and 5, HEAD `e388c603`, 14 worktrees — was confirmed on disk
   before it was used. The block's expected count transitions (62→62, 2→2, 60→60, 30→31,
   0→1, 0→0, 2→3) were all met exactly, and G6's four suite sizes (303, 30, 23, 42) matched
   the reviewer's own measurements.

5. SCRATCH FILES. The round's scripts were written under the gitignored `.remedy-wt/` and
   removed BY EXACT PATH afterwards — never by a glob. `.remedy-wt/f272-r31-block.md` is
   deliberately KEPT: it is the first link of the G1 transport chain. `git ls-files
   .remedy-wt` is empty and `git status --porcelain` is empty, so none of this reached the
   index at any point.

6. THE CLOSE IS `PASS_WITH_RISKS` AND IT NAMES ITS RISKS. Five High findings are open —
   R-0803, R-0804, R-0806, R-0807 and R-0827 — all owned by F273, whose Done clause covers
   "anything registered after 2026-09-06". DECISION F272 D17 rules why naming them is the
   honest close rather than a stop. Separately, `remedy integrity check` PASSES while its
   `high_blockers_open` check reports "no open blocker/high findings", which is false with
   five High findings open; that is the already-open R-0648, the PR body states it, and this
   closure rests on the named list rather than on that check.

7. ONE AUTHORING SLIP IN THIS FILE, CAUGHT BY THE PRE-COMMIT SELF-REVIEW AND NEVER COMMITTED.
   The first draft of the G1 section above carried a HAND-TYPED, ABBREVIATED transport digest
   instead of the measured one. The AGENTS.md self-review loop caught it before C5 existed,
   and the section was rewritten by a script that recomputes all three digests from disk and
   prints the untruncated 64-character value, so no digest in this file was typed by hand. The
   slip damaged nothing on disk and is recorded here rather than as an R-id, per amend0827
   rule 2: a reviewer-or-worker prose inaccuracy that reached no committed state is a
   deviation, not a finding. The lesson generalises — a digest is copied from a measurement,
   never retyped, and that applies to the handback as much as to a gate.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C0a save the block to `.agent/authored/f272-r31.md` | done | |
| C0b mirror to `.agent/last_block.md` | done | |
| C1 `.agent/plan.md` = PLANF272R31 | done | |
| C2 append RECORDR31 to `.agent/live_review.md` | done | |
| C3 append SLIPSR31 to `.agent/prose_slips.md` | done | |
| C4 append D18SLICE to `.agent/decisions.md` | done | |
| C5 the closure commit (STATUS, README, queue, handoff) | done | one commit, last on the branch |
| G1 transport | done | one digest comparison, three artefacts identical |
| G2 the finding record | done | (a) byte (b) structural (c) negative control (d) counts |
| G3 the two prose files | done | plan byte-equal and under the 50-line cap; slips byte-append |
| G4 the decision record | done | D18 heads exactly one section, 2→3 |
| G5 the closure commit gates | done | (a)–(g) all measured |
| G6 the ledger gates | done | four suites, serial, exit 0, 303/30/23/42 |
| G7 the tree and the pull request | done | tree clean throughout; push and PR after this commit, reported in the round report |
| PR created | done | after C5; number and URL in the round report |
| PR merged | not done — FORBIDDEN | guardrail G1: the session that creates a PR never merges it; the merge belongs to the next feature's Open PR Gate |

## Next

MERGE THE PULL REQUEST AT THE NEXT FEATURE'S START, and not before — that gap is the
operator's manual-review window, and the operator may merge manually at any time instead. The
next session's FIRST action is Phase 1 rule 1 of `docs/agents/self_drive_protocol.md`: read
`.agent/STOP` from disk. Then rule 2, the AGENTS.md Open PR Gate, which merges this PR with
`gh pr merge <n> --merge --delete-branch`, then `git checkout main` and `git pull --ff-only`.

Then Rule A5 proposes F274 — One world completion, part two — which sits directly after F272
in the ledger by amend0906-split-placement and owns T004's remainder (the atomic
classic-to-unified record flip) and T005 (the prototype cluster deletion). F274's first slice
is the DECISION F272 D7 raising-property probe and a ruling on the per-commit cap, NOT the
flip itself: DECISION F272 D15 measured the flip as ATOMIC over the consumer graph, so it
cannot be staged, and its size against the 500-insertion cap has to be ruled on before it is
attempted.

`.agent/candidates.md` CARRIES NO OPEN CANDIDATE — the file is 1903 bytes of header and
discharge history and its state line reads "EMPTY — no candidate is open." — so no candidate
registration is owed at the next feature's first reviewed round. If the reviewer's gate over
THIS closure commit raises one, DECISION amend0827 D2 permits a `.agent/candidates.md`-only
commit after C5 as the single permitted successor; this worker was ordered that C5 is the
last commit and therefore wrote no such commit. The self-use queue is EXHAUSTED (SU-012 consumed by F272, zero pending),
so the next closure must call `generate_and_append_if_empty` before it can consume an item.
The next free finding id is R-0829; this round minted none and resolved none, and the open set
stands at 60 by distinct id.
