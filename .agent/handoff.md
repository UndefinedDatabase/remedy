# Handback — F272 round 21

## Session

SESSION 10 of feature F272 · round 21 · rounds so far 21

Soft limit under amend0906-triage-throughput: 12 sessions and 40 rounds. At
session 10 and round 21 the feature is INSIDE the limit, so no scope report is
owed and no `SITZUNGS-LIMIT` line is emitted.

Context self-assessment: comfortable. The round read AGENTS.md, the handback
template, the 401-line block, the widened guard, both smoke sections and the
four pair targets in full, and still had room to run every gate plus a
counterfactual measurement in a disposable worktree.

## Range

Review of `5f4f0405`..`0e660a50`

## Commits

Five commits, every one single-parent, in the block's ordered sequence
C0a, C0b, C1, C2, C3. C4 writes this file and cannot table itself.

### 3885b14d f272: save the round 21 step block verbatim  (C0a)
| Path | +/- | Reason |
|------|-----|--------|
| .agent/authored/f272-r21.md | +401 / -0 | `shutil.copyfile` of the delivered block, byte for byte |

### db46f137 f272: mirror the round 21 block into the last-block slot  (C0b)
| Path | +/- | Reason |
|------|-----|--------|
| .agent/last_block.md | +294 / -356 | `shutil.copyfile` of the same bytes over round 20's block |

### a1742194 f272: point the plan at the operator-facing half of R-0823  (C1)
| Path | +/- | Reason |
|------|-----|--------|
| .agent/plan.md | +26 / -23 | replaced byte for byte with PLANF272R21 |

### c1034332 f272: book the round 20 PASS verdict and resolve R-0823  (C2)
| Path | +/- | Reason |
|------|-----|--------|
| .agent/live_review.md | +4 / -0 | RECORDR21 appended: the `Gate: F272 R20` entry and the `Done: R-0823` resolution |

### 0e660a50 f272: widen the advertisement guard to scripts and operator docs  (C3)
| Path | +/- | Reason |
|------|-----|--------|
| tests/cli/test_advertised_commands.py | +61 / -3 | WIDENSPEC W1-W5: second collector over the operator-facing corpus, one new zero-gate, docstring sentence, `tests/` exclusion comment |
| scripts/remedy_smoke.sh | +0 / -87 | SMOKESPEC S1/S2: sections `12h` and `12ae` deleted in full |
| docs/system/architecture.md | +14 / -9 | pairs P3 and P4 |
| docs/system/core-product-spine-v0.md | +2 / -2 | pairs P1 and P2 |
| tests/test_remedy_smoke_script.py | +6 / -29 | DEVIATION 2 — the four text-presence guards for the deleted smoke section `12h`, replaced by a comment recording the deletion |

Per-commit insertions from `git diff --numstat <parent> <commit>`, compared cell
for cell against the table above: 401, 294, 26, 4 and 83 for C0a through C3 —
each under the DECISION F104 D1 cap of 500. C3's 83 is 14 + 2 + 0 + 61 + 6.

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C0a | done | `.agent/authored/f272-r21.md`, one sha with the delivered file |
| C0b | done | `.agent/last_block.md`, the same bytes |
| C1 | done | `.agent/plan.md` byte-equal to PLANF272R21, 2538 bytes, 48 lines |
| C2 | done | RECORDR21 appended; every one of G2's six counts reproduced exactly |
| C3 | deviated | applied as written, and the block's own P3 TO makes G4, G5 and G6 unmeetable — see DEVIATION 3. Two further deviations, 1 and 2, are recorded below |
| C4 | done | this file |

## External actions

| Action | Outcome |
|--------|---------|
| `git worktree add --detach .remedy-wt/g4wt 0e660a50` | EXIT 0, detached HEAD at `0e660a50` |
| `git worktree remove --force .remedy-wt/g4wt` | EXIT 0; `git worktree list` back to the primary plus the twelve pre-existing `remedy/job-*` |
| `git push -u origin feature/f272-one-world-completion` | issued after C4; outcome in the round report |

No PR was created, none merged, nothing force-pushed, and no work touched `main`.

## Verification

Every gate was run as `bash -c '<cmd>; echo "REAL_EXIT=$?"'` with no pipe between
the command and the echo; where a transcript was needed the output was redirected
to a scratch file rather than piped, so the reported code is the command's own.

