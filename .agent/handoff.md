# Handback — F275 round 63

## Session

SESSION 24 of feature F275 · round 63 · rounds so far 63

Context self-assessment (amend0905-throughput): context is comfortable and this round was
mid-weight — `AGENTS.md`, `docs/agents/handback_template.md` and
`docs/agents/self_drive_protocol.md` were read in full, all three scratch files were verified
by size and sha256 BEFORE any of them was opened (32200, 10145 and 9733 bytes), the artefact
and the instrument were transported with `shutil.copyfile` without either `.md` ever being
opened in an editor, all FOUR slices were extracted out of the COMMITTED C0a blob with their
marker digests matching on the FIRST attempt, and the two expensive commands were the
19-second canary and the instrument run.

F275 STANDS AT 63 ROUNDS AND 24 SESSIONS against the operator's soft limit of 60 rounds and
20 sessions (amend0908-f275-finish rule 1), so both halves of that limit remain EXCEEDED. THE
SCOPE REPORT THAT RULE OBLIGES WAS WRITTEN IN ROUND 51'S HANDBACK AND IT STANDS — it is not
restated here, because a report restated is a report edited. Rule 2 forbids the
amend0905-throughput split-and-close default here BY NAME: this round closed nothing,
registered no feature and did not touch `docs/roadmap/STATUS.md`. What this round adds to the
operator's pending decision on round 51's item (c) is that the flip's three largest residue
classes are now DIAGNOSED and RULED: they are ONE id-shape seam, they are not a fourth
transform rule family, they are not a data migration, and the work that closes them is
production code in T003 — a bigger remaining step than round 51's report assumed, not a
smaller one. The candidate fourth rule was built, applied and run before this round: it fixed
16 of 263 and BROKE 2, and DECISION F275 D37 rejects it on that measurement.

SITZUNGS-LIMIT ERREICHT — OPERATOR-BERICHT IN DER ÜBERGABE

`.agent/STOP` was re-read FROM DISK before the first commit and again before C6, per
constraint 7. Both readings, literally:

    before C0a, at the base `93063ec4`:
        $ python3 -B /home/decodeux/Repos/remedy/.remedy-wt/r63_probe0.py
        STOP exists: False

    before C6, at C5 `359ab572`:
        $ bash -c 'ls -la /home/decodeux/Repos/remedy/.agent/STOP > …/stop_before_c6.out 2>&1; echo "REAL_EXIT=$?"'
        REAL_EXIT=2
        ls: cannot access '/home/decodeux/Repos/remedy/.agent/STOP': No such file or directory

The file does not exist at either reading, which is what the block's constraint 7 states of
the reviewer's base reading and what this round confirms at both ends. G7(a) measured it a
third time, after G5 had run, and read the same.

## Range

Review of `93063ec4`..`HEAD`.

## Commits

### ee4994e5 F275 R63 C0a: save the round 63 step block as an authored text.
| Path | +/- | Reason |
|------|-----|--------|
| .agent/authored/f275-r63.md | +318 / -0 | NEW. The round 63 step block saved verbatim, by `shutil.copyfile` from the scratch original verified at 32200 bytes and sha256 `1830f337…d0b3` BEFORE it was opened. |

### 9fc6271a F275 R63 C0b: save the round 63 residue artefact as an authored text.
| Path | +/- | Reason |
|------|-----|--------|
| .agent/authored/f275-r63-artefact.md | +175 / -0 | NEW. The reviewer's artefact text, copied as a WHOLE FILE with `shutil.copyfile` and never opened in an editor. |

### e9397ab1 F275 R63 C0c: save the round 63 diagnosis instrument as an authored text.
| Path | +/- | Reason |
|------|-----|--------|
| .agent/authored/f275-r63-diag.py.md | +217 / -0 | NEW. The diagnosis instrument, copied as a WHOLE FILE. Its `.md` extension is load-bearing per constraint 10 and was preserved; no runnable copy was landed anywhere in the tree, which G6(c) then measures independently at zero. |

### f9c1be2e F275 R63 C0d: mirror the round 63 block into the last-block state file.
| Path | +/- | Reason |
|------|-----|--------|
| .agent/last_block.md | +157 / -128 | The C0a blob mirrored, read back out of the commit with `git show ee4994e5:…` rather than off the scratch copy. |

### df954eea F275 R63 C1: make the plan current for round 63.
| Path | +/- | Reason |
|------|-----|--------|
| .agent/plan.md | +17 / -17 | Whole-file replacement by slice PLAN63. First SUBSTANTIVE commit, so this is where the plan becomes current, per constraint 3 and item 23 of §3. |

### d633de9c F275 R63 C2: book the reviewer round 62 verdict into the finding record.
| Path | +/- | Reason |
|------|-----|--------|
| .agent/live_review.md | +12 / -0 | Slice RECORD63 appended: the round 62 PASS verdict, booked by the first substantive commit of round 63 per amend0827-process-diet rule 1. No id registered, none resolved. |

### 86e69089 F275 R63 C3: book the two round 62 prose slips.
| Path | +/- | Reason |
|------|-----|--------|
| .agent/prose_slips.md | +4 / -0 | Slice SLIPS63 appended: the two dated lines the round 62 verdict spent, per amend0827-process-diet rule 2. Neither is an id. |

### 1252140d F275 R63 C4: record DECISION F275 D37, the id-shape seam ruling.
| Path | +/- | Reason |
|------|-----|--------|
| .agent/decisions.md | +18 / -0 | Slice DEC63 appended: DECISION F275 D37, which rules the three largest residue classes ONE id-SHAPE seam, rejects the candidate fourth rule family on its own measurement, rules out a data migration by probe, and places the work in T003's resolver collapse. |

### 359ab572 F275 R63 C5: land the round 63 residue diagnosis artefact.
| Path | +/- | Reason |
|------|-----|--------|
| .agent/f275_t003_flip_residue_r63.md | +175 / -0 | NEW. A byte-identical copy of the C0b blob. |

