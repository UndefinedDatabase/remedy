# Handback — F109 Semantic dedupe, round 21 — THE CLOSURE COMMIT, THE LAST ON THIS BRANCH

## Session

SESSION 4 of feature F109 · round 21 · rounds so far 21

Soft limit is 25 rounds / 7 sessions (self_drive_protocol.md G7, amend0827 rule
6). At 21 rounds and 4 sessions it is NOT reached, so no scope report is due.
`.agent/STOP` was read from disk before the first commit, again before the pairs
were applied and again before this handback; it does not exist at any of those
points.

## State

| Feld | Wert |
|------|------|
| **Feature** | F109 Semantic dedupe (T3) |
| **Branch** | `feature/f109-semantic-dedupe` |
| **Runde** | 21 (Session 4) — CLOSURE |
| **Vorheriger Stand** | `6336513e` |
| **Fortschritt** | 100 % (T001-T003 ✅ · Integration Gate ✅ · Self-Use ✅ · Evidence+Zip ✅ · Closure) — Schätzung |
| **Gates** | G1-G8 alle ausgeführt, echte Exit-Codes und echte Ausgaben unten. G1-G4 und G6-G8 GRÜN; G5 ist TEILWEISE — die Pfadmenge von C3 hat VIER Pfade, nicht fünf, siehe Abweichung D1 |
| **Offene Findings** | 279 (Mengendifferenz, nicht Subtraktion; unverändert durch diese Runde) |

The `Fortschritt` row above is the block's SLICE FORTSCHRITT, applied verbatim as
its own line — extracted by delimiter index from the committed
`.agent/authored/f109-r21.md` and substituted into this file by script, never
retyped.

## The closure facts, as the STATUS line now carries them

| Feld | Wert |
|------|------|
| **Evidence job** | `f109-closure` |
| **package** | `remedy-review-20260903-073602-READY_FOR_REVIEW.zip` |
| **SHA-256** | `92b85aa8c28870d40d927773c1635c2aa6ae9b1ba02156e1b4e76e017aa7a538` |
| **package path (ARCHIVED PATH)** | `/home/decodeux/Repos/remedy-history/zips` |
| **PACKAGE_STATUS** | `READY_FOR_REVIEW` |
| **accepted HEAD** | `00084eef9de84b01e207a621d05d9b55378a2abc` |
| **live review** | `PASS_WITH_RISKS` — ACCEPTED |

The accepted HEAD is round 20's C2, the last CONTENT commit before the package
was built. This round's commits are `.agent/` bookkeeping plus the ledger flip
and are deliberately NOT covered by the package, which is what the closure
protocol's build order prescribes.

## Range

Review of `6336513e..HEAD` (HEAD is the commit this file is written in).

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C0a `084dbd2b` | done | block copied verbatim with `shutil.copyfile`; G1 `cmp` exit 0 against the reviewer's own `.remedy-wt/f109-r21.md` |
| C0b `fb03c23e` | done | mirrored to `.agent/last_block.md`; one sha256 for both copies |
| C1 `f6bb90f9` | done | PLAN21 extracted by delimiter index from the COMMITTED authored copy and applied; G2 `cmp` exit 0, 39 lines |
| C2 `fd865bc3` | done | RECORD21 appended as the two bytes `\n\n` + slice; arithmetic, second reader and grep all pass |
| C3 (this commit) | deviated | all five pairs applied byte for byte and the handback rewritten, but the path set is FOUR paths, not the five the block names: `.agent/plan.md` has nothing left to change at C3 because the block authored exactly one plan slice and assigned it to C1. See deviation D1. |

Every ordered item appears exactly once. No item was skipped.

## Commits

### 084dbd2b F109 R21 C0a: save the round 21 closure block verbatim
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f109-r21.md` | +296 / -0 | the reviewer's block saved verbatim; transport proof's first link |

### fb03c23e F109 R21 C0b: mirror the round 21 closure block to last_block
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/last_block.md` | +233 / -291 | round 20's block replaced by round 21's; same sha256 as the authored copy |

