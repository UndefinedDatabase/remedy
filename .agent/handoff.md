# Handback — F110 Model routing by task class, round 4 — T002a, THE CLASS TABLE AND ITS SYNC TEST

## Session

SESSION 1 of feature F110 · round 4 · rounds so far 4

Soft limit is 25 rounds / 7 sessions (self_drive_protocol.md G7, amend0827 rule
6). At 4 rounds and 1 session it is nowhere near, so no scope report is due.
`.agent/STOP` was read from disk twice — before the first commit (C0a) and again
before C5 — and does not exist at either point.

## State

| Feld | Wert |
|------|------|
| **Feature** | F110 Model routing by task class (Tier 3, depends on F103) |
| **Branch** | `feature/f110-model-routing-by-task-class` |
| **BASE** | `05d78941` — the round 3 handback commit |
| **Runde** | 4 (Session 1) — T002a: the class table seeded from the policy document, and the sync test that pins it there |
| **Fortschritt** | ~45 % (T001a ✅ inventory · T001b ✅ provider seam · T001c ✅ orchestrator model seam · T002a ✅ class table + sync test · T002b, T002c, T003 open) — Schätzung |
| **Gates** | G1-G8 alle ausgeführt, echte Exit-Codes und echte Ausgaben unten. ALLE GRÜN. |
| **Offene Findings** | UNVERÄNDERT gegen Runde 3 — diese Runde registriert nichts und löst nichts auf; bei BASE und bei HEAD mit derselben Methode gemessen, Mengendifferenz identisch (siehe D4 zur Zählmethode) |

THIS ROUND SHIPS THE TABLE F110 EXISTS FOR, AND WIRES IT TO NOTHING.
`packages/orchestration/model_routing.py` maps each of the ten task classes
`docs/agents/model_routing_policy.md` names to a model tier, and
`tests/orchestration/test_model_routing.py` parses that document and asserts the
two agree. The module is imported by its test and by no production caller, which
is constraint 7 and is deliberate: consolidation order E.d puts the per-call-site
class declarations after the seam work. No hard rule was implemented, stubbed or
named in code — constraint 6 — because an unenforced rule on disk is a claim this
round cannot prove.

## Range

Review of `05d78941..HEAD` (HEAD is the commit this file is written in).

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C0a `34f075dd` | done | block written verbatim to `.agent/authored/f110-r4.md`, 259 insertions |
| C0b `f7b9ae57` | done | mirrored with `shutil.copyfile`; one sha256 for both copies (G1) |
| C1 `a36addc9` | done | PLAN4 extracted by delimiter index from the COMMITTED authored copy and applied whole; `cmp` exit 0, 46 lines. FIRST substantive commit, item 23 |
| C2 `310999d2` | done | RECORD3 appended to `.agent/live_review.md` and SLIPS4 to `.agent/prose_slips.md`, each with the two-byte separator; full arithmetic in G3, byte-equality in G4 |
| C3 `2e22062e` | done | THE PRODUCTION COMMIT — the new `packages/orchestration/model_routing.py`, 130 insertions, no other path (G5) |
| C4 `7349421a` | done | THE TEST COMMIT — the new 48-test file carrying the sync test and its four-bullet guard |
| C5 (this commit) | done | handback rewritten per `docs/agents/handback_template.md` |

Every ordered item appears exactly once. No item was skipped and none deviated
from its ordered position. Constraint 3's order — C3 production BEFORE C4 tests —
was honoured.

## Commits

### 34f075dd F110 R4 C0a: save the round 4 block verbatim
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f110-r4.md` | +259 / -0 | the reviewer's block saved verbatim; the first link of the transport chain |

### f7b9ae57 F110 R4 C0b: mirror the round 4 block to last_block
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/last_block.md` | +175 / -152 | round 3's block replaced by this one; byte-identical copy of the authored file |

### a36addc9 F110 R4 C1: the plan turns to T002a, the class table
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/plan.md` | +20 / -20 | PLAN4 applied whole; 46 lines, under the AGENTS.md 50-line rule |

### 310999d2 F110 R4 C2: book the round 3 PASS verdict and its two prose slips
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/live_review.md` | +3 / -1 | RECORD3 appended — round 3's PASS verdict, booked in the first substantive-adjacent commit of the next round (amend0827 rule 1, item 23) |
| `.agent/prose_slips.md` | +5 / -1 | SLIPS4 appended — TWO dated reviewer prose slips this time, blank-line separated; no R-id spent (amend0827 rule 2) |

### 2e22062e F110 R4 C3: seed the task-class to model-tier table from the policy document
| Path | +/- | Reason |
|------|-----|--------|
| `packages/orchestration/model_routing.py` | +130 / -0 | new module: the tier vocabulary, the normalizer, the ten-entry class table, the resolver. Nothing else, and no caller edited |

### 7349421a F110 R4 C4: pin the class table to the policy document with a sync test
| Path | +/- | Reason |
|------|-----|--------|
| `tests/orchestration/test_model_routing.py` | +211 / -0 | 48 tests: the sync test, the four-bullet guard, the unit tests. No model id asserted anywhere |

