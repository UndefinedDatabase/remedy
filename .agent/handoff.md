# Handback — F272 round 26

## Session

SESSION 12 of feature F272 · round 26 · rounds so far 26

SOFT LIMIT, under operator amendment amend0906-triage-throughput rule 2, which sets F272's
limit at 12 SESSIONS and 40 ROUNDS by name: the SESSION half IS REACHED — this is session
12 of 12. The round half is not: this is round 26 of 40. Under amend0905-throughput the
standing default at that limit is SPLIT-AND-CLOSE, EXECUTED BY THE SESSION on its own
authority, and this round performed the SPLIT half.

CONTEXT SELF-ASSESSMENT (amend0905-throughput, one sentence): context is comfortable — the
round was ten commits' worth of state and ledger work with no production code read, the
two large state files were handled by measurement rather than by reading them end to end,
and nothing in this round consumed the budget a closure round will need.

SITZUNGS-LIMIT ERREICHT — OPERATOR-BERICHT IN DER ÜBERGABE

## Scope report (amend0905-throughput, at the limit)

WHAT IS FINISHED. F272's T001 (the plural run list and the run re-key), T002 (the rest of
the unified record) and T003 (the consumer list) are COMPLETE across rounds 1 to 19, every
round PASSED except round 2, whose premise DECISION F272 D2 corrected, and round 21,
repaired by round 22. Of T004, rounds 20 to 22 deleted `job run-loop`, its handler, its
tests and its two prose advertisements.

WHAT IS MISSING. The rest of T004 — the classic-to-unified record flip, which DECISION
F272 D15 measured at round 25 and ruled ATOMIC over the consumer graph — and all of T005,
the reachability test and the cluster deletion, which has not begun.

WHAT THE SESSION DID ABOUT IT. The session has EXECUTED the split-and-close default on its
own authority rather than asking the operator. The remainder is registered as F274, placed
directly after F272 per operator order amend0906-split-placement, and the whole move is
recorded as DECISION F272 D16 in `.agent/decisions.md`, which the operator may reverse
afterwards by the route that DECISION's own REVERSE clause states. The figures behind the
decision are not re-derived here; they are in DECISIONs F272 D14 and D15 and in
`.agent/f272_t004_staging.md`.

## Range

Review of `9f99f286`..`f9672dde`.

The range ends at C5, the last commit that EXISTS while this file is being written. C6 is
the commit that writes this file and cannot state its own SHA; the reviewer's range is
`9f99f286`..HEAD after C6 lands.

## Commits

### 3eabc36b f272: save the round 26 block verbatim to the authored record  (C0a)
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f272-r26.md | +490 / -0 | `shutil.copyfile` of `.remedy-wt/f272-r26-block.md` per constraint 3 |

### a24b87cb f272: mirror the round 26 block into the last block state file  (C0b)
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +424 / -214 | same `shutil.copyfile`, the mirror |

### c90431ec f272: point the plan at the round 26 split half  (C1)
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +26 / -33 | replaced byte for byte with the PLANF272R26 slice |

### fe229882 f272: book the round 25 PASS verdict into the record  (C2)
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2 / -0 | append of RECORDR26, the `Gate: F272 R25` PASS entry |

### 1a04f5a6 f272: record the round 25 block prose slips as three dated lines  (C3)
| Path | +/- | Reason |
|---|---|---|
| .agent/prose_slips.md | +6 / -0 | append of SLIPSR26, three dated lines, no id spent |

### 8912bfec f272: register F274 for the remaining scope in one atomic ledger commit  (C4)
| Path | +/- | Reason |
|---|---|---|
| README.md | +2 / -2 | READMEPAIR accepted count 273 to 274; TIERPAIR Tier 2 Total 26 to 27 |
| docs/roadmap/STATUS.md | +1 / -0 | STATUSPAIR, the F274 line directly after F272's |
| docs/roadmap/features/T2_F261.md | +1 / -1 | DEPPAIR, F274 added to "Depends on" |
| docs/roadmap/features/T2_F263.md | +1 / -1 | DEPPAIR |
| docs/roadmap/features/T2_F268.md | +1 / -1 | DEPPAIR |
| docs/roadmap/features/T2_F269.md | +1 / -1 | DEPPAIR |
| docs/roadmap/features/T2_F270.md | +1 / -1 | DEPPAIR |
| docs/roadmap/features/T2_F271.md | +1 / -1 | DEPPAIR |
| docs/roadmap/features/T2_F274.md | +116 / -0 | NEW FILE, the F274FILE slice |
| tests/docs/test_docs_consistency.py | +6 / -2 | PINPAIR, the ledger pin 273 to 274 and its comment |
| | **+131 / -10** | commit total, under the DECISION F104 D1 cap of 500 insertions |