### f6bb90f9 F109 R21 C1: the plan turns to the closure round itself
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/plan.md` | +13 / -16 | PLAN21 applied whole; 39 lines, under the AGENTS.md 50-line rule |

### fd865bc3 F109 R21 C2: book the round 20 gate - the package is verified READY
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/live_review.md` | +3 / -1 | RECORD21's single paragraph appended; the round 20 PASS booked, no new id registered |

### C3 (this commit) F109 R21 C3: close F109 — STATUS accepted, README synced, self-use item consumed
| Path | +/- | Reason |
|------|-----|--------|
| `docs/roadmap/STATUS.md` | +1 / -1 | PAIR S — the `[~]` F109 line rewritten as the authored `[x]` line with all six closure facts |
| `README.md` | +11 / -2 | PAIR R1 the accepted count 67→68, PAIR R2 the tier-3 Done column 2→3, PAIR R3 the F109 capability paragraph inserted at the end of the Tier 3 list. In the SAME commit as STATUS, because README and STATUS may never disagree in any committed state (R-0154) |
| `scripts/self_use_queue.json` | +1 / -1 | PAIR Q — `SU-005`'s `consumed_by` set to `F109` as a TEXT replacement, closure precondition 6 |
| `.agent/handoff.md` | rewrite | a handoff cannot table the commit that writes it (R-0149 pattern) |

`.agent/plan.md` is NOT in this commit; see deviation D1.

## External actions

| Command | Outcome |
|---|---|
| `git push -u origin feature/f109-semantic-dedupe` | run after this commit; the real result is reported in the round report |
| `gh pr create` | run AFTER this commit is pushed, per the block. PR created immediately after this commit; number in the round report |

The PR is NOT merged this session. It merges at the next feature's start through
the Open PR Gate, and that gap is the operator's manual-review window
(closure protocol algorithm step 6, guardrail G1). No `gh pr merge` was run.
No worktree was added or removed. Nothing was force-pushed.

## Verification

One line per gate first, then the transcripts.

| Gate | Reading |
|---|---|
| G1 TRANSPORT | GREEN — `cmp` exit 0 against the reviewer's own scratch original; one sha256 for both copies |
| G2 THE PLAN AND THE RECORD | GREEN — plan `cmp` exit 0, 39 lines, both headings 1; record arithmetic exact, second reader accepts, `grep -c` = 1 |
| G3 THE FIVE PAIRS | GREEN — all five FROM 1→0, all five TO 0→1, all five rewrites by the containment test |
| G4 THE LEDGER PINS | GREEN — STATUS 68 `[x]` / 0 `[~]`, README `68 of 266` ×1, tier-3 Done = 3, `tests/docs/` 295 passed exit 0 |
| G5 RULE A4 | PARTIAL — C3 IS the branch tip with nothing after it, but its path set is FOUR paths, not five. See D1 |
| G6 THE SELF-USE CONSUMPTION | GREEN on every clause — 5 items, `SU-005` = `F109`, other four unchanged, `schema_version` 2, parses. The U+2014 clause reads 0 before and 0 after, which is TRUE but VACUOUS; see D2 for the measurement that is not |
| G7 THE CANARY AND THE FEATURE SUITES | GREEN — 42, 130, 54, each exit 0, no count moved |
| G8 THE TREE, THE PR AND THE SWEEP | tree EMPTY and `git ls-files .remedy-wt` empty before this commit; insertion counts agree cell by cell; push, PR number and the post-commit tree read are in the round report |

### G1 TRANSPORT — GREEN

    $ cmp .remedy-wt/f109-r21.md .agent/authored/f109-r21.md
    REAL_EXIT=0          (no output)

    $ sha256sum .agent/authored/f109-r21.md .agent/last_block.md
    e5f746b3893ca969ab5bb3eb7a0b218ffcd7f6b7984a6eb9a5154c2f069ed997  .agent/authored/f109-r21.md
    e5f746b3893ca969ab5bb3eb7a0b218ffcd7f6b7984a6eb9a5154c2f069ed997  .agent/last_block.md

