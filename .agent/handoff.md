# Handback — F275 round 78

## Session

`SESSION 28 of feature F275 · round 78 · rounds so far 78`

NO SCOPE REPORT AND NO SESSION-LIMIT BANNER IS OWED. The amend0911-f275-to-scope paragraph this
round restores lifts F275's soft limit of 20 sessions and 60 rounds without a replacement number,
and DECISION amend0911-feedback D8 in `.agent/decisions.md` binds it on this branch already; so
the round prints no `SITZUNGS-LIMIT` line and owes no scope report.

Context self-assessment: this worker ran one round and has ample context left; nothing about the
session boundary is forced by this round.

## Range

Review of `e262f420`..`HEAD` (the seven commits C0a–C6 plus this handback commit C7).

## Commits

### fd33d98f F275 R78 C0a: save the round 78 step block as authored text

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f275-r78.md` | +347 / -0 | the block transported with `shutil.copyfile`, byte-identical to `.remedy-wt/r78_block.md` |

### 2da9b410 F275 R78 C0b: mirror the round 78 block into the last-block state file

| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +276 / -326 | verbatim rewrite of a single `.agent/` state file from the COMMITTED C0a blob |

### 6e488a9f F275 R78 C1: make the plan current for round 78

| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +24 / -24 | slice PLAN78, the first substantive commit, before the ledger moves |

### 951ceeb3 F275 R78 C2: book the round 77 verdict and register R-0881

| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +6 / -0 | slice RECORD78 appended: the round 77 PASS, its stated limit, and the `R-0881` registration |

### 77f01074 F275 R78 C3: append the round 77 prose slips

| Path | +/- | Reason |
|---|---|---|
| `.agent/prose_slips.md` | +4 / -0 | the two dated lines EXTRACTED from `b916c1a1:.agent/handoff.md`, not typed |

### 391eb79e F275 R78 C4: restore the amend0911-feedback paragraphs lost in the merge

| Path | +/- | Reason |
|---|---|---|
| `docs/agents/self_drive_protocol.md` | +66 / -0 | the round's substance: a blank line plus the 65 lines DERIVED from `d0aa833b`, inserted after the amend0908 paragraph |

### 2b301c50 F275 R78 C5: record DECISION F275 D52

| Path | +/- | Reason |
|---|---|---|
| `.agent/decisions.md` | +16 / -0 | slice DEC78: the derivation, the placement and the two-round-trip proof |

### 77a564aa F275 R78 C6: resolve R-0881

| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +2 / -0 | slice DONE78 appended, after C4 landed |

### the handback commit C7 — `.agent/handoff.md`

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | not tabled | a handoff cannot table the commit that writes it (R-0149 pattern); G8 does not cover C7 either, per item 14 |

### The cell-by-cell comparison the block's Handback section orders

Each `+/-` cell above was read from `git show --numstat <sha>` and compared against the
corresponding line of the G8 transcript `.remedy-wt/r78_g8.txt`. Printed:

    C0a fd33d98f  table +347 / -0     G8 +347 / -0     MATCH
    C0b 2da9b410  table +276 / -326   G8 +276 / -326   MATCH
    C1  6e488a9f  table +24  / -24    G8 +24  / -24    MATCH
    C2  951ceeb3  table +6   / -0     G8 +6   / -0     MATCH
    C3  77f01074  table +4   / -0     G8 +4   / -0     MATCH
    C4  391eb79e  table +66  / -0     G8 +66  / -0     MATCH
    C5  2b301c50  table +16  / -0     G8 +16  / -0     MATCH
    C6  77a564aa  table +2   / -0     G8 +2   / -0     MATCH

Eight commits compared, eight MATCH, zero mismatch. Every commit stages exactly one path, and
the largest insertion count is 347, under the 500 cap.

## External actions

- `git push -u origin feature/f275-one-world-completion-part-three` — run after C7, outcome in
  the round report.
- No `gh` command. No `remedy` command. No pull request created, edited or merged. No branch
  created or deleted. No merge, no force-push, no history rewrite.
- No `git worktree add` and no `git worktree remove`: the negative controls of G3 and G4 mutate
  byte strings IN MEMORY and write no file, so guardrail G5 is not engaged by this round at all
  (block constraint 10).

## Verification

One line per gate, with the REAL exit code read back out of the gate's own transcript file under
`.remedy-wt/` (block constraint 9).

| Gate | Command / script | Transcript | EXIT |
|---|---|---|---|
| G1 transport, block budget, insertion cap | `python3 -B .remedy-wt/r78_g1.py` | `.remedy-wt/r78_g1.txt` | 0 |
| G2 the plan | `python3 -B .remedy-wt/r78_g2.py` | `.remedy-wt/r78_g2.txt` | 0 |
| G3 the record, with full forensics | `python3 -B .remedy-wt/r78_g3.py` | `.remedy-wt/r78_g3.txt` | 0 |
| G4 the restore | `python3 -B .remedy-wt/r78_g4.py` | `.remedy-wt/r78_g4.txt` | 0 |
| G5 the prose slips | `python3 -B .remedy-wt/r78_g5.py` | `.remedy-wt/r78_g5.txt` | 0 |
| G6(a) at BASE | `python3 -B -m pytest tests/test_agent_tooling.py -q` | `.remedy-wt/r78_g6a_base.txt` | 0 |
| G6(a) at C4 | `python3 -B -m pytest tests/test_agent_tooling.py -q` | `.remedy-wt/r78_g6a_c4.txt` | 0 |
| G6(b) at C4 | `python3 -B -m pytest tests/docs/ -q` | `.remedy-wt/r78_g6b_c4.txt` | 0 |
| G6(c) THE CANARY at C6 | `python3 -B -m pytest tests/cli/test_golden_path.py -q` | `.remedy-wt/r78_g6c_c6.txt` | 0 |
| G6(d) at C6 | `ruff check .` | `.remedy-wt/r78_g6d_c6.txt` | 1 |
| G7 tree, path set, open set | `python3 -B .remedy-wt/r78_g7.py` | `.remedy-wt/r78_g7.txt` | 1 |
| G8 per-commit insertion counts | `python3 -B .remedy-wt/r78_g8.py` | `.remedy-wt/r78_g8.txt` | 0 |

Two gates ended non-zero. G6(d) is non-zero BY CONSTRUCTION — `ruff check .` exits 1 whenever it
reports any row, and the gate's substance is the row COUNT, which is 26 against the frozen
ceiling of 26. G7 is a REAL RED on its (c) clause and is declared in Deviations below; its (a),
(b) and (d) clauses all passed.

### G1 — transport, the block budget, the insertion cap

    cmp .remedy-wt/r78_c0a_blob.bin .remedy-wt/r78_block.md   -> exit 0
    G1(a) committed C0a blob == the reviewer's scratch original, 30875 bytes
    G1(b) C0b blob == the COMMITTED C0a blob, sha256 dd7d9cbc1cff4a38...
    G1(c) slices found: 4 -> DEC78, DONE78, PLAN78, RECORD78; all four stamped == actual
          DEC78 ed5a8464... DONE78 e5a8dfba... PLAN78 f6dbfa9b... RECORD78 980607cc...
    G1(d) TOTAL=347, PROSE=275 (347 minus 72 lines lying between BEGIN and END markers),
          against the caps 490 and 400
    G1(e) no single-repeated-character line outside a slice: offending lines []

### G2 — the plan

    G2 .agent/plan.md at C1 is byte-identical to slice PLAN78, 2916 bytes
    G2 48 lines, at most 50
    G2 exactly one '## Goal' (1) and exactly one '## Next Steps' (1)

### G3 — the record, with full forensics

Three appends, two independent readers and one negative control each.

    RECORD78 at 951ceeb3 -> .agent/live_review.md
      (i)   READER A  pre 1078915 B prefix=True, slice 4812 B suffix=True, post 1083727 B
      (ii)  READER B  N counted from the slice = 3; last 3 units equal in order
      (iii) CONTROL   letter flipped at byte 1078916 of the FIRST appended paragraph;
                      reader A=False reader B=False — both REJECT
      (iv)  numstat deletion column: ['6', '0', '.agent/live_review.md']
    DEC78 at 2b301c50 -> .agent/decisions.md
      (i)   READER A  pre 1226549 B prefix=True, slice 4730 B suffix=True, post 1231279 B
      (ii)  READER B  N counted from the slice = 8; last 8 units equal in order
      (iii) CONTROL   letter flipped at byte 1226553; reader A=False reader B=False
      (iv)  numstat deletion column: ['16', '0', '.agent/decisions.md']
    DONE78 at 77a564aa -> .agent/live_review.md
      (i)   READER A  pre 1083727 B prefix=True, slice 1314 B suffix=True, post 1085041 B
      (ii)  READER B  N counted from the slice = 1; last 1 unit equal
      (iii) CONTROL   letter flipped at byte 1083728; reader A=False reader B=False
      (iv)  numstat deletion column: ['2', '0', '.agent/live_review.md']
    (v) the Gate: header pattern, DERIVED from the corpus rather than asserted:
        '^Gate: F\d+ R\d+ \xe2\x80\x94 ' matched 99 of 99 prior headers;
        RECORD78 contributes exactly ONE Gate: header, it matches that shape,
        its key 'Gate: F275 R77' duplicates none of the 99, and it carries a
        VERDICT as 98 of the 99 prior headers do (a sub-pattern, reported, not required).

### G4 — the restore, and this is the gate the round exists for

The derivation was RECOMPUTED inside the gate, not quoted from the block:

    p=246  s=13  main-only=65 lines  branch-only=20 lines
    (i)   numstat for C4: '66\t0\tdocs/agents/self_drive_protocol.md'
    (ii)  SLICE IDENTITY: committed lines 267..332 == blank line + M[246:311], 4813 bytes
    (iii) ROUND TRIP A: committed minus that 66-line region == e262f420 blob (16765 bytes)
    (iv)  ROUND TRIP B: committed minus 21 lines from line 247 == d0aa833b blob (20015 bytes)
    (v)   345 lines, ends with a newline, four lines begin 'Operator amendment amend0911'
          at lines 268, 279, 299, 323; all 13 'Operator amendment' lines are preceded by a
          blank line, unpreceded=[]

The negative controls, four mutations plus the unmutated control, each a byte string mutated IN
MEMORY, no file written:

    UNMUTATED CONTROL                              (ii)=True  (iii)=True  (iv)=True   ACCEPT
    flip ASCII letter at byte 16075 (line 268)     (ii)=False (iii)=True  (iv)=False  REJECT
    delete line 270 (inside the inserted region)   (ii)=False (iii)=False (iv)=False  REJECT
    delete line 249 (inside the amend0908 block)   (ii)=False (iii)=False (iv)=False  REJECT
    delete line 343 (inside the shared tail)       (ii)=True  (iii)=False (iv)=False  REJECT

Mutations run: 4. THE GATE IS THE CONJUNCTION OF (ii), (iii) AND (iv), not three passes: the
reviewer's two measured claims reproduced exactly here — the letter flip leaves (iii) TRUE and
the shared-tail deletion leaves (ii) TRUE, so no single reading catches all four.

### G5 — the prose slips

    (a) the heading '## Authored text for round 78 to book' occurs exactly ONCE in
        b916c1a1:.agent/handoff.md, at line 872; the region to the next '## ' (line 878)
        holds 5 lines of which exactly 2 are non-blank; both begin '2026-09-12 · F275 R77 · '
        and neither carries trailing whitespace
    (b) appended bytes = blank + line 1 + blank + line 2; pre 281574 B + 2031 B == post 283605 B
    (c) numstat for C3: '4\t0\t.agent/prose_slips.md'

### G6 — the guards on the target and the colours

Every command ran in the PRIMARY checkout, never a worktree.

    (a) BASE e262f420  python3 -B -m pytest tests/test_agent_tooling.py -q
        10 passed, 1 skipped in 0.20s                                        exit 0
    (a) C4   391eb79e  python3 -B -m pytest tests/test_agent_tooling.py -q
        10 passed, 1 skipped in 0.20s                                        exit 0
    (b) C4   391eb79e  python3 -B -m pytest tests/docs/ -q
        306 passed in 0.53s                                                  exit 0
    (c) C6   77a564aa  python3 -B -m pytest tests/cli/test_golden_path.py -q
        42 passed in 18.88s                                                  exit 0
    (d) C6   77a564aa  ruff check .
        Found 26 errors.  [*] 25 fixable with the `--fix` option.            exit 1

The base and C4 readings of (a) are identical, which is the claim the gate exists to prove rather
than assume: a pure insertion into a document pinned only by substring presence cannot redden it.
The 26 ruff rows were counted mechanically from the `-->` location lines and none of them is in
`.remedy-wt/`; they sit in 18 files, 6 of them in `tests/cli/test_plan_approval.py`. The round
adds no Python to the repository, and the count did not move.

### G7 — the tree, the path set and the open set

    (a) git status --porcelain -> '' (the empty string) at C6                PASS
    (b) git worktree list -> 1 row, the primary checkout alone               PASS
    (c) changed-path set of e262f420..77a564aa: 7 paths
        MISSING = ['.agent/handoff.md']   EXTRA = []                         FAIL
        changed paths under packages/, apps/ or tests/: 0                    PASS
    (d) base e262f420  registered=109 resolved=22 OPEN=87  R-0880 open=True  PASS
        C2   951ceeb3  registered=110 resolved=22 OPEN=88  R-0880 open=True  PASS
        C6   77a564aa  registered=110 resolved=23 OPEN=87  R-0880 open=True  PASS
        membership difference base vs C6: only_in_base=[] only_in_C6=[]      PASS
        R-0881 at C2: registered and OPEN; at C6: no longer open

The (c) failure is the block's own ordering, not a defect in the change set; it is declared in
full below.

### G8 — the per-commit insertion counts

    C0a  fd33d98f  +347  -0     .agent/authored/f275-r78.md          paths=1  under 500
    C0b  2da9b410  +276  -326   .agent/last_block.md                 paths=1  under 500
    C1   6e488a9f  +24   -24    .agent/plan.md                       paths=1  under 500
    C2   951ceeb3  +6    -0     .agent/live_review.md                paths=1  under 500
    C3   77f01074  +4    -0     .agent/prose_slips.md                paths=1  under 500
    C4   391eb79e  +66   -0     docs/agents/self_drive_protocol.md   paths=1  under 500
    C5   2b301c50  +16   -0     .agent/decisions.md                  paths=1  under 500
    C6   77a564aa  +2    -0     .agent/live_review.md                paths=1  under 500

C7, this handback, is not covered: its own numbers cannot exist while its text is written
(item 14), and the reviewer measures them at the next gate (item 31).

### The STOP readings constraint 7 orders

    before C0a  2026-09-12T14:13:28Z  os.path.exists('.agent/STOP') -> False
    before C7   2026-09-12T14:21:57Z  os.path.exists('.agent/STOP') -> False

The sentinel did not appear at any point in this round. It was never staged, never created and
never deleted, and its contents were never read.

## Authored-text proofs

| Text | Target | Proof | Result |
|---|---|---|---|
| the whole block | `.agent/authored/f275-r78.md` at C0a | `cmp` against `.remedy-wt/r78_block.md` | exit 0, 30875 bytes identical |
| the whole block | `.agent/last_block.md` at C0b | byte equality against the COMMITTED C0a blob | identical, sha256 `dd7d9cbc1cff4a38…` |
| slice PLAN78 | `.agent/plan.md` at C1 | byte equality, sha256 over the bytes between the markers | `f6dbfa9bdd9ce81a…` matched |
| slice RECORD78 | `.agent/live_review.md` at C2 | reader A + reader B + a rejected control | matched, control REJECTED |
| slice DEC78 | `.agent/decisions.md` at C5 | reader A + reader B + a rejected control | matched, control REJECTED |
| slice DONE78 | `.agent/live_review.md` at C6 | reader A + reader B + a rejected control | matched, control REJECTED |

Every slice was extracted programmatically from the COMMITTED C0a blob and written with a script;
no slice was opened in an editor, retyped or reflowed. The two DERIVED texts — the 66 restored
lines at C4 and the two prose-slip lines at C3 — were computed from committed git objects by the
recipes the block states, and are proved by G4 and G5 rather than by a digest.

## Deviations & assumptions

1. **G7(c) IS RED AND IS UNMEETABLE AS WRITTEN AT THE TIME THE BLOCK ORDERS IT.** Constraint 9
   orders every gate to run at C6, strictly before C7. G7(c) requires the changed-path set of
   "the whole range" to equal the EIGHT paths of the Change section with MISSING empty. One of
   those eight, `.agent/handoff.md`, is changed by C7 alone — the commit that is forbidden to
   exist when the gate runs. The measurement: `git diff --name-only e262f420 77a564aa` returns 7
   paths, `MISSING = ['.agent/handoff.md']`, `EXTRA = []`. The gate script therefore exits 1. The
   block was NOT repaired and the recipe was NOT adjusted: the ordered reading stands as taken.
   What the reading does establish is exact — the seven paths are the Change section's eight
   minus `.agent/handoff.md`, nothing extra was touched, and the count under `packages/`, `apps/`
   or `tests/` is ZERO. The reviewer can close the clause by re-running it over
   `e262f420..HEAD` once C7 has landed.
2. **G1(c) SAYS "THREE AUTHORED SLICES"; THE BLOCK CARRIES FOUR.** The block ships PLAN78,
   RECORD78, DEC78 and DONE78 — four BEGIN/END pairs, counted mechanically by the gate script,
   which printed `slices found: 4`. The delegating prompt says four; G1(c) says three; G3 names
   three APPENDS, which is correct and is probably where the numeral came from. All four digests
   were verified and all four matched, so nothing on disk turns on it. Recorded here as a
   reviewer-prose inaccuracy with no product effect, per the `.agent/prose_slips.md` rule; no id
   was minted.
3. **G6(d)'s EXIT CODE IS 1 AND THAT IS NOT A RED GATE.** `ruff check .` exits non-zero whenever
   it reports any row at all; the gate's substance is 26 rows against the frozen ceiling of 26,
   which holds. The real exit code is reported rather than laundered, and the distinction is
   stated here so that "exit 1" is not read as movement.
4. **G3(v)'s PATTERN WAS DERIVED FROM THE CORPUS, NOT ASSERTED.** The block orders the RECORD78
   header "compared as a pattern against the headers already in `.agent/live_review.md`" and
   required to "match their repeating shape". A first, narrower pattern
   (`Gate: F<n> R<n> — the F<n> round <n> entry. VERDICT <PASS|FAIL>.`) matched only 27 of the 99
   prior headers and so was not their repeating shape. The widest pattern all 99 exhibit is
   `^Gate: F\d+ R\d+ — `, and that is what the gate compares against; the `VERDICT (PASS|FAIL)`
   sub-pattern is reported beside it (98 of 99) and is not a pass condition. No slice byte
   changed; only the gate's own reading was calibrated against what it measures.
5. **ONE GATE SCRIPT WAS REPAIRED BETWEEN RUNS, AND THE FIRST RUN IS DISCLOSED.** The first
   execution of G1 exited 1 because the worker's own script passed an unsubstituted `%s` to
   `git show`, so `cmp` never ran (`cmp exit 128`). The script was fixed and re-run; the
   transcript file `.remedy-wt/r78_g1.txt` holds the SECOND, passing run. No repository byte
   was touched by either run, and the defect was in the instrument, not in the artefact.
6. **NO DEPARTURE FROM THE ORDERED COMMIT SEQUENCE.** C0a, C0b, C1, C2, C3, C4, C5, C6, C7 landed
   in exactly that order, each staging exactly one path, with no extra commit, no dropped commit
   and no reordering. `.agent/live_review.md` is staged twice, at C2 and C6, exactly as the
   Change section provides for.
7. **NOTHING UNDER `packages/`, `apps/` OR `tests/` MOVED.** Measured, not asserted: G7(c)
   counted 0 such paths across the range. No production line moved and no test was added,
   weakened or deleted — including the substring pin that could not see the loss, which
   DECISION F275 D52 records as deliberately NOT fixed by this round.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C0a save the block as authored text | done | `fd33d98f` |
| C0b mirror the block into `.agent/last_block.md` | done | `2da9b410` |
| C1 make the plan current | done | `6e488a9f`, the first substantive commit |
| C2 book the round 77 verdict, register `R-0881` | done | `951ceeb3` |
| C3 append the round 77 prose slips | done | `77f01074`, both lines extracted |
| C4 restore the amendment | done | `391eb79e`, 66 lines derived from `d0aa833b` |
| C5 record DECISION F275 D52 | done | `2b301c50` |
| C6 resolve `R-0881` | done | `77a564aa` |
| C7 the round 78 handback | done | this commit |
| `R-0881` | done | registered at C2, resolved at C6, repair landed at C4 |
| `R-0880` | open | untouched by this round; open at the base, at C2 and at C6 |
| G7(c) | deviated | unmeetable at the ordered time; declared with its measurement |

## Next

Operator questions open: 0. `.agent/operator_questions.md` reads
`EMPTY — nothing is waiting on the operator.` under its header, and this round writes nothing to
it: restoring the operator's own text is not a reversible ruling made on the operator's behalf in
the sense restored rule C means, so there is nothing for the operator to overturn.

The single expected next action: the planner and reviewer of session 28 reads the committed range
`e262f420`..`HEAD`, re-derives every gate above against the committed blobs — including G7(c)
over the full range now that C7 exists — and issues the round 78 verdict.

After that verdict, the plan's Next Steps stand unchanged: carry the 19 surviving over-selection
frames back to the ruled sites that produce them, then the resolver collapse DECISION F260 D5
places in T003, then THE FLIP on the corrected 2185-site set DECISION F275 D51 rules, then the
classic store and the closure sequence.
