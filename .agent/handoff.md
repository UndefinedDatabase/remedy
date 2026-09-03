# Handback — F109 Semantic dedupe, round 20 — CLOSURE STEPS 1 AND 2: EVIDENCE JOB + REVIEW ZIP

## Session

SESSION 4 of feature F109 · round 20 · rounds so far 20

Soft limit is 25 rounds / 7 sessions (self_drive_protocol.md G7, amend0827 rule
6). At 20 rounds and 4 sessions it is NOT reached, so no scope report is due.
`.agent/STOP` was read from disk before the first commit, again before the zip
build and again before this handback; it does not exist at any of those points.

## State

| Feld | Wert |
|------|------|
| **Feature** | F109 Semantic dedupe (T3) |
| **Branch** | `feature/f109-semantic-dedupe` |
| **Runde** | 20 (Session 4) |
| **Vorheriger Stand** | `a06a6e69` |
| **Fortschritt** | ~99 % (T001-T003 ✅ · Integration Gate ✅ · Self-Use ✅ · Evidence+Zip in Arbeit) — Schätzung |
| **Gates** | G1-G8 alle ausgeführt, alle GRÜN — echte Exit-Codes und echte Ausgaben unten |
| **Offene Findings** | 279 (Mengendifferenz, nicht Subtraktion; 276 vor diesem Append) |

The `Fortschritt` row above is the block's SLICE FORTSCHRITT, applied verbatim as
its own line — extracted by delimiter index from the committed
`.agent/authored/f109-r20.md` and substituted into this file by script, never
retyped.

## THE CLOSURE FACTS ROUND 21 NEEDS

These six values are what the STATUS line of round 21 must carry. They were
measured this round and nowhere else; nothing below is copied from a summary.

| Feld | Wert |
|------|------|
| **Evidence job** | `f109-closure` |
| **package** | `remedy-review-20260903-073602-READY_FOR_REVIEW.zip` |
| **SHA-256** | `92b85aa8c28870d40d927773c1635c2aa6ae9b1ba02156e1b4e76e017aa7a538` |
| **package path (ARCHIVED PATH)** | `/home/decodeux/Repos/remedy-history/zips` |
| **PACKAGE_STATUS** | `READY_FOR_REVIEW` |
| **accepted HEAD** | `00084eef9de84b01e207a621d05d9b55378a2abc` |

Notes that belong with those values and nowhere else:

- The ACCEPTED HEAD is commit **C2**, the last CONTENT commit of this round. The
  evidence bundle and the zip were built from the clean tree at C2, before C3
  existed, exactly as the closure protocol's build order requires. C3 (this
  handback) is NOT covered by the package and is not meant to be.
- The manifest's `committed_review_subject` reads base
  `5e18a8536afa086b591b5a2e13009d68d6227432` (the branch point, pull request 231)
  and head `00084eef9de84b01e207a621d05d9b55378a2abc` — read out of
  `.review_zip_manifest.json` INSIDE the built package, not from the script's
  stdout.
- The SHA-256 above was re-derived with `sha256sum` against the archived file and
  matched the packager's own `final_sha256` exactly.
- The ARCHIVED PATH is where the packager itself moved the zip
  (`REVIEW_PACKAGE_DIR=/home/decodeux/Repos/remedy-history/zips`). This round
  moved nothing by hand. That directory is OUTSIDE this repository, so the
  package cannot dirty the tree and cannot enter the review subject.
- The evidence dir sits at
  `.remedy-wt/f109_closure_evidence/remedy-job-evidence-f109-closure` (27 entries)
  and is NOT committed, per the closure protocol's "Evidence dir is not
  committed" rule. `git ls-files` finds no `remedy-job-evidence` path and no
  `.zip` anywhere in the repository.

## Range

Review of `a06a6e69..HEAD` (HEAD is the commit this file is written in).

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C0a `b5083bc7` | done | block copied verbatim with `shutil.copyfile`; G1 `cmp` exit 0 against the reviewer's own `.remedy-wt/f109-r20.md` |
| C0b `7a3121b7` | done | mirrored to `.agent/last_block.md`; one sha256 for both copies |
| C1 `f94fe8ef` | done | PLAN20 extracted by delimiter index from the COMMITTED authored copy and applied; G2 `cmp` exit 0, 42 lines |
| C2 `00084eef` | done | RECORD20 appended as the two bytes `\n\n` + slice; G3 (a)(b)(c)(d) all pass; this is the ACCEPTED HEAD |
| C3 (this commit) | done | handback rewritten per handback_template.md, then pushed |