| Gate | REAL_EXIT | Result |
|------|-----------|--------|
| G1 TRANSPORT | 0 | PASS |
| G2 THE RECORD | 0 | PASS |
| G3 THE PLAN | 0 | PASS |
| G4 THE WIDENED GUARD | (i) 1, (ii) 0, (iii) 1, (iv) 1 | FAIL — (i) and (iv) were ordered EXIT 0, and (iii) names one path more than ordered |
| G5 THE SWEEPS | 1, 0, 0, 0, 0 | FAIL on the first suite only |
| G6 SHELL + STRING | `bash -n` 0; sweep 0 | FAIL — `scripts/` is 0 as ordered, `docs/system/` is 1, not 0 |
| G7 RUFF | 0 | PASS |
| G8 THE TREE | 0 | PASS |

Every one of the three failures is the SAME byte string, introduced by the
block's own P3 TO. DEVIATION 3 below carries the measurement.

### G1 TRANSPORT — EXIT 0

    .remedy-wt/f272-r21-block.md   27279 bytes   401 lines   784455aab97960fca16aeecb89830a862b91f8f3f362b1c70b63c1e6867c05e1
    .agent/authored/f272-r21.md    27279 bytes   401 lines   784455aab97960fca16aeecb89830a862b91f8f3f362b1c70b63c1e6867c05e1
    .agent/last_block.md           27279 bytes   401 lines   784455aab97960fca16aeecb89830a862b91f8f3f362b1c70b63c1e6867c05e1
    ONE_SHA_ACROSS_ALL_THREE: True

The digest was verified against the one stated in the delegation BEFORE the file
was read or copied. Per §3 item 37 this chain covers those three artefacts and
is not a claim about the bytes emitted into a prompt.

### G2 THE RECORD — EXIT 0

    (a) BYTE
    pre_len               1180176
    pre_sha256            a8a4a67b628e6cf2ec9dda440965beaab39a8b0fd099422d6b0a661804c73b3c
    pre_tail12            b'satisfy it.\n'
    pre_trailing_nl_run   1
    post_len              1186986
    post_sha256           57d68efac9db84febae0f91c4b5aaeb8973f4e08f93733c6ce2afb9aa0371ccf
    post_tail12           b'st of T004.\n'
    post_trailing_nl_run  1
    slice_len             6809
    PRE_IS_BYTE_EXACT_PREFIX_OF_POST True
    POST_EQUALS_PRE_NL_SLICE         True

The pre-image reproduces the block's stated 1180176 bytes and its stated sha256
exactly.

    (b) STRUCTURAL
    N_counted_from_slice  2      (counted by the script from the slice, not read from the block)
    units_before          721
    units_after           723
    LAST_N_EQUAL_IN_ORDER True
    EVERYTHING_BEFORE_UNCHANGED True

    (c) NEGATIVE CONTROL, in memory only
    flipped_byte_index    1180182  inside_first_appended_paragraph True
    BYTE_READER_REJECTS   True
    STRUCT_READER_REJECTS True
    BOTH_READERS_ACCEPT_REAL True
    DISK_UNMOVED_AFTER_CONTROL True 57d68efac9db84febae0f91c4b5aaeb8973f4e08f93733c6ce2afb9aa0371ccf

    (d) COUNTS, each measured, none adjusted to agree
    ^- R-\d{4} distinct        307 -> 307    (ordered 307 -> 307)
    ^Done: R-\d{4} distinct    249 -> 250    (ordered 249 -> 250)
    ^Gate:                      43 -> 44     (ordered 43 -> 44)
    ^Gate: F272 R20              0 -> 1      (ordered 0 -> 1)
    ^Done: R-0823                0 -> 1      (ordered 0 -> 1)

    OPEN FINDINGS BY DISTINCT ID
      pre : 307 registered - 249 distinct resolved = 58
      post: 307 registered - 250 distinct resolved = 57

All six ordered readings reproduce. No id was minted this round; R-0824 stays
free.

### G3 THE PLAN — EXIT 0

    plan_bytes       2538
    plan_lines       48 against the AGENTS.md cap of 50
    BYTE_EQUAL_TO_PLANF272R21: True  95a8013c7b2f952d8f6c0d5b8f9016eb436aa5025087405ce89ade7e28b3c0ff
    HAS_##_Goal      : True
    HAS_##_Next_Steps: True

### G4 THE WIDENED GUARD — FAIL, in a disposable worktree detached at C3

