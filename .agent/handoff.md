# Handback — F272 round 25 — SESSION 11 CLOSES

## Session

SESSION 11 of feature F272 · round 25 · rounds so far 25

Soft limit under amend0906-triage-throughput: 12 SESSIONS and 40 ROUNDS. At
session 11 and round 25 the feature is still INSIDE the limit, so no scope
report is owed by THIS round; session 12 reaches the session half of it and
owes one. See the session-closing section below, which the block ordered.

Context self-assessment, one sentence: this session spent its whole
measurement budget on a single question and answered it — whether T004's
remaining work can be staged by caller — so it closes with three rounds
rather than the six-to-eight target, with the answer on disk rather than in
a session that is about to be discarded.

## Range

Review of `4491ec9e`..`e72a9602`, PLUS the C5 commit that writes this file.
C5's SHA is deliberately absent: a commit cannot name its own SHA, and no SHA
is written in this repository that has not been measured. The reviewer reads
the true range as `4491ec9e`..`HEAD` after C5 lands; every figure below was
measured at or before `e72a9602`.

## Commits

### 17d7e06c f272: save the round 25 step block verbatim
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f272-r25.md` | +280 / -0 | C0a — `shutil.copyfile` of the delivered block, byte-identical (G1) |

### 1bfce0ee f272: mirror the round 25 block into the last block slot
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/last_block.md` | +167 / -172 | C0b — same `copyfile`, same bytes as C0a and as the delivered file (G1) |

### 9448a35d f272: point the plan at the atomic record flip and the session 12 scope report
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/plan.md` | +23 / -23 | C1 — replaced byte for byte with slice PLANF272R25; 47 lines, under the AGENTS.md cap of 50 (G3) |

### 1d8741b6 f272: book the round 24 PASS verdict into the record
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/live_review.md` | +2 / -0 | C2 — append of RECORDR25, the round 24 PASS gate entry owed by amend0827 rule 1. No finding minted (G2) |

### 869b6a43 f272: record the round 24 block prose slip on the append separator
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/prose_slips.md` | +2 / -0 | C3 — append of SLIPSR25, one dated line, no id spent (G3) |

### e72a9602 f272: correct D14 part 2 with DECISION F272 D15, the atomic record flip
| Path | +/- | Reason |
|------|-----|--------|
| `docs/roadmap/features/T2_F272.md` | +14 / -0 | C4 — append of D15SLICE. D14's own section byte-unchanged (G4) |

### C5 — SHA unmeasurable at write time — f272: close session 11 with the round 25 handback
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/handoff.md` | rewritten in full | C5 — this file. A handoff cannot table the commit that writes it (R-0149 pattern), and it cannot count its own insertions, which is why G6 covers C0a through C4 only |

Every `+/-` cell above was taken from `git diff --numstat <parent> <commit>`
and compared CELL FOR CELL against G6's independently-run figures; all six
agree. The change set is exactly the seven paths the block declared and
nothing else. NOTHING under `packages/`, `apps/`, `tests/` or `scripts/`
changed this round.

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C0a  | done   | |
| C0b  | done   | |
| C1   | done   | |
| C2   | done   | |
| C3   | done   | |
| C4   | done   | |
| C5   | done   | this commit |

## External actions

    git push -u origin feature/f272-one-world-completion
    -> To github.com:UndefinedDatabase/remedy.git
       4491ec9e..e72a9602  feature/f272-one-world-completion -> feature/f272-one-world-completion
       Branch 'feature/f272-one-world-completion' set up to track remote branch ...
       REAL_EXIT=0

    gh pr list --state open --json number,headRefName,baseRefName,isDraft
    -> []   REAL_EXIT=0     (no PR exists for this branch; none was created)

A SECOND push follows C5, because a handback cannot transcribe the push of
itself. Its output is in the round report. No PR was created, nothing was
merged, no worktree was added or removed (constraint 8 forbade one), and no
history was rewritten or force-pushed.

## Verification

Every gate was run with `bash -c '<cmd>; echo "REAL_EXIT=$?"'`, no pipe
between the command and the echo, in the PRIMARY checkout. All six PASS.

