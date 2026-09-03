# Handback — F110 Model routing by task class, round 5 — T002b, THE THREE HARD RULES

## Session

SESSION 1 of feature F110 · round 5 · rounds so far 5

Soft limit is 25 rounds / 7 sessions (self_drive_protocol.md G7, amend0827 rule
6). At 5 rounds and 1 session it is nowhere near, so no scope report is due.
`.agent/STOP` was read from disk twice — before the first commit (C0a) and again
before C5 — and does not exist at either point.

THIS IS THE LAST ROUND OF THE SESSION, as the block states.

## State

| Feld | Wert |
|------|------|
| **Feature** | F110 Model routing by task class (Tier 3, depends on F103) |
| **Branch** | `feature/f110-model-routing-by-task-class` |
| **BASE** | `7a4d381f` — the round 4 handback commit |
| **Runde** | 5 (Session 1) — T002b: the three hard rules as named checks, each with a violating fixture refused with the rule named |
| **Fortschritt** | ~60 % (T001a ✅ · T001b ✅ · T001c ✅ · T002a ✅ class table + sync test · T002b ✅ the three hard rules · T002c, T003 open) — Schätzung |
| **Gates** | G1-G8 alle ausgeführt, echte Exit-Codes und echte Ausgaben unten. ALLE GRÜN. |
| **Offene Findings** | 278, UNVERÄNDERT gegen Runde 4 — diese Runde registriert nichts und löst nichts auf. Gemessen unter der KANONISCHEN Lesart, die das Runde-4-Urteil festgeschrieben hat; sie reproduziert 347 / 69 / 278 exakt (siehe D7 — die Meinungsverschiedenheit aus Runde 4 D4 ist damit erledigt) |

THIS ROUND SHIPS THE ACCEPTANCE LINE THE FEATURE FILE NAMES SECOND. Each of the
three hard rules is a named check in `packages/orchestration/model_routing.py`
that returns ITS OWN rule-name constant when violated and `None` when it is not,
and each has a violating fixture in `tests/orchestration/test_model_routing.py`
that is refused WITH THE RULE NAMED — asserted against the constant, never
against a retyped literal. A collecting validator returns EVERY violated rule
name at once, in a declared order independent of `MODEL_TIERS`. Nothing is wired
to a call site and no config file is read or written (constraint 6); the config
schema that calls these checks is T002c.

THE SAFETY RULE IS PROVEN NON-VACUOUS, which is what the reviewer's second note
asked for. `SAFETY_RELEVANT_CLASSES` is an EMPTY frozenset in production, so a
check written against that constant alone could never refuse anything. The check
therefore takes the class set as a PARAMETER defaulting to that constant; the
tests supply a FIXTURE set and prove the refusal really happens (G5 and G6 both
show it firing), a separate test asserts the production constant is empty TODAY,
and a further test states in assertion form that the production default therefore
refuses nothing. The emptiness is now a property under test rather than an
accident nobody would notice changing.

WHERE EACH RULE COMES FROM, because they do not all come from one document, and a
reader comparing the code to `docs/agents/model_routing_policy.md` alone will
otherwise find one rule too many:

| Code rule name | Source |
|---|---|
| `reviewer_weaker_than_worker` | policy document, Hard rules, rule 1 |
| `orchestration_below_top_tier` | `docs/roadmap/features/T3_F110.md`, Design — "orchestrator and mission-compile calls always top tier" |
| `safety_class_below_mid_tier` | policy document, Hard rules, rule 2 ("no silent downgrade of security-relevant roles") |

The policy document's Hard rule 3 — "routed_model + reason land in evidence for
every call" — is NOT one of these checks: it is an evidence obligation, not a
routing refusal, and it belongs to T003. The class table already carries the
`reason` half of it (`SEED_MAPPING_REASON` / `UNKNOWN_CLASS_REASON`, round 4).

## Range

Review of `7a4d381f..HEAD` (HEAD is the commit this file is written in).

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C0a `98be993b` | done | block written verbatim to `.agent/authored/f110-r5.md`, 252 insertions |
| C0b `a31d97cc` | done | mirrored with `shutil.copyfile`; one sha256 for both copies (G1) |
| C1 `9dabdd5a` | done | PLAN5 extracted by delimiter index from the COMMITTED authored copy and applied whole; `cmp` exit 0, 45 lines. FIRST substantive commit, item 23 |
| C2 `939a31d8` | done | RECORD4 appended to `.agent/live_review.md` and SLIPS5 to `.agent/prose_slips.md`, each with the two-byte separator; full arithmetic in G3, byte-equality in G4 |
| C3 `e1c28478` | done | THE PRODUCTION COMMIT — the three hard rules, the tier-rank helper, `MID_TIER`, the rule-name constants and the collecting validator. 227 insertions, **0 deletions** (G5) |
| C4 `7e2035fa` | done | THE TEST COMMIT — the violating and conforming fixtures; the file grows 48 → 127 tests |
| C4b `0f4ece46` | **deviated** | AN EXTRA, UNORDERED COMMIT. The module's opening docstring still read "Owns the CLASS TABLE and nothing else yet", which C3 made FALSE. Repaired on a path the change set already names. Fully declared in D1, and G6 was re-run at this commit so the red proof pins the SHIPPED code |
| C5 (this commit) | done | handback rewritten per `docs/agents/handback_template.md` |

Every ordered item appears exactly once. No ordered item was skipped. Constraint
3's order — C3 production BEFORE C4 tests — was honoured; C4b is an ADDITIONAL
production commit placed after C4, which reorders nothing but is a departure from
the ordered bundle and is declared as one.

## Commits

### 98be993b F110 R5 C0a: save the round 5 block verbatim
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f110-r5.md` | +252 / -0 | the reviewer's block saved verbatim; the first link of the transport chain |

### a31d97cc F110 R5 C0b: mirror the round 5 block to last_block
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/last_block.md` | +161 / -168 | round 4's block replaced by this one; byte-identical copy of the authored file |

### 9dabdd5a F110 R5 C1: the plan turns to T002b, the three hard rules
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/plan.md` | +17 / -18 | PLAN5 applied whole; 45 lines, under the AGENTS.md 50-line rule |

### 939a31d8 F110 R5 C2: book the round 4 PASS verdict and its prose slip
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/live_review.md` | +3 / -1 | RECORD4 appended — round 4's PASS verdict, booked in the first round that was happening anyway (amend0827 rule 1, item 23) |
| `.agent/prose_slips.md` | +3 / -1 | SLIPS5 appended — ONE dated reviewer prose slip this round; no R-id spent (amend0827 rule 2) |