Setup, all of it measured rather than assumed:

    worktree path                       /home/decodeux/Repos/remedy/.remedy-wt/g4wt   (detached at 0e660a50)
    __pycache__ dirs before the first run   0
    __pycache__ dirs after the last run     0
    python3 -B throughout                   yes
    catalog __file__  /home/decodeux/Repos/remedy/.remedy-wt/g4wt/apps/cli/command_catalog.py
    guard   __file__  /home/decodeux/Repos/remedy/.remedy-wt/g4wt/tests/cli/test_advertised_commands.py
    REPO_ROOT         /home/decodeux/Repos/remedy/.remedy-wt/g4wt

An editable install DOES exist and DOES point at the primary checkout — from a
neutral cwd, `import apps.cli.command_catalog` resolves to
`/home/decodeux/Repos/remedy/apps/cli/command_catalog.py`. Run from inside the
worktree it does not shadow, because the cwd precedes site-packages on
`sys.path`; the three readings above are the proof, taken inside the worktree
with no explicit path insertion.

    (i) CONTROL FIRST
    cd .remedy-wt/g4wt && python3 -B -m pytest tests/cli/test_advertised_commands.py -q -p no:randomly
    REAL_EXIT=1        ORDERED: 0
    1 failed, 4 passed in 0.30s
    E  an operator-facing script or page advertises commands the catalog does not carry:
    E    docs/system/architecture.md:927: remedy job run-loop

    (ii) REVERT EXACTLY ONE LINE — P1's TO back to P1's FROM
    occurrences of P1 TO before revert: 1        (asserted before writing)
    after revert: P1 TO x0  P1 FROM x1
    bytes changed: 6599 -> 6582

    (iii) THE MUTATED RUN
    REAL_EXIT=1        ORDERED: 1
    1 failed, 4 passed in 0.34s
    full unresolved list the assertion printed:
      docs/system/architecture.md:927: remedy job run-loop
      docs/system/core-product-spine-v0.md:36: remedy approval summary
    ORDERED: core-product-spine-v0.md AND NO OTHER PATH. It names one more.

    (iv) RESTORE AND RE-RUN
    restored: P1 TO x1  P1 FROM x0
    BYTE_IDENTICAL_TO_PRIMARY_AT_C3: True  726d651e23e22ce35d82b7c90a4585485d393d0007314344bf86dc73b6d59466
    REAL_EXIT=1        ORDERED: 0
    1 failed, 4 passed in 0.35s

    removal command: git worktree remove --force /home/decodeux/Repos/remedy/.remedy-wt/g4wt   (EXIT 0)

THE MUTATION DISCRIMINATOR STILL HOLDS. Comparing (i) with (iii), the reverted
line adds `docs/system/core-product-spine-v0.md:36` to the unresolved list and
nothing else, and (iv) removes it again. The guard therefore does reach P1's
site and does discriminate on it. What it also reports, in all four runs alike,
is P3 TO's own prose — see DEVIATION 3 and the counterfactual below.

COUNTERFACTUAL, run in the same disposable worktree and NEVER on disk in the
primary checkout, to isolate the blocker. P3 TO's prose line was respelled from

    The execution loop `remedy job run-loop <job_id>` was DELETED at F272 round 19.

to

    The execution loop `job run-loop` was DELETED at F272 round 19.

and the ordered colour was run again, unchanged in every other respect:

    control : REAL_EXIT=0   5 passed in 0.33s
    mutated : REAL_EXIT=1   1 failed, 4 passed
              docs/system/core-product-spine-v0.md:36: remedy approval summary
              — that path AND NO OTHER, exactly as G4 (iii) ordered
    restored: REAL_EXIT=0   5 passed in 0.33s

Every figure the block predicted for G4 is reproduced once, and only once, P3
TO's own spelling is out of the corpus. The widening, the corpus, the
discriminator and the four pairs are all sound; the single blocker is fifteen
characters of the block's own replacement text.

### G5 THE SWEEPS — FAIL on the first suite only, primary checkout at C3, serial

    python3 -B -m pytest tests/cli/test_advertised_commands.py -q -p no:randomly   REAL_EXIT=1   1 failed, 4 passed in 0.35s
    python3 -B -m pytest tests/cli/test_product_spine.py -q -p no:randomly         REAL_EXIT=0   72 passed in 0.34s
    python3 -B -m pytest tests/test_remedy_smoke_script.py -q -p no:randomly       REAL_EXIT=0   191 passed in 0.53s
    python3 -B -m pytest tests/docs/ -q -p no:randomly                             REAL_EXIT=0   303 passed in 0.59s
    python3 -B -m pytest tests/cli/test_golden_path.py -q -p no:randomly           REAL_EXIT=0   42 passed in 22.80s