### C6 — the handoff commit (self-reference, R-0149 pattern)
| Path | +/- | Reason |
|------|-----|--------|
| .agent/handoff.md | see next round | This file. A handoff cannot table the commit that writes it; its `--numstat` numbers are recorded by the reviewer at the next gate, exactly as G7(d) states. |

Every `+/-` above is taken from `git show --numstat <sha>` and from no other source.

## External actions

| Action | Outcome |
|--------|---------|
| `git push -u origin feature/f275-one-world-completion-part-three` | run AFTER this file was committed; the transcript cannot appear inside the file it postdates, and the reviewer reads it from the round report and from `git log origin/feature/f275-one-world-completion-part-three`. |

No `gh` command was run. No pull request was created, edited or merged. No `remedy` CLI
command was run. NO `git worktree` WAS CREATED OR REMOVED by this round — `git worktree list`
shows the primary checkout alone, which is what constraint 4 fixes. Nothing was written to
`/tmp`; all scratch lives under the gitignored `.remedy-wt/`. The one thing this round wrote
outside the change set is the synthetic store constraint 12 names: the instrument created
`.remedy-wt/r63_store`, printed `the synthetic store was removed`, and G7(a)'s porcelain
reading taken AFTER that run is the empty string.

## Verification

Seven gates, each run for real as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`, every one of them at
a commit STRICTLY EARLIER than C6. One line per gate with its REAL exit code first, then the
readings each gate ordered.

| Gate | REAL exit | Reading |
|------|-----------|---------|
| G1 TRANSPORT | 0 | all four EQUAL; 4 slices; TOTAL 318 / BODY 76 / PROSE 242, agreeing with constraint 8; neither numeral over 490 or 400 |
| G2 THE PLAN | 0 | plan.md @C1 byte-identical to PLAN63 at 2669 bytes; 45 lines under the cap of 50; both headings exactly 1 |
| G3 THE RECORD | 0 | all three appends exact under READER A and READER B, at N=6, N=2 and N=9; all three negative controls rejected by both readers while all three unmutated regions are accepted; (iv)–(vii) all hold |
| G4 THE ARTEFACT AND THE INSTRUMENT | 0 (comparison), 128 (absence probe, by design) | artefact @C5 byte-identical to the C0b blob at 10145 bytes; base path does not resolve; 175 and 217 lines under the 500 cap |
| G5 THE INSTRUMENT | 0 (fence extraction), 0 (instrument run) | 1 ```python fence; (a) 337 / 223 / 90 and every frame and stderr row AGREE; (b) all four claims hold; (c) 105, 75 over 39 scopes in 18 files, 58, `load_job` 29 AGREE; (d) 1345 / 263 / 249 and FIXED 16 / BROKE 2 / 247 AGREE — **the control's "exit 0" is NOT printed by the instrument and is reported ABSENT, see deviation 6** |
| G6 THE TREE DID NOT MOVE | 0 (a), 0 (b), 1 (c, by design — the gate is the COUNT) | five trees EQUAL; canary 42 passed; ruff 26 rows at the frozen ceiling, 0 under `.remedy-wt/`, 0 `.py` under `.agent/` |
| G7 NOTHING ELSE MOVED | 0 | STOP absent; `status --porcelain` the empty string; 9 changed paths, MISSING and EXTRA both empty, 0 production paths; open set 88 at both ends; max insertions 318 |

### G1 TRANSPORT — REAL_EXIT=0

    $ bash -c 'python3 -B /home/decodeux/Repos/remedy/.remedy-wt/r63_g1.py > …/g1.out 2>&1; echo "REAL_EXIT=$?"'
    REAL_EXIT=0

    A: committed ee4994e5:.agent/authored/f275-r63.md 32200 bytes 1830f337…d0b3
    A: scratch .remedy-wt/f275-r63.block.md 32200 bytes 1830f337…d0b3
    A: EQUAL True
    B: committed 9fc6271a:.agent/authored/f275-r63-artefact.md 10145 bytes 5622ba36…90a0
    B: scratch .remedy-wt/f275-r63-artefact.md 10145 bytes 5622ba36…90a0
    B: EQUAL True
    C: committed e9397ab1:.agent/authored/f275-r63-diag.py.md 9733 bytes 7667fb82…bbde
    C: scratch .remedy-wt/f275-r63-diag.py.md 9733 bytes 7667fb82…bbde
    C: EQUAL True
    D: committed f9c1be2e:.agent/last_block.md 32200 bytes 1830f337…d0b3
    D: C0a blob 32200 bytes 1830f337…d0b3
    D: EQUAL True

All four verdicts are EQUAL. The full digests are in the Authored-text proofs table below.

Block budget, RE-MEASURED on the COMMITTED C0a blob rather than on the scratch copy:

    slice PLAN63 body lines 45 bytes 2669 BEGIN-marker sha256 MATCH True
    slice RECORD63 body lines 11 bytes 4653 BEGIN-marker sha256 MATCH True
    slice SLIPS63 body lines 3 bytes 1962 BEGIN-marker sha256 MATCH True
    slice DEC63 body lines 17 bytes 5539 BEGIN-marker sha256 MATCH True
    slice cardinality (the extraction is the sweep): 4 ['PLAN63', 'RECORD63', 'SLIPS63', 'DEC63']
    TOTAL lines 318
    summed slice BODY lines 76
    PROSE 242
    TOTAL > 490 : False
    PROSE > 400 : False
    constraint 8 states TOTAL 318 PROSE 242 -> agree: True

THE TWO NUMERALS AGREE WITH CONSTRAINT 8 EXACTLY: 318 TOTAL and 242 PROSE, measured as TOTAL
minus the summed 76 body lines of the four slices. The block states no count of its own
slices and the extraction is the sweep: its cardinality is FOUR.