### C5 (this commit) F110 R4 C5: the round 4 handback
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/handoff.md` | rewrite | a handoff cannot table the commit that writes it (R-0149 pattern). Its own numbers go to neither a round report nor this file, per the block: the reviewer measures them at the next gate |

The `+` column above is the INSERTION count from `git show --numstat`
(AGENTS.md DECISION F104 D1). The cell-by-cell comparison is in G8.

## External actions

| Command | Outcome |
|---|---|
| `git worktree add --detach .remedy-wt/f110r4_mut 7349421a` | `Preparing worktree (detached HEAD 7349421a)` — the G6 red proof ran ONLY here |
| `git -C .remedy-wt/f110r4_mut restore packages/orchestration/model_routing.py` | mutation (i) reverted by EXACT PATH; `git status --porcelain` in the worktree empty afterwards |
| `git -C .remedy-wt/f110r4_mut restore docs/agents/model_routing_policy.md` | mutations (ii) and (iii) reverted by EXACT PATH, once each; worktree status empty afterwards both times |
| `git worktree remove .remedy-wt/f110r4_mut` | removed; `git worktree list` afterwards shows no worktree of this round's making |
| `git worktree prune` | no output |
| `git push -u origin feature/f110-model-routing-by-task-class` | run after this commit; the real result is in the completion report |

No pull request was created and nothing was merged, as the block orders. Nothing
was force-pushed, no history was rewritten, no commit was made on `main`. The
five `.remedy-wt/job-*` worktrees listed by `git worktree list` are retained job
worktrees from earlier features; this round created none of them and removed none
of them.

## Verification

One line per gate first, then the transcripts.

| Gate | Reading |
|---|---|
| G1 TRANSPORT | GREEN — one sha256 twice, `5b0a1248…6dc2`; `wc -l` reads **259**, EXACTLY the reviewer's projection of 259. WORKER SELF-CONSISTENCY ONLY: the reviewer stated it holds no scratch original, so this proves the mirror equals the saved copy and nothing about the emitted bytes (§3 item 37). First round of this feature in which the projection is exact; well under the §3 item 1 cap of 400 |
| G2 THE PLAN | GREEN — `cmp` exit 0, 46 lines (< 50), `^## Goal` 1, `^## Next Steps` 1 |
| G3 THE LEDGER APPEND | GREEN — 2153907 + 2 + 4611 = 2158520 real; the second reader accepts the last 1 unit IN ORDER; the negative control REJECTS; the grep reads 0 before C2 (exit 1) and 1 after (exit 0) |
| G4 THE PROSE FILE | GREEN — `.agent/prose_slips.md` final 1425 bytes byte-equal to the extracted SLIPS4, pre-C2 content an exact byte PREFIX, file still ends WITHOUT a newline |
| G5 THE MODULE | GREEN — `git show --numstat 2e22062e` reads **130** insertions on the one path; `ast.parse` over the real text raises nothing; the SHIPPED CODE was RUN and all ten documented classes answer their documented tier with reason `seed_mapping`, the undocumented class answers `('top', 'unknown_class_conservative')`, and the normalizer answers `standard_build`, `standard_build`, `mission` |
| G6 THE SYNC TEST'S RED PROOF | GREEN, AND THE DISCRIMINATOR HOLDS IN BOTH DIRECTIONS — control 48 passed exit 0; mutation (i), a re-tiered class in the CODE, reddens 1 id at exit 1; mutation (ii), a reworded class phrase in the WORKTREE's DOCUMENT, reddens the SAME 1 id at exit 1. Neither mutation left the sync test green. Ran only in the disposable worktree, which is removed and pruned |
| G7 THE SUITES | GREEN — 48, 33, 34, 295, 42, each its own invocation, run serially, every one exit 0. The last four match the reviewer's base measurements EXACTLY: no count moved, including `tests/docs/` |
| G8 THE TREE, THE COMMITS AND THE SWEEP | GREEN — tree EMPTY before C5 was staged, `git ls-files .remedy-wt` no output, no worktree of this round's making, `git diff --stat 05d78941..7349421a` lists NO path under `docs/`, all seven insertion cells agree |

### G1 TRANSPORT — GREEN

    $ sha256sum .agent/authored/f110-r4.md .agent/last_block.md
    5b0a124832fd1160e62eebc2fab359c93dfff966c7fef8971694c3e9acbd6dc2  .agent/authored/f110-r4.md
    5b0a124832fd1160e62eebc2fab359c93dfff966c7fef8971694c3e9acbd6dc2  .agent/last_block.md
    REAL_EXIT=0

    $ wc -l .agent/authored/f110-r4.md
    259 .agent/authored/f110-r4.md
    REAL_EXIT=0

One digest, twice, both lines verbatim. The reviewer stated up front that it
holds no scratch original this round, so this is WORKER SELF-CONSISTENCY ONLY: it
proves the mirror equals the saved copy and nothing about what the reviewer
emitted. That is the §3 item 37 shape and it is reported as such.