The single failure is the new zero-gate, on `docs/system/architecture.md:927`.

Collector counts, PRINTED and not asserted from the block:

    production .py collector : 738 advertisements, 0 unresolved
    operator-facing collector: 404 advertisements, 1 unresolved
       docs/system/architecture.md:927: remedy job run-loop

738 is the block's base-commit figure exactly. The operator-facing 404 closes
against the block's base reading of 88 + 318 = 406: the smoke deletion removed
the two `remedy job run-loop` invocations from `scripts/` (88 -> 86), and the
doc trees are unchanged at 318, because P1, P3 and P4 each replaced one
advertisement with one advertisement and P2's two cells carry no `remedy `
prefix and never matched. 86 + 318 = 404.

`tests/test_remedy_smoke_script.py` was 195 passed before C3 and is 191 after —
the four deleted guards, and no other movement.

### G6 THE SHELL STILL PARSES AND THE COMMAND IS GONE — FAIL

    bash -n scripts/remedy_smoke.sh        REAL_EXIT=0

Repository-wide count of the string `remedy job run-loop`, enumerated from
`git ls-files` and excluding the path prefixes `.agent/`, `.data/` and
`docs/roadmap/`:

    docs/system/architecture.md              x1
    tests/cli/test_advertised_commands.py    x1
    tests/test_remedy_smoke_script.py        x1
    TOTAL 3
    count in scripts/     : 0     ORDERED: 0   MET
    count in docs/system/ : 1     ORDERED: 0   NOT MET

The one occurrence in `docs/system/` is P3 TO's prose. The two in `tests/` are
this feature's own guard prose, in a corpus both collectors deliberately exclude.

    before C3: 2818 lines, 75 _SMOKE_SECTION= assignments
    after  C3: 2731 lines, 73 _SMOKE_SECTION= assignments
    lines removed: 87
    assignment FALL: 2  (ordered: exactly 2)   MET
    12h  present after C3: False
    12ae present after C3: False
    12g  present after C3: True
    12i  present after C3: True
    12ad present after C3: True
    12af present after C3: True

The four neighbours are listed to show that the sections bracketing the two
deletions survive intact, which is what DEVIATION 1 turns on.

### G7 RUFF — EXIT 0

    python3 -m ruff check tests/cli/test_advertised_commands.py    REAL_EXIT=0   All checks passed!

A second `.py` was touched, so a second reading is owed and was taken:

    python3 -m ruff check tests/test_remedy_smoke_script.py        REAL_EXIT=0   All checks passed!

### G8 THE TREE — EXIT 0

`git status --porcelain` was EMPTY at every commit boundary; the real output was
empty each time, printed after C0a, C0b, C1, C2 and C3.

    git ls-files .remedy-wt      (empty)      REAL_EXIT=0

    .agent/STOP readings, all three by os.path.exists:
      before C0a  False
      before C3   False
      before C4   False

## Authored-text proofs

Every slice was extracted PROGRAMMATICALLY from the committed
`.agent/authored/f272-r21.md`, between its `<<<BEGIN NAME>>>` and
`<<<END NAME>>>` lines, inclusive of the newline ending the last content line.
Nothing was retyped.

| Slice | Bytes | Disk-to-disk result |
|-------|-------|---------------------|
| PLANF272R21 | 2538 | `.agent/plan.md` byte-equal, sha256 `95a8013c7b2f952d8f6c0d5b8f9016eb436aa5025087405ce89ade7e28b3c0ff` |
| RECORDR21 | 6809 | `post == pre + NL + slice` TRUE; last 2 units equal the slice's 2 paragraphs in order |
| P1 FROM / TO | 58 / 75 | pre FROM x1 TO x0, post FROM x0 TO x1, `TO contains FROM: false` |
| P2 FROM / TO | 79 / 93 | pre FROM x1 TO x0, post FROM x0 TO x1, `TO contains FROM: false` |
| P3 FROM / TO | 941 / 1093 | pre FROM x1 TO x0, post FROM x0 TO x1, `TO contains FROM: false` |
| P4 FROM / TO | 79 / 75 | pre FROM x1 TO x0, post FROM x0 TO x1, `TO contains FROM: false` |