### G2 THE PLAN — REAL_EXIT=0

    $ bash -c 'python3 -B /home/decodeux/Repos/remedy/.remedy-wt/r63_g2.py > …/g2.out 2>&1; echo "REAL_EXIT=$?"'
    REAL_EXIT=0

    plan.md @C1 df954eea : 2669 af9865be58706c0d668c9b81de0a260f14474ce871de5ada5844baee17e8fc11
    slice PLAN63         : 2669 af9865be58706c0d668c9b81de0a260f14474ce871de5ada5844baee17e8fc11
    BYTE-IDENTICAL: True
    line count: 45 AGENTS.md cap 50 -> under cap
    count of ^## Goal$      : 1 must be 1 -> True
    count of ^## Next Steps$: 1 must be 1 -> True

### G3 THE RECORD — REAL_EXIT=0

    $ bash -c 'python3 -B /home/decodeux/Repos/remedy/.remedy-wt/r63_g3.py > …/g3.out 2>&1; echo "REAL_EXIT=$?"'
    REAL_EXIT=0

    === C2 .agent/live_review.md slice RECORD63
     (i)  READER A: pre 996190 post 1000844 delta 4654 slice body bytes 4653 -> ACCEPT True
     (ii) READER B: N counted from slice = 6 -> ACCEPT True
     (iii) NEGATIVE CONTROL
       mutation: paragraph 1 byte offset 0 'G' -> 'B'
       reader A on mutated: False (must be False)
       reader B on mutated: False (must be False)
       reader A on unmutated: True (must be True)
       reader B on unmutated: True (must be True)
    === C3 .agent/prose_slips.md slice SLIPS63
     (i)  READER A: pre 253122 post 255085 delta 1963 slice body bytes 1962 -> ACCEPT True
     (ii) READER B: N counted from slice = 2 -> ACCEPT True
     (iii) NEGATIVE CONTROL
       mutation: paragraph 1 byte offset 14 'F' -> 'B'
       reader A on mutated: False (must be False)
       reader B on mutated: False (must be False)
       reader A on unmutated: True (must be True)
       reader B on unmutated: True (must be True)
    === C4 .agent/decisions.md slice DEC63
     (i)  READER A: pre 1130791 post 1136331 delta 5540 slice body bytes 5539 -> ACCEPT True
     (ii) READER B: N counted from slice = 9 -> ACCEPT True
     (iii) NEGATIVE CONTROL
       mutation: paragraph 1 byte offset 3 'D' -> 'B'
       reader A on mutated: False (must be False)
       reader B on mutated: False (must be False)
       reader A on unmutated: True (must be True)
       reader B on unmutated: True (must be True)

The three PRE sizes are exactly the three the block states: 996190 at the base, 253122 at C2
and 1130791 at C3. The three deltas are 4654, 1963 and 5540, each the slice body plus the one
inserted newline. READER A is a BYTE reader (`post == pre + b"\n" + body`); READER B is
structural and independent of it (the last N blank-line-separated units of the WHOLE
post-commit file equal the slice's N units, in order, N COUNTED from the slice — the block
states none of the three, and the counted values are 6, 2 and 9). Each negative control flips
exactly one byte `b` with `b < 128 and chr(b).isalpha()` inside the FIRST appended paragraph;
all three are rejected by both readers and all three unmutated regions are accepted, so
neither reader is a reader that rejects everything.

    === (iv) RECORD63 interior-line ban
    interior lines starting with any banned prefix: 0 must be 0
    ^- R- lines: pre 110 post 110 ADDED 0
    ^Done: R- lines: pre 23 post 23 ADDED 0

    === (v) the Gate heading
    RECORD63 first line: Gate: F275 R62 — the F275 round 62 entry. VERDICT PASS. Written by the planner and reviewer of session 23 after reading the committed range `7910aa7d`..`79129f58` and RE-DERIVING EVERY GATE INDEPENDEN…
    lines in .agent/live_review.md at 93063ec4 matching the pattern: 61
    new first line matches the pattern: True
    new first line duplicates none of them: True

    === (vi) DEC63 heading
    DEC63 begins '## DECISION F275 D37 ': True
    lines at base matching ^## DECISION F275 D37: 0 must be 0
    existing ^## DECISION F275 D\d+ headings at base: 36 highest: 36

    === (vii) SLIPS63 datelines
    SLIPS63 paragraphs: 2 all begin with the prefix: True
    lines at 93063ec4 beginning with that exact prefix: 0
    lines at C3: 2 ADDED by C3: 2

The count of lines already matching `^Gate: F275 R\d+ — the F275 round \d+ entry\.` at
`93063ec4` is 61 — the block states none and this is the measured value. The highest existing
`^## DECISION F275 D\d+` heading at the base is D36, of 36 such headings, so D37 is the next
number and not a collision. The base carries ZERO lines beginning `2026-09-11 · F275 R62 · `
and C3 adds exactly 2.

### G4 THE ARTEFACT AND THE INSTRUMENT — REAL_EXIT=0, absence probe REAL_EXIT=128

    $ bash -c 'python3 -B /home/decodeux/Repos/remedy/.remedy-wt/r63_g4.py > …/g4.out 2>&1; echo "REAL_EXIT=$?"'
    REAL_EXIT=0

    C5 .agent/f275_t003_flip_residue_r63.md: 10145 5622ba36421b88c7b6cea5870eb2ea54a7ad78f7b61cb7c68a24f686e05490a0
    C0b .agent/authored/f275-r63-artefact.md: 10145 5622ba36421b88c7b6cea5870eb2ea54a7ad78f7b61cb7c68a24f686e05490a0
    BYTE-IDENTICAL: True
    git show 93063ec4:.agent/f275_t003_flip_residue_r63.md exit: 128 non-zero: True
      stderr: fatal: path '.agent/f275_t003_flip_residue_r63.md' exists on disk, but not in '93063ec4'
    artefact line count: 175 vs DECISION F104 D1 cap 500 -> True
    instrument blob line count: 217 vs cap 500 -> True