Every ordered item appears exactly once. No item was skipped and none deviated.
The evidence bundle and the review zip were built BETWEEN C2 and C3 and neither
was committed, which is what the block orders, not a deviation.

## Commits

### b5083bc7 F109 R20 C0a: save the round 20 block verbatim
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f109-r20.md` | +354 / -0 | the reviewer's block saved verbatim; transport proof's first link |

### 7a3121b7 F109 R20 C0b: mirror the round 20 block to last_block
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/last_block.md` | +285 / -200 | round 19's block replaced by round 20's; same sha256 as the authored copy |

### f94fe8ef F109 R20 C1: the plan turns to closure steps 1 and 2
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/plan.md` | +15 / -16 | PLAN20 applied whole; 42 lines, under the AGENTS.md 50-line rule |

### 00084eef F109 R20 C2: book the round 19 gate and register R-0784, R-0785, R-0786
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/live_review.md` | +9 / -1 | RECORD20's four paragraphs appended; round 19 PASS booked, three findings registered |

### C3 (this commit) F109 R20 C3: handback for round 20
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/handoff.md` | rewrite | a handoff cannot table the commit that writes it (R-0149 pattern) |

## External actions

| Command | Outcome |
|---|---|
| `bash scripts/make_review_zip.sh --evidence-dir .remedy-wt/f109_closure_evidence/remedy-job-evidence-f109-closure` | REAL_EXIT=0, `PACKAGE_STATUS=READY_FOR_REVIEW`, zip written to `/home/decodeux/Repos/remedy-history/zips/remedy-review-20260903-073602-READY_FOR_REVIEW.zip` |
| `git push -u origin feature/f109-semantic-dedupe` | run after this commit; the real result is reported in the round report |

No PR was created, none was merged, no `gh` command was run, and no worktree was
added or removed by hand. The packager moved the zip to its archive directory
itself; this round moved nothing.

## Verification

### G1 TRANSPORT — GREEN

    $ cmp .remedy-wt/f109-r20.md .agent/authored/f109-r20.md
    REAL_EXIT=0          (no output)

    $ sha256sum .agent/authored/f109-r20.md .agent/last_block.md
    1324ca5a67f3f5f7ac31eedc070e5702729d5db2892d90afd960a3092f7a8e8f  .agent/authored/f109-r20.md
    1324ca5a67f3f5f7ac31eedc070e5702729d5db2892d90afd960a3092f7a8e8f  .agent/last_block.md

One digest twice. The left-hand file of the `cmp` is the REVIEWER'S OWN original,
so this is a real transport proof and not self-consistency.

### G2 THE PLAN — GREEN

PLAN20 was extracted by delimiter index (`BEGIN PLAN20` / `END PLAN20`, marker
lines excluded) from the COMMITTED `.agent/authored/f109-r20.md`, written to
`.agent/plan.md`, and compared:

    slice bytes (with the file's trailing newline)   1860
    $ cmp <extracted slice> .agent/plan.md      CMP_EXIT=0    (no output)
    $ wc -l .agent/plan.md                      42            (under 50)
    $ grep -c '^## Goal' .agent/plan.md         1
    $ grep -c '^## Next Steps' .agent/plan.md   1

### G3 THE RECORD APPEND — GREEN, all four readings

**(a) ARITHMETIC.** Base read from `git show a06a6e69:.agent/live_review.md`.

    BASE size                                 2129990
    BASE sha256                               da1fc11636c1b3fde4b6a5c85539f44de27ef121b95974bc686d95a14c8b76a9
    appended length S (the two bytes + slice)    7963
    NEW size                                  2137953
    base + S                                  2137953
    base + S == new size                      True
    NEW sha256                                95f192b58e99bd74f59942aaed7e5374dfc57a1dd6737b39d031cdb14e8ddf0d
    NEW ends with a newline                   False   (the convention is preserved)

**(b) A SECOND READER THAT COUNTS NO BYTE.** The WHOLE file was split on
blank-line boundaries. N was counted BY THE SCRIPT from the slice, not taken from
the block: N = 4. The last 4 units equal RECORD20's 4 paragraphs IN ORDER.

    unit 0 equal=True | Gate: F109 R19 — the round 19 entry. VERDICT PASS, over the
    unit 1 equal=True | - R-0784 — Low, THE SELF-USE RUN THIS CLOSURE CONSUMED ENDED
    unit 2 equal=True | - R-0785 — Low, THE SELF-USE GENERATOR REWRITES THE WHOLE QU
    unit 3 equal=True | - R-0786 — Low, THE SELF-USE QUEUE FILE'S OWN DESCRIPTION NO
    last N file units == RECORD20 paragraphs IN ORDER: True

**(c) NEGATIVE CONTROL on the FIRST appended paragraph.** The file was copied to
`.remedy-wt/live_review_negative_control_r20.md` and, in that copy only, the
FIRST appended paragraph's `VERDICT PASS` was changed to `VERDICT FAIL`.

    reader (b) on the CONTROL copy    False   (it REJECTS it)
    reader (b) on the TRACKED file    True    (it ACCEPTS it)
    tracked sha256 before             95f192b58e99bd74f59942aaed7e5374dfc57a1dd6737b39d031cdb14e8ddf0d
    tracked sha256 after              95f192b58e99bd74f59942aaed7e5374dfc57a1dd6737b39d031cdb14e8ddf0d
    tracked file untouched by the control   True

The scratch copy was deleted BY ITS EXACT PATH, never by glob, and

    os.path.exists('.remedy-wt/live_review_negative_control_r20.md')  ->  False

**(d) COUNTS, AS A SET DIFFERENCE (`R-0778`), never a subtraction.** Base read
from `git show a06a6e69:.agent/live_review.md` — THE ROUND'S OWN BASE. Registered
`^- (R-\d{4}) — `; a `Done:` line resolves the FIRST R-id it names.

    reading                                   BASE a06a6e69    NEW
    registered id lines                              344       347
    DISTINCT registered ids                          344       347
    'Done:' lines                                     70        70
    DISTINCT resolved ids                             68        68
    |set(registered) - set(resolved)|  = OPEN        276       279

    newly registered over the range:  R-0784, R-0785, R-0786
    newly resolved  over the range:   none

276 at base reproduces RECORD20's own re-verification figure exactly, so the
record and the disk agree. 347 − 70 = 277 is the WRONG reading; 279 is the set
difference, because two ids carry two `Done:` lines each. See the Deviations
section for the one measurement subtlety this reading has.

    $ grep -c '^Gate: F109 R19 — ' .agent/live_review.md  ->  1   (must be 1)
    $ grep -c '^- R-078[456] — '   .agent/live_review.md  ->  3   (must be 3)

### G4 THE EVIDENCE BUNDLE — GREEN

EVIDENCESCRIPT was extracted by delimiter index, copied byte-for-byte to
`.remedy-wt/f109_evidence.py`, and run unedited with `python3 -B`. It raised
nothing.

    $ python3 -B .remedy-wt/f109_evidence.py
    REAL_EXIT=0

    vr-0001 selected 130 node_ids 130 files 1 dur 1.04
    vr-0002 selected  54 node_ids  54 files 1 dur 0.31
    vr-0003 selected  27 node_ids  27 files 1 dur 0.59
    vr-0004 selected  20 node_ids  20 files 1 dur 0.2
    vr-0005 selected  13 node_ids  13 files 1 dur 0.19
    vr-0006 selected  14 node_ids  14 files 1 dur 0.73

Every `mkrun` asserted its expected pass count (130, 54, 27, 20, 13, 14) and every
one held; `len(node_ids) == selected` held in all six, so no record carries a
filtered id list.

    SCAN rejected strings: 0 []                                  (must be 0)
    SCAN red control: a local absolute path                       (truthy — the
        scanner still rejects '/home/user/repo/tests/x.py::t', so the 0 above is a
        real absence and not a dead scanner)

The full summary dict `create_manual_completion_bundle` returned:

    {
      "authority_count": 11,
      "commit_count": 143,
      "head_commit": "00084eef9de84b01e207a621d05d9b55378a2abc",
      "job_id": "f109-closure",
      "manual_completion": true,
      "operator_attested_tasks": ["T001", "T002", "T003"],
      "partition": {"T001": 4, "T002": 4, "T003": 3},
      "total_passed": 258,
      "verdict": "PASS_WITH_RISKS"
    }

The bundle's own verdict is **PASS_WITH_RISKS**, which is the honest reading: the
feature closes with documented Low risks, `R-0784` through `R-0786` among them.

    OUTPUT_HASH vr-0001 matches sha256(stdout_summary): True
    OUTPUT_HASH vr-0002 matches sha256(stdout_summary): True
    OUTPUT_HASH vr-0003 matches sha256(stdout_summary): True
    OUTPUT_HASH vr-0004 matches sha256(stdout_summary): True
    OUTPUT_HASH vr-0005 matches sha256(stdout_summary): True
    OUTPUT_HASH vr-0006 matches sha256(stdout_summary): True

Six of six True. No False, so no blocker.

### G5 THE TREE WAS CLEAN AT BUILD TIME — GREEN

Run immediately before the zip build, after C2 and before C3 existed:

    $ git status --porcelain
    (no output)
    $ git status --porcelain | wc -l
    0

The tree was EMPTY, so the package is valid under constraint 3.

### G6 THE REVIEW ZIP — GREEN, and the reading is READY_FOR_REVIEW

    $ bash scripts/make_review_zip.sh --evidence-dir /home/decodeux/Repos/remedy/.remedy-wt/f109_closure_evidence/remedy-job-evidence-f109-closure
    REAL_EXIT=0

    REVIEW_PACKAGE_CREATED=true
    PACKAGE_STATUS=READY_FOR_REVIEW
    PACKAGING_CWD=/home/decodeux/Repos/remedy
    EVIDENCE_DIR=/home/decodeux/Repos/remedy/.remedy-wt/f109_closure_evidence/remedy-job-evidence-f109-closure
    REVIEW_SUBJECT_ALIGNMENT=PASS
    EVIDENCE_AUTHORITATIVE=true
    REVIEW_PACKAGE_DIR=/home/decodeux/Repos/remedy-history/zips
    ZIP_PATH=/home/decodeux/Repos/remedy-history/zips/remedy-review-20260903-073602-READY_FOR_REVIEW.zip

    packager JSON line:
    member_count 3699 · authoritative_count 11 · symlink_count 0 · tombstone_count 0
    final_sha256 92b85aa8c28870d40d927773c1635c2aa6ae9b1ba02156e1b4e76e017aa7a538
    publication_capability SUPPORTED · package_status READY_FOR_REVIEW
    evidence_authoritative true · review_subject_alignment PASS
    manifest_sha256 19bb0d673a65543da20c9d51da7a6f07a0c3c7dd00fe32f0f20a8716a5b102bf

**PACKAGE_STATUS reads `READY_FOR_REVIEW`.** That is the reading this gate turns
on, not the exit code — which is 0 for `BLOCKED_EVIDENCE` too and therefore
proves nothing on its own.

    FILENAME       remedy-review-20260903-073602-READY_FOR_REVIEW.zip
    SHA-256        92b85aa8c28870d40d927773c1635c2aa6ae9b1ba02156e1b4e76e017aa7a538
    ARCHIVED PATH  /home/decodeux/Repos/remedy-history/zips
    PACKAGE_STATUS READY_FOR_REVIEW
    EVIDENCE_AUTHORITATIVE true

The SHA-256 was re-derived independently against the archived file rather than
trusted from the packager's stdout:

    $ sha256sum /home/decodeux/Repos/remedy-history/zips/remedy-review-20260903-073602-READY_FOR_REVIEW.zip
    92b85aa8c28870d40d927773c1635c2aa6ae9b1ba02156e1b4e76e017aa7a538
    REAL_EXIT=0

`committed_review_subject`, read out of `.review_zip_manifest.json` INSIDE the
package with `zipfile`, not from the packager's stdout:

    package_status  READY_FOR_REVIEW
    crs.base_commit 5e18a8536afa086b591b5a2e13009d68d6227432
    crs.head_commit 00084eef9de84b01e207a621d05d9b55378a2abc
    crs keys        base_commit, base_is_ancestor, commit_count, file_count,
                    head_commit, tombstones

The head the manifest records is C2, `00084eef9de84b01e207a621d05d9b55378a2abc`.
**That is the ACCEPTED HEAD round 21's STATUS line must carry.**

### G7 THE INTEGRITY CHECK (closure precondition 3) — GREEN

The `remedy` binary is denied session-wide here, so the check ran through the
library entry point the block names. The result is an `IntegrityGateResult`
OBJECT with attributes, not a dict.

    $ python3 -B .remedy-wt/f109_r20_g7.py
    REAL_EXIT=0
    type        : IntegrityGateResult
    passed      : True
    fail_count  : 0
    checks total: 5
    failing checks: 0

`.passed` is True and `.fail_count` is 0, so there is no failing check to name.
Closure precondition 3 is satisfied at C2.

### G8 THE TREE AND THE SWEEP — GREEN

    $ git status --porcelain
    (no output)
    PORCELAIN_LINES=0
    $ git ls-files .remedy-wt
    (no output)
    LSFILES_LINES=0
    $ git ls-files | grep -c "remedy-job-evidence"    ->  0   (no evidence dir tracked)
    $ git ls-files | grep -c "\.zip$"                 ->  0   (no zip tracked)
    os.path.exists('.agent/STOP')                     ->  False

Insertion counts, the `+` column ONLY (AGENTS.md DECISION F104 D1), from
`git show --numstat`, compared cell by cell against the `## Commits` table above:

    commit     path                              numstat +   table +   agree
    b5083bc7   .agent/authored/f109-r20.md            354       354     yes
    7a3121b7   .agent/last_block.md                   285       285     yes
    f94fe8ef   .agent/plan.md                          15        15     yes
    00084eef   .agent/live_review.md                    9         9     yes