### e1c28478 F110 R5 C3: enforce the three hard rules as named checks
| Path | +/- | Reason |
|------|-----|--------|
| `packages/orchestration/model_routing.py` | +227 / -0 | `MID_TIER`, `model_tier_rank`, the three rule-name constants, `HARD_RULE_NAMES`, `ORCHESTRATION_TASK_CLASSES`, `SAFETY_RELEVANT_CLASSES`, the three checks and `validate_routing_choice`. PURE INSERTION — zero deletions, so constraint 7's table is untouched |

### 7e2035fa F110 R5 C4: a violating fixture per hard rule, refused with the rule named
| Path | +/- | Reason |
|------|-----|--------|
| `tests/orchestration/test_model_routing.py` | +273 / -1 | five new test classes; every rule-name assertion goes through the module constant. The one deletion is the file's first docstring line, which named T002a only — see D3 |

### 0f4ece46 F110 R5 C4b: the module docstring no longer says it owns the table and nothing else
| Path | +/- | Reason |
|------|-----|--------|
| `packages/orchestration/model_routing.py` | +5 / -2 | EXTRA, UNORDERED. Repairs a sentence C3 falsified, inside the change set. D1 |

### C5 (this commit) F110 R5 C5: the round 5 handback
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/handoff.md` | rewrite | a handoff cannot table the commit that writes it (R-0149 pattern). Its own numbers go to neither a round report nor this file, per the block: the reviewer measures them at the next gate |

The `+` column above is the INSERTION count from `git show --numstat`
(AGENTS.md DECISION F104 D1). The cell-by-cell comparison is in G8.

## External actions

| Command | Outcome |
|---|---|
| `git worktree add --detach .remedy-wt/f110r5_mut 7e2035fa` | `Preparing worktree (detached HEAD 7e2035fa)` — the FIRST G6 red proof ran ONLY here |
| `git -C .remedy-wt/f110r5_mut restore packages/orchestration/model_routing.py` | run THREE times, once per mutation, by EXACT PATH; worktree `git status --porcelain` empty and 127 passed after each |
| `git worktree remove .remedy-wt/f110r5_mut` · `git worktree prune` | removed and pruned |
| `git worktree add --detach .remedy-wt/f110r5_mut2 0f4ece46` | `Preparing worktree (detached HEAD 0f4ece46)` — the SECOND G6 red proof, re-run at the FINAL code commit so the proof pins the shipped bytes (D2) |
| `git -C .remedy-wt/f110r5_mut2 restore packages/orchestration/model_routing.py` | run THREE times, once per mutation, by EXACT PATH; worktree status empty and 127 passed after each |
| `git worktree remove .remedy-wt/f110r5_mut2` · `git worktree prune` | removed and pruned; `git worktree list` afterwards shows no worktree of this round's making |
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
| G1 TRANSPORT | GREEN — one sha256 twice, `57dc4b6e…616e`; `wc -l` reads **252**, EXACTLY the reviewer's projection of 252. WORKER SELF-CONSISTENCY ONLY: the reviewer stated it holds no scratch original, so this proves the mirror equals the saved copy and nothing about the emitted bytes (§3 item 37). Second consecutive exact projection; well under the cap of 400 |
| G2 THE PLAN | GREEN — `cmp` exit 0, 45 lines (< 50), `^## Goal` 1, `^## Next Steps` 1 |
| G3 THE LEDGER APPEND | GREEN — 2158520 + 2 + 5941 = 2164463 real; the second reader accepts the last 1 unit IN ORDER; the negative control REJECTS; the grep reads 0 before C2 (exit 1) and 1 after (exit 0) |
| G4 THE PROSE FILE | GREEN — `.agent/prose_slips.md` final 978 bytes byte-equal to the extracted SLIPS5, pre-C2 content an exact byte PREFIX, file still ends WITHOUT a newline |
| G5 THE MODULE | GREEN — `git show --numstat e1c28478` reads **227 insertions and 0 DELETIONS**, so constraint 7's round 4 table is provably unrevised; `ast.parse` over the real text raises nothing; the SHIPPED CODE was RUN and every check, the validator and the rank helper returned the values transcribed below, including the empty production safety set |
| G6 THE RED PROOF | GREEN, AND THE DISCRIMINATOR HOLDS FOR ALL THREE — control 127 passed exit 0; each mutation reddens ITS OWN rule's violating fixture AND the collecting-validator case, with the OTHER TWO rules' fixtures GREEN in every case (0 cross-red ids). (i) 6 red, (ii) 8 red, (iii) 4 red, each exit 1. Run twice — at C4 and again at C4b — with identical results; both worktrees removed and pruned |
| G7 THE SUITES | GREEN — 127, 33, 34, 295, 42, each its own invocation, run serially, every one exit 0. The first GREW from 48 to 127; the last four match the reviewer's base measurements EXACTLY, so no count moved |
| G8 THE TREE, THE COMMITS AND THE SWEEP | GREEN — tree EMPTY before C5 was staged, `git ls-files .remedy-wt` no output, no worktree of this round's making, `git diff --stat 7a4d381f..0f4ece46 -- docs/` lists NOTHING, all seven ordered-commit insertion cells agree |

### G1 TRANSPORT — GREEN

    $ sha256sum .agent/authored/f110-r5.md .agent/last_block.md
    57dc4b6e31f317deb326a0624f292088d25146786d1c58d34d0610834fe7616e  .agent/authored/f110-r5.md
    57dc4b6e31f317deb326a0624f292088d25146786d1c58d34d0610834fe7616e  .agent/last_block.md
    REAL_EXIT=0

    $ wc -l .agent/authored/f110-r5.md
    252 .agent/authored/f110-r5.md
    REAL_EXIT=0

One digest, twice, both lines verbatim. The reviewer stated up front that it
holds no scratch original this round, so this is WORKER SELF-CONSISTENCY ONLY: it
proves the mirror equals the saved copy and nothing about what the reviewer
emitted. That is the §3 item 37 shape and it is reported as such.