**G1 TRANSPORT — PASS, REAL_EXIT=0.** Five blobs, one digest.

    delivered .remedy-wt/f272-r25-block.md      len 23414  lines 280  sha256 b9dda40e...3ea9ee92
    worktree  .agent/authored/f272-r25.md       len 23414  lines 280  sha256 b9dda40e...3ea9ee92
    worktree  .agent/last_block.md              len 23414  lines 280  sha256 b9dda40e...3ea9ee92
    COMMITTED HEAD:.agent/authored/f272-r25.md  len 23414  lines 280  sha256 b9dda40e...3ea9ee92
    COMMITTED HEAD:.agent/last_block.md         len 23414  lines 280  sha256 b9dda40e...3ea9ee92
    ALL_FIVE_IDENTICAL True
    DELIVERED_MATCHES_DELEGATED_DIGEST True

Full digest: `b9dda40e327c491305014c62b16058997f6c475298407004fa0aca3a3ea9ee92`.
The delegating message stated that digest, 23414 bytes and 280 lines BEFORE
the block was opened, and all three were verified against disk before any
work began. Per §3 item 37 this chain covers these artefacts and is not a
claim about the bytes emitted into a prompt.

**G2 THE RECORD — PASS, REAL_EXIT=0.** The single append at C2.

(a) BYTE

    pre_len 1209111   pre_lines 2129
    pre_sha256 8ca58e083752f4163c14f05320ec4b352cd767165333760e2033156560ea75f1
    pre_terminal_12  b'for all 17.\n'    pre_trailing_newline_run 1
    slice_len 3578    slice_lines 1
    slice_sha256 d98e1cdd71952bc110b1356cec301085ce6e547d0e5555d947c95094842b2ef0
    slice_terminal_12 b'd `\n{2,}`.\n'
    post_len 1212690  post_lines 2131
    post_sha256 57a35edca4ea83a2c5ae06abda967e5e5a7eac4cf6b1e835f12d8c8067cc4f16
    post_terminal_12 b'd `\n{2,}`.\n'    post_trailing_newline_run 1
    PRE_IS_BYTE_EXACT_PREFIX_OF_POST True
    POST_EQUALS_PRE_NL_SLICE          True

The pre-image is 1209111 bytes at 2129 lines and its sha256 begins
`8ca58e083752f416`, exactly as the block predicted.

(b) STRUCTURAL — terminal newline stripped, split on blank lines.

    N (COUNTED BY THE SCRIPT from the slice, not read from the block)  1
    units_before 730   units_after 731
    LAST_N_UNITS_EQUAL_SLICE_PARAGRAPHS_IN_ORDER True
    EVERYTHING_BEFORE_UNCHANGED                  True
    para 0  len 3577  sha256 4daea5953e355308  head "Gate: F272 R24 — the F272 round 24 entry. VERDICT PASS, AN"

(c) NEGATIVE CONTROL — in memory only, never on disk.

    flipped byte at offset 1210900, inside the FIRST added paragraph: 's' -> 'r'
    mutant_differs_from_post          True
    BYTE_READER_REJECTS_MUTANT        True
    STRUCTURAL_READER_REJECTS_MUTANT  True
    BYTE_READER_ACCEPTS_REAL_POST     True
    STRUCTURAL_READER_ACCEPTS_REAL_POST True
    DISK_REREAD_IDENTICAL_TO_REAL_POST True
    DISK_REREAD_SHA256 57a35edca4ea83a2c5ae06abda967e5e5a7eac4cf6b1e835f12d8c8067cc4f16
    DISK_NEVER_SAW_MUTANT             True

Both readers reject the one-byte mutant and both accept the real post-image,
so neither reader is a gate that cannot fail.

(d) COUNTS — each measured, none adjusted to agree. Block target on the left.

    ^- R-\d{4} distinct       309 -> 309    (block: 309 -> 309)  MATCH
    ^Done: R-\d{4} distinct   252 -> 252    (block: 252 -> 252)  MATCH
    open set BY DISTINCT ID    57 ->  57    (block:  57 ->  57)  MATCH
    ^Gate:                     47 ->  48    (block:  47 ->  48)  MATCH
    ^Gate: F272 R24             0 ->   1    (block:   0 ->   1)  MATCH
    ^- R-0826                   0 ->   0    (block:   0 ->   0)  MATCH