One digest twice. The left-hand file of the `cmp` is the REVIEWER'S OWN original,
so this is a real transport proof and not self-consistency.

### G2 THE PLAN AND THE RECORD — GREEN

PLAN21 was extracted by delimiter index (`BEGIN PLAN21` / `END PLAN21`, marker
lines excluded) from the COMMITTED `.agent/authored/f109-r21.md` and written to
`.agent/plan.md`:

    slice bytes (with the file's trailing newline)   1651
    $ cmp .remedy-wt/PLAN21.extracted .agent/plan.md   REAL_EXIT=0   (no output)
    $ wc -l .agent/plan.md                             39            (under 50)
    $ grep -c '^## Goal' .agent/plan.md                1
    $ grep -c '^## Next Steps' .agent/plan.md          1

The trailing-newline convention was not guessed. It was MEASURED against the
round 20 precedent before C1 was written: the delimiter-extracted PLAN20 slice
matches the committed `.agent/plan.md` WITH a trailing newline and not without
it, so PLAN21 landed the same way.

RECORD21, appended at C2 as exactly the two bytes `\n\n` followed by the slice:

    BASE size (at 6336513e)                   2137953
    BASE sha256                               95f192b58e99bd74f59942aaed7e5374dfc57a1dd6737b39d031cdb14e8ddf0d
    BASE ends with a newline                  False
    RECORD21 slice bytes                         2986
    appended length S (2 separator + 2986)       2988
    NEW size                                  2140941
    base + S                                  2140941
    base + S == new size                      True
    NEW ends with a newline                   False   (the convention is preserved)

A SECOND READER THAT COUNTS NO BYTE. The WHOLE file was split on blank-line
boundaries. N was counted BY THE SCRIPT from the slice, not taken from the
block: N = 1. The file holds 896 such units and the LAST 1 equals RECORD21's 1
paragraph, in order:

    unit[-1] equals RECORD21 paragraph 1: True (len 2974 vs 2974)
    last N file units == RECORD21 paragraphs IN ORDER: True

    $ grep -c '^Gate: F109 R20 — ' .agent/live_review.md   ->  1   (must be 1)

That grep answered 0 with exit 1 BEFORE the append, so the 1 is this round's
append and not a pre-existing line. `^Gate: F109 R` counted 19 before and the
append makes rounds 1-20 complete.

### G3 THE FIVE PAIRS — GREEN, every one a REWRITE

Each FROM was counted in its real target BEFORE C3 and required to be exactly 1
before any write; each replacement was `replace(FROM, TO, 1)`.

    PAIR  target                       FROM before  FROM after  TO before  TO after  TO contains FROM
    S     docs/roadmap/STATUS.md            1           0           0          1         False
    R1    README.md                         1           0           0          1         False
    R2    README.md                         1           0           0          1         False
    R3    README.md                         1           0           0          1         False
    Q     scripts/self_use_queue.json       1           0           0          1         False

`TO contains FROM` is False in all five, so all five are REWRITES and the
"FROM 0 / TO 1" reading is a real discriminator rather than something an append
would also satisfy. PAIR R3 is the one that needed the argument: its TO inserts
the F109 paragraph BETWEEN the FROM's two parts, so the FROM does not survive
contiguously — and it does not, as the 0 above shows.

### G4 THE LEDGER PINS — GREEN

    STATUS  ^- \[x\] F\d{3} — count:  68   (expected 68; was 67 before C3)
    STATUS  ^- \[~\]        count:   0   (expected 0;  was 1  before C3)
    README '68 of 266 registered items accepted':  1   (expected 1)
    README '67 of 266 registered items accepted':  0   (expected 0)
    README tier-3 row: | 3 | Full Token Economy & Autonomy | 3 | 26 |
      tier-3 Done column: 3   (expected 3; was 2)

Tier 3 now holds F106, F108 and F109 — three accepted, which is what the Done
column says and what the README's own Tier 3 paragraph list shows.

    $ python3 -m pytest tests/docs/ -q
    295 passed in 0.53s
    REAL_EXIT=0

295 collected at exit 0, exactly the count at `6336513e`. This is the suite that
pins README and STATUS against each other, so it is the one that would have gone
red had the two disagreed.

### G5 RULE A4 — PARTIAL: LAST, YES; FIVE PATHS, NO

C3 is the branch tip with nothing after it, and no `.agent/candidates.md` commit
follows it because this round raises no candidate. The `git log --oneline` for
the range and the `git show --numstat` for C3 are in the round report, because
this file is written INSIDE C3 and cannot read the commit that contains it
(R-0149 pattern).

The path set of C3 is FOUR paths — `docs/roadmap/STATUS.md`, `README.md`,
`scripts/self_use_queue.json`, `.agent/handoff.md` — and not the five the block
names. `.agent/plan.md` is the missing fifth and it is missing because there was
nothing to write into it: see deviation D1. Nothing outside those four was
touched.

### G6 THE SELF-USE CONSUMPTION — GREEN on every clause

    parses as JSON: True
    item count: 5
    schema_version: 2
      SU-001 consumed_by='F257'  UNCHANGED from pre-C3 'F257': True
      SU-002 consumed_by='F258'  UNCHANGED from pre-C3 'F258': True
      SU-003 consumed_by='F106'  UNCHANGED from pre-C3 'F106': True
      SU-004 consumed_by='F108'  UNCHANGED from pre-C3 'F108': True
      SU-005 consumed_by='F109'  (was '')  exact match 'F109': True

The four pre-C3 values were read from the file at `6336513e` before anything was
written, so "unchanged" is a comparison against a measured baseline and not
against a remembered one.

The U+2014 clause, reported as ordered and then declared:

    queue literal U+2014 characters   BEFORE C3: 0    AFTER C3: 0
    queue total non-ASCII characters  BEFORE C3: 0    AFTER C3: 0
    queue file size                   BEFORE C3: 14000 bytes   AFTER C3: 14004 bytes

The count is unchanged, so the clause passes as written — but it passes VACUOUSLY
and the handback says so rather than banking it. See D2.

### G7 THE CANARY AND THE FEATURE'S OWN SUITES — GREEN, run SERIALLY

    $ python3 -m pytest tests/cli/test_golden_path.py -q
    42 passed in 20.77s
    REAL_EXIT=0

    $ python3 -m pytest tests/orchestration/test_semantic_dedupe.py -q
    130 passed in 1.02s
    REAL_EXIT=0

    $ python3 -m pytest tests/orchestration/test_prompt_trace.py -q
    54 passed in 0.31s
    REAL_EXIT=0

42, 130 and 54 — the three expected counts, none moved, none red. This round
edits no test and no production code, so a moved count would itself have been the
finding.

### G8 THE TREE, THE PR AND THE SWEEP

Read immediately before this commit was staged (the three modified files are the
pair edits about to become C3):

    $ git status --porcelain
     M README.md
     M docs/roadmap/STATUS.md
     M scripts/self_use_queue.json
    $ git ls-files .remedy-wt
    (no output)

`git ls-files .remedy-wt` returns NOTHING, so every scratch script, extracted
slice and grep pattern file this round wrote is untracked and cannot enter the
review subject. The post-commit `git status --porcelain` EMPTY reading, the push
and the PR number are in the round report, because they happen after this file is
sealed.

Insertion counts, the `+` column ONLY (AGENTS.md DECISION F104 D1), from
`git show --numstat`, compared cell by cell against the `## Commits` table above:

    commit     path                              numstat +   table +   agree
    084dbd2b   .agent/authored/f109-r21.md            296       296     yes
    fb03c23e   .agent/last_block.md                   233       233     yes
    f6bb90f9   .agent/plan.md                          13        13     yes
    fd865bc3   .agent/live_review.md                    3         3     yes

Per-commit totals: C0a 296, C0b 233, C1 13, C2 3. Every one is far under the
500-insertion cap, and C0b would in any case be exempt as the verbatim rewrite of
a single `.agent/**` state file. C3's own numstat is in the round report; its
content edits are 13 insertions across three files, so it is nowhere near the cap
either.

Note on a number that looks wrong and is not: `git commit` printed "296
insertions" for C0b under rewrite detection, while `git show --numstat` — the
command this gate names — reports 233. The gate's own command is the one reported
here.

**THE STALENESS SWEEP over every file this round touched.**

1. `.agent/plan.md`, Current Step: "Round 21, session 4 — THE CLOSURE ROUND ...
   the PR is created but NOT merged". Written in the present tense at C1 and
   still exactly what the round did; it names the PR as created, which the round
   report confirms. NOT stale. Left as the block authored it in any case —
   `.agent/plan.md` is rewritten whole every round by construction.
2. `.agent/live_review.md`, RECORD21: every figure in it is scoped to its own
   round and was independently reproduced this round — the open set is 279 by set
   difference over 347 distinct registered and 68 distinct resolved, which is
   exactly what the paragraph claims. NOT stale.
3. `docs/roadmap/STATUS.md`: the new F109 line's six facts were each checked
   against the round 20 measurements they come from. NOT stale.
4. `README.md`: the F109 paragraph's "556 characters avoided against 97 spent on
   markers on the fixture chain" and "No concrete adapter resumes in production
   yet" both match `docs/system/semantic-dedupe-v1.md` and the plan's own risk
   line. NOT stale.
5. `.agent/authored/f109-r21.md` and `.agent/last_block.md` are verbatim copies of
   the reviewer's own block; nothing in them is edited regardless of what a later
   measurement shows.

One sentence outside the change set is now stale and was NOT repaired, per
constraint 7: the round 20 handback's `## Next` section and the round 20
`.agent/plan.md` both said round 21 "also runs the single consolidation pass on
the checklist of docs/agents/planner_reviewer_prompt.md section 3". The round 21
block orders no such pass, and `docs/agents/planner_reviewer_prompt.md` is not in
this round's change set. Declared, not repaired — see D3.

NOTHING OUTSIDE THE CHANGE SET WAS EDITED.

## Authored-text proofs

The GREP PROOF the closure protocol requires by name. Every applied
reviewer-authored text was extracted from the COMMITTED
`.agent/authored/f109-r21.md` by delimiter index, written to its own pattern file
under `.remedy-wt/`, and matched with a real `grep -c -F -f` against the real
target on disk. Blank pattern lines were filtered out first: a blank pattern
matches every blank line in the target and would prove nothing.

| Authored text | Grep proof | Expected | Read | Exit |
|---|---|---|---|---|
| the whole block | `cmp .remedy-wt/f109-r21.md .agent/authored/f109-r21.md` | identical | identical | 0 |
| the block mirror | `sha256sum` of `.agent/authored/f109-r21.md` and `.agent/last_block.md` | one digest twice | `e5f746b3…ed997` twice | 0 |
| PLAN21 (39 lines, 30 non-blank) | `grep -c -F -f GREP_PLAN21.txt .agent/plan.md` | 30 | 30 | 0 |
| PLAN21 (whole file) | `cmp .remedy-wt/PLAN21.extracted .agent/plan.md` | identical | identical | 0 |
| RECORD21 (1 line) | `grep -c -F -f GREP_RECORD21.txt .agent/live_review.md` | 1 | 1 | 0 |
| PAIR S TO (1 line) | `grep -c -F -f GREP_PAIRS_TO.txt docs/roadmap/STATUS.md` | 1 | 1 | 0 |
| PAIR R1 TO (1 line) | `grep -c -F -f GREP_PAIRR1_TO.txt README.md` | 1 | 1 | 0 |
| PAIR R2 TO (1 line) | `grep -c -F -f GREP_PAIRR2_TO.txt README.md` | 1 | 1 | 0 |
| PAIR R3 TO (12 lines, 10 non-blank) | `grep -c -F -f GREP_PAIRR3_TO.txt README.md` | 10 | 10 | 0 |
| PAIR Q TO (1 line) | `grep -c -F -f GREP_PAIRQ_TO.txt scripts/self_use_queue.json` | 1 | 1 | 0 |
| FORTSCHRITT (1 line) | `grep -c -F -f GREP_FORTSCHRITT.txt .agent/handoff.md` | 1 | 1 | 0 |

Every one of those greps ran with a real exit code and the counts above are the
real answers, not expectations restated. Beside the greps, an exact-substring
count in Python confirmed each whole multi-line slice occurs exactly once as a
contiguous byte sequence in its target — that is the reading G3's "TO after = 1"
column reports, and it is what makes the per-line grep counts a proof of the
whole slice rather than of its lines separately.

## Deviations & assumptions

**D1 — THE C3 PATH SET IS FOUR PATHS, NOT THE FIVE THE BLOCK NAMES. This is the
one deviation from the block's ordered sequence and it is unavoidable as the
block is written.** Constraint 3 and gate G5 both require C3 to touch exactly
`docs/roadmap/STATUS.md`, `README.md`, `scripts/self_use_queue.json`,
`.agent/plan.md` and `.agent/handoff.md`. The block authors exactly ONE plan
slice, PLAN21, and its own bundle assigns that slice to C1 — "C1 apply PLAN21 to
`.agent/plan.md` (FIRST substantive commit)". There is no second plan slice, and
PLAN21's text is already the terminal state of this branch: its Current Step
describes the closure round and its Next Steps say "Nothing else is owed by this
branch." So after C1 there is nothing left for C3 to write into `.agent/plan.md`.

The two ways to make G5 read "five" were both rejected, and the reasons are
recorded so the reviewer can overrule them knowingly:

  (a) Author a fresh `.agent/plan.md` edit in the worker's own words at C3. That
      would put unauthored text on disk over a slice that had just been
      `cmp`-verified byte for byte, breaking the authored-text fidelity chain
      constraint 1 exists to protect, and it would be a diff invented to make a
      gate green — the one thing AGENTS.md names as never acceptable.
  (b) Move PLAN21 from C1 to C3. That contradicts the block's explicit bundle
      order and would leave `.agent/plan.md` stale through C1 and C2, failing the
      AGENTS.md Commit Gate at both.

The path set was therefore left at the four paths that have real content, and the
gate is reported PARTIAL rather than green. Everything the five-path rule exists
to protect still holds: README and STATUS moved in ONE commit (R-0154), nothing
outside the change set was touched, and C3 is the last commit on the branch.

**D2 — G6's U+2014 CLAUSE IS TRUE BUT VACUOUS, AND HERE IS THE MEASUREMENT THAT
IS NOT.** The gate asks for the count of the literal U+2014 character in
`scripts/self_use_queue.json` before and after C3, as the discriminator against
the `json.dumps` round trip finding `R-0785` describes. That count is 0 BEFORE
and 0 AFTER — unchanged, so the clause passes. But it is 0 because the file
contains NO literal non-ASCII character at all: the em dashes are already stored
as 18 SIX-CHARACTER JSON ESCAPE SEQUENCES (backslash, `u`, `2014`), which is
`R-0785`'s damage already sitting on
disk from the generator that wrote the file. A discriminator that is 0 on both
sides of a correct edit is also 0 on both sides of an `ensure_ascii=True` round
trip, so it cannot distinguish them.

Three readings that are NOT vacuous were taken instead and all three agree that no
round trip happened:

    literal non-ASCII characters   BEFORE 0        AFTER 0        (as ordered)
    backslash-u-2014 escapes       BEFORE 18       AFTER 18       (a round trip
        with ensure_ascii=False would have turned all 18 into literal em dashes)
    file size                      BEFORE 14000    AFTER 14004    (delta +4,
        exactly len('F109') — a strictly local edit; a re-serialization would
        have moved the size by far more, or by nothing at all, never by exactly
        the inserted token)
    the committed diff             1 line changed, 1 line added, 1 removed

Constraint 5 was followed exactly: the edit is `str.replace(FROM, TO, 1)` on the
file's text. No `json.load` and no `json.dumps` was called on that file at any
point. `json.loads` WAS called on it afterwards, read-only, to prove it still
parses — that is a read, not a round trip, and it wrote nothing.

**D3 — A STALE INSTRUCTION OUTSIDE THE CHANGE SET, DECLARED AND NOT REPAIRED.**
Round 20's handback and round 20's plan both promised that round 21 would "also
run the single consolidation pass on the checklist of
docs/agents/planner_reviewer_prompt.md section 3" (amend0827 rule 4, which
freezes that checklist while a feature is open and releases it at the closure
sequence). The round 21 block orders no such pass and does not list
`docs/agents/planner_reviewer_prompt.md` in its change set. Constraint 7 says to
declare and not repair, so it is declared here. The consequence is that the
lessons parked in `.agent/prose_slips.md` during F109 are still parked; the next
session inherits the consolidation, and the checklist is unchanged and therefore
not wrong — only unconsolidated.