THE `wc -l` READING IS 252 AGAINST A PROJECTION OF 252 — no difference, so there
is nothing to report and nothing to repair. That is the second consecutive exact
projection for this feature, after rounds 1, 2 and 3 were low by 1, 1 and 3. The
committed file is 21531 bytes; the cap is 400 lines.

Every APPLIED slice below was extracted BY DELIMITER INDEX from the COMMITTED
`.agent/authored/f110-r5.md` — read with `git show HEAD:.agent/authored/f110-r5.md`,
never from the working copy — and written to its target BY SCRIPT. Nothing was
retyped. Each marker string was asserted to occur EXACTLY ONCE before any write
(the extractor raises otherwise), and the extractor also asserts the END marker
follows its BEGIN.

    PLAN5    begin line 198  end line 244   45 lines   2174 bytes (with trailing newline)   2173 without
    RECORD4  begin line 246  end line 248    1 line    5942 bytes (with trailing newline)   5941 without
    SLIPS5   begin line 250  end line 252    1 line     979 bytes (with trailing newline)    978 without

Constraint 4 settles which form each target takes: `.agent/plan.md` ends WITH a
newline and took the 2174-byte form; `.agent/live_review.md` and
`.agent/prose_slips.md` end WITHOUT one and took the 5941 / 978 forms. The
TARGET's convention wins, exactly as ordered.

### G2 THE PLAN — GREEN

    $ cmp .remedy-wt/f110r5/PLAN5.extracted .agent/plan.md
    (no output)
    REAL_EXIT=0
    $ wc -l .agent/plan.md
    45 .agent/plan.md            (must be under 50 — it is)
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

    BEFORE C2:  $ grep -c '^Gate: F110 R4 — ' .agent/live_review.md   -> 0   REAL_EXIT=1
    AFTER  C2:  $ grep -c '^Gate: F110 R4 — ' .agent/live_review.md   -> 1   REAL_EXIT=0

RECORD4 at C2, against the file size IMMEDIATELY BEFORE that commit, read from the
git OBJECT at `939a31d8^` rather than from a remembered number:

    size BEFORE C2                      2158520
    separator bytes                           2   (newline newline)
    RECORD4 slice length                   5941   (extractor yields 5942; the target takes no trailing newline)
    before + 2 + slice                  2164463
    real new size                       2164463
    equal                                  True
    new file ends WITHOUT a newline        True
    pre-append content an exact PREFIX     True
    final 5941 bytes equal the slice       True

The 2158520 matches the block's own stated base size exactly, so the append
started where the reviewer measured it would.

A SECOND READER THAT COUNTS NO BYTE. The WHOLE file was split on blank-line
boundaries. N was counted BY THE SCRIPT from the slice, never taken from the
block: N = 1.

    N counted BY THE SCRIPT from the slice   1
    blank-line units in the WHOLE file       901
    unit[-1] equals slice paragraph 1: True (len 5912 vs 5912 characters)
    last N file units == slice paragraphs IN ORDER:   True

The byte length (5941) and the character length (5912) differ because the
paragraph carries multi-byte characters; both readings are of the same string and
neither is a discrepancy.

NEGATIVE CONTROL, on a SCRATCH COPY under `.remedy-wt/` — the tracked file was
never mutated:

    first appended paragraph found at byte offset   2158522
    flipped byte at offset 2158622 (was b'T') with XOR 0x01
    second reader ACCEPTS the mutated copy:         False
    second reader REJECTS it:                       True
    (the mutated copy still reports 901 units and still matches on LENGTH,
     5912 vs 5912 — so the rejection is a content comparison, not a size one)
    tracked file untouched (still the real size):   True

### G4 THE PROSE FILE — GREEN, BYTE-EQUALITY ONLY

Which is all amend0827 rule 5 allows a `.agent/` prose file. Re-checked AFTER C2
landed, with the pre-C2 bytes read from the git OBJECT at `939a31d8^`:

    size BEFORE C2 (from the git object)                        52515
    separator bytes                                                 2
    SLIPS5 slice length                                           978
    before + 2 + slice                                          53495
    real new size                                               53495
    equal                                                        True
    final 978 bytes equal the extracted SLIPS5 slice:            True
    pre-C2 content preserved as an exact byte PREFIX:            True
    file still ends WITHOUT a newline:                           True

### G5 THE MODULE, MEASURED AND RUN — GREEN

    $ git show --numstat e1c28478 -- packages/orchestration/model_routing.py
    227	0	packages/orchestration/model_routing.py
    REAL_EXIT=0

THE DELETIONS NUMBER IS **0**, which is the number the block says matters. C3 is a
PURE INSERTION: not one line of round 4's module was removed or rewritten, so
`TASK_CLASS_TIERS`, `MODEL_TIERS`, `normalize_task_class` and
`resolve_task_class_tier` are byte-identical to round 4, and constraint 7 holds by
measurement rather than by assertion. Round 4's 48 tests were re-run against the
mutated module before C3 was committed and all 48 passed. There is no deleted line
to describe, because there is none.

The LATER commit C4b does carry 2 deletions on the same path, and they are
DOCSTRING PROSE ONLY. The two deleted lines are:

    Owns the CLASS TABLE and nothing else yet: which model TIER a declared task
    class is routed to. The table is SEEDED from the "Seed mapping" section of

They were replaced by five lines saying the module now owns the class table AND
the three hard rules. No executable line was touched; see D1.

    ast.parse over the real text: OK (no exception)