OPEN FINDINGS BY DISTINCT ID, with its arithmetic: 309 DISTINCT registered
ids minus 252 DISTINCT `Done:` ids = 57, before and after. The count is over
DISTINCT ids on both sides, not over lines, so a two-paragraph resolution is
not double-counted. `R-0826` occurs twice in the post-image as prose — once
in the round 23 entry and once in the RECORDR25 entry just added, both
saying the id is still free — and ZERO times as a `^- R-0826` registration.
R-0826 IS STILL FREE, as constraint 6 required.

**G3 THE TWO PROSE FILES — PASS, REAL_EXIT=0.**

    .agent/plan.md
      slice PLANF272R25       len 2545  lines 47  sha256 396c542e...8ecc271c
      worktree                len 2545  lines 47  sha256 396c542e...8ecc271c
      COMMITTED HEAD:         len 2545  lines 47  sha256 396c542e...8ecc271c
      PLAN_BYTE_EQUAL_TO_PLANF272R25   True (worktree AND committed)
      line count 47 vs the AGENTS.md cap of 50 -> UNDER, headroom 3
      '## Goal' present True     '## Next Steps' present True
      headings: ['## Goal', '## Current Step', '## Next Steps', '## Risks']

    .agent/prose_slips.md   (byte append check only)
      pre_len 148887 at base 4491ec9e — the block states 148887 -> MATCH
      pre_lines 555   pre_sha256 c54572e7...24568d20
      post_len 149432 post_lines 557  post_sha256 820d0c89...cff8ea10
      PRE_IS_BYTE_EXACT_PREFIX_OF_POST True
      POST_EQUALS_PRE_NL_SLICE          True
      LINE COUNT GAINED: 2 (one blank separator plus the one dated line)

**G4 THE FEATURE FILE — PASS, REAL_EXIT=0.**

    pre_len 58026   pre_lines 754   (block states 58026 bytes, 754 lines -> MATCH)
    pre_sha256  1227d1d7ce16b6ca1df26e128b263023aa3dd95f556df020ff3faf78d85dc224
    WORKING_PRE_EQUALS_BASE_BLOB (git show 4491ec9e:...) True
    slice_len 4870  slice_lines 13  sha256 3dc695e9...401f68e1
    post_len 62897  post_lines 768
    post_sha256 075e72d74c8a382afc7c09684531573b9a3dc2b04eb7863160f5d2d99aae4042
    PRE_IS_BYTE_EXACT_PREFIX_OF_POST True
    POST_EQUALS_PRE_NL_SLICE          True

`^### DECISION F272 D` headings: 14 before -> 15 after. The block states 14
at the base commit: MATCH. Numbers after, in file order, are exactly
`1,2,3,4,5,6,7,8,9,10,11,12,13,14,15` — no duplicate, no gap, each of D1
through D15 heading EXACTLY ONE section. Every heading line, in file order:

    ### DECISION F272 D1 (2026-09-06, F272 round 2) — the run re-key lands in two moves, and the run LOG keeps its job key
    ### DECISION F272 D2 (2026-09-06, F272 round 4) — correction to D1's premise: the observer set is the repository, not the three files the search read
    ### DECISION F272 D3 (2026-09-06, F272 round 5) — the name collapse takes two call shapes, chosen by whether the caller already binds the new name
    ### DECISION F272 D4 (2026-09-06, F272 round 7) — `job_id` stays the ONE required key of a job record, and the round 7 gate that said otherwise was the thing that was wrong
    ### DECISION F272 D5 (2026-09-06, F272 round 8) — the `state` collapse widens `RunState` first, then replaces `status` in ONE atomic move
    ### DECISION F272 D6 (2026-09-07, F272 round 9) — the `state` collapse is three moves, not two: the RENAME and the RETYPE are separated because only the retype can change what a state RENDERS as
    ### DECISION F272 D7 (2026-09-07, F272 round 10) — the `JobPlan.status` rename set is determined by RUNTIME PROBE, not by static classification, because `.status` is polymorphic in this repository and only a running object knows its own type
    ### DECISION F272 D8 (2026-09-07, F272 round 11) — `blocked` and `stopped` are SETTLED states in the cockpit, and a state vocabulary change is not finished until the cockpit can name it
    ### DECISION F272 D9 (2026-09-07, F272 round 12) — the run-state phrase guard in `test_digest_hero_card.py` is a FLOOR, as its two siblings already are; an equality there pinned an arity nobody meant to pin
    ### DECISION F272 D10 (2026-09-07, F272 round 13) — a `Landed:` line SURVIVES beside the `Done:` paragraph that resolves it; the record is append-only and is never overwritten
    ### DECISION F272 D11 (2026-09-07, F272 round 15) — the "D9 shape" the Mission contract is owed is `DECISION amend0905-vocab D9` in the binding vocabulary page, and under it the contract lands RESERVED
    ### DECISION F272 D12 (2026-09-07, F272 round 18) — the 2026-09-06 triage wins over this file's Acceptance, so the five tests.md ids are F273's; T003 is COMPLETE, and T004's blast radius is measured rather than estimated
    ### DECISION F272 D13 (2026-09-07, F272 round 20) — a command's ADVERTISEMENTS are deleted in the same commit as the command, and T004's remaining order is set by that rule rather than by the size of each handler
    ### DECISION F272 D14 (2026-09-07, F272 round 24) — T004 is staged BY CALLER, the twelve cluster-bound consumers are never migrated, and `job.run-next` dies WITH the rails rather than ahead of them
    ### DECISION F272 D15 (2026-09-07, F272 round 25) — correction to D14 part 2: the classic-to-unified flip is ATOMIC over the consumer graph, not stageable by caller, because `.id` is the last gap and it sits on shared helpers