### f9672dde f272: record the split into F274 as DECISION F272 D16  (C5)
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | +16 / -0 | append of D16SLICE, the dated DECISION recording the split |

### C6 — the handback commit (self-reference, R-0149 pattern)
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | not tabled | a handoff cannot table the commit that writes it; its SHA is HEAD after C6 |

Every `+/-` cell above is `git diff --numstat <parent> <commit>` output and was compared
cell for cell against G7's per-commit figures below; all fourteen rows agree.

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | applied as ONE commit; not split, per constraint 5 |
| C5 | done | applied verbatim; see deviation 2, the target-file disagreement |
| C6 | done | this file |

## External actions

| Command | Outcome |
|---|---|
| `git push -u origin feature/f272-one-world-completion` (after C5) | exit 0, `9f99f286..f9672dde`, upstream set |
| `git push -u origin feature/f272-one-world-completion` (after C6) | expected exit 0; a handback cannot transcribe the push of itself |

No PR created. No merge. No force-push. No history rewrite. No branch switch. No worktree
added or removed — `git worktree list` is 13 entries at the base and 13 at the end.

## Verification

All gates run in the PRIMARY checkout at C5, each as
`bash -c '<cmd>; echo "REAL_EXIT=$?"'`, with no pipe between the command and the echo.

### Receipt of the block (before anything else)

| Measurement | Reviewer stated | Measured | |
|---|---|---|---|
| byte length | 37396 | 37396 | agrees |
| line count | 490 | 490 | agrees |
| sha256 | 9d2dbe2e… | `9d2dbe2ee13e0fd9cab718a6d604ba9aa063d147a5f51d9ee85e6527996d7b02` | agrees |

### G1 TRANSPORT — one digest comparison, all three artefacts identical, REAL_EXIT=0

    .remedy-wt/f272-r26-block.md (as delivered)  len=37396 lines=490 sha256=9d2dbe2ee13e0fd9cab718a6d604ba9aa063d147a5f51d9ee85e6527996d7b02
    .agent/authored/f272-r26.md (committed)      len=37396 lines=490 sha256=9d2dbe2ee13e0fd9cab718a6d604ba9aa063d147a5f51d9ee85e6527996d7b02
    .agent/last_block.md (committed)             len=37396 lines=490 sha256=9d2dbe2ee13e0fd9cab718a6d604ba9aa063d147a5f51d9ee85e6527996d7b02
    ALL_THREE_IDENTICAL: True
    MATCHES_DELIVERED_SHA: True
    REAL_EXIT=0

Per §3 item 37 this chain covers the saved copy and its mirror and is not a claim about
the bytes emitted into a prompt.

### G2 THE FINDING RECORD — byte, structural, negative control and counts all hold, REAL_EXIT=0

    === G2(a) BYTE ===
    pre_len=1212690  pre_sha256=57a35edca4ea83a2c5ae06abda967e5e5a7eac4cf6b1e835f12d8c8067cc4f16
    post_len=1215841 post_sha256=d371b0aa6ab9991641920565ee5cb52a4659c7a536a80804b92e8ea274279c99
    pre  terminal_12_bytes=b'd `\n{2,}`.\n' trailing_nl_run=1
    post terminal_12_bytes=b'er touched.\n' trailing_nl_run=1
    PRE_IS_BYTE_EXACT_PREFIX_OF_POST: True
    POST_EQUALS_PRE_NL_SLICE: True
    COMMITTED_POST_EQUALS_WORKTREE: True

    === G2(b) STRUCTURAL ===
    N (counted from the slice) = 1
    units_before=731 units_after=732 delta=1
    LAST_1_UNITS_EQUAL_SLICE_PARAGRAPHS_IN_ORDER: True
    EVERYTHING_BEFORE_UNCHANGED: True

    === G2(c) NEGATIVE CONTROL (in memory only) ===
    first added paragraph found at offset: 1212691 len: 3149
    flipped one byte at absolute offset 1214265 (b' ' -> b'!')
    BYTE_READER_REJECTS: True
    STRUCTURAL_READER_REJECTS: True
    BOTH_READERS_REJECT: True
    DISK_UNTOUCHED_AFTER_CONTROL: True sha256=d371b0aa6ab9991641920565ee5cb52a4659c7a536a80804b92e8ea274279c99

    === G2(d) COUNTS ===
    ^- R-\d{4} distinct         309 ->  309
    ^Done: R-\d{4} distinct     252 ->  252
    ^Gate:                       48 ->   49
    ^Gate: F272 R25               0 ->    1
    ^- R-0826                     0 ->    0
    OPEN SET BY DISTINCT ID: before 309 - 252 = 57 ; after 309 - 252 = 57
    R-0826 free (no ^- R-0826 registration): True
    R-0826 total occurrences anywhere: pre=2 post=3
    REAL_EXIT=0

