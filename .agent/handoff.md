# Handback — F272 round 30

## CLOSURE VALUES — the seven fields the next round authors the STATUS line from

These are stated here BY NAME because `.agent/handoff.md` is rewritten at every handback and
the closure round reads them from nowhere else. Every one was measured, not carried.
NOTE: this file is written BEFORE its own commit exists, so the scratch-file deletions
declared in deviation 7 were performed immediately before that commit and the tree was
confirmed clean at it.

    EVIDENCE JOB ID              abf14422b1badab6
    PACKAGE FILENAME             remedy-review-20260907-173909-READY_FOR_REVIEW.zip
    PACKAGE SHA-256              8bbce2fa27ddd6c68398d381d1367e6e509b49cbacac0a29ff06329d9aebb706
    PACKAGE ABSOLUTE DIRECTORY   /home/decodeux/Repos/remedy-history/zips
    ACCEPTED HEAD                7f71b30ac3b2f1fefb2da6063f0453d650d3835a
    PACKAGE_STATUS               READY_FOR_REVIEW
    OPEN FINDINGS BY DISTINCT ID 60

ACCEPTED HEAD is the full sha of C4, the last CONTENT commit, and it is also the head the
manifest recorded: `committed_review_subject.head_commit` reads
`7f71b30ac3b2f1fefb2da6063f0453d650d3835a` and `committed_review_subject.base_commit` reads
`b18fad576252f7f2739a5807b6408031da8fcde6`, the fork point, over 243 commits and 184 files.
The handback commit C5 that writes this file is NOT the accepted head.

PACKAGE ABSOLUTE DIRECTORY is a real archived location, not `NOT ARCHIVED`: the packaging
script placed the zip at `/home/decodeux/Repos/remedy-history/zips`, which is OUTSIDE this
repository. See deviation 3 — the block predicted the repo root.

OPEN FINDINGS BY DISTINCT ID — 60, WITH ITS ARITHMETIC, and it is stated TWICE because the
ledger rotation at C4 changes both operands while leaving the difference identical:

    BEFORE THE ROTATION (the ledger as it stood at C3)
      distinct `^- R-\d{4} ` registrations   = 312
      distinct `^Done: R-\d{4}` resolutions  = 252
      OPEN BY DISTINCT ID                    = 312 - 252 = 60

    AFTER THE ROTATION (the ledger as it stands at C4, and at HEAD)
      distinct `^- R-\d{4} ` registrations   =  62
      distinct `^Done: R-\d{4}` resolutions  =   2
      OPEN BY DISTINCT ID                    =  62 -   2 = 60

The rotation moved 250 RESOLVED PAIRS, so it removed 250 registrations AND the 250 matching
resolutions: 312 - 250 = 62 and 252 - 250 = 2. The difference is invariant, which is exactly
what the amend0905-throughput amendment requires the script to preserve, and it is what G4(c)
gated. The SCRIPT'S OWN LINE FORMULA — registration LINES minus `Done:` LINES — reads 58 both
before (312 - 254) and after (62 - 4), because R-0721 and R-0725 each carry a two-paragraph
resolution and so contribute two `Done:` LINES against one distinct id apiece. Both readings
are correct for what they measure. THE CLOSURE REPORTS THE DISTINCT-ID ONE: 60.

## Session

SESSION 12 of feature F272 · round 30 · rounds so far 30

SOFT LIMIT, under operator amendment amend0906-triage-throughput rule 2, which sets F272's
limit at 12 SESSIONS and 40 ROUNDS by name: the SESSION half REMAINS REACHED — this is still
session 12 of 12. The round half is not: this is round 30 of 40. The SPLIT half of the
amend0905-throughput split-and-close default was executed in round 26 (F274 registered,
DECISION F272 D16); this round is the fifth step of the CLOSE half — it rotates the ledger and
builds the evidence job and the review zip, which are closure algorithm steps 1 and 2.

SITZUNGS-LIMIT ERREICHT — OPERATOR-BERICHT IN DER ÜBERGABE

CONTEXT SELF-ASSESSMENT (amend0905-throughput, one sentence): context is comfortable — this
round read the block, AGENTS.md, the closure protocol, the self-drive protocol, the handback
template, the rotation script and the previous handoff in full, and handled every large state
file (`live_review.md` 1.24 MB before the rotation, `live_review_archive.md` 2.54 MB after,
`prose_slips.md` 153 KB, the 25 MB package) by measurement rather than by reading it.