D14's OWN SECTION IS BYTE-UNCHANGED. Base span, D14's heading to EOF at
`4491ec9e`: 5540 bytes, sha256 `e964d3f8...2209c667`. Post span, D14's
heading to the first byte of D15's heading: 5541 bytes, sha256
`f1178a88...04037702`.

    BASE_SPAN_IS_BYTE_EXACT_PREFIX_OF_POST_SPAN True
    DELTA_BYTES b'\n'
    D14_SECTION_BYTE_UNCHANGED_MODULO_TRAILING_BLANK True

The one-byte delta is the append's own blank-line SEPARATOR, which belongs to
the append and not to D14 — see the assumption declared below, where this is
stated rather than smoothed over. Every byte of D14's text is unchanged:
5539 bytes, sha256 `2ee226cc...57f2488f`. The whole pre-image being a
byte-exact prefix of the post-image (G4, above) independently proves the same
thing for every earlier byte in the file.

**G5 THE DOCS GATE — PASS, three suites run SERIALLY, REAL_EXIT=0 each.**

    python3 -B -m pytest tests/docs/ -q -p no:randomly
    -> 303 passed in 0.68s                                  REAL_EXIT=0

    python3 -B -m pytest tests/orchestration/test_roadmap_index.py -q -p no:randomly
    -> 30 passed in 0.45s                                   REAL_EXIT=0

    python3 -B -m pytest tests/cli/test_golden_path.py -q -p no:randomly
    -> 42 passed in 23.20s                                  REAL_EXIT=0

MEASURED 303, 30 and 42 — the reviewer's pre-measured figures were 303, 30
and 42, so all three match cell for cell, total 375. No `.py` file changed
this round, so no ruff reading is owed and none was taken.

**G6 THE TREE — PASS, REAL_EXIT=0.**

`git status --porcelain` was run at EVERY commit boundary and was EMPTY every
time — after C0a, C0b, C1, C2, C3 and C4, each printing nothing before the
`PORCELAIN_END` marker, and `''` on the final scripted read.

    git ls-files .remedy-wt -> ''   EMPTY True
    git worktree list -> 13 entries: the primary at feature/f272-one-world-completion
      plus exactly the twelve pre-existing remedy/job-* entries. UNCHANGED FROM BASE.

Per-commit insertions, `git diff --numstat <parent> <commit>`, against the
DECISION F104 D1 cap of 500 INSERTIONS:

    C0a 17d7e06c  insertions=280  under 500: True   (280/0   .agent/authored/f272-r25.md)
    C0b 1bfce0ee  insertions=167  under 500: True   (167/172 .agent/last_block.md)
    C1  9448a35d  insertions=23   under 500: True   (23/23   .agent/plan.md)
    C2  1d8741b6  insertions=2    under 500: True   (2/0     .agent/live_review.md)
    C3  869b6a43  insertions=2    under 500: True   (2/0     .agent/prose_slips.md)
    C4  e72a9602  insertions=14   under 500: True   (14/0    docs/roadmap/features/T2_F272.md)