**D4 — THE FORTSCHRITT AND PR-NUMBER GREPS CANNOT RUN INSIDE THE COMMIT THAT
WRITES THEM.** Two readings this file is asked to carry are self-referential: the
grep of the FORTSCHRITT slice against `.agent/handoff.md`, and the PR number. The
FORTSCHRITT line was substituted into this file BY SCRIPT from the committed
authored copy rather than retyped, and its grep is run against the written file
and reported in the round report. The PR is created AFTER this commit is pushed,
exactly as the block orders, so the sentence "PR created immediately after this
commit; number in the round report" above is the block's own prescribed wording
and not an omission. C3 is NOT amended to insert the number afterwards: amending
a pushed commit is the history rewrite guardrail G2 forbids.

**D5 — THIS ROUND'S VERDICT HAS NO ON-DISK GATE ENTRY, BY CONSTRUCTION.** The
last round of a branch cannot record a gate on itself: RECORD21 books round 20,
and there is no round 22 to book round 21. Its verdict lives in this handback and
in the PR description. That absence is the branch TERMINATOR, not a missing gate
(planner_reviewer_prompt.md §4 item 13).

**D6 — THE THREE SELF-USE FINDINGS CLOSE OPEN, DELIBERATELY.** `R-0784`,
`R-0785` and `R-0786` are carried into closure as documented Low risks and none
has a `Done:` line. `R-0785` belongs to F258's generator and `R-0786` to F257's
queue file; repairing another feature's production code from this branch is the
scope drift AGENTS.md forbids. `R-0784` records the blocked self-use run that
closure precondition 6 required be recorded. The closure verdict is
`PASS_WITH_RISKS` precisely because of them, and the STATUS line says so.

**D7 — THE RETAINED JOB WORKTREES ARE STILL IN `.remedy-wt`.** Earlier rounds'
runs retained job worktrees there. This round created none and removed none. They
are gitignored, so `git status --porcelain` is empty and
`git ls-files .remedy-wt` returns nothing regardless. Pre-existing, carried
without an id, as round 20 already recorded.

**Assumptions.** (i) `.remedy-wt/` is gitignored session scratch that PERSISTS,
and the reviewer's own `.remedy-wt/f109-r21.md` must survive for G1 to be
re-runnable — so no scratch file was deleted by glob and the round's helper
scripts, extracted slices and grep pattern files were left in place so the
reviewer can re-run every gate from the same inputs. Nothing there is tracked.
(ii) The plan slice's trailing-newline convention was taken from the measured
round 20 precedent rather than assumed, as G2 records.

## Next

THE OPERATOR MERGES THE PR, or the next feature's first session merges it at the
Open PR Gate. Nothing else is owed by this branch: C3 is its last commit and F109
is `[x]` in the ledger. The next session's first action is Phase 1 rule 1 — read
`.agent/STOP` from disk — before Phase 1 rule 2, the Open PR Gate. It also
inherits the checklist consolidation pass D3 declares as unrun.
