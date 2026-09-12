# Handback — F275 round 77

## Session

SESSION 27 of feature F275 · round 77 · rounds so far 77

SITZUNGS-LIMIT ERREICHT — OPERATOR-BERICHT IN DER ÜBERGABE

F275 stands past the soft limit amend0908-f275-finish rule 1 names. The SCOPE REPORT that
rule obliges was written in round 51's handback and STANDS; it is not restated here, per the
block's Handback section. Rule 2 forbids the split-and-close default by name, so the session
writes the report reference and continues.

CONTEXT SELF-ASSESSMENT (amend0905-throughput): context is comfortable — the round was ten
single-path commits and seven gates, none of them a suite run and none of them re-taking a
transcript, so the reading budget went to the block, the artefact, the instrument carrier and
the instrument's own 157-line output rather than to the repository, and a further round in
this session would start from a healthy margin.

THE ROUND'S HEADLINE: all ten ordered commits landed in the Bundle's order, every gate ran,
and EVERY READING EVERY GATE TURNS ON HOLDS. DECISION F275 D50's inference is now a
CONSTRUCTION. The shipped owner check of DECISION F275 D47 contradicts 13 of the round 53
re-keyed set's 2198 sites, every one of those 13 is among the 60 the plain re-derivation
drops, and the corrected set — the round 53 set minus exactly those 13, at 2185 sites — is
that difference AS A SET, not merely at that count. The same owner check exits at 13
contradictions over the round 53 set and at ZERO over the corrected one, which is the
discriminator a guard needs at both ends. Run as a third arm at `ef75e213` against the same
control, the corrected set FIXES 23 test nodes and BREAKS 0; `Mission.job_id` falls from 22
location frames to none and `QueueEntry.job_id` from 5 to none. The instrument is byte-stable
across three runs, its 19 CROSS-CHECKS and 13 PARTITIONS all hold, no line of its output
reads MISMATCH, and its `EVERY CHECK HOLDS` line reads True. `R-0880` stays OPEN and the open
set is identical at both ends of the range, 87 by distinct id. NO PRODUCTION LINE MOVED.

### `.agent/STOP` EXISTS — THE SENTINEL APPEARED MID-ROUND AND THIS ROUND IS THE LAST

`.agent/STOP` did NOT exist at any reading constraint 7 orders — not before C1, not before
C6, and not inside G7(a), which measured `False`, `[]` and an empty `git status --porcelain`
at C5. It appeared afterwards, while C6 was being composed: a zero-byte file created at
`2026-09-12 10:03:36 +0200`, untracked. Guardrail G6 of `docs/agents/self_drive_protocol.md`
and constraint 7 of this round's block say the same thing — finish the commit in hand, write
the handback, stop — and the commit in hand was C6, which is this file. It was committed with
that fact recorded here rather than silently. NO FURTHER COMMIT WAS MADE, no gate was re-run
after the sentinel appeared, and the sentinel itself was NOT staged: it is not in the block's
Change section, staging it would widen the round, and deleting it would destroy the signal it
exists to carry. THE NEXT SESSION'S FIRST ACTION IS PHASE 1 RULE 1, BEFORE RULE 2: read
`.agent/STOP` from disk, write the handoff and end.

## Range

Review of `75cc221e`..`HEAD`.

## Commits

Nine ordered commits, C0a through C5, plus the handback commit C6. The `+/-` column below is
read from `git show --numstat <sha>` and from no other source; it is an INSERTION and
DELETION count, never a file's line count. The insertion cell of each of C0a through C5 is
compared CELL BY CELL against the number G4(f) reports for that same commit, at the end of
this section.

### 0b9e6f5c F275 R77 C0a: save the round 77 block as authored text.

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f275-r77.md` | +397 / -0 | the block saved as authored text, copied with `shutil.copyfile` from the reviewer's scratch original after its sha256 was verified against the wrapper's |

### 24d59a49 F275 R77 C0b: save the round 77 artefact as authored text.

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f275-r77-artefact.md` | +190 / -0 | the WHOLE TEXT artefact, transported with `shutil.copyfile`, never opened in an editor |