The absence probe was ALSO run standalone, redirected to a file per constraint 11 and never
piped into `tail`:

    $ bash -c 'git show 93063ec4:.agent/f275_t003_flip_residue_r63.md > …/g4_absent.out 2>&1; echo "REAL_EXIT=$?"'
    REAL_EXIT=128

128 is non-zero, which is what the gate requires.

### G5 THE ARTEFACT'S NUMBERS, RE-DERIVED FROM THE COMMITTED INSTRUMENT

The instrument was extracted from the COMMITTED C0c blob's ```python fence and run:

    $ bash -c 'python3 -B /home/decodeux/Repos/remedy/.remedy-wt/r63_g5_extract.py > …/g5_extract.out 2>&1; echo "REAL_EXIT=$?"'
    REAL_EXIT=0
    ```python fences found: 1
    fenced source bytes: 9450 724406604a988dc889f810917f852fca2d1430a513f1dd3f2c062b705bfa32bc

    $ bash -c 'python3 -B /home/decodeux/Repos/remedy/.remedy-wt/r63_diag_extracted.py > …/g5.out 2>&1; echo "REAL_EXIT=$?"'
    REAL_EXIT=0

FENCES FOUND: 1. Every reading below was taken by `grep`-ing the instrument's OUTPUT for the
token the gate names, in `.remedy-wt/r63_g5_read.py`, rather than by reading around it.

(a) BANNER 1. The three `E-lines` counts, literally:

    E-lines paired: 1173
      SystemExit               E-lines  337
      hexadecimal UUID         E-lines  223
      unsupported operand /    E-lines   90

Every line beginning `frame ` that the banner prints beneath them, literally:

          frame   193  packages/orchestration/data_paths.py:324
          frame    47  apps/cli/commands/brain.py:24
          frame   136  <no frame>:0
          frame    87  /usr/lib/python3.10/uuid.py:177
          frame    90  packages/orchestration/data_paths.py:200

Every line beginning `stderr `, literally:

          stderr  180  no job matches prefix 'X'  [arg=16hex]
          stderr  123  invalid job ID: 'X'  [arg=16hex]
          stderr   13  no job matches prefix 'X'  [arg=8hex]
          stderr  123  invalid job ID: 'X'  [arg=16hex]

| Artefact section 2 states | Instrument printed | Agrees |
|---|---|---|
| SystemExit 337 | 337 | yes |
| hexadecimal UUID 223 | 223 | yes |
| unsupported operand 90 | 90 | yes |
| 193 at `data_paths.py:324` | `frame 193 packages/orchestration/data_paths.py:324` | yes |
| 87 at `uuid.py:177` | `frame 87 /usr/lib/python3.10/uuid.py:177` | yes |
| 90 at `data_paths.py:200` | `frame 90 packages/orchestration/data_paths.py:200` | yes |
| the three stderr rows 180, 123, 13 | 180, 123, 13 under SystemExit | yes |

ALL AGREE. The banner prints two frame rows per class where it has them, so two rows appear
that the artefact does not state: `frame 47 apps/cli/commands/brain.py:24` as the second
SystemExit frame, and `frame 136 <no frame>:0` as the FIRST hexadecimal-UUID frame — 136 of
the 223 E-lines of that class have no frame the instrument could attribute. Those are extra
readings, not disagreements, and they are reported as printed. The fourth `stderr 123` row is
the hexadecimal-UUID class's own and is the same 123 `invalid job ID` captures seen from the
other side.

(b) BANNER 2 AND BANNER 2b, every line literally:

    === 2. THE MECHANISM, reproduced by calling the shipped functions ===
    mint_job_id() len 16 hyphens 0 | str(uuid4()) len 36 hyphens 4
      UUID(mint_job_id()) -> ValueError: badly formed hexadecimal UUID string
      job_dir(UUID, root) -> TypeError: unsupported operand type(s) for /: 'PosixPath' and 'UUID'
      load_job_plan(UUID, root) -> TypeError: unsupported operand type(s) for /: 'PosixPath' and 'UUID'
      JobPlan(job_id=uuid4()).job_id is a UUID — the dataclass does not coerce
      CONTROL job_dir(minted, root) -> /nonexistent-probe-root/jobs/6cff9df409d54735
      CONTROL load_job_plan(minted, root) -> None

    === 2b. THE RESOLVER, run against a store holding BOTH shapes ===
      classic 8-hex prefix   classic finds it  task []        resolve_job_id -> returns the canonical id
      unified 8-hex prefix   classic []        task finds it  resolve_job_id -> SystemExit: 1
      unified WHOLE id       classic []        task finds it  resolve_job_id -> SystemExit: 1
      the synthetic store was removed

The four claims sections 3 and 4 rest on, each checked against that output:

1. `UUID(mint_job_id())` raises `badly formed hexadecimal UUID string` — HOLDS, one grep hit.
2. `job_dir` and `load_job_plan` each raise `unsupported operand type(s) for /: 'PosixPath'
   and 'UUID'` — HOLDS, two grep hits, one per function.
3. The CONTROL lines beneath them SUCCEED — HOLDS. They are compared by RETURNED-rather-than-
   RAISED, not byte for byte, because each carries a freshly minted id: `job_dir` returned
   `/nonexistent-probe-root/jobs/6cff9df409d54735` and `load_job_plan` returned `None`.
   Neither is an exception line; the instrument prints `SUCCEEDED — class does not reproduce`
   on that path and printed it nowhere.
4. The unified record's WHOLE id still reads `resolve_job_id -> SystemExit: 1` while `task
   finds it` on the SAME row — HOLDS. `grep 'task finds it'` and `grep 'resolve_job_id ->
   SystemExit: 1'` each return the same two rows, the `unified 8-hex prefix` row and the
   `unified WHOLE id` row.