THE SHIPPED CODE WAS RUN, not read. These are the real returns, from the FINAL
committed module:

    module __file__: /home/decodeux/Repos/remedy/packages/orchestration/model_routing.py
    MODEL_TIERS = ('cheap', 'mid', 'top')   TOP_TIER = 'top'   MID_TIER = 'mid'

    THE TIER-RANK HELPER, on each of the three tiers and on an unknown tier:
       model_tier_rank('cheap')     -> 0
       model_tier_rank('mid')       -> 1
       model_tier_rank('top')       -> 2
       model_tier_rank('gigantic')  -> RAISED ValueError: unknown model tier 'gigantic';
                                       MODEL_TIERS names ('cheap', 'mid', 'top')

    RULE 1 — reviewer never weaker than the paired worker:
       VIOLATING   check_reviewer_not_weaker_than_worker('top', 'cheap')   -> 'reviewer_weaker_than_worker'
       CONFORMING  check_reviewer_not_weaker_than_worker('mid', 'mid')     -> None
       CONFORMING  check_reviewer_not_weaker_than_worker('cheap', 'top')   -> None

    RULE 2 — orchestrator and mission-compile always top tier:
       ORCHESTRATION_TASK_CLASSES = ['mission_compile', 'orchestrator']
       VIOLATING   check_orchestration_class_routed_to_top_tier('orchestrator', 'mid')      -> 'orchestration_below_top_tier'
       VIOLATING   check_orchestration_class_routed_to_top_tier('Mission Compile', 'cheap') -> 'orchestration_below_top_tier'
       CONFORMING  check_orchestration_class_routed_to_top_tier('orchestrator', 'top')      -> None
       OUT OF SCOPE check_orchestration_class_routed_to_top_tier('format', 'cheap')         -> None

    RULE 3 — a safety-relevant class never below mid:
       THE PRODUCTION SET:  SAFETY_RELEVANT_CLASSES = frozenset()   len = 0
       fixture set used:    ['dod_evaluation', 'fence_evaluation']
       VIOLATING   check_safety_relevant_class_not_below_mid_tier('fence_evaluation', 'cheap', FIXTURE) -> 'safety_class_below_mid_tier'
       CONFORMING  check_safety_relevant_class_not_below_mid_tier('fence_evaluation', 'mid', FIXTURE)   -> None
       PRODUCTION DEFAULT check_safety_relevant_class_not_below_mid_tier('fence_evaluation', 'cheap')   -> None

    THE COLLECTING VALIDATOR:
       HARD_RULE_NAMES = ('reviewer_weaker_than_worker', 'orchestration_below_top_tier', 'safety_class_below_mid_tier')
       BREAKS ALL THREE:
         validate_routing_choice('orchestrator', 'cheap', paired_worker_tier='top',
                                 safety_relevant_classes=frozenset({'orchestrator'}))
         -> ('reviewer_weaker_than_worker', 'orchestration_below_top_tier', 'safety_class_below_mid_tier')
       CONFORMING:
         validate_routing_choice('orchestrator', 'top', paired_worker_tier='top',
                                 safety_relevant_classes=frozenset({'orchestrator'}))
         -> ()

THE LAST LINE OF THE RULE 3 BLOCK IS THE HONEST ONE AND IT IS REPORTED AS IT
RETURNED: with the PRODUCTION default, a class that would violate the rule gets
`None`, because the production set is empty. That is the vacuity the reviewer
warned about, and it is why the parameter and the fixture set exist. It is stated
here, documented at the constant, and asserted by two tests.

### G6 THE RED PROOF — GREEN, AND THE DISCRIMINATOR HOLDS FOR ALL THREE RULES

Ran ONLY inside disposable worktrees, never in the primary checkout. `__pycache__`
was purged (a freshly added worktree has none, and `-B` writes none) and the
imported module path was printed from inside the worktree first, so each mutation
demonstrably reaches the test rather than being shadowed by an installed copy or
by the parent checkout.

    $ git worktree add --detach .remedy-wt/f110r5_mut 7e2035fa
    Preparing worktree (detached HEAD 7e2035fa)
    HEAD is now at 7e2035fa F110 R5 C4: a violating fixture per hard rule, refused with the rule named
    REAL_EXIT=0

    __pycache__ dirs inside the worktree: 0
    imported module file inside the worktree:
    /home/decodeux/Repos/remedy/.remedy-wt/f110r5_mut/packages/orchestration/model_routing.py

THE UNMUTATED CONTROL FIRST, as ordered:

    --- CONTROL, UNMUTATED ---
    $ python3 -B -m pytest tests/orchestration/test_model_routing.py -q
    127 passed in 0.36s
    REAL_EXIT=0

Each mutation replaces exactly ONE line — the `return <RULE NAME>` inside that
rule's check — with `return None`, so the check NEVER REFUSES. The script asserts
the target line occurs EXACTLY ONCE in the module before writing, and reverts by
exact path afterwards.

MUTATION (i) — RULE 1, reviewer-never-weaker, always returns None:

    -        return RULE_REVIEWER_WEAKER_THAN_WORKER
    +        return None

    $ python3 -B -m pytest tests/orchestration/test_model_routing.py -q
    6 failed, 121 passed in 0.33s
    REAL_EXIT=1

    THE IDS THAT WENT RED (6):
    TestReviewerNeverWeakerThanTheWorker::test_a_weaker_reviewer_is_refused_with_the_rule_named[mid-cheap]
    TestReviewerNeverWeakerThanTheWorker::test_a_weaker_reviewer_is_refused_with_the_rule_named[top-cheap]
    TestReviewerNeverWeakerThanTheWorker::test_a_weaker_reviewer_is_refused_with_the_rule_named[top-mid]
    TestRoutingChoiceValidatorCollectsEveryViolation::test_a_choice_breaking_all_three_returns_all_three_rule_names
    TestRoutingChoiceValidatorCollectsEveryViolation::test_only_the_reviewer_rule_fires_for_a_plain_weak_reviewer
    TestRoutingChoiceValidatorCollectsEveryViolation::test_the_result_follows_the_declared_order_not_the_alphabet

    REVERTED BY EXACT PATH, revert PROVED:
    $ git -C .remedy-wt/f110r5_mut restore packages/orchestration/model_routing.py
    $ git -C .remedy-wt/f110r5_mut status --porcelain     -> '' (empty)
    $ python3 -B -m pytest ... -q                          -> 127 passed   REAL_EXIT=0

MUTATION (ii) — RULE 2, orchestration-always-top, always returns None:

    -        return RULE_ORCHESTRATION_BELOW_TOP_TIER
    +        return None

    $ python3 -B -m pytest tests/orchestration/test_model_routing.py -q
    8 failed, 119 passed in 0.33s
    REAL_EXIT=1

    THE IDS THAT WENT RED (8):
    TestOrchestrationCallsAlwaysTopTier::test_an_orchestration_class_below_top_is_refused_with_the_rule_named[cheap-mission_compile]
    TestOrchestrationCallsAlwaysTopTier::test_an_orchestration_class_below_top_is_refused_with_the_rule_named[cheap-orchestrator]
    TestOrchestrationCallsAlwaysTopTier::test_an_orchestration_class_below_top_is_refused_with_the_rule_named[mid-mission_compile]
    TestOrchestrationCallsAlwaysTopTier::test_an_orchestration_class_below_top_is_refused_with_the_rule_named[mid-orchestrator]
    TestOrchestrationCallsAlwaysTopTier::test_the_declared_class_may_be_spelled_as_the_document_words_it
    TestRoutingChoiceValidatorCollectsEveryViolation::test_a_choice_breaking_all_three_returns_all_three_rule_names
    TestRoutingChoiceValidatorCollectsEveryViolation::test_only_the_orchestration_rule_fires_for_a_cheap_orchestrator_call
    TestRoutingChoiceValidatorCollectsEveryViolation::test_the_result_follows_the_declared_order_not_the_alphabet

    REVERTED BY EXACT PATH, revert PROVED: status '' (empty), 127 passed, REAL_EXIT=0