THE `wc -l` READING IS 259 AGAINST A PROJECTION OF 259 — no difference, so there
is nothing to report and nothing to repair. This is the first round of F110 in
which the projection is exact; rounds 1, 2 and 3 were low by 1, 1 and 3, which is
what SLIPS3 recorded and what SLIPS4's second paragraph — appended in this very
round — describes. The counter-measure is now on its second outing and is
reported either way, hit or miss. The committed file is 21133 bytes; the cap is
400 lines.

Every APPLIED slice below was extracted BY DELIMITER INDEX from the COMMITTED
`.agent/authored/f110-r4.md` — read with `git show HEAD:.agent/authored/f110-r4.md`,
never from the working copy — and written to its target BY SCRIPT. Nothing was
retyped. Each marker string was asserted to occur EXACTLY ONCE before any write
(the extractor raises otherwise).

    PLAN4    begin line 202  end line 249   46 lines   2255 bytes (with trailing newline)   2254 without
    RECORD3  begin line 251  end line 253    1 line    4612 bytes (with trailing newline)   4611 without
    SLIPS4   begin line 255  end line 259    3 lines   1426 bytes (with trailing newline)   1425 without

Constraint 4 settles which form each target takes: `.agent/plan.md` ends WITH a
newline and took the 2255-byte form; `.agent/live_review.md` and
`.agent/prose_slips.md` end WITHOUT one and took the 4611 / 1425 forms. The
TARGET's convention wins, exactly as ordered. SLIPS4 is THREE lines and TWO
blank-separated paragraphs this round, where SLIPS3 was one; the append is still
a single two-byte separator followed by the whole slice.

### G2 THE PLAN — GREEN

    $ cmp .remedy-wt/f110r4/PLAN4.extracted .agent/plan.md
    (no output)
    REAL_EXIT=0
    $ wc -l .agent/plan.md
    46 .agent/plan.md            (must be under 50 — it is)
    REAL_EXIT=0
    $ grep -c '^## Goal' .agent/plan.md
    1
    REAL_EXIT=0
    $ grep -c '^## Next Steps' .agent/plan.md
    1
    REAL_EXIT=0

### G3 THE LEDGER APPEND — GREEN, FULL ARITHMETIC

THE COUNT TAKEN BEFORE THE COMMIT, so the 1 is provably this round's append and
not a pre-existing line. `grep -c` exits 1 when it counts 0; that is the real exit
code and it is reported rather than smoothed:

    BEFORE C2:  $ grep -c '^Gate: F110 R3 — ' .agent/live_review.md   -> 0   REAL_EXIT=1
    AFTER  C2:  $ grep -c '^Gate: F110 R3 — ' .agent/live_review.md   -> 1   REAL_EXIT=0

RECORD3 at C2, against the file size IMMEDIATELY BEFORE that commit, read from the
git OBJECT at `310999d2^` rather than from a remembered number:

    size BEFORE C2                      2153907
    separator bytes                           2   (newline newline)
    RECORD3 slice length                   4611   (extractor yields 4612; the target takes no trailing newline)
    before + 2 + slice                  2158520
    real new size                       2158520
    equal                                  True
    new file ends WITHOUT a newline        True
    pre-append content an exact PREFIX     True
    final 4611 bytes equal the slice       True

The 2153907 matches the block's own stated base size exactly, so the append
started where the reviewer measured it would.

A SECOND READER THAT COUNTS NO BYTE. The WHOLE file was split on blank-line
boundaries. N was counted BY THE SCRIPT from the slice, never taken from the
block: N = 1.

    N counted BY THE SCRIPT from the slice   1
    blank-line units in the WHOLE file       900
    unit[-1] equals slice paragraph 1: True (len 4605 vs 4605 characters)
    last N file units == slice paragraphs IN ORDER:   True

The byte length (4611) and the character length (4605) differ because the
paragraph carries multi-byte characters; both readings are of the same string and
neither is a discrepancy.

NEGATIVE CONTROL, on a SCRATCH COPY under `.remedy-wt/` — the tracked file was
never mutated:

    first appended paragraph found at byte offset   2153909
    flipped byte at offset 2154009 (was 'T') with XOR 0x01
    second reader ACCEPTS the mutated copy:         False
    second reader REJECTS it:                       True

### G4 THE PROSE FILE — GREEN, BYTE-EQUALITY ONLY

Which is all amend0827 rule 5 allows a `.agent/` prose file. Re-checked AFTER C2
landed, with the pre-C2 bytes read from the git OBJECT at `310999d2^`:

    size BEFORE C2 (from the git object)                        51088
    separator bytes                                                 2
    SLIPS4 slice length                                          1425
    before + 2 + slice                                          52515
    real new size                                               52515
    equal                                                        True
    final 1425 bytes equal the extracted SLIPS4 slice:           True
    pre-C2 content preserved as an exact byte PREFIX:            True
    file still ends WITHOUT a newline:                           True

### G5 THE MODULE, MEASURED AND RUN — GREEN

    $ git show --numstat 2e22062e -- packages/orchestration/model_routing.py
    130	0	packages/orchestration/model_routing.py
    REAL_EXIT=0

    ast.parse over the real text: OK (no exception)