Per-commit totals: C0a 354, C0b 285, C1 15, C2 9. Every one is far under the
500-insertion cap; no commit needs the oversize exception. C3 is excluded by the
gate's own wording, and C0b and C2 would in any case be exempt as verbatim
rewrites of a single `.agent/**` state file.

**THE STALENESS SWEEP over every file this round touched.** Two sentences are now
stale and neither was repaired:

1. `.agent/plan.md`, Current Step: "Round 20, session 4. CLOSURE, steps 1 and 2:
   the evidence job and a FRESH review zip, plus the integrity check." True when
   C1 was written, and by the end of the round all three are DONE rather than
   pending. It reads as the round's stated GOAL, not as a claim about the end
   state, and `.agent/plan.md` is rewritten whole every round by construction —
   so it is left exactly as the block authored it. This is the same class the
   round 19 handback declared, and it is a `.agent/prose_slips.md` line at the
   consolidation, not an id.
2. `.agent/plan.md`, Risks: "A failing zip build is a CLOSURE BLOCKER, never
   something to work around." Still TRUE as a rule; stale only as a live risk,
   because the build succeeded READY_FOR_REVIEW this round. Left as authored.

`.agent/authored/f109-r20.md` and `.agent/last_block.md` are verbatim copies of
the reviewer's own block; applying them byte for byte is the whole point of them,
so nothing in them is edited regardless of what a later measurement shows.
`.agent/live_review.md`'s RECORD20 is dated to its own round and is never
rewritten (checklist item 20); its "open set is 276" claim is scoped to base
`a06a6e69` and reproduces exactly there, so nothing in it is stale.