Every one of the block's constraint-4 readings reproduced on measurement before
any pair was written. All four pairs landed byte-exact.

## Deviations & assumptions

### DEVIATION 1 — SMOKESPEC's end-bound contradicts SMOKESPEC's own S4

S1 and S2 place each section's START at its banner comment — the rule line above
`# 12h. …`, and the line `# Step 68: Autonomy Loop`. Both then place the END at
"the last line before the next `_SMOKE_SECTION=` assignment". Read literally,
that end-bound swallows the NEXT section's banner as well, because a banner sits
above its own assignment. Measured at `5f4f0405`:

    section 12h : banner 1170-1172, assignment 1173, body to 1238, blank 1239,
                  section 12i's banner 1240-1242, assignment 1243
    section 12ae: banner 1872,      assignment 1873, body to 1887, blank 1888,
                  section 12af's banner 1889-1891, assignment 1892

The literal end-bound is 1242 and 1891, which deletes the banners of sections
12i and 12af. That contradicts S4, "Nothing else in the script changes", and it
contradicts SMOKESPEC's own opening sentence, "Delete section `12h` and section
`12ae` in full" — deleting the next section's banner is deleting more than the
named section. No application can satisfy both clauses.

APPLIED: banner-to-banner, 1170-1239 and 1872-1888, 70 + 17 = 87 lines. Each
deleted span ends at the blank separator, so the surviving neighbour keeps its
banner and the file keeps the blank-line spacing it had before. G6 confirms 12i,
12ad, 12af and 12g all survive and that the assignment count falls by exactly 2,
which is the figure G6 itself ordered — and which the literal reading would also
have produced, so the assignment count alone does not discriminate between the
two readings. The banner survival does.

The spans were determined BY READING the file for S1's and S2's anchors, per S3.
Each anchor was asserted UNIQUE, the assignment line following it was asserted to
be the expected one, and the reviewer's line numbers were then confirmed against
the located spans rather than used to slice.

### DEVIATION 2 — one path outside the change set, forced by measurement

`tests/test_remedy_smoke_script.py` is not in the block's change set. Deleting
smoke section `12h` turned three of its tests red, measured immediately after the
SMOKESPEC edit and before anything else:

    python3 -B -m pytest tests/test_remedy_smoke_script.py -q -p no:randomly
    REAL_EXIT=1    3 failed, 192 passed in 0.39s
    FAILED TestSmokeScriptText::test_smoke_has_agent_loop_schema_check
    FAILED TestSmokeScriptText::test_smoke_checks_agent_loop_required_meta_keys
    FAILED TestSmokeScriptText::test_smoke_checks_no_agent_loop_task_exit

All three are text-presence guards over the smoke script, grouped in the file
under the banner `# --- Step 46.2: Agent loop run-log schema (step 12h) ---`, and
all three pin strings that existed ONLY inside the section the block ordered
deleted. The change-set clause forbids the alternative in terms: "Do not weaken a
test or an assertion to stay inside the list."

APPLIED: the whole four-test group and its banner were deleted, and a comment
recording the deletion and its reason put in their place. The fourth test,
`test_smoke_checks_agent_loop_forbidden_strings`, was GREEN after the deletion
and is not forced by the measurement — it survives only incidentally, because
`stdout`, `stderr`, `raw_output` and `Traceback` appear elsewhere in a
2731-line script. It was removed with the other three because a guard that
pins strings into a section that no longer exists is a stale advertisement, which
is the exact class this feature is removing; leaving it under a banner naming a
deleted section would have re-created the defect in the guard file itself. That
fourth removal is the judgement call in this deviation and the reviewer may
reverse it; the other three are forced.

No test was weakened and no assertion was relaxed. Nothing guards smoke section
`12ae`: `autonomy_level` is pinned only by the two `step 12a` run-contract tests,
which still pass.

### DEVIATION 3 — the block contradicts itself: P3 TO re-introduces the string every gate forbids

This is the load-bearing one. P3 TO's third line reads

    The execution loop `remedy job run-loop <job_id>` was DELETED at F272 round 19.