Two stray `Error: no job matches prefix '2e3d2949'` / `'2e3d2949c6144763'` lines appear at the
TOP of the redirected file. They are the handler's own unbuffered stderr from the two failing
`resolve_job_id` calls in banner 2b, interleaved ahead of buffered stdout by the redirect; they
are not a fifth banner and nothing in the gate names them. Reported so the reviewer is not
surprised by them.

(c) BANNER 3:

    every `UUID(...)` call: 105
    sites that BIND a UUID and pass it on: 75 over 39 scopes in 18 files
      under apps/cli/: 58   outside it: 17

Every line beginning `callee `, literally:

      callee   29  load_job
      callee   14  load_run_events
      callee   12  str
      callee    9  _emit
        callee    9  _emit
        callee    3  load_job
        callee    2  load_job_safe
        callee    2  str
        callee    1  finalize_test_outcome

The first four are the whole-set tally; the last five are the same tally restricted to the
sites OUTSIDE `apps/cli/`. The artefact's section 7 states 105, 75 over 39 scopes in 18 files,
58 and 17, and `load_job` at 29 — ALL FIVE AGREE, exactly as printed.

(d) BANNER 4, the three run rows literally:

    control    1345 passed in 225.24s (0:03:45)           ids    0  SystemExit   0  hexUUID   0  operand   0
    flipped    263 failed, 1082 passed in 201.73s (0:03:21) ids  263  SystemExit  62  hexUUID   3  operand  17
    candidate  249 failed, 1096 passed in 201.10s (0:03:21) ids  249  SystemExit  52  hexUUID   1  operand  16
    the candidate rule FIXED 16 and BROKE 2; 247 survive
      BROKE  tests/cli/test_context_inspect_cli.py::test_handler_invalid_job_id
      BROKE  tests/cli/test_propose_cli.py::TestProposeMaterializeHandler::test_materialize_non_approved_fails

| Artefact section 6 states | Instrument printed | Agrees |
|---|---|---|
| control 1345 passed | `1345 passed in 225.24s` | yes |
| control at exit 0 | nothing — no run row carries an exit code | **ABSENT, see deviation 6** |
| flipped 263 failed | `263 failed, 1082 passed` | yes |
| candidate 249 failed | `249 failed, 1096 passed` | yes |
| FIXED 16 / BROKE 2 / 247 surviving | `FIXED 16 and BROKE 2; 247 survive` | yes |

NOT ONE FIGURE THE INSTRUMENT PRINTED DISAGREES WITH THE ARTEFACT. One figure the artefact
states is NOT printed by the instrument — the control run's exit code — and it is reported as
ABSENT rather than supplied from elsewhere, which is what G5's closing paragraph orders. It is
not one of the two readings the artefact's own PROVENANCE paragraph declares are outside the
instrument (those two are section 5's seam diff and section 6's "49 calls in 17 files"), so it
is owed here and is reported as missing. Deviation 6 states it in full.

### G6 THE TREE DID NOT MOVE — REAL_EXIT=0 (a), 0 (b), 1 (c, by design)

(a) The five subtree object ids, at `93063ec4` and at C5 `359ab572`:

    $ bash -c 'python3 -B /home/decodeux/Repos/remedy/.remedy-wt/r63_g6a.py > …/g6a.out 2>&1; echo "REAL_EXIT=$?"'
    REAL_EXIT=0

    packages  93063ec4 2f8a05b5d7c2fde5ec8b0ba1e1b524767e06b8f0  C5 359ab572 2f8a05b5d7c2fde5ec8b0ba1e1b524767e06b8f0  EQUAL True
    apps      93063ec4 1dd43398c371aa88e16fa8aba95bead4c131c2ac  C5 359ab572 1dd43398c371aa88e16fa8aba95bead4c131c2ac  EQUAL True
    tests     93063ec4 509ecf860ffbc46db17f825af775e33a458f5274  C5 359ab572 509ecf860ffbc46db17f825af775e33a458f5274  EQUAL True
    docs      93063ec4 48fd2e4c9ffe468071e3e9dbe056db6e4e1dd792  C5 359ab572 48fd2e4c9ffe468071e3e9dbe056db6e4e1dd792  EQUAL True
    scripts   93063ec4 53331effaa68e4e30ece33a0acd66e077813b2c5  C5 359ab572 53331effaa68e4e30ece33a0acd66e077813b2c5  EQUAL True
    ALL FIVE EQUAL: True

ALL FIVE EQUAL. Not one line under `packages/`, `apps/`, `tests/`, `docs/` or `scripts/`
moved, which is the Goal's own condition.

(b) THE CANARY, redirected to a file per constraint 11 and never piped into `tail`:

    $ bash -c 'python3 -m pytest tests/cli/test_golden_path.py -q > …/g6b.out 2>&1; echo "REAL_EXIT=$?"'
    REAL_EXIT=0
    ..........................................                               [100%]
    42 passed in 18.77s

42 passed at exit 0, which is the base reading.

(c) RUFF. The command exits 1 whenever any finding remains, so the GATE IS THE COUNT:

    $ bash -c 'python3 -m ruff check . --output-format concise > …/g6c.out 2>&1; echo "REAL_EXIT=$?"'
    REAL_EXIT=1
    $ bash -c 'python3 -B /home/decodeux/Repos/remedy/.remedy-wt/r63_g6c.py > …/g6c_count.out 2>&1; echo "REAL_EXIT=$?"'
    REAL_EXIT=0
    rows matching ^\S+:\d+:\d+: -> 26 ceiling 26 -> True
    rows under .remedy-wt/ -> 0
    rows whose path ends .py under .agent/ -> 0
    (non-row lines) Found 26 errors.
    (non-row lines) [*] 25 fixable with the `--fix` option.