MUTATION (iii) — RULE 3, safety-never-below-mid, always returns None:

    -        return RULE_SAFETY_CLASS_BELOW_MID_TIER
    +        return None

    $ python3 -B -m pytest tests/orchestration/test_model_routing.py -q
    4 failed, 123 passed in 0.32s
    REAL_EXIT=1

    THE IDS THAT WENT RED (4):
    TestSafetyRelevantClassNeverBelowMid::test_a_safety_class_below_mid_is_refused_with_the_rule_named[cheap-dod_evaluation]
    TestSafetyRelevantClassNeverBelowMid::test_a_safety_class_below_mid_is_refused_with_the_rule_named[cheap-fence_evaluation]
    TestRoutingChoiceValidatorCollectsEveryViolation::test_a_choice_breaking_all_three_returns_all_three_rule_names
    TestRoutingChoiceValidatorCollectsEveryViolation::test_only_the_safety_rule_fires_for_a_cheap_safety_class

    REVERTED BY EXACT PATH, revert PROVED: status '' (empty), 127 passed, REAL_EXIT=0

MUTATION (iii) IS THE ONE THE REVIEWER'S SECOND NOTE IS ABOUT. It reddens two
violating fixtures that only exist because the check takes its class set as a
PARAMETER. Had the check been written against the empty production constant
alone, this mutation would have reddened NOTHING and the proof would have been
FAILED — which is exactly the §3 item 27 defect the note names. It reddens, so the
rule is real.

THE DISCRIMINATOR, computed by the script from the red-id sets rather than
asserted:

    (i)   own fixture RED: True (3 ids) | collecting-validator RED: True (3 ids) | OTHER TWO rules' fixtures RED: 0 ids -> GREEN
          DISCRIMINATOR SATISFIED: True
    (ii)  own fixture RED: True (5 ids) | collecting-validator RED: True (3 ids) | OTHER TWO rules' fixtures RED: 0 ids -> GREEN
          DISCRIMINATOR SATISFIED: True
    (iii) own fixture RED: True (2 ids) | collecting-validator RED: True (2 ids) | OTHER TWO rules' fixtures RED: 0 ids -> GREEN
          DISCRIMINATOR SATISFIED: True

No mutation reddened everything and none reddened nothing, so there is no FAILED
proof to report. Each mutation reddens ITS OWN rule and the validator, and leaves
the other two rules' fixtures green — the three checks are genuinely independent,
not one rule wearing three names.

THE WHOLE PROOF WAS RUN TWICE (see D2). The transcript above is the run at
`7e2035fa` (C4). It was repeated in a second worktree at `0f4ece46` (C4b), the
final code commit, with IDENTICAL numbers: control 127 passed exit 0; (i) 6 failed
/ 121 passed; (ii) 8 failed / 119 passed; (iii) 4 failed / 123 passed; the same
red ids; the discriminator satisfied in all three; and 127 passed after each
revert. Both worktrees were removed and pruned.

    $ git worktree remove .remedy-wt/f110r5_mut2
    $ git worktree prune
    $ git worktree list
    /home/decodeux/Repos/remedy                                  0f4ece46 [feature/f110-model-routing-by-task-class]
    /home/decodeux/Repos/remedy/.remedy-wt/job-48a379ab5ca44ec5  f0e6b9a3 [remedy/job-48a379ab5ca44ec5]
    /home/decodeux/Repos/remedy/.remedy-wt/job-5e91e080219342d9  9fdb3b4b [remedy/job-5e91e080219342d9]
    /home/decodeux/Repos/remedy/.remedy-wt/job-7d1c93e2dc98415a  f0e6b9a3 [remedy/job-7d1c93e2dc98415a]
    /home/decodeux/Repos/remedy/.remedy-wt/job-98e9364a83a34872  21a45836 [remedy/job-98e9364a83a34872]
    /home/decodeux/Repos/remedy/.remedy-wt/job-f76686b8435640e9  4b49af98 [remedy/job-f76686b8435640e9]

No worktree of THIS round's making remains; the five `job-*` entries predate it.

### G7 THE SUITES — GREEN, EACH AS ITS OWN INVOCATION, RUN SERIALLY

Never two pytest processes alive at once. Every one below was re-run at the FINAL
commit `0f4ece46`, after C4b landed:

    $ python3 -m pytest tests/orchestration/test_model_routing.py -q
    127 passed in 0.29s
    REAL_EXIT=0

    $ python3 -m pytest tests/orchestration/test_orchestrator_model_routing.py tests/orchestration/test_job_role_routing.py -q
    33 passed in 0.32s
    REAL_EXIT=0

    $ python3 -m pytest tests/orchestration/test_role_config.py -q
    34 passed in 0.27s
    REAL_EXIT=0

    $ python3 -m pytest tests/docs/ -q
    295 passed in 0.54s
    REAL_EXIT=0

    $ python3 -m pytest tests/cli/test_golden_path.py -q
    42 passed in 20.67s
    REAL_EXIT=0

127, 33, 34, 295, 42. THE FIRST GREW FROM 48 TO 127 — 79 new cases — so the new
fixtures demonstrably landed; a count that did not grow would have meant they did
not. THE LAST FOUR MATCH THE REVIEWER'S BASE MEASUREMENTS EXACTLY — 33, 34, 295,
42 — so no count moved anywhere, including in `tests/docs/`, which is run because
round 4's test READS a file under `docs/`. There is no moved count to report as a
finding. The last invocation is the canary every handback owes.

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