C5 is excluded because a commit cannot count its own insertions while it is
being written. It is in any case the verbatim rewrite of a SINGLE `.agent/**`
state file, which DECISION F104 D1 exempts by name.

THE THREE `.agent/STOP` READINGS, all by `os.path.exists`:

    before C0a  os.path.exists('.agent/STOP') = False
    before C4   os.path.exists('.agent/STOP') = False
    before C5   os.path.exists('.agent/STOP') = False

No STOP file exists; the round proceeded.

## Authored-text proofs

Four reviewer-authored texts were applied, ALL extracted PROGRAMMATICALLY by
a regex over the marker lines of the COMMITTED `.agent/authored/f272-r25.md`,
inclusive of the newline ending each slice's last content line and exclusive
of both marker lines. Not one character was retyped. The extractor asserts
exactly one BEGIN and one END marker per name before it returns.

| Slice | Target | Mode | Result |
|-------|--------|------|--------|
| PLANF272R25 | `.agent/plan.md` | replace | 2545 bytes, sha256 `396c542e...8ecc271c`; disk byte-equal to the slice, in the worktree AND as committed |
| RECORDR25 | `.agent/live_review.md` | append | 3578 bytes, sha256 `d98e1cdd...842b2ef0`; `POST_EQUALS_PRE_NL_SLICE` True |
| SLIPSR25 | `.agent/prose_slips.md` | append | 544 bytes, sha256 `150ed591...ff27894c`; `POST_EQUALS_PRE_NL_SLICE` True |
| D15SLICE | `docs/roadmap/features/T2_F272.md` | append | 4870 bytes, sha256 `3dc695e9...401f68e1`; `POST_EQUALS_PRE_NL_SLICE` True |

C0a and C0b were `shutil.copyfile` of `.remedy-wt/f272-r25-block.md`, per
constraint 3, and G1 shows all five blobs identical.

## SESSION 11 CLOSES — the four points the block orders here

**1. THREE DELEGATED ROUNDS, AND WHY THAT IS BELOW TARGET.** Session 11 ran
rounds 23, 24 and 25. All three PASSED. Three is below the six-to-eight
target amend0905-throughput sets, and amend0906 rule 3 requires the reason in
one sentence: the session spent its measurement budget establishing that
T004's remaining work is a single atomic record flip rather than the
per-caller sequence the plan assumed, and that finding is what rounds 24 and
25 put on disk.

**2. THE NEXT SESSION IS SESSION 12, WHICH REACHES F272'S SOFT LIMIT of 12
sessions.** Its first obligation after the Phase 0 probe is therefore NOT
more building. It is the SCOPE REPORT, and then the amend0905-throughput
SPLIT-AND-CLOSE DEFAULT, EXECUTED ON THE SESSION'S OWN AUTHORITY — register
the remaining scope as a new feature placed directly after F272 per
amend0906-split-placement, close F272 at a self-consistent scope through the
normal closure sequence, and record the whole move as a dated DECISION. The
session output carries the line `SITZUNGS-LIMIT ERREICHT —
OPERATOR-BERICHT IN DER ÜBERGABE` when it writes that report.

**3. THE FIGURES THAT SCOPE REPORT NEEDS ARE ALREADY MEASURED AND MUST NOT BE
RE-DERIVED.** They are in `.agent/f272_t004_staging.md` and in DECISIONs
F272 D14 and D15: 60 production and 127 test files migrate, twelve
cluster-bound consumers never do, and the `.id` flip has an upper bound of
468 reads in 74 production files and 1545 in 137 test files — a bound from a
receiver-name heuristic, NOT a probe measurement, as D15 states in terms.

**4. THE NEXT SESSION'S FIRST ACTION.** Run Phase 0, the state probe. Then
check `.agent/STOP` under Phase 1 rule 1 BEFORE the Open PR Gate under rule
2, in that order. No PR exists for this branch and none was created —
`gh pr list --state open` returned `[]` this round.

## Deviations & assumptions

**No deviation from the block's ordered commit sequence.** C0a, C0b, C1, C2,
C3, C4, C5 were committed in exactly that order, one commit each, no extra
commit, none dropped, none reordered. Every path written is one of the seven
in the Change set; nothing outside it was touched.