26 rows, exactly the ceiling `tests/orchestration/test_ci_budgets.py` freezes. ZERO rows under
`.remedy-wt/` and ZERO rows whose path ends `.py` under `.agent/` — the second is what
constraint 10 exists to protect, and both were counted by a Python matcher rather than by
`grep -c`, precisely because the expected answer is zero. The 26 rows are 20 `I001`, 4 `F401`
plus `UP035` and `F821`, all pre-existing under `packages/`, `scripts/` and `tests/`; no line
of any of them was edited.

### G7 NOTHING ELSE MOVED — REAL_EXIT=0

Taken AFTER G5 had run, per the block's own instruction in G7(a).

    $ bash -c 'python3 -B /home/decodeux/Repos/remedy/.remedy-wt/r63_g7.py > …/g7.out 2>&1; echo "REAL_EXIT=$?"'
    REAL_EXIT=0

    === G7(a)
    .agent/STOP exists on disk: False (must be absent)
    git status --porcelain exit: 0 raw bytes: 0
    git status --porcelain | cat -A  ->  literal output between the arrows:
    >>><<<
    is the empty string: True
    git worktree list (exit 0):
    /home/decodeux/Repos/remedy  359ab572 [feature/f275-one-world-completion-part-three]
    worktrees CREATED by this round: 0 ; worktrees REMOVED by this round: 0

`cat -A` printed NOTHING between the arrows — the porcelain status is the empty string, with
no trailing `$` and no invisible byte of any kind, which is why it is read through `cat -A` at
all. This is the reading that proves constraint 12's synthetic store left the tree alone. The
worktree list is REPORTED and not gated: THIS ROUND CREATED NO WORKTREE AND REMOVED NONE —
neither, which is what constraint 4 fixes.

    === G7(b)
    changed paths 93063ec4..C5: 9
        .agent/authored/f275-r63-artefact.md
        .agent/authored/f275-r63-diag.py.md
        .agent/authored/f275-r63.md
        .agent/decisions.md
        .agent/f275_t003_flip_residue_r63.md
        .agent/last_block.md
        .agent/live_review.md
        .agent/plan.md
        .agent/prose_slips.md
    MISSING: []
    EXTRA  : []
    paths under docs/ scripts/ packages/ apps/ tests/: 0 []

    === G7(c) the open set BY DISTINCT ID
    base 93063ec4: registered paragraphs 109 Done lines 21 OPEN by distinct id 88
    C5   359ab572: registered paragraphs 109 Done lines 21 OPEN by distinct id 88
    ids REGISTERED this round: []
    ids RESOLVED this round: []
    ids DE-REGISTERED this round: []
    highest id in the record at base: R-0880  at C5: R-0880

    === G7(d) per-commit insertions
    C0a ee4994e5  +318  -0  under the 500 cap: True
    C0b 9fc6271a  +175  -0  under the 500 cap: True
    C0c e9397ab1  +217  -0  under the 500 cap: True
    C0d f9c1be2e  +157  -128  under the 500 cap: True
    C1 df954eea  +17  -17  under the 500 cap: True
    C2 d633de9c  +12  -0  under the 500 cap: True
    C3 86e69089  +4  -0  under the 500 cap: True
    C4 1252140d  +18  -0  under the 500 cap: True
    C5 359ab572  +175  -0  under the 500 cap: True
    maximum insertions over C0a..C5: 318 cap 500 -> True

The open set reads 88 BY DISTINCT ID at both ends, and the COUNT is not the whole gate — the
MEMBERSHIP is, so the registered, resolved and de-registered sets are each printed and each is
EMPTY. The highest id in the record is `R-0880` at both ends. F275's single declared-oversize
allowance is STILL UNSPENT at 63 rounds: the maximum insertion count over C0a..C5 is 318, well
under the DECISION F104 D1 cap of 500. C6's own numbers are not stated here — they cannot
exist while C6 is being written, and G7(d) says so.

## Authored-text proofs

Disk-to-disk comparison against the committed `.agent/authored/` files, per the fidelity
protocol in docs/agents/split_workflow.md. This is the PRIMARY cmp-against-scratchpad proof
and not the §4.9 digest fallback — the reviewer's scratch originals were still on disk and
were compared directly.

| Authored text | Committed blob | Size | sha256 | Verdict |
|---------------|----------------|------|--------|---------|
| the step block | `.agent/authored/f275-r63.md` @ee4994e5 | 32200 | `1830f3370336cebddba0101fca89840f3bc44042b703a829c6a849327478d0b3` | EQUAL to `.remedy-wt/f275-r63.block.md` |
| the artefact | `.agent/authored/f275-r63-artefact.md` @9fc6271a | 10145 | `5622ba36421b88c7b6cea5870eb2ea54a7ad78f7b61cb7c68a24f686e05490a0` | EQUAL to `.remedy-wt/f275-r63-artefact.md` |
| the instrument | `.agent/authored/f275-r63-diag.py.md` @e9397ab1 | 9733 | `7667fb82fe2aef259c9c29f072e59f0ffa61533ae5ec851de4c6285b6a86bbde` | EQUAL to `.remedy-wt/f275-r63-diag.py.md` |
| the block mirror | `.agent/last_block.md` @f9c1be2e | 32200 | `1830f3370336cebddba0101fca89840f3bc44042b703a829c6a849327478d0b3` | EQUAL to the C0a blob |
| the landed artefact | `.agent/f275_t003_flip_residue_r63.md` @359ab572 | 10145 | `5622ba36421b88c7b6cea5870eb2ea54a7ad78f7b61cb7c68a24f686e05490a0` | EQUAL to the C0b blob |