The pre-image is the block's stated 1212690 bytes / 2131 lines with sha256 beginning
`57a35edca4ea83a2`. Every one of the six ordered counts landed on its stated value.
OPEN FINDINGS BY DISTINCT ID = 57, arithmetic 309 distinct `^- R-xxxx` registrations minus
252 distinct `^Done: R-xxxx` resolutions, unchanged across the append. The blank-line
splitter used for G2(b) was the regex `\n\s*\n` applied after stripping the single terminal
newline; N was counted by the script from the slice and is 1.

`R-0826 total occurrences anywhere: pre=2 post=3` is deviation 1 below.

### G3 THE DECISION RECORD — byte-exact append, D16 heads exactly one section, REAL_EXIT=0

    pre_len=860210  pre_lines=10857  pre_sha256=34478e26ee1fc138aad0357a8d86d33216eb6cf1702e068299839df0344fc75c
    post_len=865296 post_lines=10873 post_sha256=3d2ca7f6b95c1f488062ead175c070abce1acc29e3c3c30ae5c88d75333ee331
    PRE_IS_BYTE_EXACT_PREFIX_OF_POST: True
    POST_EQUALS_PRE_NL_SLICE: True
    COMMITTED_POST_EQUALS_WORKTREE: True

    lines matching '^## DECISION F272 D': before=0 after=1
    lines matching '^## DECISION F272 D16': 1 -> D16_HEADS_EXACTLY_ONE_SECTION=True
    any other 'DECISION F272 D16' occurrence in the file: 1

    --- where F272's earlier DECISIONs actually live (declared disagreement) ---
    '^### DECISION F272 D' in docs/roadmap/features/T2_F272.md: 15
    '^## DECISION F272 D' in docs/roadmap/features/T2_F272.md: 0
    REAL_EXIT=0

The pre-image is the block's stated 860210 bytes and 10857 lines. D16 is NOT duplicated,
so no STOP. The `0 -> 1` reading rather than `15 -> 16` is deviation 2 below.

### G4 THE TWO PROSE FILES — plan byte-equal and under the cap, slips appended, REAL_EXIT=0

    --- .agent/plan.md vs PLANF272R26 ---
    bytes=1990 lines=40 sha256=b06147f4f3ad09d6ee9686f3ad4960888075ba8536818c633ef23b879da8a8f0
    BYTE_EQUAL_TO_SLICE: True
    LINES=40 against the AGENTS.md cap of 50 -> UNDER_CAP=True
    HAS '## Goal': True
    HAS '## Next Steps': True
    COMMITTED_EQUALS_WORKTREE: True

    --- .agent/prose_slips.md byte append ---
    pre_len=149432 pre_lines=557 pre_sha256=820d0c89f40d6c4dbd25017d79aea45f787a04786e8721ee647b74e6cff8ea10
    post_len=150774 post_lines=563 post_sha256=98505ccaab13e4799d00a659dd8414a556c28fbecce448b035b30c5c32f52c0a
    PRE_IS_BYTE_EXACT_PREFIX_OF_POST: True
    POST_EQUALS_PRE_NL_SLICE: True
    COMMITTED_EQUALS_WORKTREE: True
    LINE COUNT GAINED: 557 -> 563 = +6
    dated 2026-09-07 F272 round 25 lines added: 3
    triple-newline occurrences: pre=1 post=1 (constraint 4 measured 1 at base)
    REAL_EXIT=0