NOTHING OUTSIDE THE CHANGE SET WAS EDITED. The sweep found no defect outside the
change set beyond what the Deviations section already declares.

## Authored-text proofs

| Authored text | Proof | Result |
|---|---|---|
| the whole block | `cmp .remedy-wt/f109-r20.md .agent/authored/f109-r20.md` | exit 0 |
| the block mirror | `sha256sum` of `.agent/authored/f109-r20.md` and `.agent/last_block.md` | one digest twice |
| PLAN20 | slice extracted by delimiter index from the committed authored copy, `cmp` against `.agent/plan.md` | exit 0 |
| RECORD20 | appended as `\n\n` + slice; arithmetic G3(a), the four-paragraph reader G3(b) and the set-difference count G3(d) all accept, the negative control G3(c) rejects the mutated copy | exact |
| EVIDENCESCRIPT | extracted by delimiter index, copied to `.remedy-wt/f109_evidence.py`, run unedited with `python3 -B`; first and last lines verified against the slice boundaries | ran clean, exit 0 |
| FORTSCHRITT | extracted by delimiter index and substituted into this file by script; verified as a verbatim substring of `.agent/handoff.md` | substring True |

## Deviations & assumptions

**No deviation from the block's ordered commit sequence.** C0a, C0b, C1, C2 and
C3 ran in that order, one commit each, nothing extra, nothing dropped, nothing
reordered. The evidence bundle and the zip were built between C2 and C3 as the
block orders, and neither was committed.