All three scratch files were verified by SIZE AND SHA256 BEFORE being opened or copied. The
artefact and the instrument were transported with `shutil.copyfile` and NEITHER `.md` WAS EVER
OPENED IN AN EDITOR, as constraint 2 orders — which is why this handback quotes not one line
of the artefact's prose. The two artefact readings quoted above (its PROVENANCE paragraph and
its section 6 exit-code claim) were taken by a script that greps the COMMITTED blob and prints
what it matched, which is a measurement rather than an editor read; deviation 7 states it.

| Slice | Body bytes | Body lines | Marker sha256 | Extracted from | Applied to |
|-------|-----------|-----------|---------------|----------------|------------|
| PLAN63 | 2669 | 45 | `af9865be…fc11` MATCH | the COMMITTED C0a blob | `.agent/plan.md` @df954eea, byte-identical |
| RECORD63 | 4653 | 11 | `67b689f5…5f83` MATCH | the COMMITTED C0a blob | `.agent/live_review.md` @d633de9c, appended |
| SLIPS63 | 1962 | 3 | `586a5703…620c` MATCH | the COMMITTED C0a blob | `.agent/prose_slips.md` @86e69089, appended |
| DEC63 | 5539 | 17 | `c16b1a0d…f688` MATCH | the COMMITTED C0a blob | `.agent/decisions.md` @1252140d, appended |

All four slices were extracted by `BEGIN-`/`END-` marker-line prefix with the marker lines
EXCLUDED, out of the COMMITTED C0a blob — never from the prompt, never from the scratch copy,
never from memory. All four marker digests matched on the FIRST attempt, because constraint 2
states the body convention outright: the body runs from the start of the line after BEGIN to
the first byte of the END line, INCLUDING the body's terminal newline. All four were applied
BYTE FOR BYTE with no reflow, correction, improvement or re-indent.

## Item status

Every ordered item of this round — each commit C and each gate G — appears exactly once.

| Item | Status | Reason |
|------|--------|--------|
| C0a save the block as `.agent/authored/f275-r63.md` | done | |
| C0b save the artefact as `.agent/authored/f275-r63-artefact.md` | done | |
| C0c save the instrument as `.agent/authored/f275-r63-diag.py.md` | done | |
| C0d mirror the C0a blob into `.agent/last_block.md` | done | |
| C1 `.agent/plan.md` <- PLAN63, whole-file replacement | done | |
| C2 `.agent/live_review.md` <- RECORD63 appended | done | |
| C3 `.agent/prose_slips.md` <- SLIPS63 appended | done | |
| C4 `.agent/decisions.md` <- DEC63 appended | done | |
| C5 `.agent/f275_t003_flip_residue_r63.md` <- copy of the C0b blob | done | |
| C6 `.agent/handoff.md` rewritten — the handback | done | this file |
| G1 TRANSPORT | done | all four EQUAL; 4 slices; TOTAL 318 / PROSE 242, agreeing with constraint 8 |
| G2 THE PLAN | done | byte-identical at 2669 bytes; 45 lines; both headings exactly 1 |
| G3 THE RECORD | done | (i)–(vii) all hold; N=6, 2 and 9; all three negative controls reject and all three unmutated regions are accepted |
| G4 THE ARTEFACT AND THE INSTRUMENT | done | byte-identical at 10145 bytes; absence probe 128; 175 and 217 lines under the 500 cap |
| G5 THE INSTRUMENT | deviated | (a), (b) and (c) agree with the artefact in full and (d) agrees on four of its five figures; the FIFTH — the control run's exit 0 — is NOT printed by the instrument anywhere and is reported ABSENT rather than supplied from elsewhere. Deviation 6. |
| G6 THE TREE DID NOT MOVE | done | five trees EQUAL; canary 42 passed at exit 0; ruff 26 rows at ceiling, 0 and 0 |
| G7 NOTHING ELSE MOVED | done | (a)–(d) all hold; 9 changed paths; open set 88 at both ends with all three sets empty; max insertions 318 |

No item was skipped. Every gate was run for real; none was reported without its command having
been executed, and the word "green" appears as a reading nowhere in this handback.

## Deviations & assumptions

THE BLOCK'S ORDERED COMMIT SEQUENCE WAS FOLLOWED EXACTLY: C0a, C0b, C0c, C0d, C1, C2, C3, C4,
C5, C6 — ten commits, in that order, none added, none dropped, none reordered. The Change
section's path set was honoured exactly, with MISSING and EXTRA both empty. No slice was
altered by one byte and this round has no disagreement with any of the four to record.

1. **`.agent/plan.md` names round 62 across C0a–C0d.** Sustained and ordered. Constraint 3
   fixes the commit order and states this consequence explicitly: the plan becomes current at
   C1, the first SUBSTANTIVE commit, which is what item 23 of §3 requires of a round touching
   the finding ledger. Not a defect; recorded because a reader auditing the intermediate
   commits would otherwise see a stale plan and wonder.
2. **`python3 -m ruff check .` exits 1.** Sustained and by design. Ruff exits non-zero whenever
   any finding remains, and the block states that the GATE IS THE COUNT. The count is 26, at
   the frozen ceiling. No line was edited to change it.
3. **G4's absence probe exits 128.** Sustained and standing. Non-zero is what the gate
   requires and 128 is non-zero; the path does not resolve at `93063ec4`.
4. **C5 copied the artefact from the clean working-tree path, not from `git show` output.**
   Declared because the two orders had to be reconciled: C5 says "a copy of the C0b blob" while
   constraint 2 says the artefact is transported with `shutil.copyfile` and never opened in an
   editor. The script first PROVED the working-tree file at
   `.agent/authored/f275-r63-artefact.md` byte-equal to the committed C0b blob (10145 bytes,
   sha256 `5622ba36…90a0`, asserted in code), then used `shutil.copyfile` on it. G4 re-checks
   the landed result against the committed C0b blob independently and reads BYTE-IDENTICAL, so
   the reconciliation costs the gate nothing. This is rounds 61 and 62's declared route, kept.