THE SHIPPED CODE WAS RUN, not read. These are the real answers:

    module __file__: /home/decodeux/Repos/remedy/./packages/orchestration/model_routing.py
    MODEL_TIERS = ('cheap', 'mid', 'top')   TOP_TIER = 'top'

    resolve_task_class_tier for each of the TEN documented classes:
       format                             -> ('cheap', 'seed_mapping')
       extract                            -> ('cheap', 'seed_mapping')
       summarize                          -> ('cheap', 'seed_mapping')
       boilerplate                        -> ('cheap', 'seed_mapping')
       standard_build                     -> ('mid', 'seed_mapping')
       standard_review                    -> ('mid', 'seed_mapping')
       architecture                       -> ('top', 'seed_mapping')
       mission                            -> ('top', 'seed_mapping')
       vision                             -> ('top', 'seed_mapping')
       prompt_authoring_for_other_agents  -> ('top', 'seed_mapping')

       a_class_the_document_does_not_name -> ('top', 'unknown_class_conservative')

    normalize_task_class:
       'Standard Build'     -> 'standard_build'
       'standard build'     -> 'standard_build'
       '  MISSION  '        -> 'mission'

THE UNKNOWN CASE REPORTS THE TOP TIER AND THE EXACT REASON STRING, which is what
`docs/roadmap/features/T3_F110.md`'s "Edge cases & assumption defaults" section
specifies. The ten pairs are exactly the ten the block's SPEC CODE (c) lists: four
cheap, two mid, four top. No class the document does not name was added and none
was renamed. NO MODEL ID appears anywhere in the module or the tests — this round
maps classes to TIERS.

### G6 THE SYNC TEST'S RED PROOF — GREEN, AND THE DISCRIMINATOR HOLDS BOTH WAYS

Ran ONLY inside a disposable worktree at the C4 commit, never in the primary
checkout. `__pycache__` was purged and `python3 -B` used throughout; the imported
module path was printed from inside the worktree first, so the mutation
demonstrably reaches the test rather than being shadowed by an installed copy or
by the parent checkout:

    $ git worktree add --detach .remedy-wt/f110r4_mut 7349421a
    Preparing worktree (detached HEAD 7349421a)
    HEAD is now at 7349421a F110 R4 C4: pin the class table to the policy document with a sync test

    __pycache__ dirs inside the worktree: 0 (a freshly added worktree has none, and -B writes none)
    imported module file inside the worktree:
    /home/decodeux/Repos/remedy/.remedy-wt/f110r4_mut/packages/orchestration/model_routing.py

THE UNMUTATED CONTROL FIRST, as ordered:

    --- CONTROL, UNMUTATED ---
    $ python3 -B -m pytest tests/orchestration/test_model_routing.py -q
    ................................................                         [100%]
    48 passed in 0.23s
    REAL_EXIT=0

MUTATION (i) — a class's TIER changed in the CODE table, to another VALID tier so
that only the document-versus-code claim can notice it:

    -    "boilerplate": "cheap",
    +    "boilerplate": "mid",

    $ python3 -B -m pytest tests/orchestration/test_model_routing.py -q
    F...............................................                         [100%]
    1 failed, 47 passed in 0.30s
    REAL_EXIT=1

    THE ID THAT WENT RED:
    TestPolicyDocumentSyncTest::test_the_parsed_seed_mapping_equals_the_module_table

    E  Differing items:
    E  {'boilerplate': 'cheap'} != {'boilerplate': 'mid'}

REVERTED BY EXACT PATH and the revert PROVED, not assumed:

    $ git -C .remedy-wt/f110r4_mut restore packages/orchestration/model_routing.py
    $ git -C .remedy-wt/f110r4_mut status --porcelain
    '' (empty — the worktree carried the committed bytes again)
    $ python3 -B -m pytest tests/orchestration/test_model_routing.py -q
    48 passed in 0.23s
    REAL_EXIT=0

MUTATION (ii) — a class PHRASE changed in the WORKTREE's copy of the DOCUMENT.
The primary checkout's copy was never touched; G8 confirms it:

    - - format / extract / summarize / boilerplate → cheap tier (local allowed)
    + - format / extract / summarise / boilerplate → cheap tier (local allowed)

    $ python3 -B -m pytest tests/orchestration/test_model_routing.py -q
    F...............................................                         [100%]
    1 failed, 47 passed in 0.25s
    REAL_EXIT=1

    THE ID THAT WENT RED — the SAME one:
    TestPolicyDocumentSyncTest::test_the_parsed_seed_mapping_equals_the_module_table

    E  Left contains 1 more item:
    E  {'summarise': 'cheap'}
    E  Right contains 1 more item:
    E  {'summarize': 'cheap'}

THE DISCRIMINATOR IS SATISFIED. The sync test goes RED for BOTH — code drift and
document drift — and the failure MESSAGE differs between them ("differing items"
against "left/right contains 1 more item"), so it does not merely produce a
colour: it names which side moved. Neither mutation left the sync test green, so
there is no FAILED proof to report. Reverted by exact path, revert proved:

    $ git -C .remedy-wt/f110r4_mut restore docs/agents/model_routing_policy.md
    $ git -C .remedy-wt/f110r4_mut status --porcelain
    '' (empty)