### 615018aa F275 R77 C0c: save the round 77 instrument carrier as authored text.

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f275-r77-instrument.py.md` | +329 / -0 | the WHOLE TEXT `.py.md` carrier, transported with `shutil.copyfile`; constraint 10 forbids a `.py` file under `.agent/` |

### e7c85d68 F275 R77 C0d: mirror the round 77 block into the last-block state file.

| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +156 / -144 | whole-file replacement, written from the COMMITTED C0a blob so G1 compares the two directly |

### 144b8370 F275 R77 C1: make the plan current for round 77.

| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +17 / -17 | whole-file replacement by slice PLAN77, extracted from the COMMITTED C0a blob |

### de137e51 F275 R77 C2: book the round 76 reviewer verdict.

| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +12 / -0 | append of slice RECORD77, the round 76 PASS verdict, per amend0827 rule 1 |

### b07834fb F275 R77 C3: append the round 76 prose slips.

| Path | +/- | Reason |
|---|---|---|
| `.agent/prose_slips.md` | +6 / -0 | append of slice SLIPS77, three dated lines, no id spent |

### ed7232a8 F275 R77 C4: record DECISION F275 D51, the flip's constructed input set.

| Path | +/- | Reason |
|---|---|---|
| `.agent/decisions.md` | +18 / -0 | append of slice DEC77, DECISION F275 D51; the deletion column is 0, so D50 is untouched |

### d1ee2114 F275 R77 C5: land the partition artefact for round 77.

| Path | +/- | Reason |
|---|---|---|
| `.agent/f275_t003_flip_residue_r77.md` | +190 / -0 | the partition artefact, written from the COMMITTED C0b blob |

### the handback commit C6 — `.agent/handoff.md`

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | measured by the reviewer at the next gate | this file; a handback cannot table the commit that writes it (the R-0149 self-reference exception of `docs/agents/handback_template.md`), and the block removes it from every gate of this round: "The handback commit's own numbers are NOT a gate of this round" |

### The cell-by-cell comparison the block's Handback section orders

| Commit | table insertion cell | G4(f) insertion count | AGREE |
|---|---|---|---|
| C0a | 397 | 397 | True |
| C0b | 190 | 190 | True |
| C0c | 329 | 329 | True |
| C0d | 156 | 156 | True |
| C1 | 17 | 17 | True |
| C2 | 12 | 12 | True |
| C3 | 6 | 6 | True |
| C4 | 18 | 18 | True |
| C5 | 190 | 190 | True |

ALL NINE CELLS AGREE: True. Both columns are `git show --numstat` readings taken by separate
runs — the table's by this composition, G4(f)'s inside the gate transcript.

## External actions

| Action | Outcome |
|---|---|
| `git worktree add --detach .remedy-wt/r77_g3_wt d1ee2114` | created for the G3(iii) negative control, exit 0 |
| `git worktree remove --force .remedy-wt/r77_g3_wt` | exit 0, inside the same script |
| `git worktree prune` | exit 0, inside the same script; `git worktree list` afterwards shows the primary checkout alone |
| `git push -u origin feature/f275-one-world-completion-part-three` | run after C6, which is this commit; a handback cannot carry the outcome of an action that follows it, so the outcome is in the round report and in the remote's own ref |

NO `gh` COMMAND AND NO `remedy` CLI COMMAND WAS RUN, per constraint 6. No pull request was
created, edited or merged. No branch was created. No merge. No force-push.

## Verification

ONE LINE PER GATE, with the REAL_EXIT read back out of its own transcript file under
`.remedy-wt/`, per constraint 11. Every gate ran at C5, strictly earlier than C6.

| Gate | transcript | REAL_EXIT |
|---|---|---|
| G1 transport, the block budget, the insertion cap | `.remedy-wt/r77_g1.out` | 0 |
| G2 the plan | `.remedy-wt/r77_g2.out` | 0 |
| G3 the record (i–vii, incl. the negative control) | `.remedy-wt/r77_g3.out` | 0 |
| G4 the artefact and its transcript (a–f) | `.remedy-wt/r77_g4.out` | 0 |
| G5(a) the fence extraction | `.remedy-wt/r77_g5a.out` | 0 |
| G5(b) the instrument run | `.remedy-wt/r77_g5b.out` | 0 |
| G5(c)+(d) determinism and the readings | `.remedy-wt/r77_g5cd.out` | 0 |
| G5(e) tree and worktrees after G5 | `.remedy-wt/r77_g5e.out` | 0 |
| G6(a) top-level tree object ids | `.remedy-wt/r77_g6a.out` | 0 |
| G6(b) the canary | `.remedy-wt/r77_g6b.out` | 0 |
| G6(c) `ruff check .` | `.remedy-wt/r77_g6c.out` | **1** — the block anticipates it: "Its exit is 1 whenever any finding remains, so THE GATE IS THE COUNT" |
| G6(c) the counts | `.remedy-wt/r77_g6c_counts.out` | 0 |
| G6(d) constraint 10 read off the filesystem | `.remedy-wt/r77_g6d.out` | 0 |
| G7 nothing else moved (a–c) | `.remedy-wt/r77_g7.out` | 0 |

### G1 — transport, the block budget, and the insertion cap

    === G1 TRANSPORT ===
      C0a .agent/authored/f275-r77.md                  committed (39315, 'a4006b53…039e97') | scratch (39315, 'a4006b53…039e97') | EQUAL
      C0b .agent/authored/f275-r77-artefact.md         committed (11738, 'bc4abd74…2f1303') | scratch (11738, 'bc4abd74…2f1303') | EQUAL
      C0c .agent/authored/f275-r77-instrument.py.md    committed (15578, 'bb8c3325…f1e1bf') | scratch (15578, 'bb8c3325…f1e1bf') | EQUAL
      C0d .agent/last_block.md                         committed (39315, 'a4006b53…039e97') | C0a blob (39315, 'a4006b53…039e97') | EQUAL

    === G1 THE SLICES IN THE COMMITTED C0a BLOB ===
      PLAN77    bytes  2854  lines  48  MATCHES ITS BEGIN MARKER: True
      RECORD77  bytes  5217  lines  11  MATCHES ITS BEGIN MARKER: True
      SLIPS77   bytes  2840  lines   5  MATCHES ITS BEGIN MARKER: True
      DEC77     bytes  6614  lines  17  MATCHES ITS BEGIN MARKER: True
      CARDINALITY MEASURED: 4  ['DEC77', 'PLAN77', 'RECORD77', 'SLIPS77']

    === G1 THE BLOCK BUDGET, RE-MEASURED ON THE COMMITTED C0a BLOB ===
      TOTAL lines measured : 397  | constraint 8 states 397 | EQUAL: True
      PROSE lines measured : 316  | constraint 8 states 316 | EQUAL: True
      (PROSE = TOTAL 397 minus the 81 lines lying between BEGIN and END markers)
      lines that are a single character repeated, length-two reading (len>=2): 0
      lines that are a single character repeated, length-one reading (len>=1): 0

    === G1 THE INSERTION CAP, DECISION F104 D1, OVER EVERY BLOB THIS ROUND CREATES ===
      C0a  .agent/authored/f275-r77.md                  lines  397  under 500: True
      C0b  .agent/authored/f275-r77-artefact.md         lines  190  under 500: True
      C0c  .agent/authored/f275-r77-instrument.py.md    lines  329  under 500: True
      C5   .agent/f275_t003_flip_residue_r77.md         lines  190  under 500: True
      C0d  .agent/last_block.md                         lines  397  under 500: True  (a REPLACEMENT, not a creation; its insertion count is reported by G4(f))

    === G1 THE .py.md CARRIER ROUND-TRIP ===
      '```python' fence lines: 1 [10] | bare '```' fence lines: 1 [328]
      extracted source: (15045, '1eaaf115…6fbbdb') -> .remedy-wt/f275-r77-instrument.py
      re-wrapping in the carrier's own header and fence reproduces the committed blob BYTE FOR BYTE: True

    G1_RC=0
    REAL_EXIT=0

BOTH BLOCK NUMERALS REPRODUCE. The committed C0a blob re-measures at 397 lines TOTAL and 316
lines PROSE, which are exactly the numerals constraint 8 states, and the block carries zero
repeated-character lines under BOTH the length-two and the length-one reading, as constraint
15 fixes.

### G2 — the plan

      G2 .agent/plan.md at C1 : 2854 bytes  sha256 15263f85ce972fe61289fc920ff83ff97132ba696d03ae871dad2aff2475eea9
      G2 slice PLAN77         : 2854 bytes  sha256 15263f85ce972fe61289fc920ff83ff97132ba696d03ae871dad2aff2475eea9
      G2 BYTE-IDENTICAL: True
      G2 line count: 48  against the AGENTS.md cap of 50 -> under cap: True
      G2 lines matching ^## Goal$      : 1 (must be 1)
      G2 lines matching ^## Next Steps$: 1 (must be 1)

    G2_RC=0
    REAL_EXIT=0

### G3 — the record: two independent readers and a negative control, three times over

        (i) READER A, the byte stream
          .agent/live_review.md    pre  1073697  post  1078915  delta   5218  body   5217  -> ACCEPT
          .agent/prose_slips.md    pre   278733  post   281574  delta   2841  body   2840  -> ACCEPT
          .agent/decisions.md      pre  1208247  post  1214862  delta   6615  body   6614  -> ACCEPT

        (ii) READER B, structural, over the WHOLE appended region
          .agent/live_review.md    N counted from the slice = 6  -> ACCEPT
          .agent/prose_slips.md    N counted from the slice = 3  -> ACCEPT
          .agent/decisions.md      N counted from the slice = 9  -> ACCEPT

        (iii) NEGATIVE CONTROL, in the disposable worktree .remedy-wt/r77_g3_wt
          .agent/live_review.md    byte offset  1073698  letter 'G' -> 'Z' | READER A REJECT | READER B (N=6) REJECT
          .agent/live_review.md    UNMUTATED                              | READER A ACCEPT | READER B (N=6) ACCEPT
          .agent/prose_slips.md    byte offset   278748  letter 'F' -> 'Z' | READER A REJECT | READER B (N=3) REJECT
          .agent/prose_slips.md    UNMUTATED                              | READER A ACCEPT | READER B (N=3) ACCEPT
          .agent/decisions.md      byte offset  1208251  letter 'D' -> 'Z' | READER A REJECT | READER B (N=9) REJECT
          .agent/decisions.md      UNMUTATED                              | READER A ACCEPT | READER B (N=9) ACCEPT
          worktree remove exit: 0 | worktree prune exit: 0
          git worktree list afterwards: /home/decodeux/Repos/remedy  d1ee2114 [feature/f275-one-world-completion-part-three]

        (iv) RECORD77 line count: 11 | lines AFTER THE FIRST carrying a reserved prefix: 0
             lines C2 ADDS: 12 | of them ^- R-: 0 | of them ^Done: R-: 0

        (v)  lines at the base already matching `^Gate: F275 R\d+ — the F275 round \d+ entry\.`: 75
             the new first line matches that same pattern: True
             the new first line duplicates one of them: False

        (vi) DEC77 begins '## DECISION F275 D51 ': True
             lines at the base matching ^## DECISION F275 D51: 0
             highest existing ^## DECISION F275 D<n> at the base: D50
             C4 git show --numstat: ['18', '0', '.agent/decisions.md'] -> C4 REMOVES NO LINE: True

        (vii) SLIPS77 paragraphs it adds: 3 | of them beginning '2026-09-12 · F275 R76 · ': 3
              lines at the base already beginning with that exact prefix: 0

    G3_RC=0
    REAL_EXIT=0

EVERY FLIPPED BYTE WAS AN ASCII LETTER BY THE BYTE RANGE G3(iii) NAMES — 0x41 to 0x5A or
0x61 to 0x7A, tested as a BYTE and never through `chr(b).isalpha()`, which is the latin-1
test the round 76 slip records. Each flip landed inside the FIRST appended paragraph of its
file, both readers REJECTED it, and the same two readers ACCEPTED the unmutated region
immediately afterwards in the same worktree. `.agent/prose_slips.md` is the file the range
matters for: its every paragraph opens with a U+00B7 whose lead byte 0xB7 passes the naive
test, and the flip this round took landed at offset 278748 on the ASCII letter `F`.

### G4 — the artefact and its transcript

        (a) THE ARTEFACT
            artefact at C5 : 11738 bytes  sha256 bc4abd74d806b9b36f4b413782fe9c3e0bd5c87438aebdb41e2c44a23d2f1303
            C0b blob       : 11738 bytes  sha256 bc4abd74d806b9b36f4b413782fe9c3e0bd5c87438aebdb41e2c44a23d2f1303
            BYTE-IDENTICAL: True
            git show 75cc221e:.agent/f275_t003_flip_residue_r77.md -> exit 128
            stderr: fatal: path '.agent/f275_t003_flip_residue_r77.md' exists on disk, but not in '75cc221e'

        (b) THE TRANSCRIPT
            lines consisting of three backticks (must be 0): 0
            quoted lines checked (begin with whitespace, not blank): 62
            of them with NO stripped-equal line in the instrument's output: 0

        (c) THE ORDER PROPERTY, AS A MONOTONE MATCHING
            matched in order : 62 | unmatchable : 0
            every quoted line matched: True | matched indices strictly increase: True

        (d) THE FIGURES, SWEPT OVER THE ARTEFACT'S PROSE READ AS A WHOLE
            digit runs swept: 79
            of them occurring as a digit run in the instrument's output: 57
            of them NOT occurring                                     : 22
            unresolved digit-run OCCURRENCES, each with the line that uses it,
            classified against THE ARTEFACT'S OWN PROVENANCE CLAUSE:
              275    feature id           | # F275 T003 — the flip's input set, CONSTRUCTED: the partition of the 60, and a third arm that is strictly bet
              003    task slice id        | # F275 T003 — the flip's input set, CONSTRUCTED: the partition of the 60, and a third arm that is strictly bet
              213    commit id            | > Measured by the reviewer at `ef75e213`, round 76's base and the commit all three arms of
              275    artefact file name   | > moved in the round that wrote it. It replaces `.agent/f275_t003_flip_residue_r76.md` in no
              003    artefact file name   | > moved in the round that wrote it. It replaces `.agent/f275_t003_flip_residue_r76.md` in no
              275    artefact file name   | > the output of the committed instrument `.agent/authored/f275-r77-instrument.py.md`, which is
              275    feature id           | ## 1. What DECISION F275 D50 left open, and in its own terms
              275    feature id           | Rule H stage DECISION F275 D47 landed reads each ruled site's receiver against the live record
              275    feature id           | declines to decide about are untouched. DECISION F275 D45 ruled that blind spot acceptable and
              275    feature id           | DECISION F275 D48, as corrected by D49, discharged its precondition on a witness measurement;
              48     decision id          | DECISION F275 D48, as corrected by D49, discharged its precondition on a witness measurement;
              49     decision id          | DECISION F275 D48, as corrected by D49, discharged its precondition on a witness measurement;
              275    feature id           | All three arms run the same guarded transform of DECISION F275 D43 at `ef75e213` against the
              213    commit id            | All three arms run the same guarded transform of DECISION F275 D43 at `ef75e213` against the
              275    feature id           | DECISION F275 D45 said it would, and it is the residue the next round owns.
              275    feature id           | transform consumes today it fixes 23 test nodes and breaks none. DECISION F275 D50's inference
              275    feature id           | discharged twice over — statically by DECISION F275 D44's bound and behaviourally here — but
              44     decision id          | discharged twice over — statically by DECISION F275 D44's bound and behaviourally here — but
              275    artefact file name   | `.agent/f275_t003_flip_residue_r59.md` named as unexplained by any rule this chain has written
              003    artefact file name   | `.agent/f275_t003_flip_residue_r59.md` named as unexplained by any rule this chain has written
              275    feature id           | NOTHING HERE TOUCHES THE id-SHAPE SEAM DECISION F275 D37 routed into T003's resolver collapse,
              003    task slice id        | NOTHING HERE TOUCHES THE id-SHAPE SEAM DECISION F275 D37 routed into T003's resolver collapse,
            by kind:
              feature id                                                      10
              artefact file name                                               5
              decision id                                                      3
              commit id                                                        2
              task slice id                                                    2
            COUNT THAT COULD NOT BE PLACED UNDER THE CLAUSE: 0

        (e) NO QUOTED LINE CARRIES A WALL-CLOCK DURATION
            quoted lines matching 'in \d+\.\d+s' (must be 0): 0
            for contrast, lines in the instrument's OUTPUT matching it: 0

        (f) THE INSERTION CAP, PER COMMIT
            C0a  0b9e6f5c  insertions  397  deletions    0  paths staged 1  under 500: True
            C0b  24d59a49  insertions  190  deletions    0  paths staged 1  under 500: True
            C0c  615018aa  insertions  329  deletions    0  paths staged 1  under 500: True
            C0d  e7c85d68  insertions  156  deletions  144  paths staged 1  under 500: True
            C1   144b8370  insertions   17  deletions   17  paths staged 1  under 500: True
            C2   de137e51  insertions   12  deletions    0  paths staged 1  under 500: True
            C3   b07834fb  insertions    6  deletions    0  paths staged 1  under 500: True
            C4   ed7232a8  insertions   18  deletions    0  paths staged 1  under 500: True
            C5   d1ee2114  insertions  190  deletions    0  paths staged 1  under 500: True

    G4_RC=0
    REAL_EXIT=0

G4(e) HOLDS AND ITS CONTRAST READING MOVED SINCE ROUND 76, WHICH IS WORTH STATING RATHER
THAN LEAVING TO BE NOTICED. The artefact quotes 0 lines carrying a wall-clock duration, which
is the gate. The contrast figure — lines in the INSTRUMENT'S OWN OUTPUT matching
`in \d+\.\d+s` — is 0 this round where it was 3 in round 76, because this round's
instrument reads the suite transcripts' node-id lines and its own summary parser never
prints the pytest summary line it matched. Constraint 14 is satisfied a fortiori: there is
no duration in the output for the artefact to quote.

### G5 — the instrument

      committed C0c carrier: 15578 bytes sha256 bb8c33256d936593639daa756dc3f9025eb22b69b9bbafc79b1255bc35f1e1bf
      '```python' fence lines: 1 [10] | bare '```' fence lines: 1 [328]
      extracted to .remedy-wt/f275-r77-instrument.py: 15045 bytes sha256 1eaaf115135989f8340b361a70cf15b735d08f681150da26b3c9dd3f546fbbdb

    G5A_RC=0
    REAL_EXIT=0

CONSTRAINT 12 WAS DISCHARGED BEFORE THE INSTRUMENT RAN, NOT AFTER. All TWELVE scratch inputs
its own section 0 names were checked present at the size and sha256 printed for them; none
was missing, none differed, and NOTHING WAS REGENERATED. The four pytest transcripts —
`r76_suite_ctl.out`, `r76_suite_r53.out`, `r76_suite_plain.out` and `r77_suite_corr.out` —
were read, never re-taken. Because a digest the instrument computes for its own input cannot
by itself pin that input, the seven `r76_*` inputs were ADDITIONALLY compared against the
digests round 76's own committed handback printed for them at `75cc221e`; all seven are
byte-identical at the same sizes. The five `r77_*` inputs are new to this round and are
pinned by this handback and by the instrument's section 0.

#### The instrument's output, reproduced in full (G5(b))

    === 0. THE INPUTS THIS READING IS TAKEN FROM ===
      Every figure below comes from these files and from nothing else.
        r76_r53_rekeyed.json          121516 bytes  sha256 489fdf8eeb9c4e66b452510de5d362e5d701b4cfe2de79d1d69b768f526d301f
        r76_plain_rekeyed.json        117826 bytes  sha256 b27b7cf3b0a322cb7aca8d9497df7ea0631a41cb6a65849cd9731da9bc18e247
        r77_corrected.json            120753 bytes  sha256 765b5ba99f2c92765349c3a013f4074c62ece893cb50b373450927af0290a512
        r77_stage.out                   2386 bytes  sha256 abc6418820bd0734f7f90c9bbb8b485a461aaed017a871a024d5a7989b5c85c7
        r77_stage_corrected.out          447 bytes  sha256 86ecf97aa7c6a522427e2f137782594546a2f330d7a87f2242ec37bee2e56fc6
        r76_tf_r53.out                  1285 bytes  sha256 7894590a2247eb579ddb009e33a02667fdf7b9b8ebb60ad4d2de86430159105a
        r76_tf_plain.out                1252 bytes  sha256 9f1d64a971e28cf45fd933a902917610164a6b7e1b3bd2080c942b8ebd5808a4
        r77_tf_corr.out                 1285 bytes  sha256 8897d3257d924c97d50642a7d73b47e401f92c7f0be46ae0d39eeda32f14299e
        r76_suite_ctl.out              30331 bytes  sha256 020cd6ddab345b95f9cd4a9edf7d72a696133a70a1317c483e430d087119cd51
        r76_suite_r53.out             661081 bytes  sha256 a1d3dd065cf70c40963f5952f70a85b1b762f061781429855ea13b4c5d3f2039
        r76_suite_plain.out           699487 bytes  sha256 3fe5b1b5a0fb1e347b0c28179bfeb1a3ddb90f5e3a90f6343d712a4c2b27fd75
        r77_suite_corr.out            654679 bytes  sha256 a1405326e856f9b1a88c802e6418f43f7250037c68c1fd510b94968677e9038b

    === 1. THE THREE RULED SITE SETS, IN SITES ===
      round 53 committed, re-keyed           : 2198 sites
      round 67 plain re-derivation, re-keyed : 2138 sites
      THE CORRECTED SET                      : 2185 sites
      sites the PLAIN set drops              : 60 sites
      the CORRECTED set is a SUBSET of round 53's : True
      the PLAIN set is a SUBSET of the CORRECTED one : True

    === 2. THE PARTITION OF THE DROPPED SITES ===
      the SHIPPED owner check over the round 53 set: ruled 2198, decided 1921, refused 277, CONTRADICTED 13
      CROSS-CHECK the CONTRADICTED rows parsed against the count the stage prints: 13 against 13 sites  -> MATCH
      CROSS-CHECK the stage's ruled-site count against the set file it was given: 2198 against 2198 sites  -> MATCH
      PARTITION the owner check's verdicts: 1921 + 277 = 2198 against 2198 sites  -> MATCH
      the receiver classes it names, in sites:
            9  Mission
            3  Artifact
            1  QueueEntry
      PARTITION the contradicted sites by receiver class: 9 + 3 + 1 = 13 against 13 sites  -> MATCH

      CONTRADICTED and dropped by the plain set : 13 sites
      CONTRADICTED but KEPT by the plain set     : 0 sites
      dropped but NOT contradicted               : 47 sites
      PARTITION the dropped sites, by whether the owner check contradicts them: 13 + 47 = 60 against 60 sites  -> MATCH
      EVERY SITE THE OWNER CHECK CONTRADICTS IS ONE THE PLAIN SET DROPS: True
      CROSS-CHECK the corrected set against the round 53 set minus the contradicted sites: 2185 against 2185 sites  -> MATCH
      the corrected set IS that difference, as a set: True

      the 47 sites the plain set drops that the owner check does NOT contradict, by file:
           12  packages/orchestration/long_run_executor.py
           10  tests/orchestration/test_self_dogfood_execution.py
            8  packages/orchestration/task_runner.py
            7  packages/orchestration/dag_schedule.py
            3  packages/orchestration/verifier.py
            2  tests/test_project_brain.py
            1  packages/orchestration/agent_loop.py
            1  packages/orchestration/brain_detail.py
            1  tests/cli/test_repair_runtime.py
            1  tests/cli/test_self_dogfood_execution_cli.py
            1  tests/orchestration/test_repair_loop_v1.py
      PARTITION those sites by file: 12 + 10 + 8 + 7 + 3 + 2 + 1 + 1 + 1 + 1 + 1 = 47 against 47 sites  -> MATCH

    === 3. THE GUARD FIRES, AND THEN PASSES ===
      A guard that has never been seen to fail is not a guard, and one that can never
      pass is the same defect wearing the other face. Both readings are here.
      over the round 53 set   : CONTRADICTED 13
      over the CORRECTED set  : CONTRADICTED 0
      CROSS-CHECK the corrected run's contradicted count against zero: 0 against 0 sites  -> MATCH
      CROSS-CHECK the corrected run's ruled-site count against the corrected set file: 2185 against 2185 sites  -> MATCH
      THE BLIND SPOT IS UNCHANGED AND IS STATED: refused 277 over the round 53 set and 277 over the corrected one — the corrected set removes what the check DECIDES against, never what it refuses to decide.

    === 4. THE THREE TRANSFORM RUNS, IN REWRITES ===
      round 53   ruled  2198  files  263  total  6091  undecided  3084
      CROSS-CHECK the round 53 arm's ruled-key count against its own set file: 2198 against 2198 sites  -> MATCH
      CROSS-CHECK the round 53 arm's rule table against its own printed total: 6091 against 6091 rewrites  -> MATCH
      PLAIN      ruled  2138  files  263  total  6032  undecided  3143
      CROSS-CHECK the PLAIN arm's ruled-key count against its own set file: 2138 against 2138 sites  -> MATCH
      CROSS-CHECK the PLAIN arm's rule table against its own printed total: 6032 against 6032 rewrites  -> MATCH
      CORRECTED  ruled  2185  files  263  total  6078  undecided  3097
      CROSS-CHECK the CORRECTED arm's ruled-key count against its own set file: 2185 against 2185 sites  -> MATCH
      CROSS-CHECK the CORRECTED arm's rule table against its own printed total: 6078 against 6078 rewrites  -> MATCH

    === 5. THE THREE SUITE RUNS BESIDE THEIR CONTROL, IN TEST NODES ===
      CROSS-CHECK CONTROL failed node ids against its own tally line: 1 against 1 nodes  -> MATCH
      CROSS-CHECK CONTROL error node ids against its own tally line: 0 against 0 nodes  -> MATCH
      CONTROL    failed     1   errors     0
      round 53   failed  1186   errors    42   CAUSED BY THE FLIP  1227
      CROSS-CHECK round 53 failed node ids against its own tally line: 1186 against 1186 nodes  -> MATCH
      CROSS-CHECK round 53 error node ids against its own tally line: 42 against 42 nodes  -> MATCH
      PARTITION the round 53 arm: 1185 + 42 = 1227 against 1227 nodes  -> MATCH
      PLAIN      failed  1331   errors    31   CAUSED BY THE FLIP  1361
      CROSS-CHECK PLAIN failed node ids against its own tally line: 1331 against 1331 nodes  -> MATCH
      CROSS-CHECK PLAIN error node ids against its own tally line: 31 against 31 nodes  -> MATCH
      PARTITION the PLAIN arm: 1330 + 31 = 1361 against 1361 nodes  -> MATCH
      CORRECTED  failed  1174   errors    31   CAUSED BY THE FLIP  1204
      CROSS-CHECK CORRECTED failed node ids against its own tally line: 1174 against 1174 nodes  -> MATCH
      CROSS-CHECK CORRECTED error node ids against its own tally line: 31 against 31 nodes  -> MATCH
      PARTITION the CORRECTED arm: 1173 + 31 = 1204 against 1204 nodes  -> MATCH

    === 6. THE CORRECTED ARM AGAINST THE OTHER TWO, IN NODES ===
      CORRECTED against round 53 : FIXES   23 nodes, BREAKS    0 nodes, net   -23
      PARTITION the round 53 arm by what the corrected set keeps and fixes: 1204 + 23 = 1227 against 1227 nodes  -> MATCH
      CORRECTED against PLAIN    : FIXES  174 nodes, BREAKS   17 nodes, net  -157
      PARTITION the PLAIN arm by what the corrected set keeps and fixes: 1187 + 174 = 1361 against 1361 nodes  -> MATCH

      the 23 nodes the corrected set fixes over the round 53 set, by test file:
             8  tests/orchestration/test_watchdog.py
             6  tests/orchestration/test_loop_run.py
             3  tests/cli/test_repair_request_cli.py
             2  tests/cli/test_repair_v1_cli.py
             2  tests/orchestration/test_mission_state.py
             2  tests/orchestration/test_queue_executor_binding.py
      PARTITION those nodes by file: 8 + 6 + 3 + 2 + 2 + 2 = 23 against 23 nodes  -> MATCH

    === 7. THE ATTRIBUTION ACROSS THE THREE ARMS, IN LOCATION FRAMES ===
      Every AttributeError frame naming a receiver class and a missing attribute falls in
      exactly one bucket, every bucket is listed in full, and none is abridged.

      --- round 53 ---   location frames parsed: 994
      UNDER-SELECTION, a classic field read left on a unified record: 0 frames over 0 kinds
      OVER-SELECTION on a NAMED class, which is what R-0880 reports: 59 frames over 6 kinds
             25  Artifact.job_id
             22  Mission.job_id
              5  BrainNode.task_id
              5  QueueEntry.job_id
              1  BrainNode.job_id
              1  _FakeJob.job_id
      a unified field read on an ABSENT receiver, a different cause: 5 frames over 1 kinds
              5  NoneType.job_id
      PARTITION the round 53 attribution buckets: 0 + 59 + 5 + 36 = 100 against 100 frames  -> MATCH

      --- PLAIN ---   location frames parsed: 1128
      UNDER-SELECTION, a classic field read left on a unified record: 231 frames over 2 kinds
            224  TaskEntry.id
              7  JobPlan.id
      OVER-SELECTION on a NAMED class, which is what R-0880 reports: 1 frames over 1 kinds
              1  _FakeJob.job_id
      a unified field read on an ABSENT receiver, a different cause: 5 frames over 1 kinds
              5  NoneType.job_id
      PARTITION the PLAIN attribution buckets: 231 + 1 + 5 + 35 = 272 against 272 frames  -> MATCH

      --- CORRECTED ---   location frames parsed: 969
      UNDER-SELECTION, a classic field read left on a unified record: 0 frames over 0 kinds
      OVER-SELECTION on a NAMED class, which is what R-0880 reports: 19 frames over 4 kinds
             12  Artifact.job_id
              5  BrainNode.task_id
              1  BrainNode.job_id
              1  _FakeJob.job_id
      a unified field read on an ABSENT receiver, a different cause: 5 frames over 1 kinds
              5  NoneType.job_id
      PARTITION the CORRECTED attribution buckets: 0 + 19 + 5 + 36 = 60 against 60 frames  -> MATCH

      THE TRADE, IN FRAMES. under-selection: round 53 0, PLAIN 231, CORRECTED 0. over-selection on a named class: round 53 59, PLAIN 1, CORRECTED 19.
      THE CORRECTED SET IS THE ONLY ARM WITH NO UNDER-SELECTION AND LESS OVER-SELECTION
      THAN THE SET THE TRANSFORM CONSUMES TODAY.

    === 8. THE CHECKS THIS OUTPUT CARRIES, COUNTED ===
      A CROSS-CHECK compares two numbers derived from DIFFERENT sources and can fail; a
      PARTITION adds a set's own parts back to the set and cannot. Both are printed, and
      only the first kind is evidence that anything was verified.
      CROSS-CHECKS run : 19   holding: 19   FAILING: 0
      PARTITIONS run   : 13   holding: 13   FAILING: 0
      EVERY CHECK HOLDS: True
    REAL_EXIT=0

#### G5(c) determinism and G5(d) the readings

      (c) DETERMINISM, three runs
          run 1 stdout sha256: 76fdb35b73e2e70f29262b0a10e02e98b02908fd9ae8b785acf89d37fd18fa68 (10330 bytes) exit 0
          run 2 stdout sha256: 76fdb35b73e2e70f29262b0a10e02e98b02908fd9ae8b785acf89d37fd18fa68 (10330 bytes) exit 0
          run 3 stdout sha256: 76fdb35b73e2e70f29262b0a10e02e98b02908fd9ae8b785acf89d37fd18fa68 (10330 bytes) exit 0
          all three identical: True

      (d) THE READINGS
          lines containing 'MISMATCH': 0
          lines whose stripped text BEGINS with 'CROSS-CHECK ': 19
          lines whose stripped text BEGINS with 'PARTITION '  : 14
          the same counts read at column 0, unstripped        : 0 and 0
          verdict-bearing records (lines ending '-> MATCH' or '-> MISMATCH'): 32
          section 8: CROSS-CHECKS run : 19   holding: 19   FAILING: 0
          section 8: PARTITIONS run   : 13   holding: 13   FAILING: 0
          section 8: EVERY CHECK HOLDS: True
          SIDE BY SIDE, NOT RECONCILED: the CROSS-CHECK prefix count 19 against the summary's 19; the PARTITION prefix count 14 against the summary's 13 — section 8's own explanatory prose opens with the word PARTITION, which is the excess of one constraint of the block names.

          SECTION 0 — CONSTRAINT 12, EVERY NAMED INPUT PRESENT AT ITS PRINTED SIZE AND DIGEST
            r76_r53_rekeyed.json          121516 bytes  PRESENT AND EQUAL
            r76_plain_rekeyed.json        117826 bytes  PRESENT AND EQUAL
            r77_corrected.json            120753 bytes  PRESENT AND EQUAL
            r77_stage.out                   2386 bytes  PRESENT AND EQUAL
            r77_stage_corrected.out          447 bytes  PRESENT AND EQUAL
            r76_tf_r53.out                  1285 bytes  PRESENT AND EQUAL
            r76_tf_plain.out                1252 bytes  PRESENT AND EQUAL
            r77_tf_corr.out                 1285 bytes  PRESENT AND EQUAL
            r76_suite_ctl.out              30331 bytes  PRESENT AND EQUAL
            r76_suite_r53.out             661081 bytes  PRESENT AND EQUAL
            r76_suite_plain.out           699487 bytes  PRESENT AND EQUAL
            r77_suite_corr.out            654679 bytes  PRESENT AND EQUAL
            named inputs MEASURED: 12 | failing: 0

          SECTION 2
            'EVERY SITE THE OWNER CHECK CONTRADICTS IS ONE THE PLAIN SET DROPS: True': True
            'the corrected set IS that difference, as a set: True': True

          SECTION 3
            CONTRADICTED over the round 53 set : 13 -> non-zero: True
            CONTRADICTED over the CORRECTED set: 0 -> zero    : True

          SECTION 6
            CORRECTED against round 53 : FIXES   23 nodes, BREAKS    0 nodes, net   -23
            the BREAKS cell reads 0: True

    G5CD_RC=0
    REAL_EXIT=0

        (e) AFTER G5
            git status --porcelain: ''
            git worktree list:
              /home/decodeux/Repos/remedy  d1ee2114 [feature/f275-one-world-completion-part-three]
    REAL_EXIT=0

### G6 — the tree did not move

        (a) TOP-LEVEL TREE OBJECT IDS
          packages  base 2f8a05b5d7c2fde5ec8b0ba1e1b524767e06b8f0  C5 2f8a05b5d7c2fde5ec8b0ba1e1b524767e06b8f0  EQUAL: True
          apps      base 1dd43398c371aa88e16fa8aba95bead4c131c2ac  C5 1dd43398c371aa88e16fa8aba95bead4c131c2ac  EQUAL: True
          tests     base 509ecf860ffbc46db17f825af775e33a458f5274  C5 509ecf860ffbc46db17f825af775e33a458f5274  EQUAL: True
          docs      base 48fd2e4c9ffe468071e3e9dbe056db6e4e1dd792  C5 48fd2e4c9ffe468071e3e9dbe056db6e4e1dd792  EQUAL: True
          scripts   base 53331effaa68e4e30ece33a0acd66e077813b2c5  C5 53331effaa68e4e30ece33a0acd66e077813b2c5  EQUAL: True
    G6A_RC=0
    REAL_EXIT=0

    (b) python3 -m pytest tests/cli/test_golden_path.py -q
    ..........................................                               [100%]
    42 passed in 18.74s
    REAL_EXIT=0

    (c) python3 -m ruff check . --output-format concise
        tail of the transcript:
        Found 26 errors.
        [*] 25 fixable with the `--fix` option.
        REAL_EXIT=1

          rows matching ^\S+:\d+:\d+: : 26  | the ceiling tests/orchestration/test_ci_budgets.py freezes (LINT_ERROR_CEILING): 26 | EQUAL: True
          of those rows, paths lying under .remedy-wt/ (counted, not grepped): 0
          ruff REAL_EXIT was 1: the block anticipates it — the gate is the COUNT
    REAL_EXIT=0

          (d) CONSTRAINT 10, READ OFF THE FILESYSTEM
              paths matching .agent/**/*.py that exist on disk: 0 []
              the same sweep by os.walk over .agent (every depth): 0 []
              git ls-files .agent entries: 2131 | of them ending in .py: 0 []
              BOTH ARE 0: True
    REAL_EXIT=0

G6(c) RAN AFTER G3(iii) HAD REMOVED AND PRUNED ITS WORKTREE, as the gate orders. G6(d) IS
THE REPAIR CONSTRAINT 10 NAMES: it reads the FILESYSTEM and the index for a `.py` file under
`.agent/`, where the clause carried by earlier rounds counted ruff ROWS and was blind to a
clean `.py` file by construction. Both readings are 0, and the os.walk sweep beside the glob
is a second reader of the same truth.

### G7 — nothing else moved

        (a) THE SENTINEL, THE TREE AND THE WORKTREES
            .agent/STOP exists (os.path.exists): False
            .agent/STOP by glob                : []
            git status --porcelain | cat -A    : ''
            worktree: /home/decodeux/Repos/remedy  d1ee2114 [feature/f275-one-world-completion-part-three]
            number of worktrees: 1 (must be 1, the primary checkout alone)

        (b) THE CHANGED PATHS
            changed paths over 75cc221e..d1ee2114: 9
              .agent/authored/f275-r77-artefact.md
              .agent/authored/f275-r77-instrument.py.md
              .agent/authored/f275-r77.md
              .agent/decisions.md
              .agent/f275_t003_flip_residue_r77.md
              .agent/last_block.md
              .agent/live_review.md
              .agent/plan.md
              .agent/prose_slips.md
            MISSING against the Change set minus .agent/handoff.md: []
            EXTRA   against the Change set minus .agent/handoff.md: []
            changed paths under docs/, scripts/, packages/, apps/ or tests/: 0 []

        (c) THE OPEN SET, BY DISTINCT ID
            base 75cc221e  registered 109  resolved  22  OPEN  87  highest open R-0880  R-0880 open: True
            C5   d1ee2114  registered 109  resolved  22  OPEN  87  highest open R-0880  R-0880 open: True
            ids REGISTERED this round : []
            ids RESOLVED this round   : []
            ids DE-REGISTERED this round: []
            the open membership is IDENTICAL at both ends: True

    G7_RC=0
    REAL_EXIT=0

### The STOP readings constraint 7 orders

| When | `os.path.exists('.agent/STOP')` | `glob.glob('.agent/STOP')` |
|---|---|---|
| before the first commit (C0a), by `ls .agent/STOP` — see deviation 1 | n/a: `No such file or directory` | n/a |
| before C1, by both readers | `False` | `[]` |
| before C6, by both readers | `False` | `[]` |
| at G7(a), by both readers | `False` | `[]` |
| after C6 was staged, before it was committed | `True` | `['.agent/STOP']` |

THE LAST ROW IS THE ONE THAT ENDS THE SESSION. Every reading the block orders came back
absent; the sentinel appeared after all of them, while this file was being composed, and it
is recorded here at the reading that found it. See the Session section and deviation 7.

## Authored-text proofs

Four reviewer-authored texts were applied this round, all four extracted from the COMMITTED
C0a blob and checked against the sha256 carried on their own BEGIN marker BEFORE application,
per constraint 1. Neither the delegation prompt nor the scratch file was used as the source.

| Slice | target | bytes | lines | sha256 on its BEGIN marker | verified before applying | applied result |
|---|---|---|---|---|---|---|
| PLAN77 | `.agent/plan.md` (C1, whole-file replacement) | 2854 | 48 | `15263f85…2475eea9` | MATCH | disk blob byte-identical to the slice |
| RECORD77 | `.agent/live_review.md` (C2, append) | 5217 | 11 | `08535811…0e0dd4b54` | MATCH | pre + one newline + slice, exact prefix and exact suffix |
| SLIPS77 | `.agent/prose_slips.md` (C3, append) | 2840 | 5 | `eabbd72b…6bccf3a2a` | MATCH | pre + one newline + slice, exact prefix and exact suffix |
| DEC77 | `.agent/decisions.md` (C4, append) | 6614 | 17 | `18a6167d…7567b0afbc41e` | MATCH | pre + one newline + slice, exact prefix and exact suffix |

THE CARDINALITY WAS MEASURED, NOT ASSUMED: G1 counted 4 BEGIN/END slices in the committed
C0a blob and the block states no numeral for it.

The two WHOLE TEXTS were transported with `shutil.copyfile` and never opened in an editor:

| Whole text | scratch path | bytes | sha256 | committed blob |
|---|---|---|---|---|
| the artefact | `.remedy-wt/f275-r77-artefact.md` | 11738 | `bc4abd74…4a23d2f1303` | EQUAL at C0b and at C5 |
| the instrument carrier | `.remedy-wt/f275-r77-instrument.py.md` | 15578 | `bb8c3325…c35f1e1bf` | EQUAL at C0c |

The block itself travelled the same way: `.remedy-wt/f275-r77.block.md`, 39315 bytes, sha256
`a4006b534a98021d0aa4283e8328a55d9985b45c09150822b156fb52cc039e97`, verified against the
digest the delegation wrapper states BEFORE it was read for content, copied to
`.agent/authored/f275-r77.md` at C0a and to `.agent/last_block.md` at C0d, both EQUAL.

EVERY SLICE WAS APPLIED BYTE FOR BYTE. Nothing was reflowed, re-wrapped, re-indented or
corrected, and no slice looked wrong on reading.

## Deviations & assumptions

NO DEPARTURE FROM THE BLOCK'S ORDERED COMMIT SEQUENCE. All nine commits C0a through C5
landed in exactly the Bundle's order, each staging exactly ONE path, with no extra commit, no
dropped commit and no reordering; C6 is this file. Seven deviations and notes, none of them a
change to an ordered artefact:

1. **THE PRE-C0a `.agent/STOP` READING WAS TAKEN WITH `ls`, NOT WITH THE TWO READERS
   CONSTRAINT 7 NAMES.** The constraint orders the sentinel read from disk before the first
   commit by BOTH `os.path.exists` and `glob`. My reading before C0a was the state probe's
   `ls -la .agent/STOP`, which returned `ls: cannot access '.agent/STOP': No such file or
   directory` — a real read from disk, but not the two readers the constraint names. The
   two-reader reading was taken before C1 instead, and again before C6 and inside G7(a); all
   three are `False` and `[]`. The sentinel was absent at every reading, so nothing this
   round turns on it, and the deviation is in the INSTRUMENT of the first reading only.
2. **G6(c) REAL_EXIT IS 1 AND THAT IS THE ORDERED READING.** The block states it in the
   gate's own words: "Its exit is 1 whenever any finding remains, so THE GATE IS THE COUNT".
   The count is 26 against the ceiling of 26 that `tests/orchestration/test_ci_budgets.py`
   freezes through `LINT_ERROR_CEILING` in `packages/orchestration/ci_budgets.py`, and 0 of
   the 26 rows lie under `.remedy-wt/`. Reported as 1 rather than as green, per constraint 11.
3. **G4(a)'s `git show 75cc221e:…` EXIT IS 128, NOT MERELY NON-ZERO.** The gate names a
   non-zero exit as the expected reading and orders the number literally; the real number is
   128 with `fatal: path '.agent/f275_t003_flip_residue_r77.md' exists on disk, but not in
   '75cc221e'`.
4. **G5(d)'s PARTITION PREFIX COUNT IS 14 AND SECTION 8'S SUMMARY SAYS 13; THE TWO ARE
   REPORTED SIDE BY SIDE AND NOT RECONCILED, WHICH IS WHAT THE GATE ORDERS.** The excess of
   one is section 8's own explanatory line `PARTITION adds a set's own parts back to the set
   and cannot.`, which is prose and not a record. The CROSS-CHECK prefix count is 19 and the
   summary's is 19, because that prose line opens `A CROSS-CHECK`. Both counts are measured;
   neither is taken from the block. For completeness the verdict-bearing records — lines
   ending `-> MATCH` or `-> MISMATCH` — number 32, which is 19 + 13.
5. **G1 WROTE `.remedy-wt/f275-r77-instrument.py` BEFORE G5(a) DID, AND BOTH REPORT THE SAME
   BYTES.** G1's carrier round-trip has to extract the fence to test that re-wrapping
   reproduces the committed blob, so the extracted file exists before G5(a) runs; G5(a)
   re-extracts it from the same committed C0c blob and reports 15045 bytes and sha256
   `1eaaf115135989f8340b361a70cf15b735d08f681150da26b3c9dd3f546fbbdb`, identical to G1's.
   Neither gate reads the other's file as evidence.

6. **C6's OWN INSERTION COUNT IS OVER 500 AND IS EXEMPT BY NAME, STATED HERE SO IT IS NOT
   READ AS AN UNDECLARED OVERSIZE COMMIT.** This commit is the verbatim rewrite of a SINGLE
   `.agent/**` state file, `.agent/handoff.md`, which DECISION F104 D1 in AGENTS.md exempts
   ENTIRELY from the 500-insertion cap — "such a save is one indivisible artifact, so the
   churn reading is unmeetable by construction". It is the only commit of this round that is
   not under the cap, and the block itself removes it from every gate. The exact figure is
   the reviewer's to read at the next gate. Written and committed ONCE, per the write-once
   rule (PH v3).

7. **`.agent/STOP` APPEARED AFTER EVERY ORDERED READING, AND `git status --porcelain` IS
   THEREFORE NOT THE EMPTY STRING AT THE HANDBACK.** Constraint 5 requires the empty string
   at every commit and at the handback, and it WAS empty at every one of the nine commits
   C0a through C5 and at G7(a), where it is recorded literally as `''`. After C6 was staged
   the tree carries exactly one entry, `?? .agent/STOP`: an untracked zero-byte file created
   at `2026-09-12 10:03:36 +0200`, which no step of this round wrote. I did not stage it, did
   not delete it and did not commit it. Staging it would put a path outside the block's
   Change section into the round; deleting it would destroy the sentinel. Every TRACKED path
   is clean and the working tree carries no modification: the single porcelain line is the
   sentinel itself. Guardrail G6 was honoured — the commit in hand was finished, the handback
   was written, and the session ends here.

NOTHING WAS APPLIED THAT I BELIEVED WRONG. No slice looked wrong on reading; every one
matched its own BEGIN-marker digest and every one was applied byte for byte. No numeral of
the block failed to reproduce: constraint 8's TOTAL 397 and PROSE 316 both re-measure
exactly, and constraint 15's zero holds under both readings.

## Item-status table

Every ordered item — every C of the Bundle and every G of the Done-when — appears exactly
once.

| Item | Status | Reason |
|--------|----------|------------------------------|
| C0a | done | `.agent/authored/f275-r77.md`, EQUAL to the reviewer's scratch original |
| C0b | done | `.agent/authored/f275-r77-artefact.md`, EQUAL, `shutil.copyfile` |
| C0c | done | `.agent/authored/f275-r77-instrument.py.md`, EQUAL, `shutil.copyfile` |
| C0d | done | `.agent/last_block.md`, EQUAL to the COMMITTED C0a blob |
| C1 | done | `.agent/plan.md` byte-identical to PLAN77, 48 lines against the cap of 50 |
| C2 | done | `.agent/live_review.md` +12/-0, the round 76 PASS verdict booked |
| C3 | done | `.agent/prose_slips.md` +6/-0, three dated lines, no id |
| C4 | done | `.agent/decisions.md` +18/-0, deletion column 0, D50 untouched |
| C5 | done | `.agent/f275_t003_flip_residue_r77.md`, byte-identical to the C0b blob |
| C6 | done | this file |
| G1 | done | REAL_EXIT=0; four blobs EQUAL, CARDINALITY 4 slices all matching their BEGIN markers, TOTAL 397 and PROSE 316 both equal to constraint 8, 0 repeated-character lines under both readings, carrier round-trips byte for byte |
| G2 | done | REAL_EXIT=0; byte-identical to PLAN77, 48 lines, one `## Goal`, one `## Next Steps` |
| G3 | done | REAL_EXIT=0; reader A and reader B ACCEPT all three appends at N = 6, 3 and 9 counted from the slices, all three negative controls REJECTED by both readers on a byte in 0x41–0x5A/0x61–0x7A, worktree removed and pruned |
| G4 | done | REAL_EXIT=0; artefact byte-identical to the C0b blob and absent at the base at exit 128, 62 quoted lines all matched and strictly monotone, 79 prose digit runs swept with 0 unplaceable, 0 durations, every insertion under 500 |
| G5 | done | REAL_EXIT=0/0/0/0 across (a), (b), (c)+(d) and (e); byte-stable over three runs, 0 MISMATCH, 19 cross-checks and 13 partitions all holding, `EVERY CHECK HOLDS: True`, section 2 both True, section 3 13 against 0, section 6 BREAKS 0 |
| G6 | done | (a) REAL_EXIT=0, five trees EQUAL; (b) REAL_EXIT=0, 42 passed; (c) REAL_EXIT=1 by design with the counts at REAL_EXIT=0, 26 rows = ceiling 26, 0 rows under `.remedy-wt/`; (d) REAL_EXIT=0, 0 `.py` paths under `.agent/` by glob, by os.walk and in the index |
| G7 | done | REAL_EXIT=0; STOP absent by both readings, clean tree, one worktree, 9 changed paths with MISSING and EXTRA empty and 0 production paths, open set 87 and identical at both ends with `R-0880` open |

No item was skipped and no item deviated.

## Next

THE SINGLE EXPECTED NEXT ACTION IS PHASE 1 RULE 1 OF `docs/agents/self_drive_protocol.md`,
READ BEFORE RULE 2: `.agent/STOP` exists on disk, so the session writes the handoff and ends,
and does nothing else. This file IS that handoff. No new round is authored, no branch is
created, no PR is opened or merged while the sentinel stands.

WHAT IS WAITING BEHIND IT, so that removing the sentinel resumes the work rather than
re-discovers it. The reviewer reads `75cc221e`..`HEAD`, re-derives every gate above against
the committed blobs — including the numbers of the C6 commit this file could not gate — and
issues the round 77 verdict, which amend0827-process-diet rule 1 lets the next round's first
commit book. The next round's own work, which `.agent/plan.md` now carries as item 1, is to
carry the 19 surviving over-selection frames back to the ruled sites that produce them: the
corrected set does not remove those sites because the owner check REFUSES rather than decides
on their receivers, and that residue is what `R-0880`'s second obligation still names.
DECISION F275 D51 has fixed the flip's input set, so the flip itself is unblocked on its
input and still carries DECISION F275 D48's obligations as corrected by D49.

## Reviewer verdict on round 77 — appended after the handback, by the reviewer's authored text

VERDICT ROUND 77: **PASS.** Written by the planner and reviewer of SESSION 27 after reading the committed
range `75cc221e`..`8b02f1e8` and RE-DERIVING EVERY GATE INDEPENDENTLY against the committed blobs; the
worker's report was evidence for no line below. It is carried here because under
`docs/agents/self_drive_protocol.md` a verdict that stays in the session is lost, and it is booked into
`.agent/live_review.md` by the FIRST SUBSTANTIVE COMMIT of round 78, per amend0827-process-diet rule 1.

WHAT THE TRANSPORT PROOF COVERS, STATED BEFORE THE FIGURES, per item 37 of §3. G1 is the PRIMARY
cmp-against-scratchpad proof and not the §4.9 digest fallback: the chain it walks is the reviewer's own
scratch original, the committed `.agent/authored/` blob and the working copy — three artefacts, of which
the first is the reviewer's and the other two the worker's. It does not and cannot establish what bytes
the worker RECEIVED. All three authored blobs are byte-identical to the reviewer's originals — the block
at 39315 bytes, the artefact at 11738 and the instrument carrier at 15578 — and `.agent/last_block.md`
equals the committed block blob. Four slices matched the sha256 on their own BEGIN markers, the block
re-measures at 397 lines TOTAL and 316 PROSE as its constraint 8 states, and it carries zero
repeated-character lines under both the length-two and the length-one reading.

EVERY GATE HOLDS AND THE REVIEWER RE-RAN ALL SEVEN. G2: `.agent/plan.md` byte-identical to its slice at
48 lines against the cap of 50. G3: the three appends exact under reader A, reader B holding over the
whole appended region at N counted from the slice as 6, 3 and 9, and all three negative controls placed
on the FIRST appended paragraph REJECTED by both readers; C4's deletion column is ZERO, so DECISION F275
D50 is not rewritten, and the new ledger header matches the repeating format and duplicates none of the
75 already there. G4: the artefact byte-identical to the C0b blob, absent at the base at exit 128, its 62
quoted lines all present in the instrument's output with the matching monotone and nothing unmatchable,
zero quoted lines carrying a wall-clock duration and zero three-backtick lines. G5: the instrument
extracted from the COMMITTED carrier is byte-stable across three runs, reports zero MISMATCH, and every
one of its 19 cross-checks reads MATCH. G6 and G7: five top-level tree object ids identical at the base
and at C5, the canary 42 passed, `ruff check .` 26 rows against the frozen ceiling of 26, one worktree,
nine changed paths with MISSING and EXTRA both empty and zero production paths, and the open set 87 by
distinct id with identical membership at the base, at C5 and at the tip with `R-0880` open at each.

THE HANDBACK'S OWN COMMITS TABLE WAS COMPARED CELL BY CELL AGAINST `git show --numstat`, which is item
28's obligation for a value the worker writes twice, and all nine cells agree. The handback commit's own
numbers, which no gate of the round could reach, are 627 insertions and 526 deletions over
`.agent/handoff.md` alone, exempt entirely under AGENTS.md DECISION F104 D1 as the verbatim rewrite of a
single `.agent/**` state file.

THE ROUND'S SUBSTANCE IS THAT THE FLIP NOW HAS AN INPUT SET AND IT IS BETTER THAN THE ONE THE TRANSFORM
CONSUMES. The shipped owner check names 13 ruled sites whose receiver holds another record; every one of
them is among the 60 the plain re-derivation drops and none survives in the plain set, which is the
containment DECISION F275 D50 could only infer. The corrected set is the round 53 re-keyed set minus
exactly those 13, at 2185 sites, and it is that difference as a SET and not merely at that count. The
same owner check exits with 13 contradictions over the round 53 set and ZERO over the corrected one,
which is the discriminator a guard needs at both ends. Run as a third arm at the same commit against the
same control, differing in the ruled site set alone, it FIXES 23 test nodes and BREAKS NONE — a set
difference rather than a smaller total, so nothing is traded — and `Mission.job_id` and `QueueEntry.job_id`
leave the residue entirely.

AND THE LIMIT IS STATED RATHER THAN SOFTENED. 19 over-selection frames survive the corrected set, on
classes the owner check REFUSES rather than decides, which is the 277-site blind spot DECISION F275 D45
ruled acceptable showing through exactly where it said it would. `R-0880` stays OPEN for that reason and
no id was minted for the 19, per item 30. 1204 bad nodes is the best reading this chain has taken and it
is not near green.

## Authored text for round 78 to book — two dated lines for `.agent/prose_slips.md`

2026-09-12 · F275 R77 · The round 76 instrument's section 8 opens its explanatory prose with the word `PARTITION`, which is also the prefix its own partition records are keyed by, so a gate counting records by line prefix reads one more than the tool's own summary. Round 77 carried that instrument section forward unchanged and therefore carried the collision with it, and the round 77 block ordered the worker to report the prefix count and the summary count SIDE BY SIDE rather than reconciling them. That was the right call for a round whose readings did not turn on the number, and it is not a fix: the collision is still in the shipped instrument and the next instrument to carry that section inherits it. THE RULE THAT FOLLOWS: a wording defect that a block routes around by ordering two readings instead of one is recorded as still-open at the moment it is routed around, because a gate worded to tolerate a defect is the thing most likely to carry it into the next round unnoticed.

2026-09-12 · F275 R77 · The reviewer's own round 77 re-derivation script was produced from the round 76 one by textual substitution, and the substitution reached the dictionary keys it looks slices up by while missing the LABELS it prints them under: the output reads "plan.md at C1 is byte-identical to slice PLAN76" over a comparison that correctly used PLAN77, and five further labels carry the old round's slice names. No reading moved and nothing false was landed, because the labels are in reviewer scratch that no file keeps and the verdict states the measured property in its own words rather than quoting them. THE RULE THAT FOLLOWS: this is the same class as the round 75 block's bare "74" one level further out — a retarget that fixes what the code USES and not what the code SAYS — and the counter-measure is the same sweep, run over the reviewer's own tooling before its output is read, because an output line that names the wrong artefact is indistinguishable from a wrong measurement to anyone who later quotes it.

## Session 27 ends here — TWO delegated rounds, 76 and 77, both PASS, ended by `.agent/STOP` under guardrail G6

WHY THIS SESSION ENDS BELOW THE ROUND TARGET, STATED FIRST BECAUSE IT IS THE PART A LATER READER WILL
CHECK. `.agent/STOP` appeared on disk at 10:03:36 while round 77's C6 was being composed. It is a
zero-byte untracked file that no step of either round wrote. Guardrail G6 of
`docs/agents/self_drive_protocol.md` says that when it appears the current commit is finished and the
session hands off and ends, and that is exactly what happened: the worker completed C6, recorded the
sentinel with both readings, pushed, and stopped without staging, deleting or committing it. The round
target of six to eight is not cited and is not met; G6 overrides it, and the two-round count is the
sentinel's doing rather than a judgement about context, which remains comfortable. THE SENTINEL IS LEFT
EXACTLY WHERE IT IS. Removing it is the operator's call, not this session's, and `git status --porcelain`
therefore reads one line, `?? .agent/STOP`, with every tracked path clean.

WHAT THE SESSION DID. Round 76 took the flip's dry run that DECISIONs F275 D41, D42 and D44 had each
deferred by name, against the corrected inputs of rounds 67 and 69 together, in three full suite passes
at one commit differing in the ruled site set alone. It found that the plain re-derivation costs 134
additional bad test nodes — breaking 172 and fixing 38 — because it removes every production record class
`R-0880` names while introducing 231 under-selection frames the round 53 set does not have. DECISION F275
D50 ruled the flip's input to be neither set. Round 77 constructed the set that lies between them, in a
fourth suite pass, and DECISION F275 D51 rules it the flip's input: strictly better than the set the
transform consumes today, fixing 23 nodes and breaking none.

THE CONTROLS ARE WHY THOSE READINGS ARE WORTH ANYTHING. The five top-level tree object ids are identical
at `bf692757`, round 59's base, and at `ef75e213`, so round 59's run and these are comparable at all; the
994 tracked `.py` files are identical between them. The re-key stage reproduces `.remedy-wt/r69_rekeyed.json`
byte for byte. The round 53 arm reproduces round 69's own 263 files and 6091 rewrites. The unflipped
control reproduces round 59's summary to the unit, at one failure, and that failure is the node needing
the gitignored `apps/ui/node_modules`.

AND ONE GATE OF THE REVIEWER'S OWN WAS FOUND UNABLE TO FAIL AND WAS REPAIRED MID-SESSION, which is worth
more than either reading it protects. Round 76's instrument first printed only PARTITIONS — sums of a
set's own parts against that set — and a control that deleted a single `FAILED` line from a transcript
left every one of them reading MATCH. Cross-checks between independently derived numbers were added, and
the first run of them found a real defect in the instrument's own parser: the transform's rule table was
being split at a two-space gap that three of the longest rule names do not have, so three rows worth 19
rewrites were silently dropped, and only the comparison against the transform's own printed total saw it.
The same design caught a second parser defect in round 77's instrument before emission, a missing
multiline flag that read zero contradicted rows where the stage prints 13. Both were the reviewer's, both
were caught by a check built because the previous one could not fail, and both are recorded here rather
than as findings because nothing wrong ever reached disk.

THE BRANCH IS GREEN AT EVERY READING THIS SESSION TOOK. Not one line under `packages/`, `apps/`, `tests/`,
`docs/` or `scripts/` moved in either round, which each round's tree gate proves by object id rather than
by diff. The canary reads 42 passed and `ruff check .` reads 26 findings, the frozen ceiling, at the
branch tip. Every destructive run happened in a disposable worktree that was removed and pruned, and
`git worktree list` reads one entry at both verdicts. The open set is 87 by distinct id and unchanged all
session; `R-0880` is open and the next free id is `R-0881`.

## What the next session owes, in order

FIRST, Phase 1 rule 1: re-read `.agent/STOP` from disk BEFORE the Open PR Gate. It EXISTS as this session
ends, at zero bytes and untracked, and this session did not remove it. A session that finds it still there
writes the handoff and ends without a round, per G6; only the operator's removal of that file reopens the
loop. Then the Open PR Gate: no pull request is open, and none is owed until the closure sequence.

SECOND, round 78's FIRST SUBSTANTIVE COMMIT books, from this file as the durable carrier under
amend0827-process-diet rule 1, the ROUND 77 PASS verdict above as a `Gate: F275 R77` entry in
`.agent/live_review.md`, and the TWO dated lines above into `.agent/prose_slips.md`. The open set is 87 by
distinct id and the next free id is `R-0881`.

THIRD, F275 IS PAST THE SOFT LIMIT amend0908-f275-finish rule 1 names, at 77 of 60 rounds and 27 of 20
sessions. The SCOPE REPORT that rule obliges was written in round 51's handback and STANDS; nothing this
session measured changes any of its three parts, and it is not restated here because a report restated is
a report edited. Rule 2 forbids the split-and-close default BY NAME, so the next session continues.

FOURTH, THE WORK ITSELF, in the order `.agent/plan.md` now fixes. The flip's input set exists and is ruled,
so the route is open: carry the 19 surviving over-selection frames back to the ruled sites that produce
them, which the corrected set does not remove because the owner check refuses rather than decides on their
receivers — that is the residue `R-0880`'s second obligation still names, and the carry-back probe for it
was written and works. Then the resolver collapse DECISION F260 D5 places in T003, which is PRODUCTION
CODE and therefore a SPLIT round with mutation red-proofs, and which DECISION F275 D37 names as the home
of the id-SHAPE seam behind the three largest residue classes. Then THE FLIP, on the corrected set,
carrying DECISION F275 D48's two obligations as corrected by D49: the full suite is the backstop and is
read for its failures rather than its exit code, and the thin set is re-derived before the flip with any
site fallen to zero witnesses treated as a stop. Then the classic store, then the closure sequence.

SITZUNGS-LIMIT ERREICHT — OPERATOR-BERICHT IN DER ÜBERGABE