5. **Every gate was written to a file under `.remedy-wt/` and run as `python3 -B <file>`.**
   The shell on this machine refuses loops, `$(...)` substitution and `$?` inside a compound
   command BY FORM — one such command was rejected outright at the first probe of this round
   and was immediately re-expressed as a script — so each gate was saved to disk and run from
   there, exactly as the environment notes direct. Nothing was written to `/tmp`. This is
   method, not a departure from any gate's meaning: every command reported above is the command
   that actually ran.
6. **G5(d): THE ARTEFACT STATES THE CONTROL RUN IS "A REAL EXIT 0" AND THE COMMITTED INSTRUMENT
   PRINTS NO EXIT CODE FOR ANY OF ITS THREE RUNS — REPORTED AS ABSENT, NOT SUPPLIED FROM
   ELSEWHERE.** The artefact's section 6 carries an exit-code column reading `0` for the
   control and the sentence "THE CONTROL IS A REAL EXIT 0 AT 1345 PASSED". The instrument's
   banner 4 reads each run's LOG and prints the last line matching `\d+ (passed|failed)`
   together with its own per-class counts; it never reads or prints a process exit code, and
   `grep` over its whole output returns no exit-code reading on any of the three rows — only
   the substring `SystemExit`, which is a class label. G5's closing paragraph orders exactly
   this handling for a figure the instrument does not print, and it is NOT one of the two the
   artefact's own PROVENANCE paragraph excuses (those are section 5's seam diff and section
   6's "49 calls in 17 files"). NOTHING WAS RECONCILED IN EITHER DIRECTION: the instrument was
   run unmodified, no other source was consulted for that figure, and the artefact was not
   touched. The other four figures of section 6 — 1345 passed, 263 failed, 249 failed, and
   FIXED 16 / BROKE 2 / 247 surviving — all agree exactly as printed, so the substance of the
   candidate rule's negative result is fully re-derived; what is missing is only the control's
   exit code.
7. **The COMMITTED artefact blob was grepped by script, twice.** Constraint 2 forbids opening
   the artefact and the instrument in an editor; neither `.md` was ever opened, and both were
   transported by `shutil.copyfile` before anything else happened to them. Two later readings
   were taken by scripts that run `git show` on the COMMITTED blob and print only the matched
   region: its PROVENANCE paragraph, needed to decide whether the missing exit code is one of
   the two declared absences G5 excuses, and its two lines containing `exit 0` / `1345`, needed
   to state deviation 6 accurately rather than from memory. Both happened AFTER G1 proved
   transport and neither changed a byte.
8. **The EXTRACTED scratch copy of the instrument was read.** The fenced source that G5 orders
   extracted and run was read at `.remedy-wt/r63_diag_extracted.py` before it was run — to
   establish what it writes, since constraint 12 warns it creates a store, and to confirm the
   four log files it reads were on disk. That is a gitignored scratch artefact produced by the
   gate G5 itself orders, it is not the committed `.md`, and it was not modified: the file that
   ran is byte-for-byte the fence from the committed C0c blob, sha256 `72440660…32bc`.
9. **The instrument's banner 2b emitted two lines on stderr.** `Error: no job matches prefix
   '2e3d2949'` and `…'2e3d2949c6144763'` appear at the TOP of the redirected output file, ahead
   of banner 1, because stderr is unbuffered and stdout is not. They are the shipped handler's
   own diagnostics from the two `resolve_job_id` calls the banner deliberately makes fail. No
   gate names them; they are declared so the reviewer's own run is not surprised by them.

NO PIPE INTO `tail` WAS USED ANYWHERE THIS ROUND. Constraint 11 exists because round 60's
worker hit that masking on the canary and had to re-run it; this round redirected the canary,
ruff, the instrument and every gate script to files on their first invocation, so no gate's
exit code here is a pipeline's exit code. The single pipe in the whole round is G7(a)'s
`git status --porcelain | cat -A`, which the block itself orders and whose exit code is not
reported — it was run as two `subprocess` calls precisely so the porcelain command's own exit
code (0) and its raw byte count (0) could be read separately from `cat`'s.

ASSUMPTIONS. The ten commits C0a–C6 and their SHAs are as tabled above; the short SHAs were
read back from `git log` and `git show --numstat` rather than predicted. No assumption was made
about any slice's content: all four were verified against their own marker digests. No
assumption was made about the instrument's figures: every one of them was re-derived by
running it and then grepped out of its output by the token the gate names.

NO FINDING ID WAS REGISTERED AND NONE WAS RESOLVED, which is what constraint 9 requires of this
round: registered, resolved and de-registered are all EMPTY sets and the open set reads 88 by
distinct id at both ends. The two lines SLIPS63 adds to `.agent/prose_slips.md` are NOT ids,
per operator amendment amend0827-process-diet rule 2, and G3(iv) measures that C2 added zero
`^- R-` and zero `^Done: R-` lines.

## Next

The reviewer reads the range `93063ec4`..`HEAD`, re-derives the seven gates independently
against the committed blobs, records C6's own `--numstat` insertions which no gate of this
round could reach, and rules on the one declared item: G5(d)'s missing exit-code reading —
whether the artefact's section 6 should lose the exit-code column, or the instrument should
gain it. The next substantive step is Next Step 1 of the plan, which DECISION F275 D37 now
names as the home of both halves of the seam: the resolver collapse DECISION F260 D5 places in
T003 — one resolver that reaches both stores, and the handler layer routed through it instead
of through `UUID(...)`. That is PRODUCTION CODE, so it is a SPLIT round with mutation
red-proofs, and D37 orders it BEFORE the flip. DECISION F275 D36 independently forbids the flip
commit until the 39 at-risk sites are resolved pair by pair or the site set is re-derived with
a column in its key.