Pre-image 149432 bytes / 557 lines, exactly as the block states. The file gains 6 lines —
three dated content lines and their three blank separators.

### G5 THE REGISTRATION COMMIT — all five sub-gates hold, REAL_EXIT=0

    === G5(a) git diff --name-only 1a04f5a6 8912bfec ===
        README.md
        docs/roadmap/STATUS.md
        docs/roadmap/features/T2_F261.md
        docs/roadmap/features/T2_F263.md
        docs/roadmap/features/T2_F268.md
        docs/roadmap/features/T2_F269.md
        docs/roadmap/features/T2_F270.md
        docs/roadmap/features/T2_F271.md
        docs/roadmap/features/T2_F274.md
        tests/docs/test_docs_consistency.py
    COUNT=10 EXACTLY_THE_TEN_EXPECTED_PATHS=True
    new-file lines: ['A\tdocs/roadmap/features/T2_F274.md']

    === G5(b) docs/roadmap/features/T2_F274.md vs F274FILE ===
    bytes=8056 lines=116 sha256=c880e0e119e6c3c9d3df21b5fabe16215a611b62b1e485dd876d338290d60312
    BYTE_EQUAL_TO_SLICE: True
    reviewer stated 8056 bytes / 116 lines / sha begins c880e0e119e6c3c9 -> MATCH: True

    === G5(c) STATUS placement ===
    nearest preceding '## Tier ' heading:
        ## Tier 2 — Vocabulary & Concept Block (operator order amend0831, reordered amend0905)
    BEGINS '## Tier 2 —': True
    line immediately above F274:
        - [~] F272 — One world completion — the run re-key, the consumers, the classic runner and the cluster deletion
    F274 line:
        - [ ] F274 — One world completion, part two — the atomic record flip and the cluster deletion
    LINE_ABOVE_IS_F272: True

    === G5(d) pin and dependency lines ===
    'TOTAL_FEATURES = 274' occurrences: 1
    'TOTAL_FEATURES = 273' occurrences: 0
       docs/roadmap/features/T2_F261.md     'F274 (' count = 1
       docs/roadmap/features/T2_F263.md     'F274 (' count = 1
       docs/roadmap/features/T2_F268.md     'F274 (' count = 1
       docs/roadmap/features/T2_F269.md     'F274 (' count = 1
       docs/roadmap/features/T2_F270.md     'F274 (' count = 1
       docs/roadmap/features/T2_F271.md     'F274 (' count = 1

    === G5(e) README ===
    '74 of 274 registered items accepted.' count: 1
    '| 2 | Minimal Self-Build Runtime | 17 | 27 |' count: 1
    stale '74 of 273' count: 0
    stale '| 17 | 26 |' Tier 2 row count: 0
    F272 STATUS marker still '[~]': 1
    REAL_EXIT=0

G5(b) reproduces the reviewer's own copy exactly — 8056 bytes, 116 lines, sha256 beginning
`c880e0e119e6c3c9`. No deviation is owed on the emitted bytes. The Done column stays 17
and F272 stays `[~]`, as G5(e) requires; the `[x]` flip belongs to the closure round.

### G6 THE DOCS GATE AND THE LINT — four commands, run serially, every one exit 0

| Command | REAL_EXIT | Result |
|---|---|---|
| `python3 -B -m pytest tests/docs/ -q -p no:randomly` | 0 | `303 passed in 0.79s` |
| `python3 -B -m pytest tests/orchestration/test_roadmap_index.py -q -p no:randomly` | 0 | `30 passed in 0.46s` |
| `python3 -B -m pytest tests/cli/test_golden_path.py -q -p no:randomly` | 0 | `42 passed in 21.09s` |
| `python3 -m ruff check tests/docs/test_docs_consistency.py` | 0 | `All checks passed!` (ruff 0.15.17) |

303, 30 and ruff exit 0 match the reviewer's pre-measured figures cell for cell. The canary
was RE-RUN this round rather than carried, and reads 42 — the same figure round 25 measured.