The scope report the limit obliges was written in full in round 26's handback and is durable
on disk as the `## Built State` section of `docs/roadmap/features/T2_F272.md`. It is not
re-derived here. WHAT IS FINISHED as of this round: T001, T002 and T003 complete; closure
preconditions 1 (round 29, DECISION F272 D17), 2 (round 27's integration gate, re-confirmed by
G7 here), 3 (`run_integrity_checks()` passed True, fail_count 0, untracked=0/relevant=0), 4
(Built State) and 6 (round 28, booked at round 29's C3) all discharged; and now closure
ALGORITHM steps 1 and 2 — the evidence job and a READY_FOR_REVIEW package — plus the
amend0905-throughput ledger rotation. WHAT IS MISSING: precondition 5's final leg and
algorithm steps 4 and 5 — the STATUS `[x]` line, the README capability sync, SU-012's
`consumed_by`, and the PR. The proposal is unchanged and already executed: close F272 at
DECISION F272 D16's scope, PASS_WITH_RISKS, with F274 carrying T004's remainder and T005.

## Range

Review of `c286fd92`..`7f71b30a`.

The range ends at C4, the last commit that EXISTS while this file is being written. C5 is the
commit that writes this file and cannot state its own SHA; the reviewer's range is
`c286fd92`..HEAD once C5 lands. C4 is also the ACCEPTED HEAD, deliberately: the evidence job
and the zip were built from a clean tree at C4, before this handback commit existed.

## Commits

### 71bf4d64 f272: save the round 30 block as authored text  (C0a)
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f272-r30.md | +304 / -0 | `shutil.copyfile` of `.remedy-wt/f272-r30-block.md` per constraint 3 |

### fca38fdd f272: mirror the round 30 block into last_block  (C0b)
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +239 / -194 | the same `shutil.copyfile`, the mirror |

### 3501c8b5 f272: point the plan at the round 30 closure sequence  (C1)
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +20 / -20 | replaced byte for byte with the PLANF272R30 slice |

### e41c7d62 f272: book the round 29 PASS verdict into the record  (C2)
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2 / -0 | append of RECORDR30, the `Gate: F272 R29` PASS entry |

### 37ff07bf f272: record the round 29 block prose slip on the begin marker wording  (C3)
| Path | +/- | Reason |
|---|---|---|
| .agent/prose_slips.md | +2 / -0 | append of SLIPSR30, one dated line, no id spent |

### 7f71b30a f272: rotate the live review ledger into the archive  (C4)
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +0 / -1612 | the 23 `Gate:` records of `[x]` features and the 250 resolved finding pairs leave the ledger; written by `scripts/rotate_live_review.py`, never by hand |
| .agent/live_review_archive.md | +1612 / -0 | the same 1612 lines arrive byte-verbatim in the append-only archive |

### C5 f272: hand back round 30
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | (self-referential) | this file; a handoff cannot table the commit that writes it (R-0149 pattern) |

Every `+/-` cell above is the real `git diff --numstat <parent> <commit>` figure and was
compared cell for cell against G8's per-commit table below. They agree.

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a | done | `.agent/authored/f272-r30.md`, copyfile, digest-identical to the delivered block |
| C0b | done | `.agent/last_block.md`, same copyfile, digest-identical |
| C1  | done | `.agent/plan.md` byte-equal to PLANF272R30, 2010 bytes, 38 lines |
| C2  | done | RECORDR30 appended; `^Gate:` 52 -> 53, `^Gate: F272 R29 ` 0 -> 1 |
| C3  | done | SLIPSR30 appended, `POST_EQUALS_PRE_NL_SLICE` true |
| C4  | done | the rotation, exit 0, path set exactly the two ledger files, open set unchanged |
| C5  | done | this handback |

No item was skipped and none deviated. The evidence job (G5) and the review zip (G6) are
GATES, not commits, per the block's Bundle section: neither the evidence directory nor the
package is committed, and neither appears in any commit's path set.

## External actions

| Action | Command | Outcome |
|---|---|---|
| push (after C4, before the zip) | `git push -u origin feature/f272-one-world-completion` | `c286fd92..7f71b30a`, exit 0, upstream set; `git rev-parse origin/feature/f272-one-world-completion` = `7f71b30ac3b2f1fefb2da6063f0453d650d3835a` |
| push (after C5) | `git push` | a second push after the final commit, expected and declared by the round's transport note |
| review zip build | `bash scripts/make_review_zip.sh --evidence-dir .remedy-wt/r30-evidence-abf14422b1badab6` | exit 0, `PACKAGE_STATUS=READY_FOR_REVIEW`, 4154 members, 25 MB |
| evidence bundle | `packages.orchestration.job_evidence.create_manual_completion_bundle(...)` in Python | exit 0, job `abf14422b1badab6`, verdict `PASS_WITH_RISKS` |
| worktree add | none | constraint 9 forbids creating one, and no round work needed one |
| worktree remove | none | constraint 9 forbids removing any; `git worktree list` is 14 before and 14 after |
| PR create / edit / merge | none | the block orders none; the closure PR is the NEXT round |
| `gh` commands | none | none was ordered and none was run |

## Verification

Every gate was run as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`, with no pipe between the command
and the echo, so every exit code below is the command's own and not a pipeline's last stage.
No gate went red. `git status --porcelain` was read at every commit boundary and was EMPTY
every time, and again immediately before the evidence job and before the zip.

**RECEIPT CHECK, before the block was opened.** All three stated measurements agreed with the
file on disk, so nothing was written on a mismatch:

    stated:   23472 bytes / 304 lines / 6a94bb428eb5d56377b8aa688fd242fa8c5afd040e89b4c6f6e7ea24c01ccf05
    measured: 23472 bytes / 304 lines / 6a94bb428eb5d56377b8aa688fd242fa8c5afd040e89b4c6f6e7ea24c01ccf05
    ALL THREE AGREE
    REAL_EXIT=0

**G1 TRANSPORT — exit 0, PASS.** One digest comparison over three artefacts. This reading was
taken by a READ-ONLY script; unlike round 29's, it re-ran no `shutil.copyfile` and had no
persistence side effect.

    .remedy-wt/f272-r30-block.md (as delivered)      bytes=23472 lines=304 sha256=6a94bb428eb5d56377b8aa688fd242fa8c5afd040e89b4c6f6e7ea24c01ccf05
    .agent/authored/f272-r30.md  (committed at C0a)  bytes=23472 lines=304 sha256=6a94bb428eb5d56377b8aa688fd242fa8c5afd040e89b4c6f6e7ea24c01ccf05
    .agent/last_block.md         (committed at C0b)  bytes=23472 lines=304 sha256=6a94bb428eb5d56377b8aa688fd242fa8c5afd040e89b4c6f6e7ea24c01ccf05
    ALL_THREE_IDENTICAL = True
    MATCHES_DELIVERED_MEASUREMENTS = True
    REAL_EXIT=0

Per §3 item 37 this chain covers those three artefacts and is not a claim about the bytes
emitted into a prompt.

**G2 THE FINDING RECORD at C2 — exit 0, PASS.** Every count landed on the block's stated
figure; none was adjusted to agree.

    === G2(a) BYTE ===
    slice RECORDR30: 4314 bytes, sha256 86b6c88aceb8b1b8410b97ded3860ea4f97f00f85e2b3629dab36ef064202928
      slice terminal12 = b'ng to hold.\n'  slice trailing_nl_run = 1
    pre_len = 1238279   pre_sha256 = 3b6622ba52c6b814af4d7932a845c080a8136a54708e3d846bbadc9cc9ef7761
      pre terminal12 = b'ted for it.\n'   pre trailing_nl_run = 1
    post_len = 1242594  post_sha256 = 249209eea2b5a1e6b0a62755971f30ad4aca19d90e8da47b5b02426088696af5
      post terminal12 = b'ng to hold.\n'  post trailing_nl_run = 1
    PRE_IS_BYTE_EXACT_PREFIX_OF_POST = True
    POST_EQUALS_PRE_NL_SLICE = True
    === G2(b) STRUCTURAL ===
    N_COUNTED_FROM_SLICE = 1
    units_before = 738   units_after = 739
    LAST_N_UNITS_EQUAL_SLICE_PARAGRAPHS_IN_ORDER = True
    EVERYTHING_BEFORE_UNCHANGED = True
    === G2(c) NEGATIVE CONTROL (memory only) ===
    flip_offset = 1240436   INSIDE_FIRST_APPENDED_PARAGRAPH = True
    NEG_CONTROL_BYTE_READER_REJECTS = True
    NEG_CONTROL_STRUCTURAL_READER_REJECTS = True
    DISK_UNTOUCHED_BY_CONTROL = True
      re-read sha256 = 249209eea2b5a1e6b0a62755971f30ad4aca19d90e8da47b5b02426088696af5
    === G2(d) COUNTS (pre -> post) ===
      distinct ^- R-dddd            312 ->  312
      distinct ^Done: R-dddd        252 ->  252
      OPEN SET BY DISTINCT ID        60 ->   60
      ^Gate:                         52 ->   53
      ^Gate: F272 R29                 0 ->    1
      ^- R-0829                       0 ->    0
      (also: ^Done: LINES 254 -> 254, ^- R-dddd LINES 312 -> 312)
    REAL_EXIT=0

The block's stated pre-image — 1238279 bytes, 2145 lines, sha256 beginning `3b6622ba52c6b814`
— was met exactly. N was COUNTED BY THE SCRIPT from the slice (`len(paragraphs)` = 1) and was
never taken from the block; RECORDR30 is a single paragraph, so N is 1 and the FIRST appended
paragraph and the LAST are the same unit — the negative control's placement requirement is
satisfied trivially and is stated so rather than claimed as a discrimination it cannot make.
`R-0829` is still free, as constraint 8 requires.

**G3 THE TWO PROSE FILES — exit 0, PASS.**

`.agent/plan.md`, re-read from disk after the write:

    POST_IS_BYTE_EQUAL_TO_SLICE (PLANF272R30) = True
    plan bytes = 2010   plan lines = 38   sha256 = 3d8d436e93e337ed6260258bb89d37292e70413a31226da8963ac0d923b6a5b0
    lines 38 vs the AGENTS.md cap of 50 -> UNDER_CAP = True
    HAS_GOAL_HEADING = True
    HAS_NEXT_STEPS_HEADING = True
    REAL_EXIT=0

`.agent/prose_slips.md`, the byte append check only:

    slice SLIPSR30: 657 bytes, sha256 5b0864434d156f8ac1990de45aba840486af7dd83fbeb90d7773407abc993eb3
    pre_len = 153118   pre_lines = 569   (the block's stated figures, met exactly)
    pre_sha256 = 1f3951808f796f135bb1730b29efaceb439375fc0bb47eb9456aaf6a0faee7a0
    post_len = 153776  post_lines = 571
    post_sha256 = 68c53339f00477715cf79b2963479fbcd028a7a1467e492050b23bb2027fede5
    PRE_IS_BYTE_EXACT_PREFIX_OF_POST = True
    POST_EQUALS_PRE_NL_SLICE = True
    triple-newline occurrences: 1 before, 1 after (pre-existing, NOT repaired)
    REAL_EXIT=0

Constraint 4's per-file newline measurement was re-taken at `c286fd92`: three consecutive
newlines occur 0 times in `.agent/live_review.md` and 1 time in `.agent/prose_slips.md`, as
stated. The OFFSET of that one occurrence is not what the block states — see deviation 2.
Neither file's trailing-newline run moved: 1 before and 1 after, on both.

**G4 THE ROTATION at C4 — exit 0, PASS.** The script's FULL stdout, verbatim:

    $ python3 scripts/rotate_live_review.py
    gate records moved: 23
    finding pairs moved: 250 (500 records)
    old ledger size: 1242594 bytes
    new ledger size: 487792 bytes
    old archive size: 1780229 bytes
    new archive size: 2535031 bytes
    open findings before: 58
    open findings after: 58
    written: /home/decodeux/Repos/remedy/.agent/live_review.md and /home/decodeux/Repos/remedy/.agent/live_review_archive.md
    REAL_EXIT=0

It was run with NO ARGUMENTS and its output was committed exactly as written: nothing was
reformatted, no record was moved by hand, and the pre-existing double blank line in
`.agent/prose_slips.md` was not repaired. The script did not refuse.

Then, measured by me and NOT read from that stdout. The pre-images were taken from
`git show HEAD:<path>` at C3, whose ledger digest is byte-identical to the reading I took from
the file before running the script, so the two routes agree:

    (a) LEDGER  bytes  1242594 -> 487792
        ARCHIVE bytes  1780229 -> 2535031
        PRE_IMAGE_DELTA_AGAINST_THE_DRY_RUN'S 1238279 = +4315
    (b) PRE_ARCHIVE_IS_BYTE_EXACT_PREFIX_OF_POST_ARCHIVE = True
    (c) BEFORE  BY_DISTINCT_ID: 312 - 252 = 60   BY_SCRIPT_LINE_FORMULA: 312 - 254 = 58
        AFTER   BY_DISTINCT_ID:  62 -   2 = 60   BY_SCRIPT_LINE_FORMULA:  62 -   4 = 58
        OPEN_BY_DISTINCT_ID_UNCHANGED = True     OPEN_BY_LINE_FORMULA_UNCHANGED = True
    (d) ^Gate: F272 R  count  30 before, 30 after -> UNCHANGED = True
        ^Gate: total             53 before, 30 after (53 - 23 moved = 30)
    (e) git diff --name-only 37ff07bf 7f71b30a
        .agent/live_review.md
        .agent/live_review_archive.md
        REAL_EXIT=0
    REAL_EXIT=0

THE DRY-RUN FIGURES WERE NOT TREATED AS A TARGET, and the difference is visible rather than
silent. The reviewer's `--dry-run` at `c286fd92` reported 1238279 -> 483477 for the ledger. My
pre-image is 1242594, larger by EXACTLY 4315 = RECORDR30's 4314 bytes plus the one separator
newline C2 added, and my post-image is 487792, larger by exactly the same 4315 (487792 -
483477 = 4315). The archive figures 1780229 -> 2535031 match the dry run to the byte, which is
coherent: the record C2 added is `Gate: F272 R29`, F272 is still `[~]`, so it did not move and
could not change the archive. The moved-record counts also match the dry run at 23 gates and
250 pairs. F272's OWN gate records did NOT move: 30 before and 30 after, so all 23 that moved
belonged to `[x]` features.

**G5 THE EVIDENCE JOB — closure algorithm step 1 — exit 0, PASS.**

FIRST, THE BASE PROOF, taken BEFORE the producer was called, with base
`b18fad576252f7f2739a5807b6408031da8fcde6` and head the full sha of C4:

    git rev-list --ancestry-path b18fad57..7f71b30a   count = 243   exit 0
    git rev-list                 b18fad57..7f71b30a   count = 243   exit 0
    THE_TWO_ARE_EQUAL = True
    git merge-base --is-ancestor b18fad57 main -> exit 0 -> BASE_IS_ANCESTOR_OF_main = True
    FIRST_PARENT_FORK_POINT = b18fad576252f7f2739a5807b6408031da8fcde6  EQUALS_DECLARED_BASE = True
    FOR CONTRAST, git merge-base HEAD main = 148fbd0b4f3bbc7d5d57a81af080e53359e95681
    git status --porcelain -> '' -> EMPTY = True
    REAL_EXIT=0

The counts are EQUAL, so the base is right and the F260 round 22 defect is not present. The
contrast reading is recorded because it is the whole reason the fork point is specified: the
merge-base answers `148fbd0b`, a different commit, exactly as the block warned.

THE PRE-SCAN, before the producer, over every node id and every test file:

    SCANNED_NODE_IDS 303   SCANNED_TEST_FILES 2
    FLAGGED_COUNT 0
    FLAGS_NONE_OF_THEM = True
    SCANNER_IS_LIVE (control, an absolute path) -> 'a local absolute path'
    RUN_ID_ACCEPTED_BY _VT_RUN_ID_RE -> True  (vr-3001)
    REAL_EXIT=0

The scanner flags NONE of the 305 strings, and the control proves the scanner is live rather
than vacuously silent. No full-suite node-id list was recorded anywhere — the record carries
the SCOPED `tests/docs/` selection only, per pitfall (d).

THE VERIFICATION RUN the record carries, a REAL run at C4 in the primary checkout:

    $ python3 -m pytest tests/docs/ -q
    303 passed in 0.59s
    REAL_EXIT_CODE = 0    duration_seconds = 0.831
    run_id = vr-3001  (matches ^vr-\d{4,}$)
    passed 303, failed 0, skipped 0, deselected 0, selected 303
    node_ids from a real --collect-only of the SAME selection: 303
    LEN_NODE_IDS_EQUALS_SELECTED = True
    test_files (FILES, sorted, never a directory):
        tests/docs/test_docs_consistency.py
        tests/docs/test_vocabulary.py
    stdout_summary length 420 (< 4000)
    output_hash = a3fc861c756ba65b172f38001d33ee1a58756a1b49903c3600f6e0c2e4956e8b
      (sha256 hex of EXACTLY that stdout_summary string)
    head_sha = 7f71b30ac3b2f1fefb2da6063f0453d650d3835a
    REAL_EXIT=0

303 collected against 303 passed — the two agree today, as the reviewer measured at
`c286fd92`. THE PRODUCER CALL and the summary dict it returned, IN FULL:

    GIT_STATUS_PORCELAIN_BEFORE_PRODUCER = '' -> EMPTY = True
    HEAD_CONFIRMED = 7f71b30ac3b2f1fefb2da6063f0453d650d3835a  EQUALS_C4 = True
    JOB_ID = abf14422b1badab6  (16 chars, lowercase hex, from secrets.token_hex(8))
    EVIDENCE_DIR = /home/decodeux/Repos/remedy/.remedy-wt/r30-evidence-abf14422b1badab6
      PRE_EXISTS = False  (a FRESH directory under the gitignored .remedy-wt/)
    base_commit = b18fad576252f7f2739a5807b6408031da8fcde6  (full 40 chars, never abbreviated)
    head_commit = 7f71b30ac3b2f1fefb2da6063f0453d650d3835a
    job_title = F272 one world completion closure evidence
    step_range = T001-T004    prior_job_ids = []    review_feature_id = f272
    timestamp = generated_at = 2026-09-07T15:38:43Z

    === RETURNED SUMMARY DICT (full) ===
    {
     "authority_count": 123,
     "commit_count": 243,
     "head_commit": "7f71b30ac3b2f1fefb2da6063f0453d650d3835a",
     "job_id": "abf14422b1badab6",
     "manual_completion": true,
     "operator_attested_tasks": ["T001", "T002", "T003"],
     "partition": {"T001": 41, "T002": 41, "T003": 41},
     "total_passed": 303,
     "verdict": "PASS_WITH_RISKS"
    }
    GIT_STATUS_PORCELAIN_AFTER_PRODUCER = '' -> EMPTY = True
    REAL_EXIT=0

THE JOB ID IS `abf14422b1badab6` AND THE VERDICT IT NAMES IS `PASS_WITH_RISKS`.

**G6 THE REVIEW ZIP — closure algorithm step 2 — exit 0, PASS, READY_FOR_REVIEW.**
`git status --porcelain` was EMPTY and the branch was pushed through C4 first. FULL stdout:

    $ git status --porcelain -> '' (EMPTY)
    $ bash scripts/make_review_zip.sh --evidence-dir .remedy-wt/r30-evidence-abf14422b1badab6
    UNCHANGED: runtime_integration_gate.json — rebuilt from source; identical to existing
    Evidence refresh completed for staged copy.
    Observability index generated from staged bytes: evidence/current/self_run_observability_index.json
    {"member_count": 4154, "authoritative_count": 123, "symlink_count": 0, "tombstone_count": 0, "final_path": "/home/decodeux/Repos/remedy-history/zips/remedy-review-20260907-173909-READY_FOR_REVIEW.zip", "final_sha256": "8bbce2fa27ddd6c68398d381d1367e6e509b49cbacac0a29ff06329d9aebb706", "publication_capability": "SUPPORTED", "package_status": "READY_FOR_REVIEW", "evidence_authoritative": true, "review_subject_alignment": "PASS", "manifest_sha256": "93d9de399590468c7d83733d9395325ba7f9d744fe9d0f1ad2c7cccbbe2a2b73"}

    ============================================
    REVIEW_PACKAGE_CREATED=true
    PACKAGE_STATUS=READY_FOR_REVIEW
    PACKAGING_CWD=/home/decodeux/Repos/remedy
    EVIDENCE_DIR=.remedy-wt/r30-evidence-abf14422b1badab6
    REVIEW_SUBJECT_ALIGNMENT=PASS
    EVIDENCE_AUTHORITATIVE=true
    REVIEW_PACKAGE_DIR=/home/decodeux/Repos/remedy-history/zips
    ZIP_PATH=/home/decodeux/Repos/remedy-history/zips/remedy-review-20260907-173909-READY_FOR_REVIEW.zip
    ============================================

    ZIP CREATED AND READY FOR FINAL REVIEW

    25M	/home/decodeux/Repos/remedy-history/zips/remedy-review-20260907-173909-READY_FOR_REVIEW.zip
    Included files: 4154
    Branch: feature/f272-one-world-completion
    Commit: 7f71b30ac3b2f1fefb2da6063f0453d650d3835a
    Evidence: evidence/current/
    REAL_EXIT=0

Recomputed and cross-checked from the file on disk, and read back out of the packaged manifest:

    PACKAGE FILENAME            remedy-review-20260907-173909-READY_FOR_REVIEW.zip
    PACKAGE ABSOLUTE DIRECTORY  /home/decodeux/Repos/remedy-history/zips
    package bytes               25675030
    SHA-256 as the script printed it  8bbce2fa27ddd6c68398d381d1367e6e509b49cbacac0a29ff06329d9aebb706
    SHA-256 as I recomputed it        8bbce2fa27ddd6c68398d381d1367e6e509b49cbacac0a29ff06329d9aebb706
    SHA256_AGREE = True
    committed_review_subject.base_commit = b18fad576252f7f2739a5807b6408031da8fcde6
    committed_review_subject.head_commit = 7f71b30ac3b2f1fefb2da6063f0453d650d3835a
    committed_review_subject.base_is_ancestor = True   commit_count = 243   file_count = 184
    SPANS_b18fad57_TO_C4 = True
    package_status = READY_FOR_REVIEW
    validation_errors: the manifest carries NO key of that name at all, and
      packaging_warnings = [], external_paths_detected = [],
      source_root_containment = {"blockers": [], "verdict": "PASS"},
      snapshot_inventory_status = {"ok": true, "problems": []},
      git_status_snapshot = {"diagnostic": "", "status": "OK"},
      final_verifier_reproducible = true,
      packaged_evidence_job_id = abf14422b1badab6,
      packaged_evidence_manifest_task_ids = ["T001", "T002", "T003"]
    GIT_STATUS_PORCELAIN_AFTER_ZIP = '' -> EMPTY = True
    REAL_EXIT=0

`PACKAGE_STATUS` IS `READY_FOR_REVIEW`, so constraint 7's stop path did not fire. Nothing was
adjusted to reach it: the base, every evidence field and every source file are as measured, on
the first and only build attempt of this round.

**G7 THE PRECONDITIONS, run SERIALLY in the primary checkout at C4 — exit 0 each, PASS.**

    $ python3 -B -m pytest tests/docs/ -q -p no:randomly
    ........................................................................ [ 23%]
    ........................................................................ [ 47%]
    ........................................................................ [ 71%]
    ........................................................................ [ 95%]
    ...............                                                          [100%]
    303 passed in 0.49s
    REAL_EXIT=0

    $ python3 -B -m pytest tests/cli/test_golden_path.py -q -p no:randomly
    ..........................................                               [100%]
    42 passed in 21.02s
    REAL_EXIT=0

303 and 42 reproduce the reviewer's figures exactly. Then `run_integrity_checks()`, called
directly in Python because the built `remedy` binary is denied in this session, reading
ATTRIBUTES and not dict keys:

    TYPE = IntegrityGateResult
    .passed     = True
    .fail_count = 0
    len(.checks) = 5
      IntegrityCheck(name='handler_import',       status=PASS, message='handlers=341')
      IntegrityCheck(name='live_review_verdict',  status=PASS, message='> Round-by-round review record, re-headed at the F272 claim per')
      IntegrityCheck(name='plan_consistency',     status=PASS, message='unchecked=0, context_complete=False')
      IntegrityCheck(name='relevant_untracked',   status=PASS, message='untracked=0, relevant=0')
      IntegrityCheck(name='high_blockers_open',   status=PASS, message='no open blocker/high findings')
    REAL_EXIT=0

THE `high_blockers_open` CHECK'S OWN MESSAGE, VERBATIM: `no open blocker/high findings`. THAT
MESSAGE IS FALSE AND THE CLOSURE STATES IT RATHER THAN LEANING ON IT. Measured against the
post-rotation ledger in the same run:

    R-0803 registered_lines=1  has_Done=False  OPEN=True
    R-0804 registered_lines=1  has_Done=False  OPEN=True
    R-0806 registered_lines=1  has_Done=False  OPEN=True
    R-0807 registered_lines=1  has_Done=False  OPEN=True
    R-0827 registered_lines=1  has_Done=False  OPEN=True

Five High findings are open while the check reports none. That is the already-open R-0648, it
is not repaired here, and the closure paragraph must name all five with F273 as their owner
per DECISION F272 D17. Note for the record: `.passed` and `.fail_count` are attributes on the
RESULT, as the block states; the individual `IntegrityCheck` records carry `status`, not
`passed`, so a reader probing `check.passed` gets `None` rather than a boolean.

**G8 THE TREE — exit 0, PASS.**

    git status --porcelain exit 0 -> ''   EMPTY = True
    git ls-files .remedy-wt exit 0 -> ''  EMPTY = True
    git worktree list exit 0  entries = 14  EQUALS_14 = True
        /home/decodeux/Repos/remedy                                  [feature/f272-one-world-completion]
        + thirteen /home/decodeux/Repos/remedy/.remedy-wt/job-*  worktrees,
          the newest being remedy/job-020c1ef366af4f07 from round 28's product run
    branch = feature/f272-one-world-completion
    origin/feature/f272-one-world-completion = 7f71b30ac3b2f1fefb2da6063f0453d650d3835a
    PUSHED_THROUGH_C4 = True
    REAL_EXIT=0

14 entries at the base and 14 at the end, unchanged per constraint 9. I created no worktree and
removed none.

`git status --porcelain` at every commit boundary, real output each time:

    after C0a: ''   after C0b: ''   after C1: ''   after C2: ''   after C3: ''   after C4: ''
    immediately before the evidence job: ''
    immediately before the zip:          ''
    immediately after the zip:           ''

Per-commit insertions, `git diff --numstat <parent> <commit>`, C0a through C4 (C5 excluded,
because a commit cannot count its own insertions while it is being written), each against the
DECISION F104 D1 cap of 500 INSERTIONS, and every commit SINGLE-PARENT:

    C0a  71bf4d64  parent c286fd92  single_parent=True  ins=304   del=0     under_500=True
    C0b  fca38fdd  parent 71bf4d64  single_parent=True  ins=239   del=194   under_500=True
    C1   3501c8b5  parent fca38fdd  single_parent=True  ins=20    del=20    under_500=True
    C2   e41c7d62  parent 3501c8b5  single_parent=True  ins=2     del=0     under_500=True
    C3   37ff07bf  parent e41c7d62  single_parent=True  ins=2     del=0     under_500=True
    C4   7f71b30a  parent 37ff07bf  single_parent=True  ins=1612  del=1612  under_500=FALSE
    REAL_EXIT=0

C4 IS OVER THE CAP AT 1612 INSERTIONS, IS EXEMPT BY NAME IN G8, AND I NAME THE EXEMPTION I AM
CLAIMING — see deviation 4, where both candidate readings are stated. These are the figures in
the per-commit tables above, compared cell for cell; they agree.

The three `.agent/STOP` readings, all by `os.path.exists`, per constraint 10:

    STOP_EXISTS_BEFORE_C0A = False
    STOP_EXISTS_BEFORE_C4  = False
    STOP_EXISTS_BEFORE_C5  = False

NO PULL REQUEST WAS CREATED, nothing was merged, nothing was force-pushed, no history was
rewritten and no branch was switched.

## Authored-text proofs

All three slices were extracted PROGRAMMATICALLY from the COMMITTED
`.agent/authored/f272-r30.md`. The BEGIN marker was matched BY THE PREFIX `<<<BEGIN <NAME> `,
including its trailing space, because every real BEGIN line carries a `target=` attribute after
the name; the END marker was matched as the exact line `<<<END <NAME>>>`. Each slice is read
exclusive of both marker lines and INCLUSIVE of the newline ending its last content line. The
extractor asserts exactly one BEGIN and exactly one END per name and fails loudly otherwise;
it found exactly one of each, at these line indexes, and printed each BEGIN line verbatim:

    PLANF272R30  BEGIN at line 256, END at 295  b'<<<BEGIN PLANF272R30 target=.agent/plan.md>>>\n'
    RECORDR30    BEGIN at line 297, END at 299  b'<<<BEGIN RECORDR30 target=.agent/live_review.md mode=append>>>\n'
    SLIPSR30     BEGIN at line 301, END at 303  b'<<<BEGIN SLIPSR30 target=.agent/prose_slips.md mode=append>>>\n'

Nothing was retyped and nothing was taken from the delegating message.

| Slice | Bytes | Lines | sha256 | Proof |
|---|---|---|---|---|
| PLANF272R30 | 2010 | 38 | `3d8d436e93e337ed6260258bb89d37292e70413a31226da8963ac0d923b6a5b0` | `.agent/plan.md` re-read from disk and byte-equal to the slice: `POST_IS_BYTE_EQUAL_TO_SLICE = True` |
| RECORDR30 | 4314 | 1 | `86b6c88aceb8b1b8410b97ded3860ea4f97f00f85e2b3629dab36ef064202928` | `POST_EQUALS_PRE_NL_SLICE = True` on `.agent/live_review.md` at C2, plus the structural reader (N=1) and the negative control |
| SLIPSR30 | 657 | 1 | `5b0864434d156f8ac1990de45aba840486af7dd83fbeb90d7773407abc993eb3` | `POST_EQUALS_PRE_NL_SLICE = True` on `.agent/prose_slips.md` at C3 |

Every slice ends in exactly one newline, and both append targets had a trailing-newline run of
exactly 1 before and after, so no append introduced blank-line drift. This round carried no
FROM/TO pair, as constraint 2 states. C4's two files are NOT in this table by design: they are
the rotation script's own output, never an authored slice, and constraint 5 forbids editing
them by hand.

## Deviations & assumptions

The block's ordered commit sequence C0a, C0b, C1, C2, C3, C4, C5 was followed EXACTLY: no extra
commit, no dropped commit, no reordering. The evidence job and the zip are gates and produced
no commit, as the Bundle section requires.

**1. DECLARED DISAGREEMENT — G5 names a module that does not exist; applied by intent and
declared, not silently corrected.** G5 orders the pre-scan through
`packages.orchestration.build_review_manifest._unsafe_text`. There is no such module:

    import packages.orchestration.build_review_manifest
    -> ModuleNotFoundError: No module named 'packages.orchestration.build_review_manifest'

The real module is `scripts/build_review_manifest.py`, where `_unsafe_text` is defined at line
1767 and `_VT_RUN_ID_RE` at line 2120 — the same file the closure protocol's pitfall (c) names
without a package path. I ran the pre-scan through THAT module, proved the block's path is
unimportable in the same script so the substitution is visible, and confirmed the scanner is
live with an absolute-path control. The gate's INTENT — that no node id or test file is
flagged — was met on the real scanner.

**2. DECLARED — constraint 4's stated OFFSET for the pre-existing double blank line is wrong;
the COUNT is right and neither was repaired.** Constraint 4 says the one occurrence of three
consecutive newlines in `.agent/prose_slips.md` is at offset 39213. Measured at `c286fd92`:

    triple_nl_count = 1            (as stated)
    first_triple_nl_offset = 38927 (stated: 39213)

The count, which is the load-bearing part, is exact; the offset is 286 bytes off. Nothing
depends on the offset — the append is a byte-suffix operation — and constraint 4 forbids
repairing the blank line, so I changed nothing. Recorded so the reviewer can correct the figure
rather than carry it forward.

**3. DECLARED — constraint 6 predicts the wrong location for the package, and I confirmed the
real one rather than assuming it.** Constraint 6 says "The zip lands in the repo root, which
`.gitignore` already matches". It does not: `scripts/make_review_zip.sh` reported
`REVIEW_PACKAGE_DIR=/home/decodeux/Repos/remedy-history/zips`, a directory OUTSIDE this
repository altogether (`ZIP_IS_INSIDE_REPO = False`). The constraint's PURPOSE is satisfied
either way and I verified it rather than assumed it: `git status --porcelain` was EMPTY
immediately after the build. This is also why PACKAGE ABSOLUTE DIRECTORY above is a real path
and not `NOT ARCHIVED`, and the next round must copy that path into the STATUS line's
`package path` segment per DECISION amend0827 D1.

**4. DECLARED OVERSIZE COMMIT, WITH ITS INSEPARABILITY REASON — C4, 1612 insertions against a
cap of 500.** G8 exempts C4 BY NAME. I name the exemption I am claiming and state honestly
that the two candidate readings differ. (a) THE BLOCK'S: G8 exempts it explicitly as "the
verbatim rewrite of `.agent/**` state files produced by a script". (b) AGENTS.md's DECISION
F104 D1 exemption is narrower — it covers "a commit whose diff is the verbatim rewrite of a
SINGLE `.agent/**` state file" — and C4 touches TWO files, so D1's literal text does not reach
it. The reading that does reach it without strain is AGENTS.md's declared-oversize exception,
and this paragraph is that declaration: the commit is INSEPARABLE because the rotation is one
atomic move of 1612 lines out of the ledger and into the archive, whose two-file path set the
amend0905-throughput amendment fixes by name, and splitting it would leave a committed state in
which records exist in neither file or in both — precisely the corruption the script's
before/after sha256 verification exists to prevent. It is the only oversize commit in this
feature that I am aware of. A reviewer may prefer to record this as a Low finding against
DECISION F104 D1's wording, which never anticipated a two-file script-produced state rewrite.

C5, this commit, is also over the cap — `git diff --stat` reads 563 insertions against 357
deletions for `.agent/handoff.md` alone, measured before staging. G8 excludes C5 from its
per-commit table by construction, and unlike C4 this one falls squarely inside DECISION F104
D1's literal exemption: its diff is the verbatim rewrite of a SINGLE `.agent/**` state file,
`handoff.md`, which D1 names. No declaration is owed for it; it is stated so that a reviewer
seeing 563 does not have to derive the exemption.

**5. OBSERVATION, not a deviation — the `^Done:` line/id gap survives the rotation.** The
ledger carried 254 `^Done:` LINES against 252 distinct ids before C4 and carries 4 against 2
after it: R-0721 and R-0725 each keep a two-paragraph resolution, and the rotation left both in
place because it moves a pair only when the id has EXACTLY one registration and EXACTLY one
`Done:` record. The gap is pre-existing, is unchanged by this round, and is not repaired. It is
recorded because a reader counting LINES gets 58 where the closure reports 60, without either
being wrong about the file.

**6. DECLARED — the evidence directory was KEPT, not deleted.** `.remedy-wt/r30-evidence-
abf14422b1badab6` still exists on disk. Nothing ordered its deletion, it is under the gitignored
`.remedy-wt/` so `git ls-files .remedy-wt` is empty and it never entered the review subject, and
keeping it lets the reviewer re-verify the packaged bundle against its source. It is NOT
committed, per constraint 6 and the F147 attempt-2 lesson.

**7. TOOLING — scratch scripts under `.remedy-wt/`, deleted by exact path.** This session's
bash guard rejects heredocs, brace quantifiers, loops, `$( )` and multi-operation compounds by
shape, so every multi-step measurement was written to a file under the gitignored `.remedy-wt/`
and run with `python3 -B`. The NINETEEN files were `.remedy-wt/r30_pre.py`,
`.remedy-wt/r30_c0a.py`, `.remedy-wt/r30_c0b.py`, `.remedy-wt/r30_g1.py`,
`.remedy-wt/r30_c1.py`, `.remedy-wt/r30_c2.py`, `.remedy-wt/r30_c3.py`,
`.remedy-wt/r30_g4_pre.py`, `.remedy-wt/r30_g4_post.py`, `.remedy-wt/r30_g5_base.py`,
`.remedy-wt/r30_g5_run.py`, `.remedy-wt/r30_g5_scan.py`, `.remedy-wt/r30_g5_produce.py`,
`.remedy-wt/r30_g6_verify.py`, `.remedy-wt/r30_g6_verify2.py`, `.remedy-wt/r30_g6_verify3.py`,
`.remedy-wt/r30_g7_integrity.py`, `.remedy-wt/r30_g7_extra.py` and `.remedy-wt/r30_g8.py`, and
each was deleted BY ITS EXACT PATH after the gates were taken, never by a glob. Two JSON
scratch files,
`.remedy-wt/r30_verification_run.json` and `.remedy-wt/r30_evidence_meta.json`, were deleted the
same way. `.remedy-wt/f272-r30-block.md` was NOT deleted: it is G1's first link. The evidence
directory was not deleted either, per deviation 6.

**8. TOOLING — the built `remedy` binary is denied in this session.** Closure precondition 3
asks for `remedy integrity check --json`; I called
`packages.orchestration.integrity_gate.run_integrity_checks()` directly in Python instead and
read `.passed` and `.fail_count` as attributes. No CLI invocation of `remedy` was attempted,
and `python3 -m apps.cli.grouped` was not needed by any gate this round.

**9. NOT DONE, deliberately, per constraint 8.** This round minted NO finding id and resolved
none: no `- R-XXXX` line, no `Done:` paragraph, no `Landed:` line. `R-0829` is still the next
free id and is still free — `^- R-0829 ` reads 0 before and 0 after. The open set reads the
SAME before and after the rotation, 60 by distinct id.

**10. NOT DONE, deliberately, per the Change set.** Nothing under `packages/`, `apps/`,
`tests/`, `scripts/` or `docs/` changed. `docs/roadmap/STATUS.md`, `README.md` and
`scripts/self_use_queue.json` are named nowhere in this round's diff; all three belong to the
NEXT round's closure commit. No production line moved, so no red-proof was ordered or possible,
and no ruff reading is owed. No measurement forced a path outside the declared change set.

## Next

THE CLOSURE COMMIT, and it is the last one on this branch. The reviewer reviews
`c286fd92`..HEAD, rules on this round, and authors the STATUS `[x]` line from the seven values
in the CLOSURE VALUES section at the top of this file — evidence job `abf14422b1badab6`,
package `remedy-review-20260907-173909-READY_FOR_REVIEW.zip`, SHA-256
`8bbce2fa27ddd6c68398d381d1367e6e509b49cbacac0a29ff06329d9aebb706`, package path
`/home/decodeux/Repos/remedy-history/zips`, accepted HEAD
`7f71b30ac3b2f1fefb2da6063f0453d650d3835a`, live review PASS_WITH_RISKS, open findings 60 by
distinct id. That STATUS line, the README capability sync and SU-012's `consumed_by` set to
`F272` land in ONE commit, per R-0154 and the closure protocol's step 5, and the closure
paragraph names all five open High findings — R-0803, R-0804, R-0806, R-0807 and R-0827 — with
F273 as their owner, and states that `high_blockers_open` reports "no open blocker/high
findings" while those five are open. Then the pull request. The PR is NOT merged this session;
it merges at the next feature's start via the Open PR Gate.