NO PATH UNDER `docs/` MOVED. This round reads
`docs/agents/model_routing_policy.md` (through round 4's sync test) and writes it
never:

    $ git diff --stat 7a4d381f..0f4ece46 -- docs/
    (no output — NO path under docs/ is listed)
    REAL_EXIT=0

    $ git diff --stat 7a4d381f..0f4ece46
     .agent/authored/f110-r5.md                | 252 +++++++++++++++++++++
     .agent/last_block.md                      | 329 +++++++++++++--------------
     .agent/live_review.md                     |   4 +-
     .agent/plan.md                            |  35 ++--
     .agent/prose_slips.md                     |   4 +-
     packages/orchestration/model_routing.py   | 230 ++++++++++++++++++
     tests/orchestration/test_model_routing.py | 274 ++++++++++++++++++++-
     7 files changed, 939 insertions(+), 191 deletions(-)
    REAL_EXIT=0

Seven paths, all inside the change set. `.agent/handoff.md` is the eighth and is
written by this commit.

Insertion counts, the `+` column ONLY (AGENTS.md DECISION F104 D1), from
`git show --numstat`, compared CELL BY CELL against the Commits table above:

    step commit    path                                          numstat+   table+  agree
    C0a  98be993b  .agent/authored/f110-r5.md                         252      252    yes
    C0b  a31d97cc  .agent/last_block.md                               161      161    yes
    C1   9dabdd5a  .agent/plan.md                                      17       17    yes
    C2   939a31d8  .agent/live_review.md                                3        3    yes
    C2   939a31d8  .agent/prose_slips.md                                3        3    yes
    C3   e1c28478  packages/orchestration/model_routing.py            227      227    yes
    C4   7e2035fa  tests/orchestration/test_model_routing.py          273      273    yes

    every cell agrees: True

C4b `0f4ece46` is not in the block's ordered list; its own reading is
`5	2	packages/orchestration/model_routing.py`, stated in its Commits-table row
above and repeated here so the two agree.

Per-commit insertion totals: C0a 252, C0b 161, C1 17, C2 6, C3 227, C4 273,
C4b 5. Every one is far under the 500-insertion cap. C5's own numbers go to
NEITHER a round report NOR this file, per the block: the reviewer measures them at
the next gate.

**THE STALENESS SWEEP over every file this round touched, one entry per file.**

1. `.agent/authored/f110-r5.md` — NOT stale by construction. A verbatim copy of
   the reviewer's block; nothing in it is edited regardless of what any later
   measurement shows. Its G1 projection of 252 is exactly right, so there is not
   even a difference to leave standing.
2. `.agent/last_block.md` — NOT stale, same reason, same bytes, same digest.
3. `.agent/plan.md` — NOT stale. Its `## Current Step` describes exactly what this
   round did: the three named checks, the violating fixtures, and round 4's booked
   verdict — all of which landed. Its first Risk bullet states that the
   safety-class set is EMPTY in production and that the check is therefore proven
   against a fixture set; G5 and G6 both confirm it literally. `## Next Steps`
   names T002c first and says the checks this round ships are what that validation
   will call, which is true of the code as committed. 45 lines, under the AGENTS.md
   50-line rule. ONE CAVEAT, DECLARED IN D4: PLAN5 does not carry forward round
   4's Risk bullet about `mission_cmd.py`; the slice was applied as written and the
   item is restated in D5 instead so it is not lost.
4. `.agent/live_review.md` — NOT stale. One `Gate:` paragraph appended for round
   4's PASS; no registration or resolution line was written or edited. Measured at
   BASE and at HEAD with the SAME method: 347 registered, 69 resolved, 278 open at
   both, and the sets of ids added by this round are both EMPTY.
5. `.agent/prose_slips.md` — NOT stale. One dated record of a round 4 reviewer
   observation, true of round 4. Append-only, never renumbered, and nothing here
   gates anything.
6. `packages/orchestration/model_routing.py` — NOT stale, AND IT TOOK A REPAIR TO
   KEEP IT THAT WAY. Its opening sentence said "Owns the CLASS TABLE and nothing
   else yet", which C3 falsified within its own commit; C4b repaired it, and the
   docstring now names the class table AND the three hard rules and states what
   the module still does NOT do (no config file, no model id, no call site). Every
   other claim in it was checked against the code as committed: `MID_TIER` and
   `TOP_TIER` are both derived from `MODEL_TIERS` rather than re-spelled; the
   "unknown tier raises" claim is proved by G5 and by a test; the deliberate
   absence at `SAFETY_RELEVANT_CLASSES` describes the emptiness AND why the
   parameter exists; the new "tier means something else one module over" paragraph
   names `orchestrator_brain.py`'s vocabulary, which is the sentence the round 4
   verdict ruled for. "Nothing in production imports this module yet" is still
   true — nothing outside its own test imports it.
7. `tests/orchestration/test_model_routing.py` — NOT stale. Its header line named
   T002a only and now names T002a and T002b (the file's one deletion, D3). No
   rule-name string literal appears anywhere in it: every refusal assertion goes
   through the module's constant, so a rename breaks the import instead of leaving
   a dead assertion. The tier fixtures are derived from `MODEL_TIERS` and
   `model_tier_rank`, not written out, so adding a tier extends them rather than
   silently skipping it. The two literals it does pin by hand are the FIXTURE
   safety class names, which are fixture data and not production tokens.
8. `.agent/handoff.md` — this file; written once, per the write-once rule.

NOTHING OUTSIDE THE CHANGE SET WAS EDITED. Sentences outside it that this round
makes stale are DECLARED, NOT REPAIRED, per constraint 8 — see D5.

## Authored-text proofs

Every applied reviewer-authored text was extracted by delimiter index from the
COMMITTED `.agent/authored/f110-r5.md` (read with
`git show HEAD:.agent/authored/f110-r5.md`, not from the working copy) and written
to its target BY SCRIPT. Nothing was retyped.

| Authored text | Proof | Expected | Read | Exit |
|---|---|---|---|---|
| the whole block | `sha256sum` of `.agent/authored/f110-r5.md` and `.agent/last_block.md` | one digest twice | `57dc4b6e…616e` twice | 0 |
| the whole block | `wc -l .agent/authored/f110-r5.md` | projection 252 | 252 — exact, nothing to report | 0 |
| PLAN5 (45 lines, 2174 bytes) | `cmp .remedy-wt/f110r5/PLAN5.extracted .agent/plan.md` | identical | identical | 0 |
| RECORD4 (5941 bytes applied) | append arithmetic + paragraph-order second reader + negative control | exact / in order / rejected | exact / in order / rejected | — |
| SLIPS5 (978 bytes applied) | final-bytes byte-equality + exact byte prefix + newline convention | True / True / True | True / True / True | — |

The production code and the tests are NOT authored text: the block described them
and the worker wrote them (SPEC CODE, SPEC TESTS), so they carry no transport
proof and are gated by G5, G6 and G7 instead.

## Deviations & assumptions

**D0 — THE ORDERED COMMIT SEQUENCE WAS FOLLOWED, WITH ONE ADDITION.** C0a, C0b,
C1, C2, C3, C4, C5 ran in exactly that order, with exactly the eight paths the
change set names and nothing else. Nothing was dropped and nothing was reordered —
constraint 3's production-before-tests order was honoured. ONE EXTRA COMMIT, C4b,
was inserted between C4 and C5; it is described in D1 and appears in the Commits
table and the item-status table. It writes a path the change set already names,
so no write left the change set, but an extra commit is a departure from the
ordered bundle and is declared here as the handback template requires.

**D1 — WHY C4B EXISTS: C3 SHIPPED A SENTENCE C3 ITSELF MADE FALSE.** The module's
opening docstring read "Owns the CLASS TABLE and nothing else yet". After C3 the
module also owns the three hard rules, the rank helper and the validator, so that
sentence was false in the very commit that made it false, in the first paragraph a
reader lands on. Constraint 8 tells me to declare a stale sentence OUTSIDE the
change set and not repair it; this one is INSIDE the change set, on a path the
block names, so leaving it would have meant knowingly shipping a false claim in
production code — which is worse than an extra commit. I repaired it in its own
commit rather than folding it anywhere else, so the reviewer can see it separately
and drop it if it disagrees. THE REPAIR IS DOCSTRING PROSE ONLY: 5 insertions, 2
deletions, no executable line. I should have caught it before C3 was committed;
that is my miss, not the block's.

**D2 — I RAN G6 TWICE, AND THE SECOND RUN IS THE ONE THAT COUNTS.** The block
orders the red proof "at the C4 commit". C4b then changed the module, so a proof
pinned at C4 would no longer be a proof about the shipped bytes. I ran the ordered
proof at C4 (`7e2035fa`) AND repeated the whole thing — control plus all three
mutations plus all three reverts — in a second disposable worktree at C4b
(`0f4ece46`). The numbers and red-id sets are identical, which is expected given
the change is a docstring, but "expected" is not "measured" and the block's own
rule is that gates run rather than are assumed. Both worktrees were removed and
pruned; `git worktree list` shows neither.

**D3 — THE TEST FILE HAS ONE DELETION, WHICH THE BLOCK'S "ONLY GAINS CASES" DOES
NOT LITERALLY ALLOW.** SPEC TESTS says "Round 4's existing tests are not edited;
this file only gains cases." No test was edited: all 48 of round 4's tests are
byte-identical and all 48 still pass. The single deleted line is the file's first
docstring line, which said the file covers "F110 T002a, the class table" and now
says it covers T002a and T002b. I read "existing tests" as the tests, not the
file's header, and judged a header that omits half the file's contents to be the
same defect as D1 one file over. Declared rather than assumed.

**D4 — PLAN5 DROPS A RISK BULLET ROUND 4'S PLAN CARRIED, AND I APPLIED THE SLICE
AS WRITTEN.** Round 4's `.agent/plan.md` carried the Risk bullet
"`apps/cli/commands/mission_cmd.py`'s `_orchestrator_call_fn` docstring went
half-stale in round 3 and needs a later round's change set", and round 4's D3 said
the plan carried it "so it is not lost". PLAN5 does not carry it. Constraint 1
says to apply a slice byte for byte and declare anything that looks wrong, so I
did exactly that — the plan is `cmp`-identical to PLAN5 — and I am restating the
item in D5 so the loss is only from the plan file and not from the record.

**D5 — STALE SENTENCES OUTSIDE THE CHANGE SET, DECLARED AND NOT REPAIRED
(constraint 8).**
(i) `docs/agents/model_routing_policy.md`'s header reads "Seeds routing.py's
class→model map". Three things about it are now inexact: the module is
`model_routing.py`, not `routing.py`; the seeded map is class→TIER, not
class→model; and as of this round the document does not merely SEED the module,
it is ENFORCED by it. Round 4 declared the first two; this round makes the third
true as well. The document is READ by the sync test and the block says twice that
no doc is edited, so it is left alone and needs a path in a later change set.
(ii) The same document's "Hard rules" section numbers three rules, but the code
now enforces three checks of which only TWO come from that list — the
orchestration rule comes from `docs/roadmap/features/T3_F110.md`'s Design section,
and the document's own rule 3 (evidence) is not a routing refusal at all. The
mapping table in the State section above is the reconciliation. Nothing here is
false, but a reader who diffs `HARD_RULE_NAMES` against the document's numbered
list will find a mismatch, and the document is where the explanation belongs.
(iii) `docs/roadmap/features/T3_F110.md`'s "Do not touch" section still suggests
`tests/orchestration/test_routing.py`; the file that exists is
`tests/orchestration/test_model_routing.py`, named after the source it covers per
AGENTS.md Code Discoverability. Round 4's D3, unchanged.
(iv) STILL OPEN FROM EARLIER ROUNDS, restated so they are not lost:
`apps/cli/commands/mission_cmd.py`'s `_orchestrator_call_fn` docstring,
`packages/orchestration/intake.py`'s docstring, and `.agent/f110_inventory.md`
section E — all declared by round 3, all still outside a change set. The first of
these was carried by round 4's plan and is no longer carried by round 5's (D4).

**D6 — SEMANTIC CHOICES THE SPEC LEFT OPEN, ALL DECLARED.**
(i) THE RULE-NAME TOKENS. SPEC CODE (b) says to name them for what they FORBID, so
they are `reviewer_weaker_than_worker`, `orchestration_below_top_tier` and
`safety_class_below_mid_tier` — each reads as the thing that is wrong, which is
what an operator sees in a refusal.
(ii) `MID_TIER` is derived as `MODEL_TIERS[len(MODEL_TIERS) // 2]`, not as the
literal and not as index 1, so the derivation still means "the middle one" if the
vocabulary ever grows. On today's three-tier tuple it answers `'mid'` (G5).
(iii) THE ORCHESTRATION CLASS SET. The feature file names "orchestrator and
mission-compile calls", so `ORCHESTRATION_TASK_CLASSES` is exactly
`{normalize_task_class("orchestrator"), normalize_task_class("mission compile")}`
= `{'orchestrator', 'mission_compile'}`, and a test asserts that. Note that
`mission` (which the seed table already routes to top) is NOT in this set:
"mission" and "mission compile" are different declared classes and I did not
merge them on my own authority. If the reviewer wants `mission` covered by the
rule as well, that is a one-line change and I would rather be told than guess.
(iv) ONLY THE SAFETY CHECK TAKES ITS CLASS SET AS A PARAMETER. SPEC CODE (c)
orders it there, and the reason is vacuity: that set is empty. The orchestration
set is non-empty, so its check reads the module constant directly and its tests
still see it refuse. The asymmetry is deliberate; if the reviewer prefers symmetry
I will make both parameters.
(v) THE VALIDATOR'S SIGNATURE. `paired_worker_tier` defaults to `None`, meaning
"this choice is not a reviewer call, so hard rule 1 has nothing to compare". That
is the only way one function can validate both reviewer and non-reviewer choices
without inventing a worker tier, and a test pins it.
(vi) THE VALIDATOR REPORTS WHAT THE CHECKS RETURNED, not a label it attached: it
collects the returned values into a set and filters `HARD_RULE_NAMES` by
membership. That is why a check that stops refusing drops out of the result — and
it is what makes G6's three mutations visible in the validator case.
(vii) AN UNKNOWN TIER RAISES from inside the checks too, because they rank through
`model_tier_rank`; two tests pin that, so a typo in a future config cannot read as
a pass.

**D7 — ROUND 4'S OPEN-SET DISAGREEMENT (its D4) IS RESOLVED, AND THE REVIEWER WAS
RIGHT.** Round 4's worker read 65 resolved / 282 open with its own heuristic; the
round 4 verdict recomputed under five readings and pinned 347 / 69 / 278 with the
FIRST-R-id-per-`Done:`-line reading as canonical. I implemented that canonical
reading and ran it at BASE and at HEAD: 347 registered, 69 resolved across 71
`Done:` lines, 278 open, no resolved id that is not also registered, at BOTH
revisions. It reproduces the verdict's figure exactly. The ids registered by this
round: none. The ids resolved by this round: none. Open-set delta: 0. THE FIGURE
IS 278 and I am now stating it as my own measurement rather than declining to.

**D8 — NO RUFF GATE WAS ORDERED AND I ADDED NONE**, per constraint 5. I say
nothing about lint in the code, the commits or the tests; the reviewer lints C3,
C4 and C4b itself. For what it is worth to that lint: `pyproject.toml` selects
`E`, `F`, `W`, `I`, `UP` with `E501` ignored and `line-length = 120`, and the new
import block in the test file is in the ASCII order isort produces.

**D9 — REPORTED VALUES THE BLOCK DID NOT ORDER, ADDED BECAUSE THEY BOUND A
CLAIM.** (i) G3's arithmetic is additionally re-read from the git object at
`939a31d8^`, so the "before" size is not a remembered number. (ii) G3's negative
control additionally reports that the mutated copy still matches on LENGTH
(5912 vs 5912 characters) — without that line, "the second reader rejects it"
could be a size check wearing a content check's name. (iii) G6 additionally
reports the per-mutation red-id COUNT split into own-fixture / validator /
other-rules, computed by the script, because "the discriminator holds" is a claim
about three sets and should be shown as three sets. (iv) G5 additionally reports
what the safety check returns under the PRODUCTION default — `None` for an input
that violates the rule — because that is the vacuity and hiding it would be the
one thing this round exists to avoid.

**D10 — THE SCRATCH IS LEFT IN PLACE UNDER `.remedy-wt/f110r5/`.** The extractor,
the mirror, the append and second-reader scripts, the negative control, the module
probe, the G6 driver, the G8 cell comparison and the open-set script, plus the
extracted slices and the mutated ledger copy. All of it is gitignored,
`git ls-files .remedy-wt` returns nothing, and nothing was deleted by glob. It is
left deliberately so the reviewer can re-run every gate from the same inputs. The
two G6 worktrees, by contrast, WERE removed and pruned.

**Assumptions.** (i) The block's statement that the reviewer holds no scratch
original is taken at face value, so G1 is reported as self-consistency and not as
transport — the weaker claim, on purpose. (ii) "A candidate routing choice" in
SPEC CODE (e) is read as (task class, routed tier, optionally the paired worker's
tier), because those are the values the three rules judge and constraint 6 forbids
reading a config. (iii) "MODEL_TIERS-independent, stable order" is read as: the
order is a declared tuple constant, not derived from the tier vocabulary — so
re-tiering cannot reshuffle it; a test asserts the result is in that order and not
in alphabetical order. (iv) `.remedy-wt/` is gitignored session scratch that
PERSISTS, which is what makes D10's decision to leave it the right one.
(v) Constraint 7 was verified by MEASUREMENT and not by reading: C3's numstat
deletions column is 0, and round 4's 48 tests were re-run green against the
extended module before C3 was committed.

## Next

REVIEW ROUND 5 AND ISSUE A VERDICT — lint `e1c28478`, `7e2035fa` and `0f4ece46`
reviewer-side, since constraint 5 routes lint to the reviewer; re-run all three of
G6's mutations; and rule on D1 (the extra commit C4b), D3 (the test file's one
deletion) and D6 (iii) (whether the class `mission` should join
`ORCHESTRATION_TASK_CLASSES`).

THIS IS THE LAST ROUND OF SESSION 1. THE NEXT ROUND IS T002c: the config schema
and per-project overrides, where the hard rules always win and a violating
override fails validation NAMING THE RULE — `validate_routing_choice` is the
function that validation calls, and it already returns every violated rule name at
once.

THE BRANCH HAS NO OPEN PULL REQUEST. None was created this round or in any
earlier round of F110, so the next session's Open PR Gate finds none and proceeds
normally. The next session's FIRST action is Phase 1 rule 1 — read `.agent/STOP`
from disk — BEFORE Phase 1 rule 2, the Open PR Gate.