That sentence contains `remedy job run-loop`, and the tail after the pair is
` <job_id>` — whose first non-space character is `<`, a member of the shipped
`_COMMAND_TAIL_CHARS`. Round 20's `scan_advertised_commands`, which WIDENSPEC W1
leaves untouched, therefore reads it as an advertisement of the pair
`("job", "run-loop")`, which the catalog does not carry. Measured on P3 TO's
bytes BEFORE the pair was applied, by importing the shipped scanner:

    line 1: remedy dev agent-loop   IN_CATALOG=True
    line 3: remedy job run-loop     IN_CATALOG=False
       >>> UNRESOLVED, text: 'The execution loop `remedy job run-loop <job_id>` was DELETED at F272 round 19.'

Consequences, all three measured after the pair was applied:

- G4 (i) and (iv) were ordered EXIT 0 and are EXIT 1.
- G4 (iii) was ordered to name `core-product-spine-v0.md` AND NO OTHER PATH; it
  names `architecture.md:927` as well.
- G5's first suite was ordered EXIT 0 and is EXIT 1.
- G6 was ordered `remedy job run-loop` count 0 in `docs/system/`; it is 1.

APPLIED AS WRITTEN, per constraint 1 and per the standing order that a declared
deviation is a correct outcome and a silent correction is not. P3 TO went to disk
byte-exact; nothing was reworded to make a gate green. The counterfactual under
G4 above shows, in the disposable worktree only, that respelling that one clause
turns every ordered figure green exactly as the block predicted — so the fix is a
wording change to P3 TO and nothing structural. The reviewer rules on the
wording; a worker choosing it silently is precisely what the rule forbids.

Note for whoever authors that wording: the discriminator is the `remedy ` prefix,
not the command name. Measured after C3, the only two surviving `job run-loop`
strings in the swept corpus are

    docs/guides/simple-operator-quickstart-v0.md:108  | `job run-loop <id>` | `mission run <run_id> --job-id <id>` |
    docs/system/architecture.md:927                   The execution loop `remedy job run-loop <job_id>` was DELETED …

and only the second is flagged, because only the second carries `remedy `. The
first is the migration-table row the block's own "NOT FLAGGED, AND CORRECTLY SO"
paragraph names, and it survives untouched, as intended. P3 TO's own table rows
no longer name the command at all — they read `no live emitter`.

### ASSUMPTIONS

1. "Delete the section in full" means banner-to-banner, ending at the blank
   separator before the next section's banner. See DEVIATION 1 for the
   measurement that forced the reading.
2. W2's corpus is `git ls-files` over `scripts` filtered to `.sh`, and over
   `docs/system` and `docs/guides` filtered to `.md` — three enumerations, one
   shared sweep. It reproduces the block's own 15 files / 88 advertisements and
   88 files / 318 advertisements at the base commit, exactly, including all four
   unresolved sites. That reproduction is the evidence the reading is the
   intended one.
3. W3's anti-blindness floor is `seen > 100` over the COMBINED corpus, matching
   the shape of the existing production zero-gate rather than one floor per
   directory. The block's "the combined figure clears that floor with room"
   states the combined reading.
4. W5's constraint is enforced by construction and stated in a comment beside
   `_OPERATOR_FACING_ROOTS`: neither collector reaches `tests/`. G6 shows why it
   matters — `remedy job run-loop` appears twice under `tests/`, both times in
   this feature's own guard prose.
5. G6's "excluding `.agent/`, `.data/` and `docs/roadmap/`" was read as path
   prefixes over the tracked file list, not as a directory-name match anywhere in
   a path.
6. The counterfactual respelling under G4 is EVIDENCE ONLY. It was applied inside
   the disposable worktree, never in the primary checkout, and the worktree was
   removed by exact path afterwards. `git status --porcelain` is empty and
   `git ls-files .remedy-wt` is empty.

7. AGENTS.md "If Blocked" asks for the blocker in `.agent/plan.md`, while G3
   pins that file byte-equal to PLANF272R21 and constraint 1 forbids editing a
   slice. G3 wins and `.agent/plan.md` was left byte-equal. The blocker lives in
   this handback instead, which under amend0827-process-diet rule 1 is a durable
   carrier once committed and pushed.

No other departure from the block's ordered commit sequence occurred: five
commits in the order C0a, C0b, C1, C2, C3, then C4, no extra commit, none
dropped, none reordered.

## Next

The reviewer rules on DEVIATION 3 — the wording of P3 TO — and on DEVIATION 2's
fourth test removal. Once P3 TO's prose no longer spells `remedy job run-loop`
with a command-shaped tail, G4, G5 and G6 go green with no other change, as the
counterfactual measured.