AN ADDITIONAL, UNORDERED PROBE (iii) — DECLARED AS EXTRA IN D1, NOT AS A
SUBSTITUTE FOR EITHER ORDERED MUTATION. The block's SPEC TESTS (e) makes the
fourth, non-arrow bullet load-bearing: a future editor adding a SECOND rule bullet
must turn the file red rather than have it silently filtered away. That claim is
about a mutation the two ordered mutations do not make, so it was made and
measured:

    + - Vision prompts follow the tier of the mission that raised them.

    $ python3 -B -m pytest tests/orchestration/test_model_routing.py -q
    3 failed, 45 passed in 0.25s
    REAL_EXIT=1

    TestPolicyDocumentSyncTest::test_the_section_carries_exactly_four_bullets
    TestPolicyDocumentSyncTest::test_exactly_one_bullet_is_a_rule_rather_than_a_mapping
    TestPolicyDocumentSyncTest::test_the_one_rule_bullet_is_the_repair_prompt_sentence

AND `test_the_parsed_seed_mapping_equals_the_module_table` STAYED GREEN under it,
which is exactly the hazard the reviewer named: the mapping-equality assertion
alone WOULD have passed over a second rule bullet. The three explicit bullet
assertions are what catch it. Reverted by exact path, revert proved at 48 passed
exit 0, worktree status empty.

    $ git worktree remove .remedy-wt/f110r4_mut
    $ git worktree prune
    $ git worktree list
    /home/decodeux/Repos/remedy                                  7349421a [feature/f110-model-routing-by-task-class]
    /home/decodeux/Repos/remedy/.remedy-wt/job-48a379ab5ca44ec5  f0e6b9a3 [remedy/job-48a379ab5ca44ec5]
    /home/decodeux/Repos/remedy/.remedy-wt/job-5e91e080219342d9  9fdb3b4b [remedy/job-5e91e080219342d9]
    /home/decodeux/Repos/remedy/.remedy-wt/job-7d1c93e2dc98415a  f0e6b9a3 [remedy/job-7d1c93e2dc98415a]
    /home/decodeux/Repos/remedy/.remedy-wt/job-98e9364a83a34872  21a45836 [remedy/job-98e9364a83a34872]
    /home/decodeux/Repos/remedy/.remedy-wt/job-f76686b8435640e9  4b49af98 [remedy/job-f76686b8435640e9]

No worktree of THIS round's making remains; the five `job-*` entries predate it.

### G7 THE SUITES — GREEN, EACH AS ITS OWN INVOCATION, RUN SERIALLY

Never two pytest processes alive at once.

    $ python3 -m pytest tests/orchestration/test_model_routing.py -q
    48 passed in 0.24s
    REAL_EXIT=0

    $ python3 -m pytest tests/orchestration/test_orchestrator_model_routing.py tests/orchestration/test_job_role_routing.py -q
    33 passed in 0.27s
    REAL_EXIT=0

    $ python3 -m pytest tests/orchestration/test_role_config.py -q
    34 passed in 0.23s
    REAL_EXIT=0

    $ python3 -m pytest tests/docs/ -q
    295 passed in 0.45s
    REAL_EXIT=0

    $ python3 -m pytest tests/cli/test_golden_path.py -q
    42 passed in 22.07s
    REAL_EXIT=0

48, 33, 34, 295, 42. THE LAST FOUR MATCH THE REVIEWER'S BASE MEASUREMENTS
EXACTLY — 33, 34, 295, 42 — so no count moved anywhere, including in
`tests/docs/`, which the block runs because this round's test READS a file under
`docs/`. There is no moved count to report as a finding. The new file reports 48;
the block asked for the count rather than fixing one. The last invocation is the
canary every handback owes.

### G8 THE TREE, THE COMMITS AND THE SWEEP — GREEN

Read immediately before C5 was staged:

    $ git status --porcelain
    (no output — the tree is EMPTY)
    REAL_EXIT=0
    $ git ls-files .remedy-wt
    (no output)
    REAL_EXIT=0

`git ls-files .remedy-wt` returns NOTHING, so every scratch script, extracted
slice and negative-control copy this round wrote is untracked and cannot enter the
review subject.

THE DOCUMENT IS UNCHANGED IN THE PRIMARY CHECKOUT. G6's mutation (ii) and probe
(iii) both edited `docs/agents/model_routing_policy.md` INSIDE THE DISPOSABLE
WORKTREE ONLY, and the range diff proves the primary copy never moved:

    $ git diff --stat 05d78941..7349421a
     .agent/authored/f110-r4.md                | 259 +++++++++++++++++++++++
     .agent/last_block.md                      | 327 ++++++++++++++++--------------
     .agent/live_review.md                     |   4 +-
     .agent/plan.md                            |  40 ++--
     .agent/prose_slips.md                     |   6 +-
     packages/orchestration/model_routing.py   | 130 ++++++++++++
     tests/orchestration/test_model_routing.py | 211 +++++++++++++++++++
     7 files changed, 803 insertions(+), 174 deletions(-)
    REAL_EXIT=0

    $ git diff --stat 05d78941..7349421a -- docs/
    (no output — NO path under docs/ is listed, so
     docs/agents/model_routing_policy.md is not among them)
    REAL_EXIT=0