**D1 — THE ZIP DID NOT LAND WHERE THE ROUND BRIEF EXPECTED IT.** The worker's
delegation brief said the zip would land in the repository root, which
`.gitignore` matches. It did not: the packager reports
`REVIEW_PACKAGE_DIR=/home/decodeux/Repos/remedy-history/zips` and moved the zip
there itself, OUTSIDE this repository. The consequence the brief cared about
still holds — `git status --porcelain` is empty and no zip is tracked — but the
ARCHIVED PATH is therefore a real archive directory and NOT the literal
`NOT ARCHIVED`. This is recorded here because DECISION amend0827 D1 makes this
round the only actor that knows the answer, and because a later session looking
for the package in the repository root would not find it.

**D2 — THE `Done:` READING G3(d) USES, STATED SO THE REVIEWER CAN REPRODUCE IT.**
Three readings of "resolved" are possible over this ledger and they do not agree:
attributing each `Done:` line to the ENCLOSING registration gives 49 distinct;
counting EVERY R-id named anywhere in a `Done:` line gives 76; counting the FIRST
R-id each `Done:` line names gives **68**. The third is the reading RECORD20's
own round-19 re-verification used — it is the only one that reproduces the
record's "344 registered, 68 resolved, open set 276" at base `a06a6e69` — so it
is the reading reported above. This is a measurement note, not a defect claim:
nothing on disk is wrong and no id is spent on it.