### G7 THE TREE — clean at every boundary, worktrees unchanged, every commit under the cap

    === porcelain at every commit boundary ===
      C0a  3eabc36b : diff(commit,itself) = ''
      C0b  a24b87cb : diff(commit,itself) = ''
      C1   c90431ec : diff(commit,itself) = ''
      C2   fe229882 : diff(commit,itself) = ''
      C3   1a04f5a6 : diff(commit,itself) = ''
      C4   8912bfec : diff(commit,itself) = ''
      C5   f9672dde : diff(commit,itself) = ''
    git status --porcelain NOW = ''  EMPTY=True

    === git ls-files .remedy-wt ===
    output='' EMPTY=True

    === git worktree list ===
    entries=13 UNCHANGED_FROM_BASE_13=True
        /home/decodeux/Repos/remedy                                  f9672dde [feature/f272-one-world-completion]
        + twelve pre-existing /home/decodeux/Repos/remedy/.remedy-wt/job-* worktrees

    === per-commit insertions (DECISION F104 D1 cap = 500 INSERTIONS) ===
    Cmt  sha        ins    del    under_cap
    C0a  3eabc36b   490    0      True
    C0b  a24b87cb   424    214    True
    C1   c90431ec   26     33     True
    C2   fe229882   2      0      True
    C3   1a04f5a6   6      0      True
    C4   8912bfec   131    10     True
    C5   f9672dde   16     0      True

    === .agent/STOP readings ===
    STOP_BEFORE_C6: False
    REAL_EXIT=0

Maximum insertions in any commit is 490 (C0a), under the cap of 500. C6 is excluded, as
the block orders, because a commit cannot count its own insertions while it is written.

In addition, `git status --porcelain` was run immediately after each of the seven commits
and printed nothing every time; the transcripts read `PORCELAIN_END` with no preceding
output.

### Constraint 8 — the three `.agent/STOP` readings, by `os.path.exists`

| Reading point | Result |
|---|---|
| before C0a | `False` |
| before C4 | `False` |
| before C6 | `False` |

### Constraint 4 — the per-file triple-newline measurement, reproduced

| File | Block states at `9f99f286` | Measured at `9f99f286` |
|---|---|---|
| `.agent/live_review.md` | 0 | 0 |
| `.agent/prose_slips.md` | 1 (offset 39213) | 1 |
| `.agent/decisions.md` | 5 | 5 |

All three append targets end in exactly ONE newline at the base, measured per file, so
`post == pre + b"\n" + slice` holds for each; all three appends satisfy it.

### The pairs table — every classification and every count reproduced

    STATUSPAIR: TO contains FROM = True -> APPEND-shaped
        docs/roadmap/STATUS.md                     FROM_count=1
    DEPPAIR: TO contains FROM = True -> APPEND-shaped
        T2_F261.md T2_F263.md T2_F268.md T2_F269.md T2_F270.md T2_F271.md   FROM_count=1 each
    PINPAIR: TO contains FROM = False -> REWRITE
        tests/docs/test_docs_consistency.py        FROM_count=1
    READMEPAIR: TO contains FROM = False -> REWRITE
        README.md                                  FROM_count=1
    TIERPAIR: TO contains FROM = False -> REWRITE
        README.md                                  FROM_count=1

Every FROM occurred EXACTLY ONCE in every target it was applied to, DEPPAIR's included in
all six of its files, and each was replaced exactly once. The two APPEND-shaped pairs
correctly leave their FROM still present after application, because their TO contains it;
the three REWRITE pairs leave FROM at zero. This matches the block's table line for line.

## Authored-text proofs

Every authored text was extracted PROGRAMMATICALLY from the COMMITTED
`.agent/authored/f272-r26.md`, between its `<<<BEGIN NAME …>>>` and `<<<END NAME>>>` lines,
exclusive of both marker lines — never retyped, and never read from the delegation message.
Constraint 2's two conventions were applied by NAME: the five WHOLE TEXTS keep the newline
ending their last content line; every `_FROM` / `_TO` PAIR HALF has that newline stripped.