Insertion counts, the `+` column ONLY (AGENTS.md DECISION F104 D1), from
`git show --numstat`, compared CELL BY CELL against the Commits table above:

    step commit    path                                          numstat+   table+  agree
    C0a  34f075dd  .agent/authored/f110-r4.md                         259      259    yes
    C0b  f7b9ae57  .agent/last_block.md                               175      175    yes
    C1   a36addc9  .agent/plan.md                                      20       20    yes
    C2   310999d2  .agent/live_review.md                                3        3    yes
    C2   310999d2  .agent/prose_slips.md                                5        5    yes
    C3   2e22062e  packages/orchestration/model_routing.py            130      130    yes
    C4   7349421a  tests/orchestration/test_model_routing.py          211      211    yes

Per-commit insertion totals: C0a 259, C0b 175, C1 20, C2 8, C3 130, C4 211. Every
one is far under the 500-insertion cap. C5's own numbers go to NEITHER a round
report NOR this file, per the block: the reviewer measures them at the next gate.

**THE STALENESS SWEEP over every file this round touched, one entry per file.**

1. `.agent/authored/f110-r4.md` — NOT stale by construction. A verbatim copy of
   the reviewer's block; nothing in it is edited regardless of what any later
   measurement shows. Its own G1 projection of 259 happens to be exactly right
   this round, so there is not even a difference to leave standing.