**D1 — DECLARED DISAGREEMENT WITH CONSTRAINT 4, which I applied as written.**
Constraint 4 asserts that each of the three append targets "contains ZERO
occurrences of three consecutive newlines". That is TRUE for
`.agent/live_review.md` (measured 0) and for
`docs/roadmap/features/T2_F272.md` (measured 0), and FALSE for
`.agent/prose_slips.md`, which contains ONE such occurrence at byte offset
39213, after line 310, between a 2026-08 slip line and the
`2026-09-02 · F108 R7` line — a pre-existing double blank line that landed
long before this round. I did not repair it and I did not alter the append:
the ordered relation `post == pre + b"\n" + slice` was applied verbatim to
all three targets and `POST_EQUALS_PRE_NL_SLICE` is True for each. The
claim is not load-bearing — the property the appends actually depend on is
that each target ends in exactly ONE newline, which I measured as true for
all three (`pre_trailing_newline_run` 1, 1 and 1) — so under amend0827 rule
2 this is a reviewer-prose inaccuracy that reached no file, it spends no
R-id, and it earns no correction round. It is recorded here, and here only,
per the prose_slips.md rule that a non-load-bearing inaccuracy goes in the
handback's deviations.

**D2 — DECLARED READING OF G4's D14 SPAN COMPARISON.** G4 orders D14's
section proved byte-unchanged "by comparing the bytes between its heading and
the start of D15's heading against the same span at the base commit". At the
base commit there IS no D15 heading, so the base span can only run from D14's
heading to EOF. Those two spans are therefore not literally equal: the post
span is 5541 bytes and the base span 5540, and the single extra byte is the
`\n` that the append itself contributes as the blank-line separator before
D15. I did NOT relax the gate to make it pass. I reported the strict result
(`BASE_SPAN_IS_BYTE_EXACT_PREFIX_OF_POST_SPAN` True, `DELTA_BYTES` b'\n')
alongside the reading that answers the question the gate was asking
(`D14_SECTION_BYTE_UNCHANGED_MODULO_TRAILING_BLANK` True), so the reviewer
can see the exact delta rather than a rounded verdict. The independent and
stronger proof is in G4's own byte section: the entire 58026-byte pre-image
is a byte-exact prefix of the post-image, so no byte of D14 — or of anything
else already in that file — moved.

**D3 — TWO PUSHES, NOT ONE.** The branch was pushed after C4 so that this
handback could transcribe a REAL push with its real exit code, and it is
pushed again after C5. A handback cannot transcribe the push of itself. This
follows the round 24 precedent, which the reviewer accepted in the RECORDR25
entry booked this round.

**D4 — SCRATCH SCRIPTS ON DISK.** The gate scripts were written under the
gitignored `.remedy-wt/r25scratch/` rather than passed inline, because this
session's bash guard rejects heredocs by form — the first attempt at one was
refused with "Parser skipped input between top-level statements". They are
deleted BY EXACT PATH after the final push, never by a glob, and
`git ls-files .remedy-wt` is empty (G6).

**D5 — ASSUMPTION ON THE PLAN SLICE, applied verbatim, not corrected.**
PLANF272R25's opening line reads "Rounds 1 to 25 PASSED except round 2 ...
and round 21". Round 25 is THIS round and has no verdict yet; only the
reviewer can write one. I applied the slice byte for byte as constraint 1
requires and did not silently correct it. The claim is self-correcting — the
reviewer's verdict on this round either confirms it or is the thing that
contradicts it — and no gate depends on it.

**No worktree was created.** Constraint 8 forbade one; `git worktree list`
is unchanged from the base at the primary plus twelve pre-existing
`remedy/job-*` entries (G6).

**No finding id was minted.** Constraint 6 required `R-0826` to still be
free when the round ends, and G2(d) measures `^- R-0826` at 0 before and 0
after.

## Next

The reviewer re-runs G1 through G6 over `4491ec9e`..`HEAD` in the primary
checkout and books a verdict on round 25. Session 11 is then closed; session
12 opens with Phase 0, then the `.agent/STOP` check, then the Open PR Gate,
and owes the scope report and the split-and-close default before any further
building.