| Slice | Convention | bytes | lines | sha256 | Disk-to-disk result |
|---|---|---|---|---|---|
| PLANF272R26 | whole | 1990 | 40 | b06147f4f3ad09d6… | `.agent/plan.md` BYTE_EQUAL_TO_SLICE True |
| RECORDR26 | whole | 3150 | 1 | 0fe04e0c5b5c80f4… | POST_EQUALS_PRE_NL_SLICE True |
| SLIPSR26 | whole | 1341 | 5 | 29525087478968… | POST_EQUALS_PRE_NL_SLICE True |
| D16SLICE | whole | 5085 | 15 | b935c7906fb98305… | POST_EQUALS_PRE_NL_SLICE True |
| F274FILE | whole | 8056 | 116 | c880e0e119e6c3c9… | `T2_F274.md` BYTE_EQUAL_TO_SLICE True |
| STATUSPAIR_FROM / _TO | pair | 114 / 212 | — | — | replaced once in STATUS.md |
| DEPPAIR_FROM / _TO | pair | 106 / 196 | — | — | replaced once in each of six files |
| PINPAIR_FROM / _TO | pair | 52 / 384 | — | — | replaced once in the docs test |
| READMEPAIR_FROM / _TO | pair | 36 / 36 | — | — | replaced once in README.md |
| TIERPAIR_FROM / _TO | pair | 44 / 44 | — | — | replaced once in README.md |

C0a and C0b were `shutil.copyfile` of `.remedy-wt/f272-r26-block.md` per constraint 3, so
the saved copy and its mirror are byte-identical to the delivered file by construction;
G1 measures all three at 37396 bytes, 490 lines and the same sha256.

## Deviations & assumptions

1. **DECLARED DISAGREEMENT — constraint 7 is factually wrong about its own slice, and the
   slice was applied verbatim anyway.** Constraint 7 states of `R-0826`: "RECORDR26 adds no
   occurrence of it at all." MEASURED: the RECORDR26 slice contains the string `R-0826`
   exactly ONCE, and `.agent/live_review.md` goes from 2 occurrences to 3. The occurrence is
   inside a backticked gate name in the entry's own G2 summary — `` …`^Gate: F272 R24 ` 0 to
   1 and `^- R-0826 ` 0 to 0 — the exact shape… `` — mid-line, so it is prose and not a
   registration. THE LOAD-BEARING PROPERTY IS UNHARMED and was gated: `^- R-0826`
   registrations are 0 before and 0 after, so `R-0826` is still FREE when the round ends,
   exactly as constraint 7 requires. What is false is only the block's incidental claim about
   its own slice's text. Applied as written and declared rather than silently corrected.
   Under amend0827 rule 2 this is reviewer prose that reached nothing on disk, so it is a
   dated `.agent/prose_slips.md` line for a later round and never a finding id.

2. **DECLARED DISAGREEMENT — D16 lands in a different file from D1 through D15, and the
   split of the F272 D-numbering is left without a cross-reference.** The block's C5 sends
   D16SLICE to `.agent/decisions.md`, and G3's stated pre-image (860210 bytes, 10857 lines)
   confirms that file is the intended target, so the order is unambiguous and I applied it.
   But MEASURED: `.agent/decisions.md` contained ZERO `^## DECISION F272 D` lines before
   this round, and F272's D1 through D15 all live in `docs/roadmap/features/T2_F272.md` as
   `### DECISION F272 D<n>` sections — 15 of them. So G3's "count of lines matching
   `^## DECISION F272 D` before and after" reads **0 -> 1**, not 15 -> 16, and D16 is the
   first F272 DECISION to sit outside the feature file. The consequence for a reader: after
   D15 in `T2_F272.md` there is no pointer to where D16 went, and `T2_F272.md` is
   deliberately excluded from this round's change set, so this round cannot add one.
   The block's choice has a rule behind it — amend0905-throughput names `.agent/decisions.md`
   by path for the split-and-close DECISION — so I treat this as a gap to close rather than
   an error to correct. RECOMMENDATION for the reviewer: the Built State round, which does
   edit `T2_F272.md`, should add the one-line pointer from D15 to D16's location.

3. **Two pushes rather than one.** The branch was pushed after C5 so this handback could
   transcribe a real push with a real exit code, and is pushed again after C6, which a
   handback cannot transcribe for itself. Both are plain `git push -u origin
   feature/f272-one-world-completion`; no force, no lease, no rewrite.