2. `.agent/last_block.md` — NOT stale, same reason, same bytes, same digest.
3. `.agent/plan.md` — NOT stale. Its `## Current Step` describes exactly what this
   round did: the new module, the sync test, the `unknown_class_conservative`
   reason and the booked round 3 verdict, all four of which landed. `## Next
   Steps` names T002b (the hard rules) FIRST and says in its own words why they
   are not in round 4, which is constraint 6 restated where a reader will look for
   the absence. Its first Risk bullet ("The table is not wired to any call site
   yet, by design") is confirmed by G5 and G8: no caller was edited and nothing
   outside the two new files moved. 46 lines, under the AGENTS.md 50-line rule.
4. `.agent/live_review.md` — NOT stale. One `Gate:` paragraph appended for round
   3's PASS; no registration or resolution line was written or edited. Measured at
   BASE and at HEAD with the SAME method: registered ids identical, resolved ids
   identical, the open set unchanged, and the sets of ids added by this round both
   empty. See D4 on the counting method.
5. `.agent/prose_slips.md` — NOT stale. Two dated records of reviewer prose slips;
   both are statements about round 3 and are true of it. Append-only, never
   renumbered, and nothing here gates anything. The second one institutes nothing
   new — it reports that the `wc -l` counter-measure SLIPS3 instituted worked —
   and this round's G1 ran it again and reported the reading either way.
6. `packages/orchestration/model_routing.py` — NOT stale, and written not to go
   stale. The module docstring says the sync test is what keeps it and the
   document equal, which G6 proves in both directions rather than asserts. It
   names its own deliberate absences where a reader would search for them
   (AGENTS.md Code Discoverability): no model id here, and no production importer
   yet. Both statements are true at this commit — `TOP_TIER` is derived from
   `MODEL_TIERS[-1]` rather than re-spelled, so the tier order has exactly one
   source. It carries no hard rule, per constraint 6.
7. `tests/orchestration/test_model_routing.py` — NOT stale. It asserts no model
   id, so no repointing of the alias table can falsify it, and every expectation
   is either derived from the module's own table (the resolver tests) or read from
   the document (the sync test). The one literal it pins by hand is the reason
   token `unknown_class_conservative`, which is pinned ON PURPOSE: it is a fixed
   string the feature file specifies and evidence readers group on, so it must not
   be free to drift with a refactor.
8. `.agent/handoff.md` — this file; written once, per the write-once rule.

NOTHING OUTSIDE THE CHANGE SET WAS EDITED. Sentences outside it that this round
makes stale are DECLARED, NOT REPAIRED, per constraint 8 — see D2 and D3.

## Authored-text proofs

Every applied reviewer-authored text was extracted by delimiter index from the
COMMITTED `.agent/authored/f110-r4.md` (read with
`git show HEAD:.agent/authored/f110-r4.md`, not from the working copy) and written
to its target BY SCRIPT. Nothing was retyped.

| Authored text | Proof | Expected | Read | Exit |
|---|---|---|---|---|
| the whole block | `sha256sum` of `.agent/authored/f110-r4.md` and `.agent/last_block.md` | one digest twice | `5b0a1248…6dc2` twice | 0 |
| the whole block | `wc -l .agent/authored/f110-r4.md` | projection 259 | 259 — exact, nothing to report | 0 |
| PLAN4 (46 lines, 2255 bytes) | `cmp .remedy-wt/f110r4/PLAN4.extracted .agent/plan.md` | identical | identical | 0 |
| RECORD3 (4611 bytes applied) | append arithmetic + paragraph-order second reader + negative control | exact / in order / rejected | exact / in order / rejected | — |
| SLIPS4 (1425 bytes applied) | final-bytes byte-equality + exact byte prefix + newline convention | True / True / True | True / True / True | — |

The production code and the tests are NOT authored text: the block described them
and the worker wrote them (SPEC CODE, SPEC TESTS), so they carry no transport
proof and are gated by G5, G6 and G7 instead.

## Deviations & assumptions

**D0 — NONE OF THE BLOCK'S ORDERED COMMIT SEQUENCE WAS DEPARTED FROM.** C0a, C0b,
C1, C2, C3, C4, C5 ran in exactly that order, with exactly the eight paths the
change set names and nothing else. No commit was added, dropped or reordered.
Constraint 3's fixed order — production BEFORE tests — was honoured. This entry
exists because the handback template asks for the departure to be named HERE even
when there is none.

**D1 — I RAN A THIRD, UNORDERED MUTATION IN G6 AND AM DECLARING IT AS AN
ADDITION.** The block orders TWO mutations; I made three. The third — adding a
SECOND non-arrow rule bullet to the worktree's document — is not a substitute for
either ordered one, both of which ran and are reported in full above it. I made it
because SPEC TESTS (e) puts a specific claim on disk ("a future editor who adds a
second rule bullet turns this test red instead of having it ignored") that neither
ordered mutation exercises, and a claim that ships untested is what this round is
meant to avoid. The result is worth the reviewer's attention: three ids redden,
and `test_the_parsed_seed_mapping_equals_the_module_table` STAYS GREEN — so the
mapping-equality assertion on its own really would have passed over the change,
exactly as the reviewer warned. It ran inside the same disposable worktree, was
reverted by exact path, and the revert was proved.

**D2 — A STALE SENTENCE OUTSIDE THE CHANGE SET, DECLARED AND NOT REPAIRED:
`docs/agents/model_routing_policy.md`'s OWN HEADER.** It reads "Seeds routing.py's
class→model map". Two things about that are now inexact: the module is named
`model_routing.py`, not `routing.py` (the feature file's Design section suggested
`routing.py`; the repo already has a `builder_routing.py`, so the 2-4 word
domain-carrying name in AGENTS.md Code Discoverability points at
`model_routing.py`), and the seeded map is class→TIER, not class→model — this
round deliberately maps to tiers, and which model serves a tier is a later
question. The document is READ by the sync test and is explicitly NOT in the
change set (the block says so twice), so it is declared here and left alone. It
needs a path in a later round's change set.

**D3 — A SECOND STALE SENTENCE OUTSIDE THE CHANGE SET:
`docs/roadmap/features/T3_F110.md`'s "Do not touch" section.** It suggests
`tests/orchestration/test_routing.py` as the test path; the file shipped is
`tests/orchestration/test_model_routing.py`, named after the source it covers per
AGENTS.md Code Discoverability ("Test files are named after the source they
cover"). A suggestion is not a rule and the rule wins, but the suggested name is
now the one that does not exist. `docs/roadmap/**` is not in the change set and a
round touching it would also owe `tests/orchestration/test_roadmap_index.py`
(context.md), so it is declared and not repaired. Round 3's D3, D4 and D5 —
`apps/cli/commands/mission_cmd.py`'s docstring, `packages/orchestration/intake.py`'s
docstring and `.agent/f110_inventory.md` section E — are all STILL OPEN and still
outside this round's change set; the plan's second Risk bullet now carries the
first of them so it is not lost.

**D4 — MY OPEN-FINDING MEASUREMENT DISAGREES WITH ROUND 3'S BY FOUR, AND I AM
REPORTING BOTH RATHER THAN PICKING ONE.** My script counts registered ids as the
ledger's entry lines (`- R-nnnn — `) and resolved ids as those a `RESOLVED` clause
names within 80 characters. It reads 347 registered — which reproduces round 3's
347 exactly — but 65 resolved and 282 open, where round 3's handback states 69 and
278. The difference is in the RESOLVED heuristic, not on disk: I ran the identical
script against `05d78941:.agent/live_review.md` and against HEAD and got the same
347 / 65 / 282 at both, with the set of ids added by this round EMPTY in both
directions. THE LOAD-BEARING FACT IS THE DELTA, AND IT IS ZERO: this round
registers no finding and resolves none. I did not adopt round 3's absolute figure
as my own measurement, because I cannot reproduce it with a method I can show, and
writing an unmeasured number would be worse than declaring the gap.

**D5 — TWO REPORTED VALUES THE BLOCK DID NOT ORDER, ADDED BECAUSE THEY BOUND A
CLAIM.** (i) G3 additionally reports the live_review arithmetic re-read from the
git object at `310999d2^`, not only from the pre-commit measurement, so the
"before" size is not a remembered number. (ii) G6 reports the failure MESSAGE of
each mutation, not only the reddened id, because "the same one id reddens for both
mutations" is a weaker claim than it looks until you can see that the two failures
say different things about which side moved.

**D6 — SEMANTIC CHOICES THE SPEC LEFT OPEN, ALL OF THEM DECLARED.** (i) The reason
string for a KNOWN class is `seed_mapping`; SPEC CODE (d) says only "a reason
naming the seed mapping" and does not fix the token, so I exported it as
`SEED_MAPPING_REASON` and the tests assert through the constant rather than the
literal — the unknown reason, which the feature file DOES fix, is asserted as a
literal on purpose. (ii) The tier names are `cheap`, `mid`, `top` — the first word
of each right-hand side in the document, which is also what the parse in SPEC
TESTS (e) yields, so the code and the parser cannot disagree about the vocabulary.
(iii) An EMPTY or whitespace-only task class normalizes to `""`, which is in no
table, so it resolves to the top tier with `unknown_class_conservative`; that is
the conservative reading of the same rule and it is tested. (iv) `TOP_TIER` is
derived as `MODEL_TIERS[-1]` rather than written out, so constraint (a)'s
"stated once" holds literally.

**D7 — NO RUFF GATE WAS ORDERED AND I ADDED NONE**, per constraint 5. I say
nothing about lint in the code, the commits or the tests; the reviewer lints C3
and C4 itself. `.agent/context.md`'s ruff bullet is untouched and still invites a
gate this worker's permission layer refuses.

**D8 — THE SCRATCH IS LEFT IN PLACE UNDER `.remedy-wt/f110r4/`.** The extractor,
the append and second-reader scripts, the negative control, the G8 cell
comparison, the open-set scripts, the extracted slices and the mutated ledger
copy. All of it is gitignored, `git ls-files .remedy-wt` returns nothing, and
nothing was deleted by glob. It is left deliberately so the reviewer can re-run
every gate from the same inputs. The G6 worktree, by contrast, WAS removed and
pruned, as ordered.

**D9 — A NAME COLLISION I FOUND WHILE MEASURING CONSTRAINT 7, DECLARED AND NOT
ACTED ON, BECAUSE THE FIX IS NOT THIS ROUND'S AND MAY NOT BE ANYONE'S.** The word
"tier" already means something else in this repo.
`packages/orchestration/orchestrator_brain.py` carries
`OrchestratorModelRoutingPlan` with a field `tier`, whose vocabulary is
`HUMAN_REVIEW_REQUIRED`, `EXTERNAL_BUILDER_NEEDED`, `local_advisor_preferred` —
WHEN to escalate a job, not WHICH model a task class gets. It surfaces as
`model_routing_plan.tier` in the ledger, the review bundle, the UI server and the
CLI, and as `model_routing_tier` in three JSON payloads. My new module's
`MODEL_TIERS` (`cheap`/`mid`/`top`) is a DIFFERENT vocabulary under a
near-identical name, which is the synonym-drift AGENTS.md Code Discoverability
warns about. I did not rename anything: mass renames of existing code are
FORBIDDEN as their own activity by that same section, `orchestrator_brain.py` is
not in the change set, and the two names are at least distinguishable
(`model_routing_plan.tier` against `MODEL_TIERS`). `.agent/context.md` already
records the analogous distinction for `builder_routing.py`. Flagged so the
reviewer decides whether F110's later rounds should name the concept more
sharply BEFORE anything else imports it — which is cheap now and expensive after
the call-site declarations land.

**Assumptions.** (i) The block's statement that the reviewer holds no scratch
original is taken at face value, so G1 is reported as self-consistency and not as
transport — the weaker claim, on purpose. (ii) "The lines between the heading and
the next heading that begin with `- `" is implemented as a prefix match on
`## Seed mapping` and `## Hard rules`, and the parser ASSERTS the first heading
occurs exactly once, so a duplicated section is an error rather than a silent
first-match. (iii) `.remedy-wt/` is gitignored session scratch that PERSISTS,
which is what makes D8's decision to leave it the right one. (iv) Constraint 7's
"imported by its test and by nothing else" was MEASURED, not assumed:
`grep -rn "model_routing" --include=*.py .` over the repo returns no importer of
`packages.orchestration.model_routing` outside
`tests/orchestration/test_model_routing.py`. Every other hit is a different
identifier — `model_routing_plan`, `model_routing_tier`, or the policy document's
path — which is the subject of D9.

## Next

REVIEW ROUND 4 AND ISSUE A VERDICT — lint `2e22062e` and `7349421a`
reviewer-side, since constraint 5 routes that to the reviewer, and re-run both of
G6's mutations plus the unordered third — then author round 5 as T002b: the three
hard rules, each a named check with a violating fixture refused with the rule
named, which is what constraint 6 deferred out of this round. The next session's
first action is Phase 1 rule 1 — read `.agent/STOP` from disk — before Phase 1
rule 2, the Open PR Gate, which is currently satisfied: no pull request is open,
because none was created. D2 and D3 need a path in a later block's change set, as
do round 3's still-open D3, D4 and D5.