**D3 — NO `Done:` OR `Landed:` LINE WAS WRITTEN FOR R-0784, R-0785 OR R-0786,
DELIBERATELY.** Constraint 5 forbids it and the reason is scope: all three are
documented Low risks carried into closure, `R-0785` and `R-0786` belong to
F258's generator and to F257's queue file, and repairing another feature's
production code from this branch is the scope drift AGENTS.md forbids outright.
They are registered and left open.

**D4 — THE RETAINED JOB WORKTREES ARE STILL THERE.** `.remedy-wt` holds the job
worktrees earlier rounds' runs retained, including
`.remedy-wt/job-5e91e080219342d9` from round 19. This round created none and
removed none. They are gitignored, so `git status --porcelain` is EMPTY and
`git ls-files .remedy-wt` returns nothing regardless. RECORD20 already records
this as pre-existing product behaviour carried without an id.

**Assumptions.** (i) `.remedy-wt/` is gitignored session scratch that PERSISTS,
and the reviewer's own `.remedy-wt/f109-r20.md` must survive for G1 to be
re-runnable — so only the negative-control copy the block names for deletion was
deleted, by its exact path, and the round's helper scripts, the extracted slices
and the evidence dir were left in place so the reviewer can re-run every gate.
Nothing there is tracked. (ii) C2 is the correct ACCEPTED HEAD because it is the
last CONTENT commit and the manifest independently names it.

## Next

ROUND 21, THE CLOSURE COMMIT. The authored STATUS line carrying the six closure
facts above, with the README capability sync in the SAME commit (R-0154), the
`consumed_by = "F109"` edit on `SU-005` in `scripts/self_use_queue.json`, the
final `.agent/` state, and then the PR. That round also runs the single
consolidation pass on the checklist of
docs/agents/planner_reviewer_prompt.md section 3. Phase 1 rule 1 — re-read
`.agent/STOP` from disk — comes before Phase 1 rule 2, the Open PR Gate.