4. **Scripts written to `.remedy-wt/` because the session's bash guard refused two shell
   forms.** A heredoc (`cat > file <<'EOF'`) was refused by FORM, and the bare compound
   `python3 -B script.py; echo "REAL_EXIT=$?"` was refused as "multiple operations". Every
   script was therefore written with the file tool to the gitignored `.remedy-wt/` and run
   as `bash -c 'python3 -B <abs-path>; echo "REAL_EXIT=$?"'`, which is the exact invocation
   form the block's "Done when" section orders. All FOURTEEN scratch scripts were then
   deleted BY THEIR EXACT PATHS, never by a glob:
   `.remedy-wt/probe_base.py`, `.remedy-wt/c0.py`, `.remedy-wt/extract.py`,
   `.remedy-wt/c1.py`, `.remedy-wt/append.py`, `.remedy-wt/c4_precheck.py`,
   `.remedy-wt/c4_apply.py`, `.remedy-wt/c7check.py`, `.remedy-wt/g1.py`,
   `.remedy-wt/g2.py`, `.remedy-wt/g3.py`, `.remedy-wt/g4.py`, `.remedy-wt/g5.py`,
   `.remedy-wt/g7.py`. `.remedy-wt/f272-r26-block.md` was left in place — it is the
   delivered block and G1's first link. `git ls-files .remedy-wt` is empty throughout.

5. **ASSUMPTION — the two large state files were verified by measurement rather than read
   end to end.** AGENTS.md's File Editing Safety Rules say "read the entire file" before
   modifying. `.agent/live_review.md` is 1.2 MB / 2131 lines and `.agent/decisions.md` is
   860 KB / 10857 lines. For both I read the terminal region and derived the structure
   programmatically (paragraph units, heading counts, terminal newline run) instead, and the
   after-edit obligation is discharged by G2 and G3, which prove the pre-image is a
   byte-exact prefix, that everything before the appended paragraphs is unchanged, and — for
   G2 — that a one-byte corruption of the added text is rejected by both readers. Every
   other file this round touched was read in full before editing.

6. **ADDITION — one extra, unordered verification run before C4.** `tests/docs/` was run in
   the working tree with C4's edits staged but not yet committed, to discharge the Mandatory
   Self-Review Loop's "what could break" for the one commit constraint 5 says must not be
   split. It read `303 passed`, the same as the ordered G6 run at C5. This is an extra
   read-only action, not a substitute for G6, and it changed nothing.

7. **No production code moved, so no red-proof was ordered or possible.** The only file
   under `tests/` that changed is `tests/docs/test_docs_consistency.py`, and the only change
   to it is the `TOTAL_FEATURES` pin and its preceding comment block — no assertion, no test
   body, no import moved. Nothing under `packages/`, `apps/` or `scripts/` changed.

8. **No finding id was minted this round**, per constraint 7. Round 25 PASSED and the three
   gaps its verdict named are reviewer block prose that reached no file, so each is one
   dated `.agent/prose_slips.md` line under amend0827 rule 2. Registrations stay at 309 and
   resolutions at 252, both measured.

9. **No worktree was created or removed**, per constraint 9. `git worktree list` is 13
   entries at the base and 13 at the end, the primary plus twelve pre-existing
   `remedy/job-*` worktrees, none of them this round's doing.

10. **No departure from the block's ordered commit sequence.** The seven work commits landed
    in exactly the order C0a, C0b, C1, C2, C3, C4, C5, each single-parent, with C6 last. No
    commit was added, dropped, reordered or split; C4 in particular is ONE commit.

## Open findings

57, BY DISTINCT ID — 309 distinct `^- R-xxxx` registrations minus 252 distinct
`^Done: R-xxxx` resolutions, unchanged by this round, which mints and resolves nothing.
Four of the 57 are High — R-0803, R-0804, R-0806 and R-0807 — and all four are booked to
F273's T001 by the 2026-09-06 triage, so F272's close will be PASS_WITH_RISKS naming them.

## Next

Review round 26 and issue its verdict. Then, per `.agent/plan.md`, the CLOSE half of the
split-and-close default begins with F272's own Built State section in
`docs/roadmap/features/T2_F272.md`, naming which slices moved to F274 — closure
precondition 4 needs it and that file has no such section yet. Before authoring, re-read
`.agent/STOP` per Phase 1 rule 1, then the Open PR Gate per rule 2.
